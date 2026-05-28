#!/usr/bin/env python3
"""Rank Cities source-page line crops by review priority without transcription."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.build_cities_source_page_line_crop_packet import (
    DEFAULT_OUT as DEFAULT_PACKET,
    FIELDNAMES as PACKET_FIELDNAMES,
    NO_INPUT_BOUNDARY,
)
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell


DEFAULT_OUT = Path("reports/cities_pdf_recovery_probe/cities_source_page_line_crop_triage.csv")
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_triage_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_PAGE_LINE_CROP_TRIAGE.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_triage.manifest.json"
)

CLAIM_BOUNDARY = (
    "triage only; no OCR body text, no source-script body text, no verified "
    "transcription, no source-row import, no city normalization, no ELS, no "
    "compactness, no p-level"
)

FIELDNAMES = [
    "triage_rank",
    "source_order",
    "line_rank",
    "transcription_decision_id",
    "label",
    "page_number",
    "page_class",
    "page_line_rank",
    "crop_path",
    "crop_exists",
    "line_width",
    "line_height",
    "crop_height",
    "ocr_word_count",
    "ocr_hebrew_letters",
    "review_priority",
    "review_bucket",
    "triage_reason",
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


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    packet_fieldnames, packet_rows = read_packet(args.packet)
    rows = build_triage_rows(packet_rows)
    summary_rows = build_summary_rows(rows, packet_fieldnames)
    write_csv(args.out, FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, rows, summary_rows, args)
    write_manifest(args.manifest_out, args, rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_triage_rows(packet_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = [triage_row(index, row) for index, row in enumerate(packet_rows, start=1)]
    rows.sort(key=triage_sort_key)
    for rank, row in enumerate(rows, start=1):
        row["triage_rank"] = str(rank)
    return rows


def triage_row(source_order: int, row: dict[str, str]) -> dict[str, str]:
    word_count = to_int(row.get("ocr_word_count"))
    hebrew_letters = to_int(row.get("ocr_hebrew_letters"))
    line_width = to_int(row.get("line_width"))
    line_height = to_int(row.get("line_height"))
    crop_height = to_int(row.get("crop_height"))
    priority, bucket, reason = classify_line_crop(
        word_count=word_count,
        hebrew_letters=hebrew_letters,
        line_width=line_width,
        line_height=line_height,
        crop_height=crop_height,
    )
    return {
        "triage_rank": "",
        "source_order": str(source_order),
        "line_rank": row.get("line_rank", ""),
        "transcription_decision_id": row.get("transcription_decision_id", ""),
        "label": row.get("label", ""),
        "page_number": row.get("page_number", ""),
        "page_class": row.get("page_class", ""),
        "page_line_rank": row.get("page_line_rank", ""),
        "crop_path": row.get("crop_path", ""),
        "crop_exists": row.get("crop_exists", ""),
        "line_width": str(line_width),
        "line_height": str(line_height),
        "crop_height": str(crop_height),
        "ocr_word_count": str(word_count),
        "ocr_hebrew_letters": str(hebrew_letters),
        "review_priority": priority,
        "review_bucket": bucket,
        "triage_reason": reason,
        "allowed_without_input": "rank line-crop visual review only",
        "next_manual_action": (
            "review crop image against page image/contact sheet; classify visual role "
            "before any transcription"
        ),
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def classify_line_crop(
    *,
    word_count: int,
    hebrew_letters: int,
    line_width: int,
    line_height: int,
    crop_height: int,
) -> tuple[str, str, str]:
    if word_count <= 0 or hebrew_letters <= 0:
        return "priority_4_no_text", "noise_or_blank", "no OCR text signal in line box"
    if word_count >= 6 and hebrew_letters >= 20:
        return "priority_1_dense_text", "likely_row_or_header", "dense OCR signal"
    if word_count >= 3 and hebrew_letters >= 10:
        return "priority_2_medium_text", "likely_row_or_header", "medium OCR signal"
    if line_width <= 120 or word_count <= 2:
        return "priority_3_short_text", "short_label_or_marker", "short OCR signal"
    if line_height >= 60 or crop_height >= 80:
        return "priority_2_medium_text", "wide_context_candidate", "tall crop needs context"
    return "priority_3_short_text", "short_label_or_marker", "text signal below row threshold"


def triage_sort_key(row: dict[str, str]) -> tuple[int, int, int]:
    priority_order = {
        "priority_1_dense_text": 1,
        "priority_2_medium_text": 2,
        "priority_3_short_text": 3,
        "priority_4_no_text": 4,
    }
    return (
        priority_order.get(row["review_priority"], 99),
        to_int(row["source_order"]),
        to_int(row["page_line_rank"]),
    )


def build_summary_rows(
    rows: list[dict[str, str]],
    packet_fieldnames: list[str],
) -> list[dict[str, str]]:
    priority_counts = Counter(row["review_priority"] for row in rows)
    bucket_counts = Counter(row["review_bucket"] for row in rows)
    page_counts = Counter(row["transcription_decision_id"] for row in rows)
    summary: list[tuple[str, str | int]] = [
        ("packet_fieldnames_match", str(packet_fieldnames == PACKET_FIELDNAMES).lower()),
        ("triage_rows", len(rows)),
        ("unique_table_pages", len(page_counts)),
        ("crop_images_available", count_value(rows, "crop_exists", "true")),
        ("ocr_words", sum_int(rows, "ocr_word_count")),
        ("ocr_hebrew_letters", sum_int(rows, "ocr_hebrew_letters")),
        ("source_row_imports", 0),
        ("city_name_normalization", 0),
        ("els_runs", 0),
        ("compactness_runs", 0),
        ("p_levels", 0),
    ]
    for priority in (
        "priority_1_dense_text",
        "priority_2_medium_text",
        "priority_3_short_text",
        "priority_4_no_text",
    ):
        summary.append((priority, priority_counts.get(priority, 0)))
    for bucket in sorted(bucket_counts):
        summary.append((f"bucket_{bucket}", bucket_counts[bucket]))
    return [{"metric": metric, "value": str(value)} for metric, value in summary]


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    summary = {row["metric"]: row["value"] for row in summary_rows}
    page_counts = Counter(row["transcription_decision_id"] for row in rows)
    lines = [
        "# Cities Source Page Line Crop Triage",
        "",
        "Status: no-input visual triage for Cities source-page line crops.",
        "It ranks crop images by layout and OCR-count signal only; it does not read Hebrew, transcribe rows, or import source rows.",
        "Tracked files contain no OCR body text or source-script body text.",
        CLAIM_BOUNDARY,
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_page_line_crop_triage "
            f"--packet {args.packet} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Line-crop triage rows: {summary['triage_rows']}.",
        f"- Unique table pages: {summary['unique_table_pages']}.",
        f"- Crop images available: {summary['crop_images_available']}.",
        f"- OCR words represented by line boxes: {summary['ocr_words']}.",
        f"- OCR Hebrew letters represented by line boxes: {summary['ocr_hebrew_letters']}.",
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
        "## Page Counts",
        "",
        "| Transcription id | Triage rows |",
        "| --- | ---: |",
    ]
    for transcription_id in sorted(page_counts):
        lines.append(f"| `{markdown_cell(transcription_id)}` | {page_counts[transcription_id]} |")
    lines.extend(
        [
            "",
            "## Priority Buckets",
            "",
            "| Priority | Rows | Meaning |",
            "| --- | ---: | --- |",
            f"| `priority_1_dense_text` | {summary['priority_1_dense_text']} | strongest visual review candidates by count signal |",
            f"| `priority_2_medium_text` | {summary['priority_2_medium_text']} | likely text rows needing page context |",
            f"| `priority_3_short_text` | {summary['priority_3_short_text']} | short labels, markers, or weak line boxes |",
            f"| `priority_4_no_text` | {summary['priority_4_no_text']} | no OCR-count signal in the line box |",
            "",
            "## Review Rule",
            "",
            "- This triage is a queue order, not transcription.",
            "- A dense crop can still be a header, note, or noise.",
            "- A short crop can still matter if page context says it does.",
            "- Any future import still needs readable row/column evidence and an explicit source-row import decision.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    started: float,
) -> None:
    summary = {row["metric"]: row["value"] for row in summary_rows}
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {"packet": str(args.packet)},
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(rows),
        "summary": summary,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_packet_boundary": NO_INPUT_BOUNDARY,
        "source_row_imports": 0,
        "city_name_normalization": 0,
        "els_runs": 0,
        "compactness_runs": 0,
        "p_levels": 0,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_packet(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def to_int(value: str | None) -> int:
    try:
        return int(value or 0)
    except ValueError:
        return 0


def count_value(rows: list[dict[str, str]], key: str, value: str) -> int:
    return sum(1 for row in rows if row.get(key) == value)


def sum_int(rows: list[dict[str, str]], key: str) -> int:
    return sum(to_int(row.get(key)) for row in rows)


if __name__ == "__main__":
    raise SystemExit(main())
