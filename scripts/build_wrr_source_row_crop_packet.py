#!/usr/bin/env python3
"""Build WRR source-row crop packet from the primary Table 2 render."""

from __future__ import annotations

import argparse
import csv
import json
import math
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.analyze_wrr_primary_table2_row_ocr_probe import (
    build_row_centers,
    read_tsv_words,
    row_bands,
)


DEFAULT_ROW_CHECKLIST = Path(
    "reports/wrr_1994/wrr_source_transcription_row_review_checklist.csv"
)
DEFAULT_TSV = Path("reports/wrr_1994/wrr_primary_table2_row_ocr.tsv")
DEFAULT_IMAGE = Path("reports/wrr_1994/wrr_primary_table2_page-06.png")
DEFAULT_CROP_DIR = Path("reports/wrr_1994/source_review_crops_auto")
DEFAULT_MANUAL_CROP_DIR = Path("reports/wrr_1994/source_review_crops")
DEFAULT_OUT = Path("reports/wrr_1994/wrr_source_row_crop_packet.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/wrr_source_row_crop_packet_summary.csv")
DEFAULT_MD = Path("docs/WRR_SOURCE_ROW_CROP_PACKET.md")
DEFAULT_CONTACT_SHEET = Path("reports/wrr_1994/wrr_source_row_crop_contact_sheet.png")
DEFAULT_CONTACT_MD = Path("docs/WRR_SOURCE_ROW_CROP_CONTACT_SHEET.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_source_row_crop_packet.manifest.json")

NO_INPUT_BOUNDARY = (
    "Crops are review aids only; no row transcription, source correction, pair "
    "exclusion, or method change is selected by this packet."
)

FIELDNAMES = [
    "run_label",
    "row_rank",
    "row_number",
    "concept",
    "action_terms",
    "frontier_pairs",
    "row_band_top",
    "row_band_bottom",
    "crop_left",
    "crop_top",
    "crop_right",
    "crop_bottom",
    "crop_width",
    "crop_height",
    "crop_path",
    "crop_exists",
    "crop_status",
    "manual_crop_count",
    "manual_crop_paths",
    "no_input_boundary",
    "next_manual_action",
]

