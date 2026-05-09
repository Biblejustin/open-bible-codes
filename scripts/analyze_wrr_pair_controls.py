#!/usr/bin/env python3
"""Control-screen top WRR same-record pair audit rows."""

from __future__ import annotations

import argparse
import csv
import json
import random
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.corpus import load_corpus
from els.statistics import benjamini_hochberg_q_values, numeric_value, round_float
from scripts import analyze_gog_magog_pairs as pair_tool


PAIR_SUMMARY = Path("reports/wrr_1994/wrr2_genesis_pair_audit_summary.csv")
CONFIG = Path("configs/example_koren_genesis.toml")
OUT = Path("reports/wrr_1994/wrr2_genesis_pair_controls.csv")
MD_OUT = Path("reports/wrr_1994/wrr2_genesis_pair_controls.md")
MANIFEST_OUT = Path("reports/wrr_1994/wrr2_genesis_pair_controls.manifest.json")

FIELDNAMES = [
    "rank",
    "corpus",
    "concept",
    "appellation_term_id",
    "appellation_normalized",
    "appellation_length",
    "date_term_id",
    "date_normalized",
    "date_length",
    "observed_close_pairs",
    "observed_overlap_pairs",
    "observed_strict_pairs",
    "observed_best_span_gap",
    "term_control_samples",
    "term_close_mean",
    "term_close_p_ge",
    "term_overlap_mean",
    "term_overlap_p_ge",
    "term_strict_mean",
    "term_strict_p_ge",
    "term_best_gap_mean",
    "term_best_gap_p_le",
    "random_control_samples",
    "random_close_mean",
    "random_close_p_ge",
    "random_overlap_mean",
    "random_overlap_p_ge",
    "random_strict_mean",
    "random_strict_p_ge",
    "random_best_gap_mean",
    "random_best_gap_p_le",
    "combined_min_p",
    "combined_min_q",
    "band",
    "read",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    corpus = load_corpus(args.config)
    selected = select_top_pairs(read_rows(args.pair_summary), args.top)
    prepared = prepare_pairs(selected, corpus.text, args)
    queries = sorted(queries_for_prepared_pairs(prepared))
    hits_by_query = pair_tool.collect_hits_by_query(
        corpus,
        queries,
        min_skip=args.min_skip,
        max_skip=args.max_skip,
        direction=args.direction,
        jobs=args.jobs,
    )
    rows = []
    for rank, item in enumerate(prepared, start=1):
        rows.append(control_row(rank, item, corpus, hits_by_query, args))
    annotate_q_values(rows)
    write_rows(args.out, FIELDNAMES, rows)
    write_markdown(args.markdown_out, rows, args)
    if args.manifest_out:
        write_manifest(args, corpus, selected, queries, rows, started)
    print(args.out)
    print(args.markdown_out)
    if args.manifest_out:
        print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair-summary", type=Path, default=PAIR_SUMMARY)
    parser.add_argument("--config", type=Path, default=CONFIG)
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--min-skip", type=int, default=2)
    parser.add_argument("--max-skip", type=int, default=250)
    parser.add_argument(
        "--direction",
        choices=["forward", "backward", "both"],
        default="both",
    )
    parser.add_argument("--max-gap", type=int, default=500)
    parser.add_argument("--term-control-samples", type=int, default=100)
    parser.add_argument("--random-control-samples", type=int, default=20)
    parser.add_argument("--seed", type=int, default=1994)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def select_top_pairs(rows: list[dict[str, str]], limit: int) -> list[dict[str, str]]:
    candidates = [row for row in rows if int_or_zero(row.get("all_pairs_within_gap")) > 0]
    return sorted(candidates, key=pair_rank_key)[:limit]


def pair_rank_key(row: dict[str, str]) -> tuple[int, int, int, int]:
    return (
        -int_or_zero(row.get("strict_pairs_within_gap")),
        -int_or_zero(row.get("all_pairs_within_gap")),
        int_or_large(row.get("best_span_gap")),
        int_or_large(row.get("best_center_distance")),
    )


def prepare_pairs(
    rows: list[dict[str, str]],
    corpus_text: str,
    args: argparse.Namespace,
) -> list[dict[str, object]]:
    prepared = []
    for row in rows:
        app_query = row["appellation_normalized"]
        date_query = row["date_normalized"]
        term_samples = pair_tool.paired_term_samples(
            app_query,
            date_query,
            samples=args.term_control_samples,
            rng=random.Random(stable_seed(args.seed, row["appellation_term_id"], row["date_term_id"], "term")),
        )
        random_samples = pair_tool.paired_random_samples(
            left_length=len(app_query),
            right_length=len(date_query),
            corpus_text=corpus_text,
            samples=args.random_control_samples,
            rng=random.Random(
                stable_seed(args.seed, row["appellation_term_id"], row["date_term_id"], "random")
            ),
        )
        prepared.append(
            {
                "row": row,
                "app_query": app_query,
                "date_query": date_query,
                "term_samples": term_samples,
                "random_samples": random_samples,
            }
        )
    return prepared


def queries_for_prepared_pairs(prepared: list[dict[str, object]]) -> set[str]:
    queries = set()
    for item in prepared:
        queries.add(str(item["app_query"]))
        queries.add(str(item["date_query"]))
        for sample in item["term_samples"]:
            queries.add(sample.left_query)
            queries.add(sample.right_query)
        for sample in item["random_samples"]:
            queries.add(sample.left_query)
            queries.add(sample.right_query)
    return queries


def control_row(
    rank: int,
    item: dict[str, object],
    corpus,
    hits_by_query: dict[str, list[pair_tool.HitLite]],
    args: argparse.Namespace,
) -> dict[str, object]:
    row = item["row"]
    app_query = str(item["app_query"])
    date_query = str(item["date_query"])
    term_samples = item["term_samples"]
    random_samples = item["random_samples"]

    observed, _examples = pair_tool.score_pair(
        str(row["corpus"]),
        corpus,
        app_query,
        date_query,
        hits_by_query,
        max_gap=args.max_gap,
        keep_examples=False,
        chapter_cache={},
    )
    observed_strict = pair_tool.score_pair(
        str(row["corpus"]),
        corpus,
        app_query,
        date_query,
        hits_by_query,
        max_gap=args.max_gap,
        require_same_chapter=True,
        require_same_skip=True,
        keep_examples=False,
        chapter_cache={},
    )[0]
    term_metrics = pair_tool.score_control_samples(
        str(row["corpus"]),
        corpus,
        term_samples,
        hits_by_query,
        max_gap=args.max_gap,
        chapter_cache={},
    )
    term_strict_metrics = pair_tool.score_control_samples(
        str(row["corpus"]),
        corpus,
        term_samples,
        hits_by_query,
        max_gap=args.max_gap,
        require_same_chapter=True,
        require_same_skip=True,
        chapter_cache={},
    )
    random_metrics = pair_tool.score_control_samples(
        str(row["corpus"]),
        corpus,
        random_samples,
        hits_by_query,
        max_gap=args.max_gap,
        chapter_cache={},
    )
    random_strict_metrics = pair_tool.score_control_samples(
        str(row["corpus"]),
        corpus,
        random_samples,
        hits_by_query,
        max_gap=args.max_gap,
        require_same_chapter=True,
        require_same_skip=True,
        chapter_cache={},
    )
    output = {
        "rank": rank,
        "corpus": row["corpus"],
        "concept": row["concept"],
        "appellation_term_id": row["appellation_term_id"],
        "appellation_normalized": app_query,
        "appellation_length": len(app_query),
        "date_term_id": row["date_term_id"],
        "date_normalized": date_query,
        "date_length": len(date_query),
        "observed_close_pairs": observed.pairs_within_gap,
        "observed_overlap_pairs": observed.overlap_pairs,
        "observed_strict_pairs": observed_strict.pairs_within_gap,
        "observed_best_span_gap": empty_if_none(observed.best_span_gap),
    }
    output.update(control_fields("term", observed, observed_strict, term_metrics, term_strict_metrics))
    output.update(
        control_fields("random", observed, observed_strict, random_metrics, random_strict_metrics)
    )
    p_values = [
        numeric_value(output.get("term_close_p_ge")),
        numeric_value(output.get("term_overlap_p_ge")),
        numeric_value(output.get("term_strict_p_ge")),
        numeric_value(output.get("term_best_gap_p_le")),
        numeric_value(output.get("random_close_p_ge")),
        numeric_value(output.get("random_overlap_p_ge")),
        numeric_value(output.get("random_strict_p_ge")),
        numeric_value(output.get("random_best_gap_p_le")),
    ]
    p_values = [value for value in p_values if value is not None]
    output["combined_min_p"] = round_float(min(p_values)) if p_values else ""
    output["combined_min_q"] = ""
    output["band"] = ""
    output["read"] = ""
    return output


def control_fields(
    prefix: str,
    observed: pair_tool.PairMetrics,
    observed_strict: pair_tool.PairMetrics,
    metrics: tuple[pair_tool.PairMetrics, ...],
    strict_metrics: tuple[pair_tool.PairMetrics, ...],
) -> dict[str, object]:
    close = tuple(metric.pairs_within_gap for metric in metrics)
    overlaps = tuple(metric.overlap_pairs for metric in metrics)
    strict = tuple(metric.pairs_within_gap for metric in strict_metrics)
    gaps = tuple(metric.best_span_gap for metric in metrics if metric.best_span_gap is not None)
    return {
        f"{prefix}_control_samples": len(metrics),
        f"{prefix}_close_mean": round_float(mean_or_none(close)),
        f"{prefix}_close_p_ge": round_float(pair_tool.p_value_ge(observed.pairs_within_gap, close)),
        f"{prefix}_overlap_mean": round_float(mean_or_none(overlaps)),
        f"{prefix}_overlap_p_ge": round_float(pair_tool.p_value_ge(observed.overlap_pairs, overlaps)),
        f"{prefix}_strict_mean": round_float(mean_or_none(strict)),
        f"{prefix}_strict_p_ge": round_float(
            pair_tool.p_value_ge(observed_strict.pairs_within_gap, strict)
        ),
        f"{prefix}_best_gap_mean": round_float(mean_or_none(gaps)),
        f"{prefix}_best_gap_p_le": round_float(pair_tool.p_value_le(observed.best_span_gap, gaps)),
    }


def annotate_q_values(rows: list[dict[str, object]]) -> None:
    q_values = benjamini_hochberg_q_values(
        [numeric_value(row.get("combined_min_p")) for row in rows]
    )
    for row, q_value in zip(rows, q_values, strict=True):
        row["combined_min_q"] = round_float(q_value)
        row["band"] = band(row)
        row["read"] = read_label(row)


def band(row: dict[str, object]) -> str:
    q_value = numeric_value(row.get("combined_min_q"))
    p_value = numeric_value(row.get("combined_min_p"))
    if q_value is not None:
        if q_value <= 0.01:
            return "q_le_0.01"
        if q_value <= 0.05:
            return "q_le_0.05"
        if q_value <= 0.10:
            return "q_le_0.10"
    if p_value is not None and p_value <= 0.05:
        return "uncorrected_p_le_0.05"
    return "not_unusual"


def read_label(row: dict[str, object]) -> str:
    if row["band"] == "not_unusual":
        return "not unusual under top-pair controls"
    if row["band"] == "uncorrected_p_le_0.05":
        return "uncorrected only; audit"
    return "adjusted control signal; inspect manually"


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, object]], args: argparse.Namespace) -> None:
    band_counts: dict[str, int] = {}
    for row in rows:
        band_counts[str(row["band"])] = band_counts.get(str(row["band"]), 0) + 1
    lines = [
        "# WRR2 Genesis Pair Controls",
        "",
        "This report applies shuffled-letter and random-letter pair controls to the top raw WRR2 pair-audit rows. It is not the WRR aggregate statistic.",
        "",
        "## Scope",
        "",
        f"- Top pair rows: `{args.top}`",
        f"- Skip range: `{args.min_skip}..{args.max_skip}`",
        f"- Direction: `{args.direction}`",
        f"- Max gap: `{args.max_gap}`",
        f"- Term controls per row: `{args.term_control_samples}`",
        f"- Random controls per row: `{args.random_control_samples}`",
        "",
        "## Bands",
        "",
        "| Band | Rows |",
        "| --- | ---: |",
    ]
    for label, count in sorted(band_counts.items()):
        lines.append(f"| `{label}` | {count} |")
    lines.extend(
        [
            "",
            "## Rows",
            "",
            "| Rank | Concept | Appellation | Date | Close | Strict | Min p | Min q | Band | Read |",
            "| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["rank"]),
                    str(row["concept"]),
                    f"`{row['appellation_term_id']}` `{row['appellation_normalized']}`",
                    f"`{row['date_term_id']}` `{row['date_normalized']}`",
                    str(row["observed_close_pairs"]),
                    str(row["observed_strict_pairs"]),
                    str(row["combined_min_p"]),
                    str(row["combined_min_q"]),
                    f"`{row['band']}`",
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
            "This control screen is a post-audit diagnostic over selected rows. It reduces raw-count over-reading but does not substitute for WRR's declared aggregate statistic and permutation test.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    corpus,
    selected: list[dict[str, str]],
    queries: list[str],
    rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "pair_summary": str(args.pair_summary),
        "config": str(args.config),
        "corpus": corpus.summary(),
        "top": args.top,
        "min_skip": args.min_skip,
        "max_skip": args.max_skip,
        "direction": args.direction,
        "max_gap": args.max_gap,
        "term_control_samples": args.term_control_samples,
        "random_control_samples": args.random_control_samples,
        "seed": args.seed,
        "selected_rows": len(selected),
        "queries": len(queries),
        "rows": len(rows),
        "outputs": {
            "csv": str(args.out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def mean_or_none(values: tuple[int, ...]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def int_or_zero(value: object) -> int:
    if value in ("", None):
        return 0
    return int(float(str(value)))


def int_or_large(value: object) -> int:
    if value in ("", None):
        return 10**12
    return int_or_zero(value)


def empty_if_none(value: int | None) -> int | str:
    return "" if value is None else value


def stable_seed(*parts: object) -> int:
    value = 0
    for part in parts:
        for char in str(part):
            value = (value * 131 + ord(char)) % 2_147_483_647
    return value


if __name__ == "__main__":
    raise SystemExit(main())
