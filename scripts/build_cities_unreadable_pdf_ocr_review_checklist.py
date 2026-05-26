#!/usr/bin/env python3
"""Build Cities unreadable-PDF OCR review checklist and local contact sheets."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell, markdown_link


DEFAULT_PACKET = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_review_packet.csv"
)
DEFAULT_OUT = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_review_checklist.csv"
)
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_review_checklist_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_UNREADABLE_PDF_OCR_REVIEW_CHECKLIST.md")
DEFAULT_CONTACT_SHEET = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_contact_sheet.png"
)
DEFAULT_CONTACT_DIR = Path("reports/cities_pdf_recovery_probe/unreadable_pdf_ocr_review/contact_sheets")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_unreadable_pdf_ocr_review_checklist.manifest.json"
)

CLAIM_BOUNDARY = (
    "OCR review checklist only; contact sheets and OCR text sidecars are ignored "
    "local review aids; no OCR text in tracked files, no repaired text, no "
    "source-row import, no city normalization, no ELS, no compactness, no p-level"
)

FIELDNAMES = [
    "review_rank",
    "label",
    "family",
    "lane",
    "pages_total",
    "pages_with_ocr_text",
    "pages_without_ocr_text",
    "low_signal_pages",
    "ocr_text_signal_chars",
    "ocr_words",
    "ocr_lines",
    "contact_sheet_path",
    "all_contact_sheet_path",
    "review_priority",
    "review_state",
    "next_manual_action",
    "claim_boundary",
]

SUMMARY_FIELDNAMES = ["metric", "value"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    packet_rows = read_csv(args.packet)
    checklist_rows = build_checklist_rows(packet_rows, args)
    contact_summary = write_contact_sheets(packet_rows, checklist_rows, args)
    summary_rows = build_summary_rows(checklist_rows, contact_summary)
    write_csv(args.out, FIELDNAMES, checklist_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, checklist_rows, summary_rows, args, contact_summary)
    write_manifest(
        args.manifest_out,
        args,
        checklist_rows,
        summary_rows,
        contact_summary,
        started,
    )
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.contact_sheet_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--contact-sheet-out", type=Path, default=DEFAULT_CONTACT_SHEET)
    parser.add_argument("--contact-sheet-dir", type=Path, default=DEFAULT_CONTACT_DIR)
    parser.add_argument("--thumb-width", type=int, default=240)
    parser.add_argument("--thumb-height", type=int, default=320)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_checklist_rows(
    packet_rows: list[dict[str, str]], args: argparse.Namespace
) -> list[dict[str, str]]:
    by_label: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in packet_rows:
        by_label[row.get("label", "")].append(row)

    rows: list[dict[str, str]] = []
    for label, page_rows in by_label.items():
        page_rows = sorted(page_rows, key=lambda row: int_or_zero(row.get("page_number", "")))
        pages_without_text = [
            row["page_number"]
            for row in page_rows
            if row.get("ocr_status") != "page_ocr_text_detected"
        ]
        low_signal_pages = [
            row["page_number"]
            for row in page_rows
            if int_or_zero(row.get("ocr_text_signal_chars", "")) < 100
        ]
        first = page_rows[0]
        rows.append(
            {
                "review_rank": "0",
                "label": label,
                "family": first.get("family", ""),
                "lane": first.get("lane", ""),
                "pages_total": str(len(page_rows)),
                "pages_with_ocr_text": str(len(page_rows) - len(pages_without_text)),
                "pages_without_ocr_text": str(len(pages_without_text)),
                "low_signal_pages": ";".join(low_signal_pages),
                "ocr_text_signal_chars": str(sum_int(page_rows, "ocr_text_signal_chars")),
                "ocr_words": str(sum_int(page_rows, "ocr_word_count")),
                "ocr_lines": str(sum_int(page_rows, "ocr_line_count")),
                "contact_sheet_path": str(args.contact_sheet_dir / f"{label}.png"),
                "all_contact_sheet_path": str(args.contact_sheet_out),
                "review_priority": review_priority(first, len(pages_without_text), low_signal_pages),
                "review_state": "awaiting_page_image_vs_ocr_sidecar_review",
                "next_manual_action": next_manual_action(first, pages_without_text, low_signal_pages),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.sort(key=sort_key)
    for index, row in enumerate(rows, start=1):
        row["review_rank"] = str(index)
    return rows


def review_priority(
    row: dict[str, str], pages_without_text: int, low_signal_pages: list[str]
) -> str:
    if pages_without_text:
        return "1_empty_or_low_ocr_pages"
    if row.get("lane") == "encoding_or_ocr_candidate":
        return "2_encoding_or_ocr_candidate"
    if row.get("family") == "aumann_committee":
        return "3_aumann_ocr_image_only"
    return "4_context_pdf"


def next_manual_action(
    row: dict[str, str], pages_without_text: list[str], low_signal_pages: list[str]
) -> str:
    if pages_without_text:
        return (
            "inspect page images for OCR-empty pages "
            + ",".join(pages_without_text)
            + " before any OCR sidecar use"
        )
    if low_signal_pages:
        return (
            "compare low-signal OCR pages "
            + ",".join(low_signal_pages)
            + " against page images before any source-row use"
        )
    if row.get("lane") == "encoding_or_ocr_candidate":
        return "compare OCR sidecars against page images before treating garbled extraction as replaceable"
    if row.get("family") == "aumann_committee":
        return "compare OCR sidecars against page images before any Aumann source-row decision"
    return "review as context paper; do not import source rows without separate source decision"


def sort_key(row: dict[str, str]) -> tuple[str, str]:
    return (row["review_priority"], row["label"])


def write_contact_sheets(
    packet_rows: list[dict[str, str]],
    checklist_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> dict[str, object]:
    args.contact_sheet_dir.mkdir(parents=True, exist_ok=True)
    by_label: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in packet_rows:
        by_label[row.get("label", "")].append(row)
    written = 0
    for checklist in checklist_rows:
        label = checklist["label"]
        out = Path(checklist["contact_sheet_path"])
        page_rows = sorted(by_label[label], key=lambda row: int_or_zero(row.get("page_number", "")))
        write_contact_sheet(page_rows, out, args, columns=min(4, max(1, len(page_rows))))
        written += 1
    write_contact_sheet(packet_rows, args.contact_sheet_out, args, columns=4)
    return {
        "label_contact_sheets": written,
        "all_contact_sheet_path": str(args.contact_sheet_out),
        "all_contact_sheet_exists": args.contact_sheet_out.exists(),
    }


def write_contact_sheet(
    rows: list[dict[str, str]],
    path: Path,
    args: argparse.Namespace,
    *,
    columns: int,
) -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageOps
    except ImportError as exc:  # pragma: no cover - local dependency guard
        raise RuntimeError("Pillow is required to write OCR review contact sheets") from exc

    font = ImageFont.load_default()
    padding = 16
    label_height = 52
    gap = 14
    cell_width = args.thumb_width + padding * 2
    cell_height = args.thumb_height + label_height + padding * 2
    rows_count = (len(rows) + columns - 1) // columns if rows else 1
    sheet = Image.new(
        "RGB",
        (columns * cell_width + gap * (columns - 1), rows_count * cell_height + gap * (rows_count - 1)),
        "white",
    )
    draw = ImageDraw.Draw(sheet)
    for index, row in enumerate(rows):
        col = index % columns
        row_index = index // columns
        x = col * (cell_width + gap)
        y = row_index * (cell_height + gap)
        image_box = (x + padding, y + padding + label_height)
        source = Path(row.get("image_path", ""))
        if source.exists():
            image = Image.open(source).convert("RGB")
            thumb = ImageOps.contain(image, (args.thumb_width, args.thumb_height))
        else:
            thumb = Image.new("RGB", (args.thumb_width, args.thumb_height), "white")
        label = (
            f"{row.get('label', '')}\n"
            f"p{row.get('page_number', '')} | {row.get('ocr_status', '')} | "
            f"{row.get('ocr_text_signal_chars', '0')} chars"
        )
        draw.multiline_text((x + padding, y + padding), label, fill="black", font=font, spacing=2)
        sheet.paste(thumb, image_box)
        draw.rectangle(
            (
                image_box[0],
                image_box[1],
                image_box[0] + thumb.width - 1,
                image_box[1] + thumb.height - 1,
            ),
            outline="black",
            width=1,
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path)


def build_summary_rows(
    rows: list[dict[str, str]], contact_summary: dict[str, object]
) -> list[dict[str, str]]:
    return [
        metric("checklist_rows", len(rows)),
        metric("pdf_rows", len(rows)),
        metric("pages_total", sum_int(rows, "pages_total")),
        metric("pages_with_ocr_text", sum_int(rows, "pages_with_ocr_text")),
        metric("pages_without_ocr_text", sum_int(rows, "pages_without_ocr_text")),
        metric("ocr_text_signal_chars", sum_int(rows, "ocr_text_signal_chars")),
        metric("ocr_words", sum_int(rows, "ocr_words")),
        metric("ocr_lines", sum_int(rows, "ocr_lines")),
        metric("label_contact_sheets", contact_summary["label_contact_sheets"]),
        metric("all_contact_sheet_exists", str(contact_summary["all_contact_sheet_exists"]).lower()),
        metric("claim_boundary", CLAIM_BOUNDARY),
    ]


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    args: argparse.Namespace,
    contact_summary: dict[str, object],
) -> None:
    summary = {row["metric"]: row["value"] for row in summary_rows}
    lines = [
        "# Cities Unreadable PDF OCR Review Checklist",
        "",
        "Status: no-input OCR review checklist. This groups ignored local page-image and OCR-text sidecars into review order and creates contact sheets.",
        "It does not track OCR text, repair text, import source rows, normalize city names, run ELS searches, compute compactness, or verify p-levels.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_unreadable_pdf_ocr_review_checklist "
            f"--packet {args.packet} "
            f"--contact-sheet-out {args.contact_sheet_out} "
            f"--contact-sheet-dir {args.contact_sheet_dir} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Summary",
        "",
        f"- Checklist rows: {summary['checklist_rows']}.",
        f"- PDF rows: {summary['pdf_rows']}.",
        f"- Pages total: {summary['pages_total']}.",
        f"- Pages with OCR text: {summary['pages_with_ocr_text']}.",
        f"- Pages without OCR text: {summary['pages_without_ocr_text']}.",
        f"- OCR text signal chars: {summary['ocr_text_signal_chars']}.",
        f"- OCR words: {summary['ocr_words']}.",
        f"- OCR lines: {summary['ocr_lines']}.",
        f"- Label contact sheets: {summary['label_contact_sheets']}.",
        f"- All-pages contact sheet: `{contact_summary['all_contact_sheet_path']}`.",
        f"- Boundary: {CLAIM_BOUNDARY}",
        "",
        f"![Cities unreadable PDF OCR contact sheet](../{contact_summary['all_contact_sheet_path']})",
        "",
        "## Checklist",
        "",
        "| Rank | Label | Lane | Pages | With text | Empty | Low-signal pages | Contact sheet | Priority | Next action |",
        "| ---: | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["review_rank"]),
                    markdown_cell(row["label"]),
                    f"`{markdown_cell(row['lane'])}`",
                    markdown_cell(row["pages_total"]),
                    markdown_cell(row["pages_with_ocr_text"]),
                    markdown_cell(row["pages_without_ocr_text"]),
                    markdown_cell(row["low_signal_pages"]),
                    markdown_link("sheet", "../" + row["contact_sheet_path"]),
                    markdown_cell(row["review_priority"]),
                    markdown_cell(row["next_manual_action"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Contact sheets are visual review aids only.",
            "- OCR sidecars remain ignored local files and are not tracked source text.",
            "- Source-row decisions require separate citable decision records.",
            "- No row here changes source admissibility or creates city-name rows.",
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
        "inputs": {"packet": str(args.packet)},
        "parameters": {
            "contact_sheet_out": str(args.contact_sheet_out),
            "contact_sheet_dir": str(args.contact_sheet_dir),
            "thumb_width": args.thumb_width,
            "thumb_height": args.thumb_height,
        },
        "rows": len(rows),
        "summary": {row["metric"]: row["value"] for row in summary_rows},
        "contact_summary": contact_summary,
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def metric(name: str, value: object) -> dict[str, str]:
    return {"metric": name, "value": str(value)}


def sum_int(rows: list[dict[str, str]], field: str) -> int:
    return sum(int_or_zero(row.get(field, "")) for row in rows)


def int_or_zero(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


def read_csv(path: Path) -> list[dict[str, str]]:
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
