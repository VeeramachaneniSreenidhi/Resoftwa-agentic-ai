import json
from datetime import datetime

AUDIT_FILE = "audit.jsonl"
POS_FILE = "pos.json"

def log_audit(tool_name, inputs, result):
    """Writes every tool call to an immutable audit trail."""
    record = {
        "timestamp": datetime.now().isoformat(),
        "tool": tool_name,
        "inputs": inputs,
        "result": result
    }
    with open(AUDIT_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")

def list_open_pos():
    with open(POS_FILE, "r") as f:
        data = json.load(f)
    log_audit("list_open_pos", {}, data)
    return data

def get_po_status(po_number):
    with open(POS_FILE, "r") as f:
        data = json.load(f)
    po = next((item for item in data if item["po_number"] == str(po_number)), None)
    result = po if po else {"error": "PO not found"}
    log_audit("get_po_status", {"po_number": po_number}, result)
    return result

def draft_email(vendor, text):
    draft = {"vendor": vendor, "email_text": text, "status": "DRAFTED"}
    log_audit("draft_email", {"vendor": vendor, "text": text}, draft)
    return draft

def send_email(draft_id):
    print(f"\n[GUARDRAIL SECURITY CHECK] Agent wants to execute: send_email for draft ID: {draft_id}")
    approval = input("Authorize this send action? (y/n): ").strip().lower()
    
    if approval == 'y':
        result = {"status": "SUCCESS", "message": f"Email {draft_id} sent successfully."}
    else:
        result = {"status": "BLOCKED", "message": "Human operator denied permission to send email."}
        
    log_audit("send_email", {"draft_id": draft_id}, result)
    return result

TOOLS = [
    {
        "name": "list_open_pos",
        "description": "List all open purchase orders.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "get_po_status",
        "description": "Get detailed status for a specific PO number.",
        "input_schema": {
            "type": "object",
            "properties": {"po_number": {"type": "string", "description": "The PO number"}},
            "required": ["po_number"]
        }
    },
    {
        "name": "draft_email",
        "description": "Draft a reminder email to a vendor.",
        "input_schema": {
            "type": "object",
            "properties": {
                "vendor": {"type": "string"},
                "text": {"type": "string"}
            },
            "required": ["vendor", "text"]
        }
    },
    {
        "name": "send_email",
        "description": "Send a drafted email (requires human approval).",
        "input_schema": {
            "type": "object",
            "properties": {"draft_id": {"type": "string"}},
            "required": ["draft_id"]
        }
    }
]

def run_tool(name, inputs):
    if name == "list_open_pos":
        return list_open_pos()
    elif name == "get_po_status":
        return get_po_status(**inputs)
    elif name == "draft_email":
        return draft_email(**inputs)
    elif name == "send_email":
        return send_email(**inputs)
    else:
        return {"error": f"Unknown tool: {name}"}