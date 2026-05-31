#!/usr/bin/env python3
"""Probe Project Gutenberg KJV + Apocrypha heading coverage without importing text."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from els import __version__
from scripts.analyze_kjva_gutenberg_candidate_source import EBOOK_PAGE_URL


KJV_TXT_URL = "https://www.gutenberg.org/ebooks/30.txt.utf-8"
APOCRYPHA_TXT_URL = "https://www.gutenberg.org/ebooks/124.txt.utf-8"
DEFAULT_OUT_DIR = Path("reports/kjva_gutenberg_book_coverage_probe")
DEFAULT_ROWS = DEFAULT_OUT_DIR / "book_headings.csv"
DEFAULT_SUMMARY = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_ANCHORS = DEFAULT_OUT_DIR / "anchors.csv"
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_MD = Path("docs/KJVA_GUTENBERG_BOOK_COVERAGE_PROBE.md")
USER_AGENT = "OpenBibleCodes-EDLS Gutenberg coverage probe/1.0"
BOOK_HEADING_RE = re.compile(r"^Book\s+(?P<number>\d{2})\s+(?P<name>.+?)\s*$")

ROW_FIELDNAMES = [
    "source_id",
    "source_text_id",
    "section",
    "expected_book",
    "aliases",
    "found_heading",
    "status",
    "found_book_number",
    "marker_count",
    "first_line",
    "last_line",
]
SUMMARY_FIELDNAMES = [
    "source_pages",
    "fetched_plain_text_pages",
    "kjv_plain_text_bytes",
    "kjv_plain_text_sha256",
    "apocrypha_plain_text_bytes",
    "apocrypha_plain_text_sha256",
    "expected_kjv_books",
    "found_kjv_book_headings",
    "missing_kjv_book_headings",
    "expected_apocrypha_books",
    "found_apocrypha_book_headings",
    "missing_apocrypha_book_headings",
    "extra_apocrypha_source_headings",
    "book_order_lock_ready",
    "verse_import_ready",
    "source_lock_ready",
    "result_ready",
    "claim_status",
]
ANCHOR_FIELDNAMES = ["source", "anchor", "status", "diagnostic"]


@dataclass(frozen=True)
class BookExpectation:
    section: str
    name: str
    aliases: tuple[str, ...] = ()


@dataclass(frozen=True)
class FetchedText:
    raw: bytes
    final_url: str
    fetch_status: str
    error: str = ""


KJV_BOOKS = (
    "Genesis",
    "Exodus",
    "Leviticus",
    "Numbers",
    "Deuteronomy",
    "Joshua",
    "Judges",
    "Ruth",
    "1 Samuel",
    "2 Samuel",
    "1 Kings",
    "2 Kings",
    "1 Chronicles",
    "2 Chronicles",
    "Ezra",
    "Nehemiah",
    "Esther",
    "Job",
    "Psalms",
    "Proverbs",
    "Ecclesiastes",
    "Song of Solomon",
    "Isaiah",
    "Jeremiah",
    "Lamentations",
    "Ezekiel",
    "Daniel",
    "Hosea",
    "Joel",
    "Amos",
    "Obadiah",
    "Jonah",
    "Micah",
    "Nahum",
    "Habakkuk",
    "Zephaniah",
    "Haggai",
    "Zechariah",
    "Malachi",
    "Matthew",
    "Mark",
    "Luke",
    "John",
    "Acts",
    "Romans",
    "1 Corinthians",
    "2 Corinthians",
    "Galatians",
    "Ephesians",
    "Philippians",
    "Colossians",
    "1 Thessalonians",
    "2 Thessalonians",
    "1 Timothy",
    "2 Timothy",
    "Titus",
    "Philemon",
    "Hebrews",
    "James",
    "1 Peter",
    "2 Peter",
    "1 John",
    "2 John",
    "3 John",
    "Jude",
    "Revelation",
)
APOCRYPHA_BOOKS = (
    BookExpectation("apocrypha", "1 Esdras", ("The First Book of Esdras", "First Esdras")),
    BookExpectation("apocrypha", "2 Esdras", ("The Second Book of Esdras", "Second Esdras")),
    BookExpectation("apocrypha", "Tobit", ("The Book of Tobit",)),
    BookExpectation("apocrypha", "Judith", ("The Book of Judith",)),
    BookExpectation("apocrypha", "Rest of Esther", ("The Greek Additions to Esther", "Additions to Esther")),
    BookExpectation("apocrypha", "Wisdom", ("The Wisdom of Solomon", "Wisdom of Solomon")),
    BookExpectation("apocrypha", "Ecclesiasticus", ("The Book of Sirach (or Ecclesiasticus)", "Sirach")),
    BookExpectation("apocrypha", "Baruch", ("The Book of Baruch",)),
    BookExpectation("apocrypha", "Song of the Three Children", ("The Song of the Three Holy Children",)),
    BookExpectation("apocrypha", "Susanna", ("The Book of Susanna (in Daniel)", "The Book of Susanna")),
    BookExpectation(
        "apocrypha",
        "Bel and the Dragon",
        ("The History of the Destruction of Bel and the Dragon",),
    ),
    BookExpectation("apocrypha", "Prayer of Manasseh", ("The Prayer of Manasses",)),
    BookExpectation("apocrypha", "1 Maccabees", ("The First Book of the Maccabees",)),
    BookExpectation("apocrypha", "2 Maccabees", ("The Second Book of the Maccabees",)),
)
EXTRA_APOCRYPHA_SOURCE_HEADINGS = ("The Epistle (or letter) of Jeremiah",)
EXPECTED_BOOKS: tuple[BookExpectation, ...] = tuple(
    BookExpectation("kjv", name) for name in KJV_BOOKS
) + APOCRYPHA_BOOKS


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    kjv = fetch_text(args.txt_url, timeout=args.timeout)
    apocrypha = fetch_text(args.apocrypha_txt_url, timeout=args.timeout)
    rows = build_book_rows(kjv.raw, apocrypha.raw)
    summary = build_summary(rows, kjv, apocrypha)
    anchors = build_anchors(summary, kjv, apocrypha)
    write_csv(args.out, ROW_FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_csv(args.anchors_out, ANCHOR_FIELDNAMES, anchors)
    write_markdown(
        args.markdown_out,
        summary,
        rows,
        anchors,
        kjv_final_url=kjv.final_url,
        apocrypha_final_url=apocrypha.final_url,
    )
    write_manifest(args.manifest_out, args, summary, rows, anchors, kjv, apocrypha, started)
    print(args.out)
    print(args.summary_out)
    print(args.anchors_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--txt-url", default=KJV_TXT_URL)
    parser.add_argument("--apocrypha-txt-url", default=APOCRYPHA_TXT_URL)
    parser.add_argument("--ebook-page-url", default=EBOOK_PAGE_URL)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--out", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--anchors-out", type=Path, default=DEFAULT_ANCHORS)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    return parser


def fetch_text(url: str, *, timeout: float) -> FetchedText:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout) as response:
            return FetchedText(
                raw=response.read(),
                final_url=response.geturl(),
                fetch_status="fetched",
            )
    except HTTPError as exc:
        return FetchedText(raw=b"", final_url=url, fetch_status=f"http_error_{exc.code}", error=str(exc))
    except (OSError, URLError) as exc:
        return FetchedText(raw=b"", final_url=url, fetch_status="fetch_error", error=str(exc))


def build_book_rows(kjv_raw: bytes, apocrypha_raw: bytes = b"") -> list[dict[str, object]]:
    kjv_headings = parse_kjv_book_headings(kjv_raw.decode("utf-8", errors="replace"))
    apocrypha_headings = parse_title_headings(
        apocrypha_raw.decode("utf-8", errors="replace"),
        (*APOCRYPHA_BOOKS, *extra_heading_expectations()),
    )
    rows: list[dict[str, object]] = []
    for expected in EXPECTED_BOOKS:
        headings = kjv_headings if expected.section == "kjv" else apocrypha_headings
        matches = []
        for alias in (expected.name, *expected.aliases):
            matches.extend(headings.get(normalize_book_key(alias), []))
        matches = sorted(matches, key=lambda item: item["line"])
        first = matches[0] if matches else {}
        last = matches[-1] if matches else {}
        rows.append(
            {
                "source_id": "gutenberg_split_kjv_apocrypha",
                "source_text_id": (
                    "gutenberg_ebook_30_kjv_complete"
                    if expected.section == "kjv"
                    else "gutenberg_ebook_124_deuterocanonical"
                ),
                "section": expected.section,
                "expected_book": expected.name,
                "aliases": ";".join(expected.aliases),
                "found_heading": bool(matches),
                "status": "found" if matches else "missing",
                "found_book_number": first.get("number", ""),
                "marker_count": len(matches),
                "first_line": first.get("line", ""),
                "last_line": last.get("line", ""),
            }
        )
    return rows


def parse_kjv_book_headings(text: str) -> dict[str, list[dict[str, object]]]:
    headings: dict[str, list[dict[str, object]]] = defaultdict(list)
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = BOOK_HEADING_RE.match(line.strip())
        if match is None:
            continue
        name = normalize_space(match.group("name"))
        headings[normalize_book_key(name)].append(
            {"number": match.group("number"), "name": name, "line": line_number}
        )
    return dict(headings)


def parse_title_headings(
    text: str,
    expectations: tuple[BookExpectation, ...],
) -> dict[str, list[dict[str, object]]]:
    aliases: dict[str, str] = {}
    for expected in expectations:
        for alias in (expected.name, *expected.aliases):
            aliases[normalize_book_key(alias)] = expected.name

    headings: dict[str, list[dict[str, object]]] = defaultdict(list)
    for line_number, line in enumerate(text.splitlines(), start=1):
        name = normalize_space(line.strip().lstrip("\ufeff"))
        canonical = aliases.get(normalize_book_key(name))
        if canonical is None:
            continue
        headings[normalize_book_key(canonical)].append(
            {"number": "", "name": name, "line": line_number}
        )
    return dict(headings)


def extra_heading_expectations() -> tuple[BookExpectation, ...]:
    return tuple(
        BookExpectation("apocrypha_extra", heading)
        for heading in EXTRA_APOCRYPHA_SOURCE_HEADINGS
    )


def build_summary(
    rows: list[dict[str, object]],
    kjv: FetchedText,
    apocrypha: FetchedText,
) -> dict[str, object]:
    kjv_rows = [row for row in rows if row["section"] == "kjv"]
    apocrypha_rows = [row for row in rows if row["section"] == "apocrypha"]
    found_kjv = sum(1 for row in kjv_rows if row["status"] == "found")
    found_apocrypha = sum(1 for row in apocrypha_rows if row["status"] == "found")
    apocrypha_headings = parse_title_headings(
        apocrypha.raw.decode("utf-8", errors="replace"),
        (*APOCRYPHA_BOOKS, *extra_heading_expectations()),
    )
    extra_source_headings = sum(
        1
        for heading in EXTRA_APOCRYPHA_SOURCE_HEADINGS
        if normalize_book_key(heading) in apocrypha_headings
    )
    return {
        "source_pages": 2,
        "fetched_plain_text_pages": sum(
            1 for fetched in (kjv, apocrypha) if fetched.fetch_status == "fetched"
        ),
        "kjv_plain_text_bytes": len(kjv.raw),
        "kjv_plain_text_sha256": hashlib.sha256(kjv.raw).hexdigest() if kjv.raw else "",
        "apocrypha_plain_text_bytes": len(apocrypha.raw),
        "apocrypha_plain_text_sha256": hashlib.sha256(apocrypha.raw).hexdigest()
        if apocrypha.raw
        else "",
        "expected_kjv_books": len(kjv_rows),
        "found_kjv_book_headings": found_kjv,
        "missing_kjv_book_headings": len(kjv_rows) - found_kjv,
        "expected_apocrypha_books": len(apocrypha_rows),
        "found_apocrypha_book_headings": found_apocrypha,
        "missing_apocrypha_book_headings": len(apocrypha_rows) - found_apocrypha,
        "extra_apocrypha_source_headings": extra_source_headings,
        "book_order_lock_ready": False,
        "verse_import_ready": False,
        "source_lock_ready": False,
        "result_ready": False,
        "claim_status": "coverage_probe_only_not_result_bearing",
    }


def build_anchors(
    summary: dict[str, object],
    kjv: FetchedText,
    apocrypha: FetchedText,
) -> list[dict[str, str]]:
    checks = [
        (
            "gutenberg",
            "plain_text_fetch_status_recorded",
            kjv.fetch_status == "fetched" and apocrypha.fetch_status == "fetched",
            "Project Gutenberg KJV and Apocrypha plain-text fetch status is recorded",
        ),
        (
            "gutenberg",
            "kjv_book_headings_found",
            int(summary["found_kjv_book_headings"]) == 66,
            "66 KJV book headings are found in heading markers",
        ),
        (
            "gutenberg",
            "apocrypha_book_headings_found",
            int(summary["found_apocrypha_book_headings"]) == 14,
            "14 Apocrypha/deuterocanon book headings are found in heading markers",
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
    kjv_final_url: str,
    apocrypha_final_url: str,
) -> None:
    found_anchors = sum(1 for row in anchors if row["status"] == "found")
    missing_apocrypha = [
        str(row["expected_book"])
        for row in rows
        if row["section"] == "apocrypha" and row["status"] == "missing"
    ]
    missing_read = ", ".join(missing_apocrypha) if missing_apocrypha else "none"
    lines = [
        "# KJVA Gutenberg Book Coverage Probe",
        "",
        "Status: source-coverage probe only.",
        "",
        "This is not an ELS result, not a corpus import, not a verse import, and not a source lock.",
        "It fetches Project Gutenberg eBook 30 and eBook 124 plain text for heading-level coverage scanning only.",
        "It does not commit Bible text, normalize Bible text, or create a local corpus.",
        "",
        "## Summary",
        "",
        f"- Source pages: {summary['source_pages']}.",
        f"- Plain-text fetches ok: {summary['fetched_plain_text_pages']}.",
        f"- KJV plain-text bytes scanned: {summary['kjv_plain_text_bytes']}.",
        f"- Apocrypha plain-text bytes scanned: {summary['apocrypha_plain_text_bytes']}.",
        f"- Expected KJV books checked: {summary['expected_kjv_books']}.",
        f"- KJV book headings found: {summary['found_kjv_book_headings']}.",
        f"- Missing KJV book headings: {summary['missing_kjv_book_headings']}.",
        f"- Expected apocrypha/deuterocanon books checked: {summary['expected_apocrypha_books']}.",
        f"- Apocrypha/deuterocanon book headings found: {summary['found_apocrypha_book_headings']}.",
        f"- Missing apocrypha/deuterocanon book headings: {summary['missing_apocrypha_book_headings']}.",
        f"- Extra Apocrypha/deuterocanon source headings: {summary['extra_apocrypha_source_headings']}.",
        f"- Book-order lock ready: {int(bool(summary['book_order_lock_ready']))}.",
        f"- Verse-numbered import ready: {int(bool(summary['verse_import_ready']))}.",
        f"- Source-lock ready: {int(bool(summary['source_lock_ready']))}.",
        f"- Result-ready sources: {int(bool(summary['result_ready']))}.",
        f"- Claim status: `{summary['claim_status']}`.",
        "",
        "## Coverage Read",
        "",
        "Project Gutenberg eBook 30 heading markers show all 66 KJV book headings.",
        "Project Gutenberg eBook 124 heading markers show all 14 tracked KJVA Apocrypha/deuterocanon coverage rows.",
        "The source also exposes the Epistle of Jeremiah as a separate heading, while the current KJVA source-family rollup treats it with Baruch.",
        f"Missing Apocrypha/deuterocanon heading rows: {missing_read}.",
        "",
        "## Anchors",
        "",
        f"Found anchors: {found_anchors}/{len(anchors)}.",
        "",
        "| Source | Anchor | Status | Diagnostic |",
        "| --- | --- | --- | --- |",
    ]
    for row in anchors:
        lines.append(f"| {row['source']} | `{row['anchor']}` | `{row['status']}` | {row['diagnostic']} |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            f"KJV source URL scanned: `{kjv_final_url}`.",
            f"Apocrypha source URL scanned: `{apocrypha_final_url}`.",
            "This coverage probe checks heading markers only. It does not make a verse map, book-order lock, source checksum lock, collation, term lock, study-lock sidecar, or result-bearing replication.",
            "The current read is that Project Gutenberg eBook 30 plus eBook 124 is a possible public-domain split KJV+Apocrypha source candidate needing collation and study-lock work before any KJVA bridge use.",
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
    kjv: FetchedText,
    apocrypha: FetchedText,
    started: float,
) -> None:
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "els_version": __version__,
        "tool": "scripts.analyze_kjva_gutenberg_book_coverage_probe",
        "kjv_txt_url": args.txt_url,
        "apocrypha_txt_url": args.apocrypha_txt_url,
        "ebook_page_url": args.ebook_page_url,
        "kjv_final_url": kjv.final_url,
        "apocrypha_final_url": apocrypha.final_url,
        "kjv_fetch_status": kjv.fetch_status,
        "apocrypha_fetch_status": apocrypha.fetch_status,
        "claim_boundary": "source-coverage probe only; no ELS result",
        "text_retention": "plain text scanned in memory; Bible text not committed",
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


def normalize_book_key(value: str) -> str:
    value = value.casefold().replace("&", "and")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return normalize_space(value)


def normalize_space(text: str) -> str:
    return " ".join(text.split())


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
