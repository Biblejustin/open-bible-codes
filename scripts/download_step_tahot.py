#!/usr/bin/env python3
"""Download STEP Bible TAHOT files and convert selected Hebrew rows to CSV."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import urllib.parse
import urllib.request
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path


SOURCE_ID = "step_tahot"
SOURCE_NAME = "STEP Bible TAHOT selected Hebrew OT"
SOURCE_REPO_URL = "https://github.com/STEPBible/STEPBible-Data"
SOURCE_DIR_URL = (
    "https://github.com/STEPBible/STEPBible-Data/tree/master/"
    "Translators%20Amalgamated%20OT%2BNT"
)
RAW_BASE_URL = (
    "https://raw.githubusercontent.com/STEPBible/STEPBible-Data/master/"
    "Translators%20Amalgamated%20OT%2BNT"
)
LICENSE_LABEL = "CC BY 4.0; credit STEP Bible linked to www.STEPBible.org"
RAW_DIR = Path("data/raw/step/tahot")
OUT_CSV = Path("data/processed/step/tahot.csv")
OUT_MANIFEST = Path("data/processed/step/tahot.manifest.json")
USER_AGENT = "Open Bible Codes source importer"

SOURCE_FILES = (
    "TAHOT Gen-Deu - Translators Amalgamated Hebrew OT - STEPBible.org CC BY.txt",
    "TAHOT Jos-Est - Translators Amalgamated Hebrew OT - STEPBible.org CC BY.txt",
    "TAHOT Job-Sng - Translators Amalgamated Hebrew OT - STEPBible.org CC BY.txt",
    "TAHOT Isa-Mal - Translators Amalgamated Hebrew OT - STEPBible.org CC BY.txt",
)

ROW_RE = re.compile(
    r"^(?P<book>(?:[1-3][A-Za-z]{2}|[A-Za-z]{3}))\."
    r"(?P<chapter>\d+)\."
    r"(?P<verse>\d+)"
    r"(?:\([^)]*\))?"
    r"#(?P<word>\d+)=(?P<text_type>[^\t]+)$"
)

STEP_BOOKS = {
    "Gen": "Gen",
    "Exo": "Exod",
    "Lev": "Lev",
    "Num": "Num",
    "Deu": "Deut",
    "Jos": "Josh",
    "Jdg": "Judg",
    "Rut": "Ruth",
    "1Sa": "1Sam",
    "2Sa": "2Sam",
    "1Ki": "1Kgs",
    "2Ki": "2Kgs",
    "1Ch": "1Chr",
    "2Ch": "2Chr",
    "Ezr": "Ezra",
    "Neh": "Neh",
    "Est": "Esth",
    "Job": "Job",
    "Psa": "Ps",
    "Pro": "Prov",
    "Ecc": "Eccl",
    "Sng": "Song",
    "Isa": "Isa",
    "Jer": "Jer",
    "Lam": "Lam",
    "Ezk": "Ezek",
    "Dan": "Dan",
    "Hos": "Hos",
    "Jol": "Joel",
    "Amo": "Amos",
    "Oba": "Obad",
    "Jon": "Jonah",
    "Mic": "Mic",
    "Nam": "Nah",
    "Hab": "Hab",
    "Zep": "Zeph",
    "Hag": "Hag",
    "Zec": "Zech",
    "Mal": "Mal",
}


@dataclass
class TahotVerse:
    book: str
    chapter: str
    verse: str
    words: list[str] = field(default_factory=list)
    source_types: list[str] = field(default_factory=list)

    @property
    def ref(self) -> str:
        return f"{self.book} {self.chapter}:{self.verse}"

    @property
    def text(self) -> str:
        return " ".join(self.words)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    raw_dir = Path(args.raw_dir)
    csv_path = Path(args.csv_out)
    manifest_path = Path(args.manifest_out)

    if (
        not args.refresh
        and csv_path.exists()
        and manifest_path.exists()
        and all((raw_dir / filename).exists() for filename in SOURCE_FILES)
    ):
        print("cached")
        return 0

    if not args.skip_download:
        downloaded = download_sources(raw_dir)
    else:
        downloaded = [raw_dir / filename for filename in SOURCE_FILES]
        missing = [path for path in downloaded if not path.exists()]
        if missing:
            raise FileNotFoundError(f"missing raw TAHOT files: {missing}")

    verses = parse_tahot_files(downloaded)
    write_csv(csv_path, verses)
    write_manifest(
        manifest_path,
        raw_files=downloaded,
        csv_path=csv_path,
        verses=verses,
    )
    print(csv_path)
    print(manifest_path)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Reuse existing raw TAHOT files.",
    )
    parser.add_argument("--raw-dir", type=Path, default=RAW_DIR)
    parser.add_argument("--csv-out", type=Path, default=OUT_CSV)
    parser.add_argument("--manifest-out", type=Path, default=OUT_MANIFEST)
    return parser


def download_sources(raw_dir: Path) -> list[Path]:
    raw_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for filename in SOURCE_FILES:
        path = raw_dir / filename
        download_file(tahot_raw_url(filename), path)
        paths.append(path)
    return paths


def tahot_raw_url(filename: str) -> str:
    return f"{RAW_BASE_URL}/{urllib.parse.quote(filename)}"


def download_file(url: str, out_path: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        write_bytes_if_changed(out_path, response.read())


def parse_tahot_files(paths: list[Path]) -> list[TahotVerse]:
    verses: "OrderedDict[tuple[str, str, str], TahotVerse]" = OrderedDict()
    for path in paths:
        parse_tahot_file(path, verses)
    return list(verses.values())


def parse_tahot_file(
    path: Path,
    verses: "OrderedDict[tuple[str, str, str], TahotVerse]",
) -> None:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        for row in reader:
            if len(row) < 2:
                continue
            first = row[0].strip()
            match = ROW_RE.match(first)
            if not match:
                continue
            hebrew = clean_hebrew_cell(row[1])
            if not hebrew:
                continue
            book = STEP_BOOKS.get(match.group("book"))
            if book is None:
                raise ValueError(f"{path}: unsupported STEP book {match.group('book')}")
            chapter = normalize_number(match.group("chapter"))
            verse = normalize_number(match.group("verse"))
            key = (book, chapter, verse)
            record = verses.setdefault(
                key,
                TahotVerse(book=book, chapter=chapter, verse=verse),
            )
            record.words.append(hebrew)
            record.source_types.append(match.group("text_type"))


def clean_hebrew_cell(value: str) -> str:
    """Return lexical Hebrew field content without STEP punctuation suffixes."""
    return value.strip().split("\\", 1)[0].strip()


def normalize_number(value: str) -> str:
    return str(int(value))


def write_csv(path: Path, verses: list[TahotVerse]) -> None:
    handle = io.StringIO(newline="")
    writer = csv.DictWriter(
        handle,
        fieldnames=[
            "ref",
            "book",
            "chapter",
            "verse",
            "text",
            "word_count",
            "source_types",
        ],
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
                "word_count": len(verse.words),
                "source_types": " ".join(verse.source_types),
            }
        )
    write_text_if_changed(path, handle.getvalue())


def write_manifest(
    path: Path,
    *,
    raw_files: list[Path],
    csv_path: Path,
    verses: list[TahotVerse],
) -> None:
    raw_file_entries = [
        {
            "path": str(file),
            "source_url": tahot_raw_url(file.name),
            "bytes": file.stat().st_size,
            "sha256": sha256_file(file),
        }
        for file in raw_files
    ]
    csv_sha256 = sha256_file(csv_path)
    downloaded_at = stable_downloaded_at(
        path,
        raw_file_entries=raw_file_entries,
        csv_sha256=csv_sha256,
        verse_count=len(verses),
    )
    manifest = {
        "source_id": SOURCE_ID,
        "source_name": SOURCE_NAME,
        "source_repo_url": SOURCE_REPO_URL,
        "source_dir_url": SOURCE_DIR_URL,
        "license": LICENSE_LABEL,
        "downloaded_at": downloaded_at,
        "raw_files": raw_file_entries,
        "csv_path": str(csv_path),
        "csv_sha256": csv_sha256,
        "book_count": len({verse.book for verse in verses}),
        "verse_count": len(verses),
        "normalization": (
            "TAHOT selected Hebrew word rows grouped by English reference; "
            "STEP punctuation suffixes after backslash separators are removed "
            "so paragraph markers do not enter the ELS stream; "
            "vowels/cantillation are preserved in CSV and stripped by corpus "
            "normalization at load time."
        ),
        "text_policy": (
            "Selected STEP/Tyndale translator stream. This follows the TAHOT "
            "row text, which may include Qere, restored text, and LXX-based "
            "Hebrew additions as documented in the upstream header. Do not "
            "treat as a pure Leningrad ketiv stream."
        ),
    }
    write_text_if_changed(path, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")


def stable_downloaded_at(
    path: Path,
    *,
    raw_file_entries: list[dict[str, object]],
    csv_sha256: str,
    verse_count: int,
) -> str:
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            existing = {}
        if (
            existing.get("raw_files") == raw_file_entries
            and existing.get("csv_sha256") == csv_sha256
            and existing.get("verse_count") == verse_count
            and isinstance(existing.get("downloaded_at"), str)
        ):
            return str(existing["downloaded_at"])
    return datetime.now(UTC).isoformat()


def write_text_if_changed(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = text.encode("utf-8")
    if path.exists() and path.read_bytes() == content:
        return
    path.write_bytes(content)


def write_bytes_if_changed(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == content:
        return
    path.write_bytes(content)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
