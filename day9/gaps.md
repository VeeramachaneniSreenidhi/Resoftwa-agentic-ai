# Capstone 2 - Guardrail Audit (gaps.md)

## 1. Human-in-the-Loop
* **Status:** [Pass / Partial / Fail]
* **Requirement:** A person must approve where money moves or data leaves[cite: 5].
* **Current Implementation:** [Reference Day 8 agent logic: What happens when an invoice fails check or needs approval?]
* **Gap Identified:** [List any instances where high-risk actions or payments auto-execute without human sign-off]

## 2. Least Privilege
* **Status:** [Pass / Partial / Fail]
* **Requirement:** An agent gets only the access its job needs[cite: 5].
* **Current Implementation:** [Reference Day 8 tools (`inv_tools.py`): What permissions does the agent pipeline have?]
* **Gap Identified:** [List any excessive permissions, e.g., if the reader tool has direct database write/posting access]

## 3. Audit Trail
* **Status:** [Pass / Partial / Fail]
* **Requirement:** A record of every action the agent took[cite: 5].
* **Current Implementation:** [Reference Day 8 logs (`inv_audit_log.json` / `decision_log.json`): How are decisions tracked?]
* **Gap Identified:** [List missing metadata, timestamps, or unlogged tool calls during exception handling]

## 4. Boss and Workers (Separation of Concerns)
* **Status:** [Pass / Partial / Fail]
* **Requirement:** One agent plans; small agents each do one job[cite: 5].
* **Current Implementation:** [Reference Day 8 architecture: Is planning separated from worker tools?]
* **Gap Identified:** [List if your logic is currently trapped in a monolithic script instead of modular tasks]