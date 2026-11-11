import os
import agent_core as core

entries = core.process_all()
lines = ["# Day 8: Requisition Agent Output", "",
         "| Req ID | Supplier | Amount (INR) | Supplier status | Decision | Reason |",
         "|---|---|---|---|---|---|"]
for e in entries:
    lines.append(f"| {e['requisition_id']} | {e['supplier']} | {e['amount']:,} | "
                 f"{e['supplier_status']} | {e['decision']} | {e['reason']} |")
auto = sum(e["decision"] == "PO created" for e in entries)
lines += ["", f"**Result: {auto} auto-created POs, {len(entries) - auto} sent to the manager.**",
          "", "Files written: po_created.json, manager_queue.json, decision_log.json"]
text = "\n".join(lines)
with open(os.path.join(core.BASE, "output.md"), "w") as f:
    f.write(text + "\n")
print(text)
