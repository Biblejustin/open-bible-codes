#!/usr/bin/env python3
"""Consolidate STEP_TAHOT source-only screening, policy, and control checks."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


REAL_PATTERNS = Path("reports/step_tahot_screening_version_presence/hit_patterns.csv")
REAL_POLICY = Path("reports/step_tahot_policy_hits/step_tahot_only_policy_hits.csv")
CONTROL_PATTERNS = Path("reports/step_tahot_control_version_presence/hit_patterns.csv")
CONTROL_POLICY = Path("reports/step_tahot_control_policy_hits/step_tahot_only_policy_hits.csv")
OUT_DIR = Path("reports/step_tahot_final_gate")
SUMMARY_OUT = OUT_DIR / "summary.csv"
TERM_SUMMARY_OUT = OUT_DIR / "term_summary.csv"
ROW_GATE_OUT = OUT_DIR / "row_gate.csv"
MD_OUT = OUT_DIR / "step_tahot_final_gate.md"
MANIFEST_OUT = OUT_DIR / "manifest.json"
SOURCE_LABEL = "STEP_TAHOT"

SUMMARY_FIELDNAMES = ["metric", "real_terms", "controls", "read"]
TERM_FIELDNAMES = [
    "term_id",
    "concept",
    "category",
    "source_only_rows",
    "policy_touch_rows",
    "l_only_rows",
    "q_rows",
    "r_rows",
    "x_rows",
    "read",
]
ROW_GATE_FIELDNAMES = [
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "start_ref",
    "center_ref",
    "end_ref",
    "policy_flags",
    "final_gate",
    "claim_status",
    "read",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    real_patterns = read_rows(args.real_patterns)
    real_policy = read_rows(args.real_policy)
    control_patterns = read_rows(args.control_patterns)
    control_policy = read_rows(args.control_policy)

    real_counts = pattern_counts(real_patterns, args.source_label)
    control_counts = pattern_counts(control_patterns, args.source_label)
    validate_policy_rows("real", real_counts["source_only"], real_policy)
    validate_policy_rows("control", control_counts["source_only"], control_policy)

    real_policy_counts = policy_counts(real_policy)
    control_policy_counts = policy_counts(control_policy)
    summary_rows = summary_table(
        real_counts,
        real_policy_counts,
        control_counts,
        control_policy_counts,
    )
    term_rows = term_summary(real_policy)
    gated_rows = [row_gate(row) for row in real_policy]

    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_rows(args.term_summary_out, TERM_FIELDNAMES, term_rows)
    write_rows(args.row_gate_out, ROW_GATE_FIELDNAMES, gated_rows)
    write_markdown(args.markdown_out, summary_rows, term_rows, gated_rows)
    write_manifest(
        args,
        real_counts,
        real_policy_counts,
        control_counts,
        control_policy_counts,
        len(term_rows),
        len(gated_rows),
        started,
    )
    print(args.summary_out)
    print(args.term_summary_out)
    print(args.row_gate_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--real-patterns", type=Path, default=REAL_PATTERNS)
    parser.add_argument("--real-policy", type=Path, default=REAL_POLICY)
    parser.add_argument("--control-patterns", type=Path, default=CONTROL_PATTERNS)
    parser.add_argument("--control-policy", type=Path, default=CONTROL_POLICY)
    parser.add_argument("--source-label", default=SOURCE_LABEL)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--term-summary-out", type=Path, default=TERM_SUMMARY_OUT)
    parser.add_argument("--row-gate-out", type=Path, default=ROW_GATE_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def pattern_counts(rows: list[dict[str, str]], source_label: str) -> dict[str, float]:
    total = len(rows)
    with_source = sum(source_label in split_corpora(row["present_corpora"]) for row in rows)
    source_only = sum(split_corpora(row["present_corpora"]) == [source_label] for row in rows)
    return {
        "pattern_rows": total,
        "with_source": with_source,
        "source_only": source_only,
        "source_only_rate": source_only / total if total else 0.0,
    }


def policy_counts(rows: list[dict[str, str]]) -> dict[str, float]:
    total = len(rows)
    policy_touch = sum(row["policy_flags"] != "L_ONLY_PATH" for row in rows)
    l_only = sum(row["policy_flags"] == "L_ONLY_PATH" for row in rows)
    q_rows = sum("Q" in split_flags(row["policy_flags"]) for row in rows)
    r_rows = sum("R" in split_flags(row["policy_flags"]) for row in rows)
    x_rows = sum("X" in split_flags(row["policy_flags"]) for row in rows)
    return {
        "policy_rows": total,
        "policy_touch": policy_touch,
        "l_only": l_only,
        "q_rows": q_rows,
        "r_rows": r_rows,
        "x_rows": x_rows,
        "policy_touch_rate": policy_touch / total if total else 0.0,
    }


def summary_table(
    real_counts: dict[str, float],
    real_policy: dict[str, float],
    control_counts: dict[str, float],
    control_policy: dict[str, float],
) -> list[dict[str, str]]:
    rate_ratio = (
        real_counts["source_only_rate"] / control_counts["source_only_rate"]
        if control_counts["source_only_rate"]
        else 0.0
    )
    return [
        row("pattern_rows", real_counts["pattern_rows"], control_counts["pattern_rows"], "screen size"),
        row("patterns_with_step_tahot", real_counts["with_source"], control_counts["with_source"], "STEP_TAHOT participates broadly"),
        row("step_tahot_only_rows", real_counts["source_only"], control_counts["source_only"], "source-only rows exist in terms and controls"),
        row("step_tahot_only_rate", percent(real_counts["source_only_rate"]), percent(control_counts["source_only_rate"]), f"real/control ratio {rate_ratio:.3f}"),
        row("policy_touch_rows", real_policy["policy_touch"], control_policy["policy_touch"], "hidden path touches Q/R/X/other source policy"),
        row("policy_touch_rate_among_step_only", percent(real_policy["policy_touch_rate"]), percent(control_policy["policy_touch_rate"]), "computed within STEP_TAHOT-only rows"),
        row("l_only_path_rows", real_policy["l_only"], control_policy["l_only"], "letters are in L-prefixed TAHOT words"),
        row("q_rows", real_policy["q_rows"], control_policy["q_rows"], "qere-selected path rows"),
        row("r_rows", real_policy["r_rows"], control_policy["r_rows"], "restored-word path rows"),
        row("x_rows", real_policy["x_rows"], control_policy["x_rows"], "LXX-based Hebrew-addition path rows"),
    ]


def row(metric: str, real: object, controls: object, read: str) -> dict[str, str]:
    return {
        "metric": metric,
        "real_terms": str(real),
        "controls": str(controls),
        "read": read,
    }


def term_summary(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_term: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        by_term.setdefault(row["term_id"], []).append(row)
    output = []
    for term_id, term_rows in by_term.items():
        first = term_rows[0]
        flags = [split_flags(row["policy_flags"]) for row in term_rows]
        policy_touch = sum(row["policy_flags"] != "L_ONLY_PATH" for row in term_rows)
        l_only = len(term_rows) - policy_touch
        q_rows = sum("Q" in row_flags for row_flags in flags)
        r_rows = sum("R" in row_flags for row_flags in flags)
        x_rows = sum("X" in row_flags for row_flags in flags)
        output.append(
            {
                "term_id": term_id,
                "concept": first["concept"],
                "category": first["category"],
                "source_only_rows": str(len(term_rows)),
                "policy_touch_rows": str(policy_touch),
                "l_only_rows": str(l_only),
                "q_rows": str(q_rows),
                "r_rows": str(r_rows),
                "x_rows": str(x_rows),
                "read": term_read(policy_touch, l_only),
            }
        )
    return sorted(
        output,
        key=lambda row: (
            -int(row["source_only_rows"]),
            -int(row["policy_touch_rows"]),
            row["term_id"],
        ),
    )


def row_gate(source: dict[str, str]) -> dict[str, str]:
    gate = gate_for_flags(source["policy_flags"])
    return {
        "term_id": source["term_id"],
        "concept": source["concept"],
        "category": source["category"],
        "term": source["term"],
        "normalized_term": source["normalized_term"],
        "skip": source["skip"],
        "direction": source["direction"],
        "start_ref": source["start_ref"],
        "center_ref": source["center_ref"],
        "end_ref": source["end_ref"],
        "policy_flags": source["policy_flags"],
        "final_gate": gate,
        "claim_status": "hold",
        "read": gate_read(gate),
    }


def gate_for_flags(flags: str) -> str:
    if flags == "L_ONLY_PATH":
        return "hold_l_only_step_tahot_specific"
    return "hold_selected_reading_policy_path"


def gate_read(gate: str) -> str:
    if gate == "hold_selected_reading_policy_path":
        return "do not promote; hidden path touches selected TAHOT source policy"
    return "do not promote; controls also produce STEP_TAHOT-only L-path rows"


def term_read(policy_touch: int, l_only: int) -> str:
    if policy_touch and l_only:
        return "mixed policy-touch and L-only source-specific rows"
    if policy_touch:
        return "all STEP_TAHOT-only rows touch selected source policy"
    return "L-only source-specific rows; compare against controls"


def split_corpora(value: str) -> list[str]:
    return [part for part in value.replace(";", ",").split(",") if part]


def split_flags(value: str) -> set[str]:
    return {part for part in value.split() if part}


def validate_policy_rows(label: str, expected: float, rows: list[dict[str, str]]) -> None:
    if int(expected) != len(rows):
        raise ValueError(
            f"{label} policy rows are stale: expected {int(expected)}, found {len(rows)}"
        )


def percent(value: float) -> str:
    return f"{value * 100:.3f}%"


def write_markdown(
    path: Path,
    summary_rows: list[dict[str, str]],
    term_rows: list[dict[str, str]],
    gated_rows: list[dict[str, str]],
) -> None:
    lines = [
        "# STEP TAHOT Final Gate",
        "",
        "This report consolidates STEP_TAHOT source-only screening rows,",
        "TAHOT source-policy path audits, and matching null/frequency controls.",
        "",
        "## Summary",
        "",
        "| Metric | Real terms | Controls | Read |",
        "| --- | ---: | ---: | --- |",
    ]
    for item in summary_rows:
        lines.append(
            f"| `{item['metric']}` | {item['real_terms']} | {item['controls']} | {item['read']} |"
        )
    lines.extend(
        [
            "",
            "## Top Real STEP_TAHOT-Only Terms",
            "",
            "| Term | Source-only rows | Policy-touch | L-only | Q | R | X | Read |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for item in term_rows[:25]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{item['term_id']}`",
                    item["source_only_rows"],
                    item["policy_touch_rows"],
                    item["l_only_rows"],
                    item["q_rows"],
                    item["r_rows"],
                    item["x_rows"],
                    item["read"],
                ]
            )
            + " |"
        )
    gate_counts = Counter(row["final_gate"] for row in gated_rows)
    lines.extend(
        [
            "",
            "## Gate Counts",
            "",
            "| Gate | Rows |",
            "| --- | ---: |",
        ]
    )
    for gate, count in sorted(gate_counts.items()):
        lines.append(f"| `{gate}` | {count} |")
    lines.extend(
        [
            "",
            "## Read",
            "",
            "No STEP_TAHOT-only row is promoted by this gate. The selected stream is useful",
            "for source-family review, but STEP_TAHOT-only behavior also appears in",
            "null/frequency controls at a comparable rate.",
            "",
            "`hold_selected_reading_policy_path` rows touch qere, restored, LXX-based",
            "Hebrew addition, or other non-L source-policy words on the hidden-letter path.",
            "`hold_l_only_step_tahot_specific` rows avoid those path flags, but controls",
            "also produce STEP_TAHOT-only L-path rows, so they remain source-specific",
            "review rows rather than claim rows.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    real_counts: dict[str, float],
    real_policy: dict[str, float],
    control_counts: dict[str, float],
    control_policy: dict[str, float],
    term_rows: int,
    gated_rows: int,
    started: float,
) -> None:
    payload = {
        "tool": "analyze_step_tahot_final_gate",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "real_patterns": str(args.real_patterns),
            "real_policy": str(args.real_policy),
            "control_patterns": str(args.control_patterns),
            "control_policy": str(args.control_policy),
        },
        "real_counts": real_counts,
        "real_policy_counts": real_policy,
        "control_counts": control_counts,
        "control_policy_counts": control_policy,
        "term_rows": term_rows,
        "gated_rows": gated_rows,
        "outputs": {
            "summary": str(args.summary_out),
            "term_summary": str(args.term_summary_out),
            "row_gate": str(args.row_gate_out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
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


if __name__ == "__main__":
    raise SystemExit(main())
