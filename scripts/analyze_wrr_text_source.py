#!/usr/bin/env python3
"""Fingerprint the Koren Genesis source text used by WRR audit smoke runs."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import time
import tomllib
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import load_corpus


CONFIG = Path("configs/example_koren_genesis.toml")
OUT = Path("reports/wrr_1994/koren_genesis_text_source.csv")
MD_OUT = Path("reports/wrr_1994/koren_genesis_text_source.md")
MANIFEST_OUT = Path("reports/wrr_1994/koren_genesis_text_source.manifest.json")

FIELDNAMES = [
    "config",
    "config_sha256",
    "corpus_name",
    "language",
    "source_count",
    "source_paths",
    "source_raw_bytes",
    "source_raw_sha256",
    "source_text_bytes",
    "source_text_sha256",
    "normalized_letters",
    "verse_count",
    "normalized_text_sha256",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    row = audit_text_source(args.config)
    write_rows(args.out, [row])
    write_markdown(args.markdown_out, row)
    if args.manifest_out:
        write_manifest(args, row, started)
    print(args.out)
    print(args.markdown_out)
    if args.manifest_out:
        print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=CONFIG)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def audit_text_source(config: Path) -> dict[str, object]:
    config = config.resolve()
    corpus = load_corpus(config)
    source_fingerprints = [fingerprint_source(path) for path in source_paths(config)]
    return {
        "config": str(config),
        "config_sha256": sha256_bytes(config.read_bytes()),
        "corpus_name": corpus.name,
        "language": corpus.language,
        "source_count": len(source_fingerprints),
        "source_paths": ";".join(str(item["path"]) for item in source_fingerprints),
        "source_raw_bytes": sum(int(item["raw_bytes"]) for item in source_fingerprints),
        "source_raw_sha256": ";".join(str(item["raw_sha256"]) for item in source_fingerprints),
        "source_text_bytes": sum(int(item["text_bytes"]) for item in source_fingerprints),
        "source_text_sha256": ";".join(str(item["text_sha256"]) for item in source_fingerprints),
        "normalized_letters": len(corpus.text),
        "verse_count": len(corpus.verses),
        "normalized_text_sha256": sha256_text(corpus.text),
    }


def source_paths(config: Path) -> tuple[Path, ...]:
    try:
        data = tomllib.loads(config.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"{config}: invalid TOML: {exc}") from exc
    sources = data.get("sources", [])
    if not isinstance(sources, list):
        raise ValueError(f"{config}: sources must be a list")
    base = config.parent
    paths = []
    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict):
            raise ValueError(f"{config}: source {index} must be a table")
        if not isinstance(source.get("path"), str) or not source["path"].strip():
            raise ValueError(f"{config}: source {index} missing path")
        raw_path = Path(source["path"]).expanduser()
        paths.append((raw_path if raw_path.is_absolute() else base / raw_path).resolve())
    return tuple(paths)


def fingerprint_source(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    text_bytes = decompressed_bytes(path, raw)
    return {
        "path": str(path),
        "raw_bytes": len(raw),
        "raw_sha256": sha256_bytes(raw),
        "text_bytes": len(text_bytes),
        "text_sha256": sha256_bytes(text_bytes),
    }


def decompressed_bytes(path: Path, raw: bytes) -> bytes:
    if path.suffix == ".gz":
        return gzip.decompress(raw)
    return raw


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, row: dict[str, object]) -> None:
    lines = [
        "# Koren Genesis Text Source Audit",
        "",
        "This fingerprints the exact Koren Genesis source stream used by the WRR",
        "audit smoke reports. It does not license or publish the source text.",
        "",
        "| Item | Value |",
        "| --- | --- |",
    ]
    for key in FIELDNAMES:
        lines.append(f"| `{key}` | `{row[key]}` |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(args: argparse.Namespace, row: dict[str, object], started: float) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "config": str(args.config),
        "summary": row,
        "outputs": {
            "csv": str(args.out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
