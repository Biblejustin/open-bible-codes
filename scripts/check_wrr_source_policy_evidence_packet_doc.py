#!/usr/bin/env python3
"""Validate WRR source-policy evidence packet stays diagnostic."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_POLICY_EVIDENCE_PACKET.md")

REQUIRED_PHRASES = (
    "# WRR Source-Policy Evidence Packet",
    "Status: diagnostic evidence packet for source-policy residual terms.",
    "It does not choose a source correction, exclude a pair, or lock a replacement.",
    "- Priority source-policy terms: 1.",
    "- Related source-review rows: 2.",
    "- Related scenario-pair rows: 4.",
    "- WNP context blocks: 3.",
    "| 1 | `wrr2_32_app_05` | `$LMHMX@LMA` | `WRR2 32` | `wnp_chelm_spelling_context` |",
    "`wrr2_32_app_04`",
    "`RBY$LMH`",
    "`/KA/TMWZ`",
    "`reports/wrr_1994/wnp_en.html:608-619`",
    "`review_chelm_spelling_only`",
    "source/pair-rule review",
    "No automatic correction or exclusion",
    "WNP context supports why the Chełm forms are in review scope, not a final pair-rule decision.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_policy_evidence_packet_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR source-policy evidence packet failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source-policy evidence packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_source_policy_evidence_packet_doc(doc: Path) -> list[str]:
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
