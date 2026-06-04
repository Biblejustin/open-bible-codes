#!/usr/bin/env python3
"""Validate corpus config TOML structure without requiring local source files."""

from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path


CONFIGS_DIR = Path("configs")
ALLOW_EMPTY_CONFIGS = {"example_study.toml"}
SUPPORTED_LANGUAGES = {"english", "greek", "hebrew", "michigan"}
SUPPORTED_SOURCE_FORMATS = {
    "csv",
    "text",
    "michigan_claremont",
    "uxlc_dir",
    "oshb_wlc_dir",
    "sblgnt_text_dir",
    "mam_html_dir",
    "cntr_mes",
}
CSV_REQUIRED_FIELDS = {
    "name",
    "format",
    "path",
    "text_column",
    "ref_column",
    "book_column",
    "chapter_column",
    "verse_column",
}
TEXT_REQUIRED_FIELDS = {"name", "format", "path", "ref"}
GENERIC_SOURCE_REQUIRED_FIELDS = {"name", "format", "path"}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_corpus_configs(args.configs_dir)
    if failures:
        for failure in failures:
            print(f"corpus config failure: {failure}", file=sys.stderr)
        return 1
    print(f"corpus configs ok: {args.configs_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--configs-dir", type=Path, default=CONFIGS_DIR)
    return parser


def validate_corpus_configs(configs_dir: Path = CONFIGS_DIR) -> list[str]:
    if not configs_dir.exists():
        return [f"{configs_dir} is missing"]

    paths = sorted(configs_dir.glob("*.toml"))
    failures: list[str] = []
    if not paths:
        failures.append(f"{configs_dir} has no toml configs")
    for path in paths:
        failures.extend(validate_config(path))
    return failures


def validate_config(path: Path) -> list[str]:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        return [f"{path} invalid TOML: {exc}"]

    if not data:
        if path.name in ALLOW_EMPTY_CONFIGS:
            return []
        return [f"{path} is empty"]

    failures: list[str] = []
    name = clean(data.get("name"))
    language = clean(data.get("language"))
    sources = data.get("sources")

    if not name:
        failures.append(f"{path} missing name")
    if language not in SUPPORTED_LANGUAGES:
        failures.append(f"{path} unsupported language: {language}")
    if not isinstance(sources, list) or not sources:
        failures.append(f"{path} has no sources")
        return failures

    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict):
            failures.append(f"{path}:source {index} is not a table")
            continue
        failures.extend(validate_source(path, index, source))
    return failures


def validate_source(path: Path, index: int, source: dict[str, object]) -> list[str]:
    failures: list[str] = []
    source_format = clean(source.get("format"))
    if source_format not in SUPPORTED_SOURCE_FORMATS:
        failures.append(f"{path}:source {index} unsupported format: {source_format}")
        required = GENERIC_SOURCE_REQUIRED_FIELDS
    elif source_format == "csv":
        required = CSV_REQUIRED_FIELDS
    elif source_format == "text":
        required = TEXT_REQUIRED_FIELDS
    else:
        required = GENERIC_SOURCE_REQUIRED_FIELDS

    missing = [field for field in sorted(required) if not clean(source.get(field))]
    if missing:
        failures.append(
            f"{path}:source {index} missing required fields: {', '.join(missing)}"
        )
    return failures


def clean(value: object) -> str:
    return str(value or "").strip()


if __name__ == "__main__":
    raise SystemExit(main())
