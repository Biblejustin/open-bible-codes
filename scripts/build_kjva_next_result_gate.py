#!/usr/bin/env python3
"""Build a non-text KJVA next-result gate."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__


DEFAULT_SOURCE_POLICY_SUMMARY = Path("reports/kjva_source_policy_blocker_packet/summary.csv")
DEFAULT_SOURCE_POLICY_BLOCKERS = Path("reports/kjva_source_policy_blocker_packet/blockers.csv")
DEFAULT_PROSPECTIVE_TERM_SUMMARY = Path(
    "reports/kjv_apocrypha_bridge_prospective/term_summary.csv"
)
DEFAULT_NONBIBLE_CONTROLS = Path(
    "reports/kjv_apocrypha_bridge_prospective_nonbible_controls/control_summary.csv"
)
DEFAULT_OUT_DIR = Path("reports/kjva_next_result_gate")
DEFAULT_GATES = DEFAULT_OUT_DIR / "gates.csv"
DEFAULT_SUMMARY = DEFAULT_OUT_DIR / "summary.csv"
DEFAULT_MANIFEST = DEFAULT_OUT_DIR / "manifest.json"
DEFAULT_MD = Path("docs/KJVA_NEXT_RESULT_GATE.md")

GATE_FIELDNAMES = [
    "gate_id",
    "area",
    "status",
    "evidence_summary",
    "required_before_result",
    "next_action",
    "result_boundary",
]
SUMMARY_FIELDNAMES = [
    "gate_rows",
    "rerun_only_ready_rows",
    "blocked_rows",
    "source_policy_blocker_rows",
    "completed_lane_terms",
    "completed_lane_observed_bridge_rows",
    "completed_lane_significant_terms",
    "nonbible_controls_at_or_above_observed",
    "source_lock_ready",
    "fresh_terms_ready",
    "leakage_audit_ready",
    "fixed_controls_ready",
    "study_lock_ready",
    "result_allowed",
    "claim_status",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    source_policy = read_single_csv_row(args.source_policy_summary)
    source_blockers = read_csv_dicts(args.source_policy_blockers)
    term_summary = read_csv_dicts(args.prospective_term_summary)
    controls = read_csv_dicts(args.nonbible_controls)
    gates = build_gates(source_policy, source_blockers, term_summary, controls)
    summary = build_summary(gates, source_policy, source_blockers, term_summary, controls)
    write_csv(args.gates_out, GATE_FIELDNAMES, gates)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, summary, gates)
    write_manifest(args.manifest_out, args, summary, gates, started)
    print(args.gates_out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-policy-summary", type=Path, default=DEFAULT_SOURCE_POLICY_SUMMARY
    )
    parser.add_argument(
        "--source-policy-blockers", type=Path, default=DEFAULT_SOURCE_POLICY_BLOCKERS
    )
    parser.add_argument(
        "--prospective-term-summary", type=Path, default=DEFAULT_PROSPECTIVE_TERM_SUMMARY
    )
    parser.add_argument("--nonbible-controls", type=Path, default=DEFAULT_NONBIBLE_CONTROLS)
    parser.add_argument("--gates-out", type=Path, default=DEFAULT_GATES)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_gates(
    source_policy: dict[str, str],
    source_blockers: list[dict[str, str]],
    term_summary: list[dict[str, str]],
    controls: list[dict[str, str]],
) -> list[dict[str, Any]]:
    completed_lane = summarize_completed_lane(term_summary, controls)
    source_blocker_count = len(source_blockers)
    return [
        gate(
            "current_rerun_reproducibility",
            "rerun baseline",
            "rerun_only_ready",
            f"current rerun locked={source_policy.get('current_rerun_locked', '')}; checksum records ready={source_policy.get('checksum_records_ready', '')}",
            "no new result requirement; rerun current eBible baseline only",
            "Keep current-source reruns separate from independent replication.",
        ),
        gate(
            "completed_lane_claim_gate",
            "completed KJVA prospective lane",
            "blocked",
            f"terms={completed_lane['terms']}; observed_bridge_rows={completed_lane['observed_bridge_rows']}; significant_terms={completed_lane['significant_terms']}; nonbible_controls_at_or_above={completed_lane['controls_at_or_above']}",
            "new result may not reuse the completed negative prospective lane as claim evidence",
            "Keep completed lane as review material only.",
        ),
        gate(
            "source_policy_lock",
            "source policy",
            "blocked",
            f"source_policy_blockers={source_blocker_count}; source_lock_ready={source_policy.get('source_lock_ready', '')}",
            "source-use and source-role policy must authorize any selected external source",
            "Close source-use, source-text, and split-source blockers first.",
        ),
        gate(
            "source_text_lock",
            "source text",
            "blocked",
            "no independent KJVA source text is source-locked for result-bearing use",
            "selected source stream has checksum, text-retention, order, and source-use lock",
            "Do not import or substitute source text silently.",
        ),
        gate(
            "verse_map_collation_lock",
            "verse map and collation",
            "blocked",
            "no result-bearing verse map or full selected-source collation lock exists",
            "selected stream has verse map and collation sidecar before output",
            "Finish source mapping before any run.",
        ),
        gate(
            "drift_boundary_lock",
            "drift and boundary",
            "blocked",
            f"Sirach gap={source_policy.get('gutenberg_sirach_gap_refs', '')}; MAN markers={source_policy.get('gutenberg_manasseh_source_markers', '')}/{source_policy.get('gutenberg_manasseh_local_markers', '')}; Hakkaac drift verses={source_policy.get('hakkaac_length_drift_verses', '')}",
            "Sirach, Prayer of Manasseh, and Hakkaac drift policies are locked before output",
            "Write cited drift/boundary decisions first.",
        ),
        gate(
            "fresh_term_lock",
            "terms",
            "blocked",
            "no fresh KJVA term list is locked for a new result-bearing run",
            "fresh terms are preregistered before new output is seen",
            "Define term-selection rules and lock the term file.",
        ),
        gate(
            "leakage_audit_lock",
            "leakage audit",
            "blocked",
            "no leakage audit records new terms as independent from prior KJVA screens",
            "term list is checked against prior KJVA bridge files and outputs",
            "Run leakage audit after term lock.",
        ),
        gate(
            "fixed_controls_lock",
            "controls",
            "blocked",
            "no fixed control plan is locked for a new KJVA result-bearing run",
            "shuffled and non-Bible controls are preregistered with sample counts",
            "Lock control design before output.",
        ),
        gate(
            "study_lock_manifest",
            "study lock",
            "blocked",
            "no new KJVA study-lock manifest exists",
            "source, term, leakage, controls, correction, and reporting rules are frozen",
            "Write study-lock manifest only after upstream gates close.",
        ),
        gate(
            "result_allowed",
            "result permission",
            "blocked",
            "new KJVA result-bearing output is not allowed by current gates",
            "all source and study gates pass before any new result run",
            "Do not run new KJVA results yet.",
        ),
    ]


def build_summary(
    gates: list[dict[str, Any]],
    source_policy: dict[str, str],
    source_blockers: list[dict[str, str]],
    term_summary: list[dict[str, str]],
    controls: list[dict[str, str]],
) -> dict[str, Any]:
    completed_lane = summarize_completed_lane(term_summary, controls)
    return {
        "gate_rows": len(gates),
        "rerun_only_ready_rows": count_status(gates, "rerun_only_ready"),
        "blocked_rows": count_status(gates, "blocked"),
        "source_policy_blocker_rows": len(source_blockers),
        "completed_lane_terms": completed_lane["terms"],
        "completed_lane_observed_bridge_rows": completed_lane["observed_bridge_rows"],
        "completed_lane_significant_terms": completed_lane["significant_terms"],
        "nonbible_controls_at_or_above_observed": completed_lane["controls_at_or_above"],
        "source_lock_ready": source_policy.get("source_lock_ready", "") == "True",
        "fresh_terms_ready": False,
        "leakage_audit_ready": False,
        "fixed_controls_ready": False,
        "study_lock_ready": False,
        "result_allowed": False,
        "claim_status": "kjva_next_result_gate_blocks_new_output",
    }


def summarize_completed_lane(
    term_summary: list[dict[str, str]],
    controls: list[dict[str, str]],
) -> dict[str, int]:
    observed_bridge_rows = sum(int(row.get("observed_bridge_rows") or 0) for row in term_summary)
    significant_terms = sum(
        1
        for row in term_summary
        if row.get("q_ge") not in (None, "") and float(row["q_ge"]) <= 0.05
    )
    controls_at_or_above = sum(
        1 for row in controls if int(row.get("bridge_rows") or 0) >= observed_bridge_rows
    )
    return {
        "terms": len(term_summary),
        "observed_bridge_rows": observed_bridge_rows,
        "significant_terms": significant_terms,
        "controls_at_or_above": controls_at_or_above,
    }


def write_markdown(
    path: Path,
    summary: dict[str, Any],
    gates: list[dict[str, Any]],
) -> None:
    lines = [
        "# KJVA Next Result Gate",
        "",
        "Status: next-result gate only.",
        "",
        "This is not an ELS result, not a corpus import, not a source-use approval, not a source lock, not a term lock, and not a study lock.",
        "It records which gates are open or blocked before any future KJVA result-bearing run.",
        "It allows only current-source rerun reproducibility, not a new independent KJVA result.",
        "",
        "## Summary",
        "",
        f"- Gate rows: {summary['gate_rows']}.",
        f"- Rerun-only ready rows: {summary['rerun_only_ready_rows']}.",
        f"- Blocked rows: {summary['blocked_rows']}.",
        f"- Source-policy blocker rows: {summary['source_policy_blocker_rows']}.",
        f"- Completed lane terms: {summary['completed_lane_terms']}.",
        f"- Completed lane observed bridge rows: {summary['completed_lane_observed_bridge_rows']}.",
        f"- Completed lane significant terms: {summary['completed_lane_significant_terms']}.",
        f"- Non-Bible controls at or above observed: {summary['nonbible_controls_at_or_above_observed']}.",
        f"- Source-lock ready: {int(bool(summary['source_lock_ready']))}.",
        f"- Fresh terms ready: {int(bool(summary['fresh_terms_ready']))}.",
        f"- Leakage audit ready: {int(bool(summary['leakage_audit_ready']))}.",
        f"- Fixed controls ready: {int(bool(summary['fixed_controls_ready']))}.",
        f"- Study-lock ready: {int(bool(summary['study_lock_ready']))}.",
        f"- Result allowed: {int(bool(summary['result_allowed']))}.",
        f"- Claim status: `{summary['claim_status']}`.",
        "",
        "## Gates",
        "",
        "| Gate | Area | Status | Evidence | Required before result |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in gates:
        lines.append(
            f"| `{row['gate_id']}` | {row['area']} | `{row['status']}` | {row['evidence_summary']} | {row['required_before_result']} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "Current eBible KJVA reruns remain allowed for reproducibility only.",
            "No new independent KJVA result-bearing run is allowed by this gate.",
            "A future run still needs source policy, source text, verse map, collation, drift/boundary, fresh terms, leakage audit, fixed controls, and study-lock manifest gates to pass first.",
            "No Bible text is written to tracked outputs.",
            "It does not change any KJVA bridge result status.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary: dict[str, Any],
    gates: list[dict[str, Any]],
    started: float,
) -> None:
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "els_version": __version__,
        "tool": "scripts.build_kjva_next_result_gate",
        "claim_boundary": "KJVA next-result gate only; no ELS result",
        "text_retention": "no Bible text written to tracked outputs",
        "summary": summary,
        "gate_rows": len(gates),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "source_policy_summary": str(args.source_policy_summary),
            "source_policy_blockers": str(args.source_policy_blockers),
            "prospective_term_summary": str(args.prospective_term_summary),
            "nonbible_controls": str(args.nonbible_controls),
        },
        "outputs": {
            "gates": str(args.gates_out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def gate(
    gate_id: str,
    area: str,
    status: str,
    evidence_summary: str,
    required_before_result: str,
    next_action: str,
) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "area": area,
        "status": status,
        "evidence_summary": evidence_summary,
        "required_before_result": required_before_result,
        "next_action": next_action,
        "result_boundary": "not_result_bearing",
    }


def count_status(rows: list[dict[str, Any]], status: str) -> int:
    return sum(1 for row in rows if row["status"] == status)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_single_csv_row(path: Path) -> dict[str, str]:
    rows = read_csv_dicts(path)
    if len(rows) != 1:
        raise ValueError(f"{path} expected one row, found {len(rows)}")
    return rows[0]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
