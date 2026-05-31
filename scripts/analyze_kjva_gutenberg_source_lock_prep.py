#!/usr/bin/env python3
"""Prepare Project Gutenberg KJV + Apocrypha verse-shape evidence without importing text."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
from collections import OrderedDict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from els import __version__
from scripts.analyze_kjva_gutenberg_book_coverage_probe import (
    APOCRYPHA_TXT_URL,
    KJV_TXT_URL,
)


DEFAULT_KJVA_CSV = Path("data/processed/ebible/eng-kjv.csv")
DEFAULT_OUT_DIR = Path("reports/kjva_gutenberg_source_lock_prep")
DEFAULT_ROWS = DEFAULT_OUT_DIR / "book_shape.csv"
DEFAULT_SUMMARY = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_ANCHORS = DEFAULT_OUT_DIR / "anchors.csv"
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_MD = Path("docs/KJVA_GUTENBERG_SOURCE_LOCK_PREP.md")
USER_AGENT = "OpenBibleCodes-EDLS Gutenberg source-lock prep/1.0"

KJV_VERSE_MARKER_RE = re.compile(r"^(?P<book>\d{2}):(?P<chapter>\d{3}):(?P<verse>\d{3})\s+")
APOCRYPHA_CHAPTER_VERSE_MARKER_RE = re.compile(r"^(?P<chapter>\d+):(?P<verse>\d+)\s+")
APOCRYPHA_NUMBER_ONLY_MARKER_RE = re.compile(r"^(?P<verse>\d+)\s+")

ROW_FIELDNAMES = [
    "section",
    "book",
    "source_label",
    "source_components",
    "marker_shape",
    "gutenberg_marker_count",
    "local_kjva_verse_count",
    "delta",
    "status",
    "first_marker_line",
    "last_marker_line",
    "notes",
]
SUMMARY_FIELDNAMES = [
    "source_pages",
    "plain_text_pages_scanned",
    "raw_text_retained",
    "kjv_plain_text_bytes",
    "kjv_plain_text_sha256",
    "apocrypha_plain_text_bytes",
    "apocrypha_plain_text_sha256",
    "local_kjva_books",
    "local_kjva_verses",
    "local_kjva_kjv_verses",
    "local_kjva_apocrypha_verses",
    "book_shape_rows",
    "local_book_rows_compared",
    "kjv_books_compared",
    "kjv_books_exact_count_matches",
    "kjv_books_count_drift",
    "apocrypha_books_compared",
    "apocrypha_books_exact_count_matches",
    "apocrypha_books_count_drift",
    "extra_source_sections",
    "gutenberg_kjv_verse_markers",
    "gutenberg_apocrypha_chapter_verse_markers",
    "gutenberg_apocrypha_number_only_markers",
    "gutenberg_apocrypha_total_verse_like_markers",
    "baruch_epistle_split_detected",
    "source_lock_ready",
    "result_ready",
    "claim_status",
]
ANCHOR_FIELDNAMES = ["source", "anchor", "status", "diagnostic"]


@dataclass(frozen=True)
class TextPayload:
    raw: bytes
    final_url: str
    status: str
    source_mode: str
    error: str = ""


@dataclass(frozen=True)
class KJVBook:
    code: str
    name: str
    source_number: str


@dataclass(frozen=True)
class SourceSection:
    component: str
    label: str
    aliases: tuple[str, ...]


@dataclass(frozen=True)
class ApocryphaBook:
    code: str
    label: str
    source_components: tuple[str, ...]
    marker_shape: str
    notes: str = ""


KJV_BOOKS: tuple[KJVBook, ...] = (
    KJVBook("GEN", "Genesis", "01"),
    KJVBook("EXO", "Exodus", "02"),
    KJVBook("LEV", "Leviticus", "03"),
    KJVBook("NUM", "Numbers", "04"),
    KJVBook("DEU", "Deuteronomy", "05"),
    KJVBook("JOS", "Joshua", "06"),
    KJVBook("JDG", "Judges", "07"),
    KJVBook("RUT", "Ruth", "08"),
    KJVBook("1SA", "1 Samuel", "09"),
    KJVBook("2SA", "2 Samuel", "10"),
    KJVBook("1KI", "1 Kings", "11"),
    KJVBook("2KI", "2 Kings", "12"),
    KJVBook("1CH", "1 Chronicles", "13"),
    KJVBook("2CH", "2 Chronicles", "14"),
    KJVBook("EZR", "Ezra", "15"),
    KJVBook("NEH", "Nehemiah", "16"),
    KJVBook("EST", "Esther", "17"),
    KJVBook("JOB", "Job", "18"),
    KJVBook("PSA", "Psalms", "19"),
    KJVBook("PRO", "Proverbs", "20"),
    KJVBook("ECC", "Ecclesiastes", "21"),
    KJVBook("SNG", "Song of Solomon", "22"),
    KJVBook("ISA", "Isaiah", "23"),
    KJVBook("JER", "Jeremiah", "24"),
    KJVBook("LAM", "Lamentations", "25"),
    KJVBook("EZK", "Ezekiel", "26"),
    KJVBook("DAN", "Daniel", "27"),
    KJVBook("HOS", "Hosea", "28"),
    KJVBook("JOL", "Joel", "29"),
    KJVBook("AMO", "Amos", "30"),
    KJVBook("OBA", "Obadiah", "31"),
    KJVBook("JON", "Jonah", "32"),
    KJVBook("MIC", "Micah", "33"),
    KJVBook("NAM", "Nahum", "34"),
    KJVBook("HAB", "Habakkuk", "35"),
    KJVBook("ZEP", "Zephaniah", "36"),
    KJVBook("HAG", "Haggai", "37"),
    KJVBook("ZEC", "Zechariah", "38"),
    KJVBook("MAL", "Malachi", "39"),
    KJVBook("MAT", "Matthew", "40"),
    KJVBook("MRK", "Mark", "41"),
    KJVBook("LUK", "Luke", "42"),
    KJVBook("JHN", "John", "43"),
    KJVBook("ACT", "Acts", "44"),
    KJVBook("ROM", "Romans", "45"),
    KJVBook("1CO", "1 Corinthians", "46"),
    KJVBook("2CO", "2 Corinthians", "47"),
    KJVBook("GAL", "Galatians", "48"),
    KJVBook("EPH", "Ephesians", "49"),
    KJVBook("PHP", "Philippians", "50"),
    KJVBook("COL", "Colossians", "51"),
    KJVBook("1TH", "1 Thessalonians", "52"),
    KJVBook("2TH", "2 Thessalonians", "53"),
    KJVBook("1TI", "1 Timothy", "54"),
    KJVBook("2TI", "2 Timothy", "55"),
    KJVBook("TIT", "Titus", "56"),
    KJVBook("PHM", "Philemon", "57"),
    KJVBook("HEB", "Hebrews", "58"),
    KJVBook("JAS", "James", "59"),
    KJVBook("1PE", "1 Peter", "60"),
    KJVBook("2PE", "2 Peter", "61"),
    KJVBook("1JN", "1 John", "62"),
    KJVBook("2JN", "2 John", "63"),
    KJVBook("3JN", "3 John", "64"),
    KJVBook("JUD", "Jude", "65"),
    KJVBook("REV", "Revelation", "66"),
)

SOURCE_SECTIONS: tuple[SourceSection, ...] = (
    SourceSection("1ES", "1 Esdras", ("The First Book of Esdras",)),
    SourceSection("2ES", "2 Esdras", ("The Second Book of Esdras",)),
    SourceSection("TOB", "Tobit", ("The Book of Tobit",)),
    SourceSection("JDT", "Judith", ("The Book of Judith",)),
    SourceSection("ESG", "Rest of Esther", ("The Greek Additions to Esther",)),
    SourceSection("WIS", "Wisdom", ("The Wisdom of Solomon", "The Book of Wisdom")),
    SourceSection("SIR", "Ecclesiasticus", ("The Book of Sirach (or Ecclesiasticus)",)),
    SourceSection("BAR", "Baruch", ("The Book of Baruch",)),
    SourceSection(
        "LJE_SOURCE",
        "Epistle of Jeremiah",
        (
            "The Epistle [or Letter] of Jeremiah [Jeremy]",
            "The Epistle of Jeremy [sometimes Chapter Six of Baruch]",
        ),
    ),
    SourceSection("S3Y", "Song of the Three Children", ("The Song of the Three Holy Children",)),
    SourceSection("SUS", "Susanna", ("The Book of Susanna (in Daniel)",)),
    SourceSection(
        "BEL",
        "Bel and the Dragon",
        ("The History of the Destruction of Bel and the Dragon",),
    ),
    SourceSection("MAN", "Prayer of Manasseh", ("The Prayer of Manasses",)),
    SourceSection("1MA", "1 Maccabees", ("The First Book of the Maccabees",)),
    SourceSection("2MA", "2 Maccabees", ("The Second Book of the Maccabees",)),
)

APOCRYPHA_BOOKS: tuple[ApocryphaBook, ...] = (
    ApocryphaBook("TOB", "Tobit", ("TOB",), "chapter:verse"),
    ApocryphaBook("JDT", "Judith", ("JDT",), "chapter:verse"),
    ApocryphaBook("ESG", "Rest of Esther", ("ESG",), "chapter:verse"),
    ApocryphaBook("WIS", "Wisdom", ("WIS",), "chapter:verse"),
    ApocryphaBook("SIR", "Ecclesiasticus", ("SIR",), "chapter:verse"),
    ApocryphaBook(
        "BAR",
        "Baruch",
        ("BAR", "LJE_SOURCE"),
        "chapter:verse",
        "Project Gutenberg splits the Epistle of Jeremiah; local KJVA rolls it into BAR.",
    ),
    ApocryphaBook("S3Y", "Song of the Three Children", ("S3Y",), "number-only"),
    ApocryphaBook("SUS", "Susanna", ("SUS",), "chapter:verse"),
    ApocryphaBook("BEL", "Bel and the Dragon", ("BEL",), "chapter:verse"),
    ApocryphaBook("1MA", "1 Maccabees", ("1MA",), "chapter:verse"),
    ApocryphaBook("2MA", "2 Maccabees", ("2MA",), "chapter:verse"),
    ApocryphaBook("1ES", "1 Esdras", ("1ES",), "chapter:verse"),
    ApocryphaBook(
        "MAN",
        "Prayer of Manasseh",
        ("MAN",),
        "unmarked_prose",
        "Project Gutenberg body text has no verse markers for this section.",
    ),
    ApocryphaBook("2ES", "2 Esdras", ("2ES",), "chapter:verse"),
)
APOCRYPHA_CODES = {book.code for book in APOCRYPHA_BOOKS}


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    kjv = read_or_fetch_text(args.txt_path, args.txt_url, timeout=args.timeout)
    apocrypha = read_or_fetch_text(
        args.apocrypha_txt_path,
        args.apocrypha_txt_url,
        timeout=args.timeout,
    )
    local_counts = load_local_counts(args.kjva_csv)
    rows = build_book_shape_rows(kjv.raw, apocrypha.raw, local_counts)
    summary = build_summary(rows, kjv, apocrypha, local_counts)
    anchors = build_anchors(summary)
    write_csv(args.out, ROW_FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_csv(args.anchors_out, ANCHOR_FIELDNAMES, anchors)
    write_markdown(args.markdown_out, summary, rows, anchors, kjv=kjv, apocrypha=apocrypha)
    write_manifest(args.manifest_out, args, summary, rows, anchors, kjv, apocrypha, started)
    print(args.out)
    print(args.summary_out)
    print(args.anchors_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kjva-csv", type=Path, default=DEFAULT_KJVA_CSV)
    parser.add_argument("--txt-url", default=KJV_TXT_URL)
    parser.add_argument("--apocrypha-txt-url", default=APOCRYPHA_TXT_URL)
    parser.add_argument("--txt-path", type=Path)
    parser.add_argument("--apocrypha-txt-path", type=Path)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--out", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--anchors-out", type=Path, default=DEFAULT_ANCHORS)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    return parser


def read_or_fetch_text(path: Path | None, url: str, *, timeout: float) -> TextPayload:
    if path is not None:
        try:
            return TextPayload(
                raw=path.read_bytes(),
                final_url=str(path),
                status="read_local",
                source_mode="ignored_local_path",
            )
        except OSError as exc:
            return TextPayload(
                raw=b"",
                final_url=str(path),
                status="read_error",
                source_mode="ignored_local_path",
                error=str(exc),
            )
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout) as response:
            return TextPayload(
                raw=response.read(),
                final_url=response.geturl(),
                status="fetched",
                source_mode="network_fetch",
            )
    except HTTPError as exc:
        return TextPayload(
            raw=b"",
            final_url=url,
            status=f"http_error_{exc.code}",
            source_mode="network_fetch",
            error=str(exc),
        )
    except (OSError, URLError) as exc:
        return TextPayload(
            raw=b"",
            final_url=url,
            status="fetch_error",
            source_mode="network_fetch",
            error=str(exc),
        )


def load_local_counts(path: Path) -> OrderedDict[str, int]:
    counts: OrderedDict[str, int] = OrderedDict()
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            book = row["book"]
            counts[book] = counts.get(book, 0) + 1
    return counts


def build_book_shape_rows(
    kjv_raw: bytes,
    apocrypha_raw: bytes,
    local_counts: OrderedDict[str, int],
) -> list[dict[str, object]]:
    kjv_counts = parse_kjv_verse_marker_counts(kjv_raw.decode("utf-8", errors="replace"))
    apocrypha_counts = parse_apocrypha_source_sections(
        apocrypha_raw.decode("utf-8", errors="replace")
    )
    rows: list[dict[str, object]] = []
    for book in KJV_BOOKS:
        source_count = kjv_counts.get(book.source_number, {"count": 0, "first": "", "last": ""})
        local_count = local_counts.get(book.code, 0)
        rows.append(
            build_row(
                section="kjv",
                book=book.code,
                source_label=book.name,
                source_components=(book.source_number,),
                marker_shape="book:chapter:verse",
                gutenberg_count=int(source_count["count"]),
                local_count=local_count,
                first_line=source_count["first"],
                last_line=source_count["last"],
                notes="",
            )
        )
    for book in APOCRYPHA_BOOKS:
        component_counts = [apocrypha_counts.get(component, empty_component_count()) for component in book.source_components]
        source_count = sum(int(component["count"]) for component in component_counts)
        first_lines = [int(component["first"]) for component in component_counts if component["first"]]
        last_lines = [int(component["last"]) for component in component_counts if component["last"]]
        rows.append(
            build_row(
                section="apocrypha",
                book=book.code,
                source_label=book.label,
                source_components=book.source_components,
                marker_shape=book.marker_shape,
                gutenberg_count=source_count,
                local_count=local_counts.get(book.code, 0),
                first_line=min(first_lines) if first_lines else "",
                last_line=max(last_lines) if last_lines else "",
                notes=book.notes,
            )
        )
    extra = apocrypha_counts.get("LJE_SOURCE", empty_component_count())
    rows.append(
        {
            "section": "apocrypha_extra_source_section",
            "book": "LJE_SOURCE",
            "source_label": "Epistle of Jeremiah",
            "source_components": "LJE_SOURCE",
            "marker_shape": "chapter:verse",
            "gutenberg_marker_count": extra["count"],
            "local_kjva_verse_count": "",
            "delta": "",
            "status": "extra_source_component_rolls_into_BAR",
            "first_marker_line": extra["first"],
            "last_marker_line": extra["last"],
            "notes": "Project Gutenberg exposes this as a separate section; local KJVA counts it inside BAR.",
        }
    )
    return rows


def build_row(
    *,
    section: str,
    book: str,
    source_label: str,
    source_components: tuple[str, ...],
    marker_shape: str,
    gutenberg_count: int,
    local_count: int,
    first_line: object,
    last_line: object,
    notes: str,
) -> dict[str, object]:
    delta = gutenberg_count - local_count
    status = "exact_count_match" if delta == 0 else "count_drift"
    if local_count == 0:
        status = "local_book_missing"
    if gutenberg_count == 0 and local_count > 0:
        status = "source_markers_missing"
    return {
        "section": section,
        "book": book,
        "source_label": source_label,
        "source_components": ";".join(source_components),
        "marker_shape": marker_shape,
        "gutenberg_marker_count": gutenberg_count,
        "local_kjva_verse_count": local_count,
        "delta": delta,
        "status": status,
        "first_marker_line": first_line,
        "last_marker_line": last_line,
        "notes": notes,
    }


def parse_kjv_verse_marker_counts(text: str) -> dict[str, dict[str, object]]:
    counts: dict[str, dict[str, object]] = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = KJV_VERSE_MARKER_RE.match(line.strip())
        if match is None:
            continue
        book = match.group("book")
        row = counts.setdefault(book, {"count": 0, "first": line_number, "last": line_number})
        row["count"] = int(row["count"]) + 1
        row["last"] = line_number
    return counts


def parse_apocrypha_source_sections(text: str) -> dict[str, dict[str, object]]:
    aliases: dict[str, str] = {}
    for section in SOURCE_SECTIONS:
        for alias in section.aliases:
            aliases[normalize_heading(alias)] = section.component

    lines = text.splitlines()
    counts = {section.component: empty_component_count() for section in SOURCE_SECTIONS}
    current = ""
    index = 0
    while index < len(lines):
        heading = detect_heading(lines, index, aliases)
        if heading is not None:
            current, consumed = heading
            index += consumed
            continue
        stripped = lines[index].strip()
        marker_kind = ""
        if APOCRYPHA_CHAPTER_VERSE_MARKER_RE.match(stripped):
            marker_kind = "chapter_verse"
        elif APOCRYPHA_NUMBER_ONLY_MARKER_RE.match(stripped):
            marker_kind = "number_only"
        if current and marker_kind:
            row = counts[current]
            row["count"] = int(row["count"]) + 1
            row[marker_kind] = int(row[marker_kind]) + 1
            if not row["first"]:
                row["first"] = index + 1
            row["last"] = index + 1
        index += 1
    return counts


def detect_heading(
    lines: list[str],
    index: int,
    aliases: dict[str, str],
) -> tuple[str, int] | None:
    current = normalize_heading(lines[index])
    if current in aliases:
        return aliases[current], 1
    if index + 1 < len(lines):
        combined = normalize_heading(f"{lines[index]} {lines[index + 1]}")
        if combined in aliases:
            return aliases[combined], 2
    return None


def empty_component_count() -> dict[str, object]:
    return {"count": 0, "chapter_verse": 0, "number_only": 0, "first": "", "last": ""}


def build_summary(
    rows: list[dict[str, object]],
    kjv: TextPayload,
    apocrypha: TextPayload,
    local_counts: OrderedDict[str, int],
) -> dict[str, object]:
    kjv_rows = [row for row in rows if row["section"] == "kjv"]
    apocrypha_rows = [row for row in rows if row["section"] == "apocrypha"]
    exact_kjv = sum(1 for row in kjv_rows if row["status"] == "exact_count_match")
    exact_apocrypha = sum(
        1 for row in apocrypha_rows if row["status"] == "exact_count_match"
    )
    apocrypha_chapter_verse = sum(
        int(row["gutenberg_marker_count"])
        for row in apocrypha_rows
        if row["marker_shape"] == "chapter:verse"
    )
    apocrypha_number_only = sum(
        int(row["gutenberg_marker_count"])
        for row in apocrypha_rows
        if row["marker_shape"] == "number-only"
    )
    return {
        "source_pages": 2,
        "plain_text_pages_scanned": sum(1 for payload in (kjv, apocrypha) if payload.raw),
        "raw_text_retained": False,
        "kjv_plain_text_bytes": len(kjv.raw),
        "kjv_plain_text_sha256": hashlib.sha256(kjv.raw).hexdigest() if kjv.raw else "",
        "apocrypha_plain_text_bytes": len(apocrypha.raw),
        "apocrypha_plain_text_sha256": hashlib.sha256(apocrypha.raw).hexdigest()
        if apocrypha.raw
        else "",
        "local_kjva_books": len(local_counts),
        "local_kjva_verses": sum(local_counts.values()),
        "local_kjva_kjv_verses": sum(
            local_counts.get(book.code, 0) for book in KJV_BOOKS
        ),
        "local_kjva_apocrypha_verses": sum(
            count for book, count in local_counts.items() if book in APOCRYPHA_CODES
        ),
        "book_shape_rows": len(rows),
        "local_book_rows_compared": len(kjv_rows) + len(apocrypha_rows),
        "kjv_books_compared": len(kjv_rows),
        "kjv_books_exact_count_matches": exact_kjv,
        "kjv_books_count_drift": len(kjv_rows) - exact_kjv,
        "apocrypha_books_compared": len(apocrypha_rows),
        "apocrypha_books_exact_count_matches": exact_apocrypha,
        "apocrypha_books_count_drift": len(apocrypha_rows) - exact_apocrypha,
        "extra_source_sections": sum(
            1 for row in rows if row["section"] == "apocrypha_extra_source_section"
        ),
        "gutenberg_kjv_verse_markers": sum(
            int(row["gutenberg_marker_count"]) for row in kjv_rows
        ),
        "gutenberg_apocrypha_chapter_verse_markers": apocrypha_chapter_verse,
        "gutenberg_apocrypha_number_only_markers": apocrypha_number_only,
        "gutenberg_apocrypha_total_verse_like_markers": (
            apocrypha_chapter_verse + apocrypha_number_only
        ),
        "baruch_epistle_split_detected": any(
            row["book"] == "LJE_SOURCE"
            and int(row["gutenberg_marker_count"]) > 0
            for row in rows
        ),
        "source_lock_ready": False,
        "result_ready": False,
        "claim_status": "source_lock_prep_only_not_result_bearing",
    }


def build_anchors(summary: dict[str, object]) -> list[dict[str, str]]:
    checks = [
        (
            "gutenberg",
            "plain_text_pages_scanned",
            int(summary["plain_text_pages_scanned"]) == 2,
            "Project Gutenberg KJV and Apocrypha plain text were scanned for counts",
        ),
        (
            "gutenberg",
            "kjv_counts_exact",
            int(summary["kjv_books_exact_count_matches"]) == 66,
            "all 66 KJV book counts match the current local KJVA corpus",
        ),
        (
            "gutenberg",
            "apocrypha_count_drift_recorded",
            int(summary["apocrypha_books_count_drift"]) == 2,
            "two Apocrypha/deuterocanon book-count drifts are recorded",
        ),
        (
            "gutenberg",
            "baruch_epistle_split_detected",
            bool(summary["baruch_epistle_split_detected"]),
            "eBook 124 separates Epistle of Jeremiah from Baruch",
        ),
        (
            "gutenberg",
            "source_lock_not_ready",
            not bool(summary["source_lock_ready"]),
            "no source-lock-ready corpus import is declared",
        ),
        (
            "gutenberg",
            "result_not_ready",
            not bool(summary["result_ready"]),
            "no result-bearing replication is declared ready",
        ),
    ]
    return [
        {
            "source": source,
            "anchor": anchor,
            "status": "found" if ok else "missing",
            "diagnostic": diagnostic,
        }
        for source, anchor, ok, diagnostic in checks
    ]


def write_markdown(
    path: Path,
    summary: dict[str, object],
    rows: list[dict[str, object]],
    anchors: list[dict[str, str]],
    *,
    kjv: TextPayload,
    apocrypha: TextPayload,
) -> None:
    found_anchors = sum(1 for row in anchors if row["status"] == "found")
    drift_rows = [
        row
        for row in rows
        if row["section"] == "apocrypha" and row["status"] != "exact_count_match"
    ]
    extra_rows = [row for row in rows if row["section"] == "apocrypha_extra_source_section"]
    lines = [
        "# KJVA Gutenberg Source-Lock Prep",
        "",
        "Status: source-lock prep only.",
        "",
        "This is not an ELS result, not a corpus import, not a source lock, and not a result-bearing replication.",
        "It scans Project Gutenberg eBook 30 and eBook 124 plain text only to compare verse-marker counts against the current local KJVA corpus.",
        "It does not commit Bible text, normalize Bible text, create a local corpus, or declare a source-lock-ready stream.",
        "",
        "## Summary",
        "",
        f"- Source pages: {summary['source_pages']}.",
        f"- Plain-text pages scanned: {summary['plain_text_pages_scanned']}.",
        f"- Raw text retained: {int(bool(summary['raw_text_retained']))}.",
        f"- KJV plain-text bytes scanned: {summary['kjv_plain_text_bytes']}.",
        f"- Apocrypha plain-text bytes scanned: {summary['apocrypha_plain_text_bytes']}.",
        f"- Local KJVA books counted: {summary['local_kjva_books']}.",
        f"- Local KJVA verses counted: {summary['local_kjva_verses']}.",
        f"- Local KJV verses counted: {summary['local_kjva_kjv_verses']}.",
        f"- Local Apocrypha/deuterocanon verses counted: {summary['local_kjva_apocrypha_verses']}.",
        f"- Book-shape rows written: {summary['book_shape_rows']}.",
        f"- Local book rows compared: {summary['local_book_rows_compared']}.",
        f"- KJV books compared: {summary['kjv_books_compared']}.",
        f"- KJV exact count matches: {summary['kjv_books_exact_count_matches']}.",
        f"- KJV count drifts: {summary['kjv_books_count_drift']}.",
        f"- Apocrypha/deuterocanon books compared: {summary['apocrypha_books_compared']}.",
        f"- Apocrypha/deuterocanon exact count matches: {summary['apocrypha_books_exact_count_matches']}.",
        f"- Apocrypha/deuterocanon count drifts: {summary['apocrypha_books_count_drift']}.",
        f"- Extra source sections: {summary['extra_source_sections']}.",
        f"- Gutenberg KJV verse markers: {summary['gutenberg_kjv_verse_markers']}.",
        f"- Gutenberg Apocrypha/deuterocanon chapter:verse markers: {summary['gutenberg_apocrypha_chapter_verse_markers']}.",
        f"- Gutenberg Apocrypha/deuterocanon number-only markers: {summary['gutenberg_apocrypha_number_only_markers']}.",
        f"- Gutenberg Apocrypha/deuterocanon total verse-like markers: {summary['gutenberg_apocrypha_total_verse_like_markers']}.",
        f"- Baruch/Epistle split detected: {int(bool(summary['baruch_epistle_split_detected']))}.",
        f"- Source-lock ready: {int(bool(summary['source_lock_ready']))}.",
        f"- Result-ready sources: {int(bool(summary['result_ready']))}.",
        f"- Claim status: `{summary['claim_status']}`.",
        "",
        "## Shape Read",
        "",
        "Project Gutenberg eBook 30 has exact verse-count agreement with the current local KJVA corpus for all 66 KJV books.",
        "Project Gutenberg eBook 124 has exact count agreement for 12 of 14 tracked Apocrypha/deuterocanon books after Baruch is read together with the separate Epistle of Jeremiah source section.",
        "The remaining count drifts are Sirach at one fewer source marker and Prayer of Manasseh with no verse markers in the Project Gutenberg body text.",
        "That means Project Gutenberg is stronger than metadata-only evidence, but it still needs a real collation and source-use lock before any replication run.",
        "",
        "## Apocrypha Drift Rows",
        "",
        "| Book | Source marker count | Local KJVA count | Delta | Status | Notes |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in drift_rows:
        lines.append(
            f"| {row['book']} | {row['gutenberg_marker_count']} | {row['local_kjva_verse_count']} | {row['delta']} | `{row['status']}` | {row['notes']} |"
        )
    lines.extend(
        [
            "",
            "## Extra Source Sections",
            "",
            "| Source section | Marker count | Status | Notes |",
            "| --- | ---: | --- | --- |",
        ]
    )
    for row in extra_rows:
        lines.append(
            f"| {row['book']} | {row['gutenberg_marker_count']} | `{row['status']}` | {row['notes']} |"
        )
    lines.extend(
        [
            "",
            "## Anchors",
            "",
            f"Found anchors: {found_anchors}/{len(anchors)}.",
            "",
            "| Source | Anchor | Status | Diagnostic |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in anchors:
        lines.append(f"| {row['source']} | `{row['anchor']}` | `{row['status']}` | {row['diagnostic']} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            f"KJV source scanned: `{kjv.final_url}`.",
            f"Apocrypha source scanned: `{apocrypha.final_url}`.",
            "Raw source text is scanned in memory or from an ignored local path and is not written to tracked files.",
            "This prep does not choose a source stream, does not make a verse map, does not perform text collation, does not set a term lock, and does not create a study-lock sidecar.",
            "It does not change any KJVA bridge result status.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary: dict[str, object],
    rows: list[dict[str, object]],
    anchors: list[dict[str, str]],
    kjv: TextPayload,
    apocrypha: TextPayload,
    started: float,
) -> None:
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "els_version": __version__,
        "tool": "scripts.analyze_kjva_gutenberg_source_lock_prep",
        "kjva_csv": str(args.kjva_csv),
        "kjv_source": kjv.final_url,
        "apocrypha_source": apocrypha.final_url,
        "kjv_source_mode": kjv.source_mode,
        "apocrypha_source_mode": apocrypha.source_mode,
        "kjv_status": kjv.status,
        "apocrypha_status": apocrypha.status,
        "claim_boundary": "source-lock prep only; no ELS result",
        "text_retention": "plain text scanned in memory or ignored local path; Bible text not committed",
        "row_count": len(rows),
        "summary": summary,
        "anchor_count": len(anchors),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "outputs": {
            "rows": str(args.out),
            "summary": str(args.summary_out),
            "anchors": str(args.anchors_out),
            "markdown": str(args.markdown_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def normalize_heading(value: str) -> str:
    value = value.strip().lstrip("\ufeff").strip("[]")
    value = re.sub(r"[^a-z0-9]+", " ", value.casefold())
    return " ".join(value.split())


if __name__ == "__main__":
    raise SystemExit(main())
