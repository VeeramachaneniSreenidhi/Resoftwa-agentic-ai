Risk Register: Three AI Agents
Agent	Name	Purpose
1	Credit Gatekeeper (O2C Credit Check)	Decides whether a sales order is within the customer's credit limit and releases or holds it
2	Leave Desk (Leave Request)	Validates and approves routine leave against balance and team coverage
3	Invoice-to-PO Pipeline	Extracts invoice data, validates it against PO rules via an MCP tool, flags exceptions, requires human approval before posting

Impact scale: Critical > High > Medium/High > Medium

Agent 1: O2C Credit Check (Credit Gatekeeper)
No.	Risk	Description	Impact
1	Incorrect credit data	ERP provides outdated or incorrect credit limits, balances, or overdue invoices.	High
2	Incorrect exposure calculation	Open orders, unpaid invoices, or the new order are calculated incorrectly or counted twice.	High
3	Unauthorised order release	Agent releases an order without satisfying credit conditions.	Critical
4	Missing credit hold	Agent fails to identify an active customer credit hold.	High
5	Incorrect overdue detection	Agent overlooks invoices overdue by more than 30 days.	High
6	Payment history errors	Recent bounced payments or poor payment history are not identified.	High
7	Auto-release threshold failure	Agent automatically releases orders exceeding the permitted exposure or the $50K cap.	Critical
8	Human approval bypass	Agent processes a high-risk order without Credit Controller approval.	Critical
9	Unauthorised override	Sales or another unauthorised person forces a credit release.	Critical
10	ERP/MCP integration failure	Connection failure causes incomplete or incorrect credit decisions.	High
11	Incorrect escalation	Orders exceeding 110% of the credit limit are not escalated to the Finance Partner.	High
12	Incomplete audit logs	Order ID, decision, approver, timestamp, or override reason is missing.	Medium/High
13	Data privacy breach	Customer financial information is exposed to unauthorised users.	High
14	Duplicate processing	The same order is checked or released multiple times.	Medium/High
15	Notification failure	Sales is not informed about a hold or release decision.	Medium
Agent 2: Leave Request (Leave Desk)
No.	Risk	Description	Impact
1	Incorrect leave balance	Agent retrieves an incorrect or outdated employee leave balance.	High
2	Incorrect leave eligibility	Agent approves a leave type the employee is not eligible for.	High
3	Coverage calculation error	Agent approves leave even when minimum team coverage is not maintained.	High
4	Blackout date oversight	Agent misses month-end, audit, or critical project dates.	High
5	Unauthorised leave approval	Agent approves leave without the required manager approval.	Critical
6	Sensitive leave data exposure	Medical, parental, or bereavement information is exposed.	Critical
7	Incorrect policy interpretation	Agent misunderstands leave policies or notice requirements.	High
8	Retroactive leave errors	Agent automatically processes leave requests for dates in the past.	Medium/High
9	Incorrect payroll update	Approved leave is incorrectly recorded in payroll attendance.	High
10	Calendar synchronisation failure	Approved leave is not reflected in the team calendar.	Medium/High
11	Human escalation failure	Requests requiring Line Manager or HRBP approval are automatically approved.	Critical
12	Insufficient leave balance handling	Agent approves unpaid or advance leave without proper authorisation.	High
13	Notification failure	Employee or manager does not receive the approval or rejection notification.	Medium
14	Incomplete audit trail	Request ID, decision, approver, or approval timestamp is missing.	Medium/High
15	Employee data privacy breach	Personal employee information is accessed or disclosed without authorisation.	Critical
Agent 3: Invoice-to-PO Pipeline
3.1 Functional and operational risks
No.	Risk	Description	Impact
1	Incorrect invoice extraction	Invoice number, date, amount, or vendor details are misread, especially from poor scans or unusual layouts.	High
2	Missing mandatory fields	Required fields (PO number, tax ID, bank details) are absent, but processing continues instead of stopping.	High
3	Wrong PO match	Invoice is linked to the wrong PO, or to a closed or partly consumed PO.	Critical
4	Wrong vendor identification	Invoice is tied to the wrong supplier or a duplicate vendor record.	Critical
5	Validation false pass	An invoice that breaks PO rules (price, quantity, terms, PO balance) is accepted.	Critical
6	Goods receipt not verified	Invoice is passed without confirming goods or services were received (3-way match gap).	High
7	Tax, currency, and rounding errors	Tax amounts, totals, exchange rates, or rounding are extracted or validated incorrectly.	High
8	Tolerance misconfiguration	Price or quantity tolerances are too loose or outdated, so variances slip through.	High
9	Duplicate invoice processing	The same invoice is processed or posted more than once (resubmission, re-scan, or changed file name).	High
10	MCP tool failure	The validation service is down, times out, or returns wrong results, and the pipeline treats that as a pass.	High
11	Exception handling failure	Invalid invoices are not flagged, or exceptions are not clearly reported to the reviewer.	High
12	Workflow interruption	Pipeline crashes mid-run, leaving partial postings or invoices stuck with no owner.	Medium/High
3.2 Security risks
No.	Risk	Description	Impact
1	Sensitive data exposure	Vendor bank details, invoice amounts, and other financial data are visible to unauthorised users or logs.	Critical
2	Unauthorised invoice posting	A user, agent, or integration posts an invoice without proper authority.	Critical
3	Data tampering	Invoice or PO data is altered between extraction and validation.	Critical
4	API and integration vulnerabilities	Unauthorised access through the MCP or ERP connection.	Critical
5	Excessive permissions	The agent can post, edit vendor master data, or change PO rules when it only needs to read and validate.	High
6	Prompt injection	Hidden or malicious text in an invoice document influences the AI's output or decision.	High
3.3 Human approval risks
No.	Risk	Description	Impact
1	Approval bypass	Invoice is posted without explicit human approval.	Critical
2	False approval	A blank, invalid, or ambiguous response is treated as approval.	Critical
3	Wrong approver	Approval comes from someone without authority, or from the person who entered the invoice (segregation of duties).	High
4	Insufficient exception detail	The reviewer is not shown what failed and why, so they approve blindly.	Medium/High
5	Rubber-stamping	Reviewers approve in bulk without checking, so the human control is nominal only.	High
6	Approval logging failure	Approver identity, decision, or timestamp is not recorded.	High
3.4 Financial and compliance risks
No.	Risk	Description	Impact
1	Incorrect or duplicate payment	Wrong amounts or repeated invoices lead to overpayment that is hard to recover.	Critical
2	Fraudulent invoices	Fake, altered, or unsolicited invoices pass validation.	Critical
3	Vendor bank-detail change fraud	Invoice carries new bank details that are accepted without independent verification.	Critical
4	Tax compliance issues	Wrong tax treatment causes filing errors, penalties, or lost input credit.	High
5	Policy violations	Invoices are posted despite breaching procurement policy (no PO, split orders, unapproved vendor).	High
6	Audit trail gaps	Decisions cannot be traced to the agent, the rule triggered, and the human approver.	High
Common risks affecting all three agents
No.	Common risk	Description	Impact
1	AI hallucination	Agent generates decisions based on incorrect or fabricated information.	Critical
2	Incorrect business rules	Incorrect thresholds or outdated policies cause wrong decisions.	High
3	System downtime	ERP, HRMS, OCR, or MCP tools become unavailable.	High
4	API security risk	Unauthorised access to business systems through integrations.	Critical
5	Prompt injection	Malicious or untrusted input influences agent decisions.	High
6	Poor access control	Agent has more permissions than required.	Critical
7	Audit failure	Decisions cannot be traced back to the agent and human approver.	High
8	Human oversight failure	Human approval is skipped or incorrectly recorded.	Critical
9	Duplicate transactions	Repeated tool calls create duplicate approvals, releases, or postings.	High
10	Business continuity	Agent failure interrupts credit checks, leave processing, or invoice posting.	Medium/High
Priorities
Priority 1: Critical (address first)
Unauthorised credit release (Agent 1)
Human approval bypass (Agents 1, 3)
Unauthorised credit overrides (Agent 1)
Unauthorised leave approval (Agent 2)
Sensitive employee information exposure (Agent 2)
Wrong PO or vendor match, and validation false pass (Agent 3)
Fraudulent invoices, bank-detail change fraud, and duplicate payments (Agent 3)
Excessive agent permissions (all agents)
Prompt injection and API security (all agents)
Priority 2: High
Incorrect business rule interpretation (all agents)
ERP/HRMS/MCP integration failures (all agents)
Failure to escalate exceptions (Agents 1, 2)
Incorrect credit exposure calculations and missing overdue invoices (Agent 1)
Incorrect leave balance calculations and team coverage checks (Agent 2)
Incorrect payroll updates (Agent 2)
Tax, currency, and rounding errors; tolerance misconfiguration (Agent 3)
Audit trail gaps (all agents)
Recommended controls
Control	Agent 1: Credit Gatekeeper	Agent 2: Leave Desk	Agent 3: Invoice-to-PO
Human-in-the-loop	Mandatory for exceptions and overrides.	Mandatory for sensitive and exceptional leave.	Mandatory before every posting; only explicit, authenticated approval counts.
Permission control	Cannot change credit limits.	Cannot change leave policies.	Read and validate only; posting runs through an approved, logged step.
Approval validation	Verify Credit Controller / Finance Partner approval.	Verify Line Manager / HRBP approval.	Verify approver authority; approver cannot be the submitter (segregation of duties).
Data validation	Reconcile credit exposure with ERP.	Reconcile leave balance with HRMS.	Cross-check against PO, goods receipt, and vendor master; verify bank-detail changes by callback.
Fail-safe	Hold order when data is unavailable or uncertain.	Route to human review when data is unavailable.	Missing fields, low confidence, or tool errors go to a human; never auto-post.
Duplicate prevention	Unique order IDs and idempotency checks.	Unique request IDs and idempotency checks.	Check vendor + invoice no. + amount + date; idempotency keys on posting calls.
Audit logging	Log every credit decision and override.	Log every leave decision and approval.	Log extraction, rule results, exceptions, approver, and timestamp.
Access security	Role-based access and encryption.	Role-based access and sensitive-data protection.	Role-based access, encryption, and masking of bank details.
Input safety	Treat all inputs as data, not instructions.	Treat all inputs as data, not instructions.	Treat invoice content as data; scan for injection patterns.
Overall risk assessment
Agent	Overall risk level	Main reason
Agent 1: Credit Gatekeeper	High	Direct financial exposure and unauthorised credit release.
Agent 2: Leave Desk	High	Employee privacy, payroll errors, and incorrect leave approvals.
Agent 3: Invoice-to-PO Pipeline	High (Critical if auto-posting is ever enabled)	Direct payment impact, fraud exposure, and dependence on extraction accuracy.

Recommendation: All three agents should follow a fail-safe, human-in-the-loop approach. If required data is missing, an integration fails, confidence is low, or an approval cannot be verified, the agent must stop automatic processing and escalate to a human. It should never default to "approve" or "release."