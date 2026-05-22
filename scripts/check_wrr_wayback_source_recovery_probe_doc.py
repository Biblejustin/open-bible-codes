#!/usr/bin/env python3
"""Validate WRR Wayback source-recovery probe doc keeps archive limits explicit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_WAYBACK_SOURCE_RECOVERY_PROBE.md")

REQUIRED_PHRASES = (
    "# WRR Wayback Source Recovery Probe",
    "Status: archived-source recovery probe only.",
    "does not update the cached `reports/wrr_1994/` bundle",
    "claim-ready source decisions",
    "| Wayback URLs probed | 18 |",
    "| unique research concepts probed | 9 |",
    "| rows with archived snapshot | 5 |",
    "| rows where expected label appeared | 5 |",
    "| unrelated slot/gambling markers | 0 |",
    "| usable archived source rows | 5 |",
    "| usable archived concepts | 5 |",
    "| missing archived concepts | 4 |",
    "Current archive recovery status: `partial_archived_sources_recovered`.",
    "geometric-model or ELS-model pages",
    "WRR residual",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_wayback_source_recovery_probe_doc(args.doc)
    if failures:
        for failure in failures:
            print(
                f"WRR Wayback source-recovery probe doc failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"WRR Wayback source-recovery probe doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_wayback_source_recovery_probe_doc(doc: Path) -> list[str]:
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
