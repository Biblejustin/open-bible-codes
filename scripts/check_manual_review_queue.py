#!/usr/bin/env python3
"""Validate the manual-review queue stays evidence-linked and non-claiming."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/MANUAL_REVIEW_QUEUE.md")

REQUIRED_PHRASES = (
    "Status: navigation aid, not a claim report.",
    "Rows stay in review status unless a future locked",
    "Review candidates are not public claims.",
    "Any upgrade requires a new locked prospective design",
)

REQUIRED_EVIDENCE_PATHS = (
    Path("docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md"),
    Path("docs/ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_CONTROLS.md"),
    Path("docs/CENTERED_OCCURRENCE_INDEX.md"),
    Path("docs/CRD_CENTER_WORD_SELF_VS_CONCEPT_FINDINGS.md"),
    Path("docs/ALL_CODES_FOLLOWUP_REVIEW.md"),
)

REQUIRED_ROW_FAMILIES = (
    "four-source follow-up",
    "compound extension",
    "centered on open Gog",
    "referent discipline",
    "background-pressure cautions",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_manual_review_queue(args.doc)
    if failures:
        for failure in failures:
            print(f"manual review queue failure: {failure}", file=sys.stderr)
        return 1
    print(f"manual review queue ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_manual_review_queue(doc: Path) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    failures: list[str] = []
    for phrase in REQUIRED_PHRASES:
        if phrase not in text:
            failures.append(f"{doc} missing guard phrase: {phrase}")
    for family in REQUIRED_ROW_FAMILIES:
        if family not in text:
            failures.append(f"{doc} missing row family: {family}")
    for evidence_path in REQUIRED_EVIDENCE_PATHS:
        if not evidence_path.exists():
            failures.append(f"evidence path missing: {evidence_path}")
        if f"`{evidence_path}`" not in text:
            failures.append(f"{doc} missing evidence link: {evidence_path}")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
