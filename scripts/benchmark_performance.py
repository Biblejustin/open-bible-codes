#!/usr/bin/env python3
"""Benchmark core EDLS performance paths."""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, TypeVar

from els.cli import accepted_term_languages, build_surface_terms
from els.corpus import Corpus, VerseSpan, load_corpus
from els.search import count_els_terms_by_lanes, find_els, normalize_for_corpus
from els.surface import build_surface_context_index, normalize_verses


GREEK_ALPHABET = "αβγδεζηθικλμνξοπρστυφχψω"
T = TypeVar("T")


@dataclass(frozen=True)
class BenchmarkResult:
    name: str
    status: str
    seconds: float
    details: dict[str, object]


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    results: list[BenchmarkResult] = []

    results.append(benchmark_synthetic_find(args))
    results.append(benchmark_synthetic_aho(args))
    if not args.skip_real:
        results.extend(benchmark_corpus_cache(args.oshb_config))
        results.append(benchmark_real_find(args))
        results.append(benchmark_real_batch_count(args))
        results.append(benchmark_real_surface_index(args))

    print_results(results)
    if args.json_out:
        write_json(results, Path(args.json_out).expanduser())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Benchmark source loading, ELS finding, batch counts, and surface indexes."
    )
    parser.add_argument("--tr-config", default="configs/example_ebible_grctr.toml")
    parser.add_argument("--oshb-config", default="configs/example_oshb_wlc.toml")
    parser.add_argument("--terms", default="terms/theological_terms.csv")
    parser.add_argument("--term", default="θεος")
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=50)
    parser.add_argument(
        "--direction",
        choices=["forward", "backward", "both"],
        default="both",
    )
    parser.add_argument("--min-term-length", type=int, default=3)
    parser.add_argument("--synthetic-letters", type=int, default=300_000)
    parser.add_argument("--synthetic-terms", type=int, default=100)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--skip-real", action="store_true")
    parser.add_argument("--json-out")
    return parser


def benchmark_synthetic_aho(args: argparse.Namespace) -> BenchmarkResult:
    rng = random.Random(args.seed)
    text = random_text(rng, GREEK_ALPHABET, args.synthetic_letters)
    queries = random_queries(
        rng,
        GREEK_ALPHABET,
        args.synthetic_terms,
        length=args.min_term_length + 1,
    )

    seconds, counts = timed(
        lambda: count_els_terms_by_lanes(
            text,
            queries,
            min_skip=args.min_skip,
            max_skip=args.max_skip,
            direction=args.direction,
            jobs=args.jobs,
        )
    )
    return BenchmarkResult(
        name="synthetic_aho_count",
        status="ok",
        seconds=seconds,
        details={
            "letters": len(text),
            "terms": len(queries),
            "hits": sum(counts.values()),
            "min_skip": args.min_skip,
            "max_skip": args.max_skip,
            "direction": args.direction,
            "jobs": args.jobs,
        },
    )


def benchmark_synthetic_find(args: argparse.Namespace) -> BenchmarkResult:
    rng = random.Random(args.seed)
    text = random_text(rng, GREEK_ALPHABET, args.synthetic_letters)
    term_length = args.min_term_length + 1
    if len(text) < term_length:
        return BenchmarkResult(
            name="synthetic_find_els",
            status="skipped",
            seconds=0.0,
            details={"reason": "synthetic_text_short", "letters": len(text)},
        )
    term_start = min(1000, len(text) - term_length)
    term = text[term_start : term_start + term_length]
    corpus = synthetic_corpus(text)
    seconds, hit_count = timed(
        lambda: sum(
            1
            for _hit in find_els(
                corpus,
                term,
                min_skip=args.min_skip,
                max_skip=args.max_skip,
                direction=args.direction,
            )
        )
    )
    return BenchmarkResult(
        name="synthetic_find_els",
        status="ok",
        seconds=seconds,
        details={
            "letters": len(text),
            "term": term,
            "hits": hit_count,
            "min_skip": args.min_skip,
            "max_skip": args.max_skip,
            "direction": args.direction,
        },
    )


