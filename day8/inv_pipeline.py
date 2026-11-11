"""Invoice validation pipeline: validates invoices.json and writes the audit and report files.

NEVER POSTS. There is no posting code in this file; every audit entry has posted=false
and a human must approve each clean invoice before anything is posted.

Validation goes through the MCP tool `validate_invoice` in inv_mcp_server.py (stdio).
If the MCP server cannot be used, the pipeline prints a WARNING and calls inv_tools directly.
"""
import asyncio
import csv
import json
import os
import sys
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
import inv_tools  # shared rules: the same module the MCP server uses

MCP_VIA = "MCP tool (inv_mcp_server.py)"
DIRECT_VIA = "direct call (MCP not used)"


def warn(msg):
    print(f"WARNING: {msg}")


def load_invoices():
    with open(os.path.join(BASE, "invoices.json"), encoding="utf-8") as f:
        return json.load(f)


def _parse_tool_result(res):
    """Turn an MCP CallToolResult into the validation dict."""
    if res.isError:
        text = " ".join(getattr(c, "text", "") for c in res.content)
        raise RuntimeError(f"tool returned error: {text}")
    sc = getattr(res, "structuredContent", None)
    if isinstance(sc, dict):
        if "invoice_no" in sc:
            return sc
        if isinstance(sc.get("result"), dict):
            return sc["result"]
    return json.loads("".join(getattr(c, "text", "") for c in res.content))


