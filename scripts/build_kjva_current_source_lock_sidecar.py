#!/usr/bin/env python3
"""Build a non-text current eBible KJVA rerun source-lock sidecar."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
from collections import OrderedDict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.normalization import normalize_english


DEFAULT_KJVA_CSV = Path("data/processed/ebible/eng-kjv.csv")
DEFAULT_KJVA_MANIFEST = Path("data/processed/ebible/eng-kjv.manifest.json")
DEFAULT_OUT_DIR = Path("reports/kjva_current_source_lock_sidecar")
DEFAULT_BOOK_SHAPE = DEFAULT_OUT_DIR / "book_shape.csv"
DEFAULT_SUMMARY = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_MD = Path("docs/KJVA_CURRENT_SOURCE_LOCK_SIDECAR.md")

APOCRYPHA_CODES = {
    "TOB",
    "JDT",
    "ESG",
    "WIS",
    "SIR",
    "BAR",
    "S3Y",
    "SUS",
    "BEL",
    "1MA",
    "2MA",
    "1ES",
    "MAN",
    "2ES",
}

BOOK_FIELDNAMES = [
    "book",
    "first_ref",
    "last_ref",
    "verses",
    "normalized_letters",
    "stream_sha256",
    "is_apocrypha",
]
SUMMARY_FIELDNAMES = [
    "source_id",
    "source_name",
    "source_url",
    "details_url",
    "license",
    "downloaded_at",
    "zip_sha256",
    "zip_bytes",
    "csv_path",
    "csv_sha256",
    "csv_bytes",
    "book_count",
    "verse_count",
    "apocrypha_book_count",
    "apocrypha_verse_count",
    "apocrypha_normalized_letters",
    "full_book_order",
    "apocrypha_book_order",
    "rerun_baseline_locked",
    "independent_source_lock_ready",
    "result_ready",
    "claim_status",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    source_manifest = json.loads(args.kjva_manifest.read_text(encoding="utf-8"))
    verse_rows = read_csv_dicts(args.kjva_csv)
    book_rows = build_book_shape(verse_rows)
    summary = build_summary(args.kjva_csv, source_manifest, book_rows)
    write_csv(args.book_out, BOOK_FIELDNAMES, book_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, summary, book_rows)
    write_manifest(args.manifest_out, args, summary, book_rows, started)
    print(args.book_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kjva-csv", type=Path, default=DEFAULT_KJVA_CSV)
    parser.add_argument("--kjva-manifest", type=Path, default=DEFAULT_KJVA_MANIFEST)
    parser.add_argument("--book-out", type=Path, default=DEFAULT_BOOK_SHAPE)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_book_shape(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped: OrderedDict[str, list[dict[str, str]]] = OrderedDict()
    for row in rows:
        grouped.setdefault(row["book"], []).append(row)
    book_rows: list[dict[str, Any]] = []
    for book, book_verses in grouped.items():
        stream = "".join(normalize_english(row["text"]) for row in book_verses)
        book_rows.append(
            {
                "book": book,
                "first_ref": book_verses[0]["ref"],
                "last_ref": book_verses[-1]["ref"],
                "verses": len(book_verses),
                "normalized_letters": len(stream),
                "stream_sha256": sha256_text(stream),
                "is_apocrypha": book in APOCRYPHA_CODES,
            }
        )
    return book_rows


def build_summary(
    csv_path: Path,
    source_manifest: dict[str, Any],
    book_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    apocrypha_rows = [row for row in book_rows if row["is_apocrypha"]]
    return {
        "source_id": source_manifest.get("source_id", ""),
        "source_name": source_manifest.get("source_name", ""),
        "source_url": source_manifest.get("source_url", ""),
        "details_url": source_manifest.get("details_url", ""),
        "license": source_manifest.get("license", ""),
        "downloaded_at": source_manifest.get("downloaded_at", ""),
        "zip_sha256": source_manifest.get("zip_sha256", ""),
        "zip_bytes": source_manifest.get("zip_bytes", ""),
        "csv_path": str(csv_path),
        "csv_sha256": sha256_bytes(csv_path.read_bytes()),
        "csv_bytes": csv_path.stat().st_size,
        "book_count": len(book_rows),
        "verse_count": sum(int(row["verses"]) for row in book_rows),
        "apocrypha_book_count": len(apocrypha_rows),
        "apocrypha_verse_count": sum(int(row["verses"]) for row in apocrypha_rows),
        "apocrypha_normalized_letters": sum(
            int(row["normalized_letters"]) for row in apocrypha_rows
        ),
        "full_book_order": ";".join(str(row["book"]) for row in book_rows),
        "apocrypha_book_order": ";".join(str(row["book"]) for row in apocrypha_rows),
        "rerun_baseline_locked": True,
        "independent_source_lock_ready": False,
        "result_ready": False,
        "claim_status": "current_source_rerun_sidecar_only_not_result_bearing",
    }


def write_markdown(
    path: Path,
    summary: dict[str, Any],
    book_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# KJVA Current Source Lock Sidecar",
        "",
        "Status: current-source rerun sidecar only.",
        "",
        "This is not an ELS result, not a new corpus import, not an independent replication source, and not a result-bearing run.",
        "It freezes the current eBible KJV + Apocrypha rerun baseline by checksum, book order, and count-only shape.",
        "It does not commit Bible text, change source text, choose a new external source, or authorize a new KJVA bridge run.",
        "",
        "## Summary",
        "",
        f"- Source id: `{summary['source_id']}`.",
        f"- Source name: {summary['source_name']}.",
        f"- Source URL: {summary['source_url']}.",
        f"- Details URL: {summary['details_url']}.",
        f"- License: {summary['license']}.",
        f"- Downloaded at: {summary['downloaded_at']}.",
        f"- ZIP SHA-256: `{summary['zip_sha256']}`.",
        f"- CSV SHA-256: `{summary['csv_sha256']}`.",
        f"- CSV bytes: {summary['csv_bytes']}.",
        f"- Books: {summary['book_count']}.",
        f"- Verses: {summary['verse_count']}.",
        f"- Apocrypha/deuterocanon books: {summary['apocrypha_book_count']}.",
        f"- Apocrypha/deuterocanon verses: {summary['apocrypha_verse_count']}.",
        f"- Apocrypha/deuterocanon normalized letters: {summary['apocrypha_normalized_letters']}.",
        f"- Rerun baseline locked: {int(bool(summary['rerun_baseline_locked']))}.",
        f"- Independent source-lock ready: {int(bool(summary['independent_source_lock_ready']))}.",
        f"- Result-ready: {int(bool(summary['result_ready']))}.",
        f"- Claim status: `{summary['claim_status']}`.",
        "",
        "## Book Order",
        "",
        f"- Full book order: `{summary['full_book_order']}`.",
        f"- Apocrypha/deuterocanon book order: `{summary['apocrypha_book_order']}`.",
        "",
        "## Book Shape",
        "",
        "| Book | First ref | Last ref | Verses | Normalized letters | Apocrypha |",
        "| --- | --- | --- | ---: | ---: | ---: |",
    ]
    for row in book_rows:
        lines.append(
            f"| `{row['book']}` | `{row['first_ref']}` | `{row['last_ref']}` | {row['verses']} | {row['normalized_letters']} | {int(bool(row['is_apocrypha']))} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This sidecar locks the current local eBible KJVA rerun baseline only.",
            "It does not make Hakkaac, Project Gutenberg, CrossWire, Wikisource, or Open-Bibles source-ready.",
            "It does not change any KJVA bridge result status.",
            "Fresh result-bearing work still needs a fresh term lock, control lock, study-lock sidecar, and independent source-policy decision if an external replication source is used.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary: dict[str, Any],
    book_rows: list[dict[str, Any]],
    started: float,
) -> None:
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "els_version": __version__,
        "tool": "scripts.build_kjva_current_source_lock_sidecar",
        "claim_boundary": "current-source rerun sidecar only; no ELS result",
        "text_retention": "no Bible text written to tracked outputs",
        "summary": summary,
        "book_rows": len(book_rows),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "kjva_csv": str(args.kjva_csv),
            "kjva_manifest": str(args.kjva_manifest),
        },
        "outputs": {
            "book_shape": str(args.book_out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
