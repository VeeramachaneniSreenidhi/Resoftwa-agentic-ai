#!/bin/bash
# Hook: Intercept tool usage to enforce workspace safety

TOOL_NAME="$1"

echo "[HOOK] Intercepting execution for tool: $TOOL_NAME"

# Simple safety gate
if [[ "$TOOL_NAME" == "rm -rf /" ]]; then
  echo "[HOOK ERROR] Dangerous operation blocked!"
  exit 1
fi

exit 0
