#!/usr/bin/env python3
"""Evaluate tightened Greek surface rows against matched real-word controls."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.statistics import benjamini_hochberg_q_values, round_float, tail_p_value_ge
from els.term_display import display_term


COHORT_IN = Path("reports/greek_expanded_surface_triage/term_cohort.csv")
MATCHED_IN = Path("reports/greek_expanded_surface_control_pool/matched_controls.csv")
OUT_DIR = Path("reports/greek_expanded_surface_control_evaluation")
SUMMARY_OUT = OUT_DIR / "summary.csv"
DETAILS_OUT = OUT_DIR / "control_details.csv"
MD_OUT = Path("docs/GREEK_EXPANDED_SURFACE_CONTROL_EVALUATION.md")
MANIFEST_OUT = OUT_DIR / "manifest.json"

SUMMARY_FIELDNAMES = [
    "target_term_id",
    "target_concept",
    "target_normalized_term",
    "normalized_length",
    "observed_all_source_patterns",
    "observed_multi_source_patterns",
    "observed_unique_patterns",
    "observed_exact_center_hits",
    "matched_controls",
    "control_all_source_values",
    "controls_ge_observed_all_source",
    "all_source_p_ge",
    "all_source_q_value",
    "control_multi_source_values",
    "controls_ge_observed_multi_source",
    "multi_source_p_ge",
    "read",
]

DETAIL_FIELDNAMES = [
    "target_term_id",
    "target_normalized_term",
    "control_term_id",
    "control_normalized_term",
    "control_concept",
    "control_all_source_patterns",
    "control_multi_source_patterns",
    "control_unique_patterns",
    "control_exact_center_hits",
    "surface_vector_l1_delta",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    cohort = read_cohort_rows(args.cohort, args.control_cohort)
    matched = read_rows(args.matched_controls)
    summary_rows, detail_rows = evaluate_controls(cohort, matched)
    annotate_q_values(summary_rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_rows(args.details_out, DETAIL_FIELDNAMES, detail_rows)
    write_markdown(args.markdown_out, summary_rows, args.title)
    write_manifest(args, summary_rows, detail_rows, started)
    print(args.summary_out)
    print(args.details_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cohort", type=Path, default=COHORT_IN)
    parser.add_argument(
        "--control-cohort",
        action="append",
        default=[],
        help="additional cohort CSV containing matched control term rows",
    )
    parser.add_argument("--matched-controls", type=Path, default=MATCHED_IN)
    parser.add_argument("--title", default="Greek Expanded Surface Control Evaluation")
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--details-out", type=Path, default=DETAILS_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def evaluate_controls(
    cohort: dict[str, dict[str, str]],
    matched: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    controls_by_target: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in matched:
        controls_by_target[row["target_term_id"]].append(row)
    summary_rows = []
    detail_rows = []
    for target_id in sorted(controls_by_target):
        target = cohort[target_id]
        controls = controls_by_target[target_id]
        control_cohort_rows = [cohort[row["control_term_id"]] for row in controls]
        summary_rows.append(summary_row(target, control_cohort_rows))
        detail_rows.extend(detail_rows_for_target(target, controls, control_cohort_rows))
    return summary_rows, detail_rows


def summary_row(
    target: dict[str, str],
    controls: list[dict[str, str]],
) -> dict[str, str]:
    observed_all = int_value(target["all_source_patterns"])
    observed_multi = int_value(target["multi_source_patterns"])
    control_all = tuple(int_value(row["all_source_patterns"]) for row in controls)
    control_multi = tuple(int_value(row["multi_source_patterns"]) for row in controls)
    controls_ge_all = sum(value >= observed_all for value in control_all)
    controls_ge_multi = sum(value >= observed_multi for value in control_multi)
    all_source_p = tail_p_value_ge(observed_all, control_all)
    multi_source_p = tail_p_value_ge(observed_multi, control_multi)
    return {
        "target_term_id": target["term_id"],
        "target_concept": target["concept"],
        "target_normalized_term": target["normalized_term"],
        "normalized_length": target["normalized_length"],
        "observed_all_source_patterns": target["all_source_patterns"],
        "observed_multi_source_patterns": target["multi_source_patterns"],
        "observed_unique_patterns": target["unique_patterns"],
        "observed_exact_center_hits": target["total_exact_center_hits"],
        "matched_controls": str(len(controls)),
        "control_all_source_values": "/".join(str(value) for value in control_all),
        "controls_ge_observed_all_source": str(controls_ge_all),
        "all_source_p_ge": str(round_float(all_source_p)),
        "all_source_q_value": "",
        "control_multi_source_values": "/".join(str(value) for value in control_multi),
        "controls_ge_observed_multi_source": str(controls_ge_multi),
        "multi_source_p_ge": str(round_float(multi_source_p)),
        "read": read_label(all_source_p, controls_ge_all, len(controls)),
    }


def detail_rows_for_target(
    target: dict[str, str],
    matched_controls: list[dict[str, str]],
    control_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []
    for matched, control in zip(matched_controls, control_rows, strict=True):
        rows.append(
            {
                "target_term_id": target["term_id"],
                "target_normalized_term": target["normalized_term"],
                "control_term_id": control["term_id"],
                "control_normalized_term": control["normalized_term"],
                "control_concept": control["concept"],
                "control_all_source_patterns": control["all_source_patterns"],
                "control_multi_source_patterns": control["multi_source_patterns"],
                "control_unique_patterns": control["unique_patterns"],
                "control_exact_center_hits": control["total_exact_center_hits"],
                "surface_vector_l1_delta": matched["surface_vector_l1_delta"],
            }
        )
    return rows


def annotate_q_values(rows: list[dict[str, str]]) -> None:
    q_values = benjamini_hochberg_q_values(
        [float(row["all_source_p_ge"]) for row in rows]
    )
    for row, q_value in zip(rows, q_values, strict=True):
        row["all_source_q_value"] = str(round_float(q_value))


def read_label(p_value: float | None, controls_ge: int, control_count: int) -> str:
    if p_value is None:
        return "no matched controls"
    if p_value <= 0.05:
        return "exploratory matched controls below p<=0.05; still post-screen"
    if controls_ge == 0:
        return "target exceeds matched controls, but small control pool is not significant"
    return "matched controls overlap target"


def write_markdown(path: Path, rows: list[dict[str, str]], title: str) -> None:
    control_counts = [int(row["matched_controls"]) for row in rows]
    if control_counts:
        min_controls = min(control_counts)
        max_controls = max(control_counts)
        best_p_values = sorted({1 / (count + 1) for count in control_counts})
        best_p_text = ", ".join(f"{value:.6f}" for value in best_p_values)
        control_text = (
            f"Matched controls per target range from {min_controls} to {max_controls}. "
            f"The best possible add-one empirical p-values in this run are {best_p_text}."
        )
    else:
        control_text = "No selected target rows were available for control evaluation."
    lines = [
        f"# {title}",
        "",
        "Status: exploratory matched-control evaluation; no claim.",
        "",
        "This report compares the tightened surface-triage targets against their",
        "frozen same-length, real-word, surface-frequency-matched controls. The",
        "primary statistic is all-source exact-center surface pattern count.",
        "",
        control_text,
        "",
        "| Term | Concept | Observed all-source | Controls >= observed | p_ge | q | Read |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    display_control_term(row),
                    md_cell(row["target_concept"]),
                    row["observed_all_source_patterns"],
                    row["controls_ge_observed_all_source"],
                    row["all_source_p_ge"],
                    row["all_source_q_value"],
                    row["read"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            *control_read_lines(rows),
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def control_read_lines(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return [
            "No row reached the registered triage stage, so no control p/q values",
            "were computed. This is a negative result for the primary prospective",
            "control gate.",
        ]
    q_values = [float(row["all_source_q_value"]) for row in rows if row["all_source_q_value"]]
    controls_ge = [int(row["controls_ge_observed_all_source"]) for row in rows]
    if controls_ge and all(value > 0 for value in controls_ge):
        return [
            "Matched controls overlap every target's observed all-source pattern",
            "count. This weakens the length-4 follow-up and leaves no claim-grade",
            "row under study-level correction.",
        ]
    if q_values and min(q_values) > 0.05:
        return [
            "At least one target exceeds every matched control, but no row survives",
            "study-level q <= 0.05. This remains triage evidence rather than a",
            "claim-grade result.",
        ]
    return [
        "Rows where no matched control reaches the observed all-source pattern",
        "count are useful triage evidence, but this remains post-screen unless",
        "the control size and selection rule were frozen in advance.",
    ]


def display_control_term(row: dict[str, str]) -> str:
    return md_cell(
        display_term(
            row["target_normalized_term"],
            english=row.get("target_concept", ""),
        )
    )


def md_cell(value: str) -> str:
    return value.replace("|", "\\|")


def write_manifest(
    args: argparse.Namespace,
    summary_rows: list[dict[str, str]],
    detail_rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": "analyze_greek_surface_control_evaluation",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "seconds": round(time.perf_counter() - started, 3),
        "cohort": str(args.cohort),
        "control_cohorts": [str(path) for path in args.control_cohort],
        "matched_controls": str(args.matched_controls),
        "summary_rows": len(summary_rows),
        "detail_rows": len(detail_rows),
        "outputs": [
            str(args.summary_out),
            str(args.details_out),
            str(args.markdown_out),
            str(args.manifest_out),
        ],
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_cohort_rows(
    target_cohort: Path,
    control_cohorts: list[Path],
) -> dict[str, dict[str, str]]:
    rows = {row["term_id"]: row for row in read_rows(target_cohort)}
    for path in control_cohorts:
        for row in read_rows(path):
            rows.setdefault(row["term_id"], row)
    return rows


def int_value(value: str) -> int:
    return int(value or 0)


if __name__ == "__main__":
    raise SystemExit(main())
