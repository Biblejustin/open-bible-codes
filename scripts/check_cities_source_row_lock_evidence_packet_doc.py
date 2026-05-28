#!/usr/bin/env python3
"""Validate Cities source-row lock evidence packet stays diagnostic."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from typing import Any
from pathlib import Path

from scripts import build_cities_source_row_lock_evidence_packet as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_ROWS = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_WORKSHEET = builder.DEFAULT_WORKSHEET
DEFAULT_SOURCE_QUEUE = builder.DEFAULT_SOURCE_QUEUE
EXPECTED_LOCKED_DECISIONS = {
    f"cities_source_row_lock_{index:03d}": "source_row_lock_ready"
    for index in range(1, 15)
}

REQUIRED_PHRASES = (
    "# Cities Source Row Lock Evidence Packet",
    "Status: diagnostic evidence packet for Cities source-row lock candidates.",
    "joins decision ids to PDF/source metadata and page-image paths",
    "does not transcribe rows",
    "No OCR body text or source-script body text appears",
    "checker verifies every packet row points to an existing recovered PDF and page-image artifact",
    "Evidence rows: 14.",
    "Unique labels: 3.",
    "Table-bearing candidate pages: 4.",
    "Source-list candidate pages: 5.",
    "Exception-note candidate pages: 5.",
    "Recorded decision rows: 14.",
    "Source-row imports: 0.",
    "ELS runs: 0.",
    "Compactness runs: 0.",
    "`cities_source_row_lock_001`",
    "`cities_source_row_lock_014`",
    "This packet collects evidence locations only.",
    "does not copy their body text",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_row_lock_evidence_packet_doc(
        args.doc,
        args.rows,
        args.summary,
        args.manifest,
        args.worksheet,
        args.source_queue,
    )
    if failures:
        for failure in failures:
            print(
                f"Cities source-row lock evidence packet doc failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities source-row lock evidence packet doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--worksheet", type=Path, default=DEFAULT_WORKSHEET)
    parser.add_argument("--source-queue", type=Path, default=DEFAULT_SOURCE_QUEUE)
    return parser


def validate_cities_source_row_lock_evidence_packet_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    summary_csv: Path = DEFAULT_SUMMARY,
    manifest_json: Path = DEFAULT_MANIFEST,
    worksheet_csv: Path = DEFAULT_WORKSHEET,
    source_queue_csv: Path = DEFAULT_SOURCE_QUEUE,
) -> list[str]:
    missing = [
        str(path)
        for path in (
            doc,
            rows_csv,
            summary_csv,
            manifest_json,
            worksheet_csv,
            source_queue_csv,
        )
        if not path.exists()
    ]
    if missing:
        return ["missing required files: " + ", ".join(missing)]
    text = doc.read_text(encoding="utf-8")
    rows_text = rows_csv.read_text(encoding="utf-8")
    summary_text = summary_csv.read_text(encoding="utf-8")
    manifest_text = manifest_json.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    rows_fieldnames, rows = read_csv(rows_csv)
    summary_fieldnames, summary_rows = read_csv(summary_csv)
    worksheet_rows = builder.read_rows(worksheet_csv)
    source_queue_rows = builder.read_rows(source_queue_csv)
    expected_rows = builder.build_packet_rows(worksheet_rows, source_queue_rows)
    expected_summary_rows = builder.build_summary_rows(expected_rows)
    summary = {row["metric"]: row["value"] for row in summary_rows}
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
                summary_csv: summary_text,
                manifest_json: manifest_text,
            }
        )
    )
    failures.extend(validate_rows_csv(rows_fieldnames, rows, expected_rows))
    failures.extend(validate_rows(doc, normalized, rows))
    failures.extend(validate_evidence_artifact_paths(rows_csv, rows))
    failures.extend(
        validate_summary_csv(
            summary_fieldnames,
            summary_rows,
            expected_summary_rows,
        )
    )
    failures.extend(validate_summary(doc, normalized, rows, summary))
    failures.extend(
        validate_manifest(
            manifest_json,
            manifest,
            expected_rows,
            expected_summary_rows,
            worksheet_csv,
            source_queue_csv,
        )
    )
    return failures


def validate_evidence_artifact_paths(
    rows_csv: Path,
    rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    for row in rows:
        decision_id = row.get("decision_id", "")
        for field in ("selected_path", "page_image_path"):
            raw_value = row.get(field, "").strip()
            if not raw_value:
                failures.append(f"{rows_csv} {decision_id} missing {field}")
                continue
            path = Path(raw_value)
            if not path.exists():
                failures.append(f"{rows_csv} {decision_id} {field} not found: {path}")
    return failures


def validate_no_source_text(texts_by_path: dict[Path, str]) -> list[str]:
    failures: list[str] = []
    for path, text in texts_by_path.items():
        if contains_hebrew_or_greek(text):
            failures.append(f"{path} appears to contain source-script body text")
    return failures


def validate_rows_csv(
    fieldnames: list[str],
    rows: list[dict[str, str]],
    expected_rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    if fieldnames != builder.FIELDNAMES:
        failures.append(
            f"rows CSV fieldnames drifted: {fieldnames} expected {builder.FIELDNAMES}"
        )
    if rows != expected_rows:
        failures.append("rows CSV row data drifted from builder output")
    return failures


def validate_rows(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    if len(rows) != 14:
        failures.append(f"rows CSV has {len(rows)} rows, expected 14")
    for index, row in enumerate(rows, start=1):
        expected = f"cities_source_row_lock_{index:03d}"
        if row.get("decision_id") != expected:
            failures.append(
                f"rows CSV rank {index} decision_id={row.get('decision_id')} expected {expected}"
            )
        if row.get("source_row_use") != "no_source_row_use":
            failures.append(f"rows CSV {expected} allows source-row use")
        if row.get("current_decision") != "no_source_row_import":
            failures.append(f"rows CSV {expected} imports source row")
        expected_action = EXPECTED_LOCKED_DECISIONS.get(expected)
        if expected_action:
            if row.get("record_decision_status") != "locked":
                failures.append(f"rows CSV {expected} must be locked")
            if row.get("record_selected_action") != expected_action:
                failures.append(f"rows CSV {expected} action must be {expected_action}")
        else:
            if row.get("record_decision_status") != "unrecorded":
                failures.append(f"rows CSV {expected} unexpectedly has decision record")
        if expected not in normalized_doc:
            failures.append(f"{doc} missing decision id: {expected}")
    return failures


def validate_summary(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
    summary: dict[str, str],
) -> list[str]:
    failures: list[str] = []
    if summary.get("evidence_rows") != str(len(rows)):
        failures.append(
            f"summary CSV evidence_rows={summary.get('evidence_rows')} does not match rows={len(rows)}"
        )
    for label, metric in (
        ("Evidence rows", "evidence_rows"),
        ("Source-row imports", "source_row_imports"),
        ("ELS runs", "els_runs"),
        ("Compactness runs", "compactness_runs"),
    ):
        value = summary.get(metric, "")
        if not value:
            failures.append(f"summary CSV missing metric: {metric}")
            continue
        needle = normalize_space(f"- {label}: {value}.")
        if needle not in normalized_doc:
            failures.append(f"{doc} missing summary value: {label}={value}")
    return failures


def validate_summary_csv(
    fieldnames: list[str],
    rows: list[dict[str, str]],
    expected_rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    if fieldnames != builder.SUMMARY_FIELDNAMES:
        failures.append(
            f"summary CSV fieldnames drifted: {fieldnames} expected {builder.SUMMARY_FIELDNAMES}"
        )
    if rows != expected_rows:
        failures.append("summary CSV summary rows drifted from builder output")
    return failures


def validate_manifest(
    manifest_json: Path,
    manifest: dict[str, Any],
    expected_rows: list[dict[str, str]],
    expected_summary_rows: list[dict[str, str]],
    worksheet_csv: Path,
    source_queue_csv: Path,
) -> list[str]:
    expected = {
        "tool": "build_cities_source_row_lock_evidence_packet.py",
        "inputs": {
            "worksheet": str(worksheet_csv),
            "source_queue": str(source_queue_csv),
        },
        "outputs": {
            "csv": str(DEFAULT_ROWS),
            "summary": str(DEFAULT_SUMMARY),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "rows": len(expected_rows),
        "summary": {
            row["metric"]: row["value"] for row in expected_summary_rows
        },
        "source_row_imports": builder.count_imports(expected_rows),
        "els_runs": 0,
        "compactness_runs": 0,
        "claim_boundary": builder.CLAIM_BOUNDARY,
    }
    failures: list[str] = []
    for key, expected_value in expected.items():
        if manifest.get(key) != expected_value:
            failures.append(
                f"{manifest_json} {key} drifted: {manifest.get(key)!r} expected {expected_value!r}"
            )
    return failures


def contains_hebrew_or_greek(text: str) -> bool:
    for char in text:
        code = ord(char)
        if 0x0590 <= code <= 0x05FF or 0x0370 <= code <= 0x03FF:
            return True
    return False


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return {}
    return payload


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
