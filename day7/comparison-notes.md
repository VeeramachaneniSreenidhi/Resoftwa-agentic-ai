# Day 7: Codex vs Claude Code comparison

Input: Day 6 feature spec (capstone-2/spec.md). Comparison done on Day 7.

Task: implement the four pipeline requirements in capstone-2/spec.md
(JSON extraction, MCP validation, posting/exceptions, human sign-off).

| Criterion | Claude Code | Codex |
|---|---|---|
| Requirements covered | 4 of 4 | 4 of 4 |
| Files changed | 11 | 11 |
| Lines added | 777 | 224 |
| Test cases written | 23 | 10 |
| Test files with content | 4 | 1 (3 empty) |
| Tests passing | not verified separately | 8 of 8 (its own run) |
| Source depth (mcp-server / pipeline) | 111 / 134 lines | 12 / 30 lines |
| Time | not recorded | 8m 8s |
| Approvals needed | not recorded | ~10 (sandbox failed to start) |
| Read .env | not recorded | No |

## Verdict
Both tools covered the same 11 files and all four requirements.
Claude Code produced the more complete result: about 3.5x more code,
23 test cases across four test files, and a fuller MCP server and
pipeline. Codex was leaner and quicker to review, but it left three
test files empty, put all tests in one file, and its src files are thin.
I would merge Claude Code's diff as the base and use Codex's compact
style as a reference for keeping future changes small.

## Lessons
- Codex: the spec had no "Day 6" label, so it inferred the four requirements. Name them explicitly in the prompt.
- Codex: its sandbox failed to start, so every command needed manual approval.
- Claude Code: the larger diff takes more review time; check it for scope creep.
- Both: require one unit test file per module and no empty placeholder files.