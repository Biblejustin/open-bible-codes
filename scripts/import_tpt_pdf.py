#!/usr/bin/env python3
"""Import a local The Passion Translation PDF into a private CSV."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


DEFAULT_OUT = Path("data/private/english/tpt.csv")
DEFAULT_MANIFEST = Path("data/private/english/tpt.manifest.json")
VERSE_MARKER_RE = re.compile(r"\d+(?:[-\u2013]\d+)?")


@dataclass(frozen=True)
class BookInfo:
    code: str
    titles: tuple[str, ...]
    single_chapter: bool = False


@dataclass(frozen=True)
class LineItem:
    text: str
    kind: str


@dataclass(frozen=True)
class PageLine:
    page: int
    items: tuple[LineItem, ...]


@dataclass(frozen=True)
class VerseRow:
    ref: str
    book: str
    chapter: int
    verse: str
    text: str


BOOKS = [
    BookInfo("PSA", ("PSALMS",)),
    BookInfo("PRO", ("PROVERBS",)),
    BookInfo("SNG", ("SONG OF SONGS",)),
    BookInfo("MAT", ("MATTHEW",)),
    BookInfo("MRK", ("MARK",)),
    BookInfo("LUK", ("LUKE",)),
    BookInfo("JHN", ("JOHN",)),
    BookInfo("ACT", ("ACTS",)),
    BookInfo("ROM", ("ROMANS",)),
    BookInfo("1CO", ("1 CORINTHIANS",)),
    BookInfo("2CO", ("2 CORINTHIANS",)),
    BookInfo("GAL", ("GALATIANS",)),
    BookInfo("EPH", ("EPHESIANS",)),
    BookInfo("PHP", ("PHILIPPIANS",)),
    BookInfo("COL", ("COLOSSIANS",)),
    BookInfo("1TH", ("1 THESSALONIANS",)),
    BookInfo("2TH", ("2 THESSALONIANS",)),
    BookInfo("1TI", ("1 TIMOTHY",)),
    BookInfo("2TI", ("2 TIMOTHY",)),
    BookInfo("TIT", ("TITUS",)),
    BookInfo("PHM", ("PHILEMON",), single_chapter=True),
    BookInfo("HEB", ("HEBREWS",)),
    BookInfo("JAS", ("JAMES (JACOB)",)),
    BookInfo("1PE", ("1 PETER",)),
    BookInfo("2PE", ("2 PETER",)),
    BookInfo("1JN", ("1 JOHN",)),
    BookInfo("2JN", ("2 JOHN",), single_chapter=True),
    BookInfo("3JN", ("3 JOHN",), single_chapter=True),
    BookInfo("JUD", ("JUDE (JUDAH)",), single_chapter=True),
    BookInfo("REV", ("REVELATION",)),
]
BOOK_TITLES = {title for book in BOOKS for title in book.titles}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows, manifest = import_pdf(args.pdf)
    if args.dry_run:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0
    args.out.parent.mkdir(parents=True, exist_ok=True)
    write_rows(args.out, rows)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(args.out)
    print(args.manifest)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def import_pdf(path: Path) -> tuple[list[VerseRow], dict[str, object]]:
    xml_text = pdftohtml_xml(path)
    pages = build_page_lines(xml_text)
    rows, book_counts, book_pages, anomalies = parse_pages(pages)
    manifest = {
        "tool": "import_tpt_pdf",
        "created_utc": datetime.now(UTC).isoformat(),
        "source_pdf": str(path.resolve()),
        "source_pdf_sha256": sha256(path),
        "source_pdf_bytes": path.stat().st_size,
        "source_description": "Local The Passion Translation PDF, New Testament with Psalms, Proverbs, and Song of Songs.",
        "license": "copyrighted source; local private analysis only; do not commit extracted text",
        "rows": len(rows),
        "book_count": len(book_counts),
        "book_row_counts": book_counts,
        "book_start_pages": book_pages,
        "anomaly_count": len(anomalies),
        "anomalies": anomalies[:200],
        "normalization": "pdftohtml XML; blue footnote markers and small-font notes removed; whitespace collapsed; headings skipped where detectable.",
        "row_boundary_note": "Combined verse ranges and unnumbered opening paragraphs are preserved as a single row when the PDF supplies one marker.",
    }
    if anomalies:
        raise SystemExit(f"import anomalies found: {json.dumps(manifest, ensure_ascii=False, indent=2)}")
    return rows, manifest


def pdftohtml_xml(path: Path) -> str:
    try:
        result = subprocess.run(
            ["pdftohtml", "-xml", "-stdout", str(path)],
            check=True,
            text=True,
            capture_output=True,
        )
    except FileNotFoundError as exc:
        raise SystemExit("pdftohtml is required; install poppler") from exc
    return result.stdout


def build_page_lines(xml_text: str) -> list[PageLine]:
    root = ET.fromstring(xml_text)
    fonts = {
        item.attrib["id"]: {
            "size": int(item.attrib.get("size", "0")),
            "color": item.attrib.get("color", "").lower(),
        }
        for item in root.iter("fontspec")
    }
    output: list[PageLine] = []
    for page in root.findall("page"):
        page_number = int(page.attrib["number"])
        grouped: list[dict[str, object]] = []
        for text_node in page.findall("text"):
            item = line_item_from_text(text_node, fonts)
            if item is None:
                continue
            center = int(text_node.attrib["top"]) + int(text_node.attrib.get("height", "0")) / 2
            left = int(text_node.attrib["left"])
            for line in grouped:
                if abs(center - line["center"]) <= 6:
                    line["items"].append((left, item))
                    line["center"] = (line["center"] + center) / 2
                    break
            else:
                grouped.append({"center": center, "items": [(left, item)]})
        for line in sorted(grouped, key=lambda item: float(item["center"])):
            items = tuple(item for _, item in sorted(line["items"], key=lambda item: item[0]))
            output.append(PageLine(page_number, items))
    return output


def line_item_from_text(
    text_node: ET.Element,
    fonts: dict[str, dict[str, int | str]],
) -> LineItem | None:
    text = normalize_text("".join(text_node.itertext()))
    if not text:
        return None
    font = fonts.get(text_node.attrib.get("font", ""), {"size": 0, "color": ""})
    size = int(font["size"])
    color = str(font["color"])
    if color == "#0000ee" and size <= 11:
        return None
    if size >= 20 and re.fullmatch(r"\d+", text):
        return LineItem(text, "chapter")
    if size == 10 and color == "#000000" and VERSE_MARKER_RE.fullmatch(text):
        return LineItem(text.replace("\u2013", "-"), "verse")
    if size >= 12:
        return LineItem(text, "text")
    return None


def parse_pages(
    pages: list[PageLine],
) -> tuple[list[VerseRow], dict[str, int], dict[str, int], list[str]]:
    page_numbers = sorted({line.page for line in pages})
    page_map = {number: [] for number in page_numbers}
    for line in pages:
        page_map[line.page].append(line)
    starts, intros, anomalies = locate_books(page_map)
    rows: list[VerseRow] = []
    counts: dict[str, int] = {}
    start_pages: dict[str, int] = {}
    for index, book in enumerate(BOOKS):
        start = starts.get(book.code)
        if start is None:
            anomalies.append(f"{book.code}: no body start found")
            continue
        if book.code == "SNG":
            end = find_page_with_text(page_map, "THE NEW TESTAMENT", start=start) or next_book_intro(intros, index)
        elif book.code == "REV":
            end = find_page_with_text(page_map, "YOUR PERSONAL", start=start) or max(page_numbers) + 1
        else:
            end = next_book_intro(intros, index)
        segment = [
            line
            for page_number in range(start, end)
            for line in page_map.get(page_number, [])
        ]
        parsed = parse_book_lines(book, segment)
        rows.extend(parsed)
        counts[book.code] = len(parsed)
        start_pages[book.code] = start
    return rows, counts, start_pages, anomalies


def locate_books(
    page_map: dict[int, list[PageLine]],
) -> tuple[dict[str, int], dict[str, int], list[str]]:
    starts: dict[str, int] = {}
    intros: dict[str, int] = {}
    anomalies: list[str] = []
    for book in BOOKS:
        hits = []
        for page_number in sorted(page_map):
            lines = [line_text(line) for line in page_map[page_number]]
            for index, text in enumerate(lines):
                if text not in book.titles:
                    continue
                after = lines[index + 1 : index + 40]
                before = lines[index - 1] if index else ""
                hits.append((page_number, "AT A GLANCE" in after[:5], before, after[:2]))
                break
        intro = next((page for page, is_intro, _, _ in hits if is_intro), None)
        if intro is not None:
            intros[book.code] = intro
        for page, is_intro, before, after in hits:
            if is_intro or before.startswith("INTERPRETING") or (after and after[0] == "Introduction"):
                continue
            starts[book.code] = page
            break
        if book.code not in starts:
            anomalies.append(f"{book.code}: title hits did not identify body start: {hits[:3]}")
    return starts, intros, anomalies


def next_book_intro(intros: dict[str, int], index: int) -> int:
    if index + 1 >= len(BOOKS):
        return 10**9
    return intros[BOOKS[index + 1].code]


def find_page_with_text(
    page_map: dict[int, list[PageLine]],
    needle: str,
    *,
    start: int = 1,
) -> int | None:
    for page_number in sorted(page_map):
        if page_number < start:
            continue
        if any(needle in line_text(line) for line in page_map[page_number]):
            return page_number
    return None


def parse_book_lines(book: BookInfo, lines: list[PageLine]) -> list[VerseRow]:
    rows: list[VerseRow] = []
    chapter = 1 if book.single_chapter else 0
    verse: str | None = None
    parts: list[str] = []

    def flush() -> None:
        nonlocal parts, verse
        if verse is not None:
            text = normalize_text(" ".join(parts))
            if text:
                rows.append(
                    VerseRow(
                        ref=f"{book.code} {chapter}:{verse}",
                        book=book.code,
                        chapter=chapter,
                        verse=verse,
                        text=text,
                    )
                )
        parts = []

    for line in lines:
        text = line_text(line)
        if not text or text in BOOK_TITLES:
            continue
        has_marker = any(item.kind in {"chapter", "verse"} for item in line.items)
        if not has_marker and is_heading(text):
            continue
        if is_psalm_title_line(book, line):
            flush()
            chapter = int(line.items[0].text)
            verse = None
            continue
        if book.single_chapter and verse is None and not has_marker:
            verse = "1"
            parts = []
        for item in line.items:
            if item.kind == "chapter":
                flush()
                chapter = int(item.text)
                verse = "1"
                parts = []
            elif item.kind == "verse":
                flush()
                verse = item.text
                parts = []
            elif verse is not None:
                parts.append(item.text)
    flush()
    return rows


def is_psalm_title_line(book: BookInfo, line: PageLine) -> bool:
    if book.code != "PSA" or not line.items or line.items[0].kind != "chapter":
        return False
    rest = " ".join(item.text for item in line.items[1:] if item.kind == "text")
    letters = re.sub(r"[^A-Za-z]", "", rest)
    if not letters:
        return False
    return len(rest.split()) <= 10 and (
        sum(char.isupper() for char in letters) / len(letters)
    ) > 0.65


def is_heading(text: str) -> bool:
    if not text or text in BOOK_TITLES:
        return True
    if len(text) > 85 or re.search(r"[.!?;:]$", text):
        return False
    words = text.split()
    if len(words) > 8:
        return False
    lower_initials = sum(1 for word in words if word[:1].islower())
    return lower_initials <= max(1, len(words) // 4)


def line_text(line: PageLine) -> str:
    return normalize_text(" ".join(item.text for item in line.items))


def normalize_text(text: str) -> str:
    return " ".join(text.replace("\xa0", " ").split())


def write_rows(path: Path, rows: list[VerseRow]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["ref", "book", "chapter", "verse", "text"])
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "ref": row.ref,
                    "book": row.book,
                    "chapter": row.chapter,
                    "verse": row.verse,
                    "text": row.text,
                }
            )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
