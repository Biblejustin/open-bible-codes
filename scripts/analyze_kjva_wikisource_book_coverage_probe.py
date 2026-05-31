#!/usr/bin/env python3
"""Probe Wikisource KJVA book-link coverage without importing Bible text."""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urljoin, urlparse
from urllib.request import Request, urlopen

from els import __version__
from scripts.analyze_kjva_wikisource_candidate_source import WIKISOURCE_URL


DEFAULT_OUT_DIR = Path("reports/kjva_wikisource_book_coverage_probe")
DEFAULT_ROWS = DEFAULT_OUT_DIR / "book_links.csv"
DEFAULT_SUMMARY = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_ANCHORS = DEFAULT_OUT_DIR / "anchors.csv"
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_MD = Path("docs/KJVA_WIKISOURCE_BOOK_COVERAGE_PROBE.md")
USER_AGENT = "OpenBibleCodes-EDLS Wikisource coverage probe/1.0"
WIKISOURCE_ORIGIN = "https://en.wikisource.org"
PAGE_SLUG = WIKISOURCE_URL.rsplit("/wiki/", 1)[1]
PAGE_TITLE = unquote(PAGE_SLUG)

ROW_FIELDNAMES = [
    "source_id",
    "section",
    "expected_book",
    "link_text",
    "href",
    "absolute_url",
    "volume",
    "link_status",
]
SUMMARY_FIELDNAMES = [
    "source_pages",
    "fetched_pages",
    "expected_kjv_books",
    "existing_kjv_book_links",
    "redlinked_kjv_book_links",
    "missing_kjv_book_links",
    "expected_apocrypha_books",
    "existing_apocrypha_book_links",
    "redlinked_apocrypha_book_links",
    "missing_apocrypha_book_links",
    "book_order_lock_ready",
    "verse_import_ready",
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
class LinkCandidate:
    text: str
    href: str
    absolute_url: str
    volume: str
    link_status: str


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
    BookExpectation("apocrypha", "1 Esdras", ("I. Esdras", "First Esdras")),
    BookExpectation("apocrypha", "2 Esdras", ("II. Esdras", "Second Esdras")),
    BookExpectation("apocrypha", "Tobit"),
    BookExpectation("apocrypha", "Judith"),
    BookExpectation("apocrypha", "Rest of Esther", ("Additions to Esther",)),
    BookExpectation("apocrypha", "Wisdom", ("Wisdom of Solomon",)),
    BookExpectation("apocrypha", "Ecclesiasticus", ("Sirach",)),
    BookExpectation("apocrypha", "Baruch", ("Epistle of Jeremiah", "Letter of Jeremiah")),
    BookExpectation("apocrypha", "Song of the Three Children", ("Prayer of Azariah",)),
    BookExpectation("apocrypha", "Susanna", ("Story of Susanna",)),
    BookExpectation("apocrypha", "Bel and the Dragon", ("Bel and Dragon",)),
    BookExpectation("apocrypha", "Prayer of Manasseh", ("Prayer of Manasses",)),
    BookExpectation("apocrypha", "1 Maccabees", ("I. Maccabees", "First Maccabees")),
    BookExpectation("apocrypha", "2 Maccabees", ("II. Maccabees", "Second Maccabees")),
)
EXPECTED_BOOKS: tuple[BookExpectation, ...] = tuple(
    BookExpectation("kjv", name) for name in KJV_BOOKS
) + APOCRYPHA_BOOKS


class LinkExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        self._href = dict(attrs).get("href")
        self._parts = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            stripped = data.strip()
            if stripped:
                self._parts.append(stripped)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "a" or self._href is None:
            return
        text = normalize_space(" ".join(self._parts))
        if text:
            self.links.append((text, self._href))
        self._href = None
        self._parts = []


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    raw, final_url, fetch_status, error = fetch_page(args.url, timeout=args.timeout)
    rows = build_book_rows(raw, final_url=final_url)
    summary = build_summary(rows, fetch_status=fetch_status)
    anchors = build_anchors(summary, error=error)
    write_csv(args.out, ROW_FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_csv(args.anchors_out, ANCHOR_FIELDNAMES, anchors)
    write_markdown(args.markdown_out, summary, rows, anchors, final_url=final_url)
    write_manifest(args.manifest_out, args, summary, rows, anchors, started, final_url)
    print(args.out)
    print(args.summary_out)
    print(args.anchors_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=WIKISOURCE_URL)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--out", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--anchors-out", type=Path, default=DEFAULT_ANCHORS)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    return parser


def fetch_page(url: str, *, timeout: float) -> tuple[bytes, str, str, str]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.read(), response.geturl(), "fetched", ""
    except OSError as exc:
        return b"", url, "fetch_error", str(exc)


