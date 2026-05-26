#!/usr/bin/env python3
"""Validate WRR source row review bundle stays scoped to review aids."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_ROW_REVIEW_BUNDLE.md")

REQUIRED_PHRASES = (
    "# WRR Source Row Review Bundle",
    "Status: no-input row-review bundle for WRR source-row review.",
    "It combines row-checklist, crop-path, and OCR-word evidence; it does not choose row transcriptions, source corrections, method changes, or pair exclusions.",
    "Row review clusters: 22.",
    "Rows with generated crops: 22.",
    "Rows with OCR words: 22.",
    "Low-confidence OCR words: 78.",
    "Crop and OCR availability is not transcription verification.",
    "No row here changes the working WRR source or excludes a pair automatically.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_row_review_bundle_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR source row review bundle failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source row review bundle ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_source_row_review_bundle_doc(doc: Path) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized_text = normalize_space(text)
    return [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text and normalize_space(phrase) not in normalized_text
    ]


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
