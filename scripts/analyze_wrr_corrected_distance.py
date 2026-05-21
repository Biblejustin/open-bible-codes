#!/usr/bin/env python3
"""Compute WRR corrected-distance smoke rows from generated perturbations."""

from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import load_corpus
from els.search import iter_els_query_matches_by_lanes
from els.wrr import (
    WrrElsOccurrence,
    is_perturbed_els_match,
    ordinary_els_offsets,
    perturbation_triples,
    skip_cap_for_expected_count,
    wrr_corrected_distance_from_perturbation_sets,
    wrr_label_minimality_domains,
    wrr_word_pair_proximity,
)


PAIR_TABLE = Path("reports/wrr_1994/wrr2_pair_eligibility_table.csv")
CONFIG = Path("configs/example_koren_genesis.toml")
OUT = Path("reports/wrr_1994/wrr2_corrected_distance_smoke.csv")
SUMMARY_OUT = Path("reports/wrr_1994/wrr2_corrected_distance_smoke_summary.csv")
MD_OUT = Path("reports/wrr_1994/wrr2_corrected_distance_smoke.md")
MANIFEST_OUT = Path("reports/wrr_1994/wrr2_corrected_distance_smoke.manifest.json")

ORDINARY_PERTURBATION = (0, 0, 0)

FIELDNAMES = [
    "pair_id",
    "concept",
    "candidate_lane",
    "pair_review_status",
    "appellation_term_id",
    "appellation_starts_with_rabbi_title",
    "date_term_id",
    "appellation_ordinary_hits",
    "date_ordinary_hits",
    "appellation_exact_perturbed_rows",
    "date_exact_perturbed_rows",
    "appellation_defined_perturbed_rows",
    "date_defined_perturbed_rows",
    "appellation_triples_with_defined_rows",
    "date_triples_with_defined_rows",
    "pair_valid_perturbations",
    "ordinary_q",
    "corrected_distance",
    "corrected_distance_status",
    "read",
]

SUMMARY_FIELDNAMES = [
    "selected_pairs",
    "shard_index",
    "shard_count",
    "pairs",
    "candidate_lane",
    "search_max_skip",
    "skip_cap_mode",
    "skip_cap_formula",
    "minimum_valid",
    "defined_corrected_distances",
    "ordinary_not_valid_pairs",
    "under_minimum_valid_pairs",
    "min_corrected_distance",
    "min_corrected_pair_id",
    "max_pair_valid_perturbations",
    "status",
]


@dataclass(frozen=True)
class PairTerm:
    term_id: str
    normalized: str


