#!/usr/bin/env python3
"""Validate the study-lock manifest drift audit doc and CSVs."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.audit_study_lock_manifest_drift import (
    AUDIT_STATUSES,
    DEFAULT_MANIFEST,
    DEFAULT_MARKDOWN,
    DEFAULT_OUT,
    DEFAULT_SUMMARY,
    FIELDNAMES,
    SUMMARY_FIELDNAMES,
)


REQUIRED_PHRASES = (
    "Status: historical audit, not a prospective approval.",
    "A drifted historical manifest is not a failed result.",
    "Use `scripts.check_study_lock_manifest` for one fresh, study-specific",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_doc(args.doc, args.rows, args.summary, args.manifest)
    if failures:
        for failure in failures:
            print(f"study-lock manifest drift audit failure: {failure}", file=sys.stderr)
        return 1
    print(f"study-lock manifest drift audit ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--rows", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_doc(
    doc: Path = DEFAULT_MARKDOWN,
    rows_path: Path = DEFAULT_OUT,
    summary_path: Path = DEFAULT_SUMMARY,
    manifest_path: Path = DEFAULT_MANIFEST,
) -> list[str]:
    failures: list[str] = []
    try:
        text = doc.read_text(encoding="utf-8")
        row_fields, rows = read_csv(rows_path)
        summary_fields, summary_rows = read_csv(summary_path)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, csv.Error, json.JSONDecodeError) as exc:
        return [f"could not read audit artifacts: {exc}"]

    if row_fields != FIELDNAMES:
        failures.append(f"{rows_path} fieldnames drifted: {row_fields}")
    if summary_fields != SUMMARY_FIELDNAMES:
        failures.append(f"{summary_path} fieldnames drifted: {summary_fields}")

    for phrase in REQUIRED_PHRASES:
        if phrase not in text:
            failures.append(f"{doc} missing phrase: {phrase}")

    expected_summary = expected_summary_rows(rows)
    observed_summary = {row["metric"]: row["value"] for row in summary_rows}
    if observed_summary != expected_summary:
        failures.append(
            f"{summary_path} does not match rows: observed={observed_summary} "
            f"expected={expected_summary}"
        )

    for metric, value in expected_summary.items():
        if f"- {metric}: {value}" not in text:
            failures.append(f"{doc} missing summary metric: {metric}={value}")

    for row in rows:
        path = row["manifest_path"]
        if path and f"`{path}`" not in text:
            failures.append(f"{doc} missing manifest row: {path}")

    if not isinstance(manifest, dict):
        failures.append(f"{manifest_path} JSON root must be an object")
    else:
        failures.extend(validate_manifest(manifest, manifest_path, rows_path, summary_path, doc))
    return failures


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def expected_summary_rows(rows: list[dict[str, str]]) -> dict[str, str]:
    counts = Counter(row["audit_status"] for row in rows)
    expected = {"total_manifests": str(len(rows))}
    for status in AUDIT_STATUSES:
        expected[status] = str(counts.get(status, 0))
    return expected


def validate_manifest(
    manifest: dict[str, Any],
    manifest_path: Path,
    rows_path: Path,
    summary_path: Path,
    doc: Path,
) -> list[str]:
    failures: list[str] = []
    if manifest.get("tool") != "audit_study_lock_manifest_drift":
        failures.append(f"{manifest_path} tool mismatch")
    output_paths = {
        output.get("path")
        for output in manifest.get("outputs", [])
        if isinstance(output, dict)
    }
    for path in [rows_path, summary_path, doc]:
        if path.as_posix() not in output_paths:
            failures.append(f"{manifest_path} missing output fingerprint: {path}")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
