#!/usr/bin/env python3
"""Build ignored local HTML for WRR source-row crop review."""

from __future__ import annotations

import argparse
import csv
import html
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from scripts import build_wrr_source_row_crop_packet as crop_packet


DEFAULT_CROP_PACKET = crop_packet.DEFAULT_OUT
DEFAULT_HTML = Path("reports/wrr_1994/wrr_source_row_crop_review.html")
DEFAULT_SUMMARY = Path("reports/wrr_1994/wrr_source_row_crop_review_html_summary.csv")
DEFAULT_MD = Path("docs/WRR_SOURCE_ROW_CROP_REVIEW_HTML.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/wrr_source_row_crop_review_html.manifest.json")

LOCAL_HTML_BOUNDARY = (
    "Local ignored WRR source-row crop HTML review aid; HTML displays row-crop "
    "images only, tracked files contain no OCR body text or source-script body "
    "text, no row transcription, no source correction, no pair exclusion, no "
    "method change"
)

SUMMARY_FIELDNAMES = ["metric", "value"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    fieldnames, rows = read_csv(args.crop_packet)
    html_summary = write_crop_review_html(rows, args)
    summary_rows = build_summary_rows(fieldnames, rows, html_summary)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, rows, summary_rows, args)
    write_manifest(args.manifest_out, args, rows, summary_rows, started)
    print(args.html_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--crop-packet", type=Path, default=DEFAULT_CROP_PACKET)
    parser.add_argument("--html-out", type=Path, default=DEFAULT_HTML)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def write_crop_review_html(
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> dict[str, object]:
    body = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        "<title>WRR Source Row Crop Review</title>",
        "<style>",
        "body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;margin:24px;background:#f8f8f6;color:#181818;max-width:1320px}",
        "h1{font-size:24px;margin:0 0 8px}",
        ".notice{max-width:1040px;margin-bottom:18px;line-height:1.45}",
        ".row{margin:0 0 22px;padding:16px;background:white;border:1px solid #ccc}",
        ".row h2{font-size:18px;margin:0 0 10px}",
        ".meta{font-size:12px;line-height:1.35;margin-bottom:8px;color:#333}",
        ".badge{display:inline-block;border:1px solid #888;padding:1px 5px;margin-right:4px;background:#f1f1ee}",
        "img{max-width:100%;height:auto;border:1px solid #ddd;background:white}",
        "code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}",
        "@media(max-width:700px){body{margin:12px}.row{padding:10px}}",
        "</style>",
        "</head>",
        "<body>",
        "<h1>WRR Source Row Crop Review</h1>",
        '<div class="notice">',
        "<p>Local ignored review aid. Inspect crop images before any row transcription, source correction, pair exclusion, or method change.</p>",
        "<p>This file displays row-crop images only. It does not embed OCR text or source-script text.</p>",
        f"<p><code>{html.escape(LOCAL_HTML_BOUNDARY)}</code></p>",
        "</div>",
    ]
    image_rows = 0
    for row in sorted(rows, key=lambda item: safe_int(item.get("row_rank", "0"))):
        crop_path = Path(row.get("crop_path", ""))
        if crop_path.exists():
            image_rows += 1
        body.extend(
            [
                '<article class="row">',
                (
                    f"<h2>Rank <code>{html.escape(row.get('row_rank', ''))}</code> "
                    f"<span class=\"badge\">row <code>{html.escape(row.get('row_number', ''))}</code></span></h2>"
                ),
                '<div class="meta">',
                f"Run: <code>{html.escape(row.get('run_label', ''))}</code> | ",
                f"Concept: <code>{html.escape(row.get('concept', ''))}</code> | ",
                f"Action terms: <code>{html.escape(row.get('action_terms', ''))}</code> | ",
                f"Frontier pairs: <code>{html.escape(row.get('frontier_pairs', ''))}</code><br>",
                f"Crop: <code>{html.escape(str(crop_path))}</code> | ",
                f"Manual crop count: <code>{html.escape(row.get('manual_crop_count', ''))}</code>",
                "</div>",
                f'<img src="{html.escape(rel_href(args.html_out, crop_path))}" alt="WRR source row {html.escape(row.get("row_number", ""))} crop">',
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
        "html_crop_image_rows": image_rows,
    }


def build_summary_rows(
    crop_fieldnames: list[str],
    rows: list[dict[str, str]],
    html_summary: dict[str, object],
) -> list[dict[str, str]]:
    summary: list[tuple[str, str | int]] = [
        ("crop_packet_fieldnames_match", str(crop_fieldnames == crop_packet.FIELDNAMES).lower()),
        ("html_rows", html_summary["html_rows"]),
        ("html_exists", str(html_summary["html_exists"]).lower()),
        ("html_path", html_summary["html_path"]),
        ("html_embeds_source_text", "false"),
        ("html_crop_image_rows", html_summary["html_crop_image_rows"]),
        ("source_row_crop_rows", len(rows)),
        ("auto_crops_available", count_value(rows, "crop_exists", "true")),
        ("manual_crop_rows", sum(1 for row in rows if safe_int(row.get("manual_crop_count")) > 0)),
        ("action_terms", sum_int(rows, "action_terms")),
        ("frontier_pairs", sum_int(rows, "frontier_pairs")),
        ("row_transcriptions", 0),
        ("source_corrections", 0),
        ("pair_exclusions", 0),
        ("method_changes", 0),
        ("local_html_boundary", LOCAL_HTML_BOUNDARY),
        ("crop_packet_boundary", crop_packet.NO_INPUT_BOUNDARY),
    ]
    return [{"metric": metric, "value": str(value)} for metric, value in summary]


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> None:
    summary = {row["metric"]: row["value"] for row in summary_rows}
    lines = [
        "# WRR Source Row Crop Review HTML",
        "",
        "Status: local ignored HTML review aid for WRR source-row crops.",
        "The HTML file displays source-row crop images only and embeds no OCR text or source-script text.",
        "Tracked files contain no OCR body text or source-script body text.",
        LOCAL_HTML_BOUNDARY,
        "",
        "Reproduce:",
        "",
        "```bash",
        (
            "python3 -m scripts.build_wrr_source_row_crop_review_html "
            f"--crop-packet {args.crop_packet} "
            f"--html-out {args.html_out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Current Read",
        "",
        f"- HTML crop review aid: `{summary['html_path']}`.",
        f"- HTML rows: {summary['html_rows']}.",
        f"- HTML embeds source text: `{summary['html_embeds_source_text']}`.",
        f"- HTML crop image rows: {summary['html_crop_image_rows']}.",
        f"- Source-row crop rows: {summary['source_row_crop_rows']}.",
        f"- Auto crops available: {summary['auto_crops_available']}.",
        f"- Manual crop rows: {summary['manual_crop_rows']}.",
        f"- Action terms: {summary['action_terms']}.",
        f"- Frontier pairs: {summary['frontier_pairs']}.",
        "- Row transcriptions: 0.",
        "- Source corrections: 0.",
        "- Pair exclusions: 0.",
        "- Method changes: 0.",
        f"- Boundary: {LOCAL_HTML_BOUNDARY}",
        "",
        "## Row Crops",
        "",
        "| Rank | Row | Terms | Frontier | Auto crop |",
        "| ---: | --- | ---: | ---: | --- |",
    ]
    for row in sorted(rows, key=lambda item: safe_int(item.get("row_rank", "0"))):
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row.get("row_rank", "")),
                    f"`{markdown_cell(row.get('row_number', ''))}`",
                    markdown_cell(row.get("action_terms", "")),
                    markdown_cell(row.get("frontier_pairs", "")),
                    f"`{markdown_cell(row.get('crop_path', ''))}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- The ignored HTML file displays generated row-crop images only.",
            "- The crop view is not transcription and does not decide source-row admissibility.",
            "- Future source changes still require readable transcription, row/column alignment evidence, and an explicit decision record.",
            "- No row here changes the working WRR source, excludes a pair, changes method rules, or locks replacement spellings.",
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
        "inputs": {"crop_packet": str(args.crop_packet)},
        "outputs": {
            "html": str(args.html_out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(rows),
        "summary": {row["metric"]: row["value"] for row in summary_rows},
        "local_html_boundary": LOCAL_HTML_BOUNDARY,
        "crop_packet_boundary": crop_packet.NO_INPUT_BOUNDARY,
        "row_transcriptions": 0,
        "source_corrections": 0,
        "pair_exclusions": 0,
        "method_changes": 0,
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


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


if __name__ == "__main__":
    raise SystemExit(main())
