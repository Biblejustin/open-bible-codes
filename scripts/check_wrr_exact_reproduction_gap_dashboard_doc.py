#!/usr/bin/env python3
"""Validate the WRR exact-reproduction gap dashboard keeps boundaries visible."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md")

REQUIRED_PHRASES = (
    "# WRR Exact Reproduction Gap Dashboard",
    "Status: exact published WRR reproduction is not closed.",
    "It does not select source corrections, pair exclusions, replacement spellings, or method changes.",
    "Source-cited defined distances | 163",
    "Current defined distances | 72",
    "Remaining 163-distance gap | 91",
    "Residual gap after simple-variant upper bound | 40",
    "Manual decision rows | 37",
    "Locked manual decision records | 37",
    "Unlocked manual decision records | 0",
    "Recorded selected actions | method_lock=11; no_source_change=26",
    "| `source_policy_or_pair_rule_review` | 1 | 1 | 1 |",
    "| `source_transcription_or_row_alignment` | 43 | 44 | 35 |",
    "Chelm source-policy/pair-rule target | locked | no_source_change",
    "post-lock reporting boundary",
    "all current manual review rows are locked",
    "Do not describe the local result as exact published WRR reproduction.",
    "This dashboard is a review map, not a reproduction result.",
)

FORBIDDEN_PHRASES = (
    "exact published WRR reproduced",
    "source correction selected",
    "pair exclusion selected",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_gap_dashboard_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR exact gap dashboard failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR exact gap dashboard ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_gap_dashboard_doc(doc: Path) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text
    ]
    for phrase in FORBIDDEN_PHRASES:
        if phrase in text and f"- {phrase}" not in text:
            failures.append(f"{doc} forbidden phrase outside boundary list: {phrase}")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
