"""Requisition agent: deterministic rules + manager gate. Writes only local JSON files."""
import csv, json, os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
LIMIT = 2_500_000  # Rs 25 lakh; exactly 2,500,000 is NOT above the limit
OUTPUTS = ("po_created.json", "manager_queue.json", "decision_log.json")


def _path(name, base=None):
    return os.path.join(base or BASE, name)


def _read(name, base=None):
    p = _path(name, base)
    if not os.path.exists(p):
        return []
    with open(p) as f:
        return json.load(f)


def _append(name, record, base=None):
    data = _read(name, base)
    data.append(record)
    with open(_path(name, base), "w") as f:
        json.dump(data, f, indent=2)


def reset(base=None):
    for n in OUTPUTS:
        p = _path(n, base)
        if os.path.exists(p):
            os.remove(p)


# ---- the three tools (also exposed through mcp_server.py) ----
def check_supplier(name, base=None):
    """Returns 'good' | 'poor' | 'new' | 'unknown' (file unreadable)."""
    try:
        with open(_path("suppliers.csv", base), newline="") as f:
            for row in csv.reader(f):
                if len(row) >= 2 and row[0].strip().lower() == name.strip().lower():
                    return row[1].strip().lower()
    except FileNotFoundError:
        return "unknown"
    return "new"  # supplier not in the list is treated as new


def create_po(requisition_id, supplier, amount, base=None):
    """Writes ONLY to po_created.json. Never touches a real system. Idempotent."""
    existing = _read("po_created.json", base)
    if any(r["requisition_id"] == requisition_id for r in existing):
        return {"status": "duplicate_ignored", "requisition_id": requisition_id}
    po = {"po_number": f"PO-{len(existing) + 1:04d}", "requisition_id": requisition_id,
          "supplier": supplier, "amount": amount,
          "created_at": datetime.now().isoformat(timespec="seconds")}
    _append("po_created.json", po, base)
    return po


def route_to_manager(requisition_id, reason, base=None):
    existing = _read("manager_queue.json", base)
    if any(r["requisition_id"] == requisition_id for r in existing):
        return {"status": "duplicate_ignored", "requisition_id": requisition_id}
    item = {"requisition_id": requisition_id, "reason": reason, "status": "awaiting manager",
            "routed_at": datetime.now().isoformat(timespec="seconds")}
    _append("manager_queue.json", item, base)
    return item


# ---- the decision logic ----
def decide(req, base=None):
    status = check_supplier(req["supplier"], base)
    reasons, rules = [], []
    if status != "good":
        rules.append("Rule 1")
        reasons.append({"new": "New supplier", "poor": "Poor supplier"}.get(
            status, "Supplier status could not be verified"))
    if req["amount"] > LIMIT:
        rules.append("Rule 2")
        reasons.append("Amount above Rs 25 lakh threshold")

    if reasons:
        decision, reason = "Sent to manager", "; ".join(reasons)
        route_to_manager(req["id"], reason, base)
    else:
        rules.append("Rule 3")
        decision, reason = "PO created", "Good supplier, within Rs 25 lakh limit"
        create_po(req["id"], req["supplier"], req["amount"], base)

    entry = {"timestamp": datetime.now().isoformat(timespec="seconds"),
             "requisition_id": req["id"], "supplier": req["supplier"],
             "amount": req["amount"], "supplier_status": status,
             "rule_triggered": " + ".join(rules), "decision": decision, "reason": reason}
    _append("decision_log.json", entry, base)
    return entry


def process_all(base=None):
    reset(base)
    with open(_path("requisitions.json", base)) as f:
        reqs = json.load(f)
    return [decide(r, base) for r in reqs]
