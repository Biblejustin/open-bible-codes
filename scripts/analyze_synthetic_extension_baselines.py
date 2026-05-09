#!/usr/bin/env python3
"""Run synthetic same-length baselines for exact-center Greek extension rows."""

from __future__ import annotations

import argparse
import csv
import json
import random
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import Corpus, load_corpus
from els.extensions import (
    ExtensionLexicon,
    ExtensionMatch,
    build_extension_lexicon,
    extensions_for_hit,
)
from els.search import ELSHit, build_hit, iter_els_query_matches_by_lanes
from els.statistics import round_float
from scripts import analyze_extension_paired_controls as paired


BASE = Path("reports/protocols/public_baseline")
TOP_FILES = [
    BASE / "surface_context_extensions_tr_nt_top.csv",
    BASE / "surface_context_extensions_sblgnt_top.csv",
]
SURFACE_CONTEXT_HITS = BASE / "surface_context_hits.csv"

SUMMARY_OUT = Path("reports/synthetic_extension_baselines_summary.csv")
EXAMPLES_OUT = Path("reports/synthetic_extension_baselines_examples.csv")
MATCHES_OUT = Path("reports/synthetic_extension_baselines_matches.csv")
MD_OUT = Path("reports/synthetic_extension_baselines.md")
MANIFEST_OUT = Path("reports/synthetic_extension_baselines.manifest.json")

SUMMARY_FIELDNAMES = [
    "target_id",
    "corpus",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "extension_type",
    "extended_sequence",
    "observed_score",
    "synthetic_samples",
    "synthetic_same_type_mean",
    "synthetic_same_type_max",
    "synthetic_same_type_ge_target",
    "synthetic_same_type_p_ge",
    "synthetic_any_mean",
    "synthetic_any_max",
    "synthetic_any_ge_target",
    "synthetic_any_p_ge",
    "read",
]

EXAMPLE_FIELDNAMES = [
    *SUMMARY_FIELDNAMES,
    "synthetic_queries_sample",
    "synthetic_same_type_scores_sample",
    "synthetic_any_scores_sample",
]

