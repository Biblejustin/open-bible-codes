#!/usr/bin/env python3
"""Audit Torah-code.org Israeli prime-ministers sources without running ELS results."""

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
from dataclasses import dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path

from els import __version__


DEFAULT_MAIN_HTML = Path("reports/wrr_1994/torah_code_experiment_israeli_prime_ministers.html")
DEFAULT_PDF = Path("reports/wrr_1994/torah_code_experiment_israeli_prime_ministers.pdf")
DEFAULT_PAGE_GLOB = "reports/wrr_1994/torah_code_experiment_israeli_prime_ministers_*.html"
DEFAULT_OUT = Path("reports/wrr_1994/israeli_prime_ministers_source_records.csv")
DEFAULT_PDF_KEYWORDS_OUT = Path("reports/wrr_1994/israeli_prime_ministers_pdf_keyword_rows.csv")
DEFAULT_DETAIL_PAGES_OUT = Path("reports/wrr_1994/israeli_prime_ministers_detail_pages.csv")
DEFAULT_SUMMARY_OUT = Path("reports/wrr_1994/israeli_prime_ministers_source_summary.csv")
DEFAULT_ANCHORS_OUT = Path("reports/wrr_1994/israeli_prime_ministers_protocol_anchors.csv")
DEFAULT_MD = Path("docs/ISRAELI_PRIME_MINISTERS_SOURCE_AUDIT.md")
DEFAULT_MANIFEST = Path("reports/wrr_1994/israeli_prime_ministers_source_audit.manifest.json")

PM_ROW_RE = re.compile(r"^\s*(\d+)\s+")
FIELDNAMES = [
    "record_index",
    "line_count",
    "hebrew_keyword_rows",
]
PDF_KEYWORD_FIELDNAMES = [
    "source_table",
    "record_index",
    "keyword_row_index",
    "english_label",
    "hebrew_keyword",
    "raw_line",
]
DETAIL_PAGE_FIELDNAMES = [
    "page_index",
    "path",
    "sha256",
    "bytes",
    "title",
    "keyword_text",
    "keyword_token_count",
    "has_previous",
    "has_next",
]
SUMMARY_FIELDNAMES = [
    "main_html",
    "main_sha256",
    "main_bytes",
    "pdf",
    "pdf_sha256",
    "pdf_bytes",
    "pdf_pages_from_text",
    "pdf_prime_minister_rows",
    "pdf_prime_minister_min",
    "pdf_prime_minister_max",
    "pdf_keyword_phrase_rows",
    "pdf_name_keyword_rows",
    "machine_pdf_keyword_rows",
    "html_detail_pages_found",
    "html_detail_pages_with_keywords",
    "machine_html_detail_rows",
    "html_detail_page_gap_against_pdf_rows",
    "claim_status",
]
ANCHOR_FIELDNAMES = ["source", "anchor", "status", "diagnostic"]


