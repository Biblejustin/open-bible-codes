#!/usr/bin/env python3
"""Label WRR ELS hits with conservative domains of minimality."""

from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.cli import accepted_term_languages
from els.corpus import Corpus, load_corpus
from els.search import iter_els_query_matches_by_lanes, normalize_for_corpus
from els.wrr import WrrDomainAssignment, wrr_label_minimality_domains


TERMS = Path("reports/wrr_1994/wrr2_terms.csv")
CONFIG = Path("configs/example_koren_genesis.toml")
ASSIGNMENTS_OUT = Path("reports/wrr_1994/wrr2_domain_assignments.csv")
SUMMARY_OUT = Path("reports/wrr_1994/wrr2_domain_summary.csv")
MD_OUT = Path("reports/wrr_1994/wrr2_domain_labeling.md")
MANIFEST_OUT = Path("reports/wrr_1994/wrr2_domain_labeling.manifest.json")

WRR_CATEGORIES = {"wrr_appellation", "wrr_date"}

ASSIGNMENT_FIELDNAMES = [
    "corpus",
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "normalized_length",
    "hit_index",
    "skip",
    "start_offset",
    "end_offset",
    "domain_status",
    "domain_reason",
    "domain_candidate_count",
    "domain_start",
    "domain_end",
    "domain_length",
]

SUMMARY_FIELDNAMES = [
    "corpus",
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "normalized_length",
    "hit_count",
    "defined_domains",
    "undefined_domains",
    "blocked_by_inner_shorter_skip",
    "ambiguous_enclosing_shorter_skip",
    "undefined_rate",
    "read",
]


@dataclass(frozen=True)
class DomainTerm:
    term_id: str
    concept: str
    category: str
    term: str
    normalized: str


@dataclass(frozen=True)
class DomainHit:
    offsets: tuple[int, ...]
    skip: int
    start_offset: int
    end_offset: int


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    corpus = load_corpus(args.config)
    corpus_label = args.corpus_label or corpus.name
    terms = collect_terms(
        read_rows(args.terms),
        corpus,
        min_term_length=args.min_term_length,
        max_term_length=args.max_term_length,
    )
    queries = sorted({term.normalized for term in terms})
    hits_by_query = collect_domain_hits_by_query(
        corpus,
        queries,
        min_skip=args.min_skip,
        max_skip=args.max_skip,
        direction=args.direction,
        jobs=args.jobs,
    )
    assignments_by_query = {
        query: label_hits(hits, text_length=len(corpus.text))
        for query, hits in hits_by_query.items()
    }
    assignment_rows = build_assignment_rows(
        corpus_label,
        terms,
        hits_by_query,
        assignments_by_query,
    )
    summary_rows = summarize_terms(corpus_label, terms, assignments_by_query)

    write_rows(args.assignments_out, ASSIGNMENT_FIELDNAMES, assignment_rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, corpus_label, summary_rows, args)
    if args.manifest_out:
        write_manifest(args, corpus, terms, assignment_rows, summary_rows, started)

    print(args.assignments_out)
    print(args.summary_out)
    print(args.markdown_out)
    if args.manifest_out:
        print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", type=Path, default=TERMS)
    parser.add_argument("--config", type=Path, default=CONFIG)
    parser.add_argument("--corpus-label")
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=250)
    parser.add_argument(
        "--direction",
        choices=["forward", "backward", "both"],
        default="both",
    )
    parser.add_argument("--min-term-length", type=int, default=3)
    parser.add_argument("--max-term-length", type=int)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--assignments-out", type=Path, default=ASSIGNMENTS_OUT)
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
    max_term_length: int | None = None,
) -> list[DomainTerm]:
    languages = accepted_term_languages(corpus.language)
    terms: list[DomainTerm] = []
    for row in rows:
        category = row.get("category", "")
        if category not in WRR_CATEGORIES:
            continue
        if row.get("language", "").strip() not in languages:
            continue
        normalized = normalize_for_corpus(corpus, row.get("term", ""))
        if len(normalized) < min_term_length:
            continue
        if max_term_length is not None and len(normalized) > max_term_length:
            continue
        terms.append(
            DomainTerm(
                term_id=row["term_id"],
                concept=row.get("concept", ""),
                category=category,
                term=row.get("term", ""),
                normalized=normalized,
            )
        )
    return sorted(terms, key=lambda term: (term.concept, term.category, term.term_id))


