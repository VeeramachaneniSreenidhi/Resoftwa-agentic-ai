# Invoice end-to-end report

Generated: 2026-11-11T10:49:52+00:00

Validation path: MCP tool (inv_mcp_server.py)

| Invoice | Vendor | PO | Total (INR) | Status | Reasons |
|---|---|---|---|---|---|
| INV-1001 | Sharma Steels | PO-4501 | 531,000 | CLEAN | None |
| INV-1002 | Vizag Paints | PO-4502 | 141,600 | CLEAN | None |
| INV-1003 | Guntur Cables | PO-4503 | 1,162,300 | CLEAN | None |
| INV-1004 | New Vendor Co | PO-4599 | 70,800 | EXCEPTION | PO not found: PO-4599 |
| INV-1005 | Sharma Steels | PO-4501 | 3,776,000 | EXCEPTION | Net amount 3,200,000 exceeds PO amount 450,000 by 611.1% (tolerance 2%) |

**Result: 3 CLEAN, 2 EXCEPTION. Nothing was posted; clean invoices await human approval.**