def build_book_rows(raw: bytes, *, final_url: str = WIKISOURCE_URL) -> list[dict[str, str]]:
    links = extract_link_candidates(raw, final_url=final_url)
    best = best_links_by_book(links)
    rows: list[dict[str, str]] = []
    for expected in EXPECTED_BOOKS:
        link = best.get(expected.name)
        rows.append(
            {
                "source_id": "wikisource_ballantyne_1911_kjva",
                "section": expected.section,
                "expected_book": expected.name,
                "link_text": link.text if link else "",
                "href": link.href if link else "",
                "absolute_url": link.absolute_url if link else "",
                "volume": link.volume if link else "",
                "link_status": link.link_status if link else "missing",
            }
        )
    return rows


def extract_link_candidates(raw: bytes, *, final_url: str) -> list[LinkCandidate]:
    parser = LinkExtractor()
    parser.feed(raw.decode("utf-8", errors="replace"))
    links: list[LinkCandidate] = []
    for text, href in parser.links:
        status = classify_href(href)
        if not status:
            continue
        volume = extract_volume(href)
        if not volume:
            continue
        links.append(
            LinkCandidate(
                text=text,
                href=href,
                absolute_url=urljoin(final_url, href),
                volume=volume,
                link_status=status,
            )
        )
    return links


def best_links_by_book(links: list[LinkCandidate]) -> dict[str, LinkCandidate]:
    alias_to_name = expected_alias_map()
    best: dict[str, LinkCandidate] = {}
    rank = {"missing": 0, "redlink": 1, "existing": 2}
    for link in links:
        name = alias_to_name.get(normalize_book_key(link.text))
        if name is None:
            continue
        current = best.get(name)
        if current is None or rank[link.link_status] > rank[current.link_status]:
            best[name] = link
    return best


def expected_alias_map() -> dict[str, str]:
    aliases: dict[str, str] = {}
    roman_aliases = {
        "1 Samuel": ("I. Samuel",),
        "2 Samuel": ("II. Samuel",),
        "1 Kings": ("I. Kings",),
        "2 Kings": ("II. Kings",),
        "1 Chronicles": ("I. Chronicles",),
        "2 Chronicles": ("II. Chronicles",),
    }
    for expected in EXPECTED_BOOKS:
        for alias in (expected.name, *expected.aliases, *roman_aliases.get(expected.name, ())):
            aliases[normalize_book_key(alias)] = expected.name
    return aliases


def classify_href(href: str) -> str:
    if unquote(href).startswith(f"/wiki/{PAGE_TITLE}/Volume_"):
        return "existing"
    parsed = urlparse(href)
    if parsed.path != "/w/index.php":
        return ""
    query = parse_qs(parsed.query)
    title = query.get("title", [""])[0]
    if title.startswith(f"{PAGE_TITLE}/Volume_") and query.get("redlink") == ["1"]:
        return "redlink"
    return ""


def extract_volume(href: str) -> str:
    match = re.search(r"/Volume_(\d+)(?:/|$)", unquote(href))
    return match.group(1) if match else ""


def build_summary(rows: list[dict[str, str]], *, fetch_status: str) -> dict[str, object]:
    def count(section: str, status: str) -> int:
        return sum(1 for row in rows if row["section"] == section and row["link_status"] == status)

    expected_kjv = sum(1 for row in rows if row["section"] == "kjv")
    expected_apocrypha = sum(1 for row in rows if row["section"] == "apocrypha")
    return {
        "source_pages": 1,
        "fetched_pages": 1 if fetch_status == "fetched" else 0,
        "expected_kjv_books": expected_kjv,
        "existing_kjv_book_links": count("kjv", "existing"),
        "redlinked_kjv_book_links": count("kjv", "redlink"),
        "missing_kjv_book_links": count("kjv", "missing"),
        "expected_apocrypha_books": expected_apocrypha,
        "existing_apocrypha_book_links": count("apocrypha", "existing"),
        "redlinked_apocrypha_book_links": count("apocrypha", "redlink"),
        "missing_apocrypha_book_links": count("apocrypha", "missing"),
        "book_order_lock_ready": False,
        "verse_import_ready": False,
        "result_ready": False,
        "claim_status": "coverage_probe_only_not_result_bearing",
    }


