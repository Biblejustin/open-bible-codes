#!/usr/bin/env python3
"""Validate committed term files before release/report runs."""

from __future__ import annotations

import argparse
import csv
import sys
import tomllib
from pathlib import Path

from els.normalization import normalize_text


TERMS_DIR = Path("terms")
REQUIRED_TERM_FIELDS = {"term_id", "concept", "category", "language", "term"}
SUPPORTED_LANGUAGES = {"hebrew", "greek", "michigan", "english"}
NON_TERM_METADATA_FILES = {"meaningful_constants.csv"}
ALLOW_EMPTY_TERM_FILES = {"english_seed_followup_survivors.csv"}
REQUIRED_CONSTANT_FIELDS = {"constant_id", "value", "label", "category", "notes"}
REQUIRED_CONSTANT_VALUES = {7, 12, 22, 26, 40, 42, 50, 70, 144, 666}
REQUIRED_GEMATRIA_SCHEMES = {"hebrew_standard", "greek_standard"}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_term_files(args.terms_dir)
    if failures:
        for failure in failures:
            print(f"term file failure: {failure}", file=sys.stderr)
        return 1
    print(f"term files ok: {args.terms_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terms-dir", type=Path, default=TERMS_DIR)
    return parser


def validate_term_files(terms_dir: Path = TERMS_DIR) -> list[str]:
    failures: list[str] = []
    if not terms_dir.exists():
        return [f"{terms_dir} is missing"]

    term_paths = [
        path
        for path in sorted(terms_dir.glob("*.csv"))
        if path.name not in NON_TERM_METADATA_FILES
    ]
    if not term_paths:
        failures.append(f"{terms_dir} has no term csv files")
    for path in term_paths:
        failures.extend(validate_term_csv(path))

    failures.extend(validate_meaningful_constants(terms_dir / "meaningful_constants.csv"))
    failures.extend(validate_gematria_schemes(terms_dir / "gematria_schemes.toml"))
    return failures


def validate_term_csv(path: Path) -> list[str]:
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    missing = REQUIRED_TERM_FIELDS - set(fieldnames)
    if missing:
        return [f"{path} missing required columns: {', '.join(sorted(missing))}"]

    if not rows:
        if path.name not in ALLOW_EMPTY_TERM_FILES:
            failures.append(f"{path} has no rows")
        return failures

    seen_ids: set[str] = set()
    for row_number, row in enumerate(rows, start=2):
        if None in row:
            failures.append(f"{path}:{row_number} has extra unnamed columns")
        if any(value is None for value in row.values()):
            failures.append(f"{path}:{row_number} has missing cell values")

        for column in sorted(REQUIRED_TERM_FIELDS):
            value = clean(row.get(column))
            if not value:
                failures.append(f"{path}:{row_number} missing {column}")

        term_id = clean(row.get("term_id"))
        if term_id in seen_ids:
            failures.append(f"{path}:{row_number} duplicate term_id: {term_id}")
        seen_ids.add(term_id)

        language = clean(row.get("language"))
        if language and language not in SUPPORTED_LANGUAGES:
            failures.append(f"{path}:{row_number} unsupported language: {language}")
            continue

        term = clean(row.get("term"))
        if language and term:
            normalized = normalize_text(term, language)
            if not normalized and "digits are removed" not in clean(row.get("notes")):
                failures.append(
                    f"{path}:{row_number} normalizes to empty letters: {term_id}"
                )
    return failures


def validate_meaningful_constants(path: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    missing = REQUIRED_CONSTANT_FIELDS - set(reader.fieldnames or [])
    if missing:
        return [f"{path} missing required columns: {', '.join(sorted(missing))}"]
    if not rows:
        return [f"{path} has no rows"]

    failures: list[str] = []
    values: list[int] = []
    for row_number, row in enumerate(rows, start=2):
        raw_value = clean(row.get("value"))
        try:
            values.append(int(raw_value))
        except ValueError:
            failures.append(f"{path}:{row_number} value is not integer: {raw_value}")
    if len(values) != len(set(values)):
        failures.append(f"{path} has duplicate values")
    missing_required = REQUIRED_CONSTANT_VALUES - set(values)
    if missing_required:
        failures.append(
            f"{path} missing required values: {', '.join(str(v) for v in sorted(missing_required))}"
        )
    return failures


def validate_gematria_schemes(path: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        return [f"{path} is invalid TOML: {error}"]
    schemes = data.get("schemes", [])
    failures: list[str] = []
    scheme_ids = {clean(scheme.get("scheme_id")) for scheme in schemes}
    missing_schemes = REQUIRED_GEMATRIA_SCHEMES - scheme_ids
    if missing_schemes:
        failures.append(
            f"{path} missing required schemes: {', '.join(sorted(missing_schemes))}"
        )
    for index, scheme in enumerate(schemes, start=1):
        scheme_id = clean(scheme.get("scheme_id"))
        language = clean(scheme.get("language"))
        implementation = clean(scheme.get("implementation"))
        status = clean(scheme.get("status"))
        if language not in {"hebrew", "greek"}:
            failures.append(f"{path}:scheme {index} unsupported language: {language}")
        if not implementation.startswith("els.gematria."):
            failures.append(f"{path}:scheme {index} bad implementation: {scheme_id}")
        if status != "implemented":
            failures.append(f"{path}:scheme {index} status not implemented: {scheme_id}")
    return failures


def clean(value: object) -> str:
    return str(value or "").strip()


if __name__ == "__main__":
    raise SystemExit(main())
