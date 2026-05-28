#!/usr/bin/env python3
"""Build ignored local HTML for Cities source-page line-crop review."""

from __future__ import annotations

import argparse
import csv
import html
import json
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.build_cities_source_page_line_crop_packet import (
    DEFAULT_OUT as DEFAULT_PACKET,
    NO_INPUT_BOUNDARY,
)
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell


DEFAULT_HTML = Path("reports/cities_pdf_recovery_probe/source_page_line_crops/line_crop_review.html")
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_review_html_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_PAGE_LINE_CROP_REVIEW_HTML.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_review_html.manifest.json"
)

LOCAL_HTML_BOUNDARY = (
    "Local ignored HTML review aid; HTML displays line-crop images only, "
    "tracked files contain no OCR body text or source-script body text, no "
    "verified transcription, no source-row import, no city normalization, no "
    "ELS, no compactness, no p-level"
)

SUMMARY_FIELDNAMES = ["metric", "value"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    packet_rows = read_rows(args.packet)
    html_summary = write_review_html(packet_rows, args)
    summary_rows = build_summary_rows(packet_rows, html_summary)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, packet_rows, summary_rows, args)
    write_manifest(args.manifest_out, args, packet_rows, summary_rows, started)
    print(args.html_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--html-out", type=Path, default=DEFAULT_HTML)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def write_review_html(
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> dict[str, object]:
    page_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        page_rows[row.get("transcription_decision_id", "")].append(row)
    body = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        "<title>Cities Source Page Line Crop Review</title>",
        "<style>",
        "body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;margin:24px;background:#f8f8f6;color:#181818}",
        "h1{font-size:24px;margin:0 0 8px}",
        ".notice{max-width:980px;margin-bottom:18px;line-height:1.45}",
        ".page{margin:0 0 30px;padding:16px;background:white;border:1px solid #ccc}",
        ".page h2{font-size:18px;margin:0 0 12px}",
        ".grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:12px}",
        ".line-crop{border:1px solid #bbb;background:#fff;padding:8px}",
        ".meta{font-size:12px;line-height:1.35;margin-bottom:6px;color:#333}",
        "img{width:100%;height:auto;border:1px solid #ddd;background:white}",
        "code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}",
        "@media(max-width:700px){.grid{grid-template-columns:1fr}body{margin:12px}}",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Cities Source Page Line Crop Review</h1>",
        '<div class="notice">',
        "<p>Local ignored review aid. Compare crop images against full page images before any transcription or source-row import.</p>",
        "<p>This file displays crop images only. It does not embed OCR text or source-script text.</p>",
        f"<p><code>{html.escape(LOCAL_HTML_BOUNDARY)}</code></p>",
        "</div>",
    ]
    embedded_rows = 0
    for transcription_id in sorted(page_rows):
        rows_for_page = sorted(page_rows[transcription_id], key=line_rank_key)
        first = rows_for_page[0]
        body.extend(
            [
                '<section class="page">',
                (
                    f"<h2>{html.escape(transcription_id)} "
                    f"({len(rows_for_page)} line crops)</h2>"
                ),
                '<div class="grid">',
            ]
        )
        for row in rows_for_page:
            crop_path = Path(row.get("crop_path", ""))
            if crop_path.exists():
                embedded_rows += 1
            body.extend(
                [
                    '<article class="line-crop">',
                    '<div class="meta">',
                    f"Global line: <code>{html.escape(row.get('line_rank', ''))}</code> | ",
                    f"Page line: <code>{html.escape(row.get('page_line_rank', ''))}</code> | ",
                    f"Page: <code>{html.escape(first.get('page_number', ''))}</code><br>",
                    f"Words: <code>{html.escape(row.get('ocr_word_count', ''))}</code> | ",
                    f"Letters: <code>{html.escape(row.get('ocr_hebrew_letters', ''))}</code> | ",
                    f"Crop: <code>{html.escape(str(crop_path))}</code>",
                    "</div>",
                    f'<img src="{html.escape(rel_href(args.html_out, crop_path))}" alt="{html.escape(transcription_id)} line {html.escape(row.get("page_line_rank", ""))}">',
                    "</article>",
                ]
            )
        body.extend(["</div>", "</section>"])
    body.extend(["</body>", "</html>"])
    args.html_out.parent.mkdir(parents=True, exist_ok=True)
    args.html_out.write_text("\n".join(body) + "\n", encoding="utf-8")
    return {
        "html_exists": args.html_out.exists(),
        "html_path": str(args.html_out),
        "html_rows": len(rows),
        "html_line_crop_image_rows": embedded_rows,
        "html_pages": len(page_rows),
    }