def collect_domain_hits_by_query(
    corpus: Corpus,
    queries: list[str],
    *,
    min_skip: int,
    max_skip: int,
    direction: str,
    jobs: int,
) -> dict[str, list[DomainHit]]:
    hits_by_query: dict[str, list[DomainHit]] = {query: [] for query in queries}
    for query, skip, start, end in iter_els_query_matches_by_lanes(
        corpus.text,
        queries,
        min_skip=min_skip,
        max_skip=max_skip,
        direction=direction,
        jobs=jobs,
    ):
        hits_by_query[query].append(
            DomainHit(
                offsets=hit_offsets(start, skip, len(query)),
                skip=skip,
                start_offset=start,
                end_offset=end,
            )
        )
    for hits in hits_by_query.values():
        hits.sort(key=lambda hit: (hit.start_offset, abs(hit.skip), hit.skip, hit.end_offset))
    return hits_by_query


def hit_offsets(start: int, skip: int, length: int) -> tuple[int, ...]:
    return tuple(start + index * skip for index in range(length))


def label_hits(hits: list[DomainHit], *, text_length: int) -> tuple[WrrDomainAssignment, ...]:
    return wrr_label_minimality_domains(
        ((hit.offsets, hit.skip) for hit in hits),
        text_length=text_length,
    )


