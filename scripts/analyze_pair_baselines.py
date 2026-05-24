#!/usr/bin/env python3
"""Compare strict observed pair counts for Gog/Magog and baseline pairs."""

from __future__ import annotations

import argparse
import csv
import json
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.cli import accepted_term_languages
from els.corpus import Corpus, load_corpus
from els.search import normalize_for_corpus
from els.search import process_context
from scripts import analyze_gog_magog_pairs as pair_tool


TERMS = Path("terms/prophetic_terms.csv")
SUMMARY_OUT = Path("reports/pair_baselines_summary.csv")
EXAMPLES_OUT = Path("reports/pair_baselines_examples.csv")
MD_OUT = Path("reports/pair_baselines.md")
MANIFEST_OUT = Path("reports/pair_baselines.manifest.json")


CORPORA = [
    ("MT_WLC", Path("configs/example_oshb_wlc.toml")),
    ("LXX", Path("configs/example_ebible_grclxx.toml")),
    ("TR_NT", Path("configs/example_ebible_grctr.toml")),
    ("SBLGNT", Path("configs/example_sblgnt.toml")),
]


@dataclass(frozen=True)
class PairBaseline:
    pair_id: str
    label: str
    left_hebrew: str
    right_hebrew: str
    left_greek: str
    right_greek: str
    notes: str


BASELINE_PAIRS = (
    PairBaseline(
        "gog_magog",
        "Gog/Magog",
        "gog_h",
        "magog_h",
        "gog_g",
        "magog_g",
        "target pair",
    ),
    PairBaseline(
        "cyrus_darius",
        "Cyrus/Darius",
        "cyrus_h",
        "darius_h",
        "cyrus_g",
        "darius_g",
        "ruler baseline",
    ),
    PairBaseline(
        "beast_dragon",
        "Beast/Dragon",
        "beast_h",
        "dragon_h",
        "beast_g",
        "dragon_g",
        "apocalyptic symbol baseline",
    ),
    PairBaseline(
        "horn_seal",
        "Horn/Seal",
        "horn_h",
        "seal_h",
        "horn_g",
        "seal_g",
        "symbol baseline",
    ),
    PairBaseline(
        "vision_prophet",
        "Vision/Prophet",
        "vision_h",
        "prophet_h",
        "vision_g",
        "prophet_g",
        "prophecy baseline",
    ),
)


@dataclass(frozen=True)
class CorpusBaselineAnalysis:
    manifest: dict[str, object]
    summary_rows: list[dict[str, object]]
    example_rows: list[dict[str, object]]


SUMMARY_FIELDNAMES = [
    "pair_id",
    "pair_label",
    "pair_notes",
    "corpus",
    "left_term_id",
    "left_term",
    "left_normalized",
    "left_hits",
    "right_term_id",
    "right_term",
    "right_normalized",
    "right_hits",
    "max_gap",
    "observed_pairs_within_gap",
    "observed_overlap_pairs",
    "observed_best_span_gap",
    "observed_best_center_distance",
    "strict_filter",
    "read",
]


