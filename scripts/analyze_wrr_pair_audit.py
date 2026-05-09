#!/usr/bin/env python3
"""Audit same-record WRR appellation/date ELS pair proximity."""

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
from els.search import build_hit, iter_els_query_matches_by_lanes, normalize_for_corpus
from els.wrr import wrr_els_els_alpha
from scripts import analyze_gog_magog_pairs as pair_tool


TERMS = Path("reports/wrr_1994/wrr2_terms.csv")
CONFIG = Path("configs/example_koren_genesis.toml")
SUMMARY_OUT = Path("reports/wrr_1994/wrr2_genesis_pair_audit_summary.csv")
CONCEPT_OUT = Path("reports/wrr_1994/wrr2_genesis_pair_audit_concepts.csv")
EXAMPLES_OUT = Path("reports/wrr_1994/wrr2_genesis_pair_audit_examples.csv")
MD_OUT = Path("reports/wrr_1994/wrr2_genesis_pair_audit.md")
MANIFEST_OUT = Path("reports/wrr_1994/wrr2_genesis_pair_audit.manifest.json")

APP_CATEGORY = "wrr_appellation"
DATE_CATEGORY = "wrr_date"

PAIR_FIELDNAMES = [
    "corpus",
    "concept",
    "appellation_term_id",
    "appellation_term",
    "appellation_normalized",
    "appellation_length",
    "appellation_hits",
    "date_term_id",
    "date_term",
    "date_normalized",
    "date_length",
    "date_hits",
    "max_gap",
    "all_pairs_within_gap",
    "all_overlap_pairs",
    "same_chapter_pairs_within_gap",
    "same_signed_skip_pairs_within_gap",
    "strict_pairs_within_gap",
    "best_span_gap",
    "best_center_distance",
    "best_example_wrr_alpha",
    "read",
]

CONCEPT_FIELDNAMES = [
    "corpus",
    "concept",
    "pair_rows",
    "appellation_term_rows",
    "date_term_rows",
    "all_pairs_within_gap",
    "all_overlap_pairs",
    "same_chapter_pairs_within_gap",
    "same_signed_skip_pairs_within_gap",
    "strict_pairs_within_gap",
    "best_span_gap",
    "best_center_distance",
    "best_wrr_alpha",
    "best_appellation_term_id",
    "best_date_term_id",
    "read",
]

EXAMPLE_FIELDNAMES = [
    "corpus",
    "concept",
    "appellation_term_id",
    "appellation_term",
    "appellation_skip",
    "appellation_start_ref",
    "appellation_end_ref",
    "appellation_center_ref",
    "appellation_center_word",
    "date_term_id",
    "date_term",
    "date_skip",
    "date_start_ref",
    "date_end_ref",
    "date_center_ref",
    "date_center_word",
    "span_gap",
    "center_distance",
    "wrr_alpha",
    "same_signed_skip",
    "shared_chapters",
]


