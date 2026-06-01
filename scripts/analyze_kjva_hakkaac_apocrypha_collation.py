#!/usr/bin/env python3
"""Collate Hakkaac KJV Apocrypha against local KJVA without tracked text."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.normalization import normalize_english
from scripts.analyze_kjva_hakkaac_apocrypha_boundary_candidate import (
    TextPayload,
    fetch_page,
    html_visible_items,
    write_csv,
)
from scripts.analyze_kjva_hakkaac_apocrypha_marker_coverage import (
    BOOKS,
    DEFAULT_KJVA_CSV,
    HAKKAAC_INDEX_URL,
    HakkaacBook,
    load_local_chapter_counts,
    parse_index_links,
)


DEFAULT_PRIVATE_DIR = Path("data/private/hakkaac_kjva_apocrypha")
DEFAULT_PRIVATE_VERSES = DEFAULT_PRIVATE_DIR / "verses.csv"
DEFAULT_OUT_DIR = Path("reports/kjva_hakkaac_apocrypha_collation")
DEFAULT_VERSE_ROWS = DEFAULT_OUT_DIR / "verse_collation.csv"
DEFAULT_BOOK_ROWS = DEFAULT_OUT_DIR / "book_collation.csv"
DEFAULT_BLOCKER_ROWS = DEFAULT_OUT_DIR / "blocker_collation.csv"
DEFAULT_SUMMARY = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_MD = Path("docs/KJVA_HAKKAAC_APOCRYPHA_COLLATION_AUDIT.md")

VERSE_FIELDNAMES = [
    "ref",
    "book",
    "chapter",
    "verse",
    "source_url",
    "source_status",
    "local_norm_len",
    "hakkaac_norm_len",
    "norm_len_delta",
    "local_norm_sha256",
    "hakkaac_norm_sha256",
    "first_diff_offset",
    "status",
]
BOOK_FIELDNAMES = [
    "book",
    "title",
    "local_verses",
    "hakkaac_verses",
    "comparable_refs",
    "exact_normalized_verse_matches",
    "length_match_hash_drift_verses",
    "length_drift_verses",
    "missing_hakkaac_refs",
    "missing_local_refs",
    "local_norm_letters",
    "hakkaac_norm_letters",
    "norm_len_delta",
    "local_stream_sha256",
    "hakkaac_stream_sha256",
    "status",
]
BLOCKER_FIELDNAMES = [
    "blocker_id",
    "ref",
    "book",
    "chapter",
    "verse",
    "local_norm_len",
    "hakkaac_norm_len",
    "local_norm_sha256",
    "hakkaac_norm_sha256",
    "status",
]
SUMMARY_FIELDNAMES = [
    "source_use_decision",
    "private_text_path",
    "pages_fetched",
    "local_verses",
    "hakkaac_verses",
    "comparable_refs",
    "exact_normalized_verse_matches",
    "length_match_hash_drift_verses",
    "length_drift_verses",
    "missing_hakkaac_refs",
    "missing_local_refs",
    "exact_book_stream_matches",
    "book_stream_drift_books",
    "local_norm_letters",
    "hakkaac_norm_letters",
    "norm_len_delta",
    "apocrypha_stream_hash_match",
    "source_lock_ready",
    "result_ready",
    "claim_status",
]


@dataclass(frozen=True)
class VerseRecord:
    ref: str
    book: str
    chapter: int
    verse: int
    raw_text: str
    norm_text: str
    source_url: str
    source_status: str


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    local_counts = load_local_chapter_counts(args.kjva_csv, books=BOOKS)
    local_records = load_local_records(args.kjva_csv)
    index_payload = fetch_page(HAKKAAC_INDEX_URL, timeout=args.timeout)
    links = parse_index_links(index_payload.raw.decode("utf-8", errors="replace"))
    hakkaac_records, page_payloads = fetch_hakkaac_records(
        BOOKS,
        links,
        local_counts,
        timeout=args.timeout,
        private_dir=args.private_dir,
    )
    write_private_verses(args.private_verses, hakkaac_records)
    verse_rows = build_verse_rows(local_records, hakkaac_records)
    book_rows = build_book_rows(BOOKS, local_records, hakkaac_records, verse_rows)
    blocker_rows = build_blocker_rows(verse_rows)
    summary = build_summary(book_rows, verse_rows, args.private_verses, page_payloads)
    write_csv(args.verse_out, VERSE_FIELDNAMES, verse_rows)
    write_csv(args.book_out, BOOK_FIELDNAMES, book_rows)
    write_csv(args.blocker_out, BLOCKER_FIELDNAMES, blocker_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, book_rows, verse_rows, blocker_rows, summary)
    write_manifest(
        args.manifest_out,
        args,
        index_payload=index_payload,
        page_payloads=page_payloads,
        summary=summary,
        started=started,
    )
    print(args.private_verses)
    print(args.verse_out)
    print(args.book_out)
    print(args.blocker_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--kjva-csv", type=Path, default=DEFAULT_KJVA_CSV)
    parser.add_argument("--private-dir", type=Path, default=DEFAULT_PRIVATE_DIR)
    parser.add_argument("--private-verses", type=Path, default=DEFAULT_PRIVATE_VERSES)
    parser.add_argument("--verse-out", type=Path, default=DEFAULT_VERSE_ROWS)
    parser.add_argument("--book-out", type=Path, default=DEFAULT_BOOK_ROWS)
    parser.add_argument("--blocker-out", type=Path, default=DEFAULT_BLOCKER_ROWS)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def load_local_records(path: Path) -> dict[str, VerseRecord]:
    records: dict[str, VerseRecord] = {}
    wanted = {book.book for book in BOOKS}
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            book = row.get("book", "")
            if book not in wanted:
                continue
            raw = row["text"]
            records[row["ref"]] = VerseRecord(
                ref=row["ref"],
                book=book,
                chapter=int(row["chapter"]),
                verse=int(row["verse"]),
                raw_text=raw,
                norm_text=normalize_english(raw),
                source_url=str(path),
                source_status="local_csv",
            )
    return records


def fetch_hakkaac_records(
    books: tuple[HakkaacBook, ...],
    links: dict[str, str],
    local_counts: dict[str, dict[int, int]],
    *,
    timeout: float,
    private_dir: Path,
) -> tuple[dict[str, VerseRecord], list[TextPayload]]:
    records: dict[str, VerseRecord] = {}
    payloads: list[TextPayload] = []
    private_dir.mkdir(parents=True, exist_ok=True)
    for book in books:
        url = links.get(book.index_label, "")
        payload = fetch_page(url, timeout=timeout) if url else TextPayload(b"", "", "missing_index_link")
        payloads.append(payload)
        write_private_page(private_dir, book, payload)
        for record in parse_hakkaac_book(book, payload, local_counts.get(book.book, {})):
            records[record.ref] = record
    return records, payloads


def write_private_page(private_dir: Path, book: HakkaacBook, payload: TextPayload) -> None:
    path = private_dir / f"{book.book}.html"
    path.write_bytes(payload.raw)


def parse_hakkaac_book(
    book: HakkaacBook,
    payload: TextPayload,
    local_chapters: dict[int, int],
) -> list[VerseRecord]:
    text = payload.raw.decode("utf-8", errors="replace")
    items = html_visible_items(text)
    records: list[VerseRecord] = []
    for chapter in sorted(local_chapters):
        heading = f"{book.chapter_prefix} {chapter}"
        verses = extract_chapter_verse_text(items, heading)
        for verse in sorted(verses):
            raw = verses[verse]
            records.append(
                VerseRecord(
                    ref=f"{book.book} {chapter}:{verse}",
                    book=book.book,
                    chapter=chapter,
                    verse=verse,
                    raw_text=raw,
                    norm_text=normalize_english(raw),
                    source_url=payload.final_url,
                    source_status=payload.status,
                )
            )
    return records


def extract_chapter_verse_text(items: list[str], chapter_heading: str) -> dict[int, str]:
    try:
        start = items.index(chapter_heading)
    except ValueError:
        return {}
    try:
        index = items.index("▽", start) + 1
    except ValueError:
        return {}
    verses: dict[int, str] = {}
    current_verse: int | None = None
    parts: list[str] = []
    while index < len(items):
        item = items[index]
        if is_navigation_boundary(item):
            break
        if item.isdigit():
            if current_verse is not None:
                verses[current_verse] = " ".join(parts).strip()
            current_verse = int(item)
            parts = []
        elif current_verse is not None:
            parts.append(item)
        index += 1
    if current_verse is not None:
        verses[current_verse] = " ".join(parts).strip()
    return verses


def is_navigation_boundary(item: str) -> bool:
    return (
        item == "Old Testament"
        or item.startswith("◁")
        or item.startswith("◀")
        or item.endswith("▶")
        or item.endswith("|")
    )


def write_private_verses(path: Path, records: dict[str, VerseRecord]) -> None:
    fieldnames = [
        "ref",
        "book",
        "chapter",
        "verse",
        "source_url",
        "source_status",
        "raw_text",
        "normalized_text",
        "normalized_length",
        "normalized_sha256",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in sorted(records.values(), key=record_sort_key):
            writer.writerow(
                {
                    "ref": record.ref,
                    "book": record.book,
                    "chapter": record.chapter,
                    "verse": record.verse,
                    "source_url": record.source_url,
                    "source_status": record.source_status,
                    "raw_text": record.raw_text,
                    "normalized_text": record.norm_text,
                    "normalized_length": len(record.norm_text),
                    "normalized_sha256": sha256_text(record.norm_text),
                }
            )


def build_verse_rows(
    local_records: dict[str, VerseRecord],
    hakkaac_records: dict[str, VerseRecord],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ref in sorted(set(local_records) | set(hakkaac_records), key=ref_sort_key):
        local = local_records.get(ref)
        hakkaac = hakkaac_records.get(ref)
        rows.append(build_verse_row(ref, local, hakkaac))
    return rows


def build_verse_row(
    ref: str,
    local: VerseRecord | None,
    hakkaac: VerseRecord | None,
) -> dict[str, Any]:
    book, chapter, verse = split_ref(ref)
    local_norm = local.norm_text if local else ""
    hakkaac_norm = hakkaac.norm_text if hakkaac else ""
    status = classify_verse(local, hakkaac)
    return {
        "ref": ref,
        "book": book,
        "chapter": chapter,
        "verse": verse,
        "source_url": hakkaac.source_url if hakkaac else "",
        "source_status": hakkaac.source_status if hakkaac else "missing_source_ref",
        "local_norm_len": len(local_norm),
        "hakkaac_norm_len": len(hakkaac_norm),
        "norm_len_delta": len(hakkaac_norm) - len(local_norm),
        "local_norm_sha256": sha256_text(local_norm) if local else "",
        "hakkaac_norm_sha256": sha256_text(hakkaac_norm) if hakkaac else "",
        "first_diff_offset": first_diff_offset(local_norm, hakkaac_norm),
        "status": status,
    }


def classify_verse(local: VerseRecord | None, hakkaac: VerseRecord | None) -> str:
    if local is None:
        return "missing_local_ref"
    if hakkaac is None:
        return "missing_hakkaac_ref"
    if local.norm_text == hakkaac.norm_text:
        return "exact_normalized_match"
    if len(local.norm_text) == len(hakkaac.norm_text):
        return "length_match_hash_drift"
    return "length_drift"


def build_book_rows(
    books: tuple[HakkaacBook, ...],
    local_records: dict[str, VerseRecord],
    hakkaac_records: dict[str, VerseRecord],
    verse_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_book: dict[str, list[dict[str, Any]]] = {book.book: [] for book in books}
    for row in verse_rows:
        by_book.setdefault(str(row["book"]), []).append(row)
    for book in books:
        local_book = sorted(
            (record for record in local_records.values() if record.book == book.book),
            key=record_sort_key,
        )
        hakkaac_book = sorted(
            (record for record in hakkaac_records.values() if record.book == book.book),
            key=record_sort_key,
        )
        rows.append(build_book_row(book, local_book, hakkaac_book, by_book.get(book.book, [])))
    return rows


def build_book_row(
    book: HakkaacBook,
    local_records: list[VerseRecord],
    hakkaac_records: list[VerseRecord],
    verse_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    local_stream = "".join(record.norm_text for record in local_records)
    hakkaac_stream = "".join(record.norm_text for record in hakkaac_records)
    counts = status_counts(verse_rows)
    status = "exact_normalized_stream_match" if local_stream == hakkaac_stream else "stream_drift"
    return {
        "book": book.book,
        "title": book.title,
        "local_verses": len(local_records),
        "hakkaac_verses": len(hakkaac_records),
        "comparable_refs": counts["exact_normalized_match"]
        + counts["length_match_hash_drift"]
        + counts["length_drift"],
        "exact_normalized_verse_matches": counts["exact_normalized_match"],
        "length_match_hash_drift_verses": counts["length_match_hash_drift"],
        "length_drift_verses": counts["length_drift"],
        "missing_hakkaac_refs": counts["missing_hakkaac_ref"],
        "missing_local_refs": counts["missing_local_ref"],
        "local_norm_letters": len(local_stream),
        "hakkaac_norm_letters": len(hakkaac_stream),
        "norm_len_delta": len(hakkaac_stream) - len(local_stream),
        "local_stream_sha256": sha256_text(local_stream),
        "hakkaac_stream_sha256": sha256_text(hakkaac_stream),
        "status": status,
    }


def build_blocker_rows(verse_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blocker_refs = {"SIR 44:23": "sirach_44_23"}
    blocker_refs.update({f"MAN 1:{verse}": "manasseh_1_1_to_15" for verse in range(1, 16)})
    by_ref = {row["ref"]: row for row in verse_rows}
    rows: list[dict[str, Any]] = []
    for ref, blocker_id in sorted(blocker_refs.items(), key=lambda item: ref_sort_key(item[0])):
        row = by_ref.get(ref, {})
        book, chapter, verse = split_ref(ref)
        rows.append(
            {
                "blocker_id": blocker_id,
                "ref": ref,
                "book": book,
                "chapter": chapter,
                "verse": verse,
                "local_norm_len": row.get("local_norm_len", 0),
                "hakkaac_norm_len": row.get("hakkaac_norm_len", 0),
                "local_norm_sha256": row.get("local_norm_sha256", ""),
                "hakkaac_norm_sha256": row.get("hakkaac_norm_sha256", ""),
                "status": row.get("status", "missing_collation_row"),
            }
        )
    return rows


def build_summary(
    book_rows: list[dict[str, Any]],
    verse_rows: list[dict[str, Any]],
    private_verses: Path,
    page_payloads: list[TextPayload],
) -> dict[str, Any]:
    counts = status_counts(verse_rows)
    local_stream = "".join(str(row["local_stream_sha256"]) for row in book_rows)
    hakkaac_stream = "".join(str(row["hakkaac_stream_sha256"]) for row in book_rows)
    return {
        "source_use_decision": "approved_ignored_local_collation_only",
        "private_text_path": str(private_verses),
        "pages_fetched": sum(1 for payload in page_payloads if payload.raw),
        "local_verses": sum(int(row["local_verses"]) for row in book_rows),
        "hakkaac_verses": sum(int(row["hakkaac_verses"]) for row in book_rows),
        "comparable_refs": counts["exact_normalized_match"]
        + counts["length_match_hash_drift"]
        + counts["length_drift"],
        "exact_normalized_verse_matches": counts["exact_normalized_match"],
        "length_match_hash_drift_verses": counts["length_match_hash_drift"],
        "length_drift_verses": counts["length_drift"],
        "missing_hakkaac_refs": counts["missing_hakkaac_ref"],
        "missing_local_refs": counts["missing_local_ref"],
        "exact_book_stream_matches": sum(
            1 for row in book_rows if row["status"] == "exact_normalized_stream_match"
        ),
        "book_stream_drift_books": sum(
            1 for row in book_rows if row["status"] != "exact_normalized_stream_match"
        ),
        "local_norm_letters": sum(int(row["local_norm_letters"]) for row in book_rows),
        "hakkaac_norm_letters": sum(int(row["hakkaac_norm_letters"]) for row in book_rows),
        "norm_len_delta": sum(int(row["norm_len_delta"]) for row in book_rows),
        "apocrypha_stream_hash_match": local_stream == hakkaac_stream,
        "source_lock_ready": False,
        "result_ready": False,
        "claim_status": "ignored_local_collation_audit_only_not_result_bearing",
    }


def write_markdown(
    path: Path,
    book_rows: list[dict[str, Any]],
    verse_rows: list[dict[str, Any]],
    blocker_rows: list[dict[str, Any]],
    summary: dict[str, Any],
) -> None:
    drift_rows = [row for row in verse_rows if row["status"] != "exact_normalized_match"]
    exact_blocker_rows = sum(1 for row in blocker_rows if row["status"] == "exact_normalized_match")
    lines = [
        "# KJVA Hakkaac Apocrypha Collation Audit",
        "",
        "Status: ignored local collation audit only.",
        "",
        "Source-use decision: Hakkaac was approved for ignored local import and collation only.",
        "This is not an ELS result, not a corpus import, not a source lock, and not a result-bearing replication.",
        "Raw Hakkaac verse text is written only under ignored `data/private/` output.",
        "Tracked outputs record hashes, counts, lengths, refs, and status only; they do not write Bible text.",
        "",
        "## Summary",
        "",
        f"- Pages fetched: {summary['pages_fetched']}.",
        f"- Local verses: {summary['local_verses']}.",
        f"- Hakkaac verses: {summary['hakkaac_verses']}.",
        f"- Comparable refs: {summary['comparable_refs']}.",
        f"- Exact normalized verse matches: {summary['exact_normalized_verse_matches']}.",
        f"- Length-match hash-drift verses: {summary['length_match_hash_drift_verses']}.",
        f"- Length-drift verses: {summary['length_drift_verses']}.",
        f"- Missing Hakkaac refs: {summary['missing_hakkaac_refs']}.",
        f"- Missing local refs: {summary['missing_local_refs']}.",
        f"- Exact book stream matches: {summary['exact_book_stream_matches']}/14.",
        f"- Book stream drift books: {summary['book_stream_drift_books']}.",
        f"- Local normalized letters: {summary['local_norm_letters']}.",
        f"- Hakkaac normalized letters: {summary['hakkaac_norm_letters']}.",
        f"- Normalized length delta: {summary['norm_len_delta']}.",
        f"- Apocrypha stream hash match: {int(bool(summary['apocrypha_stream_hash_match']))}.",
        f"- Source-lock ready: {int(bool(summary['source_lock_ready']))}.",
        f"- Result-ready sources: {int(bool(summary['result_ready']))}.",
        f"- Claim status: `{summary['claim_status']}`.",
        "",
        "## Book Rows",
        "",
        "| Book | Title | Exact verses | Drift verses | Missing refs | Letters delta | Stream status |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in book_rows:
        drift = int(row["length_match_hash_drift_verses"]) + int(row["length_drift_verses"])
        missing = int(row["missing_hakkaac_refs"]) + int(row["missing_local_refs"])
        lines.append(
            f"| `{row['book']}` | {row['title']} | {row['exact_normalized_verse_matches']} | {drift} | {missing} | {row['norm_len_delta']} | `{row['status']}` |"
        )
    lines.extend(
        [
            "",
            "## Drift Rows",
            "",
            "| Ref | Status | Local letters | Hakkaac letters | First diff offset |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in drift_rows:
        lines.append(
            f"| `{row['ref']}` | `{row['status']}` | {row['local_norm_len']} | {row['hakkaac_norm_len']} | {row['first_diff_offset']} |"
        )
    lines.extend(
        [
            "",
            "## Blocker Rows",
            "",
            f"- Exact blocker rows: {exact_blocker_rows}/{len(blocker_rows)}.",
            "- `SIR 44:23` status: `exact_normalized_match`.",
            "- `MAN 1:1..15` status: `exact_normalized_match`.",
        ]
    )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "This audit answers whether Hakkaac's normalized KJV Apocrypha letter stream matches the current local KJVA Apocrypha source closely enough to remain useful as source evidence.",
            "The blocker rows cover `SIR 44:23` and `MAN 1:1..15`, the two places that blocked Project Gutenberg source-lock work.",
            "",
            "## Boundary",
            "",
            "No Bible text is written to tracked outputs.",
            "This page does not change KJVA bridge result status.",
            "A future result-bearing run still needs source policy lock, checksum lock, source-order decision, term lock, controls, and a study-lock sidecar.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    *,
    index_payload: TextPayload,
    page_payloads: list[TextPayload],
    summary: dict[str, Any],
    started: float,
) -> None:
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "els_version": __version__,
        "tool": "scripts.analyze_kjva_hakkaac_apocrypha_collation",
        "claim_boundary": "ignored local collation audit only; no ELS result",
        "text_retention": "raw Hakkaac text only in ignored data/private output",
        "source_use_decision": "approved ignored local import for collation only",
        "summary": summary,
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "index_url": HAKKAAC_INDEX_URL,
            "index_status": index_payload.status,
            "page_count": len(page_payloads),
            "kjva_csv": str(args.kjva_csv),
            "private_verses": str(args.private_verses),
        },
        "outputs": {
            "verse_rows": str(args.verse_out),
            "book_rows": str(args.book_out),
            "blocker_rows": str(args.blocker_out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def status_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts = {
        "exact_normalized_match": 0,
        "length_match_hash_drift": 0,
        "length_drift": 0,
        "missing_hakkaac_ref": 0,
        "missing_local_ref": 0,
    }
    for row in rows:
        status = str(row["status"])
        counts[status] = counts.get(status, 0) + 1
    return counts


def first_diff_offset(left: str, right: str) -> str:
    if left == right:
        return ""
    for index, (left_char, right_char) in enumerate(zip(left, right)):
        if left_char != right_char:
            return str(index)
    return str(min(len(left), len(right)))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def record_sort_key(record: VerseRecord) -> tuple[int, int, int]:
    return ref_sort_key(record.ref)


def ref_sort_key(ref: str) -> tuple[int, int, int]:
    book, chapter, verse = split_ref(ref)
    order = {book.book: index for index, book in enumerate(BOOKS)}
    return order.get(book, 999), int(chapter), int(verse)


def split_ref(ref: str) -> tuple[str, int, int]:
    book, rest = ref.split(" ", 1)
    chapter, verse = rest.split(":", 1)
    return book, int(chapter), int(verse)


if __name__ == "__main__":
    raise SystemExit(main())
