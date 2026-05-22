#!/usr/bin/env python3
"""Validate WRR source-transcription evidence packet stays diagnostic."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_TRANSCRIPTION_EVIDENCE_PACKET.md")

REQUIRED_PHRASES = (
    "# WRR Source-Transcription Evidence Packet",
    "Status: diagnostic evidence packet for source-transcription residual terms.",
    "It does not choose source corrections, row edits, or pair exclusions.",
    "- Source-transcription action terms: 43.",
    "- Residual pair links: 44.",
    "- Minimum-frontier pair links: 35.",
    "- Row clusters: 22.",
    "| 1 | `06` | `WRR2 06` | 4 | 4 | 4 |",
    "`wrr2_27_app_13`",
    "`B@LQWLHRMZ`",
    "primary Table 2 row transcription or row-alignment evidence",
    "No automatic source correction",
    "Rows with multiple unresolved terms should be reviewed once by row",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_transcription_evidence_packet_doc(args.doc)
    if failures:
        for failure in failures:
            print(
                f"WRR source-transcription evidence packet failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"WRR source-transcription evidence packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_source_transcription_evidence_packet_doc(doc: Path) -> list[str]:
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
