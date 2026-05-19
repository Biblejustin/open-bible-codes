#!/usr/bin/env python3
"""Diagnose WRR-style perturbation boundary and exact-match behavior."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.cli import accepted_term_languages
from els.corpus import Corpus, load_corpus
from els.search import iter_els_query_matches_by_lanes, normalize_for_corpus
from els.term_display import display_term
from els.wrr import (
    expected_els_count,
    is_perturbed_els_match,
    perturbed_offsets,
    perturbation_triples,
    relative_letter_frequencies,
    skip_cap_for_expected_count,
)


TERMS = Path("reports/wrr_1994/wrr2_terms.csv")
COUNTS = Path("reports/wrr_1994/wrr2_genesis_counts.csv")
CONFIG = Path("configs/example_koren_genesis.toml")
OUT = Path("reports/wrr_1994/wrr2_perturbation_diagnostics.csv")
SUMMARY_OUT = Path("reports/wrr_1994/wrr2_perturbation_diagnostics_summary.csv")
MD_OUT = Path("reports/wrr_1994/wrr2_perturbation_diagnostics.md")
MANIFEST_OUT = Path("reports/wrr_1994/wrr2_perturbation_diagnostics.manifest.json")

APP_CATEGORY = "wrr_appellation"
DATE_CATEGORY = "wrr_date"

FIELDNAMES = [
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "normalized_length",
    "observed_hits",
    "search_max_skip",
    "skip_cap",
    "expected_at_skip_cap",
    "target_reached",
    "sampled_hits",
    "min_in_bounds_perturbations",
    "median_in_bounds_perturbations",
    "max_in_bounds_perturbations",
    "min_exact_perturbation_matches",
    "median_exact_perturbation_matches",
    "max_exact_perturbation_matches",
    "ordinary_in_bounds_failures",
    "ordinary_exact_match_failures",
    "read",
]

SUMMARY_FIELDNAMES = [
    "rows",
    "unique_normalized_terms",
    "search_max_skip",
    "sample_hits_per_query",
    "perturbation_triples",
    "rows_with_hits",
    "rows_without_hits",
    "sampled_hits",
    "rows_with_sample_under_10_valid",
    "rows_with_sample_under_10_exact_matches",
    "min_in_bounds_perturbations",
    "median_in_bounds_perturbations",
    "max_in_bounds_perturbations",
    "min_exact_perturbation_matches",
    "median_exact_perturbation_matches",
    "max_exact_perturbation_matches",
    "ordinary_in_bounds_failures",
    "ordinary_exact_match_failures",
]


@dataclass(frozen=True)
class TermRow:
    term_id: str
    concept: str
    category: str
    term: str
    normalized: str

    @property
    def length(self) -> int:
        return len(self.normalized)


@dataclass(frozen=True)
class HitSample:
    query: str
    skip: int
    start: int
    end: int


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    corpus = load_corpus(args.config)
    count_rows = {row["term_id"]: row for row in read_rows(args.counts)}
    terms = collect_terms(
        read_rows(args.terms),
        corpus,
        min_term_length=args.min_term_length,
        max_term_length=args.max_term_length,
    )
    query_samples = collect_query_samples(
        corpus,
        sorted({term.normalized for term in terms}),
        min_skip=args.min_skip,
        max_skip=args.search_max_skip,
        direction=args.direction,
        sample_hits_per_query=sample_cap(args.sample_hits_per_query),
    )
    rows = diagnostic_rows(terms, count_rows, query_samples, corpus, args)
    summary = summarize(rows, args)
    write_rows(args.out, FIELDNAMES, rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, rows, summary)
    if args.manifest_out:
        write_manifest(args, corpus, rows, summary, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    if args.manifest_out:
        print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", type=Path, default=TERMS)
    parser.add_argument("--counts", type=Path, default=COUNTS)
    parser.add_argument("--config", type=Path, default=CONFIG)
    parser.add_argument("--min-term-length", type=int, default=5)
    parser.add_argument("--max-term-length", type=int, default=8)
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--search-max-skip", type=int, default=250)
    parser.add_argument("--direction", choices=["forward", "backward", "both"], default="both")
    parser.add_argument("--target-expected-hits", type=float, default=10.0)
    parser.add_argument(
        "--sample-hits-per-query",
        type=int,
        default=20,
        help="Maximum hits to check per normalized query; 0 or less checks all hits.",
    )
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def collect_terms(
    rows: list[dict[str, str]],
    corpus: Corpus,
    *,
    min_term_length: int,
    max_term_length: int,
) -> list[TermRow]:
    languages = accepted_term_languages(corpus.language)
    terms: list[TermRow] = []
    for row in rows:
        if row.get("category", "") not in {APP_CATEGORY, DATE_CATEGORY}:
            continue
        if row.get("language", "").strip() not in languages:
            continue
        normalized = normalize_for_corpus(corpus, row.get("term", ""))
        if len(normalized) < min_term_length or len(normalized) > max_term_length:
            continue
        terms.append(
            TermRow(
                term_id=row["term_id"],
                concept=row.get("concept", ""),
                category=row.get("category", ""),
                term=row.get("term", ""),
                normalized=normalized,
            )
        )
    return sorted(terms, key=lambda term: term.term_id)


def collect_query_samples(
    corpus: Corpus,
    queries: list[str],
    *,
    min_skip: int,
    max_skip: int,
    direction: str,
    sample_hits_per_query: int | None,
) -> dict[str, list[HitSample]]:
    samples = {query: [] for query in queries}
    for query, skip, start, end in iter_els_query_matches_by_lanes(
        corpus.text,
        queries,
        min_skip=min_skip,
        max_skip=max_skip,
        direction=direction,
        max_hits_per_query=sample_hits_per_query,
    ):
        samples[query].append(HitSample(query=query, skip=skip, start=start, end=end))
    return samples


def diagnostic_rows(
    terms: list[TermRow],
    count_rows: dict[str, dict[str, str]],
    query_samples: dict[str, list[HitSample]],
    corpus: Corpus,
    args: argparse.Namespace,
) -> list[dict[str, object]]:
    frequencies = relative_letter_frequencies(corpus.text)
    triples = perturbation_triples()
    rows = []
    for term in terms:
        cap = skip_cap_for_expected_count(
            corpus.text,
            term.normalized,
            target_expected=args.target_expected_hits,
        )
        expected_at_cap = expected_els_count(len(corpus.text), term.normalized, cap, frequencies)
        target_reached = expected_at_cap >= args.target_expected_hits
        samples = query_samples.get(term.normalized, [])
        valid_counts = [
            valid_perturbation_count(
                start=sample.start,
                skip=sample.skip,
                word_length=term.length,
                text_length=len(corpus.text),
                triples=triples,
            )
            for sample in samples
        ]
        exact_counts = [
            exact_perturbation_match_count(
                text=corpus.text,
                word=term.normalized,
                start=sample.start,
                skip=sample.skip,
                triples=triples,
            )
            for sample in samples
        ]
        ordinary_failures = sum(
            1
            for sample in samples
            if not offsets_in_bounds(
                perturbed_offsets(sample.start, sample.skip, term.length, (0, 0, 0)),
                len(corpus.text),
            )
        )
        ordinary_exact_failures = sum(
            1
            for sample in samples
            if not is_perturbed_els_match(
                corpus.text,
                term.normalized,
                sample.start,
                sample.skip,
                (0, 0, 0),
            )
        )
        rows.append(
            {
                "term_id": term.term_id,
                "concept": term.concept,
                "category": term.category,
                "term": term.term,
                "normalized_term": term.normalized,
                "normalized_length": term.length,
                "observed_hits": int_or_zero(count_rows.get(term.term_id, {}).get("hit_count")),
                "search_max_skip": args.search_max_skip,
                "skip_cap": cap,
                "expected_at_skip_cap": round(expected_at_cap, 6),
                "target_reached": target_reached,
                "sampled_hits": len(samples),
                "min_in_bounds_perturbations": min(valid_counts) if valid_counts else "",
                "median_in_bounds_perturbations": median_int(valid_counts) if valid_counts else "",
                "max_in_bounds_perturbations": max(valid_counts) if valid_counts else "",
                "min_exact_perturbation_matches": min(exact_counts) if exact_counts else "",
                "median_exact_perturbation_matches": median_int(exact_counts)
                if exact_counts
                else "",
                "max_exact_perturbation_matches": max(exact_counts) if exact_counts else "",
                "ordinary_in_bounds_failures": ordinary_failures,
                "ordinary_exact_match_failures": ordinary_exact_failures,
                "read": diagnostic_read(
                    valid_counts,
                    exact_counts,
                    ordinary_failures,
                    ordinary_exact_failures,
                ),
            }
        )
    return rows


def valid_perturbation_count(
    *,
    start: int,
    skip: int,
    word_length: int,
    text_length: int,
    triples: tuple[tuple[int, int, int], ...] | None = None,
) -> int:
    active_triples = triples if triples is not None else perturbation_triples()
    return sum(
        1
        for triple in active_triples
        if offsets_in_bounds(perturbed_offsets(start, skip, word_length, triple), text_length)
    )


def exact_perturbation_match_count(
    *,
    text: str,
    word: str,
    start: int,
    skip: int,
    triples: tuple[tuple[int, int, int], ...] | None = None,
) -> int:
    active_triples = triples if triples is not None else perturbation_triples()
    return sum(
        1
        for triple in active_triples
        if is_perturbed_els_match(text, word, start, skip, triple)
    )


def offsets_in_bounds(offsets: tuple[int, ...], text_length: int) -> bool:
    if text_length < 1:
        raise ValueError("text_length must be > 0")
    return all(0 <= offset < text_length for offset in offsets)


def median_int(values: list[int]) -> int:
    return int(statistics.median(values))


def diagnostic_read(
    valid_counts: list[int],
    exact_counts: list[int],
    ordinary_failures: int,
    ordinary_exact_failures: int,
) -> str:
    if ordinary_failures:
        return "ordinary hit boundary failure"
    if ordinary_exact_failures:
        return "ordinary hit exact-match failure"
    if not valid_counts:
        return "no checked hits"
    if min(valid_counts) < 10:
        return "checked hits include fewer than 10 in-bound perturbations"
    if min(exact_counts) < 10:
        return "checked hits include fewer than 10 exact perturbation matches"
    return "checked perturbation exact-match ok"


def summarize(rows: list[dict[str, object]], args: argparse.Namespace) -> dict[str, object]:
    sampled_rows = [row for row in rows if row.get("sampled_hits") not in ("", 0)]
    valid_counts = [
        int(row["min_in_bounds_perturbations"])
        for row in sampled_rows
        if row.get("min_in_bounds_perturbations") not in ("", None)
    ]
    exact_counts = [
        int(row["min_exact_perturbation_matches"])
        for row in sampled_rows
        if row.get("min_exact_perturbation_matches") not in ("", None)
    ]
    return {
        "rows": len(rows),
        "unique_normalized_terms": len({row["normalized_term"] for row in rows}),
        "search_max_skip": args.search_max_skip,
        "sample_hits_per_query": sample_label(args.sample_hits_per_query),
        "perturbation_triples": len(perturbation_triples()),
        "rows_with_hits": len(sampled_rows),
        "rows_without_hits": len(rows) - len(sampled_rows),
        "sampled_hits": sum(int_or_zero(row.get("sampled_hits")) for row in rows),
        "rows_with_sample_under_10_valid": sum(1 for count in valid_counts if count < 10),
        "rows_with_sample_under_10_exact_matches": sum(
            1 for count in exact_counts if count < 10
        ),
        "min_in_bounds_perturbations": min(valid_counts) if valid_counts else "",
        "median_in_bounds_perturbations": median_int(valid_counts) if valid_counts else "",
        "max_in_bounds_perturbations": max(valid_counts) if valid_counts else "",
        "min_exact_perturbation_matches": min(exact_counts) if exact_counts else "",
        "median_exact_perturbation_matches": median_int(exact_counts)
        if exact_counts
        else "",
        "max_exact_perturbation_matches": max(exact_counts) if exact_counts else "",
        "ordinary_in_bounds_failures": sum(
            int_or_zero(row.get("ordinary_in_bounds_failures")) for row in rows
        ),
        "ordinary_exact_match_failures": sum(
            int_or_zero(row.get("ordinary_exact_match_failures")) for row in rows
        ),
    }


def sample_cap(value: int) -> int | None:
    return None if value <= 0 else value


def sample_label(value: int) -> int | str:
    return "all" if value <= 0 else value


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary: dict[str, object],
) -> None:
    lines = [
        "# WRR2 Perturbation Diagnostics",
        "",
        "This report checks imported WRR2 length 5..8 ELS hits and counts how many",
        "of the 125 WRR-style last-three-gap perturbation triples remain inside",
        "the corpus boundaries and how many still spell the same term exactly. It",
        "does not compute proximity `Q(w,w')`, corrected distance `c(w,w')`, or",
        "the WRR permutation statistic.",
        "",
        "## Summary",
        "",
        "| Item | Count |",
        "| --- | ---: |",
    ]
    for key in SUMMARY_FIELDNAMES:
        lines.append(f"| `{key}` | {summary[key]} |")
    lines.extend(
        [
            "",
            "## Boundary/Exact-Limited Rows",
            "",
            "| Term | Hits checked | Min in-bound | Min exact | Read |",
            "| --- | ---: | ---: | ---: | --- |",
        ]
    )
    boundary_rows = sorted(
        rows,
        key=lambda row: (
            int_or_large(row.get("min_exact_perturbation_matches")),
            int_or_large(row.get("min_in_bounds_perturbations")),
            str(row["term_id"]),
        ),
    )[:20]
    for row in boundary_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    display_boundary_term(row),
                    str(row["sampled_hits"]),
                    str(row["min_in_bounds_perturbations"]),
                    str(row["min_exact_perturbation_matches"]),
                    str(row["read"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Caution",
            "",
            "This is only a term-hit diagnostic for future corrected-distance work.",
            "A row with enough exact perturbed matches is not evidence for WRR; it only",
            "means that the checked ordinary ELS rows are not blocked by this one",
            "source-described validity condition.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def display_boundary_term(row: dict[str, object]) -> str:
    term_id = str(row["term_id"])
    term = display_term(str(row["normalized_term"]), english=str(row.get("concept", "")) or None)
    return f"`{term_id}` {term}"


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    args: argparse.Namespace,
    corpus: Corpus,
    rows: list[dict[str, object]],
    summary: dict[str, object],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "terms": str(args.terms),
        "counts": str(args.counts),
        "config": str(args.config),
        "corpus": corpus.summary(),
        "summary": summary,
        "rows": len(rows),
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def int_or_zero(value: object) -> int:
    if value in ("", None):
        return 0
    return int(float(str(value)))


def int_or_large(value: object) -> int:
    if value in ("", None):
        return 10**12
    return int_or_zero(value)


if __name__ == "__main__":
    raise SystemExit(main())
