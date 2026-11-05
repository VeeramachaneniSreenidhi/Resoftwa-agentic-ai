---
name: code-reviewer
description: Evaluates proposed code changes for security, performance, and formatting.
---

# Code Reviewer Skill

When reviewing code or pull requests, follow this mandatory checklist:

1. **Security:** Check for hardcoded credentials, unvalidated inputs, or SQL/command injections.
2. **Performance:** Verify async/await handling, avoid unindexed loops, and check memory cleanup.
3. **Standards:** Ensure proper error handling, clear variable naming, and standard formatting.

Provide concise feedback with explicit line-level suggestions.
