#!/usr/bin/env python3
"""Build ignored local HTML for Cities line-crop band review."""

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
from scripts import build_cities_source_page_line_crop_band_contact_sheet as band_contact
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell


DEFAULT_BAND_CONTACT = band_contact.DEFAULT_OUT
DEFAULT_HTML = Path("reports/cities_pdf_recovery_probe/source_page_line_crops/band_review.html")
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_review_html_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_PAGE_LINE_CROP_BAND_REVIEW_HTML.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_band_review_html.manifest.json"
)

LOCAL_HTML_BOUNDARY = (
    "Local ignored band HTML review aid; HTML displays band contact-sheet images "
    "only, tracked files contain no OCR body text or source-script body text, "
    "no verified transcription, no source-row import, no city normalization, "
    "no ELS, no compactness, no p-level"
)

SUMMARY_FIELDNAMES = ["metric", "value"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    fieldnames, band_rows = read_csv(args.band_contact)
    html_summary = write_band_html(band_rows, args)
    summary_rows = build_summary_rows(fieldnames, band_rows, html_summary)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, band_rows, summary_rows, args)
    write_manifest(args.manifest_out, args, band_rows, summary_rows, started)
    print(args.html_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--band-contact", type=Path, default=DEFAULT_BAND_CONTACT)
    parser.add_argument("--html-out", type=Path, default=DEFAULT_HTML)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def write_band_html(
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> dict[str, object]:
    body = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        "<title>Cities Source Page Line Crop Band Review</title>",
        "<style>",
        "body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;margin:24px;background:#f8f8f6;color:#181818}",
        "h1{font-size:24px;margin:0 0 8px}",
        ".notice{max-width:980px;margin-bottom:18px;line-height:1.45}",
        ".band{margin:0 0 30px;padding:16px;background:white;border:1px solid #ccc}",
        ".band h2{font-size:18px;margin:0 0 12px}",
        ".meta{font-size:12px;line-height:1.35;margin-bottom:8px;color:#333}",
        ".badge{display:inline-block;border:1px solid #888;padding:1px 5px;margin-right:4px;background:#f1f1ee}",
        "img{max-width:100%;height:auto;border:1px solid #ddd;background:white}",
        "code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}",
        "body{max-width:1240px}",
        "@media(max-width:700px){body{margin:12px}.band{padding:10px}}",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Cities Source Page Line Crop Band Review</h1>",
        '<div class="notice">',
        "<p>Local ignored review aid. Compare band contact-sheet images against full page images before any transcription or source-row import.</p>",
        "<p>This file displays contact-sheet images only. It does not embed OCR text or source-script text.</p>",
        f"<p><code>{html.escape(LOCAL_HTML_BOUNDARY)}</code></p>",
        "</div>",
    ]
    embedded_rows = 0
    for row in sorted(rows, key=lambda item: safe_int(item.get("sheet_rank", "0"))):
        sheet_path = Path(row.get("contact_sheet_path", ""))
        if sheet_path.exists():
            embedded_rows += 1
        body.extend(
            [
                '<article class="band">',
                (
                    f"<h2>Band <code>{html.escape(row.get('sheet_rank', ''))}</code> "
                    f"({html.escape(row.get('line_crop_rows', ''))} line crops)</h2>"
                ),
                '<div class="meta">',
                f'<span class="badge"><code>{html.escape(row.get("band_review_id", ""))}</code></span>',
                f'<span class="badge"><code>{html.escape(row.get("transcription_decision_id", ""))}</code></span><br>',
                f"Page line range: <code>{html.escape(row.get('first_page_line_rank', ''))}-{html.escape(row.get('last_page_line_rank', ''))}</code> | ",
                f"Images: <code>{html.escape(row.get('line_crop_images_found', ''))}</code> | ",
                f"Words: <code>{html.escape(row.get('ocr_word_count', ''))}</code> | ",
                f"Letters: <code>{html.escape(row.get('ocr_hebrew_letters', ''))}</code><br>",
                f"Sheet: <code>{html.escape(str(sheet_path))}</code>",
                "</div>",
                f'<img src="{html.escape(rel_href(args.html_out, sheet_path))}" alt="band {html.escape(row.get("sheet_rank", ""))} contact sheet">',
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
        "html_band_image_rows": embedded_rows,
    }


def build_summary_rows(
    band_contact_fieldnames: list[str],
    rows: list[dict[str, str]],
    html_summary: dict[str, object],
) -> list[dict[str, str]]:
    page_counts = Counter(row.get("transcription_decision_id", "") for row in rows)
    summary: list[tuple[str, str | int]] = [
        ("band_contact_fieldnames_match", str(band_contact_fieldnames == band_contact.FIELDNAMES).lower()),
        ("html_rows", html_summary["html_rows"]),
        ("html_exists", str(html_summary["html_exists"]).lower()),
        ("html_path", html_summary["html_path"]),
        ("html_embeds_source_text", "false"),
        ("html_band_image_rows", html_summary["html_band_image_rows"]),
        ("band_contact_sheet_rows", len(rows)),
        ("band_contact_sheets_available", count_value(rows, "contact_sheet_exists", "true")),
        ("line_crop_rows", sum_int(rows, "line_crop_rows")),
        ("line_crop_images_found", sum_int(rows, "line_crop_images_found")),
        ("unique_table_pages", len(page_counts)),
        ("ocr_words", sum_int(rows, "ocr_word_count")),
        ("ocr_hebrew_letters", sum_int(rows, "ocr_hebrew_letters")),
        ("source_row_imports", 0),
        ("city_name_normalization", 0),
        ("els_runs", 0),
        ("compactness_runs", 0),
        ("p_levels", 0),
    ]
    for transcription_id in sorted(page_counts):
        summary.append((f"bands_{transcription_id}", page_counts[transcription_id]))
    summary.append(("local_html_boundary", LOCAL_HTML_BOUNDARY))
    summary.append(("contact_sheet_boundary", band_contact.NO_INPUT_BOUNDARY))
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
        "# Cities Source Page Line Crop Band Review HTML",
        "",
        "Status: local ignored HTML review aid for Cities source-page line-crop coordinate bands.",
        "The HTML file displays band contact-sheet images only and embeds no OCR text or source-script text.",
        "Tracked files contain no OCR body text or source-script body text.",
        LOCAL_HTML_BOUNDARY,
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_page_line_crop_band_review_html "
            f"--band-contact {args.band_contact} "
            f"--html-out {args.html_out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- HTML band review aid: `{summary['html_path']}`.",
        f"- HTML rows: {summary['html_rows']}.",
        f"- HTML embeds source text: `{summary['html_embeds_source_text']}`.",
        f"- HTML band image rows: {summary['html_band_image_rows']}.",
        f"- Band contact-sheet rows: {summary['band_contact_sheet_rows']}.",
        f"- Band contact sheets available: {summary['band_contact_sheets_available']}.",
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
        f"- Boundary: {LOCAL_HTML_BOUNDARY}",
        "",
        "## Page Counts",
        "",
        "| Transcription id | Band rows |",
        "| --- | ---: |",
    ]
    for transcription_id in sorted(page_counts):
        lines.append(f"| `{markdown_cell(transcription_id)}` | {page_counts[transcription_id]} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- The ignored HTML file displays band contact-sheet images only.",
            "- The band view is not transcription and does not decide row admissibility.",
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
        "inputs": {"band_contact": str(args.band_contact)},
        "outputs": {
            "html": str(args.html_out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(rows),
        "summary": {row["metric"]: row["value"] for row in summary_rows},
        "local_html_boundary": LOCAL_HTML_BOUNDARY,
        "contact_sheet_boundary": band_contact.NO_INPUT_BOUNDARY,
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
