#!/usr/bin/env python3
"""Validate WRR source-recovery probe doc keeps live-source limits explicit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_RECOVERY_PROBE.md")

REQUIRED_PHRASES = (
    "# WRR Source Recovery Probe",
    "Status: live-source recovery probe only.",
    "does not update the cached `reports/wrr_1994/` bundle",
    "claim-ready source decisions",
    "| downloads probed | 15 |",
    "| rows where expected label appeared | 0 |",
    "| redirected rows | 15 |",
    "| final URL is Torah-code root | 15 |",
    "| canonical URL is Torah-code root | 15 |",
    "| unrelated slot/gambling markers | 15 |",
    "| usable current source rows | 0 |",
    "Current recovery status: `no_live_sources_recovered`.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_recovery_probe_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR source-recovery probe doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source-recovery probe doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_source_recovery_probe_doc(doc: Path) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    return [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text
    ]


if __name__ == "__main__":
    raise SystemExit(main())
