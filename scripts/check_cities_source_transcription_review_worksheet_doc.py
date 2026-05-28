#!/usr/bin/env python3
"""Validate Cities source-transcription worksheet stays no-input."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_source_transcription_review_worksheet as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_ROWS = builder.DEFAULT_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_EVIDENCE_PACKET = builder.DEFAULT_EVIDENCE_PACKET
DEFAULT_RECORDS = builder.DEFAULT_RECORDS

EXPECTED_IDS = tuple(
    f"cities_source_transcription_{index:03d}" for index in range(1, 15)
)

REQUIRED_PHRASES = (
    "# Cities Source Transcription Review Worksheet",
    "Status: no-input worksheet for future Cities source-row transcription review.",
    "does not transcribe rows or import source rows",
    "No OCR body text or source-script body text appears",
    "Rows needing transcription review: 14.",
    "Locked source pages: 14.",
    "Table-bearing candidate pages: 4.",
    "Source-list candidate pages: 5.",
    "Exception-note candidate pages: 5.",
    "Transcription decision rows recorded: 0.",
    "Unrecorded transcription decision rows: 14.",
    "Review state: `pending_readable_transcription`.",
    "Source-row imports: 0.",
    "City-name normalization: 0.",
    "ELS runs: 0.",
    "Compactness runs: 0.",
    "p-levels: 0.",
    "readable Hebrew transcription plus row/column alignment evidence",
    "`cities_source_transcription_001`",
    "`cities_source_transcription_014`",
    "This worksheet organizes review work only.",
    "Locked source pages are not source rows.",
    "before any source row can be imported",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_transcription_review_worksheet_doc(
        args.doc,
        args.rows,
        args.manifest,
        args.evidence_packet,
        args.records,
    )
    if failures:
        for failure in failures:
            print(
                f"Cities source-transcription review worksheet failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities source-transcription review worksheet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--evidence-packet", type=Path, default=DEFAULT_EVIDENCE_PACKET)
    parser.add_argument("--records", type=Path, default=DEFAULT_RECORDS)
    return parser


def validate_cities_source_transcription_review_worksheet_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    manifest_json: Path = DEFAULT_MANIFEST,
    evidence_packet_csv: Path = DEFAULT_EVIDENCE_PACKET,
    records_csv: Path = DEFAULT_RECORDS,
) -> list[str]:
    missing = [
        str(path)
        for path in (doc, rows_csv, manifest_json, evidence_packet_csv, records_csv)
        if not path.exists()
    ]
    if missing:
        return ["missing required files: " + ", ".join(missing)]
    text = doc.read_text(encoding="utf-8")
    rows_text = rows_csv.read_text(encoding="utf-8")
    manifest_text = manifest_json.read_text(encoding="utf-8")
    records_text = records_csv.read_text(encoding="utf-8")
    normalized = normalize_space(text)

    rows_data = read_csv(rows_csv)
    evidence_data = read_csv(evidence_packet_csv)
    records_data = read_csv(records_csv)
    for data in (rows_data, evidence_data, records_data):
        if isinstance(data, str):
            return [data]

    _, rows = rows_data
    _, evidence_rows = evidence_data
    record_fieldnames, record_rows = records_data
    expected_rows = builder.build_worksheet_rows(
        evidence_rows,
        builder.records_by_transcription_id(record_rows),
    )
    manifest = read_json(manifest_json)

    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized
    ]
    failures.extend(
        validate_no_source_text(
            {
                doc: text,
                rows_csv: rows_text,
                manifest_json: manifest_text,
                records_csv: records_text,
            }
        )
    )
    failures.extend(validate_records_template(records_csv, record_fieldnames, record_rows))
    failures.extend(validate_rows_csv(rows_csv, rows_data, expected_rows))
    failures.extend(validate_rows(doc, normalized, rows))
    failures.extend(validate_manifest(manifest_json, manifest, expected_rows, evidence_packet_csv, records_csv))
    return failures


def validate_records_template(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    if fieldnames != builder.RECORD_FIELDS:
        failures.append(f"{path} fieldnames drifted")
    for index, row in enumerate(rows, start=1):
        if row.get("selected_action") == "transcription_ready_for_import":
            failures.append(
                f"{path} row {index} selects source-row import without manual preflight"
            )
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


def validate_rows(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    if len(rows) != 14:
        failures.append(f"rows CSV has {len(rows)} rows, expected 14")
    ids = [row.get("transcription_decision_id", "") for row in rows]
    if tuple(ids) != EXPECTED_IDS:
        failures.append("rows CSV transcription ids do not match expected 1..14 sequence")
    for row in rows:
        decision_id = row.get("transcription_decision_id", "")
        if row.get("lock_record_decision_status") != "locked":
            failures.append(f"rows CSV {decision_id} source lock is not locked")
        if row.get("lock_record_selected_action") != "source_row_lock_ready":
            failures.append(f"rows CSV {decision_id} source lock is not ready")
        if row.get("review_state") != builder.REVIEW_STATE:
            failures.append(f"rows CSV {decision_id} review state drifted")
        for field in (
            "source_row_import",
            "city_name_normalization",
            "els_runs",
            "compactness_runs",
            "p_levels",
        ):
            if row.get(field) != "0":
                failures.append(f"rows CSV {decision_id} {field} must be 0")
        if row.get("current_transcription_status") != "unrecorded":
            failures.append(f"rows CSV {decision_id} unexpectedly has transcription record")
        if decision_id and decision_id not in normalized_doc:
            failures.append(f"{doc} missing transcription decision id: {decision_id}")
    return failures


def validate_manifest(
    path: Path,
    data: dict[str, Any] | str,
    expected_rows: list[dict[str, str]],
    evidence_packet_csv: Path,
    records_csv: Path,
) -> list[str]:
    if isinstance(data, str):
        return [data]
    expected: dict[str, Any] = {
        "tool": "build_cities_source_transcription_review_worksheet.py",
        "inputs": {
            "evidence_packet": str(evidence_packet_csv),
            "records_template": str(records_csv),
        },
        "outputs": {
            "csv": str(DEFAULT_ROWS),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "rows": len(expected_rows),
        "locked_source_pages": builder.locked_source_pages(expected_rows),
        "class_counts": {
            "table_candidate_page": 4,
            "source_list_candidate_page": 5,
            "exception_note_candidate_page": 5,
        },
        "transcription_record_status_counts": {"unrecorded": len(expected_rows)},
        "recorded_rows": 0,
        "source_row_imports": 0,
        "city_name_normalization": 0,
        "els_runs": 0,
        "compactness_runs": 0,
        "p_levels": 0,
        "review_state": builder.REVIEW_STATE,
        "claim_boundary": builder.CLAIM_BOUNDARY,
    }
    failures: list[str] = []
    for key, value in expected.items():
        if data.get(key) != value:
            failures.append(f"{path} {key} drifted")
    return failures


def validate_no_source_text(texts_by_path: dict[Path, str]) -> list[str]:
    failures: list[str] = []
    for path, text in texts_by_path.items():
        if contains_hebrew_or_greek(text):
            failures.append(f"{path} appears to contain source-script body text")
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
