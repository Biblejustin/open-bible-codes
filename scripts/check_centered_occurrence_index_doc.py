#!/usr/bin/env python3
"""Validate generated centered-occurrence index markdown freshness."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from scripts import build_centered_occurrence_index as builder


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_centered_occurrence_index_doc(args)
    if failures:
        for failure in failures:
            print(f"centered-occurrence index doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"centered-occurrence index doc ok: {args.markdown_out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all-codes-review", type=Path, default=builder.DEFAULT_ALL_CODES_REVIEW)
    parser.add_argument("--all-codes-selected", type=Path, default=builder.DEFAULT_ALL_CODES_SELECTED)
    parser.add_argument("--all-codes-context", type=Path, default=builder.DEFAULT_ALL_CODES_CONTEXT)
    parser.add_argument("--strong-queue", type=Path, default=builder.DEFAULT_STRONG_QUEUE)
    parser.add_argument("--strong-bundle", type=Path, default=builder.DEFAULT_STRONG_BUNDLE)
    parser.add_argument("--original-findings", type=Path, default=builder.DEFAULT_ORIGINAL_FINDINGS)
    parser.add_argument("--gog-source-review", type=Path, default=builder.DEFAULT_GOG_SOURCE_REVIEW)
    parser.add_argument("--gog-control-review", type=Path, default=builder.DEFAULT_GOG_CONTROL_REVIEW)
    parser.add_argument(
        "--apocrypha-bridge-context",
        type=Path,
        default=builder.DEFAULT_APOCRYPHA_BRIDGE_CONTEXT,
    )
    parser.add_argument(
        "--kjv-apocrypha-bridge-context",
        type=Path,
        default=builder.DEFAULT_KJV_APOCRYPHA_BRIDGE_CONTEXT,
    )
    parser.add_argument("--out", type=Path, default=builder.DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=builder.DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=builder.DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=builder.DEFAULT_MANIFEST)
    parser.add_argument("--markdown-row-limit", type=int, default=80)
    return parser


def validate_centered_occurrence_index_doc(
    args: argparse.Namespace | None = None,
) -> list[str]:
    args = args or build_parser().parse_args([])
    inputs = [
        args.all_codes_review,
        args.all_codes_selected,
        args.all_codes_context,
        args.strong_queue,
        args.strong_bundle,
        args.original_findings,
        args.gog_source_review,
        args.gog_control_review,
        args.apocrypha_bridge_context,
        args.kjv_apocrypha_bridge_context,
        args.out,
        args.summary_out,
        args.markdown_out,
        args.manifest_out,
    ]
    for path in inputs:
        if not path.exists():
            return [f"{path} is missing"]
    rows = builder.build_occurrences(args)
    summary_rows = builder.build_presence_summary(rows)
    failures: list[str] = []
    failures.extend(
        validate_csv(
            args.out,
            fieldnames=builder.FIELDNAMES,
            expected_rows=rows,
            label="centered occurrences",
        )
    )
    failures.extend(
        validate_csv(
            args.summary_out,
            fieldnames=builder.SUMMARY_FIELDNAMES,
            expected_rows=summary_rows,
            label="presence summary",
        )
    )
    failures.extend(validate_manifest(args.manifest_out, args, rows, summary_rows))
    expected = builder.render_markdown(rows, summary_rows, args)
    actual = args.markdown_out.read_text(encoding="utf-8")
    if actual != expected:
        failures.append(
            f"{args.markdown_out} is stale; rerun python3 -m scripts.build_centered_occurrence_index"
        )
    return failures


def validate_csv(
    path: Path,
    *,
    fieldnames: list[str],
    expected_rows: list[dict[str, object]],
    label: str,
) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    actual_fieldnames, actual_rows = data
    failures: list[str] = []
    if actual_fieldnames != fieldnames:
        failures.append(f"{path} {label} fieldnames drifted")
    expected = [_string_row(row, fieldnames) for row in expected_rows]
    if actual_rows != expected:
        failures.append(f"{path} {label} rows drifted")
    return failures


def validate_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[str]:
    data = _read_json(path)
    if isinstance(data, str):
        return [data]
    failures: list[str] = []
    expected_inputs = {
        "all_codes_review": str(args.all_codes_review),
        "all_codes_selected": str(args.all_codes_selected),
        "all_codes_context": str(args.all_codes_context),
        "strong_queue": str(args.strong_queue),
        "strong_bundle": str(args.strong_bundle),
        "original_findings": str(args.original_findings),
        "gog_source_review": str(args.gog_source_review),
        "gog_control_review": str(args.gog_control_review),
        "apocrypha_bridge_context": str(args.apocrypha_bridge_context),
        "kjv_apocrypha_bridge_context": str(args.kjv_apocrypha_bridge_context),
    }
    expected_outputs = {
        "out": str(args.out),
        "summary_out": str(args.summary_out),
        "markdown_out": str(args.markdown_out),
        "manifest_out": str(args.manifest_out),
    }
    checks: dict[str, Any] = {
        "script": "scripts/build_centered_occurrence_index.py",
        "rows": len(rows),
        "summary_rows": len(summary_rows),
        "type_counts": dict(Counter(str(row["occurrence_type"]) for row in rows)),
        "summary_type_counts": dict(
            Counter(str(row["occurrence_type"]) for row in summary_rows)
        ),
        "source_counts": dict(Counter(str(row["source_family"]) for row in rows)),
        "summary_source_counts": dict(
            Counter(str(row["source_family"]) for row in summary_rows)
        ),
        "inputs": expected_inputs,
        "outputs": expected_outputs,
    }
    for key, expected in checks.items():
        if data.get(key) != expected:
            failures.append(f"{path} {key} drifted")
    return failures


def _string_row(row: dict[str, object], fieldnames: list[str]) -> dict[str, str]:
    return {field: str(row.get(field, "")) for field in fieldnames}


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def _read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
