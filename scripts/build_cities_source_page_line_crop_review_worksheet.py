#!/usr/bin/env python3
"""Build Cities source-page line-crop review worksheet without transcription."""

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
    NO_INPUT_BOUNDARY,
)
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell


DEFAULT_OUT = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_review_worksheet.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_PAGE_LINE_CROP_REVIEW_WORKSHEET.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_review_worksheet.manifest.json"
)
DEFAULT_HTML_REVIEW_AID = Path(
    "reports/cities_pdf_recovery_probe/source_page_line_crops/line_crop_review.html"
)

REVIEW_STATE = "pending_line_crop_review"
CLAIM_BOUNDARY = (
    "worksheet only; no OCR body text, no source-script body text, no verified "
    "transcription, no source-row import, no city normalization, no ELS, no "
    "compactness, no p-level"
)

FIELDNAMES = [
    "review_rank",
    "line_review_id",
    "line_rank",
    "transcription_decision_id",
    "label",
    "page_number",
    "page_class",
    "page_line_rank",
    "page_image_path",
    "crop_path",
    "crop_exists",
    "crop_width",
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


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = build_worksheet_rows(read_rows(args.packet))
    write_csv(args.out, FIELDNAMES, rows)
    write_markdown(args.markdown_out, rows, args)
    write_manifest(args.manifest_out, args, rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--html-review-aid", type=Path, default=DEFAULT_HTML_REVIEW_AID)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_worksheet_rows(packet_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(packet_rows, start=1):
        rows.append(worksheet_row(index, row))
    return rows


def worksheet_row(index: int, row: dict[str, str]) -> dict[str, str]:
    line_review_id = f"cities_source_line_crop_{index:03d}"
    return {
        "review_rank": str(index),
        "line_review_id": line_review_id,
        "line_rank": row.get("line_rank", ""),
        "transcription_decision_id": row.get("transcription_decision_id", ""),
        "label": row.get("label", ""),
        "page_number": row.get("page_number", ""),
        "page_class": row.get("page_class", ""),
        "page_line_rank": row.get("page_line_rank", ""),
        "page_image_path": row.get("page_image_path", ""),
        "crop_path": row.get("crop_path", ""),
        "crop_exists": row.get("crop_exists", ""),
        "crop_width": row.get("crop_width", ""),
        "crop_height": row.get("crop_height", ""),
        "ocr_word_count": row.get("ocr_word_count", "0"),
        "ocr_hebrew_letters": row.get("ocr_hebrew_letters", "0"),
        "review_state": REVIEW_STATE,
        "required_comparison": (
            "compare local line crop against full page image and OCR HTML before "
            "any transcription decision"
        ),
        "allowed_without_input": "organize line-crop review only",
        "next_manual_action": (
            "human visual review; mark crop as table row, header, note, noise, "
            "or needs wider context before transcription"
        ),
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    page_counts = Counter(row["transcription_decision_id"] for row in rows)
    class_counts = Counter(row["page_class"] for row in rows)
    lines = [
        "# Cities Source Page Line Crop Review Worksheet",
        "",
        "Status: no-input worksheet for future Cities source-page line-crop review.",
        "It organizes local line-crop images for later human visual review but does not transcribe rows or import source rows.",
        "No OCR body text or source-script body text appears in this doc, CSV, or manifest.",
        CLAIM_BOUNDARY,
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_page_line_crop_review_worksheet "
            f"--packet {args.packet} "
            f"--html-review-aid {args.html_review_aid} "
            f"--out {args.out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Line-crop review rows: {len(rows)}.",
        f"- Unique table pages: {len(page_counts)}.",
        f"- Table-candidate page rows: {class_counts['table_candidate_page']}.",
        f"- Crop images available: {count_value(rows, 'crop_exists', 'true')}.",
        f"- OCR words represented by line boxes: {sum_int(rows, 'ocr_word_count')}.",
        f"- OCR Hebrew letters represented by line boxes: {sum_int(rows, 'ocr_hebrew_letters')}.",
        f"- Review state: `{REVIEW_STATE}`.",
        f"- Local HTML review aid: `{args.html_review_aid}`.",
        "- Source-row imports: 0.",
        "- City-name normalization: 0.",
        "- ELS runs: 0.",
        "- Compactness runs: 0.",
        "- p-levels: 0.",
        f"- Boundary: {CLAIM_BOUNDARY}",
        "",
        "## Page Counts",
        "",
        "| Transcription id | Line-crop review rows |",
        "| --- | ---: |",
    ]
    for transcription_id in sorted(page_counts):
        lines.append(
            f"| `{markdown_cell(transcription_id)}` | {page_counts[transcription_id]} |"
        )
    lines.extend(
        [
            "",
            "## Worksheet Scope",
            "",
            "- This worksheet organizes visual review only.",
            "- Line crops are not verified source rows.",
            "- Human review must decide whether each crop is table row, header, note, noise, or needs wider context.",
            "- Readable transcription, row/column alignment evidence, and an explicit import decision are still required before any source row can be imported.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "packet": str(args.packet),
            "html_review_aid": str(args.html_review_aid),
        },
        "outputs": {
            "csv": str(args.out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(rows),
        "unique_table_pages": len({row["transcription_decision_id"] for row in rows}),
        "crop_images_available": count_value(rows, "crop_exists", "true"),
        "ocr_words": sum_int(rows, "ocr_word_count"),
        "ocr_hebrew_letters": sum_int(rows, "ocr_hebrew_letters"),
        "source_row_imports": 0,
        "city_name_normalization": 0,
        "els_runs": 0,
        "compactness_runs": 0,
        "p_levels": 0,
        "review_state": REVIEW_STATE,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_packet_boundary": NO_INPUT_BOUNDARY,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def count_value(rows: list[dict[str, str]], key: str, value: str) -> int:
    return sum(1 for row in rows if row.get(key) == value)


def sum_int(rows: list[dict[str, str]], key: str) -> int:
    total = 0
    for row in rows:
        try:
            total += int(row.get(key, "0"))
        except ValueError:
            continue
    return total


if __name__ == "__main__":
    raise SystemExit(main())
