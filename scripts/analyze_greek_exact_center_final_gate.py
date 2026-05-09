#!/usr/bin/env python3
"""Consolidate Greek exact-center pattern version, control, context, and synthetic checks."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.statistics import numeric_value


PATTERN_SUMMARY = Path("reports/greek_pattern_versions/summary.csv")
CONTEXT_FILES = [
    Path("reports/greek_exact_center_four_source/context_review_summary.csv"),
    Path("reports/greek_exact_center_three_source/context_review_summary.csv"),
    Path("reports/sblgnt_source_only_exact_center/context_review_summary.csv"),
    Path("reports/byz_source_only_exact_center/context_review_summary.csv"),
]
SYNTHETIC_SUMMARY = Path(
    "reports/greek_exact_center_three_source/synthetic_extension_baselines_summary.csv"
)
OUT_DIR = Path("reports/greek_exact_center_final_gate")
SUMMARY_OUT = OUT_DIR / "summary.csv"
MD_OUT = OUT_DIR / "greek_exact_center_final_gate.md"
MANIFEST_OUT = OUT_DIR / "manifest.json"

FIELDNAMES = [
    "overlap_key",
    "normalized_term",
    "skip",
    "direction",
    "extension_type",
    "extended_sequence",
    "current_present_corpora",
    "current_absent_corpora",
    "current_scope",
    "controlled_corpora",
    "best_q",
    "context_corpora",
    "center_surface_corpora",
    "hit_span_surface_corpora",
    "extension_span_surface_phrase_corpora",
    "synthetic_rows",
    "synthetic_same_type_ge_target",
    "synthetic_any_ge_target",
    "final_gate",
    "claim_status",
    "read",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    patterns = read_rows(args.pattern_summary)
    contexts = read_contexts(args.context_file)
    synthetics = read_synthetics(args.synthetic_summary)
    rows = [
        final_gate_row(
            pattern,
            contexts.get(pattern["overlap_key"], []),
            synthetics.get(pattern["overlap_key"], []),
        )
        for pattern in patterns
    ]
    rows = sorted(rows, key=sort_key)
    write_rows(args.summary_out, rows)
    write_markdown(args.markdown_out, rows)
    write_manifest(args, len(patterns), len(rows), started)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern-summary", type=Path, default=PATTERN_SUMMARY)
    parser.add_argument("--context-file", action="append", type=Path, default=CONTEXT_FILES)
    parser.add_argument("--synthetic-summary", type=Path, default=SYNTHETIC_SUMMARY)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def read_contexts(paths: list[Path]) -> dict[str, list[dict[str, str]]]:
    contexts: dict[str, list[dict[str, str]]] = defaultdict(list)
    seen: set[tuple[str, str]] = set()
    for path in paths:
        if not path.exists():
            continue
        for row in read_rows(path):
            key = (row["overlap_key"], row["corpus"])
            if key in seen:
                continue
            seen.add(key)
            contexts[row["overlap_key"]].append(row)
    return contexts


def read_synthetics(path: Path) -> dict[str, list[dict[str, str]]]:
    if not path.exists():
        return defaultdict(list)
    return group_synthetic_rows(read_rows(path))


def group_synthetic_rows(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    synthetics: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        synthetics[synthetic_key(row)].append(row)
    return synthetics


def synthetic_key(row: dict[str, str]) -> str:
    return "|".join(
        [
            row["normalized_term"],
            row["skip"],
            row["direction"],
            row["extension_type"],
            row["extended_sequence"],
            row["extended_sequence"],
        ]
    )


def final_gate_row(
    pattern: dict[str, str],
    contexts: list[dict[str, str]],
    synthetics: list[dict[str, str]],
) -> dict[str, str]:
    context_summary = summarize_contexts(contexts)
    synthetic_summary = summarize_synthetics(synthetics)
    gate = final_gate(
        current_scope=pattern["current_scope"],
        best_q=pattern["best_q"],
        extension_span_surface_phrase=bool(context_summary["extension_span_surface_phrase"]),
        synthetic_any_ge_target=synthetic_summary["any_ge_target"],
    )
    return {
        "overlap_key": pattern["overlap_key"],
        "normalized_term": pattern["normalized_term"],
        "skip": pattern["skip"],
        "direction": pattern["direction"],
        "extension_type": pattern["extension_type"],
        "extended_sequence": pattern["extended_sequence"],
        "current_present_corpora": pattern["current_present_corpora"],
        "current_absent_corpora": pattern["current_absent_corpora"],
        "current_scope": pattern["current_scope"],
        "controlled_corpora": pattern["controlled_corpora"],
        "best_q": pattern["best_q"],
        "context_corpora": ",".join(context_summary["context_corpora"]),
        "center_surface_corpora": ",".join(context_summary["center_surface"]),
        "hit_span_surface_corpora": ",".join(context_summary["hit_span_surface"]),
        "extension_span_surface_phrase_corpora": ",".join(
            context_summary["extension_span_surface_phrase"]
        ),
        "synthetic_rows": str(synthetic_summary["rows"]),
        "synthetic_same_type_ge_target": str(synthetic_summary["same_type_ge_target"]),
        "synthetic_any_ge_target": str(synthetic_summary["any_ge_target"]),
        "final_gate": gate,
        "claim_status": claim_status(gate),
        "read": gate_read(gate),
    }


def summarize_contexts(rows: list[dict[str, str]]) -> dict[str, list[str]]:
    context_corpora = sorted({row["corpus"] for row in rows})
    center_surface = sorted(
        row["corpus"] for row in rows if row.get("center_has_term_surface") == "yes"
    )
    hit_span_surface = sorted(
        row["corpus"] for row in rows if row.get("hit_span_has_term_surface") == "yes"
    )
    extension_span_surface_phrase = sorted(
        row["corpus"]
        for row in rows
        if row.get("extension_span_has_matched_phrase_surface") == "yes"
    )
    return {
        "context_corpora": context_corpora,
        "center_surface": center_surface,
        "hit_span_surface": hit_span_surface,
        "extension_span_surface_phrase": extension_span_surface_phrase,
    }


def summarize_synthetics(rows: list[dict[str, str]]) -> dict[str, int]:
    return {
        "rows": len(rows),
        "same_type_ge_target": sum(int_or_zero(row["synthetic_same_type_ge_target"]) for row in rows),
        "any_ge_target": sum(int_or_zero(row["synthetic_any_ge_target"]) for row in rows),
    }


def final_gate(
    *,
    current_scope: str,
    best_q: str,
    extension_span_surface_phrase: bool,
    synthetic_any_ge_target: int,
) -> str:
    if current_scope == "source_only":
        return "source_specific_hidden_path_candidate"
    if current_scope == "multi_source":
        return "multi_source_hidden_path_candidate"
    q_value = numeric_value(best_q)
    if q_value is None or q_value > 0.01:
        return "all_source_presence_needs_controls"
    if not extension_span_surface_phrase:
        return "cross_version_controlled_surface_anchored_hidden_candidate"
    if synthetic_any_ge_target:
        return "cross_version_controlled_surface_echo_candidate_with_synthetic_caution"
    return "cross_version_controlled_surface_echo_candidate"


def claim_status(gate: str) -> str:
    if gate == "all_source_presence_needs_controls":
        return "needs_controls"
    return "review_candidate_not_claim"


def gate_read(gate: str) -> str:
    return {
        "source_specific_hidden_path_candidate": "source-specific hidden-path candidate; not cross-text evidence",
        "multi_source_hidden_path_candidate": "multi-source hidden-path candidate; missing compared sources",
        "all_source_presence_needs_controls": "all-source presence, but controls not strong enough under q <= 0.01 gate",
        "cross_version_controlled_surface_anchored_hidden_candidate": "cross-version controlled hidden-path candidate with related surface anchor",
        "cross_version_controlled_surface_echo_candidate_with_synthetic_caution": "rare surface-echo candidate; synthetic baselines can match or exceed target",
        "cross_version_controlled_surface_echo_candidate": "rare surface-echo candidate; still review-only until study-level controls pass",
    }[gate]


def write_markdown(path: Path, rows: list[dict[str, str]]) -> None:
    gate_counts = Counter(row["final_gate"] for row in rows)
    lines = [
        "# Greek Exact-Center Final Gate",
        "",
        "This report consolidates exact-center Greek extension pattern presence,",
        "row-local controls, context review, and same-length synthetic baselines.",
        "",
        "## Rows",
        "",
        "| Pattern | Present | Missing | Best q | Surface phrase in span | Synthetic >= target | Gate | Read |",
        "| --- | --- | --- | ---: | --- | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['overlap_key']}`",
                    row["current_present_corpora"],
                    row["current_absent_corpora"] or "none",
                    row["best_q"],
                    row["extension_span_surface_phrase_corpora"] or "none",
                    row["synthetic_any_ge_target"],
                    f"`{row['final_gate']}`",
                    row["read"],
                ]
            )
            + " |"
        )
    lines.extend(["", "## Gate Counts", "", "| Gate | Rows |", "| --- | ---: |"])
    for gate, count in sorted(gate_counts.items()):
        lines.append(f"| `{gate}` | {count} |")
    lines.extend(
        [
            "",
            "## Read",
            "",
            "This gate now separates candidate type from claim status. Hidden-path-only",
            "phrases are normal ELS candidates, not failures. A same-span surface echo",
            "would be a rarer and stronger subtype.",
            "",
            "`δοξα` is the strongest current row because it has four-source presence,",
            "q <= 0.01 controls, and related surface context around glory/glorified.",
            "Its current type is a cross-version controlled surface-anchored hidden",
            "candidate. It is still not a claim because study-level controls and",
            "predeclared interpretation standards have not promoted it that far.",
            "",
            "`υιος` and `αιμα` remain weaker review candidates because their exact",
            "patterns are missing from one or more compared Greek NT sources.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    input_rows: int,
    output_rows: int,
    started: float,
) -> None:
    payload = {
        "tool": "analyze_greek_exact_center_final_gate",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "pattern_summary": str(args.pattern_summary),
            "context_files": [str(path) for path in args.context_file],
            "synthetic_summary": str(args.synthetic_summary),
        },
        "input_rows": input_rows,
        "output_rows": output_rows,
        "outputs": {
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


def sort_key(row: dict[str, str]) -> tuple[int, str]:
    order = {
        "cross_version_controlled_surface_echo_candidate": 0,
        "cross_version_controlled_surface_echo_candidate_with_synthetic_caution": 1,
        "cross_version_controlled_surface_anchored_hidden_candidate": 2,
        "multi_source_hidden_path_candidate": 3,
        "source_specific_hidden_path_candidate": 4,
        "all_source_presence_needs_controls": 5,
    }
    return (order.get(row["final_gate"], 99), row["overlap_key"])


def int_or_zero(value: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    raise SystemExit(main())
