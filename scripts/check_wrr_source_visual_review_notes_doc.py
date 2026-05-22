#!/usr/bin/env python3
"""Validate WRR source visual-review notes stay scoped to triage."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_VISUAL_REVIEW_NOTES.md")

REQUIRED_PHRASES = (
    "# WRR Source Visual Review Notes",
    "Status: visual triage notes only. These are not a locked primary transcription and not a WRR reproduction.",
    "Source reviewed: `reports/wrr_1994/wrr_1994_paper.pdf`, Table 2 page render `reports/wrr_1994/wrr_primary_table2_page-06.png`.",
    "| `wrr2_23_app_04` `Y@QBHLWY` | 23 | Row visibly contains",
    "| `wrr2_23_app_05` `MHRYSGL` | 23 | Row visibly contains",
    "| `wrr2_30_app_05` `B@LY$RLBB` | 30 | Row visibly contains",
    "| `wrr2_28_app_04` `B@LPNYM$H` | 28 | Row visibly contains",
    "| `wrr2_32_app_04` `$LMHMXLMA` | 32 | Bottom row crop clearly shows",
    "| `wrr2_27_date_01` `/+Z/T$RY` | 27 | Row visibly contains",
    "| `wrr2_27_app_06` `M$HZKWTW` | 27 | Row visibly contains",
    "OCR miss, not obvious source absence.",
    "Source/title-prefix rule needs review.",
    "Needs wider crop or row-boundary/source review.",
    "## Local WNP Critique Context",
    "Rabbi II-27 Zacut forms",
    "Rabbi II-30 Yosher-Levav",
    "Rabbi II-32 Chelma",
    "The current `ocr_not_matched_with_variant_lead` bucket is mixed.",
    "Some top rows are plain OCR misses against visible primary-page text.",
    "Some rows are not simple source errors; they look like title/prefix normalization questions",
    "None of these notes authorize changing WRR terms or claiming reproduction.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_visual_review_notes_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR source visual-review notes doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source visual-review notes doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_source_visual_review_notes_doc(doc: Path) -> list[str]:
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