MATCH_FIELDNAMES = [
    "target_id",
    "corpus",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "target_extension_type",
    "target_extended_sequence",
    "observed_score",
    "synthetic_query",
    "synthetic_score",
    "synthetic_extension_type",
    "synthetic_extension_side",
    "synthetic_extension_length",
    "synthetic_extended_sequence",
    "synthetic_matched_examples",
    "synthetic_matched_refs",
    "synthetic_hit_start_ref",
    "synthetic_hit_end_ref",
    "synthetic_hit_center_ref",
    "synthetic_hit_center_word",
    "synthetic_hit_center_normalized_word",
    "synthetic_extension_start_offset",
    "synthetic_extension_end_offset",
    "synthetic_extension_start_ref",
    "synthetic_extension_end_ref",
    "read",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    targets = exact_center_targets(args)
    rows = []
    examples = []
    matches = []
    corpus_manifests = []
    for corpus_label in sorted({target.corpus for target in targets}):
        corpus_started = time.perf_counter()
        corpus = load_corpus(paired.CORPUS_CONFIGS[corpus_label])
        lexicon = build_extension_lexicon(corpus, max_phrase_words=args.phrase_words)
        corpus_targets = [target for target in targets if target.corpus == corpus_label]
        for target in corpus_targets:
            row, example, target_matches = analyze_target(corpus, lexicon, target, args)
            rows.append(row)
            examples.append(example)
            matches.extend(target_matches)
        corpus_manifests.append(
            {
                "label": corpus_label,
                "config": str(paired.CORPUS_CONFIGS[corpus_label]),
                "summary": corpus.summary(),
                "targets": len(corpus_targets),
                "seconds": round(time.perf_counter() - corpus_started, 3),
            }
        )
    rows.sort(key=row_sort_key)
    examples.sort(key=row_sort_key)
    matches.sort(key=match_sort_key)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, rows)
    write_rows(args.examples_out, EXAMPLE_FIELDNAMES, examples)
    write_rows(args.matches_out, MATCH_FIELDNAMES, matches)
    write_markdown(args.markdown_out, rows)
    write_manifest(args, targets, corpus_manifests, len(rows), len(matches), started)
    print(args.summary_out)
    print(args.examples_out)
    print(args.matches_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--top-file", action="append", type=Path)
    parser.add_argument("--surface-context-hits", type=Path, default=SURFACE_CONTEXT_HITS)
    parser.add_argument("--require-cross-corpus-overlap", action="store_true")
    parser.add_argument(
        "--require-overlap-corpus",
        action="append",
        default=[],
        help="Require each overlap key group to include this corpus label. Repeatable.",
    )
    parser.add_argument("--include-overlap-key", action="append", default=[])
    parser.add_argument("--synthetic-samples", type=int, default=100)
    parser.add_argument("--seed", type=int, default=86420)
    parser.add_argument("--max-before", type=int, default=12)
    parser.add_argument("--max-after", type=int, default=12)
    parser.add_argument("--phrase-words", type=int, default=4)
    parser.add_argument("--include-both-sided", action="store_true", default=True)
    parser.add_argument("--max-extensions-per-hit", type=int, default=20)
    parser.add_argument("--min-extension-length", type=int, default=3)
    parser.add_argument("--match-kind-prefix", default="phrase_")
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--examples-out", type=Path, default=EXAMPLES_OUT)
    parser.add_argument("--matches-out", type=Path, default=MATCHES_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def exact_center_targets(args: argparse.Namespace) -> list[paired.ExtensionTarget]:
    target_args = argparse.Namespace(
        top_file=args.top_file,
        require_cross_corpus_overlap=args.require_cross_corpus_overlap,
        require_overlap_corpus=args.require_overlap_corpus,
        include_overlap_key=args.include_overlap_key,
        require_center_exact=True,
        dedupe_targets=True,
        surface_context_hits=args.surface_context_hits,
    )
    targets = paired.read_targets(args.top_file or TOP_FILES)
    surface_context = paired.read_surface_context(args.surface_context_hits)
    return paired.prepare_targets(targets, target_args, surface_context=surface_context)


def analyze_target(
    corpus: Corpus,
    lexicon: ExtensionLexicon,
    target: paired.ExtensionTarget,
    args: argparse.Namespace,
) -> tuple[dict[str, object], dict[str, object], list[dict[str, object]]]:
    queries = paired.sample_random_controls(
        length=len(target.normalized_term),
        corpus_text=corpus.text,
        samples=args.synthetic_samples,
        rng=random.Random(paired.stable_seed(args.seed, target.target_id, "synthetic")),
    )
    scores, matches = score_synthetic_controls(corpus, lexicon, target, queries, args)
    same_ge = ge_count(target.observed_score, scores.same_type_scores)
    any_ge = ge_count(target.observed_score, scores.any_scores)
    row = {
        "target_id": target.target_id,
        "corpus": target.corpus,
        "term": target.row["term"],
        "normalized_term": target.normalized_term,
        "skip": target.row["skip"],
        "direction": target.direction,
        "extension_type": target.extension_type,
        "extended_sequence": target.row["extended_sequence"],
        "observed_score": target.observed_score,
        "synthetic_samples": len(queries),
        "synthetic_same_type_mean": round_float(paired.mean_or_none(scores.same_type_scores)),
        "synthetic_same_type_max": max(scores.same_type_scores) if scores.same_type_scores else "",
        "synthetic_same_type_ge_target": same_ge,
        "synthetic_same_type_p_ge": round_float(
            paired.p_value_ge(target.observed_score, scores.same_type_scores)
        ),
        "synthetic_any_mean": round_float(paired.mean_or_none(scores.any_scores)),
        "synthetic_any_max": max(scores.any_scores) if scores.any_scores else "",
        "synthetic_any_ge_target": any_ge,
        "synthetic_any_p_ge": round_float(
            paired.p_value_ge(target.observed_score, scores.any_scores)
        ),
        "read": synthetic_read(same_ge, any_ge),
    }
    example = dict(row)
    example["synthetic_queries_sample"] = paired.sample_cell(queries)
    example["synthetic_same_type_scores_sample"] = paired.sample_cell(scores.same_type_scores)
    example["synthetic_any_scores_sample"] = paired.sample_cell(scores.any_scores)
    return row, example, matches


def score_synthetic_controls(
    corpus: Corpus,
    lexicon: ExtensionLexicon,
    target: paired.ExtensionTarget,
    queries: tuple[str, ...],
    args: argparse.Namespace,
) -> tuple[paired.ControlScores, list[dict[str, object]]]:
    scores_by_query = {query: (0, 0) for query in queries if query}
    best_match_by_query: dict[str, tuple[int, ExtensionMatch, ELSHit]] = {}
    direction = "forward" if target.skip > 0 else "backward"
    skip = abs(target.skip)
    for query, signed_skip, start, end in iter_els_query_matches_by_lanes(
        corpus.text,
        scores_by_query,
        min_skip=skip,
        max_skip=skip,
        direction=direction,
    ):
        same_type_score, any_score = scores_by_query[query]
        hit = build_hit(corpus, query, query, signed_skip, start, end)
        for extension in extensions_for_hit(
            corpus,
            hit,
            lexicon,
            max_before=args.max_before,
            max_after=args.max_after,
            include_both_sided=args.include_both_sided,
            max_extensions=args.max_extensions_per_hit,
        ):
            if not paired.extension_passes_filter(extension, args):
                continue
            score = paired.extension_score(
                extension.extension_type,
                extension.extension_length,
                extension.match_kind,
                extension.match_count,
            )
            if score > any_score:
                any_score = score
                best_match_by_query[query] = (score, extension, hit)
            if extension.extension_type == target.extension_type:
                same_type_score = max(same_type_score, score)
        scores_by_query[query] = (same_type_score, any_score)
    matches = [
        match_row(target, query, *best_match)
        for query in queries
        if (best_match := best_match_by_query.get(query)) is not None
        and best_match[0] >= target.observed_score
    ]
    return (
        paired.ControlScores(
            same_type_scores=tuple(scores_by_query.get(query, (0, 0))[0] for query in queries),
            any_scores=tuple(scores_by_query.get(query, (0, 0))[1] for query in queries),
            queries=queries,
        ),
        matches,
    )


def match_row(
    target: paired.ExtensionTarget,
    query: str,
    score: int,
    extension: ExtensionMatch,
    hit: ELSHit,
) -> dict[str, object]:
    return {
        "target_id": target.target_id,
        "corpus": target.corpus,
        "term": target.row["term"],
        "normalized_term": target.normalized_term,
        "skip": target.row["skip"],
        "direction": target.direction,
        "target_extension_type": target.extension_type,
        "target_extended_sequence": target.row["extended_sequence"],
        "observed_score": target.observed_score,
        "synthetic_query": query,
        "synthetic_score": score,
        "synthetic_extension_type": extension.extension_type,
        "synthetic_extension_side": extension.extension_side,
        "synthetic_extension_length": extension.extension_length,
        "synthetic_extended_sequence": extension.extended_sequence,
        "synthetic_matched_examples": extension.matched_examples,
        "synthetic_matched_refs": extension.matched_refs,
        "synthetic_hit_start_ref": hit.start_ref,
        "synthetic_hit_end_ref": hit.end_ref,
        "synthetic_hit_center_ref": hit.center_ref,
        "synthetic_hit_center_word": hit.center_word,
        "synthetic_hit_center_normalized_word": hit.center_normalized_word,
        "synthetic_extension_start_offset": extension.extension_start_offset,
        "synthetic_extension_end_offset": extension.extension_end_offset,
        "synthetic_extension_start_ref": extension.extension_start_ref,
        "synthetic_extension_end_ref": extension.extension_end_ref,
        "read": "synthetic any-type score matches or exceeds target",
    }


def ge_count(observed: int, samples: tuple[int, ...]) -> int:
    return sum(1 for sample in samples if sample >= observed)


def synthetic_read(same_type_ge: int, any_ge: int) -> str:
    if same_type_ge or any_ge:
        return "synthetic samples can match or exceed target extension score"
    return "target exceeds sampled synthetic extension score"


def write_markdown(path: Path, rows: list[dict[str, object]]) -> None:
    lines = [
        "# Synthetic Extension Baselines",
        "",
        "Same-length synthetic Greek baselines for exact-center NT extension rows.",
        "",
        "## Target Comparison",
        "",
        "| Corpus | Target | Score | Synthetic any mean | Synthetic >= target | p_ge | Read |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["corpus"]),
                    f"`{row['term']}` {row['skip']} {row['extension_type']} `{row['extended_sequence']}`",
                    str(row["observed_score"]),
                    str(row["synthetic_any_mean"]),
                    str(row["synthetic_any_ge_target"]),
                    str(row["synthetic_any_p_ge"]),
                    str(row["read"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Match details for synthetic rows that equal or exceed target any-type scores are written to `reports/synthetic_extension_baselines_matches.csv`.",
            "",
            "## Caution",
            "",
            "Synthetic strings are density controls, not lexical controls. Existing shuffled-term controls remain the stronger comparison for real-word extension rows.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    targets: list[paired.ExtensionTarget],
    corpora: list[dict[str, object]],
    rows: int,
    matches: int,
    started: float,
) -> None:
    payload = {
        "tool": "analyze_synthetic_extension_baselines",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "top_files": [str(path) for path in (args.top_file or TOP_FILES)],
        "surface_context_hits": str(args.surface_context_hits),
        "require_cross_corpus_overlap": args.require_cross_corpus_overlap,
        "require_overlap_corpus": list(args.require_overlap_corpus),
        "include_overlap_keys": list(args.include_overlap_key),
        "targets": len(targets),
        "synthetic_samples": args.synthetic_samples,
        "max_before": args.max_before,
        "max_after": args.max_after,
        "phrase_words": args.phrase_words,
        "max_extensions_per_hit": args.max_extensions_per_hit,
        "min_extension_length": args.min_extension_length,
        "match_kind_prefix": args.match_kind_prefix,
        "rows": rows,
        "matches": matches,
        "corpora": corpora,
        "outputs": [
            str(args.summary_out),
            str(args.examples_out),
            str(args.matches_out),
            str(args.markdown_out),
            str(args.manifest_out),
        ],
        "seconds": round(time.perf_counter() - started, 3),
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def row_sort_key(row: dict[str, object]) -> tuple[str, str]:
    return (str(row["corpus"]), str(row["target_id"]))


def match_sort_key(row: dict[str, object]) -> tuple[str, str, int]:
    return (
        str(row["corpus"]),
        str(row["target_id"]),
        -int(row["synthetic_score"]),
    )


if __name__ == "__main__":
    raise SystemExit(main())
