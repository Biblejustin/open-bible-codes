#!/usr/bin/env python3
"""Download Open Translation Bible English control sources."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els.ebible_usfm import UsfmVerse


DEFAULT_MANIFEST = Path("configs/otb_english_controls.csv")
DEFAULT_RAW_DIR = Path("data/raw/otb")
REPO = "OpenTranslationBible/open-bible"
DEFAULT_REF = "main"
USER_AGENT = "Open Bible Codes OTB source importer"

BOOK_NAME_CODES = {
    "Genesis": "GEN",
    "Exodus": "EXO",
    "Leviticus": "LEV",
    "Numbers": "NUM",
    "Deuteronomy": "DEU",
    "Joshua": "JOS",
    "Judges": "JDG",
    "Ruth": "RUT",
    "1 Samuel": "1SA",
    "2 Samuel": "2SA",
    "1 Kings": "1KI",
    "2 Kings": "2KI",
    "1 Chronicles": "1CH",
    "2 Chronicles": "2CH",
    "Ezra": "EZR",
    "Nehemiah": "NEH",
    "Esther": "EST",
    "Job": "JOB",
    "Psalms": "PSA",
    "Psalm": "PSA",
    "Proverbs": "PRO",
    "Ecclesiastes": "ECC",
    "Song of Solomon": "SNG",
    "Isaiah": "ISA",
    "Jeremiah": "JER",
    "Lamentations": "LAM",
    "Ezekiel": "EZK",
    "Daniel": "DAN",
    "Hosea": "HOS",
    "Joel": "JOL",
    "Amos": "AMO",
    "Obadiah": "OBA",
    "Jonah": "JON",
    "Micah": "MIC",
    "Nahum": "NAM",
    "Habakkuk": "HAB",
    "Zephaniah": "ZEP",
    "Haggai": "HAG",
    "Zechariah": "ZEC",
    "Malachi": "MAL",
    "Matthew": "MAT",
    "Mark": "MRK",
    "Luke": "LUK",
    "John": "JHN",
    "Acts": "ACT",
    "Romans": "ROM",
    "1 Corinthians": "1CO",
    "2 Corinthians": "2CO",
    "Galatians": "GAL",
    "Ephesians": "EPH",
    "Philippians": "PHP",
    "Colossians": "COL",
    "1 Thessalonians": "1TH",
    "2 Thessalonians": "2TH",
    "1 Timothy": "1TI",
    "2 Timothy": "2TI",
    "Titus": "TIT",
    "Philemon": "PHM",
    "Hebrews": "HEB",
    "James": "JAS",
    "1 Peter": "1PE",
    "2 Peter": "2PE",
    "1 John": "1JN",
    "2 John": "2JN",
    "3 John": "3JN",
    "Jude": "JUD",
    "Revelation": "REV",
}

CANONICAL_BOOK_ORDER = {code: index for index, code in enumerate(dict.fromkeys(BOOK_NAME_CODES.values()), start=1)}

MARKDOWN_QUOTE_RE = re.compile(r"^>\s*")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = read_rows(args.manifest)
    selected = select_rows(rows, args.only)
    if args.dry_run:
        for row in selected:
            print(f"{row['label']} {row['source_id']} {row['source_path_prefix']}")
        print(f"selected={len(selected)}")
        return 0

    completed = []
    commit_sha = fetch_commit_sha(args.ref)
    for row in selected:
        completed.append(download_row(row, args, commit_sha=commit_sha))
    write_run_manifest(args, rows=completed, commit_sha=commit_sha)
    for path in completed:
        print(path)
    print(f"downloaded={len(completed)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--ref", default=DEFAULT_REF)
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        help="Restrict to a label or source_id; may be repeated.",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Reuse existing CSV and source manifest when both are present.",
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


def download_row(row: dict[str, str], args: argparse.Namespace, *, commit_sha: str) -> str:
    source_id = row["source_id"]
    raw_root = args.raw_dir / source_id
    csv_path = Path(row["local_csv"])
    manifest_path = csv_path.with_suffix(".manifest.json")
    if args.skip_existing and csv_path.exists() and manifest_path.exists():
        return str(csv_path)

    entries = selected_json_entries(row["source_path_prefix"], args.ref)
    if not entries:
        raise SystemExit(f"{row['label']}: no JSON chapter files found under {row['source_path_prefix']}")

    downloaded_files = []
    for entry in entries:
        source_path = str(entry["path"])
        local_path = raw_root / relative_source_path(source_path, row["source_path_prefix"])
        if not local_path.exists():
            download(str(entry["download_url"]), local_path)
        downloaded_files.append((entry, local_path))

    verses = []
    for entry, path in sorted(downloaded_files, key=lambda item: source_path_sort_key(str(item[0]["path"]))):
        verses.extend(parse_otb_chapter_json(path.read_text(encoding="utf-8-sig"), path=str(entry["path"])))
    write_csv(csv_path, verses)
    write_source_manifest(
        manifest_path,
        row=row,
        raw_root=raw_root,
        csv_path=csv_path,
        verses=verses,
        downloaded_files=downloaded_files,
        commit_sha=commit_sha,
        ref=args.ref,
    )
    return str(csv_path)


def selected_json_entries(prefix: str, ref: str) -> list[dict[str, Any]]:
    books = fetch_books_json(prefix, ref)
    slugs = fetch_book_slugs(prefix, ref)
    entries: list[dict[str, Any]] = []
    for index, (book_name, chapter_count) in enumerate(books.items(), start=1):
        canonical_book_name(book_name)
        book_dir = f"{index:02d}.{book_name}"
        slug = slugs.get(book_name, slugify_book_name(book_name))
        chapter_width = 3 if int(chapter_count) >= 100 else 2
        for chapter in range(1, int(chapter_count) + 1):
            path = f"{prefix.rstrip('/')}/{book_dir}/json/{slug}-{chapter:0{chapter_width}d}.json"
            entries.append(
                {
                    "path": path,
                    "download_url": raw_url(path, ref),
                    "sha": "",
                }
            )
    return sorted(entries, key=lambda entry: source_path_sort_key(str(entry["path"])))


def fetch_books_json(prefix: str, ref: str) -> dict[str, int]:
    payload = fetch_raw_json(raw_url(f"{prefix.rstrip('/')}/books.json", ref))
    if not isinstance(payload, dict):
        raise SystemExit("OTB books.json response must be an object")
    return {str(book): int(chapters) for book, chapters in payload.items()}


def fetch_book_slugs(prefix: str, ref: str) -> dict[str, str]:
    payload = fetch_raw_json(raw_url(f"{prefix.rstrip('/')}/booksSlug.json", ref))
    if not isinstance(payload, dict):
        raise SystemExit("OTB booksSlug.json response must be an object")
    return {str(book): str(slug) for book, slug in payload.items()}


def fetch_commit_sha(ref: str) -> str:
    try:
        completed = subprocess.run(
            [
                "git",
                "ls-remote",
                f"https://github.com/{REPO}.git",
                f"refs/heads/{ref}",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except (OSError, subprocess.SubprocessError):
        return ref
    first = completed.stdout.split()
    return first[0] if first else ref


def fetch_json(url: str) -> Any:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(request, timeout=120) as response:
        try:
            return json.loads(response.read().decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"OTB GitHub API response is invalid JSON: {exc}") from exc


def fetch_raw_json(url: str) -> Any:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        try:
            return json.loads(response.read().decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"OTB raw JSON response is invalid JSON: {exc}") from exc


def download(url: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        out_path.write_bytes(response.read())


def raw_url(path: str, ref: str) -> str:
    quoted_path = urllib.parse.quote(path, safe="/")
    quoted_ref = urllib.parse.quote(ref, safe="")
    return f"https://raw.githubusercontent.com/{REPO}/{quoted_ref}/{quoted_path}"


def relative_source_path(source_path: str, prefix: str) -> Path:
    normalized_prefix = prefix.rstrip("/") + "/"
    if source_path.startswith(normalized_prefix):
        return Path(source_path[len(normalized_prefix):])
    return Path(source_path).name


def parse_otb_chapter_json(text: str, *, path: str = "") -> list[UsfmVerse]:
    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: OTB chapter JSON root must be an object")
    book_name = str(payload.get("book", "")).strip()
    chapter = str(payload.get("chapter", "")).strip()
    book = canonical_book_name(book_name or book_name_from_path(path))
    if not book or not chapter:
        raise ValueError(f"{path}: missing book or chapter")

    verses: list[UsfmVerse] = []
    raw_verses = payload.get("verses", [])
    if not isinstance(raw_verses, list):
        raise ValueError(f"{path}: OTB chapter verses must be a list")
    for item in raw_verses:
        if not isinstance(item, dict) or "verse" not in item:
            continue
        verse = str(item.get("verse", "")).strip()
        parts = item.get("text", [])
        if not verse or not isinstance(parts, list):
            continue
        verse_text = clean_verse_text(parts)
        if verse_text:
            verses.append(UsfmVerse(book=book, chapter=chapter, verse=verse, text=verse_text))
    return verses


def clean_verse_text(parts: list[Any]) -> str:
    cleaned = []
    for part in parts:
        line = MARKDOWN_QUOTE_RE.sub("", str(part)).strip()
        if not line or line == "---":
            continue
        cleaned.append(line)
    return " ".join(" ".join(cleaned).split())


def canonical_book_name(book_name: str) -> str:
    if book_name in BOOK_NAME_CODES:
        return BOOK_NAME_CODES[book_name]
    compact = " ".join(book_name.replace("-", " ").split())
    if compact in BOOK_NAME_CODES:
        return BOOK_NAME_CODES[compact]
    raise ValueError(f"unknown OTB book name: {book_name}")


def book_name_from_path(path: str) -> str:
    for part in Path(path).parts:
        if "." in part and part.split(".", 1)[0].isdigit():
            return part.split(".", 1)[1]
    return ""


def slugify_book_name(book_name: str) -> str:
    return book_name.lower().replace(" ", "-")


def source_path_sort_key(path: str) -> tuple[int, int, str]:
    book = canonical_book_name(book_name_from_path(path))
    chapter = chapter_from_path(path)
    return (CANONICAL_BOOK_ORDER.get(book, 999), chapter, path)


def chapter_from_path(path: str) -> int:
    stem = Path(path).stem
    suffix = stem.rsplit("-", 1)[-1]
    try:
        return int(suffix)
    except ValueError:
        return 999


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
    raw_root: Path,
    csv_path: Path,
    verses: list[UsfmVerse],
    downloaded_files: list[tuple[dict[str, Any], Path]],
    commit_sha: str,
    ref: str,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "source_id": row["source_id"],
        "label": row["label"],
        "source_name": row["name"],
        "source_url": row["source_url"],
        "details_url": row["details_url"],
        "license": row["license_label"],
        "repo": REPO,
        "ref": ref,
        "commit_sha": commit_sha,
        "source_path_prefix": row["source_path_prefix"],
        "downloaded_at": datetime.now(UTC).isoformat(),
        "raw_root": str(raw_root),
        "raw_file_count": len(downloaded_files),
        "raw_files": [
            {
                "source_path": str(entry["path"]),
                "source_sha": str(entry.get("sha", "")),
                "local_path": str(local_path),
                "local_sha256": sha256(local_path),
                "bytes": local_path.stat().st_size,
            }
            for entry, local_path in downloaded_files
        ],
        "csv_path": str(csv_path),
        "csv_sha256": sha256(csv_path),
        "book_count": len({verse.book for verse in verses}),
        "verse_count": len(verses),
        "first_ref": verses[0].ref if verses else "",
        "last_ref": verses[-1].ref if verses else "",
        "normalization": "OTB chapter JSON converted to verse CSV; non-verse separator records skipped; Markdown blockquote markers removed.",
    }
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_run_manifest(args: argparse.Namespace, *, rows: list[str], commit_sha: str) -> None:
    path = Path("reports/otb_english_controls/download.manifest.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "tool": "download_otb_english_controls",
        "created_utc": datetime.now(UTC).isoformat(),
        "manifest": str(args.manifest.resolve()),
        "repo": REPO,
        "ref": args.ref,
        "commit_sha": commit_sha,
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
