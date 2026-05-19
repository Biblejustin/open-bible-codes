#!/usr/bin/env python3
"""Run local-only checks for BibleGateway English version stubs."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
import tomllib
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


DEFAULT_VERSIONS = Path("configs/biblegateway_english_versions.csv")
DEFAULT_TERMS = Path("terms/english_search_terms.csv")
DEFAULT_OUT_DIR = Path("reports/biblegateway_english_versions")
SOURCE_URL = "https://www.biblegateway.com/versions/"


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    started = time.perf_counter()
    versions = read_versions(args.versions)
    included, missing = resolve_versions(versions, args)
    write_version_rows(args.out_dir / "included_versions.csv", included)
    write_version_rows(args.out_dir / "missing_versions.csv", missing)

    if args.require_all and missing:
        raise SystemExit(
            f"missing {len(missing)} local version files; see {args.out_dir / 'missing_versions.csv'}"
        )
    if not included:
        raise SystemExit("no available English version corpora")

    generated_configs = build_generated_configs(included, args.out_dir)
    corpus_args = [
        f"{row['label']}={generated_configs[row['label']]}"
        for row in included
    ]
    if args.dry_run:
        for raw in corpus_args:
            print(f"--corpus {raw}")
        print(f"included={len(included)} missing={len(missing)}")
        return 0

    run_batch(args, corpus_args)
    run_presence(args)
    write_manifest(args, included, missing, started)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--versions", type=Path, default=DEFAULT_VERSIONS)
    parser.add_argument("--terms", type=Path, default=DEFAULT_TERMS)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=100)
    parser.add_argument(
        "--direction",
        choices=["forward", "backward", "both"],
        default="both",
    )
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--corpus-jobs", type=int, default=1)
    parser.add_argument("--require-all", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def read_versions(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def resolve_versions(
    versions: list[dict[str, str]],
    args: argparse.Namespace,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    included = []
    missing = []
    for row in versions:
        config_path = resolved_optional_path(row.get("config_path", ""))
        local_csv = resolved_optional_path(row.get("local_csv", ""))
        copied = dict(row)
        if config_path and config_path.exists():
            missing_sources = missing_config_sources(config_path)
            if not missing_sources:
                copied["resolved_config_path"] = str(config_path)
                copied["resolved_local_csv"] = ""
                copied["missing_reason"] = ""
                included.append(copied)
            else:
                copied["resolved_config_path"] = str(config_path)
                copied["resolved_local_csv"] = str(local_csv) if local_csv else ""
                copied["missing_reason"] = "missing config sources: " + "; ".join(
                    missing_sources
                )
                missing.append(copied)
        elif local_csv and local_csv.exists():
            copied["resolved_config_path"] = ""
            copied["resolved_local_csv"] = str(local_csv)
            copied["missing_reason"] = ""
            included.append(copied)
        else:
            copied["resolved_config_path"] = str(config_path) if config_path else ""
            copied["resolved_local_csv"] = str(local_csv) if local_csv else ""
            copied["missing_reason"] = "missing config and local CSV"
            missing.append(copied)
    return included, missing


def resolved_optional_path(value: str) -> Path | None:
    value = value.strip()
    if not value:
        return None
    return Path(value).expanduser().resolve()


def missing_config_sources(config_path: Path) -> list[str]:
    try:
        with config_path.open("rb") as handle:
            config = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        return [f"{config_path}: {exc}"]

    missing = []
    sources = config.get("sources", [])
    if not isinstance(sources, list):
        return [f"{config_path}: sources must be a list"]
    for source in sources:
        if not isinstance(source, dict) or not isinstance(source.get("path"), str):
            continue
        source_path = resolve_config_path(config_path.parent, source["path"])
        if not source_path.exists():
            missing.append(str(source_path))
    return missing


def resolve_config_path(base_dir: Path, configured_path: str) -> Path:
    path = Path(configured_path).expanduser()
    if not path.is_absolute():
        path = base_dir / path
    return path.resolve()


def write_version_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    base_fieldnames = [
        "label",
        "name",
        "config_path",
        "local_csv",
        "coverage",
        "ot_basis",
        "nt_basis",
        "source_family",
        "basis_status",
        "notes",
        "resolved_config_path",
        "resolved_local_csv",
        "missing_reason",
    ]
    extra_fieldnames = sorted(
        {
            key
            for row in rows
            for key in row
            if key not in base_fieldnames
        }
    )
    fieldnames = base_fieldnames + extra_fieldnames
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def build_generated_configs(
    included: list[dict[str, str]],
    out_dir: Path,
) -> dict[str, str]:
    generated_dir = out_dir / "generated_configs"
    generated_dir.mkdir(parents=True, exist_ok=True)
    configs = {}
    for row in included:
        label = row["label"]
        existing_config = row.get("resolved_config_path", "")
        if existing_config:
            configs[label] = existing_config
            continue
        local_csv = row["resolved_local_csv"]
        config_path = generated_dir / f"{label.lower()}.toml"
        config_path.write_text(render_config(row, local_csv), encoding="utf-8")
        configs[label] = str(config_path.resolve())
    return configs


def render_config(row: dict[str, str], local_csv: str) -> str:
    return "\n".join(
        [
            f"name = {toml_string('Local Private English ' + row['label'])}",
            'language = "english"',
            "",
            "[[sources]]",
            f"name = {toml_string(row['label'])}",
            'format = "csv"',
            f"path = {toml_string(local_csv)}",
            'text_column = "text"',
            'ref_column = "ref"',
            'book_column = "book"',
            'chapter_column = "chapter"',
            'verse_column = "verse"',
            "",
        ]
    )


def toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def run_batch(args: argparse.Namespace, corpus_args: list[str]) -> None:
    cmd = [
        sys.executable,
        "-m",
        "els",
        "batch-many",
        "--term-set",
        f"english_search_terms={args.terms}",
    ]
    for corpus in corpus_args:
        cmd.extend(["--corpus", corpus])
    cmd.extend(
        [
            "--min-skip",
            str(args.min_skip),
            "--max-skip",
            str(args.max_skip),
            "--direction",
            args.direction,
            "--jobs",
            str(args.jobs),
            "--corpus-jobs",
            str(args.corpus_jobs),
            "--out-dir",
            str(args.out_dir),
            "--manifest-out",
            str(args.out_dir / "biblegateway_english_versions.manifest.json"),
        ]
    )
    subprocess.run(cmd, check=True)


def run_presence(args: argparse.Namespace) -> None:
    cmd = [
        sys.executable,
        "-m",
        "scripts.analyze_broad_version_presence",
        "--counts-dir",
        str(args.out_dir),
        "--summary-out",
        str(args.out_dir / "version_presence.csv"),
        "--markdown-out",
        str(args.out_dir / "version_presence.md"),
        "--manifest-out",
        str(args.out_dir / "version_presence.manifest.json"),
    ]
    subprocess.run(cmd, check=True)


def write_manifest(
    args: argparse.Namespace,
    included: list[dict[str, str]],
    missing: list[dict[str, str]],
    started: float,
) -> None:
    manifest = {
        "tool": "run_biblegateway_english_versions",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "source_url": SOURCE_URL,
        "versions_manifest": str(args.versions.resolve()),
        "terms": str(args.terms.resolve()),
        "out_dir": str(args.out_dir.resolve()),
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "direction": args.direction,
        "included_versions": len(included),
        "missing_versions": len(missing),
        "included_labels": [row["label"] for row in included],
        "missing_labels": [row["label"] for row in missing],
        "seconds": round(time.perf_counter() - started, 3),
    }
    path = args.out_dir / "run_biblegateway_english_versions.manifest.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
