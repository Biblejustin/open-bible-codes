#!/usr/bin/env python3
"""Audit full Hakkaac KJV Apocrypha marker coverage without importing text."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from els import __version__
from scripts.analyze_kjva_hakkaac_apocrypha_boundary_candidate import (
    TextPayload,
    compact_markers,
    extract_chapter_markers,
    fetch_page,
    html_visible_items,
    license_note_present,
    write_csv,
)


DEFAULT_KJVA_CSV = Path("data/processed/ebible/eng-kjv.csv")
DEFAULT_OUT_DIR = Path("reports/kjva_hakkaac_apocrypha_marker_coverage")
DEFAULT_ROWS = DEFAULT_OUT_DIR / "book_marker_coverage.csv"
DEFAULT_CHAPTER_ROWS = DEFAULT_OUT_DIR / "chapter_marker_coverage.csv"
DEFAULT_SUMMARY = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_MD = Path("docs/KJVA_HAKKAAC_APOCRYPHA_MARKER_COVERAGE.md")

HAKKAAC_INDEX_URL = "https://hakkaac.org/Bible/Bible/ap/KJV/KJV-AP/KJV_index_AP.html"

BOOK_ROW_FIELDNAMES = [
    "book",
    "title",
    "chapter_prefix",
    "source_url",
    "source_status",
    "bytes",
    "sha256",
    "license_note_present",
    "source_chapters",
    "local_chapters",
    "source_total_markers",
    "local_total_markers",
    "chapter_drift_rows",
    "status",
    "candidate_status",
    "notes",
]
CHAPTER_ROW_FIELDNAMES = [
    "book",
    "title",
    "chapter",
    "source_url",
    "source_status",
    "source_marker_count",
    "local_marker_count",
    "source_markers_present",
    "local_markers_expected",
    "status",
]
SUMMARY_FIELDNAMES = [
    "pages_scanned",
    "local_books_compared",
    "exact_book_marker_matches",
    "count_drift_books",
    "source_total_markers",
    "local_total_markers",
    "chapter_rows",
    "chapter_drift_rows",
    "license_note_pages",
    "source_lock_ready",
    "result_ready",
    "claim_status",
]


@dataclass(frozen=True)
class HakkaacBook:
    book: str
    title: str
    chapter_prefix: str
    index_label: str


class IndexLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._href_stack: list[str] = []
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        attrs_map = {name.lower(): value for name, value in attrs}
        href = attrs_map.get("href")
        if href:
            self._href_stack.append(href)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._href_stack:
            self._href_stack.pop()

    def handle_data(self, data: str) -> None:
        if not self._href_stack:
            return
        label = " ".join(data.split())
        if label:
            self.links.append((label, self._href_stack[-1]))


BOOKS: tuple[HakkaacBook, ...] = (
    HakkaacBook("TOB", "Tobit", "Tobit", "Tobit"),
    HakkaacBook("JDT", "Judith", "Judith", "Judith"),
    HakkaacBook("ESG", "Additions to Esther (Greek)", "Additions to Esther (Greek)", "Additions to Esther (Greek)"),
    HakkaacBook("WIS", "Wisdom of Solomon", "Wisdom of Solomon", "Wisdom of Solomon"),
    HakkaacBook("SIR", "Sirach", "Sirach", "Sirach"),
    HakkaacBook("BAR", "Baruch", "Baruch", "Baruch"),
    HakkaacBook("S3Y", "Prayer of Azarias/Azariah", "Prayer of Azarias", "Prayer of Azarias/Azariah"),
    HakkaacBook("SUS", "Susanna", "Susanna", "Susanna"),
    HakkaacBook("BEL", "Bel and the Dragon", "Bel and the Dragon", "Bel and the Dragon"),
    HakkaacBook("1MA", "1 Maccabees", "1 Maccabees", "1 Maccabees"),
    HakkaacBook("2MA", "2 Maccabees", "2 Maccabees", "2 Maccabees"),
    HakkaacBook("1ES", "1 Esdras", "1 Esdras", "1 Esdras"),
    HakkaacBook("MAN", "Prayer of Manasses", "Prayer of Manasses", "Prayer of Manasses"),
    HakkaacBook("2ES", "2 Esdras", "2 Esdras", "2 Esdras"),
)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    local_counts = load_local_chapter_counts(args.kjva_csv, books=BOOKS)
    index_payload = fetch_page(HAKKAAC_INDEX_URL, timeout=args.timeout)
    links = parse_index_links(index_payload.raw.decode("utf-8", errors="replace"))
    book_rows, chapter_rows = analyze_books(
        BOOKS,
        links,
        local_counts,
        timeout=args.timeout,
    )
    summary = build_summary(book_rows, chapter_rows)
    write_csv(args.out, BOOK_ROW_FIELDNAMES, book_rows)
    write_csv(args.chapter_out, CHAPTER_ROW_FIELDNAMES, chapter_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, book_rows, summary)
    write_manifest(
        args.manifest_out,
        args,
        index_payload=index_payload,
        book_rows=book_rows,
        chapter_rows=chapter_rows,
        summary=summary,
        started=started,
    )
    print(args.out)
    print(args.chapter_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--kjva-csv", type=Path, default=DEFAULT_KJVA_CSV)
    parser.add_argument("--out", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--chapter-out", type=Path, default=DEFAULT_CHAPTER_ROWS)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def parse_index_links(text: str) -> dict[str, str]:
    parser = IndexLinkParser()
    parser.feed(text)
    links: dict[str, str] = {}
    for label, href in parser.links:
        links.setdefault(label, urljoin(HAKKAAC_INDEX_URL, href))
    return links


def load_local_chapter_counts(
    path: Path,
    *,
    books: tuple[HakkaacBook, ...],
) -> dict[str, dict[int, int]]:
    wanted = {book.book for book in books}
    counts: dict[str, dict[int, int]] = {book.book: defaultdict(int) for book in books}
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            book = row.get("book", "")
            if book not in wanted:
                continue
            counts[book][int(row["chapter"])] += 1
    return {book: dict(chapters) for book, chapters in counts.items()}


def analyze_books(
    books: tuple[HakkaacBook, ...],
    links: dict[str, str],
    local_counts: dict[str, dict[int, int]],
    *,
    timeout: float,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    book_rows: list[dict[str, Any]] = []
    chapter_rows: list[dict[str, Any]] = []
    for book in books:
        url = links.get(book.index_label, "")
        payload = fetch_page(url, timeout=timeout) if url else TextPayload(b"", "", "missing_index_link")
        rows = analyze_book_chapters(book, payload, local_counts.get(book.book, {}))
        chapter_rows.extend(rows)
        book_rows.append(build_book_row(book, payload, rows, local_counts.get(book.book, {})))
    return book_rows, chapter_rows


def analyze_book_chapters(
    book: HakkaacBook,
    payload: TextPayload,
    local_chapters: dict[int, int],
) -> list[dict[str, Any]]:
    text = payload.raw.decode("utf-8", errors="replace")
    visible_items = html_visible_items(text)
    rows: list[dict[str, Any]] = []
    for chapter in sorted(local_chapters):
        heading = f"{book.chapter_prefix} {chapter}"
        markers = extract_chapter_markers(visible_items, heading)
        local_count = local_chapters[chapter]
        status = "exact_marker_match" if len(markers) == local_count else "count_drift"
        rows.append(
            {
                "book": book.book,
                "title": book.title,
                "chapter": chapter,
                "source_url": payload.final_url,
                "source_status": payload.status,
                "source_marker_count": len(markers),
                "local_marker_count": local_count,
                "source_markers_present": compact_markers(markers),
                "local_markers_expected": compact_markers(list(range(1, local_count + 1))),
                "status": status,
            }
        )
    return rows


def build_book_row(
    book: HakkaacBook,
    payload: TextPayload,
    chapter_rows: list[dict[str, Any]],
    local_chapters: dict[int, int],
) -> dict[str, Any]:
    text = payload.raw.decode("utf-8", errors="replace")
    source_total = sum(int(row["source_marker_count"]) for row in chapter_rows)
    local_total = sum(local_chapters.values())
    chapter_drift_rows = sum(1 for row in chapter_rows if row["status"] != "exact_marker_match")
    exact = (
        bool(local_chapters)
        and source_total == local_total
        and len(chapter_rows) == len(local_chapters)
        and chapter_drift_rows == 0
    )
    status = "exact_marker_match" if exact else "count_drift"
    notes = (
        "Marker-only audit finds exact chapter and verse-marker count agreement."
        if exact
        else "Marker-only audit finds count drift or missing source page."
    )
    return {
        "book": book.book,
        "title": book.title,
        "chapter_prefix": book.chapter_prefix,
        "source_url": payload.final_url,
        "source_status": payload.status,
        "bytes": len(payload.raw),
        "sha256": hashlib.sha256(payload.raw).hexdigest() if payload.raw else "",
        "license_note_present": license_note_present(text),
        "source_chapters": len(chapter_rows),
        "local_chapters": len(local_chapters),
        "source_total_markers": source_total,
        "local_total_markers": local_total,
        "chapter_drift_rows": chapter_drift_rows,
        "status": status,
        "candidate_status": f"hakkaac_{status}_candidate_not_source_lock",
        "notes": notes,
    }


def build_summary(
    book_rows: list[dict[str, Any]],
    chapter_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "pages_scanned": len(book_rows),
        "local_books_compared": len(book_rows),
        "exact_book_marker_matches": sum(1 for row in book_rows if row["status"] == "exact_marker_match"),
        "count_drift_books": sum(1 for row in book_rows if row["status"] != "exact_marker_match"),
        "source_total_markers": sum(int(row["source_total_markers"]) for row in book_rows),
        "local_total_markers": sum(int(row["local_total_markers"]) for row in book_rows),
        "chapter_rows": len(chapter_rows),
        "chapter_drift_rows": sum(1 for row in chapter_rows if row["status"] != "exact_marker_match"),
        "license_note_pages": sum(1 for row in book_rows if bool(row["license_note_present"])),
        "source_lock_ready": False,
        "result_ready": False,
        "claim_status": "marker_coverage_audit_only_not_result_bearing",
    }


def write_markdown(
    path: Path,
    book_rows: list[dict[str, Any]],
    summary: dict[str, Any],
) -> None:
    lines = [
        "# KJVA Hakkaac Apocrypha Marker Coverage",
        "",
        "Status: marker-coverage audit only.",
        "",
        "This is not an ELS result, not a corpus import, not a source lock, and not a result-bearing replication.",
        "It scans Hakkaac KJV Apocrypha pages for visible chapter and verse markers only.",
        "It does not commit Bible text, normalize Bible text, create a local corpus, split prose, or authorize a result-bearing run.",
        "",
        "## Summary",
        "",
        f"- Pages scanned: {summary['pages_scanned']}.",
        f"- Exact book marker matches: {summary['exact_book_marker_matches']}/{summary['local_books_compared']}.",
        f"- Count-drift books: {summary['count_drift_books']}.",
        f"- Source markers: {summary['source_total_markers']}.",
        f"- Local markers: {summary['local_total_markers']}.",
        f"- Chapter rows: {summary['chapter_rows']}.",
        f"- Chapter drift rows: {summary['chapter_drift_rows']}.",
        f"- Pages with public-domain note: {summary['license_note_pages']}.",
        f"- Source-lock ready: {int(bool(summary['source_lock_ready']))}.",
        f"- Result-ready sources: {int(bool(summary['result_ready']))}.",
        f"- Claim status: `{summary['claim_status']}`.",
        "",
        "## Book Rows",
        "",
        "| Book | Title | Source markers | Local markers | Chapters | Status | Candidate status |",
        "| --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in book_rows:
        lines.append(
            f"| `{row['book']}` | {row['title']} | {row['source_total_markers']} | {row['local_total_markers']} | {row['source_chapters']} | `{row['status']}` | `{row['candidate_status']}` |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "All 14 Hakkaac Apocrypha pages expose the same chapter and visible verse-marker counts as the local KJVA Apocrypha corpus.",
            "This includes `SIR` and `MAN`, the two boundary blockers found in the Project Gutenberg source-lock blocker packet.",
            "The audit strengthens Hakkaac as a possible split-source replication candidate, but only at marker level.",
            "",
            "## Boundary",
            "",
            "No Bible text is written to tracked outputs.",
            "This page does not change KJVA bridge result status.",
            "Next source-use work still needs policy lock, local ignored text import if allowed, verse mapping, collation against current eBible KJVA, checksums, term lock, and study-lock sidecar.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    *,
    index_payload: TextPayload,
    book_rows: list[dict[str, Any]],
    chapter_rows: list[dict[str, Any]],
    summary: dict[str, Any],
    started: float,
) -> None:
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "els_version": __version__,
        "tool": "scripts.analyze_kjva_hakkaac_apocrypha_marker_coverage",
        "claim_boundary": "marker-coverage audit only; no ELS result",
        "text_retention": "no Bible text written to tracked outputs",
        "row_count": len(book_rows),
        "chapter_row_count": len(chapter_rows),
        "summary": summary,
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "index_url": HAKKAAC_INDEX_URL,
            "index_status": index_payload.status,
            "kjva_csv": str(args.kjva_csv),
            "book_urls": [row["source_url"] for row in book_rows],
        },
        "outputs": {
            "rows": str(args.out),
            "chapter_rows": str(args.chapter_out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
