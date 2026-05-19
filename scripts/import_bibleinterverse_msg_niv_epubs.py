#!/usr/bin/env python3
"""Import local BibleInterVerse Message/NIV EPUB bundle into private CSVs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import zipfile
from dataclasses import dataclass, field
from datetime import UTC, datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path


DEFAULT_OUT_DIR = Path("data/private/english")
BOOK_CODES = {
    1: "GEN",
    2: "EXO",
    3: "LEV",
    4: "NUM",
    5: "DEU",
    6: "JOS",
    7: "JDG",
    8: "RUT",
    9: "1SA",
    10: "2SA",
    11: "1KI",
    12: "2KI",
    13: "1CH",
    14: "2CH",
    15: "EZR",
    16: "NEH",
    17: "EST",
    18: "JOB",
    19: "PSA",
    20: "PRO",
    21: "ECC",
    22: "SNG",
    23: "ISA",
    24: "JER",
    25: "LAM",
    26: "EZK",
    27: "DAN",
    28: "HOS",
    29: "JOL",
    30: "AMO",
    31: "OBA",
    32: "JON",
    33: "MIC",
    34: "NAM",
    35: "HAB",
    36: "ZEP",
    37: "HAG",
    38: "ZEC",
    39: "MAL",
    40: "MAT",
    41: "MRK",
    42: "LUK",
    43: "JHN",
    44: "ACT",
    45: "ROM",
    46: "1CO",
    47: "2CO",
    48: "GAL",
    49: "EPH",
    50: "PHP",
    51: "COL",
    52: "1TH",
    53: "2TH",
    54: "1TI",
    55: "2TI",
    56: "TIT",
    57: "PHM",
    58: "HEB",
    59: "JAS",
    60: "1PE",
    61: "2PE",
    62: "1JN",
    63: "2JN",
    64: "3JN",
    65: "JUD",
    66: "REV",
}
BOOK_NAME_BY_CODE = {
    "GEN": "Genesis",
    "EXO": "Exodus",
    "LEV": "Leviticus",
    "NUM": "Numbers",
    "DEU": "Deuteronomy",
    "JOS": "Joshua",
    "JDG": "Judges",
    "RUT": "Ruth",
    "1SA": "1 Samuel",
    "2SA": "2 Samuel",
    "1KI": "1 Kings",
    "2KI": "2 Kings",
    "1CH": "1 Chronicles",
    "2CH": "2 Chronicles",
    "EZR": "Ezra",
    "NEH": "Nehemiah",
    "EST": "Esther",
    "JOB": "Job",
    "PSA": "Psalms",
    "PRO": "Proverbs",
    "ECC": "Ecclesiastes",
    "SNG": "Song of Solomon",
    "ISA": "Isaiah",
    "JER": "Jeremiah",
    "LAM": "Lamentations",
    "EZK": "Ezekiel",
    "DAN": "Daniel",
    "HOS": "Hosea",
    "JOL": "Joel",
    "AMO": "Amos",
    "OBA": "Obadiah",
    "JON": "Jonah",
    "MIC": "Micah",
    "NAM": "Nahum",
    "HAB": "Habakkuk",
    "ZEP": "Zephaniah",
    "HAG": "Haggai",
    "ZEC": "Zechariah",
    "MAL": "Malachi",
    "MAT": "Matthew",
    "MRK": "Mark",
    "LUK": "Luke",
    "JHN": "John",
    "ACT": "Acts",
    "ROM": "Romans",
    "1CO": "1 Corinthians",
    "2CO": "2 Corinthians",
    "GAL": "Galatians",
    "EPH": "Ephesians",
    "PHP": "Philippians",
    "COL": "Colossians",
    "1TH": "1 Thessalonians",
    "2TH": "2 Thessalonians",
    "1TI": "1 Timothy",
    "2TI": "2 Timothy",
    "TIT": "Titus",
    "PHM": "Philemon",
    "HEB": "Hebrews",
    "JAS": "James",
    "1PE": "1 Peter",
    "2PE": "2 Peter",
    "1JN": "1 John",
    "2JN": "2 John",
    "3JN": "3 John",
    "JUD": "Jude",
    "REV": "Revelation",
}
EPUB_NAME_RE = re.compile(r"BibInVs MN (?P<num>\d{2}) .+\.epub$")
CHAPTER_RE = re.compile(r"(?P<chapter>\d+)\s*$")
VERSE_RE = re.compile(r"^(?P<verse>\d+[A-Za-z]?)(?:\s+|$)(?P<text>.*)$")


@dataclass
class ChapterBlock:
    title: str
    chapter: int
    paragraphs: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class VerseRow:
    ref: str
    book: str
    chapter: int
    verse: str
    text: str


class InterverseHtmlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.chapters: list[ChapterBlock] = []
        self._tag: str | None = None
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"h1", "p"}:
            self._tag = tag
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._tag:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != self._tag:
            return
        text = normalize_text("".join(self._parts))
        if tag == "h1":
            chapter = parse_chapter_title(text)
            if chapter is not None:
                self.chapters.append(ChapterBlock(title=text, chapter=chapter))
        elif tag == "p" and self.chapters:
            self.chapters[-1].paragraphs.append(text)
        self._tag = None
        self._parts = []


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    msg_rows, niv_rows, manifest = import_bundle(args.zip)
    if args.dry_run:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_rows(args.out_dir / "msg.csv", msg_rows)
    write_rows(args.out_dir / "niv.csv", niv_rows)
    (args.out_dir / "bibleinterverse_msg_niv_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(args.out_dir / "msg.csv")
    print(args.out_dir / "niv.csv")
    print(args.out_dir / "bibleinterverse_msg_niv_manifest.json")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def import_bundle(path: Path) -> tuple[list[VerseRow], list[VerseRow], dict[str, object]]:
    msg_rows: list[VerseRow] = []
    niv_rows: list[VerseRow] = []
    anomalies: list[str] = []
    unpaired_rows: list[dict[str, str]] = []
    book_counts: dict[str, int] = {}
    with zipfile.ZipFile(path) as outer_zip:
        epub_names = sorted(
            (name for name in outer_zip.namelist() if name.endswith(".epub")),
            key=epub_sort_key,
        )
        for epub_name in epub_names:
            book_code = book_code_from_epub_name(epub_name)
            book_counts[book_code] = 0
            with zipfile.ZipFile(outer_zip.open(epub_name)) as epub_zip:
                html = read_epub_html(epub_zip)
            parsed_msg, parsed_niv, parsed_anomalies, parsed_unpaired = parse_book_html(
                book_code, html
            )
            msg_rows.extend(parsed_msg)
            niv_rows.extend(parsed_niv)
            anomalies.extend(f"{epub_name}: {item}" for item in parsed_anomalies)
            unpaired_rows.extend(
                {"source": epub_name, **item} for item in parsed_unpaired
            )
            book_counts[book_code] = len(parsed_msg)

    manifest = {
        "tool": "import_bibleinterverse_msg_niv_epubs",
        "created_utc": datetime.now(UTC).isoformat(),
        "source_zip": str(path.resolve()),
        "source_zip_sha256": sha256(path),
        "source_zip_bytes": path.stat().st_size,
        "source_description": "Local BibleInterVerse interversed Message/NIV 66-book EPUB bundle.",
        "license": "copyrighted sources; local private analysis only; do not commit extracted text",
        "msg_rows": len(msg_rows),
        "niv_rows": len(niv_rows),
        "book_count": len(book_counts),
        "book_row_counts": book_counts,
        "unpaired_row_count": len(unpaired_rows),
        "unpaired_rows": unpaired_rows[:200],
        "anomaly_count": len(anomalies),
        "anomalies": anomalies[:200],
        "normalization": "HTML paragraph text unescaped; whitespace collapsed; contiguous same-verse paragraphs split as MSG then NIV.",
    }
    if anomalies:
        raise SystemExit(f"import anomalies found: {json.dumps(manifest, ensure_ascii=False, indent=2)}")
    return msg_rows, niv_rows, manifest


def parse_book_html(
    book_code: str,
    html: str,
) -> tuple[list[VerseRow], list[VerseRow], list[str], list[dict[str, str]]]:
    parser = InterverseHtmlParser()
    parser.feed(html)
    msg_rows: list[VerseRow] = []
    niv_rows: list[VerseRow] = []
    anomalies: list[str] = []
    unpaired_rows: list[dict[str, str]] = []
    for chapter in parser.chapters:
        current_verse: str | None = None
        current_texts: list[str] = []
        for paragraph_index, paragraph in enumerate(chapter.paragraphs, start=1):
            if not paragraph or paragraph in {"MSG", "NIV"}:
                continue
            parsed = split_verse(paragraph)
            if parsed is None:
                anomalies.append(
                    f"{book_code} {chapter.chapter}: cannot parse paragraph {paragraph_index}"
                )
                continue
            verse, text = parsed
            if current_verse is not None and verse != current_verse:
                append_verse_group(
                    book_code,
                    chapter.chapter,
                    current_verse,
                    current_texts,
                    msg_rows,
                    niv_rows,
                    anomalies,
                    unpaired_rows,
                )
                current_texts = []
            current_verse = verse
            current_texts.append(text)
        if current_verse is not None:
            append_verse_group(
                book_code,
                chapter.chapter,
                current_verse,
                current_texts,
                msg_rows,
                niv_rows,
                anomalies,
                unpaired_rows,
            )
    return msg_rows, niv_rows, anomalies, unpaired_rows


def append_verse_group(
    book_code: str,
    chapter: int,
    verse: str,
    texts: list[str],
    msg_rows: list[VerseRow],
    niv_rows: list[VerseRow],
    anomalies: list[str],
    unpaired_rows: list[dict[str, str]],
) -> None:
    ref = f"{book_code} {chapter}:{verse}"
    if len(texts) > 2:
        anomalies.append(f"{ref}: expected one or two version paragraphs, found {len(texts)}")
        return
    msg_rows.append(VerseRow(ref, book_code, chapter, verse, texts[0]))
    if len(texts) == 2:
        niv_rows.append(VerseRow(ref, book_code, chapter, verse, texts[1]))
    else:
        unpaired_rows.append({"ref": ref, "assumed_version": "MSG"})


def read_epub_html(epub_zip: zipfile.ZipFile) -> str:
    names = epub_zip.namelist()
    html_names = sorted(
        name
        for name in names
        if re.fullmatch(r"index(?:_split_\d+)?\.html", Path(name).name)
    )
    if not html_names:
        raise SystemExit(f"EPUB has no index html files: {names[:20]}")
    return "\n".join(epub_zip.read(name).decode("utf-8") for name in html_names)


def epub_sort_key(name: str) -> int:
    return int(EPUB_NAME_RE.search(name).group("num"))


def book_code_from_epub_name(name: str) -> str:
    match = EPUB_NAME_RE.search(name)
    if not match:
        raise SystemExit(f"unexpected EPUB name: {name}")
    number = int(match.group("num"))
    try:
        return BOOK_CODES[number]
    except KeyError as exc:
        raise SystemExit(f"unsupported book number in {name}") from exc


def parse_chapter_title(text: str) -> int | None:
    match = CHAPTER_RE.search(text)
    if not match:
        return None
    return int(match.group("chapter"))


def split_verse(text: str) -> tuple[str, str] | None:
    match = VERSE_RE.match(text)
    if not match:
        return None
    return match.group("verse"), match.group("text").strip()


def normalize_text(text: str) -> str:
    return " ".join(unescape(text).replace("\xa0", " ").split())


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
