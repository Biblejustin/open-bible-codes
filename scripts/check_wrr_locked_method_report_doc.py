#!/usr/bin/env python3
"""Validate the WRR locked-method report keeps claim boundaries visible."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_wrr_locked_method_report as builder

DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_REPORT = builder.DEFAULT_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST

FIELDNAMES = builder.FIELDNAMES

EXPECTED_ROWS = {
    "report_status": (
        "status",
        "locked local WRR method report; not an exact published WRR reproduction",
        "locked_local_not_exact_reproduction",
    ),
    "Pair universe": ("lock", "keep_all_working_source", "source_locked"),
    "D(w)": (
        "lock",
        "printed WRR formula main; reported-program formula sensitivity",
        "source_locked",
    ),
    "corrected_distance": (
        "lock",
        "full selected universe cap1000; undefined ordinary-not-valid",
        "defined_full_run",
    ),
    "Permutation": ("lock", "999,999 date-label shuffles", "permutation_locked"),
    "Manual decisions": (
        "lock",
        "37 locked rows: 26 no_source_change; 11 method_lock",
        "locked",
    ),
    "observed_rows": (
        "local_result",
        "182",
        "diagnostic_only_not_wrr_reproduction",
    ),
    "defined_c_values": (
        "local_result",
        "72",
        "diagnostic_only_not_wrr_reproduction",
    ),
    "ordinary_not_valid": (
        "local_result",
        "110",
        "diagnostic_only_not_wrr_reproduction",
    ),
    "P-values": (
        "local_result",
        "P1=0.00252257011468; P2=1.16472976875e-05; "
        "P3=0.0184584022574; P4=0.000274264355592",
        "diagnostic_only_not_wrr_reproduction",
    ),
    "rho_values": (
        "local_result",
        "rho P1=0.019722; rho P2=0.000101; rho P3=0.0506065; "
        "rho P4=0.000535; rho0=0.000404",
        "diagnostic_only_not_wrr_reproduction",
    ),
    "Table 3 Genesis": (
        "published_anchor",
        "min statistic P4; rank 4; p0=0.000016",
        "found",
    ),
    "source_defined_gap": (
        "boundary",
        "defined 72 of 163; gap 91",
        "diagnostic_only_not_wrr_reproduction",
    ),
    "D(w) skip-cap formula": ("readiness_gate", "true", "source_locked"),
    "Corrected distance c(w,w')": (
        "readiness_gate",
        "true",
        "defined_full_run",
    ),
    "Aggregate statistic and permutation": (
        "readiness_gate",
        "true",
        "permutation_locked",
    ),
}

EXPECTED_DUPLICATE_ITEMS = {
    ("readiness_gate", "Pair universe"): ("true", "source_locked"),
}

REQUIRED_PHRASES = (
    "# WRR Locked Method Report",
    "Status: locked local WRR method report; not an exact published WRR reproduction.",
    "Pair universe: keep_all_working_source",
    "D(w): printed WRR formula main",
    "Permutation: 999,999 date-label shuffles",
    "Manual decisions: 37 locked rows",
    "26 no_source_change",
    "11 method_lock",
    "Defined c-values",
    "rho0 | 0.000404",
    "Exact published WRR reproduction remains caveated",
    "source-defined 163-distance gap",
    "current manual decision records keep the working source unchanged",
    "lock method-lane rows",
    "Do not describe this as an exact published WRR reproduction.",
    "source correction selected",
)

FORBIDDEN_PHRASES = (
    "exact published WRR reproduced",
    "proves WRR",
    "conclusive WRR",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_locked_method_report_doc(
        args.doc,
        args.report,
        args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"WRR locked-method report failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR locked-method report ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_locked_method_report_doc(
    doc: Path,
    report: Path | None = DEFAULT_REPORT,
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
    for phrase in FORBIDDEN_PHRASES:
        if phrase in text and f"- {phrase}" not in text:
            failures.append(f"{doc} forbidden phrase outside forbidden-language list: {phrase}")
    if report is not None:
        failures.extend(validate_report_csv(report))
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    return failures


def validate_report_csv(report: Path) -> list[str]:
    data = _read_csv(report)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != FIELDNAMES:
        failures.append(f"{report} fieldnames drifted")
    expected_count = len(EXPECTED_ROWS) + len(EXPECTED_DUPLICATE_ITEMS)
    if len(rows) != expected_count:
        failures.append(f"{report} has {len(rows)} rows; expected {expected_count}")

    keyed_rows = {
        (row.get("section", ""), row.get("item", "")): row
        for row in rows
    }
    expected_keys = {
        (section, item)
        for item, (section, _value, _status) in EXPECTED_ROWS.items()
    } | set(EXPECTED_DUPLICATE_ITEMS)
    if set(keyed_rows) != expected_keys:
        failures.append(f"{report} section/item set drifted")
    for item, (section, value, status) in EXPECTED_ROWS.items():
        row = keyed_rows.get((section, item))
        if row is None:
            continue
        failures.extend(_validate_row(report, item, row, section, value, status))

    for (section, item), (value, status) in EXPECTED_DUPLICATE_ITEMS.items():
        row = keyed_rows.get((section, item))
        if row is None:
            failures.append(f"{report} missing {section}/{item}")
            continue
        failures.extend(_validate_row(report, f"{section}/{item}", row, section, value, status))
    return failures


def _validate_row(
    report: Path,
    label: str,
    row: dict[str, str],
    section: str,
    value: str,
    status: str,
) -> list[str]:
    failures: list[str] = []
    if row.get("section") != section:
        failures.append(f"{report} {label} section drifted")
    if row.get("value") != value:
        failures.append(f"{report} {label} value drifted")
    if row.get("status") != status:
        failures.append(f"{report} {label} status drifted")
    if not row.get("evidence") or not row.get("source"):
        failures.append(f"{report} {label} missing evidence/source")
    return failures


def validate_manifest(manifest: Path) -> list[str]:
    data = _read_json(manifest)
    if isinstance(data, str):
        return [data]
    expected = {
        "tool": "build_wrr_locked_method_report",
        "inputs": {
            "method_status": str(builder.DEFAULT_METHOD_STATUS),
            "readiness": str(builder.DEFAULT_READINESS),
            "lock_options": str(builder.DEFAULT_LOCK_OPTIONS),
            "manual_worksheet": str(builder.DEFAULT_MANUAL_WORKSHEET),
            "corrected_distance_summary": str(builder.DEFAULT_CORRECTED_DISTANCE_SUMMARY),
            "corrected_distance_aggregate": str(builder.DEFAULT_CORRECTED_DISTANCE_AGGREGATE),
            "permutation_summary": str(builder.DEFAULT_PERMUTATION_SUMMARY),
            "primary_result_table": str(builder.DEFAULT_PRIMARY_RESULT_TABLE),
            "defined_pair_summary": str(builder.DEFAULT_DEFINED_PAIR_SUMMARY),
        },
        "outputs": {
            "out": str(DEFAULT_REPORT),
            "markdown_out": str(DEFAULT_DOC),
            "manifest_out": str(DEFAULT_MANIFEST),
        },
        "report_rows": len(EXPECTED_ROWS) + len(EXPECTED_DUPLICATE_ITEMS),
        "method_status_rows": 6,
        "manual_decision_rows": 37,
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
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
