#!/usr/bin/env python3
"""Run length-matched synthetic Hebrew pair baselines."""

from __future__ import annotations

import argparse
import csv
import json
import random
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import Corpus, load_corpus
from els.statistics import round_float, tail_p_value_ge
from scripts import analyze_gog_magog_pairs as pair_tool


CONFIG = Path("configs/example_oshb_wlc.toml")
PAIR_BASELINES = Path("reports/pair_baselines_summary.csv")
SUMMARY_OUT = Path("reports/synthetic_pair_baselines_summary.csv")
COMPARISON_OUT = Path("reports/synthetic_pair_baselines_comparison.csv")
MD_OUT = Path("reports/synthetic_pair_baselines.md")
MANIFEST_OUT = Path("reports/synthetic_pair_baselines.manifest.json")

SUMMARY_FIELDNAMES = [
    "sample_id",
    "left_query",
    "right_query",
    "left_hits",
    "right_hits",
    "pairs_within_gap",
    "overlap_pairs",
    "best_span_gap",
    "best_center_distance",
]

COMPARISON_FIELDNAMES = [
    "target_pair",
    "target_pairs_within_gap",
    "target_overlap_pairs",
    "synthetic_samples",
    "synthetic_pairs_mean",
    "synthetic_pairs_ge_target",
    "synthetic_pairs_p_ge",
    "synthetic_overlap_mean",
    "synthetic_overlap_ge_target",
    "synthetic_overlap_p_ge",
    "read",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    corpus = load_corpus(args.config)
    samples = synthetic_samples(
        corpus,
        samples=args.samples,
        left_length=args.left_length,
        right_length=args.right_length,
        seed=args.seed,
    )
    queries = sorted({query for sample in samples for query in sample})
    hits_by_query = pair_tool.collect_hits_by_query(
        corpus,
        queries,
        min_skip=args.min_skip,
        max_skip=args.max_skip,
        direction=args.direction,
        jobs=args.hit_jobs,
    )
    rows = [
        sample_row(index, left_query, right_query, corpus, hits_by_query, args)
        for index, (left_query, right_query) in enumerate(samples, start=1)
    ]
    comparisons = comparison_rows(rows, args.pair_baselines, args.corpus_label)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, rows)
    write_rows(args.comparison_out, COMPARISON_FIELDNAMES, comparisons)
    write_markdown(args.markdown_out, rows, comparisons)
    write_manifest(args, corpus, len(rows), started)
    print(args.summary_out)
    print(args.comparison_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=CONFIG)
    parser.add_argument("--corpus-label", default="MT_WLC")
    parser.add_argument("--pair-baselines", type=Path, default=PAIR_BASELINES)
    parser.add_argument("--samples", type=int, default=25)
    parser.add_argument("--left-length", type=int, default=3)
    parser.add_argument("--right-length", type=int, default=4)
    parser.add_argument("--seed", type=int, default=5150)
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=50)
    parser.add_argument(
        "--direction",
        choices=["forward", "backward", "both"],
        default="both",
    )
    parser.add_argument("--max-gap", type=int, default=500)
    parser.add_argument("--hit-jobs", type=int, default=1)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--comparison-out", type=Path, default=COMPARISON_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def synthetic_samples(
    corpus: Corpus,
    *,
    samples: int,
    left_length: int,
    right_length: int,
    seed: int,
) -> list[tuple[str, str]]:
    counts = Counter(corpus.text)
    alphabet = sorted(counts)
    weights = [counts[char] for char in alphabet]
    rng = random.Random(seed)
    output = []
    for _index in range(samples):
        output.append(
            (
                random_query(alphabet, weights, left_length, rng),
                random_query(alphabet, weights, right_length, rng),
            )
        )
    return output


def sample_row(
    index: int,
    left_query: str,
    right_query: str,
    corpus: Corpus,
    hits_by_query: dict[str, list[pair_tool.HitLite]],
    args: argparse.Namespace,
) -> dict[str, object]:
    metrics, _examples = pair_tool.score_pair(
        args.corpus_label,
        corpus,
        left_query,
        right_query,
        hits_by_query,
        max_gap=args.max_gap,
        require_same_chapter=True,
        require_same_skip=True,
        keep_examples=False,
    )
    return {
        "sample_id": f"synthetic_{index:03d}",
        "left_query": left_query,
        "right_query": right_query,
        "left_hits": metrics.left_hits,
        "right_hits": metrics.right_hits,
        "pairs_within_gap": metrics.pairs_within_gap,
        "overlap_pairs": metrics.overlap_pairs,
        "best_span_gap": pair_tool.empty_if_none(metrics.best_span_gap),
        "best_center_distance": round_float(metrics.best_center_distance),
    }


