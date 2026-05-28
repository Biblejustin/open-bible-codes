#!/usr/bin/env python3
"""Validate Cities claim-catalog row stays source-review only."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_CATALOG = Path("claims/claim_catalog.csv")
DEFAULT_DOC = Path("docs/CLAIM_CATALOG.md")
DEFAULT_RECORDS = Path("data/study/mappings/cities_source_row_lock_decisions.csv")
CLAIM_ID = "cities_aumann_simon_mckay_source_chain"
EXPECTED_POPULATED_LOCK_ROWS = 1
EXPECTED_LOCKED_DECISION = {
    "decision_id": "cities_source_row_lock_001",
    "decision_status": "locked",
    "selected_action": "source_row_lock_ready",
}

REQUIRED_ROW_VALUES = {
    "claim_group": "torah_code_cities_source",
    "status": "under_specified",
    "language": "hebrew",
    "spellings_or_forms": "not imported",
    "skip_or_rule": "not locked",
    "evidence": "docs/CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md",
}
REQUIRED_ROW_PHRASES = {
    "current_reproduction": (
        "source-row lock handoff",
        "1 populated lock row",
        "no source rows imported",
    ),
    "notes": (
        "14 candidate pages",
        "source-review only",
        "no city-name normalization",
        "ELS searches",
        "compactness runs",
        "p-levels",
        "future lock rows must cite evidence and pass preflight",
    ),
}
REQUIRED_DOC_PHRASES = (
    "Torah-code.org Cities/Aumann/Simon-McKay source chain",
    "Cities source-row lock handoff has 14 source-row lock candidate pages",
    "1 populated lock row",
    "no source rows imported",
    "no city-name normalization, ELS searches, compactness runs, or p-levels",
    "data/study/mappings/cities_source_row_lock_decisions.csv",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_claim_catalog_boundary(
        args.catalog,
        args.doc,
        args.records,
    )
    if failures:
        for failure in failures:
            print(f"Cities claim-catalog boundary failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities claim-catalog boundary ok: {args.catalog}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--records", type=Path, default=DEFAULT_RECORDS)
    return parser


def validate_cities_claim_catalog_boundary(
    catalog: Path = DEFAULT_CATALOG,
    doc: Path = DEFAULT_DOC,
    records: Path = DEFAULT_RECORDS,
) -> list[str]:
    missing = [str(path) for path in (catalog, doc, records) if not path.exists()]
    if missing:
        return ["missing required files: " + ", ".join(missing)]

    failures: list[str] = []
    catalog_rows = read_csv(catalog)
    row_matches = [row for row in catalog_rows if row.get("claim_id") == CLAIM_ID]
    if len(row_matches) != 1:
        failures.append(
            f"{catalog} has {len(row_matches)} rows for {CLAIM_ID}, expected 1"
        )
        return failures

    row = row_matches[0]
    for field, expected in REQUIRED_ROW_VALUES.items():
        if row.get(field) != expected:
            failures.append(
                f"{catalog} {CLAIM_ID} {field}={row.get(field)!r}, expected {expected!r}"
            )
    for field, phrases in REQUIRED_ROW_PHRASES.items():
        value = normalize_space(row.get(field, ""))
        for phrase in phrases:
            if normalize_space(phrase) not in value:
                failures.append(
                    f"{catalog} {CLAIM_ID} {field} missing phrase: {phrase}"
                )

    record_rows = read_csv(records)
    if len(record_rows) != EXPECTED_POPULATED_LOCK_ROWS:
        failures.append(
            f"{records} has {len(record_rows)} populated rows, expected {EXPECTED_POPULATED_LOCK_ROWS}"
        )
    if record_rows:
        for expected_field, expected_value in EXPECTED_LOCKED_DECISION.items():
            actual = record_rows[0].get(expected_field, "")
            if actual != expected_value:
                failures.append(
                    f"{records} first row {expected_field}={actual!r}, expected {expected_value!r}"
                )

    doc_text = normalize_space(doc.read_text(encoding="utf-8"))
    for phrase in REQUIRED_DOC_PHRASES:
        if normalize_space(phrase) not in doc_text:
            failures.append(f"{doc} missing phrase: {phrase}")
    return failures


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
