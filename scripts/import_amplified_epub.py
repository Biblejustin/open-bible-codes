#!/usr/bin/env python3
"""Import a local Amplified Bible EPUB into a private CSV."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import zipfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from xml.etree import ElementTree as ET


DEFAULT_OUT = Path("data/private/english/ampc.csv")
DEFAULT_MANIFEST = Path("data/private/english/ampc.manifest.json")
EMPTY_BRACKET_RE = re.compile(r"\[\s*[,.;: ]*\]")
SPACE_BEFORE_PUNCT_RE = re.compile(r"\s+([,.;:])")


BOOKS = [
    ("GEN", "Genesis"),
    ("EXO", "Exodus"),
    ("LEV", "Leviticus"),
    ("NUM", "Numbers"),
    ("DEU", "Deuteronomy"),
    ("JOS", "Joshua"),
    ("JDG", "Judges"),
    ("RUT", "Ruth"),
    ("1SA", "1 Samuel"),
    ("2SA", "2 Samuel"),
    ("1KI", "1 Kings"),
    ("2KI", "2 Kings"),
    ("1CH", "1 Chronicles"),
    ("2CH", "2 Chronicles"),
    ("EZR", "Ezra"),
    ("NEH", "Nehemiah"),
    ("EST", "Esther"),
    ("JOB", "Job"),
    ("PSA", "Psalms"),
    ("PRO", "Proverbs"),
    ("ECC", "Ecclesiastes"),
    ("SNG", "Song of Solomon"),
    ("ISA", "Isaiah"),
    ("JER", "Jeremiah"),
    ("LAM", "Lamentations"),
    ("EZK", "Ezekiel"),
    ("DAN", "Daniel"),
    ("HOS", "Hosea"),
    ("JOL", "Joel"),
    ("AMO", "Amos"),
    ("OBA", "Obadiah"),
    ("JON", "Jonah"),
    ("MIC", "Micah"),
    ("NAM", "Nahum"),
    ("HAB", "Habakkuk"),
    ("ZEP", "Zephaniah"),
    ("HAG", "Haggai"),
    ("ZEC", "Zechariah"),
    ("MAL", "Malachi"),
    ("MAT", "Matthew"),
    ("MRK", "Mark"),
    ("LUK", "Luke"),
    ("JHN", "John"),
    ("ACT", "Acts"),
    ("ROM", "Romans"),
    ("1CO", "1 Corinthians"),
    ("2CO", "2 Corinthians"),
    ("GAL", "Galatians"),
    ("EPH", "Ephesians"),
    ("PHP", "Philippians"),
    ("COL", "Colossians"),
    ("1TH", "1 Thessalonians"),
    ("2TH", "2 Thessalonians"),
    ("1TI", "1 Timothy"),
    ("2TI", "2 Timothy"),
    ("TIT", "Titus"),
    ("PHM", "Philemon"),
    ("HEB", "Hebrews"),
    ("JAS", "James"),
    ("1PE", "1 Peter"),
    ("2PE", "2 Peter"),
    ("1JN", "1 John"),
    ("2JN", "2 John"),
    ("3JN", "3 John"),
    ("JUD", "Jude"),
    ("REV", "Revelation"),
]
BOOK_NAME_TO_CODE = {name: code for code, name in BOOKS}
BOOK_NAME_TO_CODE["Psalm"] = "PSA"
BOOK_INDEX = {code: index for index, (code, _name) in enumerate(BOOKS)}
BOOK_HEADER_RE = re.compile(
    r"^(?P<book>"
    + "|".join(re.escape(name) for name in sorted(BOOK_NAME_TO_CODE, key=len, reverse=True))
    + r")\s+(?P<chapter>\d+)$"
)


@dataclass(frozen=True)
class VerseRow:
    ref: str
    book: str
    chapter: int
    verse: str
    text: str


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows, manifest = import_epub(args.epub, label=args.label, source_url=args.source_url)
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
    parser.add_argument("--epub", type=Path, required=True)
    parser.add_argument("--label", default="AMPC")
    parser.add_argument("--source-url", default="")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def import_epub(
    path: Path,
    *,
    label: str,
    source_url: str = "",
) -> tuple[list[VerseRow], dict[str, object]]:
    rows: list[VerseRow] = []
    anomalies: list[str] = []
    parsed_files: list[str] = []
    with zipfile.ZipFile(path) as archive:
        for name in sorted(archive.namelist(), key=epub_name_sort_key):
            if not re.fullmatch(r"index_split_\d+\.html", Path(name).name):
                continue
            parsed, parsed_anomalies = parse_chapter_html(archive.read(name).decode("utf-8"))
            if parsed:
                parsed_files.append(name)
            rows.extend(parsed)
            anomalies.extend(f"{name}: {item}" for item in parsed_anomalies)
    anomalies.extend(validate_rows(rows))
    manifest = build_manifest(path, label, source_url, rows, parsed_files, anomalies)
    if anomalies:
        raise SystemExit(f"import anomalies found: {json.dumps(manifest, ensure_ascii=False, indent=2)}")
    return rows, manifest


def parse_chapter_html(html: str) -> tuple[list[VerseRow], list[str]]:
    try:
        root = ET.fromstring(html)
    except ET.ParseError as exc:
        return [], [f"XML parse failed: {exc}"]

    current_book: str | None = None
    current_chapter: int | None = None
    rows: list[VerseRow] = []
    anomalies: list[str] = []
    for paragraph in root.iter():
        if local_name(paragraph.tag) != "p":
            continue
        full_text = normalize_text(collect_text(paragraph))
        header = parse_book_chapter(full_text)
        if header is not None:
            current_book, current_chapter = header
            continue
        verse = first_sup_verse(paragraph)
        if verse is None:
            continue
        if current_book is None or current_chapter is None:
            anomalies.append(f"verse {verse}: missing chapter header")
            continue
        text = clean_verse_text(collect_text(paragraph, skip_links=True, skip_sup=True))
        if not text:
            anomalies.append(f"{current_book} {current_chapter}:{verse}: empty text")
            continue
        rows.append(
            VerseRow(
                ref=f"{current_book} {current_chapter}:{verse}",
                book=current_book,
                chapter=current_chapter,
                verse=verse,
                text=text,
            )
        )
    return rows, anomalies


def collect_text(
    element: ET.Element,
    *,
    skip_links: bool = False,
    skip_sup: bool = False,
) -> str:
    parts: list[str] = []

    def walk(node: ET.Element) -> None:
        tag = local_name(node.tag)
        if (skip_links and tag == "a") or (skip_sup and tag == "sup"):
            return
        if node.text:
            parts.append(node.text)
        for child in node:
            walk(child)
            if child.tail:
                parts.append(child.tail)

    walk(element)
    return "".join(parts)


def parse_book_chapter(text: str) -> tuple[str, int] | None:
    text = re.sub(r"\s*\[\d+\]\s*$", "", text)
    match = BOOK_HEADER_RE.match(text)
    if not match:
        return None
    return BOOK_NAME_TO_CODE[match.group("book")], int(match.group("chapter"))


def first_sup_verse(element: ET.Element) -> str | None:
    for child in element.iter():
        if local_name(child.tag) != "sup":
            continue
        text = normalize_text(collect_text(child))
        if re.fullmatch(r"\d+[A-Za-z]?", text):
            return text
    return None


def clean_verse_text(text: str) -> str:
    text = EMPTY_BRACKET_RE.sub("", text)
    text = SPACE_BEFORE_PUNCT_RE.sub(r"\1", text)
    return normalize_text(text)


def validate_rows(rows: list[VerseRow]) -> list[str]:
    anomalies: list[str] = []
    seen: set[str] = set()
    previous_key: tuple[int, int, int] | None = None
    counts = {code: 0 for code, _name in BOOKS}
    for row in rows:
        if row.ref in seen:
            anomalies.append(f"{row.ref}: duplicate ref")
        seen.add(row.ref)
        counts[row.book] += 1
        order_key = (BOOK_INDEX[row.book], row.chapter, int(re.match(r"\d+", row.verse).group(0)))
        if previous_key is not None and order_key <= previous_key:
            anomalies.append(f"{row.ref}: non-increasing order")
        previous_key = order_key
    missing = [code for code, count in counts.items() if count == 0]
    if missing:
        anomalies.append(f"missing books: {', '.join(missing)}")
    return anomalies


def build_manifest(
    path: Path,
    label: str,
    source_url: str,
    rows: list[VerseRow],
    parsed_files: list[str],
    anomalies: list[str],
) -> dict[str, object]:
    counts = {code: 0 for code, _name in BOOKS}
    for row in rows:
        counts[row.book] += 1
    return {
        "tool": "import_amplified_epub",
        "created_utc": datetime.now(UTC).isoformat(),
        "label": label,
        "source_epub": str(path.resolve()),
        "source_epub_sha256": sha256(path),
        "source_epub_bytes": path.stat().st_size,
        "source_url": source_url,
        "source_description": f"Local {label} EPUB with one chapter per XHTML file.",
        "license": "copyrighted source; local private analysis only; do not commit extracted text",
        "rows": len(rows),
        "book_count": sum(1 for count in counts.values() if count),
        "book_row_counts": {code: count for code, count in counts.items() if count},
        "parsed_file_count": len(parsed_files),
        "parsed_files": parsed_files[:200],
        "anomaly_count": len(anomalies),
        "anomalies": anomalies[:200],
        "normalization": "EPUB XHTML paragraphs parsed by chapter header and verse superscript; linked cross-reference text removed; whitespace collapsed.",
    }


def epub_name_sort_key(name: str) -> tuple[int, str]:
    match = re.search(r"index_split_(\d+)\.html$", name)
    if match:
        return (int(match.group(1)), name)
    return (10**9, name)


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


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
