#!/usr/bin/env python3
"""Audit deuterocanon/apocrypha book coverage in configured corpora."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
import tomllib
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.normalization import normalize_text


DEFAULT_CONFIGS = [
    "LXX=configs/example_ebible_grclxx.toml",
    "KJV=configs/example_ebible_engkjv.toml",
    "KJVA=configs/example_ebible_engkjv_apocrypha.toml",
]
DEFAULT_OUT = Path("reports/apocrypha_coverage/coverage.csv")
DEFAULT_MARKDOWN = Path("docs/APOCRYPHA_SOURCE_COVERAGE.md")
DEFAULT_MANIFEST = Path("reports/apocrypha_coverage/manifest.json")

DEUTEROCANON_BOOKS = {
    "TOB": "Tobit",
    "JDT": "Judith",
    "ESG": "Greek Esther / Esther additions",
    "WIS": "Wisdom of Solomon",
    "SIR": "Sirach / Ecclesiasticus",
    "BAR": "Baruch",
    "LJE": "Letter of Jeremiah",
    "S3Y": "Song of the Three Young Men",
    "SUS": "Susanna",
    "BEL": "Bel and the Dragon",
    "DAG": "Greek Daniel / Daniel additions",
    "1MA": "1 Maccabees",
    "2MA": "2 Maccabees",
    "3MA": "3 Maccabees",
    "4MA": "4 Maccabees",
    "1ES": "1 Esdras",
    "2ES": "2 Esdras",
    "MAN": "Prayer of Manasseh",
    "ODA": "Odes",
    "PS2": "Psalm 151",
}

FIELDNAMES = [
    "corpus_label",
    "config",
    "corpus_name",
    "language",
    "book",
    "book_name",
    "present",
    "verses",
    "normalized_letters",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    if args.corpus is None:
        args.corpus = list(DEFAULT_CONFIGS)
    configs = [parse_label_config(value) for value in args.corpus]
    rows = []
    totals = []
    for label, config_path in configs:
        corpus_rows, total = audit_config(label, config_path)
        rows.extend(corpus_rows)
        totals.append(total)
    write_csv(args.out, rows)
    write_markdown(args.markdown_out, rows, totals, args)
    write_manifest(args.manifest_out, args, rows, totals, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", action="append")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def parse_label_config(value: str) -> tuple[str, Path]:
    if "=" not in value:
        path = Path(value)
        return path.stem, path
    label, config = value.split("=", 1)
    return label, Path(config)


def audit_config(label: str, config_path: Path) -> tuple[list[dict[str, object]], dict[str, object]]:
    config_path = config_path.expanduser()
    config = load_audit_config(config_path)
    language = config["language"]
    keep_finals = bool(config.get("keep_hebrew_final_forms", False))
    book_counts: Counter[str] = Counter()
    letter_counts: Counter[str] = Counter()
    for source in config["sources"]:
        if source.get("format") != "csv":
            continue
        path = (config_path.parent / source["path"]).resolve()
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                book = row.get(str(source.get("book_column", "book")), "")
                text = row.get(str(source.get("text_column", "text")), "")
                book_counts[book] += 1
                letter_counts[book] += len(
                    normalize_text(text, language, keep_hebrew_final_forms=keep_finals)
                )
    rows = []
    for book, book_name in DEUTEROCANON_BOOKS.items():
        rows.append(
            {
                "corpus_label": label,
                "config": str(config_path),
                "corpus_name": config.get("name", config_path.stem),
                "language": language,
                "book": book,
                "book_name": book_name,
                "present": "yes" if book_counts[book] else "no",
                "verses": book_counts[book],
                "normalized_letters": letter_counts[book],
            }
        )
    total = {
        "corpus_label": label,
        "config": str(config_path),
        "corpus_name": config.get("name", config_path.stem),
        "language": language,
        "present_books": sum(1 for book in DEUTEROCANON_BOOKS if book_counts[book]),
        "present_verses": sum(book_counts[book] for book in DEUTEROCANON_BOOKS),
        "present_letters": sum(letter_counts[book] for book in DEUTEROCANON_BOOKS),
    }
    return rows, total


def load_audit_config(config_path: Path) -> dict[str, Any]:
    try:
        with config_path.open("rb") as handle:
            config = tomllib.load(handle)
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"{config_path}: invalid TOML: {exc}") from exc

    language = config.get("language")
    if not isinstance(language, str) or not language.strip():
        raise ValueError(f"{config_path}: language must be a non-empty string")
    sources = config.get("sources", [])
    if not isinstance(sources, list):
        raise ValueError(f"{config_path}: sources must be a list")
    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict):
            raise ValueError(f"{config_path}: source #{index} must be a table")
        if source.get("format") != "csv":
            continue
        source_path = source.get("path")
        if not isinstance(source_path, str) or not source_path.strip():
            raise ValueError(f"{config_path}: source #{index} path must be a non-empty string")
    return config


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    totals: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    lines = [
        "# Apocrypha Source Coverage",
        "",
        "Status: source-coverage audit for completed apocrypha/deuterocanon",
        "bridge review layers. This is not an ELS result.",
        "",
        "## Reproduce",
        "",
        "```bash",
        reproduce_command(args),
        "```",
        "",
        "## Corpus Coverage Summary",
        "",
        "| Corpus | Language | Present books | Verses | Normalized letters |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for row in totals:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_md(str(row['corpus_label']))}`",
                    escape_md(str(row["language"])),
                    str(row["present_books"]),
                    str(row["present_verses"]),
                    str(row["present_letters"]),
                ]
            )
            + " |"
        )

    labels = [str(row["corpus_label"]) for row in totals]
    lines.extend(
        [
            "",
            "## Book Coverage",
            "",
            "| " + " | ".join(["Book", "Name", *labels]) + " |",
            "| " + " | ".join(["---", "---", *(["---:"] * len(labels))]) + " |",
        ]
    )
    by_book: dict[str, dict[str, dict[str, object]]] = {}
    for row in rows:
        by_book.setdefault(str(row["book"]), {})[str(row["corpus_label"])] = row
    for book, book_name in DEUTEROCANON_BOOKS.items():
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{book}`",
                    escape_md(book_name),
                    *(coverage_cell(by_book.get(book, {}).get(label, {})) for label in labels),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Read",
            "",
            "- The current eBible GRCLXX source already contains a substantial Greek",
            "  deuterocanon/apocrypha block.",
            "- The current eBible KJV source in this repo is a 66-book KJV stream and",
            "  does not contain a KJV Apocrypha block.",
            "- The eBible KJV + Apocrypha source is tracked as a separate corpus path",
            "  so English apocrypha runs do not silently alter prior KJV baselines.",
            "- Bridge-completion work can start with the existing LXX deuterocanon",
            "  before adding new manuscript/source families.",
            "- Any added source should get a separate license/provenance audit before",
            "  being included in claim-facing runs.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    totals: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "audit_apocrypha_coverage",
        "version": __version__,
        "generated_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "commit": git_commit(),
        "inputs": {"corpora": args.corpus},
        "outputs": {
            "coverage": str(args.out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "rows": len(rows),
        "totals": totals,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def reproduce_command(args: argparse.Namespace) -> str:
    corpora = " ".join(f"--corpus {value}" for value in args.corpus)
    return (
        f"python3 -m scripts.audit_apocrypha_coverage {corpora} "
        f"--out {args.out} --markdown-out {args.markdown_out} --manifest-out {args.manifest_out}"
    )


def coverage_cell(row: dict[str, object]) -> str:
    if not row or row.get("present") != "yes":
        return "absent"
    return f"{row['verses']} verses / {row['normalized_letters']} letters"


def escape_md(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
