#!/usr/bin/env python3
"""Validate WRR direct all-lane diagnostic doc stays diagnostic."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_DIRECT_ALL_LANES_DIAGNOSTIC.md")

REQUIRED_PHRASES = (
    "# WRR Direct All-Lane Corrected-Distance Diagnostic",
    "Status: diagnostic-only, not a WRR reproduction.",
    "182 imported same-record WRR2 pairs",
    "| all lanes, cap 250 | 182 | 50 | 130 | 2 | 0.008 | 125 |",
    "| all lanes, cap 1000 split | 182 | 72 | 110 | 0 | 0.008 | 125 |",
    "| `length_5_8_smoke_candidate` | 46 | 40 |",
    "| `excluded_by_appellation_min_length` | 14 | 3 |",
    "| defined `c(w,w')` values | 72 |",
    "| P1 | 0.00252257011468 |",
    "| all lanes, cap 1000, program formula | 0 |",
    "direct all-lane cap 1000 defines 72 values, not 163.",
    "The 14 defined rows in `excluded_by_appellation_min_length` are diagnostic only",
    "Local locked-method language is governed by `docs/WRR_CLAIM_READINESS.md`; exact published reproduction remains caveated.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_direct_all_lanes_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR direct all-lane doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR direct all-lane doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_direct_all_lanes_doc(doc: Path) -> list[str]:
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
