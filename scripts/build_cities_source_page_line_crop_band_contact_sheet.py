#!/usr/bin/env python3
"""Build local contact sheets for Cities line-crop coordinate bands."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts import build_cities_source_page_line_crop_band_review_worksheet as band_review
from scripts.build_cities_source_page_line_crop_contact_sheet import png_dimensions
from scripts.build_cities_source_page_line_crop_packet import (
    DEFAULT_OUT as DEFAULT_PACKET,
    FIELDNAMES as PACKET_FIELDNAMES,
)
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell


DEFAULT_BAND_REVIEW = band_review.DEFAULT_OUT
DEFAULT_BASE_DIR = Path(
    "reports/cities_pdf_recovery_probe/source_page_line_crops/band_contact_sheets"
)
DEFAULT_OUT = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_contact_sheet.csv"
)
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_contact_sheet_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_PAGE_LINE_CROP_BAND_CONTACT_SHEET.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_contact_sheet.manifest.json"
)

NO_INPUT_BOUNDARY = (
    "band contact sheets only; local line-crop images are visual review aids, "
    "no OCR body text or source-script body text in tracked files, no verified "
    "transcription, no source-row import, no city normalization, no ELS, no "
    "compactness, no p-level"
)

FIELDNAMES = [
    "sheet_rank",
    "band_review_id",
    "band_rank",
    "band_id",
    "transcription_decision_id",
    "page_number",
    "page_class",
    "page_band_rank",
    "first_page_line_rank",
    "last_page_line_rank",
    "line_crop_rows",
    "line_crop_images_found",
    "ocr_word_count",
    "ocr_hebrew_letters",
    "contact_sheet_path",
    "contact_sheet_exists",
    "contact_sheet_width",
    "contact_sheet_height",
    "source_row_import",
    "city_name_normalization",
    "els_runs",
    "compactness_runs",
    "p_levels",
    "no_input_boundary",
]
SUMMARY_FIELDNAMES = ["metric", "value"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    packet_fieldnames, packet_rows = read_csv(args.packet)
    band_fieldnames, band_rows = read_csv(args.band_review)
    sheet_rows = build_band_sheet_rows(packet_rows, band_rows, args)
    write_csv(args.out, FIELDNAMES, sheet_rows)
    summary_rows = build_summary_rows(
        packet_fieldnames,
        packet_rows,
        band_fieldnames,
        band_rows,
        sheet_rows,
    )
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, sheet_rows, summary_rows, args)
    write_manifest(
        args.manifest_out,
        args,
        packet_rows,
        band_rows,
        sheet_rows,
        summary_rows,
        started,
    )
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--band-review", type=Path, default=DEFAULT_BAND_REVIEW)
    parser.add_argument("--base-dir", type=Path, default=DEFAULT_BASE_DIR)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--thumb-width", type=int, default=980)
    parser.add_argument("--thumb-height", type=int, default=72)
    parser.add_argument("--columns", type=int, default=1)
    return parser


def build_band_sheet_rows(
    packet_rows: list[dict[str, str]],
    band_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> list[dict[str, str]]:
    packet_by_page: dict[str, list[dict[str, str]]] = {}
    for row in packet_rows:
        packet_by_page.setdefault(row.get("transcription_decision_id", ""), []).append(row)
    sheet_rows: list[dict[str, str]] = []
    for sheet_rank, band_row in enumerate(band_rows, start=1):
        transcription_id = band_row.get("transcription_decision_id", "")
        page_rows = sorted(packet_by_page.get(transcription_id, []), key=page_line_key)
        first_line = to_int(band_row.get("first_page_line_rank"))
        last_line = to_int(band_row.get("last_page_line_rank"))
        rows_for_band = [
            row
            for row in page_rows
            if first_line <= to_int(row.get("page_line_rank")) <= last_line
        ]
        contact_path = args.base_dir / f"{band_row.get('band_review_id', '')}_line_crops.png"
        summary = write_contact_sheet(contact_path, band_row, rows_for_band, args)
        sheet_rows.append(
            {
                "sheet_rank": str(sheet_rank),
                "band_review_id": band_row.get("band_review_id", ""),
                "band_rank": band_row.get("band_rank", ""),
                "band_id": band_row.get("band_id", ""),
                "transcription_decision_id": transcription_id,
                "page_number": band_row.get("page_number", ""),
                "page_class": band_row.get("page_class", ""),
                "page_band_rank": band_row.get("page_band_rank", ""),
                "first_page_line_rank": band_row.get("first_page_line_rank", ""),
                "last_page_line_rank": band_row.get("last_page_line_rank", ""),
                "line_crop_rows": str(len(rows_for_band)),
                "line_crop_images_found": str(count_value(rows_for_band, "crop_exists", "true")),
                "ocr_word_count": str(sum_int(rows_for_band, "ocr_word_count")),
                "ocr_hebrew_letters": str(sum_int(rows_for_band, "ocr_hebrew_letters")),
                "contact_sheet_path": str(contact_path),
                "contact_sheet_exists": str(contact_path.exists()).lower(),
                "contact_sheet_width": str(summary["contact_sheet_width"]),
                "contact_sheet_height": str(summary["contact_sheet_height"]),
                "source_row_import": "0",
                "city_name_normalization": "0",
                "els_runs": "0",
                "compactness_runs": "0",
                "p_levels": "0",
                "no_input_boundary": NO_INPUT_BOUNDARY,
            }
        )
    return sheet_rows


def write_contact_sheet(
    path: Path,
    band_row: dict[str, str],
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> dict[str, int]:
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageOps
    except ImportError as exc:  # pragma: no cover - local dependency guard
        raise RuntimeError("Pillow is required to write contact sheets") from exc

    columns = max(1, args.columns)
    row_count = max(1, (len(rows) + columns - 1) // columns)
    padding = 14
    gap = 10
    label_height = 46
    cell_width = args.thumb_width + padding * 2
    cell_height = args.thumb_height + label_height + padding * 2
    width = columns * cell_width + gap * (columns - 1)
    height = row_count * cell_height + gap * (row_count - 1)
    sheet = Image.new("RGB", (max(width, 1), max(height, 1)), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for index, row in enumerate(rows):
        column = index % columns
        row_index = index // columns
        x = column * (cell_width + gap)
        y = row_index * (cell_height + gap)
        crop_path = Path(row.get("crop_path", ""))
        if crop_path.exists():
            image = Image.open(crop_path).convert("RGB")
            thumb = ImageOps.contain(image, (args.thumb_width, args.thumb_height))
        else:
            thumb = Image.new("RGB", (args.thumb_width, args.thumb_height), "white")
        label = (
            f"band {band_row.get('sheet_rank', band_row.get('band_rank', ''))} | "
            f"global {row.get('line_rank', '')} | page line {row.get('page_line_rank', '')} | "
            f"words {row.get('ocr_word_count', '')} | letters {row.get('ocr_hebrew_letters', '')}"
        )
        draw.text((x + padding, y + padding), label, fill="black", font=font)
        image_x = x + padding
        image_y = y + padding + label_height
        sheet.paste(thumb, (image_x, image_y))
        draw.rectangle(
            (
                image_x,
                image_y,
                image_x + args.thumb_width,
                image_y + args.thumb_height,
            ),
            outline="black",
            width=1,
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path)
    width, height = png_dimensions(path)
    return {"contact_sheet_width": width, "contact_sheet_height": height}


def build_summary_rows(
    packet_fieldnames: list[str],
    packet_rows: list[dict[str, str]],
    band_fieldnames: list[str],
    band_rows: list[dict[str, str]],
    sheet_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    page_counts = Counter(row.get("transcription_decision_id", "") for row in sheet_rows)
    summary: list[tuple[str, str | int]] = [
        ("packet_fieldnames_match", str(packet_fieldnames == PACKET_FIELDNAMES).lower()),
        ("band_review_fieldnames_match", str(band_fieldnames == band_review.FIELDNAMES).lower()),
        ("band_contact_sheets", len(sheet_rows)),
        ("band_contact_sheets_available", count_value(sheet_rows, "contact_sheet_exists", "true")),
        ("band_review_rows", len(band_rows)),
        ("packet_rows", len(packet_rows)),
        ("line_crop_rows", sum_int(sheet_rows, "line_crop_rows")),
        ("line_crop_images_found", sum_int(sheet_rows, "line_crop_images_found")),
        ("unique_table_pages", len(page_counts)),
        ("ocr_words", sum_int(sheet_rows, "ocr_word_count")),
        ("ocr_hebrew_letters", sum_int(sheet_rows, "ocr_hebrew_letters")),
        ("source_row_imports", 0),
        ("city_name_normalization", 0),
        ("els_runs", 0),
        ("compactness_runs", 0),
        ("p_levels", 0),
    ]
    for transcription_id in sorted(page_counts):
        summary.append((f"bands_{transcription_id}", page_counts[transcription_id]))
    summary.append(("no_input_boundary", NO_INPUT_BOUNDARY))
    return [{"metric": metric, "value": str(value)} for metric, value in summary]


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    summary = {row["metric"]: row["value"] for row in summary_rows}
    lines = [
        "# Cities Source Page Line Crop Band Contact Sheet",
        "",
        "Status: local visual contact sheets for Cities source-page line-crop coordinate bands.",
        "These contact sheets group crop images by coordinate band without transcribing Hebrew or importing source rows.",
        "Tracked files contain no OCR body text or source-script body text.",
        band_review.CLAIM_BOUNDARY,
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_page_line_crop_band_contact_sheet "
            f"--packet {args.packet} "
            f"--band-review {args.band_review} "
            f"--base-dir {args.base_dir} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Band contact sheets: {summary['band_contact_sheets']}.",
        f"- Band contact sheets available: {summary['band_contact_sheets_available']}.",
        f"- Band review rows: {summary['band_review_rows']}.",
        f"- Line crop rows: {summary['line_crop_rows']}.",
        f"- Line crop images found: {summary['line_crop_images_found']}.",
        f"- Unique table pages: {summary['unique_table_pages']}.",
        f"- OCR words represented by line boxes: {summary['ocr_words']}.",
        f"- OCR Hebrew letters represented by line boxes: {summary['ocr_hebrew_letters']}.",
        "- Source-row imports: 0.",
        "- City-name normalization: 0.",
        "- ELS runs: 0.",
        "- Compactness runs: 0.",
        "- p-levels: 0.",
        f"- Boundary: {NO_INPUT_BOUNDARY}",
        "",
        "## Contact Sheets",
        "",
        "| Rank | Band | Page | Lines | Line crops | Image rows | Sheet | Dimensions |",
        "| ---: | --- | --- | --- | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["sheet_rank"]),
                    f"`{markdown_cell(row['band_review_id'])}`",
                    f"`{markdown_cell(row['transcription_decision_id'])}`",
                    f"{markdown_cell(row['first_page_line_rank'])}-{markdown_cell(row['last_page_line_rank'])}",
                    markdown_cell(row["line_crop_rows"]),
                    markdown_cell(row["line_crop_images_found"]),
                    f"`{markdown_cell(row['contact_sheet_path'])}`",
                    f"{markdown_cell(row['contact_sheet_width'])} x {markdown_cell(row['contact_sheet_height'])}",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Band contact sheets are not transcription verification.",
            "- Image review can speed visual sorting, but it does not read or import Hebrew source rows.",
            "- Any future import still needs explicit source-row evidence and an import decision.",
            "- No row here creates a result-bearing corpus, term list, ELS run, compactness run, or p-level.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    packet_rows: list[dict[str, str]],
    band_rows: list[dict[str, str]],
    sheet_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "packet": str(args.packet),
            "band_review": str(args.band_review),
        },
        "outputs": {
            "base_dir": str(args.base_dir),
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(sheet_rows),
        "line_crop_rows": sum_int(sheet_rows, "line_crop_rows"),
        "packet_rows": len(packet_rows),
        "band_review_rows": len(band_rows),
        "summary": {row["metric"]: row["value"] for row in summary_rows},
        "no_input_boundary": NO_INPUT_BOUNDARY,
        "claim_boundary": band_review.CLAIM_BOUNDARY,
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


def page_line_key(row: dict[str, str]) -> tuple[int, int]:
    return (to_int(row.get("page_line_rank")), to_int(row.get("line_rank")))


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