@dataclass(frozen=True)
class PrimeMinisterRecord:
    record_index: int
    lines: tuple[str, ...]

    @property
    def hebrew_keyword_rows(self) -> int:
        return sum(1 for line in self.lines if keyword_field(line))

    def as_row(self) -> dict[str, object]:
        return {
            "record_index": self.record_index,
            "line_count": len(self.lines),
            "hebrew_keyword_rows": self.hebrew_keyword_rows,
        }


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        stripped = data.strip()
        if stripped:
            self.parts.append(stripped)

    @property
    def text(self) -> str:
        return " ".join(self.parts)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    main_html = args.main_html.read_text(encoding="utf-8", errors="replace")
    pdf_text = extract_pdf_text(args.pdf)
    page_paths = [Path(path) for path in sorted(glob.glob(args.keyword_page_glob))]
    detail_pages = [parse_detail_page(path) for path in page_paths]
    records = parse_pdf_records(pdf_text)
    rows = [record.as_row() for record in records]
    pdf_keyword_rows = pdf_keyword_rows_from_source(pdf_text, records)
    detail_rows = detail_page_rows(detail_pages)
    summary = build_summary(
        args,
        main_html,
        pdf_text,
        records,
        detail_pages,
        pdf_keyword_rows,
        detail_rows,
    )
    anchors = protocol_anchors(main_html, pdf_text, detail_pages)
    write_csv(args.out, FIELDNAMES, rows)
    write_csv(args.pdf_keywords_out, PDF_KEYWORD_FIELDNAMES, pdf_keyword_rows)
    write_csv(args.detail_pages_out, DETAIL_PAGE_FIELDNAMES, detail_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_csv(args.anchors_out, ANCHOR_FIELDNAMES, anchors)
    write_markdown(args.markdown_out, summary, anchors)
    write_manifest(args.manifest_out, args, summary, anchors, len(rows), started)
    print(args.out)
    print(args.pdf_keywords_out)
    print(args.detail_pages_out)
    print(args.summary_out)
    print(args.anchors_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--main-html", type=Path, default=DEFAULT_MAIN_HTML)
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--keyword-page-glob", default=DEFAULT_PAGE_GLOB)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--pdf-keywords-out", type=Path, default=DEFAULT_PDF_KEYWORDS_OUT)
    parser.add_argument("--detail-pages-out", type=Path, default=DEFAULT_DETAIL_PAGES_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--anchors-out", type=Path, default=DEFAULT_ANCHORS_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def extract_pdf_text(path: Path) -> str:
    try:
        completed = subprocess.run(
            ["pdftotext", "-layout", str(path), "-"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as error:
        raise SystemExit("pdftotext is required; install poppler") from error
    return completed.stdout


def parse_pdf_records(text: str) -> list[PrimeMinisterRecord]:
    records: list[tuple[int, list[str]]] = []
    current_index: int | None = None
    current_lines: list[str] = []
    in_table = False
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if "English Name" in line and "Hebrew Name" in line:
            in_table = True
            continue
        if not in_table or not line.strip():
            continue
        match = PM_ROW_RE.match(line)
        if match:
            if current_index is not None:
                records.append((current_index, current_lines))
            current_index = int(match.group(1))
            current_lines = [line]
            continue
        if current_index is not None:
            current_lines.append(line)
    if current_index is not None:
        records.append((current_index, current_lines))
    return [PrimeMinisterRecord(index, tuple(lines)) for index, lines in records]


def keyword_field(line: str) -> str:
    if len(line) <= 35:
        return ""
    return line[35:].strip()


def english_name_field(line: str) -> str:
    if not PM_ROW_RE.match(line):
        return ""
    parts = re.split(r"\s{2,}", line.strip())
    if len(parts) >= 3:
        return parts[1].strip()
    return ""


def pdf_keyword_phrase_rows(text: str) -> int:
    return len(phrase_keyword_rows_from_pdf(text))


def phrase_keyword_rows_from_pdf(text: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line in text.splitlines():
        if "English Name" in line:
            break
        stripped = line.strip()
        if not stripped or stripped == "Israeli Prime Ministers":
            continue
        parts = re.split(r"\s{2,}", stripped)
        if len(parts) < 2:
            continue
        rows.append(
            {
                "source_table": "prime_minister_phrase_keywords",
                "record_index": "",
                "keyword_row_index": len(rows) + 1,
                "english_label": parts[0].strip(),
                "hebrew_keyword": parts[-1].strip(),
                "raw_line": stripped,
            }
        )
    return rows


def name_keyword_rows_from_records(
    records: list[PrimeMinisterRecord],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for record in records:
        keyword_row_index = 0
        for line in record.lines:
            keyword = keyword_field(line)
            if not keyword:
                continue
            keyword_row_index += 1
            rows.append(
                {
                    "source_table": "prime_minister_name_keywords",
                    "record_index": record.record_index,
                    "keyword_row_index": keyword_row_index,
                    "english_label": english_name_field(line),
                    "hebrew_keyword": keyword,
                    "raw_line": line.strip(),
                }
            )
    return rows


def pdf_keyword_rows_from_source(
    pdf_text: str,
    records: list[PrimeMinisterRecord],
) -> list[dict[str, object]]:
    return phrase_keyword_rows_from_pdf(pdf_text) + name_keyword_rows_from_records(records)


def parse_detail_page(path: Path) -> dict[str, object]:
    html = path.read_text(encoding="utf-8", errors="replace")
    extractor = TextExtractor()
    extractor.feed(html)
    text = re.sub(r"\s+", " ", extractor.text)
    match = re.search(r"Key Words:\s*([^<&]+)", html, flags=re.IGNORECASE)
    keyword_text = re.sub(r"\s+", " ", match.group(1).strip()) if match else ""
    title_match = re.search(r"<p><b>([^<]+)</b></p>", html, flags=re.IGNORECASE)
    title = re.sub(r"\s+", " ", title_match.group(1).strip()) if title_match else ""
    return {
        "path": str(path),
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
        "title": title,
        "keyword_text": keyword_text,
        "has_key_words": bool(keyword_text),
        "keyword_token_count": len(keyword_text.replace(",", " ").split()),
        "has_previous": "&lt; Previous &gt;" in html,
        "has_next": "&lt; Next &gt;" in html,
        "text": text,
    }


def detail_page_rows(detail_pages: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for page in detail_pages:
        path = str(page["path"])
        match = re.search(r"_(\d+)\.html$", path)
        rows.append(
            {
                "page_index": int(match.group(1)) if match else "",
                "path": path,
                "sha256": page["sha256"],
                "bytes": page["bytes"],
                "title": page["title"],
                "keyword_text": page["keyword_text"],
                "keyword_token_count": page["keyword_token_count"],
                "has_previous": int(bool(page["has_previous"])),
                "has_next": int(bool(page["has_next"])),
            }
        )
    return rows


def build_summary(
    args: argparse.Namespace,
    main_html: str,
    pdf_text: str,
    records: list[PrimeMinisterRecord],
    detail_pages: list[dict[str, object]],
    pdf_keyword_rows: list[dict[str, object]],
    detail_rows: list[dict[str, object]],
) -> dict[str, object]:
    record_rows = [record.as_row() for record in records]
    indexes = [record.record_index for record in records]
    detail_with_keywords = sum(1 for page in detail_pages if page["has_key_words"])
    return {
        "main_html": str(args.main_html),
        "main_sha256": sha256(args.main_html),
        "main_bytes": args.main_html.stat().st_size,
        "pdf": str(args.pdf),
        "pdf_sha256": sha256(args.pdf),
        "pdf_bytes": args.pdf.stat().st_size,
        "pdf_pages_from_text": pages_from_text(pdf_text),
        "pdf_prime_minister_rows": len(records),
        "pdf_prime_minister_min": min(indexes, default=""),
        "pdf_prime_minister_max": max(indexes, default=""),
        "pdf_keyword_phrase_rows": pdf_keyword_phrase_rows(pdf_text),
        "pdf_name_keyword_rows": sum(int(row["hebrew_keyword_rows"]) for row in record_rows),
        "machine_pdf_keyword_rows": len(pdf_keyword_rows),
        "html_detail_pages_found": len(detail_pages),
        "html_detail_pages_with_keywords": detail_with_keywords,
        "machine_html_detail_rows": len(detail_rows),
        "html_detail_page_gap_against_pdf_rows": max(0, len(records) - detail_with_keywords),
        "claim_status": "source_shape_only_not_result_bearing",
    }


def pages_from_text(text: str) -> int:
    stripped = text.rstrip("\f\n\r ")
    if not stripped:
        return 0
    return stripped.count("\f") + 1


def protocol_anchors(
    main_html: str,
    pdf_text: str,
    detail_pages: list[dict[str, object]],
) -> list[dict[str, str]]:
    main_text = text_from_html(main_html)
    normalized_pdf = re.sub(r"\s+", " ", pdf_text)
    detail_with_keywords = sum(1 for page in detail_pages if page["has_key_words"])
    checks = [
        (
            "main_html",
            "twelve_people_statement",
            "twelve people" in main_text,
            "main page states source population size",
        ),
        (
            "main_html",
            "expected_els_10",
            "Expected Number of ELS = 10" in main_text,
            "expected-ELS setting found",
        ),
        (
            "main_html",
            "trials_10000",
            "10,000" in main_text,
            "trial count found",
        ),
        (
            "main_html",
            "reported_p_level_6_of_10000",
            "6/10,000" in main_text,
            "reported p-level text found",
        ),
        (
            "pdf",
            "pdf_prime_minister_table",
            "English Name" in normalized_pdf and "Hebrew Name Key Words" in normalized_pdf,
            "PDF prime-minister keyword table found",
        ),
        (
            "detail_html",
            "detail_keyword_pages",
            detail_with_keywords > 0,
            "detail pages with keyword labels found",
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


def text_from_html(html: str) -> str:
    extractor = TextExtractor()
    extractor.feed(html)
    return re.sub(r"\s+", " ", extractor.text)


def write_markdown(
    path: Path,
    summary: dict[str, object],
    anchors: list[dict[str, str]],
) -> None:
    anchor_counts = Counter(anchor["status"] for anchor in anchors)
    lines = [
        "# Israeli Prime Ministers Source Audit",
        "",
        "Status: source-shape audit only. This is not an ELS result, not a",
        "statistical test, and not a claim-ready replication.",
        "",
        "## Sources",
        "",
        "- Main page: `https://www.torah-code.org/experiments/israeli_prime_ministers.shtml`",
        "- Keyword PDF: `https://www.torah-code.org/experiments/Israeli_prime_ministers.pdf`",
        "- Detail pages: `https://www.torah-code.org/experiments/israeli_prime_ministers_1.html` through `_8.html`",
        f"- Main SHA-256: `{summary['main_sha256']}`",
        f"- PDF SHA-256: `{summary['pdf_sha256']}`",
        "",
        "## Parsed Shape",
        "",
        "| Item | Count |",
        "| --- | ---: |",
        f"| PDF pages from extracted text | {summary['pdf_pages_from_text']} |",
        f"| PDF prime-minister rows | {summary['pdf_prime_minister_rows']} |",
        f"| PDF row index minimum | {summary['pdf_prime_minister_min']} |",
        f"| PDF row index maximum | {summary['pdf_prime_minister_max']} |",
        f"| PDF prime-minister phrase keyword rows | {summary['pdf_keyword_phrase_rows']} |",
        f"| PDF name-keyword rows | {summary['pdf_name_keyword_rows']} |",
        f"| machine PDF keyword rows extracted | {summary['machine_pdf_keyword_rows']} |",
        f"| HTML detail pages found | {summary['html_detail_pages_found']} |",
        f"| HTML detail pages with keyword labels | {summary['html_detail_pages_with_keywords']} |",
        f"| machine HTML detail rows extracted | {summary['machine_html_detail_rows']} |",
        f"| detail-page gap against PDF rows | {summary['html_detail_page_gap_against_pdf_rows']} |",
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
            "This audit verifies source shape and exports PDF keyword rows plus HTML",
            "detail-page keyword labels. It also exposes a source-coverage gap: the",
            "PDF lists 12 prime-minister rows, while the downloaded detail-page",
            "sequence has keyword labels for 8 pages. This should be treated as",
            "missing detail-source coverage, not inferred data.",
            "",
            "No term normalization, ELS search, compactness calculation, random-placement",
            "control, or p-level verification is performed here.",
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
        "sources": {
            "main_html": str(args.main_html),
            "pdf": str(args.pdf),
            "keyword_page_glob": args.keyword_page_glob,
        },
        "summary": summary,
        "anchor_status_counts": dict(Counter(anchor["status"] for anchor in anchors)),
        "rows": rows,
        "outputs": {
            "records": str(args.out),
            "pdf_keywords": str(args.pdf_keywords_out),
            "detail_pages": str(args.detail_pages_out),
            "summary": str(args.summary_out),
            "anchors": str(args.anchors_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "claim_boundary": "source-shape audit only; no ELS result",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