async def validate_all_via_mcp(invoices):
    """Validate all invoices in order over one MCP stdio session.
    A single failed call falls back to a direct call for that invoice only.
    Raises if the session itself cannot start (caller falls back for the whole batch)."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(
        command=sys.executable,
        args=[os.path.join(BASE, "inv_mcp_server.py")],
        cwd=BASE,
    )
    out = []
    seen = []
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            for inv in invoices:
                label = str(inv.get("invoice_no", "(missing)"))
                try:
                    res = await session.call_tool(
                        "validate_invoice",
                        {"invoice": inv, "seen_invoice_nos": list(seen)},
                    )
                    r, via = _parse_tool_result(res), MCP_VIA
                except Exception as e:  # per-call fallback
                    warn(f"MCP call failed for {label} ({type(e).__name__}: {e}); "
                         f"using direct call for this invoice")
                    r, via = inv_tools.validate_invoice(inv, seen), DIRECT_VIA
                out.append((r, via))
                if str(inv.get("invoice_no", "")).strip():
                    seen.append(str(inv["invoice_no"]).strip())
    return out


def validate_all_direct(invoices):
    out, seen = [], []
    for inv in invoices:
        out.append((inv_tools.validate_invoice(inv, seen), DIRECT_VIA))
        if str(inv.get("invoice_no", "")).strip():
            seen.append(str(inv["invoice_no"]).strip())
    return out


def suggest_action(reasons):
    """Map validation reasons to a suggested human action."""
    actions = []
    for r in reasons:
        if r.startswith("PO not found"):
            actions.append("Confirm the PO number with the requester; get a valid PO or reject the invoice")
        elif r.startswith("Net amount") and "exceeds PO" in r:
            actions.append("Do not pay the excess; ask vendor for a credit note or requester for a PO amendment")
        elif r.startswith("Duplicate"):
            actions.append("Check for double submission; reject the duplicate")
        elif r.startswith("Vendor mismatch"):
            actions.append("Verify vendor and bank details against the vendor master; confirm the PO vendor")
        elif "is closed" in r or "not open" in r:
            actions.append("Confirm whether the PO should be reopened; otherwise return the invoice")
        elif r.startswith("Missing required field"):
            actions.append("Return to vendor for a complete invoice")
        elif r.startswith("Total ") or r.startswith("Amount is not a number"):
            actions.append("Ask vendor to correct the amounts or tax and resubmit")
        elif r.startswith("PO master unavailable"):
            actions.append("Restore inv_po_master.csv and rerun the pipeline")
        else:
            actions.append("Review manually")
    return "; ".join(dict.fromkeys(actions)) or "None (clean)"


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _money(v):
    n = _num(v)
    return f"{n:,.0f}" if n is not None else str(v)


def build_entry(inv, r, via, ts):
    clean = r["status"] == "clean"
    next_step = ("Ready for human AP approval; NOT posted" if clean
                 else "Hold; resolve exception: " + suggest_action(r["reasons"]) + "; NOT posted")
    return {
        "timestamp": ts,
        "invoice_no": r["invoice_no"],
        "vendor": inv.get("vendor"),
        "po_number": inv.get("po_number"),
        "total_amount": inv.get("total_amount"),
        "status": r["status"],
        "reasons": r["reasons"],
        "validated_via": via,
        "next_step": next_step,
        "posted": False,
    }


def write_files(invoices, results, ts):
    entries = [build_entry(inv, r, via, ts) for inv, (r, via) in zip(invoices, results)]
    clean = [(inv, r) for inv, (r, _) in zip(invoices, results) if r["status"] == "clean"]
    exc = [(inv, r) for inv, (r, _) in zip(invoices, results) if r["status"] != "clean"]
    total_clean = sum(_num(inv.get("total_amount")) or 0 for inv, _ in clean)
    vias = sorted({via for _, via in results})

    with open(os.path.join(BASE, "inv_audit_log.json"), "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    # clean summary
    lines = [
        "# Clean invoices", "",
        f"Generated: {ts}", "",
        f"- Count: {len(clean)}",
        f"- Total value (INR): {total_clean:,.0f}", "",
        "| Invoice | Vendor | PO | Total (INR) | Variance vs PO % |",
        "|---|---|---|---|---|",
    ]
    for inv, r in clean:
        var = "" if r["variance_pct"] is None else f"{r['variance_pct']:+.2f}"
        lines.append(f"| {r['invoice_no']} | {inv.get('vendor')} | {inv.get('po_number')} | "
                     f"{_money(inv.get('total_amount'))} | {var} |")
    lines += ["", "**Nothing has been posted.** A human must review and approve each invoice above before it is posted.", ""]
    with open(os.path.join(BASE, "inv_clean_summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # exceptions md + csv
    rows = []
    for inv, r in exc:
        rows.append({
            "invoice": r["invoice_no"], "vendor": inv.get("vendor"), "PO": inv.get("po_number"),
            "total": inv.get("total_amount"), "reasons": "; ".join(r["reasons"]),
            "suggested_action": suggest_action(r["reasons"]),
        })
    md = ["# Exceptions", "", f"Generated: {ts}", "", f"Count: {len(exc)}", ""]
    if rows:
        md += ["| Invoice | Vendor | PO | Total (INR) | Reasons | Suggested action |",
               "|---|---|---|---|---|---|"]
        for x in rows:
            md.append(f"| {x['invoice']} | {x['vendor']} | {x['PO']} | {_money(x['total'])} | "
                      f"{x['reasons']} | {x['suggested_action']} |")
    else:
        md.append("No exceptions.")
    md += ["", "Nothing has been posted.", ""]
    with open(os.path.join(BASE, "inv_exceptions.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    with open(os.path.join(BASE, "inv_exceptions.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["invoice", "vendor", "PO", "total", "reasons", "suggested_action"])
        w.writeheader()
        w.writerows(rows)

    # end-to-end report
    report = ["# Invoice end-to-end report", "", f"Generated: {ts}", "",
              f"Validation path: {', '.join(vias)}", "",
              "| Invoice | Vendor | PO | Total (INR) | Status | Reasons |",
              "|---|---|---|---|---|---|"]
    for inv, (r, _) in zip(invoices, results):
        status = r["status"].upper()
        reasons = "; ".join(r["reasons"]) or "None"
        report.append(f"| {r['invoice_no']} | {inv.get('vendor')} | {inv.get('po_number')} | "
                      f"{_money(inv.get('total_amount'))} | {status} | {reasons} |")
    report += ["", f"**Result: {len(clean)} CLEAN, {len(exc)} EXCEPTION. "
                   f"Nothing was posted; clean invoices await human approval.**", ""]
    text = "\n".join(report)
    with open(os.path.join(BASE, "inv_e2e_report.md"), "w", encoding="utf-8") as f:
        f.write(text)
    return text


def main():
    invoices = load_invoices()
    try:
        results = asyncio.run(validate_all_via_mcp(invoices))
    except Exception as e:
        warn(f"MCP validation unavailable ({type(e).__name__}: {e}); "
             f"validating all invoices with direct call (MCP not used)")
        results = validate_all_direct(invoices)
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    text = write_files(invoices, results, ts)
    print(text)
    print("Files written: inv_audit_log.json, inv_clean_summary.md, inv_exceptions.md, "
          "inv_exceptions.csv, inv_e2e_report.md")


if __name__ == "__main__":
    main()
