#!/usr/bin/env python3
"""Run diagnostic WRR date-label permutations over a cross-pair c-value grid."""

from __future__ import annotations

import argparse
import csv
import json
import random
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.wrr import (
    bonferroni_rho0,
    p1_binomial_tail,
    p2_product_statistic,
    permutation_rank_rho,
)
from scripts.analyze_wrr_corrected_distance_aggregate import (
    c_cell,
    corrected_distance_values,
    p3_p4_sample_rows,
)


INPUT = Path("reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_corrected_distance_250.csv")
OUT = Path("reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_permutations_1000.csv")
SUMMARY_OUT = Path("reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_permutations_1000_summary.csv")
MD_OUT = Path("reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_permutations_1000.md")
MANIFEST_OUT = Path(
    "reports/wrr_1994/cross_pair_grid/wrr2_cross_pair_permutations_1000.manifest.json"
)

SAMPLE_FIELDNAMES = [
    "sample_type",
    "permutation_index",
    "seed",
    "date_concept_order",
    "identity_mapping",
    "rows",
    "defined_corrected_distances",
    "undefined_rows",
    "p3_p4_sample_rows",
    "p3_p4_sample_defined_corrected_distances",
    "p3_p4_sample_undefined_rows",
    "p1",
    "p2",
    "p3",
    "p4",
    "min_corrected_distance",
    "max_corrected_distance",
]

