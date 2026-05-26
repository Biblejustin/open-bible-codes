#!/usr/bin/env python3
"""Validate WRR source row crop contact sheet stays scoped to review aids."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_ROW_CROP_CONTACT_SHEET.md")

REQUIRED_PHRASES = (
    "# WRR Source Row Crop Contact Sheet",
    "Status: local visual contact sheet for WRR source-row review.",
    "It is a review aid only; it is not transcription verification",
    "Contact sheet image: `reports/wrr_1994/wrr_source_row_crop_contact_sheet.png`.",
    "Crop availability is not transcription verification.",
    "Manual visual notes remain triage notes unless a separate decision record cites source evidence.",
    "No row here changes the working WRR source or excludes a pair automatically.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_row_crop_contact_sheet_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR source row crop contact sheet failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source row crop contact sheet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_source_row_crop_contact_sheet_doc(doc: Path) -> list[str]:
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
