# Day 8: Requisition Agent Output

| Req ID | Supplier | Amount (INR) | Supplier status | Decision | Reason |
|---|---|---|---|---|---|
| PR1 | Sharma Steels | 450,000 | good | PO created | Good supplier, within Rs 25 lakh limit |
| PR2 | Vizag Paints | 120,000 | good | PO created | Good supplier, within Rs 25 lakh limit |
| PR3 | Guntur Cables | 980,000 | good | PO created | Good supplier, within Rs 25 lakh limit |
| PR4 | New Vendor Co | 60,000 | new | Sent to manager | New supplier |
| PR5 | Sharma Steels | 3,200,000 | good | Sent to manager | Amount above Rs 25 lakh threshold |

**Result: 3 auto-created POs, 2 sent to the manager.**

Files written: po_created.json, manager_queue.json, decision_log.json
