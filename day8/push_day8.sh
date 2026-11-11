#!/usr/bin/env bash
# Commit and push the day8 folder only. Never force-pushes, never touches other folders or .env.
# Patterns below are written with bracket tricks (e.g. api_[k]ey=) so this script does not match itself.
set -u

ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "ERROR: not inside a git repository"; exit 1; }
cd "$ROOT" || exit 1

# 1. Secret scan over day8. Abort if anything matches.
PATTERN='sk-[A-Za-z0-9]{20,}|BEGIN[ ]PRIVATE[ ]KEY|AKIA[0-9A-Z]{16}|passw[o]rd=|api_[k]ey='
MATCHES=$(grep -rIEn -- "$PATTERN" day8 2>/dev/null)
if [ -n "$MATCHES" ]; then
  echo "ABORT: possible secret pattern found under day8. Nothing staged, committed or pushed."
  echo "$MATCHES"
  exit 1
fi
echo "Secret scan: no matches under day8."

# 2. Stage day8 only.
git add -- day8 || { echo "ERROR: git add failed"; exit 1; }

# 3. Commit only if something under day8 is staged. Pathspec limits the commit to day8.
if git diff --cached --quiet -- day8; then
  echo "Nothing staged under day8; no commit made."
else
  git commit -m "day-08: requisition agent, invoice-to-PO pipeline, ABAP review, lab log" \
    -m "Co-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>" -- day8 \
    || { echo "ERROR: commit failed"; exit 1; }
fi

# 4. Push the current branch if a remote exists. Never --force.
if [ -z "$(git remote)" ]; then
  echo "No git remote configured; skipping push. No remote was invented."
  exit 0
fi
REMOTE=origin
git remote | grep -qx "$REMOTE" || REMOTE=$(git remote | head -n 1)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Pushing branch $BRANCH to $REMOTE"
if git rev-parse --abbrev-ref --symbolic-full-name '@{u}' >/dev/null 2>&1; then
  git push "$REMOTE" "$BRANCH"
else
  git push --set-upstream "$REMOTE" "$BRANCH"
fi
RC=$?
if [ $RC -eq 0 ]; then
  echo "PUSH OK: $BRANCH -> $REMOTE"
else
  echo "PUSH FAILED (exit $RC): $BRANCH -> $REMOTE"
fi
exit $RC
