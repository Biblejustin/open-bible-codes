#!/usr/bin/env python3
"""Build local contact sheet for locked Cities source-page review."""

from __future__ import annotations

import argparse
import csv
import json
import struct
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell


DEFAULT_BUNDLE = Path("reports/cities_pdf_recovery_probe/cities_source_page_review_bundle.csv")
DEFAULT_CONTACT_SHEET = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_contact_sheet.png"
)
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_contact_sheet_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_PAGE_CONTACT_SHEET.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_contact_sheet.manifest.json"
)

NO_INPUT_BOUNDARY = (
    "Contact sheet only; local page images are visual review aids, no OCR body "
    "text, no source-script body text in tracked files, no source-row import, "
    "no city normalization, no ELS, no compactness, no p-level"
)

SUMMARY_FIELDNAMES = ["metric", "value"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = read_rows(args.bundle)
    contact_summary = write_contact_sheet(rows, args)
    summary_rows = build_summary_rows(rows, contact_summary)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, rows, summary_rows, args)
    write_manifest(args.manifest_out, args, rows, summary_rows, contact_summary, started)
    print(args.contact_sheet_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--contact-sheet-out", type=Path, default=DEFAULT_CONTACT_SHEET)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--thumb-width", type=int, default=360)
    parser.add_argument("--thumb-height", type=int, default=480)
    parser.add_argument("--columns", type=int, default=2)
    return parser


def write_contact_sheet(
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> dict[str, object]:
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageOps
    except ImportError as exc:  # pragma: no cover - local dependency guard
        raise RuntimeError("Pillow is required to write contact sheets") from exc

    columns = max(1, args.columns)
    rows_count = (len(rows) + columns - 1) // columns if rows else 1
    padding = 18
    gap = 16
    label_height = 58
    cell_width = args.thumb_width + padding * 2
    cell_height = args.thumb_height + label_height + padding * 2
    width = columns * cell_width + gap * (columns - 1)
    height = rows_count * cell_height + gap * (rows_count - 1)
    sheet = Image.new("RGB", (max(width, 1), max(height, 1)), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for index, row in enumerate(rows):
        column = index % columns
        row_index = index // columns
        x = column * (cell_width + gap)
        y = row_index * (cell_height + gap)
        image_path = Path(row.get("page_image_path", ""))
        if image_path.exists():
            image = Image.open(image_path).convert("RGB")
            thumb = ImageOps.contain(image, (args.thumb_width, args.thumb_height))
        else:
            thumb = Image.new("RGB", (args.thumb_width, args.thumb_height), "white")
        label = (
            f"{row.get('bundle_rank', '')}. {row.get('transcription_decision_id', '')}\n"
            f"{row.get('label', '')} p{row.get('page_number', '')} | "
            f"{row.get('page_class', '')}"
        )
        draw.multiline_text(
            (x + padding, y + padding),
            label,
            fill="black",
            font=font,
            spacing=2,
        )
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

    args.contact_sheet_out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.contact_sheet_out)
    actual_width, actual_height = png_dimensions(args.contact_sheet_out)
    return {
        "contact_sheet_exists": args.contact_sheet_out.exists(),
        "contact_sheet_path": str(args.contact_sheet_out),
        "contact_sheet_pages": len(rows),
        "contact_sheet_width": actual_width,
        "contact_sheet_height": actual_height,
    }


def build_summary_rows(
    rows: list[dict[str, str]],
    contact_summary: dict[str, object],
) -> list[dict[str, str]]:
    return [
        metric("contact_sheet_pages", contact_summary["contact_sheet_pages"]),
        metric("contact_sheet_exists", str(contact_summary["contact_sheet_exists"]).lower()),
        metric("contact_sheet_path", contact_summary["contact_sheet_path"]),
        metric("contact_sheet_width", contact_summary["contact_sheet_width"]),
        metric("contact_sheet_height", contact_summary["contact_sheet_height"]),
        metric("page_images_found", count_value(rows, "page_image_exists", "true")),
        metric("page_images_missing", count_value(rows, "page_image_exists", "false")),
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
        "# Cities Source Page Contact Sheet",
        "",
        "Status: local visual contact sheet for locked Cities source-page review.",
        "It is a review aid only; it is not transcription verification and it does not import source rows.",
        "Tracked files contain no OCR body text or source-script body text.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_page_contact_sheet "
            f"--bundle {args.bundle} "
            f"--contact-sheet-out {args.contact_sheet_out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Contact sheet image: `{summary['contact_sheet_path']}`.",
        f"- Contact sheet pages: {summary['contact_sheet_pages']}.",
        f"- Contact sheet dimensions: {summary['contact_sheet_width']} x {summary['contact_sheet_height']}.",
        f"- Page images found: {summary['page_images_found']}.",
        f"- Page images missing: {summary['page_images_missing']}.",
        f"- Source-row imports: {summary['source_row_imports']}.",
        f"- City-name normalization: {summary['city_name_normalization']}.",
        f"- ELS runs: {summary['els_runs']}.",
        f"- Compactness runs: {summary['compactness_runs']}.",
        f"- p-levels: {summary['p_levels']}.",
        f"- Boundary: {NO_INPUT_BOUNDARY}",
        "",
        f"![Cities source page contact sheet](../{summary['contact_sheet_path']})",
        "",
        "## Page Order",
        "",
        "| Rank | Transcription id | Label | Page | Class | Page image |",
        "| ---: | --- | --- | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["bundle_rank"]),
                    f"`{markdown_cell(row['transcription_decision_id'])}`",
                    markdown_cell(row["label"]),
                    markdown_cell(row["page_number"]),
                    f"`{markdown_cell(row['page_class'])}`",
                    f"`{markdown_cell(row['page_image_path'])}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Contact-sheet availability is not transcription verification.",
            "- Manual visual review still needs readable transcription and row/column alignment evidence before any source-row import.",
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
    contact_summary: dict[str, object],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {"bundle": str(args.bundle)},
        "outputs": {
            "contact_sheet": str(args.contact_sheet_out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(rows),
        "contact_sheet": contact_summary,
        "summary": {row["metric"]: row["value"] for row in summary_rows},
        "no_input_boundary": NO_INPUT_BOUNDARY,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def png_dimensions(path: Path) -> tuple[int, int]:
    if not path.exists():
        return 0, 0
    with path.open("rb") as handle:
        header = handle.read(24)
    if header.startswith(b"\x89PNG\r\n\x1a\n") and header[12:16] == b"IHDR":
        return tuple(int(value) for value in struct.unpack(">II", header[16:24]))
    return 0, 0


def count_value(rows: list[dict[str, str]], field: str, value: str) -> int:
    return sum(1 for row in rows if row.get(field) == value)


def metric(name: str, value: object) -> dict[str, str]:
    return {"metric": name, "value": str(value)}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
