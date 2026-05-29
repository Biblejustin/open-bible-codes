#!/usr/bin/env python3
"""Build ignored local HTML for Cities line-crop priority review."""

from __future__ import annotations

import argparse
import csv
import html
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts import build_cities_source_page_line_crop_priority_contact_sheet as priority_contact
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell


DEFAULT_PRIORITY_CONTACT = priority_contact.DEFAULT_OUT
DEFAULT_HTML = Path("reports/cities_pdf_recovery_probe/source_page_line_crops/priority_review.html")
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_priority_review_html_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_PAGE_LINE_CROP_PRIORITY_REVIEW_HTML.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_priority_review_html.manifest.json"
)

LOCAL_HTML_BOUNDARY = (
    "Local ignored priority HTML review aid; HTML displays priority contact-sheet "
    "images only, tracked files contain no OCR body text or source-script body "
    "text, no verified transcription, no source-row import, no city "
    "normalization, no ELS, no compactness, no p-level"
)

SUMMARY_FIELDNAMES = ["metric", "value"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    fieldnames, priority_rows = read_csv(args.priority_contact)
    html_summary = write_priority_html(priority_rows, args)
    summary_rows = build_summary_rows(fieldnames, priority_rows, html_summary)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, priority_rows, summary_rows, args)
    write_manifest(args.manifest_out, args, priority_rows, summary_rows, started)
    print(args.html_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--priority-contact", type=Path, default=DEFAULT_PRIORITY_CONTACT)
    parser.add_argument("--html-out", type=Path, default=DEFAULT_HTML)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def write_priority_html(
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> dict[str, object]:
    body = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        "<title>Cities Source Page Line Crop Priority Review</title>",
        "<style>",
        "body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;margin:24px;background:#f8f8f6;color:#181818;max-width:1240px}",
        "h1{font-size:24px;margin:0 0 8px}",
        ".notice{max-width:980px;margin-bottom:18px;line-height:1.45}",
        ".priority{margin:0 0 30px;padding:16px;background:white;border:1px solid #ccc}",
        ".priority h2{font-size:18px;margin:0 0 12px}",
        ".meta{font-size:12px;line-height:1.35;margin-bottom:8px;color:#333}",
        ".badge{display:inline-block;border:1px solid #888;padding:1px 5px;margin-right:4px;background:#f1f1ee}",
        "img{max-width:100%;height:auto;border:1px solid #ddd;background:white}",
        "code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}",
        "@media(max-width:700px){body{margin:12px}.priority{padding:10px}}",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Cities Source Page Line Crop Priority Review</h1>",
        '<div class="notice">',
        "<p>Local ignored review aid. Compare priority contact-sheet images before any transcription or source-row import.</p>",
        "<p>This file displays contact-sheet images only. It does not embed OCR text or source-script text.</p>",
        f"<p><code>{html.escape(LOCAL_HTML_BOUNDARY)}</code></p>",
        "</div>",
    ]
    embedded_rows = 0
    for row in sorted(rows, key=lambda item: safe_int(item.get("sheet_rank", "0"))):
        sheet_path = Path(row.get("contact_sheet_path", ""))
        if sheet_path.exists():
            embedded_rows += 1
        priority = row.get("review_priority", "")
        body.extend(
            [
                '<article class="priority">',
                (
                    f"<h2>Priority <code>{html.escape(row.get('sheet_rank', ''))}</code> "
                    f"<span class=\"badge\"><code>{html.escape(priority)}</code></span></h2>"
                ),
                '<div class="meta">',
                f"Line crops: <code>{html.escape(row.get('line_crop_rows', ''))}</code> | ",
                f"Images: <code>{html.escape(row.get('line_crop_images_found', ''))}</code> | ",
                f"Pages represented: <code>{html.escape(row.get('unique_table_pages', ''))}</code> | ",
                f"Words: <code>{html.escape(row.get('ocr_word_count', ''))}</code> | ",
                f"Letters: <code>{html.escape(row.get('ocr_hebrew_letters', ''))}</code><br>",
                f"Sheet: <code>{html.escape(str(sheet_path))}</code>",
                "</div>",
                f'<img src="{html.escape(rel_href(args.html_out, sheet_path))}" alt="{html.escape(priority)} contact sheet">',
                "</article>",
            ]
        )
    body.extend(["</body>", "</html>"])
    args.html_out.parent.mkdir(parents=True, exist_ok=True)
    args.html_out.write_text("\n".join(body) + "\n", encoding="utf-8")
    return {
        "html_exists": args.html_out.exists(),
        "html_path": str(args.html_out),
        "html_rows": len(rows),
        "html_priority_image_rows": embedded_rows,
    }


def build_summary_rows(
    priority_contact_fieldnames: list[str],
    rows: list[dict[str, str]],
    html_summary: dict[str, object],
) -> list[dict[str, str]]:
    priorities = Counter(row.get("review_priority", "") for row in rows)
    summary: list[tuple[str, str | int]] = [
        (
            "priority_contact_fieldnames_match",
            str(priority_contact_fieldnames == priority_contact.FIELDNAMES).lower(),
        ),
        ("html_rows", html_summary["html_rows"]),
        ("html_exists", str(html_summary["html_exists"]).lower()),
        ("html_path", html_summary["html_path"]),
        ("html_embeds_source_text", "false"),
        ("html_priority_image_rows", html_summary["html_priority_image_rows"]),
        ("priority_contact_sheet_rows", len(rows)),
        ("priority_contact_sheets_available", count_value(rows, "contact_sheet_exists", "true")),
        ("line_crop_rows", sum_int(rows, "line_crop_rows")),
        ("line_crop_images_found", sum_int(rows, "line_crop_images_found")),
        ("ocr_words", sum_int(rows, "ocr_word_count")),
        ("ocr_hebrew_letters", sum_int(rows, "ocr_hebrew_letters")),
        ("source_row_imports", 0),
        ("city_name_normalization", 0),
        ("els_runs", 0),
        ("compactness_runs", 0),
        ("p_levels", 0),
    ]
    for priority in priority_contact.PRIORITY_ORDER:
        row = next((item for item in rows if item.get("review_priority") == priority), None)
        summary.append((priority, safe_int(row.get("line_crop_rows")) if row else 0))
        summary.append((f"{priority}_sheet_rows", priorities.get(priority, 0)))
    summary.append(("local_html_boundary", LOCAL_HTML_BOUNDARY))
    summary.append(("priority_contact_boundary", priority_contact.NO_INPUT_BOUNDARY))
    return [{"metric": metric, "value": str(value)} for metric, value in summary]


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    summary = {row["metric"]: row["value"] for row in summary_rows}
    lines = [
        "# Cities Source Page Line Crop Priority Review HTML",
        "",
        "Status: local ignored HTML review aid for Cities source-page line-crop triage priorities.",
        "The HTML file displays priority contact-sheet images only and embeds no OCR text or source-script text.",
        "Tracked files contain no OCR body text or source-script body text.",
        LOCAL_HTML_BOUNDARY,
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_page_line_crop_priority_review_html "
            f"--priority-contact {args.priority_contact} "
            f"--html-out {args.html_out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- HTML priority review aid: `{summary['html_path']}`.",
        f"- HTML rows: {summary['html_rows']}.",
        f"- HTML embeds source text: `{summary['html_embeds_source_text']}`.",
        f"- HTML priority image rows: {summary['html_priority_image_rows']}.",
        f"- Priority contact-sheet rows: {summary['priority_contact_sheet_rows']}.",
        f"- Priority contact sheets available: {summary['priority_contact_sheets_available']}.",
        f"- Line crop rows: {summary['line_crop_rows']}.",
        f"- Line crop images found: {summary['line_crop_images_found']}.",
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
        f"- Boundary: {LOCAL_HTML_BOUNDARY}",
        "",
        "## Priority Counts",
        "",
        "| Priority | Line crops | Sheet rows |",
        "| --- | ---: | ---: |",
    ]
    for priority in priority_contact.PRIORITY_ORDER:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{markdown_cell(priority)}`",
                    summary[priority],
                    summary[f"{priority}_sheet_rows"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- The ignored HTML file displays priority contact-sheet images only.",
            "- The priority view is not transcription and does not decide row admissibility.",
            "- Future source-row import still requires readable transcription, row/column alignment evidence, and an explicit import decision record.",
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
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {"priority_contact": str(args.priority_contact)},
        "outputs": {
            "html": str(args.html_out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(rows),
        "summary": {row["metric"]: row["value"] for row in summary_rows},
        "local_html_boundary": LOCAL_HTML_BOUNDARY,
        "priority_contact_boundary": priority_contact.NO_INPUT_BOUNDARY,
        "source_row_imports": 0,
        "city_name_normalization": 0,
        "els_runs": 0,
        "compactness_runs": 0,
        "p_levels": 0,
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


def rel_href(html_path: Path, target: Path) -> str:
    try:
        return str(target.relative_to(html_path.parent))
    except ValueError:
        return str(target)


def count_value(rows: list[dict[str, str]], key: str, value: str) -> int:
    return sum(1 for row in rows if row.get(key) == value)


def sum_int(rows: list[dict[str, str]], key: str) -> int:
    return sum(safe_int(row.get(key, "0")) for row in rows)


def safe_int(value: str | None) -> int:
    try:
        return int(value or 0)
    except ValueError:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
