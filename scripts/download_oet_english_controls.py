#!/usr/bin/env python3
"""Download Open English Translation control sources from the tracked manifest."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import urllib.request
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els.ebible_usfm import UsfmVerse, parse_usfm


DEFAULT_MANIFEST = Path("configs/oet_english_controls.csv")
DEFAULT_RAW_DIR = Path("data/raw/oet")
REPO = "Freely-Given-org/OpenEnglishTranslation--OET"
DEFAULT_REF = "main"
USER_AGENT = "Open Bible Codes OET source importer"

USFM_SUFFIXES = (".usfm", ".sfm")

BOOK_ALIASES = {
    "1Ch": "1CH",
    "1Co": "1CO",
    "1Jn": "1JN",
    "1Ki": "1KI",
    "1Ma": "1MA",
    "1Pe": "1PE",
    "1Sa": "1SA",
    "1Th": "1TH",
    "1Ti": "1TI",
    "2Ch": "2CH",
    "2Co": "2CO",
    "2Jn": "2JN",
    "2Ki": "2KI",
    "2Ma": "2MA",
    "2Pe": "2PE",
    "2Sa": "2SA",
    "2Th": "2TH",
    "2Ti": "2TI",
    "3Jn": "3JN",
    "3Ma": "3MA",
    "4Ma": "4MA",
    "Act": "ACT",
    "Amo": "AMO",
    "Bar": "BAR",
    "Col": "COL",
    "Dag": "DAG",
    "Dan": "DAN",
    "Deu": "DEU",
    "Ecc": "ECC",
    "Eph": "EPH",
    "EsG": "ESG",
    "Est": "EST",
    "Exo": "EXO",
    "Ezk": "EZK",
    "Ezr": "EZR",
    "Gal": "GAL",
    "Gen": "GEN",
    "Hab": "HAB",
    "Hag": "HAG",
    "Heb": "HEB",
    "Hos": "HOS",
    "Isa": "ISA",
    "Jas": "JAS",
    "Jdg": "JDG",
    "Jdt": "JDT",
    "Jer": "JER",
    "Jhn": "JHN",
    "Job": "JOB",
    "Jol": "JOL",
    "Jon": "JON",
    "Jos": "JOS",
    "Jud": "JUD",
    "Lam": "LAM",
    "Lev": "LEV",
    "Luk": "LUK",
    "Mal": "MAL",
    "Man": "MAN",
    "Mat": "MAT",
    "Mic": "MIC",
    "Mrk": "MRK",
    "Nam": "NAM",
    "Neh": "NEH",
    "Num": "NUM",
    "Oba": "OBA",
    "Phm": "PHM",
    "Php": "PHP",
    "Pro": "PRO",
    "Ps2": "PS2",
    "Psa": "PSA",
    "Rev": "REV",
    "Rom": "ROM",
    "Rut": "RUT",
    "Sir": "SIR",
    "Sng": "SNG",
    "Tob": "TOB",
    "Tit": "TIT",
    "Wis": "WIS",
    "Zec": "ZEC",
    "Zep": "ZEP",
}
BOOK_ALIASES.update({value: value for value in BOOK_ALIASES.values()})

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
            "EST",
            "JOB",
            "PSA",
            "PRO",
            "ECC",
            "SNG",
            "ISA",
            "JER",
            "LAM",
            "EZK",
            "DAN",
            "HOS",
            "JOL",
            "AMO",
            "OBA",
            "JON",
            "MIC",
            "NAM",
            "HAB",
            "ZEP",
            "HAG",
            "ZEC",
            "MAL",
            "TOB",
            "JDT",
            "ESG",
            "WIS",
            "SIR",
            "BAR",
            "DAG",
            "MAN",
            "1MA",
            "2MA",
            "3MA",
            "4MA",
            "PS2",
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
            print(f"{row['label']} {row['source_id']} {row['source_path_prefix']}")
        print(f"selected={len(selected)}")
        return 0

    completed = []
    tree_payload = fetch_repo_tree(args.ref)
    commit_sha = fetch_commit_sha(args.ref)
    for row in selected:
        completed.append(download_row(row, args, tree_payload=tree_payload, commit_sha=commit_sha))
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


def download_row(
    row: dict[str, str],
    args: argparse.Namespace,
    *,
    tree_payload: dict[str, Any],
    commit_sha: str,
) -> str:
    source_id = row["source_id"]
    raw_root = args.raw_dir / source_id
    csv_path = Path(row["local_csv"])
    manifest_path = csv_path.with_suffix(".manifest.json")
    if args.skip_existing and csv_path.exists() and manifest_path.exists():
        return str(csv_path)

    entries = selected_usfm_entries(tree_payload, row["source_path_prefix"])
    if not entries:
        raise SystemExit(f"{row['label']}: no USFM files found under {row['source_path_prefix']}")

    downloaded_files = []
    for entry in entries:
        local_path = raw_root / Path(entry["path"]).name
        download(raw_url(entry["path"], args.ref), local_path)
        downloaded_files.append((entry, local_path))

    verses = []
    for entry, path in sorted(downloaded_files, key=lambda item: source_file_sort_key(item[1])):
        verses.extend(parse_oet_usfm(path.read_text(encoding="utf-8-sig"), path=entry["path"]))
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


def fetch_repo_tree(ref: str) -> dict[str, Any]:
    payload = fetch_json(f"https://api.github.com/repos/{REPO}/git/trees/{ref}?recursive=1")
    if not isinstance(payload, dict):
        raise SystemExit("OET repository tree response must be an object")
    tree = payload.get("tree")
    if not isinstance(tree, list):
        raise SystemExit("OET repository tree response tree must be a list")
    for index, entry in enumerate(tree):
        if not isinstance(entry, dict):
            raise SystemExit(
                f"OET repository tree response entry {index} must be an object"
            )
    if payload.get("truncated"):
        raise SystemExit("OET repository tree response was truncated")
    return payload


def fetch_commit_sha(ref: str) -> str:
    payload = fetch_json(f"https://api.github.com/repos/{REPO}/commits/{ref}")
    if not isinstance(payload, dict):
        raise SystemExit("OET commit response must be an object")
    return str(payload.get("sha", ref))


def fetch_json(url: str) -> Any:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(request, timeout=120) as response:
        try:
            return json.loads(response.read().decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"OET GitHub API response is invalid JSON: {exc}") from exc


def selected_usfm_entries(tree_payload: dict[str, Any], prefix: str) -> list[dict[str, Any]]:
    normalized_prefix = prefix.rstrip("/") + "/"
    entries = [
        entry
        for entry in tree_payload.get("tree", [])
        if entry.get("type") == "blob"
        and str(entry.get("path", "")).startswith(normalized_prefix)
        and str(entry.get("path", "")).lower().endswith(USFM_SUFFIXES)
    ]
    return sorted(entries, key=lambda entry: source_path_sort_key(str(entry["path"])))


def raw_url(path: str, ref: str) -> str:
    return f"https://raw.githubusercontent.com/{REPO}/{ref}/{path}"


def download(url: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        out_path.write_bytes(response.read())


def parse_oet_usfm(text: str, *, path: str) -> list[UsfmVerse]:
    default_book = canonical_book_from_path(path)
    verses = parse_usfm(text, default_book=default_book)
    return [
        replace(verse, book=canonical_book_id(verse.book or default_book))
        for verse in verses
    ]


def canonical_book_from_path(path: str | Path) -> str:
    name = Path(path).stem
    marker = name.rsplit("_", 1)[-1]
    return canonical_book_id(marker)


def canonical_book_id(value: str) -> str:
    base = value.strip().split(" ", 1)[0]
    if base in BOOK_ALIASES:
        return BOOK_ALIASES[base]
    upper = base.upper()
    if upper in BOOK_ALIASES:
        return BOOK_ALIASES[upper]
    return upper


def source_path_sort_key(path: str) -> tuple[int, str]:
    book = canonical_book_from_path(path)
    return (CANONICAL_BOOK_ORDER.get(book, 999), path)


def source_file_sort_key(path: Path) -> tuple[int, str]:
    book = canonical_book_from_path(path)
    return (CANONICAL_BOOK_ORDER.get(book, 999), path.name)


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
        "normalization": "USFM markers, notes, crossrefs, and word attributes removed; verse text preserved; books sorted in Protestant canon, deuterocanon/apocrypha, then NT order.",
    }
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_run_manifest(args: argparse.Namespace, *, rows: list[str], commit_sha: str) -> None:
    path = Path("reports/oet_english_controls/download.manifest.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "tool": "download_oet_english_controls",
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