SUMMARY_FIELDNAMES = [
    "source",
    "permutations",
    "seed",
    "sample_rows_written",
    "concepts",
    "observed_rows",
    "observed_defined_corrected_distances",
    "observed_p1",
    "observed_p2",
    "observed_p3",
    "observed_p4",
    "rho_p1",
    "rho_p2",
    "rho_p3",
    "rho_p4",
    "rho0_bonferroni",
    "permutation_rows_min",
    "permutation_rows_max",
    "permutation_defined_min",
    "permutation_defined_max",
    "identity_permutations",
    "status",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    rows = filtered_rows(
        read_rows(args.input),
        candidate_lanes=args.candidate_lane,
        pair_review_statuses=args.pair_review_status,
        excluded_pair_review_statuses=args.exclude_pair_review_status,
    )
    summary = analyze_permutations_streaming(
        rows,
        source=str(args.input),
        permutations=args.permutations,
        seed=args.seed,
        p1_threshold=args.p1_threshold,
        sample_output_limit=args.sample_output_limit,
        out=args.out,
    )
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, summary, args)
    if args.manifest_out:
        write_manifest(args, summary, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    if args.manifest_out:
        print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--permutations", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=1994)
    parser.add_argument("--p1-threshold", type=float, default=0.2)
    parser.add_argument(
        "--candidate-lane",
        action="append",
        default=[],
        help="Optional candidate_lane filter. Repeat for multiple values.",
    )
    parser.add_argument(
        "--pair-review-status",
        action="append",
        default=[],
        help="Optional pair_review_status include filter. Repeat for multiple values.",
    )
    parser.add_argument(
        "--exclude-pair-review-status",
        action="append",
        default=[],
        help="Optional pair_review_status exclude filter. Repeat for multiple values.",
    )
    parser.add_argument(
        "--sample-output-limit",
        type=int,
        default=-1,
        help="Permutation sample rows to write; negative writes all, 0 writes observed only.",
    )
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def filtered_rows(
    rows: list[dict[str, str]],
    *,
    candidate_lanes: list[str],
    pair_review_statuses: list[str],
    excluded_pair_review_statuses: list[str],
) -> list[dict[str, str]]:
    lane_set = normalized_filter(candidate_lanes)
    status_set = normalized_filter(pair_review_statuses)
    excluded_status_set = normalized_filter(excluded_pair_review_statuses)
    return [
        row
        for row in rows
        if matches_filter(row.get("candidate_lane", "").strip(), lane_set)
        and matches_filter(row.get("pair_review_status", "").strip(), status_set)
        and row.get("pair_review_status", "").strip() not in excluded_status_set
    ]


def normalized_filter(values: list[str]) -> set[str]:
    normalized = {value.strip() for value in values if value.strip()}
    if "all" in normalized:
        return set()
    return normalized


def matches_filter(value: str, allowed: set[str]) -> bool:
    return not allowed or value in allowed


def analyze_permutations(
    rows: list[dict[str, str]],
    *,
    source: str,
    permutations: int,
    seed: int,
    p1_threshold: float,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    if permutations < 1:
        raise ValueError("permutations must be >= 1")
    concepts = source_concepts(rows)
    pair_index = build_pair_index(rows)
    rng = random.Random(seed)
    observed_order = tuple(concepts)
    samples = [
        statistic_row(
            rows_for_mapping(pair_index, dict(zip(concepts, observed_order, strict=True))),
            sample_type="observed",
            permutation_index=-1,
            seed=seed,
            concepts=concepts,
            date_order=observed_order,
            p1_threshold=p1_threshold,
        )
    ]
    for index in range(permutations):
        shuffled = list(concepts)
        rng.shuffle(shuffled)
        date_order = tuple(shuffled)
        samples.append(
            statistic_row(
                rows_for_mapping(pair_index, dict(zip(concepts, date_order, strict=True))),
                sample_type="permutation",
                permutation_index=index,
                seed=seed,
                concepts=concepts,
                date_order=date_order,
                p1_threshold=p1_threshold,
            )
        )
    summary = summarize_samples(
        samples,
        source=source,
        permutations=permutations,
        seed=seed,
        concepts=concepts,
    )
    return samples, summary


def analyze_permutations_streaming(
    rows: list[dict[str, str]],
    *,
    source: str,
    permutations: int,
    seed: int,
    p1_threshold: float,
    sample_output_limit: int,
    out: Path,
) -> dict[str, object]:
    if permutations < 1:
        raise ValueError("permutations must be >= 1")
    concepts = source_concepts(rows)
    pair_index = build_pair_index(rows)
    rng = random.Random(seed)
    observed_order = tuple(concepts)
    observed = statistic_row(
        rows_for_mapping(pair_index, dict(zip(concepts, observed_order, strict=True))),
        sample_type="observed",
        permutation_index=-1,
        seed=seed,
        concepts=concepts,
        date_order=observed_order,
        p1_threshold=p1_threshold,
    )
    state = initialize_summary_state(observed)
    samples_written = 0
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SAMPLE_FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerow(observed)
        samples_written += 1
        for index in range(permutations):
            shuffled = list(concepts)
            rng.shuffle(shuffled)
            date_order = tuple(shuffled)
            sample = statistic_row(
                rows_for_mapping(pair_index, dict(zip(concepts, date_order, strict=True))),
                sample_type="permutation",
                permutation_index=index,
                seed=seed,
                concepts=concepts,
                date_order=date_order,
                p1_threshold=p1_threshold,
            )
            update_summary_state(state, sample)
            if should_write_permutation_sample(index, sample_output_limit):
                writer.writerow(sample)
                samples_written += 1
    return finalize_summary_state(
        state,
        source=source,
        permutations=permutations,
        seed=seed,
        concepts=concepts,
        samples_written=samples_written,
    )


def source_concepts(rows: list[dict[str, str]]) -> list[str]:
    concepts = {
        app_concept
        for row in rows
        for app_concept, date_concept in [row_concepts(row)]
        if app_concept == date_concept
    }
    if not concepts:
        raise ValueError("input has no same-concept source rows")
    return sorted(concepts, key=concept_sort_key)


def build_pair_index(
    rows: list[dict[str, str]],
) -> dict[tuple[str, str], list[dict[str, str]]]:
    pair_index: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        pair_index.setdefault(row_concepts(row), []).append(row)
    return pair_index


def row_concepts(row: dict[str, str]) -> tuple[str, str]:
    concept = row.get("concept", "").strip()
    if "->" in concept:
        left, right = concept.split("->", 1)
        return left.strip(), right.strip()
    if concept:
        return concept, concept
    return term_concept(row["appellation_term_id"]), term_concept(row["date_term_id"])


def term_concept(term_id: str) -> str:
    parts = term_id.split("_")
    if len(parts) < 2:
        raise ValueError(f"cannot infer WRR concept from term id: {term_id}")
    return f"{parts[0].upper()} {int(parts[1]):02d}"


def concept_sort_key(concept: str) -> tuple[str, int, str]:
    head, _, tail = concept.partition(" ")
    try:
        number = int(tail)
    except ValueError:
        number = 0
    return head, number, concept


def rows_for_mapping(
    pair_index: dict[tuple[str, str], list[dict[str, str]]],
    mapping: dict[str, str],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for app_concept in sorted(mapping, key=concept_sort_key):
        rows.extend(pair_index.get((app_concept, mapping[app_concept]), []))
    return rows


def statistic_row(
    rows: list[dict[str, str]],
    *,
    sample_type: str,
    permutation_index: int,
    seed: int,
    concepts: list[str],
    date_order: tuple[str, ...],
    p1_threshold: float,
) -> dict[str, object]:
    values = corrected_distance_values(rows)
    p3_rows = p3_p4_sample_rows(rows)
    p3_values = corrected_distance_values(p3_rows)
    p1 = p1_binomial_tail(values, threshold=p1_threshold) if values else ""
    p2 = p2_product_statistic(values) if values else ""
    p3 = p1_binomial_tail(p3_values, threshold=p1_threshold) if p3_values else ""
    p4 = p2_product_statistic(p3_values) if p3_values else ""
    min_c: object = min(values) if values else ""
    max_c: object = max(values) if values else ""
    return {
        "sample_type": sample_type,
        "permutation_index": permutation_index,
        "seed": seed,
        "date_concept_order": "|".join(date_order),
        "identity_mapping": str(tuple(concepts) == date_order).lower(),
        "rows": len(rows),
        "defined_corrected_distances": len(values),
        "undefined_rows": len(rows) - len(values),
        "p3_p4_sample_rows": len(p3_rows),
        "p3_p4_sample_defined_corrected_distances": len(p3_values),
        "p3_p4_sample_undefined_rows": len(p3_rows) - len(p3_values),
        "p1": "" if p1 == "" else c_cell(float(p1)),
        "p2": "" if p2 == "" else c_cell(float(p2)),
        "p3": "" if p3 == "" else c_cell(float(p3)),
        "p4": "" if p4 == "" else c_cell(float(p4)),
        "min_corrected_distance": "" if min_c == "" else c_cell(float(min_c)),
        "max_corrected_distance": "" if max_c == "" else c_cell(float(max_c)),
    }


def summarize_samples(
    samples: list[dict[str, object]],
    *,
    source: str,
    permutations: int,
    seed: int,
    concepts: list[str],
) -> dict[str, object]:
    observed = next(row for row in samples if row["sample_type"] == "observed")
    permuted = [row for row in samples if row["sample_type"] == "permutation"]
    rhos = {
        metric: metric_rho(observed, permuted, metric)
        for metric in ("p1", "p2", "p3", "p4")
    }
    rho_values = [value for value in rhos.values() if value != ""]
    return {
        "source": source,
        "permutations": permutations,
        "seed": seed,
        "sample_rows_written": len(samples),
        "concepts": len(concepts),
        "observed_rows": observed["rows"],
        "observed_defined_corrected_distances": observed["defined_corrected_distances"],
        "observed_p1": observed["p1"],
        "observed_p2": observed["p2"],
        "observed_p3": observed["p3"],
        "observed_p4": observed["p4"],
        "rho_p1": "" if rhos["p1"] == "" else c_cell(float(rhos["p1"])),
        "rho_p2": "" if rhos["p2"] == "" else c_cell(float(rhos["p2"])),
        "rho_p3": "" if rhos["p3"] == "" else c_cell(float(rhos["p3"])),
        "rho_p4": "" if rhos["p4"] == "" else c_cell(float(rhos["p4"])),
        "rho0_bonferroni": "" if not rho_values else c_cell(bonferroni_rho0(rho_values)),
        "permutation_rows_min": min(int(row["rows"]) for row in permuted),
        "permutation_rows_max": max(int(row["rows"]) for row in permuted),
        "permutation_defined_min": min(
            int(row["defined_corrected_distances"]) for row in permuted
        ),
        "permutation_defined_max": max(
            int(row["defined_corrected_distances"]) for row in permuted
        ),
        "identity_permutations": sum(
            1 for row in permuted if row["identity_mapping"] == "true"
        ),
        "status": "diagnostic_only_not_wrr_reproduction",
    }


def initialize_summary_state(observed: dict[str, object]) -> dict[str, object]:
    return {
        "observed": observed,
        "metric_counts": {
            metric: {"less": 0, "equal": 0, "count": 0}
            for metric in ("p1", "p2", "p3", "p4")
        },
        "rows_min": None,
        "rows_max": None,
        "defined_min": None,
        "defined_max": None,
        "identity_permutations": 0,
    }


def update_summary_state(state: dict[str, object], sample: dict[str, object]) -> None:
    metric_counts = state["metric_counts"]
    for metric, counts in metric_counts.items():
        update_metric_counts(counts, state["observed"], sample, metric)
    row_count = int(sample["rows"])
    defined_count = int(sample["defined_corrected_distances"])
    state["rows_min"] = min_optional(state["rows_min"], row_count)
    state["rows_max"] = max_optional(state["rows_max"], row_count)
    state["defined_min"] = min_optional(state["defined_min"], defined_count)
    state["defined_max"] = max_optional(state["defined_max"], defined_count)
    if sample["identity_mapping"] == "true":
        state["identity_permutations"] = int(state["identity_permutations"]) + 1


def update_metric_counts(
    counts: dict[str, int],
    observed: dict[str, object],
    sample: dict[str, object],
    metric: str,
) -> None:
    observed_value = numeric_cell(observed.get(metric, ""))
    sample_value = numeric_cell(sample.get(metric, ""))
    if observed_value is None or sample_value is None:
        return
    if sample_value < observed_value:
        counts["less"] += 1
    elif sample_value == observed_value:
        counts["equal"] += 1
    counts["count"] += 1


def finalize_summary_state(
    state: dict[str, object],
    *,
    source: str,
    permutations: int,
    seed: int,
    concepts: list[str],
    samples_written: int,
) -> dict[str, object]:
    observed = state["observed"]
    metric_counts = state["metric_counts"]
    rhos = {
        metric: rho_from_counts(counts)
        for metric, counts in metric_counts.items()
        if counts["count"] > 0
    }
    return {
        "source": source,
        "permutations": permutations,
        "seed": seed,
        "sample_rows_written": samples_written,
        "concepts": len(concepts),
        "observed_rows": observed["rows"],
        "observed_defined_corrected_distances": observed["defined_corrected_distances"],
        "observed_p1": observed["p1"],
        "observed_p2": observed["p2"],
        "observed_p3": observed["p3"],
        "observed_p4": observed["p4"],
        "rho_p1": c_cell(rhos["p1"]) if "p1" in rhos else "",
        "rho_p2": c_cell(rhos["p2"]) if "p2" in rhos else "",
        "rho_p3": c_cell(rhos["p3"]) if "p3" in rhos else "",
        "rho_p4": c_cell(rhos["p4"]) if "p4" in rhos else "",
        "rho0_bonferroni": "" if not rhos else c_cell(bonferroni_rho0(rhos.values())),
        "permutation_rows_min": state["rows_min"] if state["rows_min"] is not None else "",
        "permutation_rows_max": state["rows_max"] if state["rows_max"] is not None else "",
        "permutation_defined_min": (
            state["defined_min"] if state["defined_min"] is not None else ""
        ),
        "permutation_defined_max": (
            state["defined_max"] if state["defined_max"] is not None else ""
        ),
        "identity_permutations": state["identity_permutations"],
        "status": "diagnostic_only_not_wrr_reproduction",
    }


def rho_from_counts(counts: dict[str, int]) -> float:
    return (1.0 + counts["less"] + 0.5 * counts["equal"]) / (counts["count"] + 1)


def min_optional(current: object, value: int) -> int:
    return value if current is None else min(int(current), value)


def max_optional(current: object, value: int) -> int:
    return value if current is None else max(int(current), value)


def should_write_permutation_sample(index: int, limit: int) -> bool:
    return limit < 0 or index < limit


def metric_rho(
    observed: dict[str, object],
    permuted: list[dict[str, object]],
    metric: str,
) -> float | str:
    observed_value = numeric_cell(observed.get(metric, ""))
    values = [
        value
        for row in permuted
        if (value := numeric_cell(row.get(metric, ""))) is not None
    ]
    if observed_value is None or not values:
        return ""
    return permutation_rank_rho(observed_value, values)


def numeric_cell(value: object) -> float | None:
    if value in ("", None):
        return None
    return float(str(value))


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    path: Path,
    summary: dict[str, object],
    args: argparse.Namespace,
) -> None:
    lines = [
        "# WRR Cross-Pair Date Permutation Diagnostic",
        "",
        "Status: diagnostic-only, not a WRR reproduction.",
        "",
        "This shuffles date-concept labels over the generated cross-pair corrected-distance",
        "matrix. It ranks the observed same-record diagnostic aggregate against sampled",
        "date-label permutations. The pair universe, D(w) rule, and final permutation",
        "procedure are not claim-locked.",
        "",
        "## Reproduce",
        "",
        "```bash",
        (
            "python3 -m scripts.analyze_wrr_cross_pair_permutations "
            f"--input {args.input} "
            f"--permutations {args.permutations} "
            f"--seed {args.seed} "
            f"--p1-threshold {args.p1_threshold} "
            f"--sample-output-limit {args.sample_output_limit} "
            f"--out {args.out} "
            f"--summary-out {args.summary_out} "
            f"--markdown-out {args.markdown_out} "
            f"--manifest-out {args.manifest_out}"
        ),
        "```",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
    ]
    for field in SUMMARY_FIELDNAMES:
        lines.append(f"| `{field}` | {summary[field]} |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    summary: dict[str, object],
    started: float,
) -> None:
    payload = {
        "tool": Path(__file__).name,
        "edls_version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "input": str(args.input),
        "parameters": {
            "permutations": args.permutations,
            "seed": args.seed,
            "p1_threshold": args.p1_threshold,
            "candidate_lane": args.candidate_lane,
            "pair_review_status": args.pair_review_status,
            "exclude_pair_review_status": args.exclude_pair_review_status,
            "sample_output_limit": args.sample_output_limit,
        },
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


if __name__ == "__main__":
    raise SystemExit(main())
