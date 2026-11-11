# Day 8 Lab Log

Date: 2026-11-11

**Answer:** A skill is a small, testable action with a fixed input and output (like check_supplier or validate_invoice), while an agent is the layer that decides which skills to call, applies the auto-versus-human rules, and logs every decision; today the MCP tool was the skill and the pipeline that sent 3 invoices to the clean summary and 2 to the exception list was the agent.

## Evidence

| Category | Example | File | What it does |
|---|---|---|---|
| Skill | `check_supplier(name)` | agent_core.py (line 37) | Returns good / poor / new / unknown for a supplier |
| Skill | `create_po(...)` | agent_core.py (line 49) | Writes one PO record to po_created.json; never touches a real system |
| Skill | `route_to_manager(...)` | agent_core.py (line 61) | Adds one item to manager_queue.json |
| Skill | `validate_invoice(invoice, seen)` | inv_tools.py (line 24), exposed as an MCP tool in inv_mcp_server.py (line 9) | Read-only check of one invoice against the PO master; returns clean or exception with reasons |
| Agent | Requisition decision logic `decide(req)` | agent_core.py (line 72) | Applies Rule 1 (supplier), Rule 2 (amount above Rs 25 lakh), Rule 3 (auto PO); calls the skills and logs each decision |
| Agent | Invoice pipeline `main()` | inv_pipeline.py (line 215) | Calls the MCP tool for every invoice, falls back to a direct call if MCP fails, writes the audit log with posted=false |
| Agent | `suggest_action(reasons)` | inv_pipeline.py (line 90) | Maps each exception reason to a suggested human action |

### Results seen in the files

| Check | Value | Source |
|---|---|---|
| Invoices CLEAN | 3 (INV-1001, INV-1002, INV-1003) | inv_e2e_report.md, inv_clean_summary.md (`Count: 3`) |
| Invoices EXCEPTION | 2 (INV-1004, INV-1005) | inv_e2e_report.md |
| Test summary line | `Ran 16 tests in 0.005s` followed by `OK` | inv_test_results.txt |
| Validated via | `MCP tool (inv_mcp_server.py)` on all 5 audit entries | inv_audit_log.json |
| Posted | `false` on all 5 entries; nothing posted | inv_audit_log.json |
| Requisition agent | 3 POs created (PR1, PR2, PR3), 2 sent to manager (PR4, PR5) | output.md |
