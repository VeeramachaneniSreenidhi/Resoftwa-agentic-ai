# Capstone 2 Specification (spec.md)

## Pipeline Overview
1. **Watch & Extract:** Read vendor invoices from JSON, enforce fixed fields with temperature 0.
2. **Validate:** Check extracted fields against PO rules via custom MCP tool.
3. **Clean vs. Exceptions:** Route valid records to posting summary; route anomalies to exception review list with clear reasons.
4. **Human-in-the-Loop:** Require explicit human sign-off before final posting.
