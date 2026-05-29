#!/usr/bin/env python3
"""Build a priority-ordered Cities line-crop review worksheet without transcription."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts import build_cities_source_page_line_crop_priority_contact_sheet as contact_builder
from scripts import build_cities_source_page_line_crop_triage as triage_builder
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell


DEFAULT_TRIAGE = triage_builder.DEFAULT_OUT
DEFAULT_PRIORITY_CONTACT = contact_builder.DEFAULT_OUT
DEFAULT_OUT = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_priority_review_worksheet.csv"
)
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_priority_review_worksheet_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_PAGE_LINE_CROP_PRIORITY_REVIEW_WORKSHEET.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_priority_review_worksheet.manifest.json"
)

REVIEW_STATE = "pending_priority_line_crop_review"
CLAIM_BOUNDARY = (
    "priority worksheet only; no OCR body text, no source-script body text, "
    "no verified transcription, no source-row import, no city normalization, "
    "no ELS, no compactness, no p-level"
)

FIELDNAMES = [
    "review_rank",
    "line_review_id",
    "triage_rank",
    "source_order",
    "line_rank",
    "transcription_decision_id",
    "label",
    "page_number",
    "page_class",
    "page_line_rank",
    "review_priority",
    "review_bucket",
    "triage_reason",
    "priority_contact_sheet_path",
    "crop_path",
    "crop_exists",
    "line_width",
    "line_height",
    "crop_height",
    "ocr_word_count",
    "ocr_hebrew_letters",
    "review_state",
    "required_comparison",
    "allowed_without_input",
    "next_manual_action",
    "source_row_import",
    "city_name_normalization",
    "els_runs",
    "compactness_runs",
    "p_levels",
    "claim_boundary",
]

SUMMARY_FIELDNAMES = ["metric", "value"]
PRIORITY_ORDER = contact_builder.PRIORITY_ORDER


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    triage_fieldnames, triage_rows = read_csv(args.triage)
    contact_fieldnames, contact_rows = read_csv(args.priority_contact)
    rows = build_priority_review_rows(triage_rows, contact_rows)
    summary_rows = build_summary_rows(
        triage_fieldnames, contact_fieldnames, rows, contact_rows
    )
    write_csv(args.out, FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, rows, summary_rows, args)
    write_manifest(
        args.manifest_out,
        args,
        rows,
        summary_rows,
        triage_fieldnames,
        contact_fieldnames,
        started,
    )
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--triage", type=Path, default=DEFAULT_TRIAGE)
    parser.add_argument("--priority-contact", type=Path, default=DEFAULT_PRIORITY_CONTACT)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_priority_review_rows(
    triage_rows: list[dict[str, str]],
    contact_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    contact_by_priority = {
        row.get("review_priority", ""): row.get("contact_sheet_path", "")
        for row in contact_rows
    }
    rows: list[dict[str, str]] = []
    for index, row in enumerate(triage_rows, start=1):
        rows.append(priority_review_row(index, row, contact_by_priority))
    return rows


def priority_review_row(
    index: int,
    row: dict[str, str],
    contact_by_priority: dict[str, str],
) -> dict[str, str]:
    review_priority = row.get("review_priority", "")
    line_review_id = f"cities_source_priority_line_crop_{index:03d}"
    return {
        "review_rank": str(index),
        "line_review_id": line_review_id,
        "triage_rank": row.get("triage_rank", ""),
        "source_order": row.get("source_order", ""),
        "line_rank": row.get("line_rank", ""),
        "transcription_decision_id": row.get("transcription_decision_id", ""),
        "label": row.get("label", ""),
        "page_number": row.get("page_number", ""),
        "page_class": row.get("page_class", ""),
        "page_line_rank": row.get("page_line_rank", ""),
        "review_priority": review_priority,
        "review_bucket": row.get("review_bucket", ""),
        "triage_reason": row.get("triage_reason", ""),
        "priority_contact_sheet_path": contact_by_priority.get(review_priority, ""),
        "crop_path": row.get("crop_path", ""),
        "crop_exists": row.get("crop_exists", ""),
        "line_width": row.get("line_width", ""),
        "line_height": row.get("line_height", ""),
        "crop_height": row.get("crop_height", ""),
        "ocr_word_count": row.get("ocr_word_count", "0"),
        "ocr_hebrew_letters": row.get("ocr_hebrew_letters", "0"),
        "review_state": REVIEW_STATE,
        "required_comparison": (
            "compare crop image against priority contact sheet, full page image, "
            "and local HTML before any transcription decision"
        ),
        "allowed_without_input": "organize priority line-crop review only",
        "next_manual_action": (
            "review crop image; classify visual role and decide whether readable "
            "transcription evidence exists before any import"
        ),
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_summary_rows(
    triage_fieldnames: list[str],
    contact_fieldnames: list[str],
    rows: list[dict[str, str]],
    contact_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    priority_counts = Counter(row["review_priority"] for row in rows)
    bucket_counts = Counter(row["review_bucket"] for row in rows)
    page_counts = Counter(row["transcription_decision_id"] for row in rows)
    summary: list[tuple[str, str | int]] = [
        (
            "triage_fieldnames_match",
            str(triage_fieldnames == triage_builder.FIELDNAMES).lower(),
        ),
        (
            "priority_contact_fieldnames_match",
            str(contact_fieldnames == contact_builder.FIELDNAMES).lower(),
        ),
        ("priority_review_rows", len(rows)),
        ("unique_table_pages", len(page_counts)),
        ("priority_contact_sheets", len(contact_rows)),
        (
            "priority_contact_sheets_available",
            count_value(contact_rows, "contact_sheet_exists", "true"),
        ),
        ("crop_images_available", count_value(rows, "crop_exists", "true")),
        ("ocr_words", sum_int(rows, "ocr_word_count")),
        ("ocr_hebrew_letters", sum_int(rows, "ocr_hebrew_letters")),
        ("source_row_imports", 0),
        ("city_name_normalization", 0),
        ("els_runs", 0),
        ("compactness_runs", 0),
        ("p_levels", 0),
        ("review_state", REVIEW_STATE),
    ]
    for priority in PRIORITY_ORDER:
        summary.append((priority, priority_counts.get(priority, 0)))
    for bucket in sorted(bucket_counts):
        summary.append((f"bucket_{bucket}", bucket_counts[bucket]))
    summary.append(("claim_boundary", CLAIM_BOUNDARY))
    return [{"metric": metric, "value": str(value)} for metric, value in summary]


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    summary = {row["metric"]: row["value"] for row in summary_rows}
    lines = [
        "# Cities Source Page Line Crop Priority Review Worksheet",
        "",
        "Status: priority-ordered worksheet for future Cities source-page line-crop review.",
        "It joins triage rank, crop image paths, and priority contact sheet paths without transcribing Hebrew or importing source rows.",
        "No OCR body text or source-script body text appears in this doc, CSV, or manifest.",
        CLAIM_BOUNDARY,
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_page_line_crop_priority_review_worksheet "
            f"--triage {args.triage} "
            f"--priority-contact {args.priority_contact} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Priority review rows: {summary['priority_review_rows']}.",
        f"- Unique table pages: {summary['unique_table_pages']}.",
        f"- Priority contact sheets: {summary['priority_contact_sheets']}.",
        f"- Priority contact sheets available: {summary['priority_contact_sheets_available']}.",
        f"- Crop images available: {summary['crop_images_available']}.",
        f"- OCR words represented by line boxes: {summary['ocr_words']}.",
        f"- OCR Hebrew letters represented by line boxes: {summary['ocr_hebrew_letters']}.",
        f"- Review state: `{REVIEW_STATE}`.",
        f"- Dense-text priority rows: {summary['priority_1_dense_text']}.",
        f"- Medium-text priority rows: {summary['priority_2_medium_text']}.",
        f"- Short-text priority rows: {summary['priority_3_short_text']}.",
        f"- No-text priority rows: {summary['priority_4_no_text']}.",
        "- Source-row imports: 0.",
        "- City-name normalization: 0.",
        "- ELS runs: 0.",
        "- Compactness runs: 0.",
        "- p-levels: 0.",
        f"- Boundary: {CLAIM_BOUNDARY}",
        "",
        "## Priority Counts",
        "",
        "| Priority | Review rows |",
        "| --- | ---: |",
    ]
    for priority in PRIORITY_ORDER:
        lines.append(f"| `{markdown_cell(priority)}` | {summary[priority]} |")
    lines.extend(
        [
            "",
            "## Worksheet Scope",
            "",
            "- This worksheet organizes visual review in triage priority order only.",
            "- Priority order is not transcription and is not source-row verification.",
            "- Every row still needs visual role classification and readable source evidence before import.",
            "- No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    triage_fieldnames: list[str],
    contact_fieldnames: list[str],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "triage": str(args.triage),
            "priority_contact": str(args.priority_contact),
        },
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(rows),
        "summary": {row["metric"]: row["value"] for row in summary_rows},
        "triage_fieldnames_match": triage_fieldnames == triage_builder.FIELDNAMES,
        "priority_contact_fieldnames_match": contact_fieldnames == contact_builder.FIELDNAMES,
        "source_row_imports": 0,
        "city_name_normalization": 0,
        "els_runs": 0,
        "compactness_runs": 0,
        "p_levels": 0,
        "review_state": REVIEW_STATE,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_triage_boundary": triage_builder.CLAIM_BOUNDARY,
        "source_priority_contact_boundary": contact_builder.NO_INPUT_BOUNDARY,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def count_value(rows: list[dict[str, str]], key: str, value: str) -> int:
    return sum(1 for row in rows if row.get(key) == value)


def sum_int(rows: list[dict[str, str]], key: str) -> int:
    return sum(to_int(row.get(key)) for row in rows)


def to_int(value: str | None) -> int:
    try:
        return int(value or 0)
    except ValueError:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
