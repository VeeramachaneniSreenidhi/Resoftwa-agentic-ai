import json
from datetime import datetime

def log_audit_event(action: str, details: dict):
    """Writes every action/tool call to audit.jsonl immediately."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "details": details
    }
    with open("audit.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def read_system_data(record_id: str):
    """Read-only tool to fetch dummy data."""
    log_audit_event("tool_call", {"tool": "read_system_data", "record_id": record_id})
    mock_db = {"404": {"client": "Acme Corp", "email": "contact@acme.com"}}
    return mock_db.get(record_id, "Record not found")

def send_email(recipient: str, body: str):
    """Gated tool requiring human permission (y/n) before sending."""
    print(f"\n========================================")
    print(f"  [SECURITY GATE] EMAIL OUTBOUND PENDING")
    print(f"========================================")
    print(f"To   : {recipient}")
    print(f"Body : {body}")
    print(f"----------------------------------------")
    
    # Human-in-the-loop prompt in the BAS terminal
    choice = input("Do you approve sending this email? (y/n): ").strip().lower()
    
    if choice == 'y':
        log_audit_event("send_email_decision", {"status": "approved", "recipient": recipient})
        print("✅ Email sent successfully.")
        return "Sent"
    else:
        log_audit_event("send_email_decision", {"status": "refused", "recipient": recipient})
        print("❌ Email sending REFUSED by human operator.")
        return "Refused"

def run_agent():
    max_steps = 10
    current_step = 0
    
    print("🤖 Agent execution started...")
    log_audit_event("agent_start", {"max_steps": max_steps})
    
    while current_step < max_steps:
        current_step += 1
        print(f"\n[Step {current_step}/{max_steps}] Agent thinking...")
        
        # Simulating agent tool selection steps for the test
        if current_step == 1:
            read_system_data("404")
        elif current_step == 2:
            result = send_email("contact@acme.com", "Hello, here is your requested report.")
            if result == "Refused":
                print("🛑 Agent halting execution due to human refusal.")
                break
        
    print("\n🏁 Agent run finished.")

if __name__ == "__main__":
    run_agent()
    