def benchmark_corpus_cache(config_path: str) -> list[BenchmarkResult]:
    config = Path(config_path).expanduser()
    if not config.exists():
        return [
            BenchmarkResult(
                name="corpus_load_cold",
                status="skipped",
                seconds=0.0,
                details={"reason": "config_missing", "config": str(config)},
            ),
            BenchmarkResult(
                name="corpus_load_warm",
                status="skipped",
                seconds=0.0,
                details={"reason": "config_missing", "config": str(config)},
            ),
        ]

    old_cache_dir = os.environ.get("EDLS_CORPUS_CACHE_DIR")
    old_no_cache = os.environ.get("EDLS_NO_CORPUS_CACHE")
    try:
        with tempfile.TemporaryDirectory(prefix="edls-corpus-cache-") as cache_dir:
            os.environ["EDLS_CORPUS_CACHE_DIR"] = cache_dir
            os.environ.pop("EDLS_NO_CORPUS_CACHE", None)
            cold_seconds, cold = timed(lambda: load_corpus(config))
            warm_seconds, warm = timed(lambda: load_corpus(config))
    except FileNotFoundError as error:
        return [
            BenchmarkResult(
                name="corpus_load_cold",
                status="skipped",
                seconds=0.0,
                details={
                    "reason": "source_missing",
                    "config": str(config),
                    "error": str(error),
                },
            ),
            BenchmarkResult(
                name="corpus_load_warm",
                status="skipped",
                seconds=0.0,
                details={
                    "reason": "source_missing",
                    "config": str(config),
                    "error": str(error),
                },
            ),
        ]
    finally:
        restore_env("EDLS_CORPUS_CACHE_DIR", old_cache_dir)
        restore_env("EDLS_NO_CORPUS_CACHE", old_no_cache)

    common = {
        "config": str(config),
        "letters": len(cold.text),
        "verses": len(cold.verses),
        "language": cold.language,
    }
    return [
        BenchmarkResult(
            name="corpus_load_cold",
            status="ok",
            seconds=cold_seconds,
            details={**common, "cache": "empty_before_run"},
        ),
        BenchmarkResult(
            name="corpus_load_warm",
            status="ok",
            seconds=warm_seconds,
            details={
                **common,
                "cache": "pickle_hit",
                "same_letters": len(warm.text) == len(cold.text),
            },
        ),
    ]


def benchmark_real_find(args: argparse.Namespace) -> BenchmarkResult:
    return real_benchmark(
        "real_find_els",
        args.tr_config,
        lambda corpus: _benchmark_find(corpus, args),
    )


def _benchmark_find(
    corpus: Corpus,
    args: argparse.Namespace,
) -> tuple[float, dict[str, object]]:
    normalized = normalize_for_corpus(corpus, args.term)
    seconds, hit_count = timed(
        lambda: sum(
            1
            for _hit in find_els(
                corpus,
                args.term,
                min_skip=args.min_skip,
                max_skip=args.max_skip,
                direction=args.direction,
            )
        )
    )
    return seconds, {
        "config": args.tr_config,
        "term": args.term,
        "normalized_term": normalized,
        "hits": hit_count,
        "letters": len(corpus.text),
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "direction": args.direction,
    }


def benchmark_real_batch_count(args: argparse.Namespace) -> BenchmarkResult:
    return real_benchmark(
        "real_batch_count",
        args.tr_config,
        lambda corpus: _benchmark_batch_count(corpus, args),
    )


def _benchmark_batch_count(
    corpus: Corpus,
    args: argparse.Namespace,
) -> tuple[float, dict[str, object]]:
    term_rows = read_term_rows(args.terms)
    terms = normalized_terms_for_corpus(corpus, term_rows, args.min_term_length)
    seconds, counts = timed(
        lambda: count_els_terms_by_lanes(
            corpus.text,
            terms,
            min_skip=args.min_skip,
            max_skip=args.max_skip,
            direction=args.direction,
            jobs=args.jobs,
        )
    )
    return seconds, {
        "config": args.tr_config,
        "terms_file": args.terms,
        "terms": len(terms),
        "unique_terms": len(counts),
        "hits": sum(counts.values()),
        "letters": len(corpus.text),
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "direction": args.direction,
        "jobs": args.jobs,
    }