def comparison_rows(
    synthetic_rows: list[dict[str, object]],
    pair_baselines: Path,
    corpus_label: str,
) -> list[dict[str, object]]:
    target_rows = {
        row["pair_label"]: row
        for row in read_rows(pair_baselines)
        if row["corpus"] == corpus_label and row["pair_label"] in {"Gog/Magog", "Beast/Dragon"}
    }
    return [
        comparison_row(label, target_rows[label], synthetic_rows)
        for label in ["Gog/Magog", "Beast/Dragon"]
        if label in target_rows
    ]


def comparison_row(
    label: str,
    target: dict[str, str],
    synthetic_rows: list[dict[str, object]],
) -> dict[str, object]:
    pairs = tuple(int(row["pairs_within_gap"]) for row in synthetic_rows)
    overlaps = tuple(int(row["overlap_pairs"]) for row in synthetic_rows)
    target_pairs = int(target["observed_pairs_within_gap"])
    target_overlaps = int(target["observed_overlap_pairs"])
    pairs_ge = sum(1 for value in pairs if value >= target_pairs)
    overlaps_ge = sum(1 for value in overlaps if value >= target_overlaps)
    samples = len(synthetic_rows)
    return {
        "target_pair": label,
        "target_pairs_within_gap": target_pairs,
        "target_overlap_pairs": target_overlaps,
        "synthetic_samples": samples,
        "synthetic_pairs_mean": round_float(mean(pairs)),
        "synthetic_pairs_ge_target": pairs_ge,
        "synthetic_pairs_p_ge": round_float(tail_p_value_ge(target_pairs, pairs)),
        "synthetic_overlap_mean": round_float(mean(overlaps)),
        "synthetic_overlap_ge_target": overlaps_ge,
        "synthetic_overlap_p_ge": round_float(tail_p_value_ge(target_overlaps, overlaps)),
        "read": synthetic_read(pairs_ge, overlaps_ge),
    }


def synthetic_read(pairs_ge: int, overlaps_ge: int) -> str:
    if pairs_ge or overlaps_ge:
        return "synthetic samples can match or exceed target density"
    return "target exceeds sampled synthetic density"


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    comparisons: list[dict[str, object]],
) -> None:
    lines = [
        "# Synthetic Pair Baselines",
        "",
        "Length-matched synthetic Hebrew pair baselines for short 3+4 letter pairs.",
        "",
        "## Target Comparison",
        "",
        "| Target | Target close | Synthetic close mean | Synthetic >= target | p_ge | Read |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in comparisons:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["target_pair"]),
                    str(row["target_pairs_within_gap"]),
                    str(row["synthetic_pairs_mean"]),
                    str(row["synthetic_pairs_ge_target"]),
                    str(row["synthetic_pairs_p_ge"]),
                    str(row["read"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Synthetic Samples",
            "",
            "| Sample | Left | Right | Close pairs | Overlaps |",
            "| --- | --- | --- | ---: | ---: |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["sample_id"]),
                    f"`{row['left_query']}`",
                    f"`{row['right_query']}`",
                    str(row["pairs_within_gap"]),
                    str(row["overlap_pairs"]),
                ]
            )
            + " |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    corpus: Corpus,
    rows: int,
    started: float,
) -> None:
    payload = {
        "tool": "analyze_synthetic_pair_baselines",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "config": str(args.config),
        "corpus_label": args.corpus_label,
        "pair_baselines": str(args.pair_baselines),
        "samples": args.samples,
        "left_length": args.left_length,
        "right_length": args.right_length,
        "seed": args.seed,
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "direction": args.direction,
        "max_gap": args.max_gap,
        "hit_jobs": args.hit_jobs,
        "corpus": corpus.summary(),
        "rows": rows,
        "outputs": [
            str(args.summary_out),
            str(args.comparison_out),
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


def random_query(
    alphabet: list[str],
    weights: list[int],
    length: int,
    rng: random.Random,
) -> str:
    return "".join(rng.choices(alphabet, weights=weights, k=length))


def mean(values: tuple[int, ...]) -> float:
    return sum(values) / len(values) if values else 0.0


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
