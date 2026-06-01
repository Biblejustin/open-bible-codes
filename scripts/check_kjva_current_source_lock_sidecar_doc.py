#!/usr/bin/env python3
"""Validate current eBible KJVA source-lock sidecar boundaries."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from scripts import build_kjva_current_source_lock_sidecar as sidecar


DEFAULT_DOC = sidecar.DEFAULT_MD
DEFAULT_BOOK_SHAPE = sidecar.DEFAULT_BOOK_SHAPE
DEFAULT_SUMMARY = sidecar.DEFAULT_SUMMARY
DEFAULT_MANIFEST = sidecar.DEFAULT_MANIFEST

EXPECTED_FULL_ORDER = "GEN;EXO;LEV;NUM;DEU;JOS;JDG;RUT;1SA;2SA;1KI;2KI;1CH;2CH;EZR;NEH;EST;JOB;PSA;PRO;ECC;SNG;ISA;JER;LAM;EZK;DAN;HOS;JOL;AMO;OBA;JON;MIC;NAM;HAB;ZEP;HAG;ZEC;MAL;TOB;JDT;ESG;WIS;SIR;BAR;S3Y;SUS;BEL;1MA;2MA;1ES;MAN;2ES;MAT;MRK;LUK;JHN;ACT;ROM;1CO;2CO;GAL;EPH;PHP;COL;1TH;2TH;1TI;2TI;TIT;PHM;HEB;JAS;1PE;2PE;1JN;2JN;3JN;JUD;REV"
EXPECTED_APOCRYPHA_ORDER = "TOB;JDT;ESG;WIS;SIR;BAR;S3Y;SUS;BEL;1MA;2MA;1ES;MAN;2ES"
EXPECTED_CSV_SHA256 = "f4f4549c7323de20a6cdd7aa74aeae32d184b2b6a1a51cd41390540efd710360"
EXPECTED_ZIP_SHA256 = "0ec30ed796dbc1aea401c497359a9e115077c7d72bf19d3dbf93f20acd784f8b"

REQUIRED_PHRASES = (
    "# KJVA Current Source Lock Sidecar",
    "Status: current-source rerun sidecar only.",
    "not an ELS result",
    "not a new corpus import",
    "not an independent replication source",
    "not a result-bearing run",
    "does not commit Bible text",
    "current eBible KJV + Apocrypha rerun baseline",
    f"ZIP SHA-256: `{EXPECTED_ZIP_SHA256}`.",
    f"CSV SHA-256: `{EXPECTED_CSV_SHA256}`.",
    "Books: 80.",
    "Verses: 36822.",
    "Apocrypha/deuterocanon books: 14.",
    "Apocrypha/deuterocanon verses: 5720.",
    "Apocrypha/deuterocanon normalized letters: 593090.",
    "Rerun baseline locked: 1.",
    "Independent source-lock ready: 0.",
    "Result-ready: 0.",
    f"Full book order: `{EXPECTED_FULL_ORDER}`.",
    f"Apocrypha/deuterocanon book order: `{EXPECTED_APOCRYPHA_ORDER}`.",
    "does not make Hakkaac, Project Gutenberg, CrossWire, Wikisource, or Open-Bibles source-ready",
    "does not change any KJVA bridge result status",
)
FORBIDDEN_OVERCLAIM_RE = re.compile(
    r"\b(?:independent replication source is ready|result-bearing run is ready|"
    r"claim report|claim-level|proved|proves|proof|conclusive evidence|"
    r"significant finding)\b",
    re.IGNORECASE,
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_kjva_current_source_lock_sidecar_doc(
        args.doc,
        book_shape=args.book_shape,
        summary=args.summary,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"KJVA current source sidecar failure: {failure}", file=sys.stderr)
        return 1
    print(f"KJVA current source sidecar ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--book-shape", type=Path, default=DEFAULT_BOOK_SHAPE)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_kjva_current_source_lock_sidecar_doc(
    doc: Path = DEFAULT_DOC,
    *,
    book_shape: Path | None = DEFAULT_BOOK_SHAPE,
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
    if book_shape is not None:
        failures.extend(validate_book_shape_csv(book_shape))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest, doc=doc))
    return failures


def validate_book_shape_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != sidecar.BOOK_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 80:
        failures.append(f"{path} expected 80 book rows, found {len(rows)}")
    apocrypha_rows = [row for row in rows if row.get("is_apocrypha") == "True"]
    if len(apocrypha_rows) != 14:
        failures.append(f"{path} expected 14 apocrypha rows, found {len(apocrypha_rows)}")
    order = ";".join(row["book"] for row in rows)
    if order != EXPECTED_FULL_ORDER:
        failures.append(f"{path} full book order drifted")
    apocrypha_order = ";".join(row["book"] for row in apocrypha_rows)
    if apocrypha_order != EXPECTED_APOCRYPHA_ORDER:
        failures.append(f"{path} apocrypha book order drifted")
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
        "source_id": "eng-kjv",
        "source_name": "eBible English KJV + Apocrypha",
        "zip_sha256": EXPECTED_ZIP_SHA256,
        "csv_sha256": EXPECTED_CSV_SHA256,
        "csv_bytes": "5705852",
        "book_count": "80",
        "verse_count": "36822",
        "apocrypha_book_count": "14",
        "apocrypha_verse_count": "5720",
        "apocrypha_normalized_letters": "593090",
        "full_book_order": EXPECTED_FULL_ORDER,
        "apocrypha_book_order": EXPECTED_APOCRYPHA_ORDER,
        "rerun_baseline_locked": "True",
        "independent_source_lock_ready": "False",
        "result_ready": "False",
        "claim_status": "current_source_rerun_sidecar_only_not_result_bearing",
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
    failures: list[str] = []
    if payload.get("claim_boundary") != "current-source rerun sidecar only; no ELS result":
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
