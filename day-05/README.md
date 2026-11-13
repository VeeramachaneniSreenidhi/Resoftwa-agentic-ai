## Application Details & Capstone Overview
| | |
| ------------- | ------------- |
|**Project Name**<br>Capstone 1: Autonomous Procurement Agent Loop & Guardrails |
|**Phase**<br>Phase 5 - Agentic AI & Apps (Day 5 Capstone) |
|**Environment**<br>SAP Business Application Studio (BAS) |
|**Core Components**<br>`tools.py`, `agent.py`, `audit.jsonl`, `pos.json` |

---

## The 5 Production-Ready Prompts

1. **Intent & Data Extractor:** Parses incoming unstructured text or raw vendor emails into clean, structured JSON entities (`po_number`, `vendor_name`, `due_date`, `delivered_qty`, `total_qty`).
2. **Open PO & Lateness Analyzer:** Compares current execution dates against due dates to flag overdue items and calculate fulfillment ratios.
3. **Vendor Communication Drafter:** Drafts professional, polite reminder emails for vendors with overdue purchase orders without auto-sending.
4. **Guardrail & Safety Validator:** Scans proposed tool inputs and agent actions for prompt injection attempts, unauthorized policy overrides, or unapproved data transmissions.
5. **Agent Loop Orchestrator & Summary Writer:** Reviews the execution trace (`audit.jsonl`) to summarize final operations, tool calls, and exceptions across the 10-step loop.

---

## Failure Notes & Iteration Log

* **Hallucination on Missing Dates:** 
  * *Issue:* Early prompt versions guessed delivery dates when legacy records had `null` values.
  * *Fix:* Added strict negative constraints telling the model to return `null` and implemented a code-level dataset validation check.
* **Markdown Formatting Breaks:** 
  * *Issue:* Claude occasionally wrapped JSON outputs in markdown code blocks (` ```json ... ``` `), causing Python parsing errors.
  * *Fix:* Enforced explicit system output constraints and added a fallback string-stripping utility in Python.
* **Guardrail Bypass Attempts:** 
  * *Issue:* Test prompt injections tried to trick the agent into skipping human-in-the-loop approvals on `send_email`.
  * *Fix:* Moved safety enforcement entirely out of prompt instructions and implemented a hardcoded interactive `(y/n)` approval block directly inside `tools.py`.

---

## Setup & Execution

1. Ensure the Anthropic API key is exported in your BAS terminal:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"

   [ Start: agent.py Execution ]
                   │
                   ▼
         ┌───────────────────┐
         │ Claude Code Agent │
         └─────────┬─────────┘
                   │
                   ▼
          ┌─────────────────┐
          │  list_open_pos  │ ──► Reads and filters open records from pos.json
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │  get_po_status  │ ──► Calculates delivery lateness & fulfillment ratios
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │   draft_email   │ ──► Generates vendor reminder message draft
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────────────────────────────┐
          │               send_email                │ ──► 🛡️ HUMAN GUARDRAIL GATE
          └────────────┬────────────────────────────┘     (Interactive stdin prompt)
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
   [ User types 'y' ]        [ User types 'n' ]
          │                         │
          ▼                         ▼
  { Status: SUCCESS }      { Status: BLOCKED }
          │                         │
          └────────────┬────────────┘
                       │
                       ▼
        [ Appended to audit.jsonl immutably ]