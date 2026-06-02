#!/usr/bin/env python3
"""Validate Cities unreadable-PDF OCR review packet doc stays review-only."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_unreadable_pdf_ocr_review_packet as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_ROWS = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_REVIEW = builder.DEFAULT_REVIEW

REQUIRED_PHRASES = (
    "# Cities Unreadable PDF OCR Review Packet",
    "Status: OCR review packet only.",
    "records only paths/counts/status in tracked files",
    "does not track OCR text",
    "repair text",
    "import source rows",
    "normalize city names",
    "ELS searches",
    "compute compactness",
    "verify p-levels",
    "PDF rows: 11.",
    "Page rows: 61.",
    "Pages with OCR text: 59.",
    "Pages without OCR text: 2.",
    "Image sidecars: 61.",
    "OCR text sidecars: 61.",
    "Page OCR text detected rows: 59.",
    "Page OCR empty rows: 2.",
    "OCR text sidecars are ignored local review aids",
    "source-row use",
    "separate citable decision records",
)

EXPECTED_LABELS = (
    "cities_pdf_dp365a_appendix_6",
    "cities_pdf_dp365a_appendix_7",
    "cities_pdf_dp365a_part_2_p105_111",
    "cities_pdf_wrr",
    "cities_pdf_dp364_short",
    "cities_pdf_dp365a_appendix_2",
    "cities_pdf_dp365a_appendix_4",
    "cities_pdf_dp365a_appendix_5",
    "cities_pdf_dp365a_p12_17",
    "cities_pdf_dp365a_p1_4",
    "cities_pdf_dp365a_p5_11",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_unreadable_pdf_ocr_review_packet_doc(
        args.doc,
        args.rows,
        args.summary,
        args.manifest,
        args.review,
    )
    if failures:
        for failure in failures:
            print(
                f"Cities unreadable-PDF OCR review packet doc failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities unreadable-PDF OCR review packet doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    return parser


def validate_cities_unreadable_pdf_ocr_review_packet_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    summary_csv: Path = DEFAULT_SUMMARY,
    manifest_json: Path = DEFAULT_MANIFEST,
    review_csv: Path = DEFAULT_REVIEW,
) -> list[str]:
    missing = [
        str(path)
        for path in (doc, rows_csv, summary_csv, manifest_json, review_csv)
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
    expected_summary_rows = builder.build_summary(rows)
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
    failures.extend(validate_rows_csv(rows_fieldnames, rows))
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
            rows,
            expected_summary_rows,
            review_csv,
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
) -> list[str]:
    failures: list[str] = []
    if fieldnames != builder.FIELDNAMES:
        failures.append(
            f"rows CSV fieldnames drifted: {fieldnames} expected {builder.FIELDNAMES}"
        )
    for row in rows:
        label = row.get("label", "")
        if row.get("claim_boundary") != builder.CLAIM_BOUNDARY:
            failures.append(f"rows CSV {label} claim boundary drifted")
        if row.get("language") != "eng":
            failures.append(f"rows CSV {label} language={row.get('language')} expected eng")
        if row.get("dpi") != "200":
            failures.append(f"rows CSV {label} dpi={row.get('dpi')} expected 200")
        if row.get("psm") != "6":
            failures.append(f"rows CSV {label} psm={row.get('psm')} expected 6")
        if row.get("ocr_status") not in {
            "page_ocr_text_detected",
            "page_ocr_empty",
            "ocr_error",
            "blocked_missing_dependency",
            "source_missing",
        }:
            failures.append(f"rows CSV {label} has unexpected OCR status")
        for key in ("image_path", "ocr_text_path"):
            if row.get(key, "") and not row[key].startswith(str(builder.DEFAULT_BASE_DIR)):
                failures.append(f"rows CSV {label} {key} outside review base dir")
    return failures


def validate_rows(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
) -> list[str]:
    labels = {row.get("label", "") for row in rows}
    statuses = {row.get("ocr_status", "") for row in rows}
    failures: list[str] = []
    for label in EXPECTED_LABELS:
        if label not in labels:
            failures.append(f"rows CSV missing label: {label}")
        if label not in normalized_doc:
            failures.append(f"{doc} missing label: {label}")
    for status in ("page_ocr_text_detected", "page_ocr_empty"):
        if status not in statuses:
            failures.append(f"rows CSV missing status: {status}")
        if status not in normalized_doc:
            failures.append(f"{doc} missing status: {status}")
    return failures


def validate_summary(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
    summary: dict[str, str],
) -> list[str]:
    expected = {
        "PDF rows": summary.get("pdf_rows", ""),
        "Page rows": summary.get("page_rows", ""),
        "Pages with OCR text": summary.get("pages_with_ocr_text", ""),
        "Pages without OCR text": summary.get("pages_without_ocr_text", ""),
        "OCR text signal chars": summary.get("ocr_text_signal_chars", ""),
        "OCR words": summary.get("ocr_words", ""),
        "OCR lines": summary.get("ocr_lines", ""),
        "Image sidecars": summary.get("image_sidecars", ""),
        "OCR text sidecars": summary.get("ocr_text_sidecars", ""),
        "Page OCR text detected rows": summary.get("status_page_ocr_text_detected", "0"),
        "Page OCR empty rows": summary.get("status_page_ocr_empty", "0"),
        "OCR error rows": summary.get("status_ocr_error", "0"),
    }
    failures: list[str] = []
    if summary.get("page_rows") != str(len(rows)):
        failures.append(
            f"summary CSV page_rows={summary.get('page_rows')} "
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
        failures.append("summary CSV summary rows drifted from packet row totals")
    return failures


def validate_manifest(
    manifest_json: Path,
    manifest: dict[str, Any] | str,
    rows: list[dict[str, str]],
    expected_summary_rows: list[dict[str, str]],
    review_csv: Path,
) -> list[str]:
    if isinstance(manifest, str):
        return [manifest]
    expected = {
        "tool": "build_cities_unreadable_pdf_ocr_review_packet.py",
        "inputs": {"review": str(review_csv)},
        "parameters": {
            "base_dir": str(builder.DEFAULT_BASE_DIR),
            "language": "eng",
            "dpi": 200,
            "psm": "6",
            "max_pages": 0,
        },
        "rows": len(rows),
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


def read_json(path: Path) -> dict[str, Any] | str:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        return f"{path} could not be read as JSON: {exc}"
    except json.JSONDecodeError as exc:
        return f"{path} is invalid JSON: {exc}"
    if not isinstance(payload, dict):
        return f"{path} JSON root must be an object"
    return payload


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
