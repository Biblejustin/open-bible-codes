#!/usr/bin/env python3
"""Validate tracked WRR claim-readiness docs keep blocker language visible."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import check_wrr_claim_readiness as generator

DEFAULT_DOC = generator.DEFAULT_MD
DEFAULT_READINESS = generator.DEFAULT_OUT
DEFAULT_MANIFEST = generator.DEFAULT_MANIFEST

FIELDNAMES = generator.FIELDNAMES

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
    failures = validate_readiness_doc(args.doc, args.readiness, args.manifest)
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
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_readiness_doc(
    doc: Path,
    readiness: Path | None = DEFAULT_READINESS,
    manifest: Path | None = DEFAULT_MANIFEST,
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
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    return failures


def validate_readiness_csv(readiness: Path) -> list[str]:
    data = _read_csv(readiness)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != FIELDNAMES:
        failures.append(f"{readiness} fieldnames drifted")
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


def validate_manifest(manifest: Path) -> list[str]:
    data = _read_json(manifest)
    if isinstance(data, str):
        return [data]
    expected = {
        "tool": "check_wrr_claim_readiness.py",
        "status": "ready",
        "input": str(generator.DEFAULT_STATUS),
        "outputs": {
            "csv": str(DEFAULT_READINESS),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
    }
    failures: list[str] = []
    for key, value in expected.items():
        if data.get(key) != value:
            failures.append(f"{manifest} {key} drifted")
    return failures


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def _read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return f"{path} is invalid JSON: {exc}"
    if not isinstance(data, dict):
        return f"{path} JSON root must be an object"
    return data


if __name__ == "__main__":
    raise SystemExit(main())
