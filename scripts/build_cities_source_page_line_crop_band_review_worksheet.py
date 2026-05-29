#!/usr/bin/env python3
"""Build a Cities line-crop band review worksheet without transcription."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts import build_cities_source_page_line_crop_band_map as band_builder
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell


DEFAULT_BAND_MAP = band_builder.DEFAULT_OUT
DEFAULT_OUT = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_review_worksheet.csv"
)
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_review_worksheet_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_PAGE_LINE_CROP_BAND_REVIEW_WORKSHEET.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_review_worksheet.manifest.json"
)

REVIEW_STATE = "pending_band_visual_review"
CLAIM_BOUNDARY = (
    "band review worksheet only; no OCR body text, no source-script body text, "
    "no verified transcription, no source-row import, no city normalization, "
    "no ELS, no compactness, no p-level"
)

FIELDNAMES = [
    "review_rank",
    "band_review_id",
    "band_rank",
    "band_id",
    "transcription_decision_id",
    "label",
    "page_number",
    "page_class",
    "page_band_rank",
    "gap_threshold_px",
    "gap_before_band_px",
    "first_line_rank",
    "last_line_rank",
    "first_page_line_rank",
    "last_page_line_rank",
    "line_crop_rows",
    "crop_images_available",
    "band_top",
    "band_bottom",
    "band_height",
    "max_internal_gap_px",
    "ocr_word_count",
    "ocr_hebrew_letters",
    "dominant_review_priority",
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


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    band_fieldnames, band_rows = read_csv(args.band_map)
    rows = build_review_rows(band_rows)
    summary_rows = build_summary_rows(band_fieldnames, band_rows, rows)
    write_csv(args.out, FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, rows, summary_rows, args)
    write_manifest(args.manifest_out, args, rows, summary_rows, band_fieldnames, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--band-map", type=Path, default=DEFAULT_BAND_MAP)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_review_rows(band_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [review_row(index, row) for index, row in enumerate(band_rows, start=1)]


def review_row(index: int, row: dict[str, str]) -> dict[str, str]:
    return {
        "review_rank": str(index),
        "band_review_id": f"cities_source_band_review_{index:03d}",
        "band_rank": row.get("band_rank", ""),
        "band_id": row.get("band_id", ""),
        "transcription_decision_id": row.get("transcription_decision_id", ""),
        "label": row.get("label", ""),
        "page_number": row.get("page_number", ""),
        "page_class": row.get("page_class", ""),
        "page_band_rank": row.get("page_band_rank", ""),
        "gap_threshold_px": row.get("gap_threshold_px", ""),
        "gap_before_band_px": row.get("gap_before_band_px", ""),
        "first_line_rank": row.get("first_line_rank", ""),
        "last_line_rank": row.get("last_line_rank", ""),
        "first_page_line_rank": row.get("first_page_line_rank", ""),
        "last_page_line_rank": row.get("last_page_line_rank", ""),
        "line_crop_rows": row.get("line_crop_rows", ""),
        "crop_images_available": row.get("crop_images_available", ""),
        "band_top": row.get("band_top", ""),
        "band_bottom": row.get("band_bottom", ""),
        "band_height": row.get("band_height", ""),
        "max_internal_gap_px": row.get("max_internal_gap_px", ""),
        "ocr_word_count": row.get("ocr_word_count", "0"),
        "ocr_hebrew_letters": row.get("ocr_hebrew_letters", "0"),
        "dominant_review_priority": row.get("dominant_review_priority", ""),
        "review_state": REVIEW_STATE,
        "required_comparison": (
            "compare band against page image, line-crop HTML, and line crops before "
            "any source-row decision"
        ),
        "allowed_without_input": "organize coordinate-band visual review only",
        "next_manual_action": (
            "classify visual band role as table section, header group, data rows, "
            "note or noise, or needs wider context"
        ),
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_summary_rows(
    band_fieldnames: list[str],
    band_rows: list[dict[str, str]],
    review_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    page_counts = Counter(row.get("transcription_decision_id", "") for row in review_rows)
    priority_counts = Counter(row.get("dominant_review_priority", "") for row in review_rows)
    summary: list[tuple[str, str | int]] = [
        ("band_map_fieldnames_match", str(band_fieldnames == band_builder.FIELDNAMES).lower()),
        ("band_review_rows", len(review_rows)),
        ("source_band_rows", len(band_rows)),
        ("source_line_rows", sum_int(review_rows, "line_crop_rows")),
        ("unique_table_pages", len(page_counts)),
        ("crop_images_available", sum_int(review_rows, "crop_images_available")),
        ("ocr_words", sum_int(review_rows, "ocr_word_count")),
        ("ocr_hebrew_letters", sum_int(review_rows, "ocr_hebrew_letters")),
        ("source_row_imports", 0),
        ("city_name_normalization", 0),
        ("els_runs", 0),
        ("compactness_runs", 0),
        ("p_levels", 0),
        ("review_state", REVIEW_STATE),
    ]
    for transcription_id in sorted(page_counts):
        summary.append((f"bands_{transcription_id}", page_counts[transcription_id]))
    for priority in sorted(priority_counts):
        summary.append((f"dominant_{priority}", priority_counts[priority]))
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
        "# Cities Source Page Line Crop Band Review Worksheet",
        "",
        "Status: no-input worksheet for future Cities source-page line-crop band review.",
        "It reduces the 203 line crops into coordinate bands for later human visual review.",
        "No OCR body text or source-script body text appears in this doc, CSV, or manifest.",
        CLAIM_BOUNDARY,
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_page_line_crop_band_review_worksheet "
            f"--band-map {args.band_map} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Band review rows: {summary['band_review_rows']}.",
        f"- Source line rows represented: {summary['source_line_rows']}.",
        f"- Unique table pages: {summary['unique_table_pages']}.",
        f"- Crop images available: {summary['crop_images_available']}.",
        f"- OCR words represented by line boxes: {summary['ocr_words']}.",
        f"- OCR Hebrew letters represented by line boxes: {summary['ocr_hebrew_letters']}.",
        f"- Review state: `{REVIEW_STATE}`.",
        "- Source-row imports: 0.",
        "- City-name normalization: 0.",
        "- ELS runs: 0.",
        "- Compactness runs: 0.",
        "- p-levels: 0.",
        f"- Boundary: {CLAIM_BOUNDARY}",
        "",
        "## Page Bands",
        "",
        "| Transcription id | Review bands |",
        "| --- | ---: |",
    ]
    for row in rows:
        metric = f"bands_{row['transcription_decision_id']}"
        if row["page_band_rank"] == "1":
            lines.append(
                f"| `{markdown_cell(row['transcription_decision_id'])}` | {summary[metric]} |"
            )
    lines.extend(
        [
            "",
            "## Review Rows",
            "",
            "| Review rank | Page | Lines | Crop rows | Dominant priority |",
            "| ---: | --- | --- | ---: | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["review_rank"]),
                    f"`{markdown_cell(row['transcription_decision_id'])}`",
                    f"{markdown_cell(row['first_page_line_rank'])}-{markdown_cell(row['last_page_line_rank'])}",
                    markdown_cell(row["line_crop_rows"]),
                    f"`{markdown_cell(row['dominant_review_priority'])}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This worksheet organizes coordinate-band review only.",
            "- A band review row is not a verified source row, table row, transcription, or city-name record.",
            "- Any future import still needs readable row evidence and an explicit import decision.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    band_fieldnames: list[str],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {"band_map": str(args.band_map)},
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(rows),
        "summary": {row["metric"]: row["value"] for row in summary_rows},
        "band_map_fieldnames_match": band_fieldnames == band_builder.FIELDNAMES,
        "source_row_imports": 0,
        "city_name_normalization": 0,
        "els_runs": 0,
        "compactness_runs": 0,
        "p_levels": 0,
        "review_state": REVIEW_STATE,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_band_boundary": band_builder.CLAIM_BOUNDARY,
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


def sum_int(rows: list[dict[str, str]], key: str) -> int:
    return sum(to_int(row.get(key)) for row in rows)


def to_int(value: str | None) -> int:
    try:
        return int(value or 0)
    except ValueError:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