def build_assignment_rows(
    corpus_label: str,
    terms: list[DomainTerm],
    hits_by_query: dict[str, list[DomainHit]],
    assignments_by_query: dict[str, tuple[WrrDomainAssignment, ...]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for term in terms:
        hits = hits_by_query.get(term.normalized, [])
        assignments = assignments_by_query.get(term.normalized, ())
        for hit_index, (hit, assignment) in enumerate(
            zip(hits, assignments, strict=True),
            start=1,
        ):
            rows.append(assignment_row(corpus_label, term, hit_index, hit, assignment))
    return rows


def assignment_row(
    corpus_label: str,
    term: DomainTerm,
    hit_index: int,
    hit: DomainHit,
    assignment: WrrDomainAssignment,
) -> dict[str, object]:
    domain_length = ""
    if assignment.domain_start is not None and assignment.domain_end is not None:
        domain_length = assignment.domain_end - assignment.domain_start
    return {
        "corpus": corpus_label,
        "term_id": term.term_id,
        "concept": term.concept,
        "category": term.category,
        "term": term.term,
        "normalized_term": term.normalized,
        "normalized_length": len(term.normalized),
        "hit_index": hit_index,
        "skip": hit.skip,
        "start_offset": hit.start_offset,
        "end_offset": hit.end_offset,
        "domain_status": assignment.status,
        "domain_reason": assignment.reason,
        "domain_candidate_count": assignment.candidate_count,
        "domain_start": empty_if_none(assignment.domain_start),
        "domain_end": empty_if_none(assignment.domain_end),
        "domain_length": domain_length,
    }


def summarize_terms(
    corpus_label: str,
    terms: list[DomainTerm],
    assignments_by_query: dict[str, tuple[WrrDomainAssignment, ...]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for term in terms:
        assignments = assignments_by_query.get(term.normalized, ())
        defined = sum(1 for assignment in assignments if assignment.status == "defined")
        blocked = sum(
            1
            for assignment in assignments
            if assignment.reason == "blocked_by_inner_shorter_skip"
        )
        ambiguous = sum(
            1
            for assignment in assignments
            if assignment.reason == "ambiguous_enclosing_shorter_skip"
        )
        undefined = len(assignments) - defined
        rows.append(
            {
                "corpus": corpus_label,
                "term_id": term.term_id,
                "concept": term.concept,
                "category": term.category,
                "term": term.term,
                "normalized_term": term.normalized,
                "normalized_length": len(term.normalized),
                "hit_count": len(assignments),
                "defined_domains": defined,
                "undefined_domains": undefined,
                "blocked_by_inner_shorter_skip": blocked,
                "ambiguous_enclosing_shorter_skip": ambiguous,
                "undefined_rate": ratio(undefined, len(assignments)),
                "read": summary_read_label(defined, blocked, ambiguous),
            }
        )
    return rows


def summary_read_label(defined: int, blocked: int, ambiguous: int) -> str:
    undefined = blocked + ambiguous
    if defined == 0 and undefined == 0:
        return "no hits"
    if undefined == 0:
        return "all domains defined under conservative helper"
    if defined == 0 and ambiguous == 0:
        return "all domains blocked by inner shorter-skip rows"
    if defined == 0 and blocked == 0:
        return "all domains ambiguous from enclosing shorter-skip rows"
    if defined == 0:
        return "all domains undefined under conservative helper"
    return "mixed defined and undefined domains"


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    corpus_label: str,
    rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    totals = summarize_totals(rows)
    lines = [
        "# WRR Domain Labeling Diagnostic",
        "",
        f"- corpus: `{corpus_label}`",
        f"- terms: `{len(rows)}`",
        f"- min skip: `{args.min_skip}`",
        f"- max skip: `{args.max_skip}`",
        f"- direction: `{args.direction}`",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
    ]
    for key, value in totals.items():
        lines.append(f"| {key} | {value} |")
    lines.extend(
        [
            "",
            "## Terms With Undefined Domains",
            "",
            "| Term ID | Concept | Category | Hit count | Undefined | Blocked | Ambiguous | Undefined rate | Read |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    shown = 0
    for row in sorted(rows, key=undefined_sort_key):
        if int(row["undefined_domains"]) == 0:
            continue
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["term_id"]),
                    str(row["concept"]),
                    str(row["category"]),
                    str(row["hit_count"]),
                    str(row["undefined_domains"]),
                    str(row["blocked_by_inner_shorter_skip"]),
                    str(row["ambiguous_enclosing_shorter_skip"]),
                    str(row["undefined_rate"]),
                    str(row["read"]),
                ]
            )
            + " |"
        )
        shown += 1
        if shown >= 25:
            break
    if shown == 0:
        lines.append("| none |  |  | 0 | 0 | 0 | 0 | 0 | all domains defined or no hits |")
    lines.extend(
        [
            "",
            "This is a domain-labeling diagnostic for future corrected-distance "
            "work. Undefined rows are not exclusions; they mark cases needing "
            "source-checked handling before a WRR reproduction run.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def summarize_totals(rows: list[dict[str, object]]) -> dict[str, int]:
    return {
        "terms": len(rows),
        "terms_with_hits": sum(1 for row in rows if int(row["hit_count"]) > 0),
        "terms_with_undefined_domains": sum(
            1 for row in rows if int(row["undefined_domains"]) > 0
        ),
        "hits": sum(int(row["hit_count"]) for row in rows),
        "defined_domains": sum(int(row["defined_domains"]) for row in rows),
        "undefined_domains": sum(int(row["undefined_domains"]) for row in rows),
        "blocked_by_inner_shorter_skip": sum(
            int(row["blocked_by_inner_shorter_skip"]) for row in rows
        ),
        "ambiguous_enclosing_shorter_skip": sum(
            int(row["ambiguous_enclosing_shorter_skip"]) for row in rows
        ),
    }


def undefined_sort_key(row: dict[str, object]) -> tuple[int, int, str]:
    return (
        -int(row["undefined_domains"]),
        -int(row["hit_count"]),
        str(row["term_id"]),
    )


def write_manifest(
    args: argparse.Namespace,
    corpus: Corpus,
    terms: list[DomainTerm],
    assignment_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "analyze_wrr_domain_labeling",
        "version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "inputs": {
            "terms": str(args.terms),
            "config": str(args.config),
            "corpus": corpus.summary(),
        },
        "parameters": {
            "min_skip": args.min_skip,
            "max_skip": args.max_skip,
            "direction": args.direction,
            "min_term_length": args.min_term_length,
            "max_term_length": args.max_term_length,
            "jobs": args.jobs,
        },
        "outputs": {
            "assignments": str(args.assignments_out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
        },
        "counts": {
            "terms": len(terms),
            "assignment_rows": len(assignment_rows),
            "summary_rows": len(summary_rows),
        },
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def empty_if_none(value: int | None) -> int | str:
    if value is None:
        return ""
    return value


def ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 6)


if __name__ == "__main__":
    raise SystemExit(main())
