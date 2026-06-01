#!/usr/bin/env python3
"""Validate the consolidated Cities no-input handoff status document."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/CITIES_NO_INPUT_HANDOFF_STATUS.md")
DEFAULT_STATUS = Path("reports/cities_no_input_handoff_status/status.csv")
DEFAULT_SUMMARY = Path("reports/cities_no_input_handoff_status/summary.csv")
DEFAULT_MANIFEST = Path("reports/cities_no_input_handoff_status/manifest.json")

REQUIRED_STATUS_IDS = {
    "source_row_lock_queue",
    "source_row_lock_decisions",
    "transcription_review",
    "page_review_bundle",
    "local_ocr_review_aids",
    "line_crop_review_aids",
    "priority_review_queue",
    "result_boundary",
}
REQUIRED_DOC_PHRASES = (
    "Status: consolidated Cities no-input handoff.",
    "not a source-row import",
    "not city-name normalization",
    "not an ELS run",
    "not a compactness run",
    "not a p-level",
    "Status rows: 8.",
    "Manual-input-needed rows: 6.",
    "Queue rows: 14.",
    "Evidence rows: 14.",
    "Source-row lock decision rows: 14.",
    "Locked source-row lock decisions: 14.",
    "Transcription review rows: 14.",
    "Pending transcription rows: 14.",
    "Transcription decision rows: 0.",
    "OCR review rows: 14.",
    "OCR text sidecars: 14.",
    "Line crop rows: 203.",
    "Priority review rows: 203.",
    "Source-row imports: 0.",
    "City-name normalization: 0.",
    "ELS runs: 0.",
    "Compactness runs: 0.",
    "P-levels: 0.",
    "Result allowed: 0.",
    "`cities_no_input_handoff_blocks_source_import_and_results`",
)
FORBIDDEN_DOC_PHRASES = (
    "Cities source-row import ready",
    "Cities ELS run ready",
    "Result allowed: 1.",
    "Source-row imports: 1.",
    "ELS runs: 1.",
    "Compactness runs: 1.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_no_input_handoff_doc(
        args.doc,
        status_path=args.status,
        summary_path=args.summary,
        manifest_path=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"Cities no-input handoff doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities no-input handoff doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--status", type=Path, default=DEFAULT_STATUS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_cities_no_input_handoff_doc(
    path: Path = DEFAULT_DOC,
    *,
    status_path: Path = DEFAULT_STATUS,
    summary_path: Path = DEFAULT_SUMMARY,
    manifest_path: Path = DEFAULT_MANIFEST,
) -> list[str]:
    failures: list[str] = []
    for required_path in (path, status_path, summary_path, manifest_path):
        if not required_path.exists():
            failures.append(f"{required_path} is missing")
    if failures:
        return failures

    text = normalize_space(path.read_text(encoding="utf-8"))
    for phrase in REQUIRED_DOC_PHRASES:
        if normalize_space(phrase) not in text:
            failures.append(f"{path} missing phrase: {phrase}")
    for phrase in FORBIDDEN_DOC_PHRASES:
        if normalize_space(phrase) in text:
            failures.append(f"{path} contains stale phrase: {phrase}")

    status_rows = read_rows(status_path)
    summary = first_row(read_rows(summary_path))
    status_ids = {row.get("status_id", "") for row in status_rows}
    missing_ids = sorted(REQUIRED_STATUS_IDS - status_ids)
    if missing_ids:
        failures.append(f"{status_path} missing status ids: {', '.join(missing_ids)}")
    if len(status_rows) != int_or_zero(summary.get("status_rows")):
        failures.append(
            f"{status_path} row count {len(status_rows)} != summary status_rows {summary.get('status_rows')}"
        )
    expected_summary = {
        "status_rows": "8",
        "handoff_ready_rows": "8",
        "manual_input_needed_rows": "6",
        "queue_rows": "14",
        "evidence_rows": "14",
        "source_row_lock_decision_rows": "14",
        "locked_source_row_lock_decisions": "14",
        "transcription_review_rows": "14",
        "transcription_decision_rows": "0",
        "pending_transcription_rows": "14",
        "ocr_review_rows": "14",
        "ocr_text_sidecars": "14",
        "line_crop_rows": "203",
        "priority_review_rows": "203",
        "source_row_imports": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "result_allowed": "False",
        "claim_status": "cities_no_input_handoff_blocks_source_import_and_results",
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            failures.append(
                f"{summary_path} {key} drifted: expected {expected!r}, got {summary.get(key)!r}"
            )
    manual_input_rows = [
        row for row in status_rows if row.get("manual_input_needed") == "yes"
    ]
    if len(manual_input_rows) != int_or_zero(summary.get("manual_input_needed_rows")):
        failures.append(
            f"{status_path} manual rows drifted: expected {summary.get('manual_input_needed_rows')}, got {len(manual_input_rows)}"
        )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("tool") != "scripts.build_cities_no_input_handoff_status":
        failures.append(f"{manifest_path} tool drifted")
    if manifest.get("summary", {}).get("claim_status") != expected_summary["claim_status"]:
        failures.append(f"{manifest_path} claim status drifted")
    if "no source import or result" not in manifest.get("claim_boundary", ""):
        failures.append(f"{manifest_path} missing no-result claim boundary")
    return failures


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def first_row(rows: list[dict[str, str]]) -> dict[str, str]:
    return rows[0] if rows else {}


def int_or_zero(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
