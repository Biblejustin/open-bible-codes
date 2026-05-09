#!/usr/bin/env python3
"""Convert exact-center rows into hits-compatible input for extension scans."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.cli import FIELDNAMES


DEFAULT_IN = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_rows.csv")
DEFAULT_OUT = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_extension_hits.csv")
DEFAULT_MANIFEST = Path("reports/dynamic_skip_focus/strong_full_span_exact_center_extension_hits.manifest.json")

OUT_FIELDNAMES = ["corpus", *FIELDNAMES]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    result = convert(args.input, args.out, corpus_filter=set(args.corpus))
    write_manifest(args.manifest_out, args, result, started)
    print(args.out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_IN)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--corpus", action="append", default=[])
    return parser


def convert(input_path: Path, out: Path, *, corpus_filter: set[str]) -> dict[str, Any]:
    read_rows = 0
    written_rows = 0
    written_by_corpus: Counter[str] = Counter()
    out.parent.mkdir(parents=True, exist_ok=True)
    with input_path.open("r", encoding="utf-8", newline="") as input_handle:
        reader = csv.DictReader(input_handle)
        with out.open("w", encoding="utf-8", newline="") as output_handle:
            writer = csv.DictWriter(output_handle, fieldnames=OUT_FIELDNAMES)
            writer.writeheader()
            for row in reader:
                read_rows += 1
                corpus = row.get("corpus", "")
                if corpus_filter and corpus not in corpus_filter:
                    continue
                writer.writerow(hit_row(row))
                written_rows += 1
                written_by_corpus[corpus] += 1
    return {
        "input_rows": read_rows,
        "written_rows": written_rows,
        "written_by_corpus": dict(sorted(written_by_corpus.items())),
    }


def hit_row(row: dict[str, str]) -> dict[str, str]:
    source = row.get("center_source", "")
    return {
        "corpus": row.get("corpus", ""),
        "term": row.get("term", ""),
        "normalized_term": row.get("normalized_term", ""),
        "skip": row.get("skip", ""),
        "direction": row.get("direction", ""),
        "start_offset": row.get("start_offset", ""),
        "end_offset": row.get("end_offset", ""),
        "span_letters": row.get("span_letters", ""),
        "sequence": row.get("normalized_term", ""),
        "start_ref": row.get("start_ref", ""),
        "end_ref": row.get("end_ref", ""),
        "start_source": source,
        "end_source": source,
        "center_offset": row.get("center_offset", ""),
        "center_ref": row.get("center_ref", ""),
        "center_source": source,
        "center_word_index": row.get("center_word_index", ""),
        "center_word": row.get("center_word", ""),
        "center_normalized_word": row.get("center_normalized_word", ""),
    }


def write_manifest(path: Path, args: argparse.Namespace, result: dict[str, Any], started: float) -> None:
    payload = {
        "script": "scripts/build_dynamic_span_exact_center_extension_hits.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "input": str(args.input),
        "out": str(args.out),
        "corpus_filter": args.corpus,
        "result": result,
        "git_commit": git_commit(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