@dataclass(frozen=True)
class WrrTerm:
    term_id: str
    concept: str
    category: str
    term: str
    normalized: str

    @property
    def length(self) -> int:
        return len(self.normalized)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    corpus = load_corpus(args.config)
    corpus_label = args.corpus_label or corpus.name
    terms_by_concept = collect_pair_terms(
        read_rows(args.terms),
        corpus,
        min_term_length=args.min_term_length,
        max_term_length=args.max_term_length,
    )
    queries = sorted(
        {
            term.normalized
            for terms in terms_by_concept.values()
            for term in terms
        }
    )
    hits_by_query = collect_hits_by_query(
        corpus,
        queries,
        min_skip=args.min_skip,
        max_skip=args.max_skip,
        direction=args.direction,
        jobs=args.jobs,
    )
    pair_rows, example_rows = audit_pairs(corpus_label, corpus, terms_by_concept, hits_by_query, args)
    concept_rows = summarize_concepts(corpus_label, pair_rows)

    write_rows(args.summary_out, PAIR_FIELDNAMES, pair_rows)
    write_rows(args.concept_out, CONCEPT_FIELDNAMES, concept_rows)
    write_rows(args.examples_out, EXAMPLE_FIELDNAMES, example_rows)
    write_markdown(args.markdown_out, corpus_label, pair_rows, concept_rows, args)
    if args.manifest_out:
        write_manifest(args, corpus, queries, pair_rows, concept_rows, example_rows, started)

    print(args.summary_out)
    print(args.concept_out)
    print(args.examples_out)
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
    parser.add_argument("--max-gap", type=int, default=500)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--max-examples-per-pair", type=int, default=3)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--concept-out", type=Path, default=CONCEPT_OUT)
    parser.add_argument("--examples-out", type=Path, default=EXAMPLES_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def collect_pair_terms(
    rows: list[dict[str, str]],
    corpus: Corpus,
    min_term_length: int,
    max_term_length: int | None = None,
) -> dict[str, list[WrrTerm]]:
    languages = accepted_term_languages(corpus.language)
    terms_by_concept: dict[str, list[WrrTerm]] = {}
    for row in rows:
        category = row.get("category", "")
        if category not in {APP_CATEGORY, DATE_CATEGORY}:
            continue
        if row.get("language", "").strip() not in languages:
            continue
        normalized = normalize_for_corpus(corpus, row.get("term", ""))
        if len(normalized) < min_term_length:
            continue
        if max_term_length is not None and len(normalized) > max_term_length:
            continue
        term = WrrTerm(
            term_id=row["term_id"],
            concept=row.get("concept", ""),
            category=category,
            term=row.get("term", ""),
            normalized=normalized,
        )
        terms_by_concept.setdefault(term.concept, []).append(term)
    return {
        concept: sorted(terms, key=lambda term: (term.category, term.term_id))
        for concept, terms in terms_by_concept.items()
        if has_appellation_and_date(terms)
    }


def has_appellation_and_date(terms: list[WrrTerm]) -> bool:
    categories = {term.category for term in terms}
    return APP_CATEGORY in categories and DATE_CATEGORY in categories


def collect_hits_by_query(
    corpus: Corpus,
    queries: list[str],
    *,
    min_skip: int,
    max_skip: int,
    direction: str,
    jobs: int,
) -> dict[str, list[pair_tool.HitLite]]:
    hits_by_query = {query: [] for query in queries}
    for query, skip, start, end in iter_els_query_matches_by_lanes(
        corpus.text,
        queries,
        min_skip=min_skip,
        max_skip=max_skip,
        direction=direction,
        jobs=jobs,
    ):
        hits_by_query[query].append(pair_tool.HitLite(query=query, skip=skip, start=start, end=end))
    for hits in hits_by_query.values():
        hits.sort(key=lambda hit: hit.center)
    return hits_by_query


def audit_pairs(
    corpus_label: str,
    corpus: Corpus,
    terms_by_concept: dict[str, list[WrrTerm]],
    hits_by_query: dict[str, list[pair_tool.HitLite]],
    args: argparse.Namespace,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    pair_rows: list[dict[str, object]] = []
    example_rows: list[dict[str, object]] = []
    chapter_cache: dict[pair_tool.HitLite, set[str]] = {}

    for concept in sorted(terms_by_concept):
        terms = terms_by_concept[concept]
        appellations = [term for term in terms if term.category == APP_CATEGORY]
        dates = [term for term in terms if term.category == DATE_CATEGORY]
        for appellation in appellations:
            for date in dates:
                row, examples = audit_pair(
                    corpus_label,
                    corpus,
                    appellation,
                    date,
                    hits_by_query,
                    args.max_gap,
                    chapter_cache,
                )
                pair_rows.append(row)
                for example in examples[: args.max_examples_per_pair]:
                    example_rows.append(example_row(corpus, appellation, date, row, example))
    return pair_rows, example_rows


def audit_pair(
    corpus_label: str,
    corpus: Corpus,
    appellation: WrrTerm,
    date: WrrTerm,
    hits_by_query: dict[str, list[pair_tool.HitLite]],
    max_gap: int,
    chapter_cache: dict[pair_tool.HitLite, set[str]],
) -> tuple[dict[str, object], list[pair_tool.PairExample]]:
    all_metrics, examples = pair_tool.score_pair(
        corpus_label,
        corpus,
        appellation.normalized,
        date.normalized,
        hits_by_query,
        max_gap=max_gap,
        keep_examples=True,
        chapter_cache=chapter_cache,
    )
    chapter_metrics = pair_tool.score_pair(
        corpus_label,
        corpus,
        appellation.normalized,
        date.normalized,
        hits_by_query,
        max_gap=max_gap,
        require_same_chapter=True,
        keep_examples=False,
        chapter_cache=chapter_cache,
    )[0]
    same_skip_metrics = pair_tool.score_pair(
        corpus_label,
        corpus,
        appellation.normalized,
        date.normalized,
        hits_by_query,
        max_gap=max_gap,
        require_same_skip=True,
        keep_examples=False,
        chapter_cache=chapter_cache,
    )[0]
    strict_metrics = pair_tool.score_pair(
        corpus_label,
        corpus,
        appellation.normalized,
        date.normalized,
        hits_by_query,
        max_gap=max_gap,
        require_same_chapter=True,
        require_same_skip=True,
        keep_examples=False,
        chapter_cache=chapter_cache,
    )[0]
    row = {
        "corpus": corpus_label,
        "concept": appellation.concept,
        "appellation_term_id": appellation.term_id,
        "appellation_term": appellation.term,
        "appellation_normalized": appellation.normalized,
        "appellation_length": appellation.length,
        "appellation_hits": all_metrics.left_hits,
        "date_term_id": date.term_id,
        "date_term": date.term,
        "date_normalized": date.normalized,
        "date_length": date.length,
        "date_hits": all_metrics.right_hits,
        "max_gap": max_gap,
        "all_pairs_within_gap": all_metrics.pairs_within_gap,
        "all_overlap_pairs": all_metrics.overlap_pairs,
        "same_chapter_pairs_within_gap": chapter_metrics.pairs_within_gap,
        "same_signed_skip_pairs_within_gap": same_skip_metrics.pairs_within_gap,
        "strict_pairs_within_gap": strict_metrics.pairs_within_gap,
        "best_span_gap": empty_if_none(all_metrics.best_span_gap),
        "best_center_distance": round_float(all_metrics.best_center_distance),
        "best_example_wrr_alpha": best_example_wrr_alpha(examples),
        "read": read_label(all_metrics, chapter_metrics, same_skip_metrics, strict_metrics),
    }
    return row, examples


def summarize_concepts(corpus_label: str, pair_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows_by_concept: dict[str, list[dict[str, object]]] = {}
    for row in pair_rows:
        rows_by_concept.setdefault(str(row["concept"]), []).append(row)

    output = []
    for concept, rows in rows_by_concept.items():
        best = best_pair_row(rows)
        output.append(
            {
                "corpus": corpus_label,
                "concept": concept,
                "pair_rows": len(rows),
                "appellation_term_rows": len({row["appellation_term_id"] for row in rows}),
                "date_term_rows": len({row["date_term_id"] for row in rows}),
                "all_pairs_within_gap": sum_int(rows, "all_pairs_within_gap"),
                "all_overlap_pairs": sum_int(rows, "all_overlap_pairs"),
                "same_chapter_pairs_within_gap": sum_int(rows, "same_chapter_pairs_within_gap"),
                "same_signed_skip_pairs_within_gap": sum_int(
                    rows,
                    "same_signed_skip_pairs_within_gap",
                ),
                "strict_pairs_within_gap": sum_int(rows, "strict_pairs_within_gap"),
                "best_span_gap": best.get("best_span_gap", "") if best else "",
                "best_center_distance": best.get("best_center_distance", "") if best else "",
                "best_wrr_alpha": best_wrr_alpha(rows),
                "best_appellation_term_id": best.get("appellation_term_id", "") if best else "",
                "best_date_term_id": best.get("date_term_id", "") if best else "",
                "read": concept_read_label(rows),
            }
        )
    return sorted(output, key=lambda row: str(row["concept"]))


def best_pair_row(rows: list[dict[str, object]]) -> dict[str, object] | None:
    scored = [row for row in rows if row.get("best_span_gap") not in ("", None)]
    if not scored:
        return None
    return min(
        scored,
        key=lambda row: (
            int_or_zero(row.get("best_span_gap")),
            float_or_large(row.get("best_center_distance")),
        ),
    )


def example_row(
    corpus: Corpus,
    appellation: WrrTerm,
    date: WrrTerm,
    pair_row: dict[str, object],
    example: pair_tool.PairExample,
) -> dict[str, object]:
    app_hit = build_hit(
        corpus,
        appellation.term,
        appellation.normalized,
        example.left_hit.skip,
        example.left_hit.start,
        example.left_hit.end,
    )
    date_hit = build_hit(
        corpus,
        date.term,
        date.normalized,
        example.right_hit.skip,
        example.right_hit.start,
        example.right_hit.end,
    )
    shared_chapters = sorted(
        pair_tool.hit_chapters(corpus, example.left_hit)
        & pair_tool.hit_chapters(corpus, example.right_hit)
    )
    return {
        "corpus": pair_row["corpus"],
        "concept": pair_row["concept"],
        "appellation_term_id": appellation.term_id,
        "appellation_term": appellation.term,
        "appellation_skip": app_hit.skip,
        "appellation_start_ref": app_hit.start_ref,
        "appellation_end_ref": app_hit.end_ref,
        "appellation_center_ref": app_hit.center_ref,
        "appellation_center_word": app_hit.center_word,
        "date_term_id": date.term_id,
        "date_term": date.term,
        "date_skip": date_hit.skip,
        "date_start_ref": date_hit.start_ref,
        "date_end_ref": date_hit.end_ref,
        "date_center_ref": date_hit.center_ref,
        "date_center_word": date_hit.center_word,
        "span_gap": example.span_gap,
        "center_distance": round_float(example.center_distance),
        "wrr_alpha": round_float(wrr_alpha_for_example(example)),
        "same_signed_skip": app_hit.skip == date_hit.skip,
        "shared_chapters": ";".join(shared_chapters),
    }


def write_markdown(
    path: Path,
    corpus_label: str,
    pair_rows: list[dict[str, object]],
    concept_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    close_rows = [row for row in pair_rows if int_or_zero(row["all_pairs_within_gap"]) > 0]
    strict_rows = [row for row in pair_rows if int_or_zero(row["strict_pairs_within_gap"]) > 0]
    top_concepts = sorted(
        concept_rows,
        key=lambda row: (
            -int_or_zero(row["strict_pairs_within_gap"]),
            -int_or_zero(row["all_pairs_within_gap"]),
            int_or_large(row["best_span_gap"]),
        ),
    )[:20]
    top_pairs = sorted(
        pair_rows,
        key=lambda row: (
            -int_or_zero(row["strict_pairs_within_gap"]),
            -int_or_zero(row["all_pairs_within_gap"]),
            int_or_large(row["best_span_gap"]),
        ),
    )[:20]
    lines = [
        "# WRR2 Genesis Pair Audit",
        "",
        "This is a same-record appellation/date proximity smoke test for the imported external WRR2 list. It is not the WRR aggregate statistic.",
        "",
        "## Scope",
        "",
        f"- Corpus: `{corpus_label}`",
        f"- Skip range: `{args.min_skip}..{args.max_skip}`",
        f"- Direction: `{args.direction}`",
        f"- Max gap: `{args.max_gap}`",
        f"- Term length: `{term_length_label(args)}`",
        "- Pairing: appellation rows only against date rows with the same imported WRR record concept",
        "",
        "## Totals",
        "",
        "| Item | Count |",
        "| --- | ---: |",
        f"| concept rows | {len(concept_rows)} |",
        f"| pair rows | {len(pair_rows)} |",
        f"| pair rows with close hits | {len(close_rows)} |",
        f"| pair rows with strict same-chapter/same-skip close hits | {len(strict_rows)} |",
        f"| all close pairs | {sum_int(pair_rows, 'all_pairs_within_gap')} |",
        f"| all overlap pairs | {sum_int(pair_rows, 'all_overlap_pairs')} |",
        f"| strict close pairs | {sum_int(pair_rows, 'strict_pairs_within_gap')} |",
        "",
        "## Top Concepts",
        "",
        "| Concept | Pairs | Close | Same chapter | Same skip | Strict | Best gap | Best alpha | Best app | Best date | Read |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for row in top_concepts:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["concept"]),
                    str(row["pair_rows"]),
                    str(row["all_pairs_within_gap"]),
                    str(row["same_chapter_pairs_within_gap"]),
                    str(row["same_signed_skip_pairs_within_gap"]),
                    str(row["strict_pairs_within_gap"]),
                    str(row["best_span_gap"]),
                    str(row["best_wrr_alpha"]),
                    f"`{row['best_appellation_term_id']}`",
                    f"`{row['best_date_term_id']}`",
                    str(row["read"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Top Pair Rows",
            "",
            "| Concept | Appellation | Date | App hits | Date hits | Close | Strict | Best gap | Best alpha | Read |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in top_pairs:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["concept"]),
                    f"`{row['appellation_term_id']}` `{row['appellation_normalized']}`",
                    f"`{row['date_term_id']}` `{row['date_normalized']}`",
                    str(row["appellation_hits"]),
                    str(row["date_hits"]),
                    str(row["all_pairs_within_gap"]),
                    str(row["strict_pairs_within_gap"]),
                    str(row["best_span_gap"]),
                    str(row["best_example_wrr_alpha"]),
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
            "This audit only checks nearest ELS hit proximity for imported rows. The `alpha` values use the WRR 1994 fixed-hit cylinder-distance primitive, but the report still does not implement WRR domain weights, aggregate `Q`, corrected-distance rank transform, or permutation test.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    args: argparse.Namespace,
    corpus: Corpus,
    queries: list[str],
    pair_rows: list[dict[str, object]],
    concept_rows: list[dict[str, object]],
    example_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "terms": str(args.terms),
        "config": str(args.config),
        "corpus": corpus.summary(),
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "direction": args.direction,
        "min_term_length": args.min_term_length,
        "max_term_length": args.max_term_length,
        "max_gap": args.max_gap,
        "queries": len(queries),
        "pair_rows": len(pair_rows),
        "concept_rows": len(concept_rows),
        "example_rows": len(example_rows),
        "outputs": {
            "summary": str(args.summary_out),
            "concepts": str(args.concept_out),
            "examples": str(args.examples_out),
            "markdown": str(args.markdown_out),
        },
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_label(
    all_metrics: pair_tool.PairMetrics,
    chapter_metrics: pair_tool.PairMetrics,
    same_skip_metrics: pair_tool.PairMetrics,
    strict_metrics: pair_tool.PairMetrics,
) -> str:
    if all_metrics.pairs_within_gap == 0:
        return "no close same-record pairs"
    if strict_metrics.pairs_within_gap > 0:
        return "strict same-chapter and same-skip pair; audit only"
    if chapter_metrics.pairs_within_gap > 0:
        return "same-chapter pair; audit only"
    if same_skip_metrics.pairs_within_gap > 0:
        return "same-skip pair; audit only"
    return "close pair; audit only"


def hit_offsets(hit: pair_tool.HitLite) -> tuple[int, ...]:
    return tuple(hit.start + index * hit.skip for index in range(len(hit.query)))


def wrr_alpha_for_example(example: pair_tool.PairExample) -> float:
    return wrr_els_els_alpha(
        hit_offsets(example.left_hit),
        hit_offsets(example.right_hit),
        left_skip=example.left_hit.skip,
        right_skip=example.right_hit.skip,
    )


def best_example_wrr_alpha(examples: list[pair_tool.PairExample]) -> float | str:
    if not examples:
        return ""
    return round_float(max(wrr_alpha_for_example(example) for example in examples))


def best_wrr_alpha(rows: list[dict[str, object]]) -> float | str:
    values = [
        float(row["best_example_wrr_alpha"])
        for row in rows
        if row.get("best_example_wrr_alpha") not in ("", None)
    ]
    if not values:
        return ""
    return round_float(max(values))


def concept_read_label(rows: list[dict[str, object]]) -> str:
    if sum_int(rows, "all_pairs_within_gap") == 0:
        return "no close same-record pairs"
    if sum_int(rows, "strict_pairs_within_gap") > 0:
        return "strict rows present; audit only"
    if sum_int(rows, "same_chapter_pairs_within_gap") > 0:
        return "same-chapter rows present; audit only"
    return "close rows present; audit only"


def sum_int(rows: list[dict[str, object]], key: str) -> int:
    return sum(int_or_zero(row.get(key)) for row in rows)


def int_or_zero(value: object) -> int:
    if value in ("", None):
        return 0
    return int(float(str(value)))


def int_or_large(value: object) -> int:
    if value in ("", None):
        return 10**12
    return int_or_zero(value)


def float_or_large(value: object) -> float:
    if value in ("", None):
        return 10**12
    return float(str(value))


def round_float(value: float | None) -> float | str:
    return "" if value is None else round(value, 1)


def empty_if_none(value: int | None) -> int | str:
    return "" if value is None else value


def term_length_label(args: argparse.Namespace) -> str:
    if args.max_term_length is None:
        return f"{args.min_term_length}+"
    return f"{args.min_term_length}..{args.max_term_length}"


if __name__ == "__main__":
    raise SystemExit(main())
