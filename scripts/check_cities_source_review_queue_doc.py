#!/usr/bin/env python3
"""Validate Cities source-review queue doc stays source-triage only."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_source_review_queue as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_QUEUE = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_RECOVERY = builder.DEFAULT_RECOVERY
DEFAULT_TEXT_AUDIT = builder.DEFAULT_TEXT_AUDIT

REQUIRED_PHRASES = (
    "# Cities Source Review Queue",
    "Status: source-review triage only.",
    "does not run OCR",
    "normalize city names",
    "ELS searches",
    "compute compactness",
    "verify p-levels",
    "Rows queued: 35.",
    "does not decide source admissibility",
    "does not create city-name rows",
    "does not make any result-bearing claim",
    "CITIES_UNREADABLE_PDF_OCR_PAGE_REVIEW.md",
    "records visual page-role decisions for reviewed OCR-packet pages",
    "source-row imports at zero",
    "CITIES_SOURCE_ROW_LOCK_QUEUE.md",
    "14 table/list/exception-note",
    "separate citable source-row locks",
)

EXPECTED_LANES = (
    "review_extractable_text",
    "ocr_image_only_pdf",
    "encoding_or_ocr_candidate",
    "recover_missing_pdf",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_review_queue_doc(
        args.doc,
        args.queue,
        args.summary,
        args.manifest,
        args.recovery,
        args.text_audit,
    )
    if failures:
        for failure in failures:
            print(f"Cities source-review queue doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities source-review queue doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--recovery", type=Path, default=DEFAULT_RECOVERY)
    parser.add_argument("--text-audit", type=Path, default=DEFAULT_TEXT_AUDIT)
    return parser


def validate_cities_source_review_queue_doc(
    doc: Path,
    queue_csv: Path = DEFAULT_QUEUE,
    summary_csv: Path = DEFAULT_SUMMARY,
    manifest_json: Path = DEFAULT_MANIFEST,
    recovery_csv: Path = DEFAULT_RECOVERY,
    text_audit_csv: Path = DEFAULT_TEXT_AUDIT,
) -> list[str]:
    missing = [
        str(path)
        for path in (
            doc,
            queue_csv,
            summary_csv,
            manifest_json,
            recovery_csv,
            text_audit_csv,
        )
        if not path.exists()
    ]
    if missing:
        return ["missing required files: " + ", ".join(missing)]
    text = doc.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    queue_data = read_csv(queue_csv)
    summary_data = read_csv(summary_csv)
    recovery_data = read_csv(recovery_csv)
    text_audit_data = read_csv(text_audit_csv)
    for data in (queue_data, summary_data, recovery_data, text_audit_data):
        if isinstance(data, str):
            return [data]
    _, queue_rows = queue_data
    _, summary_rows = summary_data
    _, recovery_rows = recovery_data
    _, text_audit_rows = text_audit_data
    expected_queue_rows = expected_queue(recovery_rows, text_audit_rows)
    expected_summary_rows = builder.build_summary(expected_queue_rows)
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized
    ]
    failures.extend(validate_queue_csv(queue_csv, queue_data, expected_queue_rows))
    failures.extend(validate_summary_csv(summary_csv, summary_data, expected_summary_rows))
    failures.extend(
        validate_manifest(
            manifest_json,
            recovery_csv,
            text_audit_csv,
            len(recovery_rows),
            len(text_audit_rows),
            expected_queue_rows,
            expected_summary_rows,
        )
    )
    failures.extend(validate_lanes(doc, normalized, queue_rows, summary_rows))
    return failures


def expected_queue(
    recovery_rows: list[dict[str, str]],
    text_audit_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = builder.build_queue(
        recovery_rows,
        {row["label"]: row for row in text_audit_rows},
    )
    return stringify_rows(rows)


def validate_queue_csv(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
    expected_rows: list[dict[str, str]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != builder.QUEUE_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if rows != expected_rows:
        failures.append(f"{path} queue rows drifted")
    return failures


def validate_summary_csv(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
    expected_rows: list[dict[str, str]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != builder.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if rows != expected_rows:
        failures.append(f"{path} summary rows drifted")
    return failures


def validate_manifest(
    path: Path,
    recovery_csv: Path,
    text_audit_csv: Path,
    recovery_rows: int,
    text_audit_rows: int,
    queue_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[str]:
    data = read_json(path)
    if isinstance(data, str):
        return [data]
    checks: dict[str, Any] = {
        "tool": "build_cities_source_review_queue.py",
        "inputs": {
            "recovery": str(recovery_csv),
            "text_audit": str(text_audit_csv),
        },
        "rows": {
            "recovery": recovery_rows,
            "text_audit": text_audit_rows,
            "queue": len(queue_rows),
        },
        "lane_counts": {row["lane"]: row["rows"] for row in summary_rows},
        "outputs": {
            "queue": str(DEFAULT_QUEUE),
            "summary": str(DEFAULT_SUMMARY),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "claim_boundary": builder.CLAIM_BOUNDARY,
    }
    failures: list[str] = []
    for key, expected in checks.items():
        if data.get(key) != expected:
            failures.append(f"{path} {key} drifted")
    return failures


def validate_lanes(
    doc: Path,
    normalized_doc: str,
    queue_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    queue_lanes = {row.get("lane", "") for row in queue_rows}
    summary_by_lane = {row.get("lane", ""): row for row in summary_rows}
    for lane in EXPECTED_LANES:
        if lane not in queue_lanes:
            failures.append(f"queue CSV missing lane: {lane}")
        if lane not in summary_by_lane:
            failures.append(f"summary CSV missing lane: {lane}")
            continue
        expected = normalize_space(f"| `{lane}` | {summary_by_lane[lane]['rows']} |")
        if expected not in normalized_doc:
            failures.append(
                f"{doc} missing lane summary count: {lane}={summary_by_lane[lane]['rows']}"
            )
    queued_phrase = normalize_space(f"- Rows queued: {len(queue_rows)}.")
    if queued_phrase not in normalized_doc:
        failures.append(f"{doc} missing queue total: {len(queue_rows)}")
    return failures


def stringify_rows(rows: list[dict[str, object]]) -> list[dict[str, str]]:
    return [{key: str(value) for key, value in row.items()} for row in rows]


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        return f"{path} could not be read as JSON: {exc}"
    except json.JSONDecodeError as exc:
        return f"{path} is invalid JSON: {exc}"
    if not isinstance(data, dict):
        return f"{path} JSON root must be an object"
    return data


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
