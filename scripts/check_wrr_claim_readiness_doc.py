#!/usr/bin/env python3
"""Validate tracked WRR claim-readiness docs keep blocker language visible."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_CLAIM_READINESS.md")
DEFAULT_READINESS = Path("reports/wrr_1994/wrr_claim_readiness.csv")

EXPECTED_ROWS = {
    "Pair universe": ("source_locked", "locked,source_locked"),
    "D(w) skip-cap formula": ("source_locked", "locked,source_locked"),
    "Corrected distance c(w,w')": (
        "defined_full_run",
        "defined_full_run,full_run_locked",
    ),
    "Aggregate statistic and permutation": (
        "permutation_locked",
        "claim_grade_ready,permutation_locked",
    ),
}

REQUIRED_PHRASES = (
    "Status: ready for claim-grade WRR locked-method language.",
    "Pair universe",
    "D(w) skip-cap formula",
    "Corrected distance c(w,w')",
    "Aggregate statistic and permutation",
    "variant-gap impact best run",
    "`permutation_locked`",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_readiness_doc(args.doc, args.readiness)
    if failures:
        for failure in failures:
            print(f"WRR claim-readiness doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR claim-readiness doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--readiness", type=Path, default=DEFAULT_READINESS)
    return parser


def validate_readiness_doc(
    doc: Path,
    readiness: Path | None = DEFAULT_READINESS,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text
    ]
    if readiness is not None:
        failures.extend(validate_readiness_csv(readiness))
    return failures


def validate_readiness_csv(readiness: Path) -> list[str]:
    rows = _read_csv(readiness)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    if len(rows) != len(EXPECTED_ROWS):
        failures.append(f"{readiness} has {len(rows)} rows; expected {len(EXPECTED_ROWS)}")
    by_area = {row.get("decision_area", ""): row for row in rows}
    if set(by_area) != set(EXPECTED_ROWS):
        failures.append(f"{readiness} decision area set drifted")
    for area, (status, required_statuses) in EXPECTED_ROWS.items():
        row = by_area.get(area)
        if row is None:
            continue
        if row.get("status") != status:
            failures.append(f"{readiness} {area} status drifted")
        if row.get("required_statuses") != required_statuses:
            failures.append(f"{readiness} {area} required statuses drifted")
        if row.get("ready") != "true":
            failures.append(f"{readiness} {area} readiness drifted")
        if row.get("blocker"):
            failures.append(f"{readiness} {area} blocker drifted")
        if not row.get("current_read") or not row.get("evidence"):
            failures.append(f"{readiness} {area} missing read/evidence")
    return failures


def _read_csv(path: Path) -> list[dict[str, str]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    raise SystemExit(main())
