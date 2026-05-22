#!/usr/bin/env python3
"""Validate WRR source-policy review checklist stays no-input."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_POLICY_REVIEW_CHECKLIST.md")

REQUIRED_PHRASES = (
    "# WRR Source-Policy Review Checklist",
    "Status: no-input checklist for Chełm source-policy/pair-rule review.",
    "It does not choose a source correction, exclude a pair, or lock a replacement.",
    "- Source-policy checklist terms: 1.",
    "- Residual pair links: 1.",
    "- Minimum-frontier pair links: 1.",
    "- Related source-review rows: 2.",
    "- Related scenario-pair rows: 4.",
    "- WNP context blocks: 3.",
    "No source correction, pair exclusion, or replacement lock is selected by this checklist.",
    "| 1 | `pending_source_policy_pair_rule_lock` | `wrr2_32_app_05` | `$LMHMX@LMA` |",
    "`reports/wrr_1994/wnp_en.html:608-619`",
    "Citable primary source/pair-rule evidence is required before changing the working source.",
    "The record must say whether Chełm forms belong in the Hebrew source cell, a source-policy note, or neither.",
)

FORBIDDEN_PHRASES = (
    "selected correction",
    "selected exclusion",
    "source corrected to",
    "pair excluded",
    "replacement locked",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_policy_review_checklist_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR source-policy checklist failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source-policy checklist ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_source_policy_review_checklist_doc(doc: Path) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized_text = normalize_space(text)
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text and normalize_space(phrase) not in normalized_text
    ]
    failures.extend(
        f"{doc} contains forbidden phrase: {phrase}"
        for phrase in FORBIDDEN_PHRASES
        if phrase in normalized_text
    )
    return failures


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