def benchmark_real_surface_index(args: argparse.Namespace) -> BenchmarkResult:
    return real_benchmark(
        "real_surface_index",
        args.tr_config,
        lambda corpus: _benchmark_surface_index(corpus, args),
    )


def _benchmark_surface_index(
    corpus: Corpus,
    args: argparse.Namespace,
) -> tuple[float, dict[str, object]]:
    term_rows = [
        row
        for row in read_term_rows(args.terms)
        if row.get("language", "").strip() in accepted_term_languages(corpus.language)
    ]
    corpus_terms = build_surface_terms(corpus, term_rows)
    corpus_terms = [
        term for term in corpus_terms if len(term.normalized_term) >= args.min_term_length
    ]
    seconds, context_index = timed(
        lambda: build_surface_context_index(corpus, corpus_terms, normalize_verses(corpus))
    )
    indexed_terms = sum(
        1 for indexes in context_index.verse_indexes_by_term.values() if indexes
    )
    return seconds, {
        "config": args.tr_config,
        "terms_file": args.terms,
        "terms": len(corpus_terms),
        "indexed_terms": indexed_terms,
        "verses": len(corpus.verses),
        "includes_verse_normalization": True,
    }


def real_benchmark(
    name: str,
    config_path: str,
    benchmark: Callable[[Corpus], tuple[float, dict[str, object]]],
) -> BenchmarkResult:
    config = Path(config_path).expanduser()
    if not config.exists():
        return BenchmarkResult(
            name=name,
            status="skipped",
            seconds=0.0,
            details={"reason": "config_missing", "config": str(config)},
        )
    try:
        corpus = load_corpus(config)
        seconds, details = benchmark(corpus)
    except FileNotFoundError as error:
        return BenchmarkResult(
            name=name,
            status="skipped",
            seconds=0.0,
            details={
                "reason": "source_missing",
                "config": str(config),
                "error": str(error),
            },
        )
    return BenchmarkResult(name=name, status="ok", seconds=seconds, details=details)


def read_term_rows(path: str) -> list[dict[str, str]]:
    with Path(path).expanduser().open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def normalized_terms_for_corpus(
    corpus: Corpus,
    term_rows: list[dict[str, str]],
    min_term_length: int,
) -> list[str]:
    languages = accepted_term_languages(corpus.language)
    terms: list[str] = []
    for row in term_rows:
        if row.get("language", "").strip() not in languages:
            continue
        term = normalize_for_corpus(corpus, row.get("term", ""))
        if len(term) >= min_term_length:
            terms.append(term)
    return terms


def random_text(rng: random.Random, alphabet: str, length: int) -> str:
    return "".join(rng.choice(alphabet) for _index in range(length))


def random_queries(
    rng: random.Random,
    alphabet: str,
    count: int,
    *,
    length: int,
) -> list[str]:
    queries: set[str] = set()
    while len(queries) < count:
        queries.add(random_text(rng, alphabet, length))
    return sorted(queries)


def timed(call: Callable[[], T]) -> tuple[float, T]:
    start = time.perf_counter()
    result = call()
    return time.perf_counter() - start, result


def restore_env(name: str, value: str | None) -> None:
    if value is None:
        os.environ.pop(name, None)
    else:
        os.environ[name] = value


def print_results(results: list[BenchmarkResult]) -> None:
    print(f"{'benchmark':<22} {'status':<8} {'seconds':>9} details")
    for result in results:
        details = json.dumps(result.details, ensure_ascii=False, sort_keys=True)
        print(f"{result.name:<22} {result.status:<8} {result.seconds:9.4f} {details}")


def write_json(results: list[BenchmarkResult], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(result) for result in results]
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def synthetic_corpus(text: str) -> Corpus:
    return Corpus(
        name="synthetic_greek",
        language="greek",
        keep_hebrew_final_forms=False,
        text=text,
        verses=(
            VerseSpan(
                source="synthetic",
                ref="Synthetic 1:1",
                book="Synthetic",
                chapter="1",
                verse="1",
                raw_text=text,
                norm_start=0,
                norm_end=len(text) - 1,
                norm_length=len(text),
            ),
        ),
        position_to_verse=[0] * len(text),
    )


if __name__ == "__main__":
    raise SystemExit(main())