@dataclass(frozen=True)
class PerturbedTermStats:
    term_id: str
    normalized: str
    search_max_skip: int
    ordinary_hits: int
    exact_perturbed_rows: int
    defined_perturbed_rows: int
    triples_with_exact_rows: int
    triples_with_defined_rows: int


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    validate_shard_args(args.shard_index, args.shard_count)
    corpus = load_corpus(args.config)
    selected_pair_rows = select_pair_rows(read_rows(args.pair_table), args.candidate_lane)
    pair_rows = shard_pair_rows(
        selected_pair_rows,
        shard_index=args.shard_index,
        shard_count=args.shard_count,
    )
    terms = collect_pair_terms(pair_rows)
    max_skip_by_query = build_max_skip_by_query(corpus.text, terms, args)
    occurrences, stats = collect_perturbed_occurrences_by_term(
        corpus.text,
        terms,
        min_skip=args.min_skip,
        max_skip=args.search_max_skip,
        direction=args.direction,
        jobs=args.jobs,
        triples=perturbation_triples(),
        max_skip_by_query=max_skip_by_query,
    )
    rows = build_corrected_distance_rows(
        pair_rows,
        occurrences,
        stats,
        text_length=len(corpus.text),
        row_width_count=args.row_width_count,
        minimum_valid=args.minimum_valid,
    )
    summary = summarize(rows, args, selected_pair_count=len(selected_pair_rows))
    write_rows(args.out, FIELDNAMES, rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, rows, summary, args)
    if args.manifest_out:
        write_manifest(args, corpus.summary(), rows, summary, stats, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    if args.manifest_out:
        print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair-table", type=Path, default=PAIR_TABLE)
    parser.add_argument("--config", type=Path, default=CONFIG)
    parser.add_argument("--candidate-lane", default="length_5_8_smoke_candidate")
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--search-max-skip", type=int, default=250)
    parser.add_argument("--direction", choices=["forward", "backward", "both"], default="both")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--row-width-count", type=int, default=10)
    parser.add_argument("--minimum-valid", type=int, default=10)
    parser.add_argument("--skip-cap-mode", choices=["term", "fixed"], default="term")
    parser.add_argument("--target-expected-hits", type=float, default=10.0)
    parser.add_argument("--skip-cap-formula", choices=["printed", "program"], default="printed")
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def validate_shard_args(shard_index: int, shard_count: int) -> None:
    if shard_count < 1:
        raise ValueError("--shard-count must be >= 1")
    if shard_index < 0 or shard_index >= shard_count:
        raise ValueError("--shard-index must be >= 0 and < --shard-count")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def select_pair_rows(
    rows: list[dict[str, str]],
    candidate_lane: str,
) -> list[dict[str, str]]:
    if candidate_lane in ("", "all"):
        return rows
    return [row for row in rows if row.get("candidate_lane", "") == candidate_lane]


def shard_pair_rows(
    rows: list[dict[str, str]],
    *,
    shard_index: int,
    shard_count: int,
) -> list[dict[str, str]]:
    validate_shard_args(shard_index, shard_count)
    if shard_count == 1:
        return rows
    return [
        row
        for index, row in enumerate(rows)
        if index % shard_count == shard_index
    ]


def collect_pair_terms(rows: list[dict[str, str]]) -> dict[str, PairTerm]:
    terms: dict[str, PairTerm] = {}
    for row in rows:
        add_pair_term(terms, row["appellation_term_id"], row["appellation_normalized"])
        add_pair_term(terms, row["date_term_id"], row["date_normalized"])
    return terms


def add_pair_term(terms: dict[str, PairTerm], term_id: str, normalized: str) -> None:
    existing = terms.get(term_id)
    if existing is not None and existing.normalized != normalized:
        raise ValueError(f"conflicting normalized term for {term_id}")
    terms[term_id] = PairTerm(term_id=term_id, normalized=normalized)


def build_max_skip_by_query(
    text: str,
    terms: dict[str, PairTerm],
    args: argparse.Namespace,
) -> dict[str, int] | None:
    if args.skip_cap_mode == "fixed":
        return None
    caps: dict[str, int] = {}
    for term in terms.values():
        caps[term.normalized] = skip_cap_for_expected_count(
            text,
            term.normalized,
            target_expected=args.target_expected_hits,
            max_skip_limit=args.search_max_skip,
            formula=args.skip_cap_formula,
        )
    return caps


def collect_perturbed_occurrences_by_term(
    text: str,
    terms: dict[str, PairTerm],
    *,
    min_skip: int,
    max_skip: int,
    direction: str,
    jobs: int = 1,
    triples: tuple[tuple[int, int, int], ...] | None = None,
    max_skip_by_query: dict[str, int] | None = None,
) -> tuple[
    dict[str, dict[tuple[int, int, int], tuple[WrrElsOccurrence, ...]]],
    dict[str, PerturbedTermStats],
]:
    active_triples = triples if triples is not None else perturbation_triples()
    queries = sorted(
        {
            term.normalized
            for term in terms.values()
            if len(term.normalized) >= 4
        }
    )
    raw_by_query: dict[str, dict[tuple[int, int, int], set[tuple[tuple[int, ...], int]]]] = {
        query: {} for query in queries
    }
    ordinary_hits_by_query = {query: 0 for query in queries}
    for query, skip, start, _end in iter_els_query_matches_by_lanes(
        text,
        queries,
        min_skip=min_skip,
        max_skip=max_skip,
        direction=direction,
        jobs=jobs,
        max_skip_by_query=max_skip_by_query,
    ):
        ordinary_hits_by_query[query] += 1
        for triple in active_triples:
            if not is_perturbed_els_match(text, query, start, skip, triple):
                continue
            # Sources require exact perturbed letters, but use the unperturbed
            # (n,d,k) positions for distance/domain measurements.
            offsets = ordinary_els_offsets(start, skip, len(query))
            raw_by_query[query].setdefault(triple, set()).add((offsets, skip))

    occurrences_by_query: dict[
        str,
        dict[tuple[int, int, int], tuple[WrrElsOccurrence, ...]],
    ] = {}
    stats_by_query: dict[str, PerturbedTermStats] = {}
    for query in queries:
        defined_by_triple: dict[tuple[int, int, int], tuple[WrrElsOccurrence, ...]] = {}
        exact_rows = 0
        defined_rows = 0
        for triple, raw_rows in sorted(raw_by_query[query].items()):
            rows = sorted(raw_rows, key=perturbed_row_sort_key)
            exact_rows += len(rows)
            assignments = wrr_label_minimality_domains(rows, text_length=len(text))
            defined = tuple(
                assignment.to_occurrence()
                for assignment in assignments
                if assignment.status == "defined"
            )
            if defined:
                defined_by_triple[triple] = defined
                defined_rows += len(defined)
        occurrences_by_query[query] = defined_by_triple
        stats_by_query[query] = PerturbedTermStats(
            term_id="",
            normalized=query,
            search_max_skip=(max_skip_by_query or {}).get(query, max_skip),
            ordinary_hits=ordinary_hits_by_query[query],
            exact_perturbed_rows=exact_rows,
            defined_perturbed_rows=defined_rows,
            triples_with_exact_rows=len(raw_by_query[query]),
            triples_with_defined_rows=len(defined_by_triple),
        )

    occurrences_by_term: dict[
        str,
        dict[tuple[int, int, int], tuple[WrrElsOccurrence, ...]],
    ] = {}
    stats_by_term: dict[str, PerturbedTermStats] = {}
    for term in terms.values():
        occurrences_by_term[term.term_id] = occurrences_by_query.get(term.normalized, {})
        query_stats = stats_by_query.get(
            term.normalized,
            PerturbedTermStats(term.term_id, term.normalized, max_skip, 0, 0, 0, 0, 0),
        )
        stats_by_term[term.term_id] = PerturbedTermStats(
            term_id=term.term_id,
            normalized=term.normalized,
            search_max_skip=query_stats.search_max_skip,
            ordinary_hits=query_stats.ordinary_hits,
            exact_perturbed_rows=query_stats.exact_perturbed_rows,
            defined_perturbed_rows=query_stats.defined_perturbed_rows,
            triples_with_exact_rows=query_stats.triples_with_exact_rows,
            triples_with_defined_rows=query_stats.triples_with_defined_rows,
        )
    return occurrences_by_term, stats_by_term


def perturbed_row_sort_key(row: tuple[tuple[int, ...], int]) -> tuple[int, int, tuple[int, ...]]:
    offsets, skip = row
    return abs(skip), skip, offsets


def build_corrected_distance_rows(
    pair_rows: list[dict[str, str]],
    occurrences: dict[str, dict[tuple[int, int, int], tuple[WrrElsOccurrence, ...]]],
    stats: dict[str, PerturbedTermStats],
    *,
    text_length: int,
    row_width_count: int,
    minimum_valid: int,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for pair in pair_rows:
        app_id = pair["appellation_term_id"]
        date_id = pair["date_term_id"]
        app_occurrences = occurrences.get(app_id, {})
        date_occurrences = occurrences.get(date_id, {})
        app_stats = stats.get(app_id, empty_stats(app_id))
        date_stats = stats.get(date_id, empty_stats(date_id))
        valid_triples = valid_pair_triples(app_occurrences, date_occurrences)
        ordinary_q = ordinary_q_cell(
            app_occurrences,
            date_occurrences,
            text_length,
            row_width_count,
        )
        corrected_distance = ""
        if ORDINARY_PERTURBATION not in valid_triples:
            status = "ordinary_not_valid"
        elif len(valid_triples) < minimum_valid:
            status = "under_minimum_valid_perturbations"
        else:
            result = wrr_corrected_distance_from_perturbation_sets(
                app_occurrences,
                date_occurrences,
                text_length=text_length,
                row_width_count=row_width_count,
                minimum_valid=minimum_valid,
            )
            corrected_distance = c_cell(result.corrected_distance)
            status = "defined"
        rows.append(
            {
                "pair_id": pair["pair_id"],
                "concept": pair.get("concept", ""),
                "candidate_lane": pair.get("candidate_lane", ""),
                "pair_review_status": pair.get("pair_review_status", ""),
                "appellation_term_id": app_id,
                "appellation_starts_with_rabbi_title": pair.get(
                    "appellation_starts_with_rabbi_title",
                    "",
                ),
                "date_term_id": date_id,
                "appellation_ordinary_hits": app_stats.ordinary_hits,
                "date_ordinary_hits": date_stats.ordinary_hits,
                "appellation_exact_perturbed_rows": app_stats.exact_perturbed_rows,
                "date_exact_perturbed_rows": date_stats.exact_perturbed_rows,
                "appellation_defined_perturbed_rows": app_stats.defined_perturbed_rows,
                "date_defined_perturbed_rows": date_stats.defined_perturbed_rows,
                "appellation_triples_with_defined_rows": app_stats.triples_with_defined_rows,
                "date_triples_with_defined_rows": date_stats.triples_with_defined_rows,
                "pair_valid_perturbations": len(valid_triples),
                "ordinary_q": ordinary_q,
                "corrected_distance": corrected_distance,
                "corrected_distance_status": status,
                "read": read_label(status, len(valid_triples), minimum_valid),
            }
        )
    return rows


def empty_stats(term_id: str) -> PerturbedTermStats:
    return PerturbedTermStats(term_id, "", 0, 0, 0, 0, 0, 0)


def valid_pair_triples(
    left: dict[tuple[int, int, int], tuple[WrrElsOccurrence, ...]],
    right: dict[tuple[int, int, int], tuple[WrrElsOccurrence, ...]],
) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        triple
        for triple in sorted(set(left) & set(right))
        if left.get(triple) and right.get(triple)
    )


def ordinary_q_cell(
    left: dict[tuple[int, int, int], tuple[WrrElsOccurrence, ...]],
    right: dict[tuple[int, int, int], tuple[WrrElsOccurrence, ...]],
    text_length: int,
    row_width_count: int,
) -> str:
    left_rows = left.get(ORDINARY_PERTURBATION, ())
    right_rows = right.get(ORDINARY_PERTURBATION, ())
    if not left_rows or not right_rows:
        return ""
    return c_cell(
        wrr_word_pair_proximity(
            left_rows,
            right_rows,
            text_length=text_length,
            row_width_count=row_width_count,
        )
    )


def read_label(status: str, valid_triples: int, minimum_valid: int) -> str:
    if status == "defined":
        return "corrected distance defined from generated domain-labeled perturbations"
    if status == "ordinary_not_valid":
        return "undefined: ordinary perturbation lacks a defined-domain pair"
    if status == "under_minimum_valid_perturbations":
        return f"undefined: {valid_triples} valid perturbations below minimum {minimum_valid}"
    return "undefined"


def summarize(
    rows: list[dict[str, object]],
    args: argparse.Namespace,
    *,
    selected_pair_count: int | None = None,
) -> dict[str, object]:
    defined_rows = [
        row for row in rows if row.get("corrected_distance_status") == "defined"
    ]
    min_row = min(
        defined_rows,
        key=lambda row: float(str(row["corrected_distance"])),
        default=None,
    )
    return {
        "selected_pairs": len(rows) if selected_pair_count is None else selected_pair_count,
        "shard_index": args.shard_index,
        "shard_count": args.shard_count,
        "pairs": len(rows),
        "candidate_lane": args.candidate_lane,
        "search_max_skip": args.search_max_skip,
        "skip_cap_mode": args.skip_cap_mode,
        "skip_cap_formula": args.skip_cap_formula,
        "minimum_valid": args.minimum_valid,
        "defined_corrected_distances": len(defined_rows),
        "ordinary_not_valid_pairs": count_status(rows, "ordinary_not_valid"),
        "under_minimum_valid_pairs": count_status(
            rows,
            "under_minimum_valid_perturbations",
        ),
        "min_corrected_distance": "" if min_row is None else min_row["corrected_distance"],
        "min_corrected_pair_id": "" if min_row is None else min_row["pair_id"],
        "max_pair_valid_perturbations": max(
            (int(row["pair_valid_perturbations"]) for row in rows),
            default=0,
        ),
        "status": "diagnostic_only_not_wrr_reproduction",
    }


def count_status(rows: list[dict[str, object]], status: str) -> int:
    return sum(1 for row in rows if row.get("corrected_distance_status") == status)


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary: dict[str, object],
    args: argparse.Namespace,
) -> None:
    lines = [
        "# WRR2 Corrected Distance Smoke",
        "",
        "This generates exact WRR perturbation rows from ordinary ELS hits, labels",
        "their domains conservatively, and computes pair-level corrected distance",
        "when the ordinary triple and minimum valid perturbation count are present.",
        "It remains a smoke diagnostic, not a WRR reproduction.",
        "",
        f"- pair table: `{args.pair_table}`",
        f"- candidate lane: `{args.candidate_lane}`",
        f"- skip cap mode: `{args.skip_cap_mode}`",
        f"- skip cap formula: `{args.skip_cap_formula}`",
        f"- shard: `{args.shard_index}` of `{args.shard_count}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
    ]
    for key in SUMMARY_FIELDNAMES:
        lines.append(f"| `{key}` | {summary[key]} |")
    lines.extend(
        [
            "",
            "## First Rows",
            "",
            "| Pair | Valid triples | Ordinary Q | c(w,w') | Status |",
            "| --- | ---: | ---: | ---: | --- |",
        ]
    )
    for row in rows[:25]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['pair_id']}`",
                    str(row["pair_valid_perturbations"]),
                    str(row["ordinary_q"]),
                    str(row["corrected_distance"]),
                    f"`{row['corrected_distance_status']}`",
                ]
            )
            + " |"
        )
    if not rows:
        lines.append("| none | 0 |  |  | `no_rows` |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    corpus_summary: dict[str, object],
    rows: list[dict[str, object]],
    summary: dict[str, object],
    stats: dict[str, PerturbedTermStats],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "pair_table": str(args.pair_table),
        "config": str(args.config),
        "parameters": {
            "candidate_lane": args.candidate_lane,
            "min_skip": args.min_skip,
            "search_max_skip": args.search_max_skip,
            "direction": args.direction,
            "row_width_count": args.row_width_count,
            "minimum_valid": args.minimum_valid,
            "skip_cap_mode": args.skip_cap_mode,
            "skip_cap_formula": args.skip_cap_formula,
            "target_expected_hits": args.target_expected_hits,
            "shard_index": args.shard_index,
            "shard_count": args.shard_count,
        },
        "corpus": corpus_summary,
        "term_count": len(stats),
        "rows": len(rows),
        "summary": summary,
        "outputs": {
            "csv": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def c_cell(value: float) -> str:
    return f"{value:.12g}"


if __name__ == "__main__":
    raise SystemExit(main())
