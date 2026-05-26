#!/usr/bin/env python3
"""Validate Cities PDF recovery probe doc keeps source limits explicit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/CITIES_PDF_RECOVERY_PROBE.md")

REQUIRED_PHRASES = (
    "# Cities PDF Recovery Probe",
    "Status: live/archive PDF recovery probe only.",
    "does not update the cached `reports/wrr_1994/` bundle",
    "does not make claim-ready source decisions",
    "| PDF URLs probed | 35 |",
    "Current PDF recovery status:",
    "Recovered PDF bytes are source-shape inputs only.",
    "city-name normalization",
    "ELS searches",
    "p-level verification",
)

EXPECTED_LABELS = (
    "cities_pdf_gans_original_report",
    "cities_pdf_dp364_appendix_4",
    "cities_pdf_margoliot_cities_data",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_pdf_recovery_probe_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"Cities PDF recovery probe doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities PDF recovery probe doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_cities_pdf_recovery_probe_doc(doc: Path) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized
    ]
    present_labels = probe_labels(text)
    missing = sorted(set(EXPECTED_LABELS) - present_labels)
    if missing:
        failures.append(f"{doc} missing probe labels: " + ", ".join(missing))
    return failures


def probe_labels(text: str) -> set[str]:
    labels: set[str] = set()
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 6 and cells[0].startswith("cities_pdf_"):
            labels.add(cells[0])
    return labels


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
