#!/usr/bin/env python3
"""Validate WRR method-status doc keeps reproduction blockers explicit."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_METHOD_STATUS.md")
DEFAULT_STATUS = Path("reports/wrr_1994/wrr_method_status.csv")

EXPECTED_STATUS = {
    "Genesis text stream": "locally_locked",
    "WRR2 term source": "working_source_locked",
    "Pair universe": "source_locked",
    "D(w) skip-cap formula": "source_locked",
    "Corrected distance c(w,w')": "defined_full_run",
    "Aggregate statistic and permutation": "permutation_locked",
}

REQUIRED_PHRASES = (
    "# WRR Method Status",
    "Status: current audit matrix; not an exact published WRR reproduction.",
    "still has a 163-distance gap; current manual records do not authorize source edits",
    "| Genesis text stream | `locally_locked` |",
    "| WRR2 term source | `working_source_locked` |",
    "| Pair universe | `source_locked` |",
    "| D(w) skip-cap formula | `source_locked` |",
    "| Corrected distance c(w,w') | `defined_full_run` |",
    "| Aggregate statistic and permutation | `permutation_locked` |",
    "variant-gap impact best run",
    "variant residual review best run",
    "manual no-source-change locks visible",
    "Source Anchors",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_method_status_doc(args.doc, args.status)
    if failures:
        for failure in failures:
            print(f"WRR method-status doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR method-status doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--status", type=Path, default=DEFAULT_STATUS)
    return parser


def validate_method_status_doc(
    doc: Path,
    status: Path | None = DEFAULT_STATUS,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text
    ]
    if status is not None:
        failures.extend(validate_status_csv(status))
    return failures


def validate_status_csv(status: Path) -> list[str]:
    rows = _read_csv(status)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    if len(rows) != len(EXPECTED_STATUS):
        failures.append(f"{status} has {len(rows)} rows; expected {len(EXPECTED_STATUS)}")
    by_area = {row.get("decision_area", ""): row for row in rows}
    if set(by_area) != set(EXPECTED_STATUS):
        failures.append(f"{status} decision area set drifted")
    for area, expected_status in EXPECTED_STATUS.items():
        row = by_area.get(area)
        if row is None:
            continue
        if row.get("status") != expected_status:
            failures.append(f"{status} {area} status drifted")
        if not row.get("current_read") or not row.get("evidence") or not row.get("next_action"):
            failures.append(f"{status} {area} missing read/evidence/action")
    return failures


def _read_csv(path: Path) -> list[dict[str, str]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    raise SystemExit(main())
