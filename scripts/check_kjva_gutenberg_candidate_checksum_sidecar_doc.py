#!/usr/bin/env python3
"""Validate Project Gutenberg KJVA candidate checksum sidecar boundaries."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from scripts import build_kjva_gutenberg_candidate_checksum_sidecar as sidecar


DEFAULT_DOC = sidecar.DEFAULT_MD
DEFAULT_CHECKSUMS = sidecar.DEFAULT_CHECKSUMS
DEFAULT_SUMMARY = sidecar.DEFAULT_SUMMARY
DEFAULT_MANIFEST = sidecar.DEFAULT_MANIFEST

EXPECTED_KJV_PLAIN_SHA = "349cb0de0e1e0c14bbb960d201b44a1753b64d5cd23316a17fdb9e9ac01747ac"
EXPECTED_APOCRYPHA_PLAIN_SHA = "ed2f875e0f0972ed4748988f5b44480eccdb22ca3b4a3ce85edc75f17d259f4b"

REQUIRED_PHRASES = (
    "# KJVA Gutenberg Candidate Checksum Sidecar",
    "Status: checksum sidecar only.",
    "not an ELS result",
    "not a corpus import",
    "not a source-use approval",
    "not a source lock",
    "not a result-bearing replication",
    "does not commit Bible text",
    "Project Gutenberg eBook 30 and eBook 124 RDF and plain-text checksums",
    "Source rows: 2.",
    "Metadata fetches OK: 2.",
    "Public-domain-USA rows: 2.",
    "Plain-text checksum rows: 2.",
    "Checksum records ready: 2.",
    f"KJV plain-text SHA-256: `{EXPECTED_KJV_PLAIN_SHA}`.",
    f"Apocrypha plain-text SHA-256: `{EXPECTED_APOCRYPHA_PLAIN_SHA}`.",
    "Source-use ready pages: 0.",
    "Verse-import ready pages: 0.",
    "Source-lock ready: 0.",
    "Result-ready: 0.",
    "`gutenberg_ebook_30_kjv_complete`",
    "`gutenberg_ebook_124_deuterocanonical`",
    "closes only the candidate checksum-record step",
    "does not close source-use, verse mapping, collation",
    "No Bible text is written to tracked outputs.",
    "does not change any KJVA bridge result status",
)
FORBIDDEN_OVERCLAIM_RE = re.compile(
    r"\b(?:source-lock ready|source-use approved|result-bearing replication is ready|"
    r"claim report|claim-level|proved|proves|proof|conclusive evidence|"
    r"significant finding)\b",
    re.IGNORECASE,
)
ALLOWED_FORBIDDEN_CONTEXTS = (
    "Source-lock ready: 0.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_kjva_gutenberg_candidate_checksum_sidecar_doc(
        args.doc,
        checksums=args.checksums,
        summary=args.summary,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"KJVA Gutenberg checksum sidecar failure: {failure}", file=sys.stderr)
        return 1
    print(f"KJVA Gutenberg checksum sidecar ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--checksums", type=Path, default=DEFAULT_CHECKSUMS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_kjva_gutenberg_candidate_checksum_sidecar_doc(
    doc: Path = DEFAULT_DOC,
    *,
    checksums: Path | None = DEFAULT_CHECKSUMS,
    summary: Path | None = DEFAULT_SUMMARY,
    manifest: Path | None = DEFAULT_MANIFEST,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    failures: list[str] = []
    for phrase in REQUIRED_PHRASES:
        if normalize_space(phrase) not in normalized:
            failures.append(f"{doc} missing phrase: {phrase}")
    failures.extend(validate_no_overclaim(doc, text))
    if checksums is not None:
        failures.extend(validate_checksums_csv(checksums))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest, doc=doc))
    return failures


def validate_checksums_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != sidecar.CHECKSUM_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 2:
        failures.append(f"{path} expected 2 checksum rows, found {len(rows)}")
        return failures
    by_id = {row["source_id"]: row for row in rows}
    expected = {
        "gutenberg_ebook_30_kjv_complete": {
            "component": "kjv_66_book_component",
            "ebook_no": "30",
            "plain_text_sha256": EXPECTED_KJV_PLAIN_SHA,
        },
        "gutenberg_ebook_124_deuterocanonical": {
            "component": "apocrypha_deuterocanon_component",
            "ebook_no": "124",
            "plain_text_sha256": EXPECTED_APOCRYPHA_PLAIN_SHA,
        },
    }
    for source_id, expected_values in expected.items():
        row = by_id.get(source_id)
        if row is None:
            failures.append(f"{path} missing source row {source_id}")
            continue
        for key, value in expected_values.items():
            if row.get(key) != value:
                failures.append(f"{path} {source_id} {key} drifted")
        if row.get("lock_status") != "checksum_record_ready_not_source_locked":
            failures.append(f"{path} {source_id} lock_status drifted")
        if row.get("result_boundary") != "not_result_bearing":
            failures.append(f"{path} {source_id} result_boundary drifted")
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != sidecar.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} expected 1 summary row, found {len(rows)}")
        return failures
    expected = {
        "source_rows": "2",
        "metadata_fetches_ok": "2",
        "public_domain_usa_rows": "2",
        "plain_text_rows": "2",
        "checksum_records_ready": "2",
        "kjv_plain_text_sha256": EXPECTED_KJV_PLAIN_SHA,
        "apocrypha_plain_text_sha256": EXPECTED_APOCRYPHA_PLAIN_SHA,
        "source_use_ready_pages": "0",
        "verse_import_ready_pages": "0",
        "source_lock_ready": "False",
        "result_ready": "False",
        "claim_status": "checksum_sidecar_only_not_result_bearing",
    }
    row = rows[0]
    for key, value in expected.items():
        if row.get(key) != value:
            failures.append(f"{path} {key} drifted: {row.get(key)!r}")
    return failures


def validate_manifest(path: Path, *, doc: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path} is invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        return [f"{path} JSON root must be an object"]
    failures: list[str] = []
    if payload.get("claim_boundary") != "checksum sidecar only; no ELS result":
        failures.append(f"{path} claim_boundary drifted")
    if payload.get("text_retention") != "no Bible text written to tracked outputs":
        failures.append(f"{path} text_retention drifted")
    outputs = payload.get("outputs", {})
    markdown = outputs.get("markdown") if isinstance(outputs, dict) else None
    allowed_markdown_paths = {str(doc)}
    try:
        allowed_markdown_paths.add(str(doc.relative_to(Path.cwd())))
    except ValueError:
        pass
    if markdown not in allowed_markdown_paths:
        failures.append(f"{path} markdown output drifted")
    return failures


def validate_no_overclaim(path: Path, text: str) -> list[str]:
    failures: list[str] = []
    for match in FORBIDDEN_OVERCLAIM_RE.finditer(text):
        line = text.count("\n", 0, match.start()) + 1
        line_text = text.splitlines()[line - 1].strip()
        if any(context in line_text for context in ALLOWED_FORBIDDEN_CONTEXTS):
            continue
        failures.append(f"{path}:{line} overclaim phrase: {match.group(0)!r}")
    return failures


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
