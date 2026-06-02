#!/usr/bin/env python3
"""Validate CRD relevance dictionary coverage and lock metadata."""

from __future__ import annotations

import argparse
import csv
import sys
import tomllib
from pathlib import Path
from typing import Any

from scripts.classify_centered_relevance import CRDConfigurationError, load_relevance_dictionary, sha256_file


PLACEHOLDER_MARKERS = {"", "TEMPLATE", "TEMPLATE_REPLACE_WITH_FILE_SHA256_AFTER_LOCK"}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = check_dictionary(
            dictionary=args.dictionary,
            term_files=args.term_file,
            require_reviewed=args.require_reviewed,
            expected_sha256=args.expected_sha256,
        )
    except CRDConfigurationError as exc:
        print(f"CRD dictionary check failed: {exc}", file=sys.stderr)
        return 1
    print(f"entries={report['entries']}")
    print(f"term_rows={report['term_rows']}")
    print(f"missing_entries={report['missing_entries']}")
    print(f"extra_entries={report['extra_entries']}")
    print(f"sha256={report['sha256']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dictionary", type=Path, default=Path("terms/relevance_dictionary.toml"))
    parser.add_argument("--term-file", type=Path, action="append", required=True)
    parser.add_argument("--expected-sha256")
    parser.add_argument("--require-reviewed", action="store_true")
    return parser


def check_dictionary(
    *,
    dictionary: Path,
    term_files: list[Path],
    require_reviewed: bool = False,
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    try:
        raw = tomllib.loads(dictionary.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise CRDConfigurationError(f"dictionary invalid TOML: {exc}") from exc
    metadata = raw.get("metadata", {})
    if not isinstance(metadata, dict):
        raise CRDConfigurationError("dictionary metadata block is required")
    actual_sha = sha256_file(dictionary)
    if expected_sha256 and expected_sha256 != actual_sha:
        raise CRDConfigurationError(f"dictionary sha256 mismatch: expected {expected_sha256}, got {actual_sha}")
    if require_reviewed:
        validate_metadata_locked(metadata)
    entries = load_relevance_dictionary(dictionary)
    term_ids = term_ids_from_files(term_files)
    missing = sorted(term_ids - set(entries))
    extra = sorted(set(entries) - term_ids)
    if require_reviewed:
        if missing:
            raise CRDConfigurationError(f"dictionary missing term entries: {', '.join(missing[:20])}")
        for entry in entries.values():
            if all(not values for values in (entry.surface_keywords, entry.concept_codes, entry.verse_refs)):
                raise CRDConfigurationError(f"entry has no relevance criteria: {entry.term_id}")
            if entry.provenance.get("reviewer", "") in PLACEHOLDER_MARKERS:
                raise CRDConfigurationError(f"entry reviewer is not locked: {entry.term_id}")
    return {
        "entries": len(entries),
        "term_rows": len(term_ids),
        "missing_entries": len(missing),
        "extra_entries": len(extra),
        "sha256": actual_sha,
    }


def validate_metadata_locked(metadata: dict[str, Any]) -> None:
    for field in ("schema_version", "locked_by", "locked_at", "sha256", "drafted_with"):
        if str(metadata.get(field, "")).strip() in PLACEHOLDER_MARKERS:
            raise CRDConfigurationError(f"dictionary metadata field is not locked: {field}")


def term_ids_from_files(paths: list[Path]) -> set[str]:
    ids: set[str] = set()
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                term_id = row.get("term_id", "").strip()
                if term_id:
                    ids.add(term_id)
    return ids


if __name__ == "__main__":
    raise SystemExit(main())
