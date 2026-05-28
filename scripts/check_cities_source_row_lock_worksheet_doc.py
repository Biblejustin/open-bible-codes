#!/usr/bin/env python3
"""Validate Cities source-row lock worksheet stays pre-import."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from scripts import build_cities_source_row_lock_worksheet as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_ROWS = builder.DEFAULT_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_QUEUE = builder.DEFAULT_QUEUE
DEFAULT_RECORDS = builder.DEFAULT_RECORDS

REQUIRED_PHRASES = (
    "# Cities Source Row Lock Worksheet",
    "Status: worksheet plus current Cities source-row lock decision-record status.",
    "does not update either file",
    "No OCR body text or source-script body text appears",
    "Worksheet rows: 14.",
    "Table-bearing candidate pages: 4.",
    "Source-list candidate pages: 5.",
    "Exception-note candidate pages: 5.",
    "Recorded decision rows: 1.",
    "Locked decision rows: 1.",
    "Unrecorded decision rows: 13.",
    "Source-row imports: 0.",
    "ELS runs: 0.",
    "Compactness runs: 0.",
    "Recorded selected actions: source_row_lock_ready=1.",
    "source_row_lock_ready",
    "`cities_source_row_lock_001`",
    "`cities_source_row_lock_014`",
    "never imports or transcribes source rows",
    "CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md",
    "recovered PDF metadata and page-image paths",
    "## Decision Meanings",
    "`source_row_lock_ready` means page evidence can support later source-row extraction",
    "`no_source_row_import` means do not use this page for source-row extraction",
    "`exclude_page_from_source_rows` means explicitly keep this page out",
    "`deferred_no_lock` means no lock decision yet",
)

EXPECTED_IDS = tuple(f"cities_source_row_lock_{index:03d}" for index in range(1, 15))
EXPECTED_LOCKED_DECISIONS = {
    "cities_source_row_lock_001": "source_row_lock_ready",
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_row_lock_worksheet_doc(
        args.doc,
        args.rows,
        args.manifest,
        args.queue,
        args.records,
    )
    if failures:
        for failure in failures:
            print(
                f"Cities source-row lock worksheet doc failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities source-row lock worksheet doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--records", type=Path, default=DEFAULT_RECORDS)
    return parser


def validate_cities_source_row_lock_worksheet_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    manifest_json: Path = DEFAULT_MANIFEST,
    queue_csv: Path = DEFAULT_QUEUE,
    records_csv: Path = DEFAULT_RECORDS,
) -> list[str]:
    missing = [
        str(path)
        for path in (doc, rows_csv, manifest_json, queue_csv, records_csv)
        if not path.exists()
    ]
    if missing:
        return ["missing required files: " + ", ".join(missing)]
    text = doc.read_text(encoding="utf-8")
    rows_text = rows_csv.read_text(encoding="utf-8")
    manifest_text = manifest_json.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    rows_data = read_csv(rows_csv)
    queue_data = read_csv(queue_csv)
    records_data = read_csv(records_csv)
    for data in (rows_data, queue_data, records_data):
        if isinstance(data, str):
            return [data]
    _, rows = rows_data
    _, queue_rows = queue_data
    _, record_rows = records_data
    expected_rows = builder.build_worksheet_rows(
        queue_rows,
        builder.records_by_decision_id(record_rows),
    )
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized
    ]
    failures.extend(
        validate_no_source_text(
            {
                str(doc): text,
                str(rows_csv): rows_text,
                str(manifest_json): manifest_text,
            }
        )
    )
    failures.extend(validate_rows_csv(rows_csv, rows_data, expected_rows))
    failures.extend(
        validate_manifest(manifest_json, queue_csv, records_csv, expected_rows)
    )
    failures.extend(validate_rows(doc, normalized, rows))
    return failures


def validate_no_source_text(text_by_name: dict[str, str]) -> list[str]:
    failures: list[str] = []
    for name, text in text_by_name.items():
        if contains_hebrew_or_greek(text):
            failures.append(f"{name} appears to contain source-script body text")
    return failures


def validate_rows_csv(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
    expected_rows: list[dict[str, str]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != builder.FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if rows != expected_rows:
        failures.append(f"{path} row data drifted")
    return failures


def validate_manifest(
    path: Path,
    queue_csv: Path,
    records_csv: Path,
    expected_rows: list[dict[str, str]],
) -> list[str]:
    data = read_json(path)
    if isinstance(data, str):
        return [data]
    status_counts = Counter(row["record_decision_status"] for row in expected_rows)
    action_counts = Counter(
        row["record_selected_action"]
        for row in expected_rows
        if row["record_selected_action"]
    )
    checks: dict[str, Any] = {
        "tool": "build_cities_source_row_lock_worksheet.py",
        "inputs": {
            "queue": str(queue_csv),
            "records_template": str(records_csv),
        },
        "outputs": {
            "csv": str(DEFAULT_ROWS),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "rows": len(expected_rows),
        "class_counts": dict(Counter(row["page_class"] for row in expected_rows)),
        "record_status_counts": dict(status_counts),
        "recorded_action_counts": dict(action_counts),
        "recorded_rows": sum(
            1 for row in expected_rows if row["record_decision_status"] != "unrecorded"
        ),
        "locked_rows": status_counts["locked"],
        "source_row_imports": builder.count_imports(expected_rows),
        "els_runs": 0,
        "compactness_runs": 0,
        "claim_boundary": builder.CLAIM_BOUNDARY,
    }
    failures: list[str] = []
    for key, expected in checks.items():
        if data.get(key) != expected:
            failures.append(f"{path} {key} drifted")
    return failures


def validate_rows(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    ids = [row.get("decision_id", "") for row in rows]
    if tuple(ids) != EXPECTED_IDS:
        failures.append("rows CSV decision ids do not match expected 1..14 sequence")
    for row in rows:
        decision_id = row.get("decision_id", "")
        if row.get("source_row_use") != "no_source_row_use":
            failures.append(f"rows CSV {decision_id} allows source-row use")
        if row.get("current_decision") != "no_source_row_import":
            failures.append(f"rows CSV {decision_id} imports source row")
        expected_action = EXPECTED_LOCKED_DECISIONS.get(decision_id)
        if expected_action:
            if row.get("record_decision_status") != "locked":
                failures.append(f"rows CSV {decision_id} must be locked")
            if row.get("record_selected_action") != expected_action:
                failures.append(
                    f"rows CSV {decision_id} action must be {expected_action}"
                )
        else:
            if row.get("record_decision_status") != "unrecorded":
                failures.append(f"rows CSV {decision_id} unexpectedly has a lock record")
            if row.get("record_selected_action"):
                failures.append(f"rows CSV {decision_id} unexpectedly has selected action")
        if decision_id and decision_id not in normalized_doc:
            failures.append(f"{doc} missing decision id: {decision_id}")
    return failures


def contains_hebrew_or_greek(text: str) -> bool:
    for char in text:
        code = ord(char)
        if 0x0590 <= code <= 0x05FF or 0x0370 <= code <= 0x03FF:
            return True
    return False


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
