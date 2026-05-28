#!/usr/bin/env python3
"""Build ignored local HTML for Cities line-crop triage review."""

from __future__ import annotations

import argparse
import csv
import html
import json
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.build_cities_source_page_line_crop_triage import (
    CLAIM_BOUNDARY,
    DEFAULT_OUT as DEFAULT_TRIAGE,
    FIELDNAMES as TRIAGE_FIELDNAMES,
)
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell


DEFAULT_HTML = Path(
    "reports/cities_pdf_recovery_probe/source_page_line_crops/line_crop_triage.html"
)
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_triage_html_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_PAGE_LINE_CROP_TRIAGE_HTML.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_line_crop_triage_html.manifest.json"
)

LOCAL_HTML_BOUNDARY = (
    "Local ignored HTML triage aid; HTML displays line-crop images in priority "
    "order only, tracked files contain no OCR body text or source-script body "
    "text, no verified transcription, no source-row import, no city "
    "normalization, no ELS, no compactness, no p-level"
)

SUMMARY_FIELDNAMES = ["metric", "value"]
PRIORITY_ORDER = [
    "priority_1_dense_text",
    "priority_2_medium_text",
    "priority_3_short_text",
    "priority_4_no_text",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    fieldnames, triage_rows = read_csv(args.triage)
    html_summary = write_triage_html(triage_rows, args)
    summary_rows = build_summary_rows(fieldnames, triage_rows, html_summary)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, triage_rows, summary_rows, args)
    write_manifest(args.manifest_out, args, triage_rows, summary_rows, started)
    print(args.html_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--triage", type=Path, default=DEFAULT_TRIAGE)
    parser.add_argument("--html-out", type=Path, default=DEFAULT_HTML)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def write_triage_html(
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> dict[str, object]:
    priority_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in sorted(rows, key=lambda r: to_int(r.get("triage_rank"))):
        priority_rows[row.get("review_priority", "")].append(row)
    body = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        "<title>Cities Source Page Line Crop Triage</title>",
        "<style>",
        "body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;margin:24px;background:#f8f8f6;color:#181818}",
        "h1{font-size:24px;margin:0 0 8px}",
        ".notice{max-width:980px;margin-bottom:18px;line-height:1.45}",
        ".priority{margin:0 0 30px;padding:16px;background:white;border:1px solid #ccc}",
        ".priority h2{font-size:18px;margin:0 0 12px}",
        ".grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:12px}",
        ".line-crop{border:1px solid #bbb;background:#fff;padding:8px}",
        ".meta{font-size:12px;line-height:1.35;margin-bottom:6px;color:#333}",
        ".badge{display:inline-block;border:1px solid #888;padding:1px 5px;margin-right:4px;background:#f1f1ee}",
        "img{width:100%;height:auto;border:1px solid #ddd;background:white}",
        "code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}",
        "@media(max-width:700px){.grid{grid-template-columns:1fr}body{margin:12px}}",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Cities Source Page Line Crop Triage</h1>",
        '<div class="notice">',
        "<p>Local ignored triage aid. Review crop images in priority order before any transcription or source-row import.</p>",
        "<p>This file displays crop images only. It does not embed OCR text or source-script text.</p>",
        f"<p><code>{html.escape(LOCAL_HTML_BOUNDARY)}</code></p>",
        "</div>",
    ]
    embedded_rows = 0
    section_count = 0
    for priority in PRIORITY_ORDER:
        rows_for_priority = priority_rows.get(priority, [])
        section_count += 1
        body.extend(
            [
                '<section class="priority">',
                f"<h2>{html.escape(priority)} ({len(rows_for_priority)} line crops)</h2>",
                '<div class="grid">',
            ]
        )
        for row in rows_for_priority:
            crop_path = Path(row.get("crop_path", ""))
            if crop_path.exists():
                embedded_rows += 1
            body.extend(
                [
                    '<article class="line-crop">',
                    '<div class="meta">',
                    f'<span class="badge">triage <code>{html.escape(row.get("triage_rank", ""))}</code></span>',
                    f'<span class="badge">source <code>{html.escape(row.get("source_order", ""))}</code></span>',
                    f'<span class="badge">{html.escape(row.get("review_bucket", ""))}</span><br>',
                    f"Page: <code>{html.escape(row.get('page_number', ''))}</code> | ",
                    f"Page line: <code>{html.escape(row.get('page_line_rank', ''))}</code> | ",
                    f"Decision: <code>{html.escape(row.get('transcription_decision_id', ''))}</code><br>",
                    f"Words: <code>{html.escape(row.get('ocr_word_count', ''))}</code> | ",
                    f"Letters: <code>{html.escape(row.get('ocr_hebrew_letters', ''))}</code> | ",
                    f"Crop: <code>{html.escape(str(crop_path))}</code>",
                    "</div>",
                    f'<img src="{html.escape(rel_href(args.html_out, crop_path))}" alt="triage rank {html.escape(row.get("triage_rank", ""))}">',
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
        "html_priority_sections": section_count,
    }


def build_summary_rows(
    triage_fieldnames: list[str],
    rows: list[dict[str, str]],
    html_summary: dict[str, object],
) -> list[dict[str, str]]:
    priority_counts = Counter(row.get("review_priority", "") for row in rows)
    bucket_counts = Counter(row.get("review_bucket", "") for row in rows)
    page_counts = Counter(row.get("transcription_decision_id", "") for row in rows)
    summary: list[tuple[str, str | int]] = [
        ("triage_fieldnames_match", str(triage_fieldnames == TRIAGE_FIELDNAMES).lower()),
        ("html_rows", html_summary["html_rows"]),
        ("html_exists", str(html_summary["html_exists"]).lower()),
        ("html_path", html_summary["html_path"]),
        ("html_embeds_source_text", "false"),
        ("html_line_crop_image_rows", html_summary["html_line_crop_image_rows"]),
        ("html_priority_sections", html_summary["html_priority_sections"]),
        ("triage_rows", len(rows)),
        ("unique_table_pages", len(page_counts)),
        ("crop_images_available", count_value(rows, "crop_exists", "true")),
        ("ocr_words", sum_int(rows, "ocr_word_count")),
        ("ocr_hebrew_letters", sum_int(rows, "ocr_hebrew_letters")),
        ("source_row_imports", 0),
        ("city_name_normalization", 0),
        ("els_runs", 0),
        ("compactness_runs", 0),
        ("p_levels", 0),
    ]
    for priority in PRIORITY_ORDER:
        summary.append((priority, priority_counts.get(priority, 0)))
    for bucket in sorted(bucket_counts):
        summary.append((f"bucket_{bucket}", bucket_counts[bucket]))
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
        "# Cities Source Page Line Crop Triage HTML",
        "",
        "Status: local ignored HTML triage aid for Cities source-page line crops.",
        "The HTML file displays line-crop images in priority order and embeds no OCR text or source-script text.",
        "Tracked files contain no OCR body text or source-script body text.",
        CLAIM_BOUNDARY,
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_page_line_crop_triage_html "
            f"--triage {args.triage} "
            f"--html-out {args.html_out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- HTML triage aid: `{summary['html_path']}`.",
        f"- HTML rows: {summary['html_rows']}.",
        f"- HTML embeds source text: `{summary['html_embeds_source_text']}`.",
        f"- HTML line-crop image rows: {summary['html_line_crop_image_rows']}.",
        f"- HTML priority sections: {summary['html_priority_sections']}.",
        f"- Line-crop triage rows: {summary['triage_rows']}.",
        f"- Unique table pages: {summary['unique_table_pages']}.",
        f"- Crop images available: {summary['crop_images_available']}.",
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
        "## Page Counts",
        "",
        "| Transcription id | Triage rows |",
        "| --- | ---: |",
    ]
    for transcription_id in sorted(page_counts):
        lines.append(f"| `{markdown_cell(transcription_id)}` | {page_counts[transcription_id]} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- The ignored HTML file displays crop images in priority order only.",
            "- The priority order is not transcription and does not decide row admissibility.",
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
        "inputs": {"triage": str(args.triage)},
        "outputs": {
            "html": str(args.html_out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(rows),
        "summary": {row["metric"]: row["value"] for row in summary_rows},
        "claim_boundary": CLAIM_BOUNDARY,
        "local_html_boundary": LOCAL_HTML_BOUNDARY,
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
        return target.resolve().relative_to(html_path.parent.resolve()).as_posix()
    except ValueError:
        return str(target)


def to_int(value: str | None) -> int:
    try:
        return int(value or 0)
    except ValueError:
        return 0


def count_value(rows: list[dict[str, str]], key: str, value: str) -> int:
    return sum(1 for row in rows if row.get(key) == value)


def sum_int(rows: list[dict[str, str]], key: str) -> int:
    return sum(to_int(row.get(key)) for row in rows)


if __name__ == "__main__":
    raise SystemExit(main())
