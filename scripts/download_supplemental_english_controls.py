#!/usr/bin/env python3
"""Download supplemental open English control sources."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import urllib.request
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from xml.etree import ElementTree

from els.ebible_usfm import UsfmVerse, parse_usfm


DEFAULT_MANIFEST = Path("configs/supplemental_english_controls.csv")
DEFAULT_RAW_DIR = Path("data/raw/supplemental")
USER_AGENT = "Open Bible Codes supplemental source importer"
USFM_SUFFIXES = (".usfm", ".sfm", ".p.sfm", ".ufsm")

AKJV_BOOK_CODES = {
    "Gen": "GEN",
    "Ex": "EXO",
    "Lev": "LEV",
    "Num": "NUM",
    "Dt": "DEU",
    "Josh": "JOS",
    "Jud": "JDG",
    "Ruth": "RUT",
    "1Sam": "1SA",
    "2Sam": "2SA",
    "1Ki": "1KI",
    "2Ki": "2KI",
    "1Chr": "1CH",
    "2Chr": "2CH",
    "Ezra": "EZR",
    "Neh": "NEH",
    "Est": "EST",
    "Job": "JOB",
    "Ps": "PSA",
    "Prov": "PRO",
    "Eccl": "ECC",
    "Song": "SNG",
    "Isa": "ISA",
    "Jer": "JER",
    "Lam": "LAM",
    "Ezek": "EZK",
    "Dan": "DAN",
    "Hos": "HOS",
    "Joel": "JOL",
    "Amos": "AMO",
    "Obad": "OBA",
    "Jon": "JON",
    "Mic": "MIC",
    "Nah": "NAM",
    "Hab": "HAB",
    "Zeph": "ZEP",
    "Hag": "HAG",
    "Zech": "ZEC",
    "Mal": "MAL",
    "Mt": "MAT",
    "Mk": "MRK",
    "Lk": "LUK",
    "Jn": "JHN",
    "Acts": "ACT",
    "Rom": "ROM",
    "1Cor": "1CO",
    "2Cor": "2CO",
    "Gal": "GAL",
    "Eph": "EPH",
    "Phil": "PHP",
    "Col": "COL",
    "1Th": "1TH",
    "2Th": "2TH",
    "1Tim": "1TI",
    "2Tim": "2TI",
    "Ti": "TIT",
    "Phile": "PHM",
    "Heb": "HEB",
    "Jas": "JAS",
    "1Pet": "1PE",
    "2Pet": "2PE",
    "1Jn": "1JN",
    "2Jn": "2JN",
    "3Jn": "3JN",
    "Jude": "JUD",
    "Rev": "REV",
}

STRUCTURAL_MARKERS = (
    "\\b",
    "\\b3",
    "\\cd",
    "\\cl",
    "\\h",
    "\\h0",
    "\\h1",
    "\\ide",
    "\\iex",
    "\\im",
    "\\imt",
    "\\ip",
    "\\is",
    "\\mt",
    "\\mt1",
    "\\mt2",
    "\\mt3",
    "\\mt4",
    "\\mt7",
    "\\mte",
    "\\mte9",
    "\\rem",
    "\\toc",
    "\\toc1",
    "\\toc2",
    "\\toc3",
)

FILENAME_BOOK_CODES = {
    "GENESIS": "GEN",
    "EXODUS": "EXO",
    "LEVITICUS": "LEV",
    "NUMBERS": "NUM",
    "DEUTERONOMY": "DEU",
    "JOSHUA": "JOS",
    "JUDGES": "JDG",
    "RUTH": "RUT",
    "1SAMUEL": "1SA",
    "2SAMUEL": "2SA",
    "1KINGS": "1KI",
    "2KINGS": "2KI",
    "1CHRONICLES": "1CH",
    "2CHRONICLES": "2CH",
    "EZRA": "EZR",
    "NEHEMIAH": "NEH",
    "ESTHER": "EST",
    "JOB": "JOB",
    "PSALM": "PSA",
    "PSALMS": "PSA",
    "PROVERBS": "PRO",
    "ECCLESIASTES": "ECC",
    "SONG": "SNG",
    "SONGOFSONGS": "SNG",
    "ISAIAH": "ISA",
    "JEREMIAH": "JER",
    "LAMENTATIONS": "LAM",
    "EZEKIEL": "EZK",
    "DANIEL": "DAN",
    "HOSEA": "HOS",
    "JOEL": "JOL",
    "AMOS": "AMO",
    "OBADIAH": "OBA",
    "JONAH": "JON",
    "MICAH": "MIC",
    "NAHUM": "NAM",
    "HABAKKUK": "HAB",
    "ZEPHANIAH": "ZEP",
    "HAGGAI": "HAG",
    "ZECHARIAH": "ZEC",
    "MALACHI": "MAL",
    "MATTHEW": "MAT",
    "MARK": "MRK",
    "LUKE": "LUK",
    "JOHN": "JHN",
    "ACTS": "ACT",
    "ROMANS": "ROM",
    "1CORINTHIANS": "1CO",
    "2CORINTHIANS": "2CO",
    "GALATIANS": "GAL",
    "EPHESIANS": "EPH",
    "PHILIPPIANS": "PHP",
    "COLOSSIANS": "COL",
    "1THESSALONIANS": "1TH",
    "2THESSALONIANS": "2TH",
    "1TIMOTHY": "1TI",
    "2TIMOTHY": "2TI",
    "TITUS": "TIT",
    "PHILEMON": "PHM",
    "HEBREWS": "HEB",
    "JAMES": "JAS",
    "1PETER": "1PE",
    "2PETER": "2PE",
    "1JOHN": "1JN",
    "2JOHN": "2JN",
    "3JOHN": "3JN",
    "JUDE": "JUD",
    "REVELATION": "REV",
}

ZEFANIA_BOOK_CODES = {
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

ZEFANIA_BOOK_SHORT_CODES = {
    "GEN": "GEN",
    "EXO": "EXO",
    "LEV": "LEV",
    "NUM": "NUM",
    "DEU": "DEU",
    "JOSH": "JOS",
    "JUDG": "JDG",
    "RUTH": "RUT",
    "1SA": "1SA",
    "2SA": "2SA",
    "1KI": "1KI",
    "2KI": "2KI",
    "1CHR": "1CH",
    "2CHR": "2CH",
    "EZRA": "EZR",
    "NEH": "NEH",
    "ESTH": "EST",
    "EST": "EST",
    "JOB": "JOB",
    "PS": "PSA",
    "PROV": "PRO",
    "ECCL": "ECC",
    "SOL": "SNG",
    "SONG": "SNG",
    "ISA": "ISA",
    "JER": "JER",
    "LAM": "LAM",
    "EZ": "EZK",
    "EZEK": "EZK",
    "DAN": "DAN",
    "HOS": "HOS",
    "JOEL": "JOL",
    "AMOS": "AMO",
    "OBAD": "OBA",
    "JONAH": "JON",
    "JON": "JON",
    "MIC": "MIC",
    "NAH": "NAM",
    "HAB": "HAB",
    "ZEPH": "ZEP",
    "HAG": "HAG",
    "ZECH": "ZEC",
    "MAL": "MAL",
    "MATT": "MAT",
    "MAT": "MAT",
    "MARK": "MRK",
    "MRK": "MRK",
    "LUKE": "LUK",
    "LUK": "LUK",
    "JOHN": "JHN",
    "JHN": "JHN",
    "ACTS": "ACT",
    "ROM": "ROM",
    "1COR": "1CO",
    "2COR": "2CO",
    "GAL": "GAL",
    "EPH": "EPH",
    "PHI": "PHP",
    "PHIL": "PHP",
    "COL": "COL",
    "1THESS": "1TH",
    "2THESS": "2TH",
    "1TI": "1TI",
    "2TI": "2TI",
    "TIT": "TIT",
    "PHLM": "PHM",
    "PHILE": "PHM",
    "PHILEMON": "PHM",
    "HEB": "HEB",
    "JAS": "JAS",
    "1PET": "1PE",
    "2PET": "2PE",
    "1JOHN": "1JN",
    "2JOHN": "2JN",
    "3JOHN": "3JN",
    "JUDE": "JUD",
    "REV": "REV",
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = read_rows(args.manifest)
    selected = select_rows(rows, args.only)
    if args.dry_run:
        for row in selected:
            print(f"{row['label']} {row['source_id']} {row['source_url']}")
        print(f"selected={len(selected)}")
        return 0

    completed = []
    for row in selected:
        completed.append(download_row(row, args))
    write_run_manifest(args, rows=completed)
    for path in completed:
        print(path)
    print(f"downloaded={len(completed)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        help="Restrict to a label or source_id; may be repeated.",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Reuse existing zip and CSV files when both are present.",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def select_rows(rows: list[dict[str, str]], only: list[str]) -> list[dict[str, str]]:
    wanted = {item.strip() for item in only if item.strip()}
    if not wanted:
        return rows
    selected = [
        row
        for row in rows
        if row["label"] in wanted or row["source_id"] in wanted
    ]
    missing = sorted(wanted - {row["label"] for row in selected} - {row["source_id"] for row in selected})
    if missing:
        raise SystemExit(f"unknown source filters: {', '.join(missing)}")
    return selected


def download_row(row: dict[str, str], args: argparse.Namespace) -> str:
    source_id = row["source_id"]
    zip_path = args.raw_dir / f"{source_id}.zip"
    csv_path = Path(row["local_csv"])
    manifest_path = csv_path.with_suffix(".manifest.json")
    if args.skip_existing and zip_path.exists() and csv_path.exists():
        return str(csv_path)

    download(row["source_url"], zip_path)
    verses = parse_archive(zip_path, row)
    write_csv(csv_path, verses)
    write_source_manifest(manifest_path, row=row, zip_path=zip_path, csv_path=csv_path, verses=verses)
    return str(csv_path)


def download(url: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        out_path.write_bytes(response.read())


def parse_archive(path: Path, row: dict[str, str]) -> list[UsfmVerse]:
    source_format = row["source_format"]
    if source_format == "crosswire_gitlab_usfm_zip":
        return parse_usfm_archive(path, row["source_path_prefix"])
    if source_format == "biblecorps_usfm_zip":
        return parse_usfm_archive(path, row["source_path_prefix"])
    if source_format == "openenglishbible_usfm_zip":
        return parse_usfm_archive(path, row["source_path_prefix"])
    if source_format == "zefania_xml_zip":
        return parse_zefania_xml_zip(path)
    if source_format == "akjv_text_zip":
        return parse_akjv_text_zip(path, row["source_path_prefix"])
    raise SystemExit(f"{row['label']}: unknown source_format {source_format}")


def parse_usfm_archive(path: Path, source_path_prefix: str) -> list[UsfmVerse]:
    verses: list[UsfmVerse] = []
    clean_prefix = source_path_prefix.strip("/")
    wanted = f"/{clean_prefix}/" if clean_prefix else ""
    with zipfile.ZipFile(path) as archive:
        names = [
            name
            for name in archive.namelist()
            if (not wanted or wanted in name)
            and "/intro/" not in name
            and name.lower().endswith(USFM_SUFFIXES)
        ]
        for name in sorted(names, key=archive_sort_key):
            raw = archive.read(name).decode("utf-8-sig")
            verses.extend(parse_usfm(scrub_structural_lines(raw), default_book=book_from_filename(name)))
    return verses


def parse_akjv_text_zip(path: Path, source_path: str) -> list[UsfmVerse]:
    with zipfile.ZipFile(path) as archive:
        raw = archive.read(source_path).decode("utf-8-sig")
    return parse_akjv_text(raw)


def parse_zefania_xml_zip(path: Path) -> list[UsfmVerse]:
    with zipfile.ZipFile(path) as archive:
        names = [name for name in archive.namelist() if name.lower().endswith(".xml")]
        if len(names) != 1:
            raise ValueError(f"expected one Zefania XML file in {path}, found {len(names)}")
        root = ElementTree.fromstring(archive.read(names[0]))
    verses: list[UsfmVerse] = []
    for book in root.findall("BIBLEBOOK"):
        book_code = zefania_book_code(book)
        if not book_code:
            continue
        for chapter in book.findall("CHAPTER"):
            chapter_number = chapter.attrib["cnumber"]
            for verse in chapter.findall("VERS"):
                text = zefania_verse_text(verse)
                if text:
                    verses.append(
                        UsfmVerse(
                            book=book_code,
                            chapter=chapter_number,
                            verse=verse.attrib["vnumber"],
                            text=text,
                        )
                    )
    return verses


def zefania_book_code(book: ElementTree.Element) -> str | None:
    number_code = ZEFANIA_BOOK_CODES.get(int(book.attrib["bnumber"]))
    short_codes = [
        short_code
        for attr in ("bsname", "bname")
        if (short_code := zefania_book_short_code(book.attrib.get(attr, "")))
    ]
    if number_code and number_code in short_codes:
        return number_code
    unique_short_codes = sorted(set(short_codes))
    if len(unique_short_codes) == 1 and unique_short_codes[0] != number_code:
        return unique_short_codes[0]
    if not number_code and unique_short_codes:
        return unique_short_codes[0]
    return number_code


def zefania_book_short_code(value: str) -> str | None:
    key = re.sub(r"[^0-9A-Za-z]", "", value).upper()
    return ZEFANIA_BOOK_SHORT_CODES.get(key)


def zefania_verse_text(element: ElementTree.Element) -> str:
    parts: list[str] = []
    append_zefania_text(element, parts)
    return " ".join("".join(parts).split())


def append_zefania_text(element: ElementTree.Element, parts: list[str]) -> None:
    if element.tag.upper() == "NOTE":
        return
    if element.text:
        parts.append(element.text)
    for child in element:
        append_zefania_text(child, parts)
        if child.tail:
            parts.append(child.tail)


def parse_akjv_text(raw: str) -> list[UsfmVerse]:
    book = ""
    verses: list[UsfmVerse] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        heading = re.match(r"^\[([^\]]+)\]\s*", line)
        if heading:
            abbr = heading.group(1)
            try:
                book = AKJV_BOOK_CODES[abbr]
            except KeyError as exc:
                raise ValueError(f"unknown AKJV book abbreviation {abbr}") from exc
            continue
        verse = re.match(r"^(\d+):(\d+[A-Za-z]?)\s+(.+)$", line)
        if verse and book:
            verses.append(
                UsfmVerse(
                    book=book,
                    chapter=verse.group(1),
                    verse=verse.group(2),
                    text=" ".join(verse.group(3).split()),
                )
            )
    return verses


def scrub_structural_lines(raw: str) -> str:
    kept = []
    for line in raw.splitlines():
        stripped = line.lstrip()
        if structural_line_without_verse(stripped):
            continue
        kept.append(line)
    return "\n".join(kept)


def structural_line_without_verse(stripped: str) -> bool:
    if "\\v " in stripped:
        return False
    return any(stripped == marker or stripped.startswith(f"{marker} ") for marker in STRUCTURAL_MARKERS)


def archive_sort_key(name: str) -> tuple[int, str]:
    match = re.match(r"^(\d+)-", Path(name).name)
    if match:
        return (int(match.group(1)), name)
    return (999, name)


def book_from_filename(name: str) -> str:
    stem = Path(name).stem
    match = re.match(r"^\d+-(.+)$", stem)
    if not match:
        return ""
    raw_book = match.group(1)
    compact = re.sub(r"[^0-9A-Za-z]", "", raw_book).upper()
    if compact in FILENAME_BOOK_CODES:
        return FILENAME_BOOK_CODES[compact]
    code_match = re.match(r"^([1-3]?[A-Z]{2,3})$", compact)
    if code_match:
        return code_match.group(1)
    return ""


def write_csv(path: Path, verses: list[UsfmVerse]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["ref", "book", "chapter", "verse", "text"],
        )
        writer.writeheader()
        for verse in verses:
            writer.writerow(
                {
                    "ref": verse.ref,
                    "book": verse.book,
                    "chapter": verse.chapter,
                    "verse": verse.verse,
                    "text": verse.text,
                }
            )


def write_source_manifest(
    path: Path,
    *,
    row: dict[str, str],
    zip_path: Path,
    csv_path: Path,
    verses: list[UsfmVerse],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "label": row["label"],
        "source_id": row["source_id"],
        "source_url": row["source_url"],
        "details_url": row["details_url"],
        "license_label": row["license_label"],
        "source_path_prefix": row["source_path_prefix"],
        "source_format": row["source_format"],
        "raw_path": str(zip_path),
        "raw_sha256": sha256(zip_path),
        "csv_path": str(csv_path),
        "csv_sha256": sha256(csv_path),
        "verse_count": len(verses),
        "book_count": len({verse.book for verse in verses}),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_run_manifest(args: argparse.Namespace, *, rows: list[str]) -> None:
    path = args.raw_dir / "download_manifest.json"
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "manifest": str(args.manifest),
        "rows": rows,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
