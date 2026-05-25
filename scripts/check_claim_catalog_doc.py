#!/usr/bin/env python3
"""Validate claim-catalog markdown summary against the source CSV."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

DEFAULT_CATALOG = Path("claims/claim_catalog.csv")
DEFAULT_DOC = Path("docs/CLAIM_CATALOG.md")

ALLOWED_DOC_STATUSES = {
    "reproducible",
    "partially_reproducible",
    "controlled_review_candidate",
    "not_reproducible",
    "under_specified",
    "license_blocked",
    "mixed",
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_claim_catalog_doc(args.catalog, args.doc)
    if failures:
        for failure in failures:
            print(f"claim-catalog doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"claim-catalog doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_claim_catalog_doc(catalog: Path = DEFAULT_CATALOG, doc: Path = DEFAULT_DOC) -> list[str]:
    if not catalog.exists():
        return [f"{catalog} is missing"]
    if not doc.exists():
        return [f"{doc} is missing"]
    catalog_rows = read_catalog_rows(catalog)
    table_rows = parse_current_entries_table(doc.read_text(encoding="utf-8"))
    if not table_rows:
        return [f"{doc} has no Current Entries table rows"]
    failures: list[str] = []
    entry_total = 0
    for row in table_rows:
        status = unquote_code(row["status"])
        if status not in ALLOWED_DOC_STATUSES:
            failures.append(f"{doc} has unknown Current Entries status: {status}")
        try:
            entries = int(row["entries"])
        except ValueError:
            failures.append(f"{doc} has non-integer entry count for {row['group']}: {row['entries']}")
            continue
        if entries <= 0:
            failures.append(f"{doc} has non-positive entry count for {row['group']}: {entries}")
        entry_total += entries
    if entry_total != len(catalog_rows):
        failures.append(
            f"{doc} Current Entries total is {entry_total}, but {catalog} has {len(catalog_rows)} rows"
        )
    if "claims/claim_catalog.csv" not in doc.read_text(encoding="utf-8"):
        failures.append(f"{doc} does not cite claims/claim_catalog.csv")
    return failures


def read_catalog_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_current_entries_table(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    in_section = False
    for line in text.splitlines():
        if line == "## Current Entries":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section or not line.startswith("|"):
            continue
        if line.startswith("| ---") or line.startswith("| Group"):
            continue
        parts = [part.strip() for part in line.strip().strip("|").split(" | ")]
        if len(parts) != 4:
            continue
        group, status, entries, current_read = parts
        rows.append(
            {
                "group": group,
                "status": status,
                "entries": entries,
                "current_read": current_read,
            }
        )
    return rows


def unquote_code(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return value


if __name__ == "__main__":
    raise SystemExit(main())
