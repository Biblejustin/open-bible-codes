#!/usr/bin/env python3
"""Build local contact sheets for Cities source-page line-crop review."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.build_cities_source_page_line_crop_packet import DEFAULT_OUT as DEFAULT_PACKET
from scripts.build_cities_source_page_line_crop_review_worksheet import CLAIM_BOUNDARY
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell


DEFAULT_BASE_DIR = Path("reports/cities_pdf_recovery_probe/source_page_line_crops/contact_sheets")
DEFAULT_OUT = Path("reports/cities_pdf_recovery_probe/cities_source_page_line_crop_contact_sheet.csv")
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_contact_sheet_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_PAGE_LINE_CROP_CONTACT_SHEET.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_contact_sheet.manifest.json"
)

NO_INPUT_BOUNDARY = (
    "contact sheets only; local line-crop images are visual review aids, no OCR "
    "body text or source-script body text in tracked files, no verified "
    "transcription, no source-row import, no city normalization, no ELS, no "
    "compactness, no p-level"
)

FIELDNAMES = [
    "sheet_rank",
    "transcription_decision_id",
    "page_number",
    "page_class",
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
    rows = read_rows(args.packet)
    sheet_rows = build_contact_sheet_rows(rows, args)
    write_csv(args.out, FIELDNAMES, sheet_rows)
    summary_rows = build_summary_rows(rows, sheet_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, sheet_rows, summary_rows, args)
    write_manifest(args.manifest_out, args, rows, sheet_rows, summary_rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--base-dir", type=Path, default=DEFAULT_BASE_DIR)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--thumb-width", type=int, default=980)
    parser.add_argument("--thumb-height", type=int, default=72)
    parser.add_argument("--columns", type=int, default=1)
    return parser


def build_contact_sheet_rows(
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row.get("transcription_decision_id", "")].append(row)
    sheet_rows: list[dict[str, str]] = []
    for sheet_rank, transcription_id in enumerate(sorted(grouped), start=1):
        page_rows = sorted(grouped[transcription_id], key=line_key)
        contact_path = args.base_dir / f"{transcription_id}_line_crops.png"
        summary = write_contact_sheet(contact_path, page_rows, args)
        first = page_rows[0]
        sheet_rows.append(
            {
                "sheet_rank": str(sheet_rank),
                "transcription_decision_id": transcription_id,
                "page_number": first.get("page_number", ""),
                "page_class": first.get("page_class", ""),
                "line_crop_rows": str(len(page_rows)),
                "line_crop_images_found": str(count_value(page_rows, "crop_exists", "true")),
                "ocr_word_count": str(sum_int(page_rows, "ocr_word_count")),
                "ocr_hebrew_letters": str(sum_int(page_rows, "ocr_hebrew_letters")),
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
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> dict[str, int]:
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageOps
    except ImportError as exc:  # pragma: no cover - local dependency guard
        raise RuntimeError("Pillow is required to write contact sheets") from exc

    columns = max(1, args.columns)
    row_count = (len(rows) + columns - 1) // columns if rows else 1
    padding = 14
    gap = 10
    label_height = 38
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
    actual_width, actual_height = png_dimensions(path)
    return {
        "contact_sheet_width": actual_width,
        "contact_sheet_height": actual_height,
    }


def build_summary_rows(
    packet_rows: list[dict[str, str]],
    sheet_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    return [
        metric("table_pages", len(sheet_rows)),
        metric("line_crop_rows", len(packet_rows)),
        metric("line_crop_images_found", count_value(packet_rows, "crop_exists", "true")),
        metric("contact_sheets", len(sheet_rows)),
        metric("contact_sheets_available", count_value(sheet_rows, "contact_sheet_exists", "true")),
        metric("ocr_words", sum_int(packet_rows, "ocr_word_count")),
        metric("ocr_hebrew_letters", sum_int(packet_rows, "ocr_hebrew_letters")),
        metric("source_row_imports", 0),
        metric("city_name_normalization", 0),
        metric("els_runs", 0),
        metric("compactness_runs", 0),
        metric("p_levels", 0),
        metric("no_input_boundary", NO_INPUT_BOUNDARY),
    ]


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    summary = {row["metric"]: row["value"] for row in summary_rows}
    lines = [
        "# Cities Source Page Line Crop Contact Sheet",
        "",
        "Status: local visual contact sheets for Cities source-page line-crop review.",
        "These contact sheets help review crop order and row shape without transcribing Hebrew or importing source rows.",
        "Tracked files contain no OCR body text or source-script body text.",
        CLAIM_BOUNDARY,
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_page_line_crop_contact_sheet "
            f"--packet {args.packet} "
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
        f"- Table pages: {summary['table_pages']}.",
        f"- Line crop rows: {summary['line_crop_rows']}.",
        f"- Line crop images found: {summary['line_crop_images_found']}.",
        f"- Contact sheets: {summary['contact_sheets']}.",
        f"- Contact sheets available: {summary['contact_sheets_available']}.",
        f"- OCR words represented by line boxes: {summary['ocr_words']}.",
        f"- OCR Hebrew letters represented by line boxes: {summary['ocr_hebrew_letters']}.",
        f"- Source-row imports: {summary['source_row_imports']}.",
        f"- City-name normalization: {summary['city_name_normalization']}.",
        f"- ELS runs: {summary['els_runs']}.",
        f"- Compactness runs: {summary['compactness_runs']}.",
        f"- p-levels: {summary['p_levels']}.",
        f"- Boundary: {NO_INPUT_BOUNDARY}",
        "",
        "## Contact Sheets",
        "",
        "| Rank | Transcription id | Page | Line crops | Image rows | Sheet | Dimensions |",
        "| ---: | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["sheet_rank"]),
                    f"`{markdown_cell(row['transcription_decision_id'])}`",
                    markdown_cell(row["page_number"]),
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
            "- Contact sheets are not transcription verification.",
            "- Image review can sort crops by visual role, but it does not read or import Hebrew source rows.",
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
    sheet_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {"packet": str(args.packet)},
        "outputs": {
            "base_dir": str(args.base_dir),
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(sheet_rows),
        "line_crop_rows": len(packet_rows),
        "summary": {row["metric"]: row["value"] for row in summary_rows},
        "no_input_boundary": NO_INPUT_BOUNDARY,
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


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        return (0, 0)
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    return width, height


def line_key(row: dict[str, str]) -> tuple[int, int]:
    return safe_int(row.get("page_line_rank", "0")), safe_int(row.get("line_rank", "0"))


def safe_int(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


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


def metric(name: str, value: object) -> dict[str, str]:
    return {"metric": name, "value": str(value)}


if __name__ == "__main__":
    raise SystemExit(main())
