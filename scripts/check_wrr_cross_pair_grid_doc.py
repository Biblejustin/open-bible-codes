#!/usr/bin/env python3
"""Validate WRR cross-pair grid doc stays aligned with locked local evidence."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_CROSS_PAIR_GRID.md")

REQUIRED_PHRASES = (
    "# WRR Cross-Pair Grid",
    "Status: locked local permutation evidence; exact published WRR reproduction remains caveated.",
    "| pairs | 5208 |",
    "| same-record source pairs | 182 |",
    "| cross-record permutation pairs | 5026 |",
    "| defined `c(w,w')` rows | 1423 |",
    "| P1 | 0.321861824814 |",
    "legacy repo-defined diagnostics over the cap-250 corrected-distance field, not exact WRR reproductions.",
    "| permutations | 1000 |",
    "| observed defined `c(w,w')` values | 50 |",
    "| Bonferroni rho0 | 0.003996003996 |",
    "Legacy repo-defined 999,999-permutation run:",
    "| permutations | 999999 |",
    "| observed defined `c(w,w')` values | 48 |",
    "| Bonferroni rho0 | 0.00086 |",
    "## Cap-1000 Corrected-Distance Matrix",
    "| defined `c(w,w')` rows | 2013 |",
    "| P1 | 6.65545084562e-07 |",
    "| P2 | 7.6208422043e-09 |",
    "## Locked Cap-1000 Date-Permutation Run",
    "claim-grade for the repo-defined local lock policy",
    "| pair universe | selected full WRR2 source universe |",
    "| corrected-distance input | cap-1000 `corrected_distance` field |",
    "| observed source rows | 182 |",
    "| observed defined `c(w,w')` values | 72 |",
    "| rho P1 | 0.019722 |",
    "| rho P2 | 0.000101 |",
    "| Bonferroni rho0 | 0.000404 |",
    "Visual-review notes do not change pair inclusion until an explicit source policy is selected.",
    "Cap-1000 corrected-distance and date-permutation output from this grid is the locked local evidence path",
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
