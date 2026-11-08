# AGENTS.md

## Project overview
Invoice-to-PO pipeline: extracts invoice JSON, validates it against PO rules
through an MCP tool, posts valid invoices, lists exceptions, and requires
human sign-off before posting.

## Structure
- capstone-2/src/ - pipeline code
- capstone-2/test/ - tests
- capstone-2/spec.md - source of truth for requirements

## Commands
- Test: cd capstone-2 && npm test

## Conventions
- Node.js with 'use strict'; tests use node:test and node:assert/strict
- One test file per module (schema, validate, mcp, pipeline)
- No empty placeholder files

## Boundaries
- Only edit capstone-2/src/ and capstone-2/test/
- Never read, print or commit .env or any secrets
- Do not add dependencies without asking
- Posting requires an explicit true from the human sign-off callback

## Workflow
1. Read spec.md and list the numbered requirements.
2. Plan briefly, then implement.
3. Run npm test and fix failures.
4. Finish with a summary mapping each change to a requirement.

## Definition of done
All requirements implemented, tests pass, no unrelated changes, no empty files.

## Lessons from the Codex vs Claude Code comparison
- Name the exact spec requirements in the prompt; the spec has no "Day 6" label.
- Write unit tests per module, not one catch-all test file.
- Keep diffs small and scoped to the spec.