SUMMARY_FIELDNAMES = ["metric", "value", "read"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    checklist_rows = read_rows(args.row_checklist)
    words = read_tsv_words(args.tsv)
    centers, detected_rows = build_row_centers(words)
    bands = row_bands(centers)
    packet_rows = build_packet_rows(checklist_rows, bands, args)
    write_crops(packet_rows, args)
    contact_summary = write_contact_sheet(packet_rows, args)
    summary_rows = build_summary_rows(packet_rows, detected_rows, args, contact_summary)
    write_csv(args.out, packet_rows, FIELDNAMES)
    write_csv(args.summary_out, summary_rows, SUMMARY_FIELDNAMES)
    write_markdown(args.markdown_out, packet_rows, summary_rows, args)
    write_contact_sheet_markdown(
        args.contact_sheet_markdown_out, packet_rows, summary_rows, args, contact_summary
    )
    write_manifest(args.manifest_out, args, packet_rows, summary_rows, contact_summary, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.contact_sheet_out)
    print(args.contact_sheet_markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--row-checklist", type=Path, default=DEFAULT_ROW_CHECKLIST)
    parser.add_argument("--tsv", type=Path, default=DEFAULT_TSV)
    parser.add_argument("--image", type=Path, default=DEFAULT_IMAGE)
    parser.add_argument("--crop-dir", type=Path, default=DEFAULT_CROP_DIR)
    parser.add_argument("--manual-crop-dir", type=Path, default=DEFAULT_MANUAL_CROP_DIR)
    parser.add_argument("--x-min", type=int, default=500)
    parser.add_argument("--x-max", type=int, default=2050)
    parser.add_argument("--padding-y", type=int, default=8)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--contact-sheet-out", type=Path, default=DEFAULT_CONTACT_SHEET)
    parser.add_argument("--contact-sheet-markdown-out", type=Path, default=DEFAULT_CONTACT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_packet_rows(
    checklist_rows: list[dict[str, str]],
    bands: dict[int, tuple[float, float]],
    args: argparse.Namespace,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in checklist_rows:
        row_number = row.get("row_number", "")
        row_index = int_or_zero(row_number)
        top, bottom = bands.get(row_index, (0.0, 0.0))
        crop_top = max(0, math.floor(top) - args.padding_y)
        crop_bottom = max(crop_top + 1, math.ceil(bottom) + args.padding_y)
        crop_left = max(0, args.x_min)
        crop_right = max(crop_left + 1, args.x_max)
        crop_path = args.crop_dir / f"wrr_table2_row{row_number}_auto.png"
        manual_paths = manual_crop_paths(args.manual_crop_dir, row_number)
        rows.append(
            {
                "run_label": row.get("run_label", ""),
                "row_rank": int_or_zero(row.get("row_rank", "")),
                "row_number": row_number,
                "concept": row.get("concept", ""),
                "action_terms": int_or_zero(row.get("action_terms", "")),
                "frontier_pairs": int_or_zero(row.get("frontier_pairs", "")),
                "row_band_top": f"{top:.2f}",
                "row_band_bottom": f"{bottom:.2f}",
                "crop_left": crop_left,
                "crop_top": crop_top,
                "crop_right": crop_right,
                "crop_bottom": crop_bottom,
                "crop_width": crop_right - crop_left,
                "crop_height": crop_bottom - crop_top,
                "crop_path": str(crop_path),
                "crop_exists": str(crop_path.exists()).lower(),
                "crop_status": "pending_write",
                "manual_crop_count": len(manual_paths),
                "manual_crop_paths": ";".join(str(path) for path in manual_paths),
                "no_input_boundary": NO_INPUT_BOUNDARY,
                "next_manual_action": next_manual_action(row),
            }
        )
    rows.sort(key=lambda item: (int(item["row_rank"]), str(item["row_number"])))
    return rows


def write_crops(rows: list[dict[str, object]], args: argparse.Namespace) -> None:
    image = load_image(args.image)
    width, height = image.size
    args.crop_dir.mkdir(parents=True, exist_ok=True)
    for row in rows:
        left = clamp(int(row["crop_left"]), 0, width - 1)
        top = clamp(int(row["crop_top"]), 0, height - 1)
        right = clamp(int(row["crop_right"]), left + 1, width)
        bottom = clamp(int(row["crop_bottom"]), top + 1, height)
        crop_path = Path(str(row["crop_path"]))
        image.crop((left, top, right, bottom)).save(crop_path)
        row["crop_left"] = left
        row["crop_top"] = top
        row["crop_right"] = right
        row["crop_bottom"] = bottom
        row["crop_width"] = right - left
        row["crop_height"] = bottom - top
        row["crop_exists"] = "true"
        row["crop_status"] = "written_review_aid_only"


def load_image(path: Path):
    try:
        from PIL import Image
    except ImportError as exc:  # pragma: no cover - local dependency guard
        raise RuntimeError("Pillow is required to write row crops") from exc
    return Image.open(path)


def write_contact_sheet(
    rows: list[dict[str, object]], args: argparse.Namespace
) -> dict[str, object]:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as exc:  # pragma: no cover - local dependency guard
        raise RuntimeError("Pillow is required to write row contact sheet") from exc

    label_width = 330
    padding = 18
    row_gap = 12
    crop_gap = 14
    font = ImageFont.load_default()
    opened_rows: list[tuple[dict[str, object], object]] = []
    for row in rows:
        crop_path = Path(str(row["crop_path"]))
        image = Image.open(crop_path).convert("RGB")
        opened_rows.append((row, image))

    max_crop_width = max((image.width for _row, image in opened_rows), default=1)
    total_height = padding
    for _row, image in opened_rows:
        total_height += image.height + row_gap
    total_height += padding
    width = padding + label_width + crop_gap + max_crop_width + padding
    sheet = Image.new("RGB", (width, max(total_height, 1)), "white")
    draw = ImageDraw.Draw(sheet)
    y = padding
    for row, image in opened_rows:
        label = (
            f"rank {row['row_rank']} | row {row['row_number']} | "
            f"terms {row['action_terms']} | frontier {row['frontier_pairs']}"
        )
        draw.text((padding, y + 6), label, fill="black", font=font)
        crop_x = padding + label_width + crop_gap
        sheet.paste(image, (crop_x, y))
        draw.rectangle(
            (crop_x, y, crop_x + image.width - 1, y + image.height - 1),
            outline="black",
            width=1,
        )
        y += image.height + row_gap

    args.contact_sheet_out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.contact_sheet_out)
    return {
        "contact_sheet_path": str(args.contact_sheet_out),
        "contact_sheet_exists": args.contact_sheet_out.exists(),
        "contact_sheet_width": sheet.width,
        "contact_sheet_height": sheet.height,
        "contact_sheet_rows": len(opened_rows),
    }


def build_summary_rows(
    rows: list[dict[str, object]],
    detected_rows: set[int],
    args: argparse.Namespace,
    contact_summary: dict[str, object],
) -> list[dict[str, object]]:
    manual_rows = sum(1 for row in rows if int(row.get("manual_crop_count", 0)) > 0)
    return [
        metric("source_rows", len(rows), "source-transcription rows with crop entries"),
        metric("auto_crops_available", count_value(rows, "crop_exists", "true"), str(args.crop_dir)),
        metric(
            "contact_sheet_available",
            str(contact_summary["contact_sheet_exists"]).lower(),
            str(args.contact_sheet_out),
        ),
        metric(
            "contact_sheet_rows",
            contact_summary["contact_sheet_rows"],
            "rows rendered into local contact sheet",
        ),
        metric(
            "existing_manual_crop_rows_in_checklist",
            manual_rows,
            str(args.manual_crop_dir),
        ),
        metric("action_terms", sum_int(rows, "action_terms"), "terms requiring row-level review"),
        metric("frontier_pairs", sum_int(rows, "frontier_pairs"), "minimum-frontier pair links"),
        metric("detected_row_markers", len(detected_rows), "OCR row markers detected from TSV"),
        metric("crop_boundary", NO_INPUT_BOUNDARY, "no source or method decision selected"),
    ]


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    summary = {str(row["metric"]): row for row in summary_rows}
    lines = [
        "# WRR Source Row Crop Packet",
        "",
        "Status: no-input row-crop packet for WRR source-row review.",
        "It writes local review crops only; it does not choose row transcriptions, source corrections, method changes, or pair exclusions.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_source_row_crop_packet "
            f"--row-checklist {args.row_checklist} "
            f"--tsv {args.tsv} "
            f"--image {args.image} "
            f"--crop-dir {args.crop_dir} "
            f"--manual-crop-dir {args.manual_crop_dir} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--contact-sheet-out {args.contact_sheet_out} "
            f"--contact-sheet-markdown-out {args.contact_sheet_markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Source rows: {summary['source_rows']['value']}.",
        f"- Auto row crops available: {summary['auto_crops_available']['value']}.",
        f"- Contact sheet available: {summary['contact_sheet_available']['value']} at `{args.contact_sheet_out}`.",
        f"- Existing manual crop rows in checklist: {summary['existing_manual_crop_rows_in_checklist']['value']}.",
        f"- Action terms: {summary['action_terms']['value']}.",
        f"- Frontier pairs: {summary['frontier_pairs']['value']}.",
        f"- Boundary: {NO_INPUT_BOUNDARY}",
        "",
        "## Row Crops",
        "",
        "| Rank | Row | Terms | Frontier | Auto crop | Manual crops | Next action |",
        "| ---: | --- | ---: | ---: | --- | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| {row_rank} | `{row_number}` | {action_terms} | {frontier_pairs} | "
            "`{crop_path}` | {manual_crop_count} | {next_manual_action} |".format(
                **markdown_row(row)
            )
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- These crops are generated from the current local Table 2 page render.",
            "- Crop availability is not transcription verification.",
            "- Manual visual notes remain triage notes unless a separate decision record cites source evidence.",
            "- No row here changes the working WRR source or excludes a pair automatically.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_contact_sheet_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    args: argparse.Namespace,
    contact_summary: dict[str, object],
) -> None:
    summary = {str(row["metric"]): row for row in summary_rows}
    lines = [
        "# WRR Source Row Crop Contact Sheet",
        "",
        "Status: local visual contact sheet for WRR source-row review.",
        "It is a review aid only; it is not transcription verification and does not choose row transcriptions, source corrections, method changes, or pair exclusions.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_source_row_crop_packet "
            f"--row-checklist {args.row_checklist} "
            f"--tsv {args.tsv} "
            f"--image {args.image} "
            f"--crop-dir {args.crop_dir} "
            f"--manual-crop-dir {args.manual_crop_dir} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--contact-sheet-out {args.contact_sheet_out} "
            f"--contact-sheet-markdown-out {args.contact_sheet_markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- Source rows: {summary['source_rows']['value']}.",
        f"- Contact sheet rows: {contact_summary['contact_sheet_rows']}.",
        f"- Contact sheet image: `{args.contact_sheet_out}`.",
        f"- Contact sheet dimensions: {contact_summary['contact_sheet_width']} x {contact_summary['contact_sheet_height']}.",
        f"- Boundary: {NO_INPUT_BOUNDARY}",
        "",
        "## Local Image",
        "",
        f"![WRR source row crop contact sheet](../{args.contact_sheet_out})",
        "",
        "## Row Order",
        "",
        "| Rank | Row | Terms | Frontier | Auto crop |",
        "| ---: | --- | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| {row_rank} | `{row_number}` | {action_terms} | {frontier_pairs} | "
            "`{crop_path}` |".format(**markdown_row(row))
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- The contact sheet is generated from local crop images under `reports/`.",
            "- Crop availability is not transcription verification.",
            "- Manual visual notes remain triage notes unless a separate decision record cites source evidence.",
            "- No row here changes the working WRR source or excludes a pair automatically.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    contact_summary: dict[str, object],
    started: float,
) -> None:
    payload = {
        "tool": "build_wrr_source_row_crop_packet",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "rows": len(rows),
        "summary": {row["metric"]: row["value"] for row in summary_rows},
        "contact_sheet": contact_summary,
        "inputs": {
            "row_checklist": str(args.row_checklist),
            "tsv": str(args.tsv),
            "image": str(args.image),
            "manual_crop_dir": str(args.manual_crop_dir),
        },
        "outputs": {
            "crop_dir": str(args.crop_dir),
            "out": str(args.out),
            "summary_out": str(args.summary_out),
            "markdown_out": str(args.markdown_out),
            "contact_sheet_out": str(args.contact_sheet_out),
            "contact_sheet_markdown_out": str(args.contact_sheet_markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def manual_crop_paths(root: Path, row_number: str) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.glob(f"wrr_table2_row{row_number}*.png"))


def next_manual_action(row: dict[str, str]) -> str:
    frontier = int_or_zero(row.get("frontier_pairs", ""))
    if frontier > 0:
        return "inspect generated crop against source row before any frontier source decision"
    return "keep crop as later review aid unless policy scope changes"


def metric(name: str, value: object, read: str) -> dict[str, object]:
    return {"metric": name, "value": value, "read": read}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def count_value(rows: list[dict[str, object]], field: str, value: str) -> int:
    return sum(1 for row in rows if str(row.get(field, "")) == value)


def sum_int(rows: list[dict[str, object]], field: str) -> int:
    return sum(int_or_zero(str(row.get(field, ""))) for row in rows)


def int_or_zero(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


def clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(value, maximum))


def markdown_row(row: dict[str, object]) -> dict[str, str]:
    return {key: markdown_cell(value) for key, value in row.items()}


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


if __name__ == "__main__":
    raise SystemExit(main())
