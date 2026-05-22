#!/usr/bin/env python3
"""Validate WRR zero-hit variant and variant-gap docs stay diagnostic."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_ZERO_HIT_DOC = Path("docs/WRR_ZERO_HIT_VARIANT_PROBE.md")
DEFAULT_VARIANT_GAP_DOC = Path("docs/WRR_VARIANT_GAP_IMPACT.md")

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


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_variant_gap_docs(
        zero_hit_doc=args.zero_hit_doc,
        variant_gap_doc=args.variant_gap_doc,
    )
    if failures:
        for failure in failures:
            print(f"WRR variant-gap doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR variant-gap docs ok: {args.zero_hit_doc}, {args.variant_gap_doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zero-hit-doc", type=Path, default=DEFAULT_ZERO_HIT_DOC)
    parser.add_argument("--variant-gap-doc", type=Path, default=DEFAULT_VARIANT_GAP_DOC)
    return parser


def validate_variant_gap_docs(
    *,
    zero_hit_doc: Path = DEFAULT_ZERO_HIT_DOC,
    variant_gap_doc: Path = DEFAULT_VARIANT_GAP_DOC,
) -> list[str]:
    return [
        *validate_doc(zero_hit_doc, ZERO_HIT_REQUIRED_PHRASES),
        *validate_doc(variant_gap_doc, VARIANT_GAP_REQUIRED_PHRASES),
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
