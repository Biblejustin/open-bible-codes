#!/usr/bin/env python3
"""Validate WRR source-transcription row checklist stays no-input."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md")

REQUIRED_PHRASES = (
    "# WRR Source-Transcription Row Review Checklist",
    "Status: no-input checklist for row-level source-transcription review.",
    "It does not choose row transcriptions, source corrections, method changes, or pair exclusions.",
    "- Row review clusters: 22.",
    "- Source-transcription action terms: 43.",
    "- Residual pair links: 44.",
    "- Minimum-frontier pair links: 35.",
    "- Review state: `pending_manual_source_lock`.",
    "No row transcription, source correction, pair exclusion, or method change is selected by this checklist.",
    "| 1 | `06` | `WRR2 06` | `pending_manual_source_lock` | 4 | 4 | 4 |",
    "`wrr2_06_app_03 B@LM@$YH$M",
    "review row image once before individual term decisions",
    "Cite the primary row image or source-list row transcription used.",
    "Record keep, correct, exclude, or method/pair-universe decision outside this checklist.",
    "Preserve the working source unless a decision record selects a change.",
)

FORBIDDEN_PHRASES = (
    "selected correction",
    "selected exclusion",
    "source corrected to",
    "pair excluded",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_row_review_checklist_doc(args.doc)
    if failures:
        for failure in failures:
            print(
                f"WRR source-transcription row checklist failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"WRR source-transcription row checklist ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_row_review_checklist_doc(doc: Path) -> list[str]:
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
