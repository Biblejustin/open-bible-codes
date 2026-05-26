#!/usr/bin/env python3
"""Validate WRR source row OCR word packet stays scoped to review aids."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_ROW_OCR_WORD_PACKET.md")

REQUIRED_PHRASES = (
    "# WRR Source Row OCR Word Packet",
    "Status: no-input OCR word packet for WRR source-row review.",
    "it is not transcription verification and does not choose row transcriptions, source corrections, method changes, or pair exclusions.",
    "OCR words are review aids only; no row transcription, source correction, pair exclusion, or method change is selected by this packet.",
    "OCR word availability is not transcription verification.",
    "Low confidence counts are review triage only.",
    "No row here changes the working WRR source or excludes a pair automatically.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_row_ocr_word_packet_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR source row OCR word packet failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source row OCR word packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_source_row_ocr_word_packet_doc(doc: Path) -> list[str]:
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
