#!/usr/bin/env python3
"""Build ignored local HTML for Cities source-page OCR/image review."""

from __future__ import annotations

import argparse
import csv
import html
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts.build_cities_source_page_ocr_review_packet import (
    DEFAULT_OUT as DEFAULT_PACKET,
    NO_INPUT_BOUNDARY,
)
from scripts.build_cities_unreadable_pdf_ocr_feasibility import markdown_cell


DEFAULT_HTML = Path(
    "reports/cities_pdf_recovery_probe/source_page_ocr_review/source_page_ocr_review.html"
)
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_ocr_review_html_summary.csv"
)
DEFAULT_MD = Path("docs/CITIES_SOURCE_PAGE_OCR_REVIEW_HTML.md")
DEFAULT_MANIFEST = Path(
    "reports/cities_pdf_recovery_probe/cities_source_page_ocr_review_html.manifest.json"
)

LOCAL_HTML_BOUNDARY = (
    "Local ignored HTML review aid; HTML embeds OCR sidecar text for manual "
    "comparison, tracked files contain no OCR body text or source-script body "
    "text, no source-row import, no city normalization, no ELS, no compactness, "
    "no p-level"
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
    body = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        "<title>Cities Source Page OCR Review</title>",
        "<style>",
        "body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;margin:24px;background:#f8f8f6;color:#181818}",
        "h1{font-size:24px;margin:0 0 8px}",
        ".notice{max-width:980px;margin-bottom:18px;line-height:1.45}",
        ".page{display:grid;grid-template-columns:minmax(360px,1fr) minmax(360px,1fr);gap:18px;margin:0 0 28px;padding:16px;background:white;border:1px solid #ccc}",
        ".meta{grid-column:1 / -1;font-size:14px;line-height:1.4}",
        "img{width:100%;height:auto;border:1px solid #bbb;background:white}",
        "pre{margin:0;padding:14px;border:1px solid #bbb;background:#fbfbfb;white-space:pre-wrap;line-height:1.45;direction:rtl;text-align:right;font-size:16px}",
        "code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}",
        "@media(max-width:900px){.page{grid-template-columns:1fr}}",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Cities Source Page OCR Review</h1>",
        '<div class="notice">',
        "<p>Local ignored review aid. Compare page image against OCR text before any transcription or source-row import.</p>",
        f"<p><code>{html.escape(LOCAL_HTML_BOUNDARY)}</code></p>",
        "</div>",
    ]
    embedded_rows = 0
    for row in rows:
        image_path = Path(row.get("page_image_path", ""))
        ocr_path = Path(row.get("ocr_text_path", ""))
        ocr_text = ocr_path.read_text(encoding="utf-8") if ocr_path.exists() else ""
        if ocr_text.strip():
            embedded_rows += 1
        body.extend(
            [
                '<section class="page">',
                '<div class="meta">',
                f"<strong>{html.escape(row.get('ocr_rank', ''))}. {html.escape(row.get('transcription_decision_id', ''))}</strong><br>",
                f"Label: <code>{html.escape(row.get('label', ''))}</code> | Page: <code>{html.escape(row.get('page_number', ''))}</code> | Class: <code>{html.escape(row.get('page_class', ''))}</code><br>",
                f"Status: <code>{html.escape(row.get('ocr_status', ''))}</code> | OCR sidecar: <code>{html.escape(str(ocr_path))}</code>",
                "</div>",
                f'<img src="{html.escape(rel_href(args.html_out, image_path))}" alt="{html.escape(row.get("transcription_decision_id", ""))} page image">',
                f"<pre>{html.escape(ocr_text)}</pre>",
                "</section>",
            ]
        )
    body.extend(["</body>", "</html>"])
    args.html_out.parent.mkdir(parents=True, exist_ok=True)
    args.html_out.write_text("\n".join(body) + "\n", encoding="utf-8")
    return {
        "html_exists": args.html_out.exists(),
        "html_path": str(args.html_out),
        "html_rows": len(rows),
        "html_embedded_ocr_text_rows": embedded_rows,
    }


def build_summary_rows(
    rows: list[dict[str, str]],
    html_summary: dict[str, object],
) -> list[dict[str, str]]:
    return [
        metric("html_rows", html_summary["html_rows"]),
        metric("html_exists", str(html_summary["html_exists"]).lower()),
        metric("html_path", html_summary["html_path"]),
        metric("html_embeds_ocr_text", "true"),
        metric("html_embedded_ocr_text_rows", html_summary["html_embedded_ocr_text_rows"]),
        metric("page_images_found", count_value(rows, "page_image_exists", "true")),
        metric("ocr_text_sidecars", count_value(rows, "ocr_text_exists", "true")),
        metric("pages_with_ocr_text", count_value(rows, "ocr_status", "source_page_ocr_text_detected")),
        metric("ocr_hebrew_letters", sum_int(rows, "ocr_hebrew_letters")),
        metric("ocr_words", sum_int(rows, "ocr_word_count")),
        metric("ocr_lines", sum_int(rows, "ocr_line_count")),
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
    lines = [
        "# Cities Source Page OCR Review HTML",
        "",
        "Status: local ignored HTML review aid for locked Cities source-page OCR.",
        "The HTML file embeds OCR sidecar text so image/text comparison can happen locally.",
        "Tracked files contain no OCR body text or source-script body text.",
        "This does not import source rows, normalize city names, run ELS searches, compute compactness, or verify p-levels.",
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_cities_source_page_ocr_review_html "
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
        f"- HTML embeds OCR text: `{summary['html_embeds_ocr_text']}`.",
        f"- HTML embedded OCR text rows: {summary['html_embedded_ocr_text_rows']}.",
        f"- Page images found: {summary['page_images_found']}.",
        f"- OCR text sidecars: {summary['ocr_text_sidecars']}.",
        f"- Pages with OCR text: {summary['pages_with_ocr_text']}.",
        f"- OCR Hebrew letters: {summary['ocr_hebrew_letters']}.",
        f"- OCR words: {summary['ocr_words']}.",
        f"- OCR lines: {summary['ocr_lines']}.",
        f"- Source-row imports: {summary['source_row_imports']}.",
        f"- City-name normalization: {summary['city_name_normalization']}.",
        f"- ELS runs: {summary['els_runs']}.",
        f"- Compactness runs: {summary['compactness_runs']}.",
        f"- p-levels: {summary['p_levels']}.",
        f"- Boundary: {LOCAL_HTML_BOUNDARY}",
        "",
        "## Page Order",
        "",
        "| Rank | Transcription id | Label | Page | Class | Status |",
        "| ---: | --- | --- | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["ocr_rank"]),
                    f"`{markdown_cell(row['transcription_decision_id'])}`",
                    markdown_cell(row["label"]),
                    markdown_cell(row["page_number"]),
                    f"`{markdown_cell(row['page_class'])}`",
                    f"`{markdown_cell(row['ocr_status'])}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- The ignored HTML file may display OCR text; tracked files do not.",
            "- OCR text is a review aid, not verified transcription.",
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


def metric(name: str, value: object) -> dict[str, str]:
    return {"metric": name, "value": str(value)}


if __name__ == "__main__":
    raise SystemExit(main())
