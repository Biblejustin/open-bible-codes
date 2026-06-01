#!/usr/bin/env python3
"""Build a non-text Project Gutenberg KJVA candidate checksum sidecar."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__


DEFAULT_SOURCE_STATUS = Path("reports/kjva_gutenberg_candidate_source/source_status.csv")
DEFAULT_SOURCE_SUMMARY = Path("reports/kjva_gutenberg_candidate_source/summary.csv")
DEFAULT_PREP_SUMMARY = Path("reports/kjva_gutenberg_source_lock_prep/summary.csv")
DEFAULT_OUT_DIR = Path("reports/kjva_gutenberg_candidate_checksum_sidecar")
DEFAULT_CHECKSUMS = DEFAULT_OUT_DIR / "source_checksums.csv"
DEFAULT_SUMMARY = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_MD = Path("docs/KJVA_GUTENBERG_CANDIDATE_CHECKSUM_SIDECAR.md")

CHECKSUM_FIELDNAMES = [
    "source_id",
    "component",
    "ebook_no",
    "metadata_url",
    "source_page_url",
    "title",
    "rights",
    "rdf_sha256",
    "rdf_bytes",
    "plain_text_sha256",
    "plain_text_bytes",
    "plain_text_utf8_url_present",
    "source_use_status",
    "checksum_role",
    "lock_status",
    "result_boundary",
]
SUMMARY_FIELDNAMES = [
    "source_rows",
    "metadata_fetches_ok",
    "public_domain_usa_rows",
    "plain_text_rows",
    "checksum_records_ready",
    "kjv_plain_text_sha256",
    "apocrypha_plain_text_sha256",
    "source_use_ready_pages",
    "verse_import_ready_pages",
    "source_lock_ready",
    "result_ready",
    "claim_status",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    source_rows = read_csv_dicts(args.source_status)
    source_summary = read_single_csv_row(args.source_summary)
    prep_summary = read_single_csv_row(args.prep_summary)
    checksum_rows = build_checksum_rows(source_rows, prep_summary)
    summary = build_summary(checksum_rows, source_summary, prep_summary)
    write_csv(args.checksums_out, CHECKSUM_FIELDNAMES, checksum_rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, summary, checksum_rows)
    write_manifest(args.manifest_out, args, summary, checksum_rows, started)
    print(args.checksums_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-status", type=Path, default=DEFAULT_SOURCE_STATUS)
    parser.add_argument("--source-summary", type=Path, default=DEFAULT_SOURCE_SUMMARY)
    parser.add_argument("--prep-summary", type=Path, default=DEFAULT_PREP_SUMMARY)
    parser.add_argument("--checksums-out", type=Path, default=DEFAULT_CHECKSUMS)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_checksum_rows(
    source_rows: list[dict[str, str]],
    prep_summary: dict[str, str],
) -> list[dict[str, Any]]:
    plain_text_by_ebook = {
        "30": (
            "kjv_66_book_component",
            prep_summary.get("kjv_plain_text_sha256", ""),
            prep_summary.get("kjv_plain_text_bytes", ""),
        ),
        "124": (
            "apocrypha_deuterocanon_component",
            prep_summary.get("apocrypha_plain_text_sha256", ""),
            prep_summary.get("apocrypha_plain_text_bytes", ""),
        ),
    }
    rows: list[dict[str, Any]] = []
    for row in source_rows:
        ebook_no = row.get("ebook_no", "")
        component, plain_sha, plain_bytes = plain_text_by_ebook.get(
            ebook_no,
            ("unknown_component", "", ""),
        )
        rows.append(
            {
                "source_id": row.get("source_id", ""),
                "component": component,
                "ebook_no": ebook_no,
                "metadata_url": row.get("final_url", ""),
                "source_page_url": row.get("ebook_page_url", ""),
                "title": row.get("title", ""),
                "rights": row.get("rights", ""),
                "rdf_sha256": row.get("sha256", ""),
                "rdf_bytes": row.get("bytes", ""),
                "plain_text_sha256": plain_sha,
                "plain_text_bytes": plain_bytes,
                "plain_text_utf8_url_present": row.get("plain_text_utf8_url_present", ""),
                "source_use_status": row.get("source_use_status", ""),
                "checksum_role": "candidate_identifier_only",
                "lock_status": "checksum_record_ready_not_source_locked",
                "result_boundary": "not_result_bearing",
            }
        )
    return rows


def build_summary(
    checksum_rows: list[dict[str, Any]],
    source_summary: dict[str, str],
    prep_summary: dict[str, str],
) -> dict[str, Any]:
    return {
        "source_rows": len(checksum_rows),
        "metadata_fetches_ok": source_summary.get("metadata_fetches_ok", ""),
        "public_domain_usa_rows": sum(
            1 for row in checksum_rows if row.get("rights") == "Public domain in the USA."
        ),
        "plain_text_rows": sum(1 for row in checksum_rows if row.get("plain_text_sha256")),
        "checksum_records_ready": sum(
            1
            for row in checksum_rows
            if row.get("rdf_sha256") and row.get("plain_text_sha256")
        ),
        "kjv_plain_text_sha256": prep_summary.get("kjv_plain_text_sha256", ""),
        "apocrypha_plain_text_sha256": prep_summary.get(
            "apocrypha_plain_text_sha256", ""
        ),
        "source_use_ready_pages": source_summary.get("source_use_ready_pages", ""),
        "verse_import_ready_pages": source_summary.get("verse_import_ready_pages", ""),
        "source_lock_ready": False,
        "result_ready": False,
        "claim_status": "checksum_sidecar_only_not_result_bearing",
    }


def write_markdown(
    path: Path,
    summary: dict[str, Any],
    checksum_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# KJVA Gutenberg Candidate Checksum Sidecar",
        "",
        "Status: checksum sidecar only.",
        "",
        "This is not an ELS result, not a corpus import, not a source-use approval, not a source lock, and not a result-bearing replication.",
        "It records Project Gutenberg eBook 30 and eBook 124 RDF and plain-text checksums as candidate identifiers.",
        "It does not commit Bible text, choose source wording, split unmarked prose, replace current eBible KJVA, or authorize a KJVA bridge run.",
        "",
        "## Summary",
        "",
        f"- Source rows: {summary['source_rows']}.",
        f"- Metadata fetches OK: {summary['metadata_fetches_ok']}.",
        f"- Public-domain-USA rows: {summary['public_domain_usa_rows']}.",
        f"- Plain-text checksum rows: {summary['plain_text_rows']}.",
        f"- Checksum records ready: {summary['checksum_records_ready']}.",
        f"- KJV plain-text SHA-256: `{summary['kjv_plain_text_sha256']}`.",
        f"- Apocrypha plain-text SHA-256: `{summary['apocrypha_plain_text_sha256']}`.",
        f"- Source-use ready pages: {summary['source_use_ready_pages']}.",
        f"- Verse-import ready pages: {summary['verse_import_ready_pages']}.",
        f"- Source-lock ready: {int(bool(summary['source_lock_ready']))}.",
        f"- Result-ready: {int(bool(summary['result_ready']))}.",
        f"- Claim status: `{summary['claim_status']}`.",
        "",
        "## Checksum Rows",
        "",
        "| Source | Component | eBook | RDF SHA-256 | Plain-text SHA-256 | Rights | Status |",
        "| --- | --- | ---: | --- | --- | --- | --- |",
    ]
    for row in checksum_rows:
        lines.append(
            f"| `{row['source_id']}` | `{row['component']}` | {row['ebook_no']} | `{row['rdf_sha256']}` | `{row['plain_text_sha256']}` | {row['rights']} | `{row['lock_status']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This sidecar closes only the candidate checksum-record step for Project Gutenberg eBook 30 and eBook 124.",
            "It does not close source-use, verse mapping, collation, `SIR 44:23`, Prayer of Manasseh, `SIR 19:1`, term/control, or study-lock blockers.",
            "No Bible text is written to tracked outputs.",
            "It does not change any KJVA bridge result status.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary: dict[str, Any],
    checksum_rows: list[dict[str, Any]],
    started: float,
) -> None:
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "els_version": __version__,
        "tool": "scripts.build_kjva_gutenberg_candidate_checksum_sidecar",
        "claim_boundary": "checksum sidecar only; no ELS result",
        "text_retention": "no Bible text written to tracked outputs",
        "summary": summary,
        "checksum_rows": len(checksum_rows),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "source_status": str(args.source_status),
            "source_summary": str(args.source_summary),
            "prep_summary": str(args.prep_summary),
        },
        "outputs": {
            "checksums": str(args.checksums_out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_single_csv_row(path: Path) -> dict[str, str]:
    rows = read_csv_dicts(path)
    if len(rows) != 1:
        raise ValueError(f"{path} expected one row, found {len(rows)}")
    return rows[0]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
