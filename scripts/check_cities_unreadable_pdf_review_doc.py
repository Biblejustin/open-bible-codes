#!/usr/bin/env python3
"""Validate Cities unreadable-PDF review doc stays OCR-planning only."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_unreadable_pdf_review as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_ROWS = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_QUEUE = builder.DEFAULT_QUEUE

REQUIRED_PHRASES = (
    "# Cities Unreadable PDF Review",
    "Status: OCR/encoding planning only.",
    "does not run OCR",
    "repair text",
    "import source rows",
    "normalize city names",
    "ELS searches",
    "compute compactness",
    "verify p-levels",
    "Unreadable rows reviewed: 12.",
    "OCR/image-only rows: 9.",
    "Encoding-or-OCR candidate rows: 3.",
    "Aumann committee rows: 11.",
    "Other-family rows: 1.",
    "Pages needing review: 61.",
    "Garbled text chars: 5364.",
    "does not repair the PDFs",
    "does not repair the PDFs, create OCR text, decide source admissibility",
    "make a result-bearing claim",
)

EXPECTED_LABELS = (
    "cities_pdf_dp365a_appendix_6",
    "cities_pdf_dp365a_appendix_7",
    "cities_pdf_dp365a_part_2_p105_111",
    "cities_pdf_wrr",
    "cities_pdf_dp364_short",
    "cities_pdf_dp365a_appendix_2",
    "cities_pdf_dp365a_appendix_3",
    "cities_pdf_dp365a_appendix_4",
    "cities_pdf_dp365a_appendix_5",
    "cities_pdf_dp365a_p12_17",
    "cities_pdf_dp365a_p1_4",
    "cities_pdf_dp365a_p5_11",
)

EXPECTED_LANES = (
    "ocr_image_only_pdf",
    "encoding_or_ocr_candidate",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_unreadable_pdf_review_doc(
        args.doc,
        args.rows,
        args.summary,
        args.manifest,
        args.queue,
    )
    if failures:
        for failure in failures:
            print(f"Cities unreadable-PDF review doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities unreadable-PDF review doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    return parser


def validate_cities_unreadable_pdf_review_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    summary_csv: Path = DEFAULT_SUMMARY,
    manifest_json: Path = DEFAULT_MANIFEST,
    queue_csv: Path = DEFAULT_QUEUE,
) -> list[str]:
    missing = [
        str(path)
        for path in (doc, rows_csv, summary_csv, manifest_json, queue_csv)
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
    queue_rows = builder.read_csv(queue_csv)
    expected_rows = builder.build_review_rows(queue_rows)
    expected_summary_rows = builder.build_summary(expected_rows)
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
            queue_csv,
        )
    )
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
    labels = {row.get("label", "") for row in rows}
    lanes = {row.get("lane", "") for row in rows}
    failures: list[str] = []
    for label in EXPECTED_LABELS:
        if label not in labels:
            failures.append(f"rows CSV missing label: {label}")
        if label not in normalized_doc:
            failures.append(f"{doc} missing label: {label}")
    for lane in EXPECTED_LANES:
        if lane not in lanes:
            failures.append(f"rows CSV missing lane: {lane}")
        if lane not in normalized_doc:
            failures.append(f"{doc} missing lane: {lane}")
    return failures


def validate_summary(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
    summary: dict[str, str],
) -> list[str]:
    expected = {
        "Unreadable rows reviewed": summary.get("unreadable_rows_reviewed", ""),
        "OCR/image-only rows": summary.get("ocr_image_only_rows", ""),
        "Encoding-or-OCR candidate rows": summary.get("encoding_or_ocr_candidate_rows", ""),
        "Aumann committee rows": summary.get("aumann_committee_rows", ""),
        "Other-family rows": summary.get("other_family_rows", ""),
        "Pages needing review": summary.get("total_pages_needing_review", ""),
        "Garbled text chars": summary.get("garbled_text_chars", ""),
    }
    failures: list[str] = []
    if summary.get("unreadable_rows_reviewed") != str(len(rows)):
        failures.append(
            f"summary CSV unreadable_rows_reviewed={summary.get('unreadable_rows_reviewed')} "
            f"does not match rows={len(rows)}"
        )
    for label, value in expected.items():
        if not value:
            failures.append(f"summary CSV missing metric for {label}")
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
    queue_csv: Path,
) -> list[str]:
    expected = {
        "tool": "build_cities_unreadable_pdf_review.py",
        "inputs": {"queue": str(queue_csv)},
        "rows": len(expected_rows),
        "summary": {
            row["metric"]: row["value"] for row in expected_summary_rows
        },
        "outputs": {
            "csv": str(DEFAULT_ROWS),
            "summary": str(DEFAULT_SUMMARY),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
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
