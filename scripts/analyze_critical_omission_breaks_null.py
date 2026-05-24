#!/usr/bin/env python3
"""Null test: are SBLGNT-omitted block breaks more than chance?"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, datetime
from pathlib import Path

from els.corpus import load_corpus
from els.critical import (
    classify_missing_verses,
    count_breaks_for_blocks,
    shuffled_block_placement,
)
from els.search import iter_els_query_matches_by_lanes
from els.statistics import benjamini_hochberg_q_values, tail_p_value_ge, tail_p_value_le
from scripts.analyze_critical_omission_breaks import (
    CRITICAL_CONFIG,
    MAX_SKIP,
    MIN_SKIP,
    MIN_TERM_LENGTH,
    TERM_PATHS,
    TR_CONFIG,
    build_stats_by_query,
    read_greek_terms,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shuffles", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--out-dir", type=Path, default=Path("reports/critical_omission_breaks_null"))
    parser.add_argument("--max-terms", type=int, help="Test helper: limit term rows before building queries.")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    tr = load_corpus(TR_CONFIG)
    critical = load_corpus(CRITICAL_CONFIG)
    actual = [block for block in classify_missing_verses(tr, critical) if block.used_as_deletion]
    terms = read_greek_terms(TERM_PATHS, tr)
    if args.max_terms:
        terms = terms[: args.max_terms]

    observed_stats, observed_queries = build_stats_by_query(tr, [dict(row) for row in terms])
    matches = list(
        iter_els_query_matches_by_lanes(
            tr.text,
            observed_queries,
            min_skip=MIN_SKIP,
            max_skip=MAX_SKIP,
            direction="both",
        )
    )
    observed_total, observed_per_block, _broken = count_breaks_for_blocks(
        tr,
        observed_queries,
        actual,
        min_skip=MIN_SKIP,
        max_skip=MAX_SKIP,
        direction="both",
        matches=matches,
    )

    null_totals: list[int] = []
    null_per_block: list[list[int]] = []
    for i in range(args.shuffles):
        placements = shuffled_block_placement(tr, actual, seed=args.seed + i)
        total, per_block, _ = count_breaks_for_blocks(
            tr,
            observed_queries,
            placements,
            min_skip=MIN_SKIP,
            max_skip=MAX_SKIP,
            direction="both",
            matches=matches,
            update_stats=False,
            collect_broken_hits=False,
        )
        null_totals.append(total)
        null_per_block.append(per_block)
        if i % 50 == 0:
            print(f"shuffle {i}/{args.shuffles}: total={total}", flush=True)

    p_total_ge = tail_p_value_ge(observed_total, null_totals)
    p_total_le = tail_p_value_le(observed_total, null_totals)
    block_p_values = [
        tail_p_value_ge(observed_per_block[i], [sample[i] for sample in null_per_block])
        for i in range(len(actual))
    ]
    block_q_values = benjamini_hochberg_q_values(block_p_values)

    write_distribution_csv(args.out_dir / "null_distribution.csv", null_totals)
    write_per_block_csv(
        args.out_dir / "null_per_block.csv",
        actual,
        observed_per_block,
        null_per_block,
        block_p_values,
        block_q_values,
    )
    write_summary_csv(
        args.out_dir / "summary.csv",
        observed_total,
        null_totals,
        p_total_ge,
        p_total_le,
        len(terms),
        len(observed_stats),
    )
    write_manifest(
        args.out_dir / "manifest.json",
        tr,
        critical,
        actual,
        args,
        observed_total,
        p_total_ge,
    )
    median = sorted(null_totals)[len(null_totals) // 2] if null_totals else ""
    p_display = f"{p_total_ge:.4f}" if p_total_ge is not None else "NA"
    print(f"observed={observed_total}  p_ge={p_display}  null_median={median}")
    return 0


def write_distribution_csv(path: Path, null_totals: list[int]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["shuffle_index", "broken_total_hits"])
        writer.writeheader()
        for index, total in enumerate(null_totals):
            writer.writerow({"shuffle_index": index, "broken_total_hits": total})


def write_per_block_csv(
    path: Path,
    actual,
    observed_per_block: list[int],
    null_per_block: list[list[int]],
    p_values: list[float | None],
    q_values: list[float | None],
) -> None:
    fieldnames = [
        "block_index",
        "ref",
        "observed_breaks",
        "null_min",
        "null_median",
        "null_max",
        "p_ge",
        "bh_q",
        "deleted_letters",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index, block in enumerate(actual):
            samples = sorted(sample[index] for sample in null_per_block)
            writer.writerow(
                {
                    "block_index": index,
                    "ref": block.ref,
                    "observed_breaks": observed_per_block[index],
                    "null_min": samples[0] if samples else "",
                    "null_median": samples[len(samples) // 2] if samples else "",
                    "null_max": samples[-1] if samples else "",
                    "p_ge": p_values[index] if p_values[index] is not None else "",
                    "bh_q": q_values[index] if q_values[index] is not None else "",
                    "deleted_letters": block.length,
                }
            )


def write_summary_csv(
    path: Path,
    observed_total: int,
    null_totals: list[int],
    p_ge: float | None,
    p_le: float | None,
    term_rows: int,
    stat_rows: int,
) -> None:
    samples = sorted(null_totals)
    row = {
        "observed_total": observed_total,
        "null_min": samples[0] if samples else "",
        "null_median": samples[len(samples) // 2] if samples else "",
        "null_max": samples[-1] if samples else "",
        "p_ge": p_ge if p_ge is not None else "",
        "p_le": p_le if p_le is not None else "",
        "shuffles": len(null_totals),
        "term_rows": term_rows,
        "stat_rows": stat_rows,
    }
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)


def write_manifest(path: Path, tr, critical, actual, args, observed_total: int, p_ge: float | None) -> None:
    path.write_text(
        json.dumps(
            {
                "tool": "critical_omission_breaks_null",
                "created_utc": datetime.now(UTC).isoformat(),
                "tr_config": str(TR_CONFIG.resolve()),
                "critical_config": str(CRITICAL_CONFIG.resolve()),
                "tr_corpus": tr.summary(),
                "critical_corpus": critical.summary(),
                "term_paths": [str(path.resolve()) for path in TERM_PATHS],
                "min_skip": MIN_SKIP,
                "max_skip": MAX_SKIP,
                "min_term_length": MIN_TERM_LENGTH,
                "shuffles": args.shuffles,
                "seed": args.seed,
                "actual_blocks": len(actual),
                "observed_total": observed_total,
                "p_ge": p_ge,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
