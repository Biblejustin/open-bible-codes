#!/usr/bin/env python3
"""Validate WRR post-lock reporting-boundary docs stay aligned."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from scripts import build_wrr_post_lock_reporting_boundary as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_CSV = builder.DEFAULT_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST

REQUIRED_PHRASES = (
    "# WRR Post-Lock Reporting Boundary",
    "Status: post-lock reporting boundary locked.",
    "allowed local locked-method language from forbidden exact-published reproduction language",
    "Local locked-method result: allowed with caveats.",
    "Exact published reproduction remains caveated by the 163-distance gap, not pending source-edit choices.",
    "Do not say exact published WRR reproduced.",
    "Current manual decision records keep 26 no_source_change rows and 11 method_lock rows.",
    "This is a reporting boundary, not a new statistical result.",
)

FORBIDDEN_PHRASES = (
    "Status: exact published WRR reproduced",
    "source corrections have been selected",
    "pair exclusions have been selected",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_post_lock_reporting_boundary_doc(
        args.doc,
        csv_path=args.csv,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"WRR post-lock reporting boundary failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR post-lock reporting boundary ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_post_lock_reporting_boundary_doc(
    doc: Path,
    *,
    csv_path: Path | None = DEFAULT_CSV,
    manifest: Path | None = DEFAULT_MANIFEST,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized
    ]
    failures.extend(
        f"{doc} contains unsupported phrase: {phrase}"
        for phrase in FORBIDDEN_PHRASES
        if normalize_space(phrase) in normalized
    )
    expected_rows = expected_boundary_rows()
    if csv_path is not None:
        failures.extend(validate_csv(csv_path, expected_rows))
    if manifest is not None:
        failures.extend(validate_manifest(manifest, expected_rows))
    return failures


def validate_csv(path: Path, expected_rows: list[dict[str, str]]) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        failures: list[str] = []
        if reader.fieldnames != builder.FIELDNAMES:
            failures.append(f"{path} fieldnames drifted")
        if rows != expected_rows:
            failures.append(f"{path} boundary rows drifted")
        by_key = {(row["section"], row["item"]): row for row in rows}
        checks = {
            ("allowed", "local_locked_method_language"): "ready",
            ("not_allowed", "exact_published_reproduction_language"): "forbidden",
            ("source_boundary", "source_changes"): "none_selected",
            ("residual_gap", "remaining_163_distance_gap"): "open",
            ("next_action", "post_lock_reporting_boundary"): "complete",
        }
        for key, status in checks.items():
            if by_key.get(key, {}).get("status") != status:
                failures.append(f"{path} {key} status drifted")
        return failures


def validate_manifest(
    path: Path,
    expected_rows: list[dict[str, str]],
) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path} is invalid JSON: {exc}"]
    if not isinstance(data, dict):
        return [f"{path} JSON root must be an object"]
    failures: list[str] = []
    expected_inputs = {
        "claim_readiness": str(builder.DEFAULT_CLAIM_READINESS),
        "locked_method_report": str(builder.DEFAULT_LOCKED_METHOD_REPORT),
        "dashboard": str(builder.DEFAULT_DASHBOARD),
        "priority_packet": str(builder.DEFAULT_PRIORITY_PACKET),
        "manual_decision_records": str(builder.DEFAULT_MANUAL_DECISION_RECORDS),
    }
    expected_outputs = {
        "out": str(builder.DEFAULT_OUT),
        "markdown": str(builder.DEFAULT_MD),
        "manifest": str(builder.DEFAULT_MANIFEST),
    }
    if data.get("tool") != "build_wrr_post_lock_reporting_boundary.py":
        failures.append(f"{path} tool drifted")
    if data.get("inputs") != expected_inputs:
        failures.append(f"{path} inputs drifted")
    if data.get("outputs") != expected_outputs:
        failures.append(f"{path} outputs drifted")
    if data.get("rows") != len(expected_rows):
        failures.append(f"{path} rows drifted")
    if data.get("boundary_rows") != expected_rows:
        failures.append(f"{path} boundary rows drifted")
    return failures


def expected_boundary_rows() -> list[dict[str, str]]:
    args = builder.build_parser().parse_args([])
    inputs = {
        "claim_readiness": builder.read_rows(args.claim_readiness),
        "locked_method_report": builder.read_rows(args.locked_method_report),
        "dashboard": builder.read_rows(args.dashboard),
        "priority_packet": builder.read_rows(args.priority_packet),
        "manual_decision_records": builder.read_rows(args.manual_decision_records),
    }
    return builder.build_boundary_rows(inputs, args)


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
