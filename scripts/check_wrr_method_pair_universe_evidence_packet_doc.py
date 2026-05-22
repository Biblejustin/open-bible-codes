#!/usr/bin/env python3
"""Validate WRR method/pair-universe evidence packet stays diagnostic."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_METHOD_PAIR_UNIVERSE_EVIDENCE_PACKET.md")

REQUIRED_PHRASES = (
    "# WRR Method/Pair-Universe Evidence Packet",
    "Status: diagnostic packet for OCR-matched WRR residual terms.",
    "It does not choose source corrections, method changes, or pair exclusions.",
    "- Method/pair-universe action terms: 11.",
    "- OCR-matched terms: 11.",
    "- Zero skip-250 appellation counts: 11.",
    "- Zero high-cap appellation ordinary hits: 11.",
    "`wrr2_02_app_03`",
    "`ZR@ABRHM`",
    "`wrr2_31_app_09`",
    "`$LWMMZRXY`",
    "OCR match is not enough to define a WRR corrected distance.",
    "Zero ordinary hits keep these rows in method or pair-universe review.",
    "No row here changes the working source or excludes a pair automatically.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_method_pair_universe_evidence_packet_doc(args.doc)
    if failures:
        for failure in failures:
            print(
                f"WRR method/pair-universe evidence packet failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"WRR method/pair-universe evidence packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_method_pair_universe_evidence_packet_doc(doc: Path) -> list[str]:
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
