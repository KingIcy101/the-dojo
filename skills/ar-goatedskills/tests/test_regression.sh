#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/podhi/.openclaw/skills/humanizer"
LINT="$ROOT/scripts/regression_lint.py"
FIXTURES="$ROOT/tests/fixtures"

# Should fail
if python3 "$LINT" --text-file "$FIXTURES/fail_stock_phrases.txt" --strict >/tmp/humanizer_test_fail1.json 2>&1; then
  echo "Expected fail_stock_phrases.txt to fail, but it passed"
  exit 1
fi

if python3 "$LINT" --text-file "$FIXTURES/fail_structural_patterns.txt" --strict >/tmp/humanizer_test_fail2.json 2>&1; then
  echo "Expected fail_structural_patterns.txt to fail, but it passed"
  exit 1
fi

# Should pass
python3 "$LINT" --text-file "$FIXTURES/pass_humanized.txt" --strict >/tmp/humanizer_test_pass.json

echo "humanizer regression tests: PASS"
