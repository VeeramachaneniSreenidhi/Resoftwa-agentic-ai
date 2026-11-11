# Invoice validator: Claude Code setup and reusable prompt

## 1. Register the MCP tool with Claude Code

Requires `pip install mcp`. Run from any directory; the path points at the server file:

```bash
claude mcp add invoice-validator -- python3 /home/user/projects/project2/day8/inv_mcp_server.py
```

Check it is registered:

```bash
claude mcp list
```

The server exposes one tool, `validate_invoice(invoice, seen_invoice_nos)`. It is read-only and never posts.

## 2. Reusable agent prompt

Paste this into Claude Code (or use it as a subagent prompt) after the server is registered:

```text
You are validating supplier invoices with the invoice-validator MCP tool (validate_invoice).

Rules:
- Read the invoices from /home/user/projects/project2/day8/invoices.json, in file order.
- For each invoice, call validate_invoice with:
    invoice = the invoice object as-is
    seen_invoice_nos = the invoice_no values of all invoices already validated in this run
- Never post, pay, approve, or modify any invoice or file. The tool is read-only; do not
  try to work around it by reading the PO master and deciding yourself.
- If the tool is unavailable, say so clearly and stop. Do not guess a result.

Report, as a markdown table, one row per invoice:
  Invoice | Vendor | PO | Total | Status (CLEAN or EXCEPTION) | Reasons | Suggested human action

Finish with one line: "N CLEAN, M EXCEPTION. Nothing posted; clean invoices need human approval."
```

## 3. Expected results for the sample data

| Invoice  | Expected | Reason |
|----------|----------|--------|
| INV-1001 | CLEAN | PO-4501 matches, within tolerance |
| INV-1002 | CLEAN | PO-4502 matches |
| INV-1003 | CLEAN | net 985000 vs PO 980000 (+0.51%, within 2%) |
| INV-1004 | EXCEPTION | PO not found: PO-4599 |
| INV-1005 | EXCEPTION | net 3200000 exceeds PO-4501 amount 450000 |
