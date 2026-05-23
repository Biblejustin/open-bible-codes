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

from els.ebible_usfm import UsfmVerse, parse_usfm


DEFAULT_MANIFEST = Path("configs/supplemental_english_controls.csv")
DEFAULT_RAW_DIR = Path("data/raw/supplemental")
USER_AGENT = "Open Bible Codes supplemental source importer"
USFM_SUFFIXES = (".usfm", ".sfm", ".p.sfm")

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
            verses.extend(parse_usfm(scrub_structural_lines(raw)))
    return verses


def parse_akjv_text_zip(path: Path, source_path: str) -> list[UsfmVerse]:
    with zipfile.ZipFile(path) as archive:
        raw = archive.read(source_path).decode("utf-8-sig")
    return parse_akjv_text(raw)


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
