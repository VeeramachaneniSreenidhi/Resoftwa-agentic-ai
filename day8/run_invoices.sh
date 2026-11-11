#!/usr/bin/env bash
# Run the invoice pipeline (validate, audit, reports), then the unit tests.
# Never posts anything. Test output is saved to inv_test_results.txt.
set -u
cd "$(dirname "$0")" || exit 1

python3 inv_pipeline.py || { echo "inv_pipeline.py failed"; exit 1; }

python3 -m unittest -v inv_test > inv_test_results.txt 2>&1
status=$?
tail -n 3 inv_test_results.txt
exit $status
