#!/usr/bin/env python3
"""Import a local reference-prefixed Bible PDF into a private CSV."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


DEFAULT_OUT = Path("data/private/english/nlt.csv")
DEFAULT_MANIFEST = Path("data/private/english/nlt.manifest.json")
REF_RE = re.compile(
    r"^(?P<book>(?:[1-3]\s*)?[A-Za-z]+)\s+"
    r"(?P<chapter>\d+):(?P<verse>\d+[A-Za-z]?(?:[-\u2013]\d+[A-Za-z]?)?)"
    r"(?:\s+(?P<text>.*))?$"
)
VERSE_START_RE = re.compile(r"\d+")
HEADER_LINES = {"The Holy Bible", "New Living Translation NLT"}


BOOK_ORDER = [
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
]
BOOK_INDEX = {code: index for index, code in enumerate(BOOK_ORDER)}
ABBR_TO_CODE = {
    "1ch": "1CH",
    "1co": "1CO",
    "1jo": "1JN",
    "1ki": "1KI",
    "1pe": "1PE",
    "1sa": "1SA",
    "1th": "1TH",
    "1ti": "1TI",
    "2ch": "2CH",
    "2co": "2CO",
    "2jo": "2JN",
    "2ki": "2KI",
    "2pe": "2PE",
    "2sa": "2SA",
    "2th": "2TH",
    "2ti": "2TI",
    "3jo": "3JN",
    "act": "ACT",
    "amo": "AMO",
    "col": "COL",
    "dan": "DAN",
    "deu": "DEU",
    "ecc": "ECC",
    "eph": "EPH",
    "est": "EST",
    "exo": "EXO",
    "eze": "EZK",
    "ezr": "EZR",
    "gal": "GAL",
    "gen": "GEN",
    "hab": "HAB",
    "hag": "HAG",
    "heb": "HEB",
    "hos": "HOS",
    "isa": "ISA",
    "jam": "JAS",
    "jdg": "JDG",
    "jer": "JER",
    "job": "JOB",
    "joe": "JOL",
    "joh": "JHN",
    "jon": "JON",
    "jos": "JOS",
    "jud": "JUD",
    "lam": "LAM",
    "lev": "LEV",
    "luk": "LUK",
    "mal": "MAL",
    "mar": "MRK",
    "mat": "MAT",
    "mic": "MIC",
    "nah": "NAM",
    "neh": "NEH",
    "num": "NUM",
    "oba": "OBA",
    "phi": "PHP",
    "phm": "PHM",
    "pro": "PRO",
    "psa": "PSA",
    "rev": "REV",
    "rom": "ROM",
    "rut": "RUT",
    "sol": "SNG",
    "tit": "TIT",
    "zec": "ZEC",
    "zep": "ZEP",
}


@dataclass(frozen=True)
class VerseRow:
    ref: str
    book: str
    chapter: int
    verse: str
    text: str


@dataclass
class MutableVerse:
    book: str
    chapter: int
    verse: str
    parts: list[str]


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows, manifest = import_pdf(args.pdf, label=args.label)
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
    parser.add_argument("--label", default="NLT")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def import_pdf(path: Path, *, label: str) -> tuple[list[VerseRow], dict[str, object]]:
    extracted = pdftotext_text(path)
    rows, parse_meta = parse_extracted_text(extracted)
    anomalies = list(parse_meta["anomalies"])
    missing_books = list(parse_meta["missing_books"])
    if missing_books:
        anomalies.append(f"missing books: {', '.join(missing_books)}")
        parse_meta["anomalies"] = anomalies
    if anomalies:
        manifest = build_manifest(path, label, rows, parse_meta)
        raise SystemExit(f"import anomalies found: {json.dumps(manifest, ensure_ascii=False, indent=2)}")
    return rows, build_manifest(path, label, rows, parse_meta)


def pdftotext_text(path: Path) -> str:
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", str(path), "-"],
            check=True,
            text=True,
            capture_output=True,
        )
    except FileNotFoundError as exc:
        raise SystemExit("pdftotext is required; install poppler") from exc
    return result.stdout


def parse_extracted_text(text: str) -> tuple[list[VerseRow], dict[str, object]]:
    rows: list[VerseRow] = []
    current: MutableVerse | None = None
    anomalies: list[str] = []
    empty_refs: list[str] = []
    ignored_heading_lines: list[str] = []
    seen_refs: set[str] = set()
    previous_key: tuple[int, int, int] | None = None

    def flush() -> None:
        nonlocal previous_key
        if current is None:
            return
        body = normalize_text(" ".join(current.parts))
        ref = f"{current.book} {current.chapter}:{current.verse}"
        if not body:
            empty_refs.append(ref)
            return
        if ref in seen_refs:
            anomalies.append(f"{ref}: duplicate ref")
            return
        seen_refs.add(ref)
        order_key = (
            BOOK_INDEX[current.book],
            current.chapter,
            verse_start(current.verse),
        )
        if previous_key is not None and order_key <= previous_key:
            anomalies.append(f"{ref}: non-increasing order")
            return
        previous_key = order_key
        rows.append(VerseRow(ref, current.book, current.chapter, current.verse, body))

    for raw_line in text.splitlines():
        line = normalize_text(raw_line.replace("\f", " "))
        if not line:
            continue
        if line in HEADER_LINES:
            ignored_heading_lines.append(line)
            continue
        match = REF_RE.match(line)
        if match:
            flush()
            book = book_code(match.group("book"))
            if book is None:
                anomalies.append(f"unknown book abbreviation: {match.group('book')}")
                current = None
                continue
            verse = match.group("verse").replace("\u2013", "-")
            current = MutableVerse(
                book=book,
                chapter=int(match.group("chapter")),
                verse=verse,
                parts=[match.group("text") or ""],
            )
            continue
        if current is None:
            ignored_heading_lines.append(line)
        else:
            current.parts.append(line)
    flush()

    book_counts = {code: 0 for code in BOOK_ORDER}
    for row in rows:
        book_counts[row.book] += 1
    present_book_counts = {code: count for code, count in book_counts.items() if count}
    missing_books = [code for code, count in book_counts.items() if count == 0]

    return rows, {
        "book_row_counts": present_book_counts,
        "missing_books": missing_books,
        "empty_ref_count": len(empty_refs),
        "empty_refs": empty_refs[:200],
        "ignored_heading_lines": ignored_heading_lines[:50],
        "ignored_heading_line_count": len(ignored_heading_lines),
        "anomalies": anomalies,
    }


def build_manifest(
    path: Path,
    label: str,
    rows: list[VerseRow],
    parse_meta: dict[str, object],
) -> dict[str, object]:
    return {
        "tool": "import_ref_prefixed_pdf",
        "created_utc": datetime.now(UTC).isoformat(),
        "label": label,
        "source_pdf": str(path.resolve()),
        "source_pdf_sha256": sha256(path),
        "source_pdf_bytes": path.stat().st_size,
        "source_description": f"Local {label} reference-prefixed Bible PDF.",
        "license": "copyrighted source; local private analysis only; do not commit extracted text",
        "rows": len(rows),
        "book_count": len(parse_meta["book_row_counts"]),
        "book_row_counts": parse_meta["book_row_counts"],
        "missing_books": parse_meta["missing_books"],
        "empty_ref_count": parse_meta["empty_ref_count"],
        "empty_refs": parse_meta["empty_refs"],
        "ignored_heading_line_count": parse_meta["ignored_heading_line_count"],
        "ignored_heading_lines": parse_meta["ignored_heading_lines"],
        "anomaly_count": len(parse_meta["anomalies"]),
        "anomalies": parse_meta["anomalies"][:200],
        "normalization": "pdftotext -layout; reference-prefixed lines start rows; non-reference body continuations are joined; whitespace collapsed.",
    }


def book_code(abbreviation: str) -> str | None:
    return ABBR_TO_CODE.get(abbreviation.lower().replace(" ", ""))


def verse_start(verse: str) -> int:
    match = VERSE_START_RE.search(verse)
    if not match:
        return -1
    return int(match.group(0))


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