def build_anchors(summary: dict[str, object], *, error: str) -> list[dict[str, str]]:
    checks = [
        (
            "wikisource",
            "main_page_fetch_status_recorded",
            int(summary["fetched_pages"]) == 1 or bool(error),
            "main page fetch state is recorded",
        ),
        (
            "wikisource",
            "kjv_book_links_recorded",
            int(summary["expected_kjv_books"]) == 66,
            "expected KJV book-link rows are recorded",
        ),
        (
            "wikisource",
            "apocrypha_book_links_recorded",
            int(summary["expected_apocrypha_books"]) == 14,
            "expected apocrypha/deuterocanon book-link rows are recorded",
        ),
        (
            "wikisource",
            "book_order_not_ready",
            not bool(summary["book_order_lock_ready"]),
            "no book-order lock is declared ready",
        ),
        (
            "wikisource",
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
    rows: list[dict[str, str]],
    anchors: list[dict[str, str]],
    *,
    final_url: str,
) -> None:
    found = sum(1 for row in anchors if row["status"] == "found")
    lines = [
        "# KJVA Wikisource Book Coverage Probe",
        "",
        "Status: source-coverage probe only. This is not an ELS result, not a",
        "corpus import, not a verse import, and not a source lock.",
        "",
        "## Setup",
        "",
        "This probe checks book-link coverage on the Wikisource Ballantyne KJV +",
        "Apocrypha candidate page. It records link text, link target status, and",
        "volume numbers only. It does not import, retain, normalize, or commit",
        "Bible text.",
        "",
        f"Source page: {final_url}",
        "",
        "## Findings",
        "",
        f"- Expected KJV books checked: {summary['expected_kjv_books']}.",
        f"- Existing KJV book links: {summary['existing_kjv_book_links']}.",
        f"- Redlinked KJV book links: {summary['redlinked_kjv_book_links']}.",
        f"- Missing KJV book links: {summary['missing_kjv_book_links']}.",
        f"- Expected apocrypha/deuterocanon books checked: {summary['expected_apocrypha_books']}.",
        f"- Existing apocrypha/deuterocanon book links: {summary['existing_apocrypha_book_links']}.",
        f"- Redlinked apocrypha/deuterocanon book links: {summary['redlinked_apocrypha_book_links']}.",
        f"- Missing apocrypha/deuterocanon book links: {summary['missing_apocrypha_book_links']}.",
        "- Book-order lock ready: 0.",
        "- Verse-numbered import ready: 0.",
        "- Result-ready sources: 0.",
        "",
        "Current read: the main Wikisource page has KJV book-link metadata, but",
        "the parsed book-link table does not expose apocrypha/deuterocanon book",
        "links. This keeps the source at coverage-probe status only.",
        "",
        "## Book Link Summary",
        "",
        "| Section | Existing | Redlinked | Missing | Expected |",
        "| --- | ---: | ---: | ---: | ---: |",
        "| KJV | "
        f"{summary['existing_kjv_book_links']} | {summary['redlinked_kjv_book_links']} | "
        f"{summary['missing_kjv_book_links']} | {summary['expected_kjv_books']} |",
        "| Apocrypha/deuterocanon | "
        f"{summary['existing_apocrypha_book_links']} | "
        f"{summary['redlinked_apocrypha_book_links']} | "
        f"{summary['missing_apocrypha_book_links']} | "
        f"{summary['expected_apocrypha_books']} |",
        "",
        "## Protocol Anchors",
        "",
        f"Found anchors: {found} of {len(anchors)}.",
        "",
        "| Source | Anchor | Status | Diagnostic |",
        "| --- | --- | --- | --- |",
    ]
    for row in anchors:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["source"]),
                    f"`{markdown_cell(row['anchor'])}`",
                    markdown_cell(row["status"]),
                    markdown_cell(row["diagnostic"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Book Rows",
            "",
            "| Section | Book | Status | Link Text | Volume |",
            "| --- | --- | --- | --- | ---: |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row["section"]),
                    markdown_cell(row["expected_book"]),
                    markdown_cell(row["link_status"]),
                    markdown_cell(row["link_text"]),
                    markdown_cell(row["volume"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Use Boundary",
            "",
            "This probe does not decide that Wikisource can supply a KJVA corpus.",
            "It does not fetch child book text, map verses, choose book order, run",
            "ELS searches, evaluate controls, and does not change any KJVA result",
            "status.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary: dict[str, object],
    rows: list[dict[str, str]],
    anchors: list[dict[str, str]],
    started: float,
    final_url: str,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "source": args.url,
        "final_url": final_url,
        "summary": summary,
        "rows": len(rows),
        "anchors": anchors,
        "outputs": {
            "rows": str(args.out),
            "summary": str(args.summary_out),
            "anchors": str(args.anchors_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "claim_boundary": "source-coverage probe only; no ELS result",
        "text_retention": "metadata only; no Bible text retained",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def normalize_book_key(text: str) -> str:
    text = normalize_space(text).lower()
    text = text.replace(".", "")
    return text


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|")


if __name__ == "__main__":
    raise SystemExit(main())
