# CLAUDE.md - Capstone 2: Invoice-to-Insight

Project: Production-style invoice extraction and validation agent
Run tests: npm test

Rules:
- Temperature 0 for invoice extraction
- Fixed schema fields only for JSON output
- Require human approval before any posting summary logs
- Log all audit actions to audit.jsonl
