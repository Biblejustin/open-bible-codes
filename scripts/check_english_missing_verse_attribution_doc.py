#!/usr/bin/env python3
"""Validate English missing-verse attribution docs and report shape."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


DEFAULT_DOC = Path("docs/ENGLISH_MISSING_VERSE_ATTRIBUTION.md")
DEFAULT_SUMMARY = Path("reports/english_missing_verse_attribution/summary.csv")
DEFAULT_MISSING_REFS = Path("reports/english_missing_verse_attribution/missing_refs.csv")
DEFAULT_CONTEXT = Path("reports/english_missing_verse_attribution/context_hit_attribution.csv")
DEFAULT_MANIFEST = Path("reports/english_missing_verse_attribution/manifest.json")

SUMMARY_COLUMNS = (
    "version_label",
    "version_name",
    "missing_kjv_refs",
    "known_nt_disputed_kjv_refs",
    "other_reference_gaps",
    "result",
)
MISSING_REF_COLUMNS = (
    "version_label",
    "ref",
    "kjv_norm_length",
    "ref_gap_category",
)
CONTEXT_COLUMNS = (
    "corpus",
    "normalized_term",
    "start_ref",
    "end_ref",
    "missing_refs_in_augmented_span",
    "missing_verse_attribution",
)
DOC_PHRASES = (
    "# English Missing-Verse Attribution",
    "`protocols/english_missing_verse_attribution.toml`",
    "`scripts/analyze_english_missing_verse_attribution.py`",
    "Reference gaps are broader than textual omissions.",
    "current reviewed English hits are not explained by missing-verse gaps",
    "Comma Johanneum",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate(
        doc=args.doc,
        summary=args.summary,
        missing_refs=args.missing_refs,
        context=args.context,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"English missing-verse attribution failure: {failure}", file=sys.stderr)
        return 1
    print("English missing-verse attribution doc ok")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--missing-refs", type=Path, default=DEFAULT_MISSING_REFS)
    parser.add_argument("--context", type=Path, default=DEFAULT_CONTEXT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate(
    *,
    doc: Path = DEFAULT_DOC,
    summary: Path = DEFAULT_SUMMARY,
    missing_refs: Path = DEFAULT_MISSING_REFS,
    context: Path = DEFAULT_CONTEXT,
    manifest: Path = DEFAULT_MANIFEST,
) -> list[str]:
    failures: list[str] = []
    manifest_data = read_json(manifest)
    if isinstance(manifest_data, str):
        return [manifest_data]
    summary_data = read_csv(summary)
    if isinstance(summary_data, str):
        return [summary_data]
    missing_ref_data = read_csv(missing_refs)
    if isinstance(missing_ref_data, str):
        return [missing_ref_data]
    context_data = read_csv(context)
    if isinstance(context_data, str):
        return [context_data]

    summary_fields, summary_rows = summary_data
    missing_fields, missing_rows = missing_ref_data
    context_fields, context_rows = context_data
    failures.extend(require_columns(summary, summary_fields, SUMMARY_COLUMNS))
    failures.extend(require_columns(missing_refs, missing_fields, MISSING_REF_COLUMNS))
    failures.extend(require_columns(context, context_fields, CONTEXT_COLUMNS))
    failures.extend(validate_report_counts(manifest_data, summary_rows, missing_rows, context_rows))
    failures.extend(validate_doc(doc, manifest_data))
    return failures


def validate_report_counts(
    manifest: dict[str, Any],
    summary_rows: list[dict[str, str]],
    missing_rows: list[dict[str, str]],
    context_rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    if len(summary_rows) != int(manifest["included_versions"]):
        failures.append("summary row count does not match manifest included_versions")
    if len(context_rows) != int(manifest["context_hit_rows"]):
        failures.append("context row count does not match manifest context_hit_rows")
    context_attributed = sum(
        row["missing_verse_attribution"] == "missing_verse_attributed"
        for row in context_rows
    )
    if context_attributed != int(manifest["context_missing_verse_attributed_rows"]):
        failures.append("context attribution count does not match manifest")
    categories = Counter(row["ref_gap_category"] for row in missing_rows)
    known = categories["known_nt_disputed_kjv_ref"]
    other = categories["other_reference_gap"]
    if known != int(manifest["known_nt_disputed_kjv_ref_rows"]):
        failures.append("known disputed ref count does not match manifest")
    if other != int(manifest["other_reference_gap_rows"]):
        failures.append("other reference gap count does not match manifest")
    if known + other != len(missing_rows):
        failures.append("missing ref categories do not cover every row")
    summary_known = sum(int(row["known_nt_disputed_kjv_refs"]) for row in summary_rows)
    summary_other = sum(int(row["other_reference_gaps"]) for row in summary_rows)
    if summary_known != known:
        failures.append("summary known disputed total does not match missing_refs")
    if summary_other != other:
        failures.append("summary other reference total does not match missing_refs")
    return failures


def validate_doc(doc: Path, manifest: dict[str, Any]) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = normalize_space(doc.read_text(encoding="utf-8"))
    failures = [f"{doc} missing phrase: {phrase}" for phrase in DOC_PHRASES if phrase not in text]
    required_dynamic = (
        f"Available BibleGateway-overlap English versions checked: {manifest['included_versions']}.",
        f"Missing BibleGateway versions skipped: {manifest['missing_versions']}.",
        f"Versions with at least one KJV reference absent: {manifest['versions_with_missing_kjv_refs']}.",
        "Reference-gap rows: "
        f"{manifest['known_nt_disputed_kjv_ref_rows'] + manifest['other_reference_gap_rows']:,}.",
        "Known New Testament disputed KJV-reference rows: "
        f"{manifest['known_nt_disputed_kjv_ref_rows']} across "
        f"{manifest['versions_with_known_nt_disputed_kjv_refs']} versions.",
        f"Current context-review rows checked: {manifest['context_hit_rows']}.",
        "Context-review rows attributed to missing verses: "
        f"{manifest['context_missing_verse_attributed_rows']}.",
    )
    failures.extend(
        f"{doc} missing current value: {phrase}" for phrase in required_dynamic if phrase not in text
    )
    return failures


def require_columns(path: Path, fieldnames: list[str], required: tuple[str, ...]) -> list[str]:
    missing = [column for column in required if column not in fieldnames]
    return [f"{path} missing column: {column}" for column in missing]


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
