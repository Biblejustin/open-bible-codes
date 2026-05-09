#!/usr/bin/env python3
"""Run the compiled pair-index counter for full-distance ELS counts."""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.corpus import load_corpus
from els.search import normalize_for_corpus
from els.skip_plan import expected_hits_through_skip, query_probability
from els.statistics import estimated_search_space, hits_per_million, round_float


ROOT = Path(__file__).resolve().parents[1]
CPP_SOURCE = ROOT / "scripts/cpp/dynamic_span_counter.cpp"
DEFAULT_BINARY = ROOT / "data/cache/bin/dynamic_span_counter"
DEFAULT_OUT = ROOT / "reports/dynamic_skip_focus/dynamic_span_counts.csv"
DEFAULT_MANIFEST = ROOT / "reports/dynamic_skip_focus/dynamic_span_counts.manifest.json"

FIELDNAMES = [
    "corpus",
    "corpus_language",
    "corpus_letters",
    "term_id",
    "concept",
    "category",
    "term_language",
    "term",
    "normalized_term",
    "normalized_length",
    "mode",
    "min_skip",
    "effective_max_skip",
    "search_space_positions",
    "expected_hits",
    "expected_hits_per_million_positions",
    "direction",
    "forward_count",
    "backward_count",
    "hit_count",
    "hits_per_million_positions",
    "counter_elapsed_seconds",
    "status",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    binary = build_binary(args.binary)
    term_rows = read_rows(args.terms)
    output_rows: list[dict[str, str]] = []
    for corpus_label, config in parse_corpus_args(args.corpus).items():
        corpus = load_corpus(config)
        active_terms = normalized_terms_for_corpus(term_rows, corpus, args.term_id)
        if not active_terms:
            continue
        counter_rows = run_counter(
            binary,
            corpus.text,
            active_terms,
            min_skip=args.min_skip,
            mode=args.mode,
            direction=args.direction,
        )
        by_id = {row["term_id"]: row for row in counter_rows}
        for term in active_terms:
            counted = by_id.get(term["term_id"], {})
            effective_max_skip = int(
                counted.get("effective_max_skip") or dynamic_max_skip(
                    len(corpus.text),
                    len(term["normalized_term"]),
                    args.mode,
                )
            )
            search_space = estimated_search_space(
                len(corpus.text),
                len(term["normalized_term"]),
                args.min_skip,
                effective_max_skip,
                args.direction,
            )
            expected = expected_hits_through_skip(
                len(corpus.text),
                len(term["normalized_term"]),
                query_probability(corpus.text, term["normalized_term"]),
                min_skip=args.min_skip,
                max_skip=effective_max_skip,
                direction=args.direction,
            )
            hit_count = int(counted.get("hit_count") or 0)
            output_rows.append(
                {
                    "corpus": corpus_label,
                    "corpus_language": corpus.language,
                    "corpus_letters": str(len(corpus.text)),
                    "term_id": term["term_id"],
                    "concept": term.get("concept", ""),
                    "category": term.get("category", ""),
                    "term_language": term.get("language", ""),
                    "term": term.get("term", ""),
                    "normalized_term": term["normalized_term"],
                    "normalized_length": counted.get("normalized_length", str(len(term["normalized_term"]))),
                    "mode": counted.get("mode", args.mode),
                    "min_skip": counted.get("min_skip", str(args.min_skip)),
                    "effective_max_skip": str(effective_max_skip),
                    "search_space_positions": str(search_space),
                    "expected_hits": str(round_float(expected)),
                    "expected_hits_per_million_positions": (
                        "" if search_space == 0 else str(round_float(1_000_000 * expected / search_space))
                    ),
                    "direction": counted.get("direction", args.direction),
                    "forward_count": counted.get("forward_count", ""),
                    "backward_count": counted.get("backward_count", ""),
                    "hit_count": str(hit_count),
                    "hits_per_million_positions": str(hits_per_million(hit_count, search_space)),
                    "counter_elapsed_seconds": counted.get("elapsed_seconds", ""),
                    "status": "counted" if counted else "missing_counter_row",
                }
            )
    write_rows(args.out, output_rows)
    write_manifest(args.manifest_out, args, output_rows, started)
    print(args.out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", type=Path, required=True)
    parser.add_argument("--corpus", action="append", required=True)
    parser.add_argument("--term-id", action="append", default=[])
    parser.add_argument("--mode", choices=["letters-per-term", "full-span"], default="letters-per-term")
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--direction", choices=["forward", "backward", "both"], default="both")
    parser.add_argument("--binary", type=Path, default=DEFAULT_BINARY)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def dynamic_max_skip(text_length: int, normalized_length: int, mode: str) -> int:
    if mode == "letters-per-term":
        return text_length // normalized_length if normalized_length else 0
    if normalized_length <= 1:
        return max(1, text_length - 1)
    return max(1, (text_length - 1) // (normalized_length - 1))


def parse_corpus_args(values: list[str]) -> dict[str, Path]:
    parsed: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"expected LABEL=CONFIG for --corpus, got {value!r}")
        label, config = value.split("=", 1)
        parsed[label] = Path(config)
    return parsed


def build_binary(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    compiler = os.environ.get("CXX", "clang++")
    command = [
        compiler,
        "-O3",
        "-std=c++17",
        str(CPP_SOURCE),
        "-o",
        str(path),
    ]
    source_mtime = CPP_SOURCE.stat().st_mtime_ns
    binary_mtime = path.stat().st_mtime_ns if path.exists() else -1
    if binary_mtime < source_mtime:
        subprocess.run(command, check=True)
    return path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def normalized_terms_for_corpus(
    rows: list[dict[str, str]],
    corpus: Any,
    term_ids: list[str],
) -> list[dict[str, str]]:
    wanted = set(term_ids)
    output: list[dict[str, str]] = []
    for row in rows:
        if wanted and row.get("term_id") not in wanted:
            continue
        if row.get("language") != corpus.language:
            continue
        normalized = normalize_for_corpus(corpus, row.get("term", ""))
        if not normalized:
            continue
        item = dict(row)
        item["normalized_term"] = normalized
        output.append(item)
    return output


def run_counter(
    binary: Path,
    text: str,
    terms: list[dict[str, str]],
    *,
    min_skip: int,
    mode: str,
    direction: str,
) -> list[dict[str, str]]:
    with tempfile.TemporaryDirectory(prefix="edls_dynamic_span_") as tmp:
        tmp_path = Path(tmp)
        text_path = tmp_path / "text.txt"
        terms_path = tmp_path / "terms.tsv"
        out_path = tmp_path / "counts.csv"
        text_path.write_text(text, encoding="utf-8")
        with terms_path.open("w", encoding="utf-8", newline="") as handle:
            for term in terms:
                handle.write(f"{term['term_id']}\t{term['normalized_term']}\n")
        subprocess.run(
            [
                str(binary),
                str(text_path),
                str(terms_path),
                str(min_skip),
                mode,
                direction,
                str(out_path),
            ],
            check=True,
        )
        return read_rows(out_path)


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {
        "script": "scripts/run_dynamic_span_counter.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "terms": str(args.terms),
        "corpora": args.corpus,
        "term_ids": args.term_id,
        "mode": args.mode,
        "direction": args.direction,
        "rows": len(rows),
        "git_commit": git_commit(),
    }
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