def build_summary_rows(
    rows: list[dict[str, str]],
    html_summary: dict[str, object],
) -> list[dict[str, str]]:
    return [
        metric("html_rows", html_summary["html_rows"]),
        metric("html_exists", str(html_summary["html_exists"]).lower()),
        metric("html_path", html_summary["html_path"]),
        metric("html_embeds_source_text", "false"),
        metric("html_line_crop_image_rows", html_summary["html_line_crop_image_rows"]),
        metric("html_pages", html_summary["html_pages"]),
        metric("line_crop_packet_rows", len(rows)),
        metric("line_crop_images_found", count_value(rows, "crop_exists", "true")),
        metric("unique_table_pages", len({row.get("transcription_decision_id", "") for row in rows})),
        metric("ocr_words", sum_int(rows, "ocr_word_count")),
        metric("ocr_hebrew_letters", sum_int(rows, "ocr_hebrew_letters")),
        metric("source_row_imports", 0),
        metric("city_name_normalization", 0),
        metric("els_runs", 0),
        metric("compactness_runs", 0),
        metric("p_levels", 0),
        metric("tracked_no_input_boundary", NO_INPUT_BOUNDARY),
        metric("local_html_boundary", LOCAL_HTML_BOUNDARY),
    ]


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    summary = {row["metric"]: row["value"] for row in summary_rows}
    page_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        page_counts[row["transcription_decision_id"]] += 1
    lines = [
        "# Cities Source Page Line Crop Review HTML",
        "",
        "Status: local ignored HTML review aid for Cities source-page line crops.",
        "The HTML file displays line-crop images only and embeds no OCR text or source-script text.",
        "Tracked files contain no OCR body text or source-script body text.",
        "This does not verify a transcription, import source rows, normalize city names, run ELS searches, compute compactness, or verify p-levels.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_page_line_crop_review_html "
            f"--packet {args.packet} "
            f"--html-out {args.html_out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- HTML review aid: `{summary['html_path']}`.",
        f"- HTML rows: {summary['html_rows']}.",
        f"- HTML embeds source text: `{summary['html_embeds_source_text']}`.",
        f"- HTML line-crop image rows: {summary['html_line_crop_image_rows']}.",
        f"- HTML pages: {summary['html_pages']}.",
        f"- Line crop packet rows: {summary['line_crop_packet_rows']}.",
        f"- Line crop images found: {summary['line_crop_images_found']}.",
        f"- Unique table pages: {summary['unique_table_pages']}.",
        f"- OCR words represented by line boxes: {summary['ocr_words']}.",
        f"- OCR Hebrew letters represented by line boxes: {summary['ocr_hebrew_letters']}.",
        f"- Source-row imports: {summary['source_row_imports']}.",
        f"- City-name normalization: {summary['city_name_normalization']}.",
        f"- ELS runs: {summary['els_runs']}.",
        f"- Compactness runs: {summary['compactness_runs']}.",
        f"- p-levels: {summary['p_levels']}.",
        f"- Boundary: {LOCAL_HTML_BOUNDARY}",
        "",
        "## Page Counts",
        "",
        "| Transcription id | Line crops |",
        "| --- | ---: |",
    ]
    for transcription_id in sorted(page_counts):
        lines.append(
            f"| `{markdown_cell(transcription_id)}` | {page_counts[transcription_id]} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- The ignored HTML file displays line-crop images only; tracked files do not contain OCR body text or source-script body text.",
            "- Line crop images are review aids, not verified transcriptions.",
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
        "inputs": {"packet": str(args.packet)},
        "outputs": {
            "html": str(args.html_out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(rows),
        "summary": {row["metric"]: row["value"] for row in summary_rows},
        "tracked_no_input_boundary": NO_INPUT_BOUNDARY,
        "local_html_boundary": LOCAL_HTML_BOUNDARY,
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


def rel_href(from_path: Path, target: Path) -> str:
    try:
        return str(target.relative_to(from_path.parent))
    except ValueError:
        return str(target)


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


def line_rank_key(row: dict[str, str]) -> tuple[int, int]:
    return safe_int(row.get("page_line_rank", "0")), safe_int(row.get("line_rank", "0"))


def safe_int(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


def metric(name: str, value: object) -> dict[str, str]:
    return {"metric": name, "value": str(value)}


if __name__ == "__main__":
    raise SystemExit(main())
