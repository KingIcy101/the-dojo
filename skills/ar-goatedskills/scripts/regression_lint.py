#!/usr/bin/env python3
"""Regression lint for recurring AI-writing patterns.

Usage:
  python3 regression_lint.py --text-file draft.txt --strict
  cat draft.txt | python3 regression_lint.py --strict
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

STOCK_PHRASES = [
    r"\bat the end of the day\b",
    r"\bit'?s worth noting\b",
    r"\bdeep dive\b",
    r"\bin today'?s fast-paced world\b",
    r"\bmoving forward\b",
    r"\bneedless to say\b",
]

PERFORMED_AUTH = [
    r"\bi genuinely (feel|think|believe)\b",
    r"\bto be honest\b",
    r"\bnot gonna lie\b",
    r"\blet'?s be real\b",
    r"\bspeaking from the heart\b",
]

HEDGING_BUNDLES = [
    r"\bcould potentially\b",
    r"\bmight possibly\b",
    r"\bit seems that\b",
    r"\bit appears that\b",
]

EM_DASH = r"[—–]"
RULE_OF_THREE = r"\b[^\n,]{2,40},\s*[^\n,]{2,40},\s*(and|or)\s+[^\n,]{2,40}\b"


def collect(patterns: list[str], text: str, label: str) -> list[dict]:
    out = []
    for pat in patterns:
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            out.append(
                {
                    "type": label,
                    "pattern": pat,
                    "match": m.group(0),
                    "index": m.start(),
                }
            )
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Detect recurring AI-writing regression patterns")
    ap.add_argument("--text-file", help="Path to text file")
    ap.add_argument("--strict", action="store_true", help="Exit non-zero when violations are found")
    args = ap.parse_args()

    if args.text_file:
        text = Path(args.text_file).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    violations: list[dict] = []
    violations += collect(STOCK_PHRASES, text, "stockPhrase")
    violations += collect(PERFORMED_AUTH, text, "performedAuthenticity")
    violations += collect(HEDGING_BUNDLES, text, "hedgingBundle")

    for m in re.finditer(EM_DASH, text):
        violations.append({"type": "emDash", "pattern": EM_DASH, "match": m.group(0), "index": m.start()})

    rule_matches = list(re.finditer(RULE_OF_THREE, text, flags=re.IGNORECASE))
    if len(rule_matches) > 1:
        # One natural list can be fine; repeated triads are usually style spam.
        for m in rule_matches:
            violations.append(
                {
                    "type": "ruleOfThreeSpam",
                    "pattern": RULE_OF_THREE,
                    "match": m.group(0),
                    "index": m.start(),
                }
            )

    report = {
        "ok": len(violations) == 0,
        "violationCount": len(violations),
        "violations": sorted(violations, key=lambda x: x["index"]),
    }
    print(json.dumps(report, indent=2))

    if args.strict and violations:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
