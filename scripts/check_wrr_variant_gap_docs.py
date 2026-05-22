#!/usr/bin/env python3
"""Validate WRR zero-hit variant and variant-gap docs stay diagnostic."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_ZERO_HIT_DOC = Path("docs/WRR_ZERO_HIT_VARIANT_PROBE.md")
DEFAULT_VARIANT_GAP_DOC = Path("docs/WRR_VARIANT_GAP_IMPACT.md")
DEFAULT_UPPER_BOUND_DOC = Path("docs/WRR_VARIANT_GAP_UPPER_BOUND.md")

ZERO_HIT_REQUIRED_PHRASES = (
    "# WRR Zero-Hit Variant Probe",
    "Status: diagnostic-only one-edit probe",
    "not a source correction",
    "not a WRR reproduction",
    "| wrr_appellation | 105 | 48 | 57 | 2981 |",
    "| wrr_date | 7 | 7 | 0 | 1358 |",
    "Variant hits are leads for source-normalization review only.",
)

VARIANT_GAP_REQUIRED_PHRASES = (
    "# WRR Variant Gap Impact",
    "Status: diagnostic-only join from current blocked WRR pair rows",
    "not a source correction",
    "not a WRR reproduction",
    "Best run label: `all_lanes_cap1000`.",
    "| `all_blocking_terms_have_variant_hit` | 51 |",
    "| `no_blocking_term_variant_hit` | 50 |",
    "| `some_blocking_terms_have_variant_hit` | 9 |",
    "Claim-grade work still needs source transcription and pair-rule locks.",
)

UPPER_BOUND_REQUIRED_PHRASES = (
    "# WRR Variant Gap Upper Bound",
    "Status: diagnostic-only upper bound.",
    "| all_lanes_cap1000 | 72 | 91 | 51 | 9 | 50 | 123 | 40 | 56.04 |",
    "Simple one-edit variant leads cover all blockers for at most 51 blocked pairs.",
    "Residual gap after that upper bound: 40.",
    "simple one-edit variants alone cannot explain the full 163-distance count gap",
    "accepting any variant still requires a citable source rule",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_variant_gap_docs(
        zero_hit_doc=args.zero_hit_doc,
        variant_gap_doc=args.variant_gap_doc,
        upper_bound_doc=args.upper_bound_doc,
    )
    if failures:
        for failure in failures:
            print(f"WRR variant-gap doc failure: {failure}", file=sys.stderr)
        return 1
    print(
        "WRR variant-gap docs ok: "
        f"{args.zero_hit_doc}, {args.variant_gap_doc}, {args.upper_bound_doc}"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zero-hit-doc", type=Path, default=DEFAULT_ZERO_HIT_DOC)
    parser.add_argument("--variant-gap-doc", type=Path, default=DEFAULT_VARIANT_GAP_DOC)
    parser.add_argument("--upper-bound-doc", type=Path, default=DEFAULT_UPPER_BOUND_DOC)
    return parser


def validate_variant_gap_docs(
    *,
    zero_hit_doc: Path = DEFAULT_ZERO_HIT_DOC,
    variant_gap_doc: Path = DEFAULT_VARIANT_GAP_DOC,
    upper_bound_doc: Path = DEFAULT_UPPER_BOUND_DOC,
) -> list[str]:
    return [
        *validate_doc(zero_hit_doc, ZERO_HIT_REQUIRED_PHRASES),
        *validate_doc(variant_gap_doc, VARIANT_GAP_REQUIRED_PHRASES),
        *validate_doc(upper_bound_doc, UPPER_BOUND_REQUIRED_PHRASES),
    ]


def validate_doc(doc: Path, required_phrases: tuple[str, ...]) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    return [
        f"{doc} missing phrase: {phrase}"
        for phrase in required_phrases
        if phrase not in text
    ]


if __name__ == "__main__":
    raise SystemExit(main())
