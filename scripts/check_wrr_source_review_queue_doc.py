#!/usr/bin/env python3
"""Validate WRR source-review queue doc stays diagnostic."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_REVIEW_QUEUE.md")

REQUIRED_PHRASES = (
    "# WRR Source Review Queue",
    "Status: diagnostic-only source-review triage",
    "not a source correction",
    "not a term replacement",
    "not a WRR reproduction",
    "- Terms queued: 97.",
    "| `ocr_not_matched_with_variant_lead` | 5 | 5 | 7 |",
    "| `ocr_matched_with_variant_lead` | 32 | 45 | 948 |",
    "| `ocr_not_matched_no_variant_lead` | 44 | 45 | 0 |",
    "WNP Context For Queued Terms",
    "visual notes show title text without visible B@L prefix",
    "visual notes show English of-Chelm label but primary Hebrew cell only supports RBY$LMH in this pass",
    "Variant leads do not validate the original blocked pairs.",
    "Locked source rows and pair rules are still required before reproduction language.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_review_queue_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR source-review queue doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source-review queue doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_source_review_queue_doc(doc: Path) -> list[str]:
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
