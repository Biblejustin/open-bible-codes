#!/usr/bin/env python3
"""Audit Torah-code.org Cities source-chain files without running ELS results."""

from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import re
import subprocess
import time
from collections import Counter
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path

from els import __version__


DEFAULT_HTML_GLOB = "reports/wrr_1994/torah_code_experiment_cities*.html"
DEFAULT_PDF_GLOB = "reports/wrr_1994/torah_code_experiment_cities*.pdf"
DEFAULT_OUT = Path("reports/wrr_1994/cities_source_chain_files.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/cities_source_chain_summary.csv")
DEFAULT_ANCHORS_OUT = Path("reports/wrr_1994/cities_source_chain_anchors.csv")
DEFAULT_MD = Path("docs/CITIES_SOURCE_CHAIN_AUDIT.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/cities_source_chain_audit.manifest.json")

FILE_FIELDNAMES = [
    "path",
    "extension",
    "detected_kind",
    "status",
    "bytes",
    "sha256",
    "pdf_pages",
    "text_chars",
    "title",
    "link_count",
    "pdf_link_count",
]
SUMMARY_FIELDNAMES = [
    "source_files",
    "html_files",
    "pdf_named_files",
    "pdf_header_files",
    "pdfinfo_success_files",
    "pdf_text_extractable_files",
    "html_wrapper_pdf_files",
    "pdf_parse_error_files",
    "empty_text_pdf_files",
    "html_links",
    "html_pdf_links",
    "claim_status",
]
ANCHOR_FIELDNAMES = ["source", "anchor", "status", "diagnostic"]


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.links: list[str] = []
        self.title_parts: list[str] = []
        self.in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "title":
            self.in_title = True
        if tag.lower() == "a":
            for name, value in attrs:
                if name.lower() == "href" and value:
                    self.links.append(value)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        stripped = data.strip()
        if not stripped:
            return
        if self.in_title:
            self.title_parts.append(stripped)
        self.parts.append(stripped)

    @property
    def text(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.parts))

    @property
    def title(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.title_parts))


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    source_globs = args.source_glob or [DEFAULT_HTML_GLOB, DEFAULT_PDF_GLOB]
    args.source_glob = source_globs
    paths = sorted({Path(path) for pattern in source_globs for path in glob.glob(pattern)})
    rows = [analyze_file(path) for path in paths]
    summary = build_summary(rows)
    anchors = protocol_anchors(rows)
    write_csv(args.out, FILE_FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_csv(args.anchors_out, ANCHOR_FIELDNAMES, anchors)
    write_markdown(args.markdown_out, summary, anchors)
    write_manifest(args.manifest_out, args, summary, anchors, len(rows), started)
    print(args.out)
    print(args.summary_out)
    print(args.anchors_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-glob",
        action="append",
        default=[],
        help="Glob for source-chain files. Repeatable.",
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--anchors-out", type=Path, default=DEFAULT_ANCHORS_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def analyze_file(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    extension = path.suffix.lower().lstrip(".")
    detected_kind = detect_kind(raw)
    title = ""
    link_count = 0
    pdf_link_count = 0
    pdf_pages = ""
    text_chars = 0
    status = detected_kind
    if detected_kind == "html":
        html = raw.decode("utf-8", errors="replace")
        extractor = TextExtractor()
        extractor.feed(html)
        title = extractor.title
        link_count = len(extractor.links)
        pdf_link_count = sum(1 for link in extractor.links if ".pdf" in link.lower())
        text_chars = len(extractor.text)
        if extension == "pdf":
            status = "html_wrapper_saved_as_pdf"
    elif detected_kind == "pdf":
        pdf_pages = pdfinfo_pages(path)
        pdf_text = pdftotext(path)
        text_chars = len(pdf_text.strip())
        if not pdf_pages:
            status = "pdf_parse_error"
        elif text_chars == 0:
            status = "pdf_no_extractable_text"
        else:
            status = "pdf_text_extractable"
    return {
        "path": str(path),
        "extension": extension,
        "detected_kind": detected_kind,
        "status": status,
        "bytes": len(raw),
        "sha256": sha256_bytes(raw),
        "pdf_pages": pdf_pages,
        "text_chars": text_chars,
        "title": title,
        "link_count": link_count,
        "pdf_link_count": pdf_link_count,
    }


def detect_kind(raw: bytes) -> str:
    stripped = raw.lstrip()
    if stripped.startswith(b"%PDF"):
        return "pdf"
    if stripped[:20].lower().startswith(b"<!doctype html") or stripped[:10].lower().startswith(
        b"<html"
    ):
        return "html"
    return "other"


def pdfinfo_pages(path: Path) -> str:
    try:
        completed = subprocess.run(
            ["pdfinfo", str(path)],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return ""
    if completed.returncode != 0:
        return ""
    for line in completed.stdout.splitlines():
        if line.startswith("Pages:"):
            return line.split(":", 1)[1].strip()
    return ""


def pdftotext(path: Path) -> str:
    try:
        completed = subprocess.run(
            ["pdftotext", "-layout", str(path), "-"],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return ""
    if completed.returncode != 0:
        return ""
    return completed.stdout


def build_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "source_files": len(rows),
        "html_files": sum(1 for row in rows if row["detected_kind"] == "html"),
        "pdf_named_files": sum(1 for row in rows if row["extension"] == "pdf"),
        "pdf_header_files": sum(1 for row in rows if row["detected_kind"] == "pdf"),
        "pdfinfo_success_files": sum(1 for row in rows if row["pdf_pages"]),
        "pdf_text_extractable_files": sum(1 for row in rows if row["status"] == "pdf_text_extractable"),
        "html_wrapper_pdf_files": sum(
            1 for row in rows if row["status"] == "html_wrapper_saved_as_pdf"
        ),
        "pdf_parse_error_files": sum(1 for row in rows if row["status"] == "pdf_parse_error"),
        "empty_text_pdf_files": sum(1 for row in rows if row["status"] == "pdf_no_extractable_text"),
        "html_links": sum(int(row["link_count"]) for row in rows),
        "html_pdf_links": sum(int(row["pdf_link_count"]) for row in rows),
        "claim_status": "source_shape_only_not_result_bearing",
    }


def protocol_anchors(rows: list[dict[str, object]]) -> list[dict[str, str]]:
    text_by_path = html_text_by_path(rows)
    all_html = " ".join(text_by_path.values())
    checks = [
        (
            "cities_main",
            "gans_original_p_level_6_of_1000000",
            "6/1,000,000" in all_html,
            "main page reports original Gans p-level",
        ),
        (
            "gans_page",
            "gans_revised_p_level_4_of_1000000",
            "4/1,000,000" in all_html,
            "Gans communities page reports revised p-level",
        ),
        (
            "aumann_page",
            "aumann_non_significant_result",
            "non-significant" in all_html,
            "Aumann page reports non-significant experiments",
        ),
        (
            "simon_mckay_page",
            "simon_city_count_330",
            "330" in all_html,
            "Simon/McKay page reports 330 Margolioth city names",
        ),
        (
            "simon_mckay_page",
            "simon_used_count_197",
            "197" in all_html,
            "Simon/McKay page reports 197 used city names found in Margolioth",
        ),
        (
            "simon_mckay_page",
            "simon_length_filter_5_8",
            "between 5 and 8 letters" in all_html,
            "Simon/McKay page reports 5..8 city-name length filter",
        ),
        (
            "downloaded_files",
            "html_wrappers_present",
            any(row["status"] == "html_wrapper_saved_as_pdf" for row in rows),
            "some downloaded .pdf files are HTML wrappers",
        ),
    ]
    return [
        {
            "source": source,
            "anchor": anchor,
            "status": "found" if found else "missing",
            "diagnostic": diagnostic if found else "anchor text not found",
        }
        for source, anchor, found, diagnostic in checks
    ]


def html_text_by_path(rows: list[dict[str, object]]) -> dict[str, str]:
    texts: dict[str, str] = {}
    for row in rows:
        path = Path(str(row["path"]))
        if row["detected_kind"] != "html":
            continue
        html = path.read_text(encoding="utf-8", errors="replace")
        extractor = TextExtractor()
        extractor.feed(html)
        texts[str(path)] = extractor.text
    return texts


def write_markdown(
    path: Path,
    summary: dict[str, object],
    anchors: list[dict[str, str]],
) -> None:
    anchor_counts = Counter(anchor["status"] for anchor in anchors)
    lines = [
        "# Cities Source Chain Audit",
        "",
        "Status: source-shape audit only. This is not an ELS result, not a",
        "statistical test, and not a claim-ready replication.",
        "",
        "## Parsed Shape",
        "",
        "| Item | Count |",
        "| --- | ---: |",
        f"| source files scanned | {summary['source_files']} |",
        f"| HTML files | {summary['html_files']} |",
        f"| `.pdf` named files | {summary['pdf_named_files']} |",
        f"| PDF-header files | {summary['pdf_header_files']} |",
        f"| PDF files with `pdfinfo` pages | {summary['pdfinfo_success_files']} |",
        f"| PDF files with extractable text | {summary['pdf_text_extractable_files']} |",
        f"| `.pdf` files that are HTML wrappers | {summary['html_wrapper_pdf_files']} |",
        f"| PDF-header files with parse errors | {summary['pdf_parse_error_files']} |",
        f"| PDF files with no extracted text | {summary['empty_text_pdf_files']} |",
        f"| HTML links | {summary['html_links']} |",
        f"| HTML PDF links | {summary['html_pdf_links']} |",
        "",
        "## Protocol Anchors",
        "",
        f"Found anchors: {anchor_counts.get('found', 0)} of {len(anchors)}.",
        "",
        "| Source | Anchor | Status | Diagnostic |",
        "| --- | --- | --- | --- |",
    ]
    for anchor in anchors:
        lines.append(
            f"| {anchor['source']} | `{anchor['anchor']}` | {anchor['status']} | {anchor['diagnostic']} |"
        )
    lines.extend(
        [
            "",
            "## Use Boundary",
            "",
            "This audit records which Cities source-chain files are actually usable local",
            "sources. Several downloaded files with `.pdf` names are Wayback/HTML wrapper",
            "pages, not PDFs. Those files must not be treated as source data unless the",
            "underlying PDFs are recovered and checksummed.",
            "",
            "No city-name rows are normalized, no ELS search is run, and no p-level is",
            "verified here.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary: dict[str, object],
    anchors: list[dict[str, str]],
    rows: int,
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "source_globs": args.source_glob,
        "summary": summary,
        "anchor_status_counts": dict(Counter(anchor["status"] for anchor in anchors)),
        "rows": rows,
        "outputs": {
            "files": str(args.out),
            "summary": str(args.summary_out),
            "anchors": str(args.anchors_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "claim_boundary": "source-shape audit only; no ELS result",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
