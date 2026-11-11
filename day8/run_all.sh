#!/bin/bash
cd "$(dirname "$0")"
echo "=== AGENT RUN ===";  python3 run_agent.py
echo; echo "=== TESTS ===";  python3 -m pytest -v 2>&1 | tee test_results.txt
