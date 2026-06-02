#!/usr/bin/env python3
"""Import a Bolls static translation JSON/ZIP into a private CSV."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import UTC, datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


BOLLS_TRANSLATION_URL = "https://bolls.life/static/translations/{slug}.zip"
BOLLS_BOOKS_URL = "https://bolls.life/static/bolls/app/views/translations_books.json"
BOLLS_LANGUAGES_URL = "https://bolls.life/static/bolls/app/views/languages.json"
DEFAULT_SOURCE_DIR = Path("data/private/english/source_files")
DEFAULT_OUT_DIR = Path("data/private/english")
USER_AGENT = "Open Bible Codes private source importer"

CANONICAL_BOOK_CODES = {
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

BOOK_NAMES = {
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
    "1ES": "1 Esdras",
    "2ES": "2 Esdras",
    "TOB": "Tobit",
    "JDT": "Judith",
    "ESG": "Greek Esther",
    "WIS": "Wisdom",
    "SIR": "Sirach",
    "BAR": "Baruch",
    "LJE": "Letter of Jeremiah",
    "S3Y": "Song of the Three Young Men",
    "SUS": "Susanna",
    "BEL": "Bel and the Dragon",
    "1MA": "1 Maccabees",
    "2MA": "2 Maccabees",
    "3MA": "3 Maccabees",
    "4MA": "4 Maccabees",
    "MAN": "Prayer of Manasseh",
    "PS2": "Psalm 151",
}


@dataclass(frozen=True)
class VerseRow:
    ref: str
    book: str
    chapter: int
    verse: str
    text: str


class BibleTextHtmlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"sup", "s"}:
            self.skip_depth += 1
        elif tag.lower() in {"br", "p", "div"} and not self.skip_depth:
            self.parts.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"sup", "s"} and self.skip_depth:
            self.skip_depth -= 1
        elif tag.lower() in {"p", "div"} and not self.skip_depth:
            self.parts.append(" ")

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.parts.append(data)

    def handle_entityref(self, name: str) -> None:
        if not self.skip_depth:
            self.parts.append(unescape(f"&{name};"))

    def handle_charref(self, name: str) -> None:
        if not self.skip_depth:
            self.parts.append(unescape(f"&#{name};"))

    def text(self) -> str:
        return normalize_text("".join(self.parts))


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    slug = args.slug.upper()
    label = args.label.upper()
    source_file = args.source_file or DEFAULT_SOURCE_DIR / f"bolls_{slug.lower()}.zip"
    books_file = args.books_file or DEFAULT_SOURCE_DIR / "bolls_translations_books.json"
    languages_file = args.languages_file or DEFAULT_SOURCE_DIR / "bolls_languages.json"
    out = args.out or DEFAULT_OUT_DIR / f"{label.lower()}.csv"
    manifest_out = args.manifest or DEFAULT_OUT_DIR / f"{label.lower()}.manifest.json"
    source_url = args.source_url or BOLLS_TRANSLATION_URL.format(slug=slug)

    if not args.skip_download:
        ensure_download(source_url, source_file, force=args.force_download)
        ensure_download(args.books_url, books_file, force=args.force_download)
        ensure_download(args.languages_url, languages_file, force=args.force_download)

    rows, manifest = import_translation(
        slug=slug,
        label=label,
        source_file=source_file,
        source_url=source_url,
        books_file=books_file,
        books_url=args.books_url,
        languages_file=languages_file if languages_file.exists() else None,
        languages_url=args.languages_url,
    )
    if args.dry_run:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0

    out.parent.mkdir(parents=True, exist_ok=True)
    write_rows(out, rows)
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(out)
    print(manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", required=True, help="Bolls translation short_name")
    parser.add_argument("--label", required=True, help="Local/BibleGateway label")
    parser.add_argument("--source-url")
    parser.add_argument("--source-file", type=Path)
    parser.add_argument("--books-url", default=BOLLS_BOOKS_URL)
    parser.add_argument("--books-file", type=Path)
    parser.add_argument("--languages-url", default=BOLLS_LANGUAGES_URL)
    parser.add_argument("--languages-file", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--skip-download", action="store_true")
    parser.add_argument("--force-download", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def ensure_download(url: str, path: Path, *, force: bool = False) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request) as response, path.open("wb") as handle:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)


def import_translation(
    *,
    slug: str,
    label: str,
    source_file: Path,
    source_url: str,
    books_file: Path,
    books_url: str,
    languages_file: Path | None,
    languages_url: str,
) -> tuple[list[VerseRow], dict[str, Any]]:
    translation_rows = load_translation_rows(source_file)
    book_metadata = load_books_metadata(books_file, slug)
    language_metadata = load_language_metadata(languages_file, slug) if languages_file else {}
    book_id_to_code, metadata_book_order, book_name_by_code, book_anomalies = build_book_maps(book_metadata)
    rows, row_anomalies, skipped_empty_refs = build_rows(translation_rows, book_id_to_code, metadata_book_order)
    source_book_order = first_occurrence_book_order(rows)
    anomalies = book_anomalies + row_anomalies + validate_rows(
        rows,
        source_book_order,
        expected_books=metadata_book_order,
    )
    manifest = build_manifest(
        slug=slug,
        label=label,
        source_file=source_file,
        source_url=source_url,
        books_file=books_file,
        books_url=books_url,
        languages_file=languages_file,
        languages_url=languages_url,
        language_metadata=language_metadata,
        rows=rows,
        book_metadata=book_metadata,
        book_name_by_code=book_name_by_code,
        source_book_order=source_book_order,
        anomalies=anomalies,
        skipped_empty_refs=skipped_empty_refs,
    )
    if anomalies:
        raise SystemExit(f"import anomalies found: {json.dumps(manifest, ensure_ascii=False, indent=2)}")
    return rows, manifest


def load_translation_rows(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as archive:
            json_names = [name for name in archive.namelist() if name.lower().endswith(".json")]
            if len(json_names) != 1:
                raise SystemExit(f"{path}: expected one JSON member, found {len(json_names)}")
            with archive.open(json_names[0]) as handle:
                try:
                    payload = json.loads(handle.read().decode("utf-8-sig"))
                except json.JSONDecodeError as exc:
                    raise SystemExit(f"{path}: translation rows JSON is invalid: {exc}") from exc
                return validate_object_list(payload, path, "translation rows")
    with path.open("r", encoding="utf-8-sig") as handle:
        payload = json.load(handle)
    return validate_object_list(payload, path, "translation rows")


def load_books_metadata(path: Path, slug: str) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        all_books = json.load(handle)
    if not isinstance(all_books, dict):
        raise SystemExit(f"{path}: JSON root must be an object")
    if slug not in all_books:
        raise SystemExit(f"{path}: no book metadata for {slug}")
    return validate_object_list(all_books[slug], path, f"book metadata for {slug}")


def load_language_metadata(path: Path, slug: str) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        languages = json.load(handle)
    if not isinstance(languages, list):
        raise SystemExit(f"{path}: JSON root must be a list")
    for index, language in enumerate(languages):
        if not isinstance(language, dict):
            raise SystemExit(f"{path}: language row {index} must be an object")
        if language.get("language") != "English":
            continue
        translations = language.get("translations", [])
        if not isinstance(translations, list):
            raise SystemExit(f"{path}: language row {index} translations must be a list")
        for translation_index, translation in enumerate(translations):
            if not isinstance(translation, dict):
                raise SystemExit(
                    f"{path}: language row {index} translation row {translation_index} must be an object"
                )
            if translation.get("short_name") == slug:
                return dict(translation)
    return {}


def validate_object_list(payload: Any, path: Path, label: str) -> list[dict[str, Any]]:
    if not isinstance(payload, list):
        raise SystemExit(f"{path}: {label} JSON root must be a list")
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(payload):
        if not isinstance(row, dict):
            raise SystemExit(f"{path}: {label} row {index} must be an object")
        rows.append(row)
    return rows


def build_book_maps(
    book_metadata: list[dict[str, Any]],
) -> tuple[dict[int, str], dict[str, int], dict[str, str], list[str]]:
    book_id_to_code: dict[int, str] = {}
    book_order: dict[str, int] = {}
    book_name_by_code: dict[str, str] = {}
    anomalies: list[str] = []
    for index, book in enumerate(book_metadata):
        book_id = int(book["bookid"])
        raw_name = str(book.get("name", ""))
        code = book_code(book_id, raw_name)
        if not code:
            anomalies.append(f"unknown book id/name: {book_id} {raw_name}")
            continue
        if book_id in book_id_to_code and book_id_to_code[book_id] != code:
            anomalies.append(f"book id {book_id} mapped twice: {book_id_to_code[book_id]} vs {code}")
        book_id_to_code[book_id] = code
        book_order.setdefault(code, index)
        book_name_by_code.setdefault(code, BOOK_NAMES.get(code, raw_name))
    return book_id_to_code, book_order, book_name_by_code, anomalies


def book_code(book_id: int, raw_name: str) -> str:
    if 1 <= book_id <= 66:
        return CANONICAL_BOOK_CODES[book_id]
    normalized = normalize_book_name(raw_name)
    if normalized in APOCRYPHA_NAME_TO_CODE:
        return APOCRYPHA_NAME_TO_CODE[normalized]
    for prefix, code in APOCRYPHA_PREFIX_TO_CODE:
        if normalized.startswith(prefix):
            return code
    return ""


APOCRYPHA_NAME_TO_CODE = {
    "1 esdras": "1ES",
    "first book of esdras": "1ES",
    "2 esdras": "2ES",
    "second book of esdras": "2ES",
    "tobit": "TOB",
    "book of tobit": "TOB",
    "judith": "JDT",
    "book of judith": "JDT",
    "greek esther": "ESG",
    "esther": "ESG",
    "esther greek version": "ESG",
    "book of esther": "ESG",
    "wisdom": "WIS",
    "wisdom of solomon": "WIS",
    "the wisdom of solomon": "WIS",
    "sirach": "SIR",
    "sirach the wisdom of jesus son of sirach": "SIR",
    "baruch": "BAR",
    "book of baruch": "BAR",
    "the book of baruch": "BAR",
    "letter of jeremiah": "LJE",
    "the letter of jeremiah": "LJE",
    "epistle of jeremiah": "LJE",
    "prayer of azariah": "S3Y",
    "azariah": "S3Y",
    "prayer of azariah and song of the three young men": "S3Y",
    "the prayer of azariah and the song of the three young men": "S3Y",
    "prayer of azariah and song of the three hebrews": "S3Y",
    "susanna": "SUS",
    "book of susanna": "SUS",
    "the book of susanna": "SUS",
    "bel and the dragon": "BEL",
    "bel and dragon": "BEL",
    "1 maccabees": "1MA",
    "first book of the maccabees": "1MA",
    "2 maccabees": "2MA",
    "second book of the maccabees": "2MA",
    "3 maccabees": "3MA",
    "4 maccabees": "4MA",
    "prayer of manasseh": "MAN",
    "the prayer of manasseh": "MAN",
    "psalm 151": "PS2",
}

APOCRYPHA_PREFIX_TO_CODE = (
    ("sirach", "SIR"),
    ("the book of tobit", "TOB"),
    ("the book of judith", "JDT"),
    ("the book of esther", "ESG"),
    ("the first book of esdras", "1ES"),
    ("the second book of esdras", "2ES"),
    ("the first book of the maccabees", "1MA"),
    ("the second book of the maccabees", "2MA"),
)


def normalize_book_name(value: str) -> str:
    value = value.lower()
    value = re.sub(r"\([^)]*\)", " ", value)
    value = value.replace(":", " ")
    value = value.replace("-", " ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def build_rows(
    translation_rows: list[dict[str, Any]],
    book_id_to_code: dict[int, str],
    book_order: dict[str, int],
) -> tuple[list[VerseRow], list[str], list[str]]:
    rows: list[VerseRow] = []
    anomalies: list[str] = []
    skipped_empty_refs: list[str] = []
    for index, item in enumerate(translation_rows):
        try:
            book_id = int(item["book"])
            chapter = int(item["chapter"])
            verse = str(item["verse"])
        except (KeyError, TypeError, ValueError) as exc:
            anomalies.append(f"row {index}: invalid reference fields: {exc}")
            continue
        code = book_id_to_code.get(book_id)
        if not code:
            anomalies.append(f"row {index}: unknown book id {book_id}")
            continue
        text = clean_html_text(str(item.get("text", "")))
        if not text:
            skipped_empty_refs.append(f"{code} {chapter}:{verse}")
            continue
        if code not in book_order:
            anomalies.append(f"{code} {chapter}:{verse}: book missing from order")
            continue
        rows.append(VerseRow(f"{code} {chapter}:{verse}", code, chapter, verse, text))
    return rows, anomalies, skipped_empty_refs


def clean_html_text(value: str) -> str:
    parser = BibleTextHtmlParser()
    parser.feed(value)
    parser.close()
    return parser.text()


def first_occurrence_book_order(rows: list[VerseRow]) -> dict[str, int]:
    order: dict[str, int] = {}
    for row in rows:
        order.setdefault(row.book, len(order))
    return order


def validate_rows(
    rows: list[VerseRow],
    book_order: dict[str, int],
    *,
    expected_books: dict[str, int],
) -> list[str]:
    anomalies: list[str] = []
    seen: set[str] = set()
    previous: tuple[int, int, float, str] | None = None
    counts = {code: 0 for code in expected_books}
    for row in rows:
        if row.ref in seen:
            anomalies.append(f"{row.ref}: duplicate ref")
        seen.add(row.ref)
        counts[row.book] = counts.get(row.book, 0) + 1
        key = (book_order[row.book], row.chapter, verse_sort_value(row.verse), row.verse)
        if previous is not None and key <= previous:
            anomalies.append(f"{row.ref}: non-increasing order")
        previous = key
    missing_books = [code for code in expected_books if counts.get(code, 0) == 0]
    if missing_books:
        anomalies.append(f"missing books: {', '.join(missing_books)}")
    return anomalies


def verse_sort_value(value: str) -> float:
    match = re.match(r"(\d+)(?:[.:,-](\d+))?([A-Za-z]?)", value)
    if not match:
        return 10**9
    number = int(match.group(1))
    suffix = match.group(3) or ""
    return number + (ord(suffix.lower()) - 96) / 100 if suffix else float(number)


def build_manifest(
    *,
    slug: str,
    label: str,
    source_file: Path,
    source_url: str,
    books_file: Path,
    books_url: str,
    languages_file: Path | None,
    languages_url: str,
    language_metadata: dict[str, Any],
    rows: list[VerseRow],
    book_metadata: list[dict[str, Any]],
    book_name_by_code: dict[str, str],
    source_book_order: dict[str, int],
    anomalies: list[str],
    skipped_empty_refs: list[str],
) -> dict[str, Any]:
    ordered_codes = sorted(source_book_order, key=source_book_order.get)
    book_counts = {code: 0 for code in ordered_codes}
    chapter_sets: dict[str, set[int]] = {code: set() for code in book_name_by_code}
    total_letters = 0
    for row in rows:
        book_counts[row.book] = book_counts.get(row.book, 0) + 1
        chapter_sets.setdefault(row.book, set()).add(row.chapter)
        total_letters += sum(1 for char in row.text if char.isalpha())
    return {
        "tool": "import_bolls_translation",
        "created_utc": datetime.now(UTC).isoformat(),
        "label": label,
        "bolls_slug": slug,
        "bolls_full_name": language_metadata.get("full_name", ""),
        "bolls_updated": language_metadata.get("updated", ""),
        "source_file": str(source_file.resolve()),
        "source_file_sha256": sha256(source_file),
        "source_file_bytes": source_file.stat().st_size,
        "source_url": source_url,
        "books_file": str(books_file.resolve()),
        "books_file_sha256": sha256(books_file),
        "books_url": books_url,
        "languages_file": str(languages_file.resolve()) if languages_file else "",
        "languages_file_sha256": sha256(languages_file) if languages_file else "",
        "languages_url": languages_url,
        "license": "copyrighted and/or third-party source; local private analysis only; do not commit extracted text",
        "rows": len(rows),
        "book_count": sum(1 for count in book_counts.values() if count),
        "book_order": [code for code in ordered_codes if book_counts.get(code, 0)],
        "book_row_counts": {code: count for code, count in book_counts.items() if count},
        "book_chapter_counts": {
            code: len(chapters)
            for code, chapters in chapter_sets.items()
            if book_counts.get(code, 0)
        },
        "book_metadata_count": len(book_metadata),
        "letters": total_letters,
        "skipped_empty_text_refs": skipped_empty_refs,
        "skipped_empty_text_count": len(skipped_empty_refs),
        "anomaly_count": len(anomalies),
        "anomalies": anomalies[:200],
        "normalization": "Bolls static translation JSON/ZIP; verse text parsed as HTML; sup and Strong-number tag contents removed; comments excluded; whitespace collapsed.",
    }


def normalize_text(value: str) -> str:
    return " ".join(unescape(value).replace("\xa0", " ").split())


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
