#!/usr/bin/env python3
"""Validate WRR manual-decision register stays no-input."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_MANUAL_DECISION_REGISTER.md")

REQUIRED_PHRASES = (
    "# WRR Manual Decision Register",
    "Status: consolidated no-input register for WRR manual-lock decisions.",
    "It does not choose source corrections, row transcriptions, pair exclusions, replacement locks, or method changes.",
    "- Manual decision rows: 37.",
    "- Action terms represented: 58.",
    "- Residual pair links represented: 59.",
    "- Minimum-frontier pair links represented: 40.",
    "- Source-policy/pair-rule decision rows: 1.",
    "- Source-transcription row-cluster decision rows: 22.",
    "- Page-image decision rows: 3.",
    "- Method/pair-universe decision rows: 11.",
    "No source correction, row transcription, pair exclusion, replacement lock, or method change is selected by this register.",
    "| `source_policy_pair_rule` | 1 | 1 | 1 | 1 |",
    "| `source_transcription_row_cluster` | 22 | 43 | 44 | 35 |",
    "| `page_image_near_match` | 3 | 3 | 3 | 2 |",
    "| `method_pair_universe` | 11 | 11 | 11 | 2 |",
    "| 1 | `source_policy_pair_rule` | `pending_source_policy_pair_rule_lock` |",
    "| 2 | `source_transcription_row_cluster` | `pending_manual_source_lock` |",
    "| 24 | `page_image_near_match` | `pending_page_image_lock` |",
    "| 27 | `method_pair_universe` | `pending_method_pair_universe_lock` |",
    "Source-policy/pair-rule rows need citable source and pair-rule evidence.",
    "Source-transcription row clusters need cited row image or source-list transcription plus row/column alignment evidence.",
    "Page-image rows need cited page-image transcription evidence.",
    "Method/pair-universe rows need an explicit explanation for zero ordinary hits.",
)

FORBIDDEN_PHRASES = (
    "selected correction",
    "selected exclusion",
    "source corrected to",
    "pair excluded",
    "replacement locked",
    "method changed to",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_manual_decision_register_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR manual decision register failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR manual decision register ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_manual_decision_register_doc(doc: Path) -> list[str]:
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