EXAMPLE_FIELDNAMES = [
    "pair_id",
    "pair_notes",
    *pair_tool.EXAMPLE_FIELDNAMES,
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    term_rows = {row["term_id"]: row for row in read_rows(args.terms)}
    corpora = selected_corpora(args)
    tasks = [(corpus_label, config, term_rows, args) for corpus_label, config in corpora]
    analyses = run_corpus_analyses(tasks, pair_tool.resolve_corpus_jobs(args.jobs, len(tasks)))
    summary_rows = [row for analysis in analyses for row in analysis.summary_rows]
    example_rows = [row for analysis in analyses for row in analysis.example_rows]
    corpus_manifests = [analysis.manifest for analysis in analyses]
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_rows(args.examples_out, EXAMPLE_FIELDNAMES, example_rows)
    write_markdown(args.markdown_out, summary_rows)
    write_manifest(args, corpus_manifests, len(summary_rows), len(example_rows), started)
    print(args.summary_out)
    print(args.examples_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", type=Path, default=TERMS)
    parser.add_argument(
        "--corpus",
        type=pair_tool.parse_corpus_arg,
        action="append",
        metavar="LABEL=CONFIG",
        help="Analyze an explicit corpus config. May be repeated. Defaults to public baseline corpora.",
    )
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=50)
    parser.add_argument(
        "--direction",
        choices=["forward", "backward", "both"],
        default="both",
    )
    parser.add_argument("--max-gap", type=int, default=500)
    parser.add_argument("--max-examples-per-pair-corpus", type=int, default=3)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--hit-jobs", type=int, default=1)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--examples-out", type=Path, default=EXAMPLES_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def selected_corpora(args: argparse.Namespace) -> list[tuple[str, Path]]:
    return list(args.corpus or CORPORA)


def run_corpus_analyses(
    tasks: list[tuple[str, Path, dict[str, dict[str, str]], argparse.Namespace]],
    jobs: int,
) -> list[CorpusBaselineAnalysis]:
    if jobs <= 1:
        return [analyze_corpus_task(task) for task in tasks]
    try:
        executor = ProcessPoolExecutor(max_workers=jobs, mp_context=process_context())
    except PermissionError:
        return [analyze_corpus_task(task) for task in tasks]
    with executor:
        return list(executor.map(analyze_corpus_task, tasks))


def analyze_corpus_task(
    task: tuple[str, Path, dict[str, dict[str, str]], argparse.Namespace],
) -> CorpusBaselineAnalysis:
    corpus_label, config, term_rows, args = task
    corpus_started = time.perf_counter()
    corpus = load_corpus(config)
    corpus_pairs = [
        pair
        for pair in BASELINE_PAIRS
        if pair_terms_for_corpus(pair, corpus, term_rows) is not None
    ]
    queries = sorted(
        {
            query
            for pair in corpus_pairs
            for query in normalized_pair_queries(pair, corpus, term_rows)
        }
    )
    hits_by_query = pair_tool.collect_hits_by_query(
        corpus,
        queries,
        min_skip=args.min_skip,
        max_skip=args.max_skip,
        direction=args.direction,
        jobs=args.hit_jobs,
    )
    summary_rows: list[dict[str, object]] = []
    example_rows: list[dict[str, object]] = []
    for pair in corpus_pairs:
        row, examples = score_baseline_pair(
            pair,
            corpus_label,
            corpus,
            term_rows,
            hits_by_query,
            args,
        )
        summary_rows.append(row)
        example_rows.extend(examples[: args.max_examples_per_pair_corpus])
    return CorpusBaselineAnalysis(
        manifest={
            "label": corpus_label,
            "config": str(config),
            "queries": len(queries),
            "summary": corpus.summary(),
            "seconds": round(time.perf_counter() - corpus_started, 3),
        },
        summary_rows=summary_rows,
        example_rows=example_rows,
    )


def score_baseline_pair(
    pair: PairBaseline,
    corpus_label: str,
    corpus: Corpus,
    term_rows: dict[str, dict[str, str]],
    hits_by_query: dict[str, list[pair_tool.HitLite]],
    args: argparse.Namespace,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    left_id, right_id = pair_terms_for_corpus(pair, corpus, term_rows) or ("", "")
    left_row = term_rows[left_id]
    right_row = term_rows[right_id]
    left_query, right_query = normalized_pair_queries(pair, corpus, term_rows)
    metrics, examples = pair_tool.score_pair(
        corpus_label,
        corpus,
        left_query,
        right_query,
        hits_by_query,
        max_gap=args.max_gap,
        require_same_chapter=True,
        require_same_skip=True,
        keep_examples=True,
    )
    row = {
        "pair_id": pair.pair_id,
        "pair_label": pair.label,
        "pair_notes": pair.notes,
        "corpus": corpus_label,
        "left_term_id": left_id,
        "left_term": left_row["term"],
        "left_normalized": left_query,
        "left_hits": metrics.left_hits,
        "right_term_id": right_id,
        "right_term": right_row["term"],
        "right_normalized": right_query,
        "right_hits": metrics.right_hits,
        "max_gap": args.max_gap,
        "observed_pairs_within_gap": metrics.pairs_within_gap,
        "observed_overlap_pairs": metrics.overlap_pairs,
        "observed_best_span_gap": pair_tool.empty_if_none(metrics.best_span_gap),
        "observed_best_center_distance": pair_tool.round_float(metrics.best_center_distance),
        "strict_filter": "same_chapter;same_signed_skip",
        "read": read_label(metrics),
    }
    result_stub = {
        "pair_label": pair.label,
        "left_term_id": left_id,
        "right_term_id": right_id,
    }
    example_rows = [
        {
            "pair_id": pair.pair_id,
            "pair_notes": pair.notes,
            **pair_tool.example_row(corpus, example, result_stub),
        }
        for example in examples
    ]
    return row, example_rows


def pair_terms_for_corpus(
    pair: PairBaseline,
    corpus: Corpus,
    term_rows: dict[str, dict[str, str]],
) -> tuple[str, str] | None:
    left_id, right_id = (
        (pair.left_hebrew, pair.right_hebrew)
        if corpus.language == "hebrew"
        else (pair.left_greek, pair.right_greek)
    )
    if left_id not in term_rows or right_id not in term_rows:
        return None
    left_row = term_rows[left_id]
    right_row = term_rows[right_id]
    if left_row["language"] not in accepted_term_languages(corpus.language):
        return None
    if right_row["language"] not in accepted_term_languages(corpus.language):
        return None
    return left_id, right_id


def normalized_pair_queries(
    pair: PairBaseline,
    corpus: Corpus,
    term_rows: dict[str, dict[str, str]],
) -> tuple[str, str]:
    left_id, right_id = pair_terms_for_corpus(pair, corpus, term_rows) or ("", "")
    return (
        normalize_for_corpus(corpus, term_rows[left_id]["term"]),
        normalize_for_corpus(corpus, term_rows[right_id]["term"]),
    )


def read_label(metrics: pair_tool.PairMetrics) -> str:
    if metrics.pairs_within_gap == 0:
        return "no strict close pairs"
    if metrics.overlap_pairs:
        return "strict overlap examples present"
    return "strict close examples present"


def write_markdown(path: Path, rows: list[dict[str, object]]) -> None:
    lines = [
        "# Pair Baselines",
        "",
        "Observed strict same-chapter and same-signed-skip pair counts for Gog/Magog and unrelated declared baselines.",
        "",
        "## Summary",
        "",
        "| Pair | Corpus | Left hits | Right hits | Close pairs | Overlaps | Best gap | Read |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["pair_label"]),
                    str(row["corpus"]),
                    str(row["left_hits"]),
                    str(row["right_hits"]),
                    str(row["observed_pairs_within_gap"]),
                    str(row["observed_overlap_pairs"]),
                    str(row["observed_best_span_gap"]),
                    str(row["read"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "This is observed baseline context only. It does not compute paired-control p-values. Use it to decide which non-target pairs deserve full controls.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    corpora: list[dict[str, object]],
    rows: int,
    examples: int,
    started: float,
) -> None:
    payload = {
        "tool": "analyze_pair_baselines",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "terms": str(args.terms),
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "direction": args.direction,
        "max_gap": args.max_gap,
        "jobs": args.jobs,
        "hit_jobs": args.hit_jobs,
        "corpus_args": [f"{label}={config}" for label, config in (args.corpus or [])],
        "strict_filter": "same_chapter;same_signed_skip",
        "pairs": [pair.__dict__ for pair in BASELINE_PAIRS],
        "rows": rows,
        "examples": examples,
        "corpora": corpora,
        "outputs": [
            str(args.summary_out),
            str(args.examples_out),
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


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    raise SystemExit(main())
