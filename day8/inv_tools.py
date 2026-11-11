"""Invoice validation rules. Read-only: this module never posts anything.
Shared by the MCP server (inv_mcp_server.py) and the pipeline (inv_pipeline.py)."""
import csv, os

BASE = os.path.dirname(os.path.abspath(__file__))
TOLERANCE = 0.02   # invoice net may exceed the PO amount by up to 2%
ROUNDING = 1.0     # allowed Rs difference in net + tax = total
REQUIRED = ["invoice_no", "vendor", "po_number", "invoice_date",
            "net_amount", "tax_amount", "total_amount"]


def load_pos(base=None):
    with open(os.path.join(base or BASE, "inv_po_master.csv"), newline="", encoding="utf-8") as f:
        return {r["po_number"].strip().upper(): r for r in csv.DictReader(f)}


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def validate_invoice(invoice, seen_invoice_nos=None, base=None):
    """Return {invoice_no, status: clean|exception, reasons[], po_amount, po_vendor, variance_pct}."""
    seen = {str(s).strip().upper() for s in (seen_invoice_nos or [])}
    inv_no = str(invoice.get("invoice_no") or "").strip()
    result = {"invoice_no": inv_no or "(missing)", "status": "exception", "reasons": [],
              "po_amount": None, "po_vendor": None, "variance_pct": None}
    reasons = result["reasons"]

    # 1. completeness: cannot validate further without the fields, so stop
    missing = [k for k in REQUIRED if invoice.get(k) in (None, "")]
    if missing:
        reasons += [f"Missing required field: {k}" for k in missing]
        return result

    # 2. duplicate invoice number
    if inv_no.upper() in seen:
        reasons.append(f"Duplicate invoice number {inv_no}")

    # 3. amounts and tax arithmetic
    net, tax, total = (_num(invoice[k]) for k in ("net_amount", "tax_amount", "total_amount"))
    if None in (net, tax, total):
        reasons.append("Amount is not a number")
        return result
    if abs(net + tax - total) > ROUNDING:
        reasons.append(f"Total {total:,.0f} does not equal net + tax ({net + tax:,.0f})")

    # 4. PO checks (fail-safe: an unreadable PO master is an exception, never a pass)
    try:
        pos = load_pos(base)
    except OSError as e:
        reasons.append(f"PO master unavailable, cannot validate ({e.__class__.__name__})")
        return result
    po_no = str(invoice["po_number"]).strip().upper()
    po = pos.get(po_no)
    if po is None:
        reasons.append(f"PO not found: {po_no}")
    else:
        po_amt = float(po["po_amount"])
        result["po_amount"], result["po_vendor"] = po_amt, po["vendor"]
        result["variance_pct"] = round((net - po_amt) / po_amt * 100, 2)
        if po["status"].strip().lower() != "open":
            reasons.append(f"PO {po_no} is {po['status']}, not open")
        if str(invoice["vendor"]).strip().lower() != po["vendor"].strip().lower():
            reasons.append(f"Vendor mismatch: invoice says '{invoice['vendor']}', "
                           f"PO belongs to '{po['vendor']}'")
        if net > round(po_amt * (1 + TOLERANCE), 2):
            reasons.append(f"Net amount {net:,.0f} exceeds PO amount {po_amt:,.0f} by "
                           f"{result['variance_pct']:.1f}% (tolerance {TOLERANCE * 100:.0f}%)")

    if not reasons:
        result["status"] = "clean"
    return result
