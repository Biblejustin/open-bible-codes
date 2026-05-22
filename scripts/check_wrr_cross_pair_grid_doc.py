#!/usr/bin/env python3
"""Validate WRR cross-pair grid doc stays diagnostic."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_CROSS_PAIR_GRID.md")

REQUIRED_PHRASES = (
    "# WRR Cross-Pair Grid",
    "Status: diagnostic-only, not a WRR reproduction.",
    "| pairs | 5208 |",
    "| same-record source pairs | 182 |",
    "| cross-record permutation pairs | 5026 |",
    "| defined `c(w,w')` rows | 1423 |",
    "| P1 | 0.321861824814 |",
    "repo-defined diagnostics over the current cap-250 corrected-distance field, not exact WRR reproductions.",
    "| permutations | 1000 |",
    "| observed defined `c(w,w')` values | 50 |",
    "| Bonferroni rho0 | 0.003996003996 |",
    "Recommended repo-defined 999,999-permutation run:",
    "| permutations | 999999 |",
    "| observed defined `c(w,w')` values | 48 |",
    "| Bonferroni rho0 | 0.00086 |",
    "Corrected-distance and date-permutation output from this grid is diagnostic",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cross_pair_grid_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR cross-pair grid doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR cross-pair grid doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_cross_pair_grid_doc(doc: Path) -> list[str]:
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
