#!/usr/bin/env python3
"""Validate WRR remaining-lane review checklist stays no-input."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md")

REQUIRED_PHRASES = (
    "# WRR Remaining-Lane Review Checklist",
    "Status: no-input checklist for page-image and method/pair-universe review.",
    "It does not choose source corrections, method changes, or pair exclusions.",
    "- Remaining-lane checklist terms: 14.",
    "- Residual pair links: 14.",
    "- Minimum-frontier pair links: 4.",
    "- Page-image terms: 3.",
    "- Method/pair-universe terms: 11.",
    "No source correction, method change, or pair exclusion is selected by this checklist.",
    "| `page_image_near_match_review` | 3 | 3 | 2 | page-image inspection against near-match OCR |",
    "| `method_or_pair_universe_review` | 11 | 11 | 2 | method or pair-universe review for OCR-matched missing ordinary hits |",
    "| 1 | `page_image_near_match_review` | `pending_page_image_lock` | `wrr2_19_app_11` |",
    "| 4 | `method_or_pair_universe_review` | `pending_method_pair_universe_lock` | `wrr2_02_app_03` |",
    "Page-image near-match rows need cited page-image transcription evidence.",
    "Method rows need an explicit method or pair-universe explanation for zero ordinary hits.",
)

FORBIDDEN_PHRASES = (
    "selected correction",
    "selected exclusion",
    "source corrected to",
    "pair excluded",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_remaining_lane_review_checklist_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR remaining-lane checklist failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR remaining-lane checklist ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_remaining_lane_review_checklist_doc(doc: Path) -> list[str]:
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
