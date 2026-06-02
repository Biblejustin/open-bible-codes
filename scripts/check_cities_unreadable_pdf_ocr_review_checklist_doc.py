#!/usr/bin/env python3
"""Validate Cities unreadable-PDF OCR review checklist doc stays no-input."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_unreadable_pdf_ocr_review_checklist as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_ROWS = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST
DEFAULT_PACKET = builder.DEFAULT_PACKET

REQUIRED_PHRASES = (
    "# Cities Unreadable PDF OCR Review Checklist",
    "Status: no-input OCR review checklist.",
    "creates contact sheets",
    "does not track OCR text",
    "repair text",
    "import source rows",
    "normalize city names",
    "ELS searches",
    "compute compactness",
    "verify p-levels",
    "Checklist rows: 11.",
    "PDF rows: 11.",
    "Pages total: 61.",
    "Pages with OCR text: 59.",
    "Pages without OCR text: 2.",
    "Label contact sheets: 11.",
    "Contact sheets are visual review aids only",
    "OCR sidecars remain ignored local files",
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
    failures = validate_cities_unreadable_pdf_ocr_review_checklist_doc(
        args.doc,
        args.rows,
        args.summary,
        args.manifest,
        args.packet,
    )
    if failures:
        for failure in failures:
            print(
                f"Cities unreadable-PDF OCR review checklist doc failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities unreadable-PDF OCR review checklist doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    return parser


def validate_cities_unreadable_pdf_ocr_review_checklist_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    summary_csv: Path = DEFAULT_SUMMARY,
    manifest_json: Path = DEFAULT_MANIFEST,
    packet_csv: Path = DEFAULT_PACKET,
) -> list[str]:
    missing = [
        str(path)
        for path in (doc, rows_csv, summary_csv, manifest_json, packet_csv)
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
    contact_summary = expected_contact_summary(rows)
    expected_summary_rows = builder.build_summary_rows(rows, contact_summary)
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
            contact_summary,
            packet_csv,
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
    expected_ranks = [str(index) for index in range(1, len(rows) + 1)]
    actual_ranks = [row.get("review_rank", "") for row in rows]
    if actual_ranks != expected_ranks:
        failures.append(f"rows CSV review_rank drifted: {actual_ranks}")
    for row in rows:
        label = row.get("label", "")
        if row.get("claim_boundary") != builder.CLAIM_BOUNDARY:
            failures.append(f"rows CSV {label} claim boundary drifted")
        if row.get("review_state") != "awaiting_page_image_vs_ocr_sidecar_review":
            failures.append(f"rows CSV {label} review_state drifted")
        if row.get("contact_sheet_path", "") and not row["contact_sheet_path"].startswith(
            str(builder.DEFAULT_CONTACT_DIR)
        ):
            failures.append(f"rows CSV {label} contact_sheet_path outside contact dir")
        if row.get("all_contact_sheet_path") != str(builder.DEFAULT_CONTACT_SHEET):
            failures.append(f"rows CSV {label} all_contact_sheet_path drifted")
    return failures


def validate_rows(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
) -> list[str]:
    labels = {row.get("label", "") for row in rows}
    priorities = {row.get("review_priority", "") for row in rows}
    failures: list[str] = []
    for label in EXPECTED_LABELS:
        if label not in labels:
            failures.append(f"rows CSV missing label: {label}")
        if label not in normalized_doc:
            failures.append(f"{doc} missing label: {label}")
    if "1_empty_or_low_ocr_pages" not in priorities:
        failures.append("rows CSV missing priority: 1_empty_or_low_ocr_pages")
    if "1_empty_or_low_ocr_pages" not in normalized_doc:
        failures.append(f"{doc} missing priority: 1_empty_or_low_ocr_pages")
    return failures


def validate_summary(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
    summary: dict[str, str],
) -> list[str]:
    expected = {
        "Checklist rows": summary.get("checklist_rows", ""),
        "PDF rows": summary.get("pdf_rows", ""),
        "Pages total": summary.get("pages_total", ""),
        "Pages with OCR text": summary.get("pages_with_ocr_text", ""),
        "Pages without OCR text": summary.get("pages_without_ocr_text", ""),
        "OCR text signal chars": summary.get("ocr_text_signal_chars", ""),
        "OCR words": summary.get("ocr_words", ""),
        "OCR lines": summary.get("ocr_lines", ""),
        "Label contact sheets": summary.get("label_contact_sheets", ""),
    }
    failures: list[str] = []
    if summary.get("checklist_rows") != str(len(rows)):
        failures.append(
            f"summary CSV checklist_rows={summary.get('checklist_rows')} "
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
        failures.append("summary CSV summary rows drifted from checklist row totals")
    return failures


def validate_manifest(
    manifest_json: Path,
    manifest: dict[str, Any] | str,
    rows: list[dict[str, str]],
    expected_summary_rows: list[dict[str, str]],
    contact_summary: dict[str, object],
    packet_csv: Path,
) -> list[str]:
    if isinstance(manifest, str):
        return [manifest]
    expected = {
        "tool": "build_cities_unreadable_pdf_ocr_review_checklist.py",
        "inputs": {"packet": str(packet_csv)},
        "parameters": {
            "contact_sheet_out": str(builder.DEFAULT_CONTACT_SHEET),
            "contact_sheet_dir": str(builder.DEFAULT_CONTACT_DIR),
            "thumb_width": 240,
            "thumb_height": 320,
        },
        "rows": len(rows),
        "summary": {
            row["metric"]: row["value"] for row in expected_summary_rows
        },
        "contact_summary": contact_summary,
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


def expected_contact_summary(rows: list[dict[str, str]]) -> dict[str, object]:
    return {
        "label_contact_sheets": len(rows),
        "all_contact_sheet_path": str(builder.DEFAULT_CONTACT_SHEET),
        "all_contact_sheet_exists": builder.DEFAULT_CONTACT_SHEET.exists(),
    }


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
