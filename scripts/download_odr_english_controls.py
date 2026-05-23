#!/usr/bin/env python3
"""Download Original Douay-Rheims English control sources."""

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

from els.ebible_usfm import UsfmVerse, parse_usfm


DEFAULT_MANIFEST = Path("configs/odr_english_controls.csv")
DEFAULT_RAW_DIR = Path("data/raw/odr")
USER_AGENT = "Open Bible Codes ODR source importer"
USFM_SUFFIXES = (".usfm", ".sfm")

CANONICAL_BOOK_ORDER = {
    book: index
    for index, book in enumerate(
        [
            "GEN",
            "EXO",
            "LEV",
            "NUM",
            "DEU",
            "JOS",
            "JDG",
            "RUT",
            "1SA",
            "2SA",
            "1KI",
            "2KI",
            "1CH",
            "2CH",
            "EZR",
            "NEH",
            "1ES",
            "2ES",
            "TOB",
            "JDT",
            "EST",
            "JOB",
            "PSA",
            "PRO",
            "ECC",
            "SNG",
            "WIS",
            "SIR",
            "ISA",
            "JER",
            "LAM",
            "BAR",
            "EZK",
            "DAN",
            "HOS",
            "JOL",
            "AMO",
            "OBA",
            "JON",
            "MIC",
            "NAH",
            "HAB",
            "ZEP",
            "HAG",
            "ZEC",
            "MAL",
            "1MA",
            "2MA",
            "MAN",
            "MAT",
            "MRK",
            "LUK",
            "JHN",
            "ACT",
            "ROM",
            "1CO",
            "2CO",
            "GAL",
            "EPH",
            "PHP",
            "COL",
            "1TH",
            "2TH",
            "1TI",
            "2TI",
            "TIT",
            "PHM",
            "HEB",
            "JAS",
            "1PE",
            "2PE",
            "1JN",
            "2JN",
            "3JN",
            "JUD",
            "REV",
        ],
        start=1,
    )
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
    parsed = parse_odr_archive(zip_path, row["source_path_prefix"])
    deduped, duplicate_refs = deduplicate_verses(parsed)
    verses = sort_verses_canonically(deduped)
    write_csv(csv_path, verses)
    write_source_manifest(
        manifest_path,
        row=row,
        zip_path=zip_path,
        csv_path=csv_path,
        verses=verses,
        parsed_verse_count=len(parsed),
        duplicate_ref_count=duplicate_refs,
    )
    return str(csv_path)


def download(url: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        out_path.write_bytes(response.read())


def parse_odr_archive(path: Path, source_path_prefix: str) -> list[UsfmVerse]:
    verses: list[UsfmVerse] = []
    wanted = f"/{source_path_prefix.strip('/')}/"
    with zipfile.ZipFile(path) as archive:
        names = [
            name
            for name in archive.namelist()
            if wanted in name and name.lower().endswith(USFM_SUFFIXES)
        ]
        for name in sorted(names, key=archive_sort_key):
            raw = archive.read(name).decode("utf-8-sig")
            verses.extend(parse_usfm(raw))
    return verses


def deduplicate_verses(verses: list[UsfmVerse]) -> tuple[list[UsfmVerse], int]:
    seen: dict[tuple[str, str, str], UsfmVerse] = {}
    duplicate_refs = 0
    for verse in verses:
        key = (verse.book, verse.chapter, verse.verse)
        existing = seen.get(key)
        if existing is None:
            seen[key] = verse
            continue
        duplicate_refs += 1
        if existing.text != verse.text and verse.text not in existing.text:
            seen[key] = UsfmVerse(
                book=existing.book,
                chapter=existing.chapter,
                verse=existing.verse,
                text=f"{existing.text} {verse.text}",
            )
    return list(seen.values()), duplicate_refs


def sort_verses_canonically(verses: list[UsfmVerse]) -> list[UsfmVerse]:
    return sorted(verses, key=verse_sort_key)


def verse_sort_key(verse: UsfmVerse) -> tuple[int, int, int, str, str]:
    return (
        CANONICAL_BOOK_ORDER.get(verse.book, 999),
        numeric_prefix(verse.chapter),
        numeric_prefix(verse.verse),
        verse.book,
        verse.verse,
    )


def numeric_prefix(value: str) -> int:
    match = re.match(r"\d+", value)
    return int(match.group(0)) if match else 999


def archive_sort_key(name: str) -> tuple[int, str]:
    book = Path(name).stem
    match = re.match(r"^(\d+)-", book)
    if match:
        return (int(match.group(1)), name)
    return (999, name)


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
    parsed_verse_count: int,
    duplicate_ref_count: int,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "source_id": row["source_id"],
        "label": row["label"],
        "source_name": row["name"],
        "source_url": row["source_url"],
        "details_url": row["details_url"],
        "license": row["license_label"],
        "downloaded_at": datetime.now(UTC).isoformat(),
        "zip_path": str(zip_path),
        "zip_sha256": sha256(zip_path),
        "zip_bytes": zip_path.stat().st_size,
        "csv_path": str(csv_path),
        "book_count": len({verse.book for verse in verses}),
        "verse_count": len(verses),
        "parsed_verse_count": parsed_verse_count,
        "duplicate_ref_count": duplicate_ref_count,
        "normalization": "USFM footnotes, crossrefs, and character markers removed; duplicate identical verse refs skipped; conflicting duplicate verse refs merged in source order.",
    }
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_run_manifest(args: argparse.Namespace, *, rows: list[str]) -> None:
    path = Path("reports/odr_english_controls/download.manifest.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "tool": "download_odr_english_controls",
        "created_utc": datetime.now(UTC).isoformat(),
        "manifest": str(args.manifest.resolve()),
        "downloaded_csvs": rows,
        "downloaded_count": len(rows),
    }
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
