# Prompts for Claude Code (run `claude` inside day8)
Rule for all prompts: do NOT modify phase1_source.abap. Cite line numbers. Do not invent anything not in the file.

## 1. Explain
Read phase1_source.abap. Give: a one-paragraph summary; a step-by-step walkthrough; the DB tables
and classes used; and anything risky or missing (authority check, error handling, filters, units).

## 2. Obsolete statements
List obsolete or discouraged ABAP statements in phase1_source.abap as a table:
Line | Statement | Why obsolete | Modern replacement | Severity. Only list what really exists.

## 3. ABAP Unit
Write ABAP Unit tests for the selection logic. Use CL_OSQL_TEST_ENVIRONMENT for EKKO and EKPO.
If the logic is not testable as written, propose the smallest refactor (local class) first.

## 4. Cross-check (after you read review_notes.md)
Here is my review_notes.md and scan_report.md. List anything wrong, missing or overstated.
Cite line numbers from phase1_source.abap.
