#!/usr/bin/env python3
"""Validate WRR D(w) formula sensitivity doc stays diagnostic."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_DW_FORMULA_SENSITIVITY.md")

REQUIRED_PHRASES = (
    "# WRR D(w) Formula Sensitivity",
    "Status: diagnostic-only sensitivity packet. No `D(w)` formula is selected.",
    "printed WRR skip-cap formula",
    "reported WRR-program",
    "| skip_cap_profile | 120 |",
    "| smoke_length_5_8_cap250 | 86 | 28 | 28 |",
    "| all_lanes_cap1000 | 182 | 72 | 72 | 0 |",
    "| Program cap below printed | 13 |",
    "| Program cap equal printed | 107 |",
    "No pair rows changed between all-lane cap-1000 printed and program formula outputs.",
    "The formula choice remains open for claim-grade WRR reproduction.",
    "This packet lowers diagnostic risk; it does not lock `D(w)`.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_dw_formula_sensitivity_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR D(w) formula sensitivity doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR D(w) formula sensitivity doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_dw_formula_sensitivity_doc(doc: Path) -> list[str]:
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
