#!/usr/bin/env python3
"""Validate Project Gutenberg KJVA source-lock prep boundaries."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from scripts import analyze_kjva_gutenberg_source_lock_prep as prep


DEFAULT_DOC = prep.DEFAULT_MD
DEFAULT_ROWS = prep.DEFAULT_ROWS
DEFAULT_SUMMARY = prep.DEFAULT_SUMMARY
DEFAULT_ANCHORS = prep.DEFAULT_ANCHORS
DEFAULT_MANIFEST = prep.DEFAULT_MANIFEST

REQUIRED_PHRASES = (
    "# KJVA Gutenberg Source-Lock Prep",
    "Status: source-lock prep only.",
    "not an ELS result",
    "not a corpus import",
    "not a source lock",
    "not a result-bearing replication",
    "does not commit Bible text, normalize Bible text, create a local corpus",
    "Raw text retained: 0.",
    "Local KJVA books counted: 80.",
    "Local KJVA verses counted: 36822.",
    "Local KJV verses counted: 31102.",
    "Local Apocrypha/deuterocanon verses counted: 5720.",
    "Book-shape rows written: 81.",
    "Local book rows compared: 80.",
    "KJV books compared: 66.",
    "KJV exact count matches: 66.",
    "KJV count drifts: 0.",
    "Apocrypha/deuterocanon books compared: 14.",
    "Apocrypha/deuterocanon exact count matches: 12.",
    "Apocrypha/deuterocanon count drifts: 2.",
    "Extra source sections: 1.",
    "Gutenberg KJV verse markers: 31102.",
    "Gutenberg Apocrypha/deuterocanon chapter:verse markers: 5636.",
    "Gutenberg Apocrypha/deuterocanon number-only markers: 68.",
    "Gutenberg Apocrypha/deuterocanon total verse-like markers: 5704.",
    "Baruch/Epistle split detected: 1.",
    "Source-lock ready: 0.",
    "Result-ready sources: 0.",
    "Project Gutenberg eBook 30 has exact verse-count agreement",
    "12 of 14 tracked Apocrypha/deuterocanon books",
    "Sirach at one fewer source marker",
    "Prayer of Manasseh with no verse markers",
    "Epistle of Jeremiah",
    "needs a real collation and source-use lock",
    "does not change any KJVA bridge result status",
)
FORBIDDEN_OVERCLAIM_RE = re.compile(
    r"\b(?:source-lock ready|result-bearing replication is ready|claim report|"
    r"claim-level|proved|proves|proof|conclusive evidence|significant finding)\b",
    re.IGNORECASE,
)
ALLOWED_FORBIDDEN_CONTEXTS = (
    "Source-lock ready: 0.",
    "Status: source-lock prep only.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_kjva_gutenberg_source_lock_prep_doc(
        args.doc,
        rows=args.rows,
        summary=args.summary,
        anchors=args.anchors,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"KJVA Gutenberg source-lock prep failure: {failure}", file=sys.stderr)
        return 1
    print(f"KJVA Gutenberg source-lock prep ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--anchors", type=Path, default=DEFAULT_ANCHORS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_kjva_gutenberg_source_lock_prep_doc(
    doc: Path = DEFAULT_DOC,
    *,
    rows: Path | None = DEFAULT_ROWS,
    summary: Path | None = DEFAULT_SUMMARY,
    anchors: Path | None = DEFAULT_ANCHORS,
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
    if rows is not None:
        failures.extend(validate_rows_csv(rows))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if anchors is not None:
        failures.extend(validate_anchors_csv(anchors))
    if manifest is not None:
        failures.extend(validate_manifest(manifest, doc=doc))
    return failures


def validate_rows_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != prep.ROW_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 81:
        failures.append(f"{path} expected 81 rows, found {len(rows)}")
    kjv_rows = [row for row in rows if row.get("section") == "kjv"]
    apocrypha_rows = [row for row in rows if row.get("section") == "apocrypha"]
    extra_rows = [
        row for row in rows if row.get("section") == "apocrypha_extra_source_section"
    ]
    if len(kjv_rows) != 66:
        failures.append(f"{path} expected 66 KJV rows, found {len(kjv_rows)}")
    if len(apocrypha_rows) != 14:
        failures.append(f"{path} expected 14 apocrypha rows, found {len(apocrypha_rows)}")
    if len(extra_rows) != 1:
        failures.append(f"{path} expected 1 extra source row, found {len(extra_rows)}")
    if any(row.get("status") != "exact_count_match" for row in kjv_rows):
        failures.append(f"{path} expected all KJV rows to be exact_count_match")
    drift_books = sorted(
        row["book"] for row in apocrypha_rows if row.get("status") != "exact_count_match"
    )
    if drift_books != ["MAN", "SIR"]:
        failures.append(f"{path} apocrypha drift books changed: {drift_books}")
    baruch = next((row for row in apocrypha_rows if row.get("book") == "BAR"), None)
    if not baruch or baruch.get("gutenberg_marker_count") != "213":
        failures.append(f"{path} BAR combined source count drifted")
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != prep.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} expected 1 summary row, found {len(rows)}")
        return failures
    expected = {
        "source_pages": "2",
        "plain_text_pages_scanned": "2",
        "raw_text_retained": "False",
        "local_kjva_books": "80",
        "local_kjva_verses": "36822",
        "local_kjva_kjv_verses": "31102",
        "local_kjva_apocrypha_verses": "5720",
        "book_shape_rows": "81",
        "local_book_rows_compared": "80",
        "kjv_books_compared": "66",
        "kjv_books_exact_count_matches": "66",
        "kjv_books_count_drift": "0",
        "apocrypha_books_compared": "14",
        "apocrypha_books_exact_count_matches": "12",
        "apocrypha_books_count_drift": "2",
        "extra_source_sections": "1",
        "gutenberg_kjv_verse_markers": "31102",
        "gutenberg_apocrypha_chapter_verse_markers": "5636",
        "gutenberg_apocrypha_number_only_markers": "68",
        "gutenberg_apocrypha_total_verse_like_markers": "5704",
        "baruch_epistle_split_detected": "True",
        "source_lock_ready": "False",
        "result_ready": "False",
        "claim_status": "source_lock_prep_only_not_result_bearing",
    }
    row = rows[0]
    for key, value in expected.items():
        if row.get(key) != value:
            failures.append(f"{path} {key} drifted: {row.get(key)!r}")
    return failures


def validate_anchors_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != prep.ANCHOR_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 6:
        failures.append(f"{path} expected 6 anchors, found {len(rows)}")
    missing = [row["anchor"] for row in rows if row.get("status") != "found"]
    if missing:
        failures.append(f"{path} missing anchors: {', '.join(missing)}")
    return failures


def validate_manifest(path: Path, *, doc: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path} is invalid JSON: {exc}"]
    failures: list[str] = []
    if payload.get("claim_boundary") != "source-lock prep only; no ELS result":
        failures.append(f"{path} claim_boundary drifted")
    if (
        payload.get("text_retention")
        != "plain text scanned in memory or ignored local path; Bible text not committed"
    ):
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
