#!/usr/bin/env python3
"""Build a consolidated KJVA no-input handoff status packet."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__


DEFAULT_NEXT_RESULT_SUMMARY = Path("reports/kjva_next_result_gate/summary.csv")
DEFAULT_NEXT_RESULT_GATES = Path("reports/kjva_next_result_gate/gates.csv")
DEFAULT_SOURCE_POLICY_SUMMARY = Path(
    "reports/kjva_source_policy_blocker_packet/summary.csv"
)
DEFAULT_SOURCE_POLICY_BLOCKERS = Path(
    "reports/kjva_source_policy_blocker_packet/blockers.csv"
)
DEFAULT_CURRENT_SOURCE_SUMMARY = Path("reports/kjva_current_source_lock_sidecar/summary.csv")
DEFAULT_GUTENBERG_BLOCKER_SUMMARY = Path(
    "reports/kjva_gutenberg_source_lock_blocker_packet/summary.csv"
)
DEFAULT_HAKKAAC_COLLATION_SUMMARY = Path(
    "reports/kjva_hakkaac_apocrypha_collation/summary.csv"
)
DEFAULT_SPLIT_ROLE_SUMMARY = Path(
    "reports/kjva_gutenberg_hakkaac_split_source_role_sidecar/summary.csv"
)
DEFAULT_PROSPECTIVE_TERM_SUMMARY = Path(
    "reports/kjv_apocrypha_bridge_prospective/term_summary.csv"
)
DEFAULT_PROSPECTIVE_NONBIBLE_SUMMARY = Path(
    "reports/kjv_apocrypha_bridge_prospective_nonbible_controls/term_summary.csv"
)
DEFAULT_OUT = Path("reports/kjva_no_input_handoff_status/status.csv")
DEFAULT_SUMMARY_OUT = Path("reports/kjva_no_input_handoff_status/summary.csv")
DEFAULT_MD = Path("docs/KJVA_NO_INPUT_HANDOFF_STATUS.md")
DEFAULT_MANIFEST = Path("reports/kjva_no_input_handoff_status/manifest.json")

STATUS_FIELDNAMES = [
    "status_id",
    "area",
    "current_status",
    "current_value",
    "handoff_ready",
    "manual_input_needed",
    "next_action",
    "boundary",
    "source",
]
SUMMARY_FIELDNAMES = [
    "status_rows",
    "handoff_ready_rows",
    "manual_input_needed_rows",
    "gate_rows",
    "rerun_only_ready_rows",
    "blocked_gate_rows",
    "source_policy_blocker_rows",
    "policy_option_rows",
    "policy_ready_options",
    "blocked_options",
    "checksum_records_ready",
    "current_rerun_locked",
    "source_use_ready_pages",
    "source_lock_ready",
    "result_allowed",
    "completed_lane_terms",
    "completed_lane_observed_bridge_rows",
    "completed_lane_significant_terms",
    "nonbible_controls_at_or_above_observed",
    "gutenberg_sirach_gap_refs",
    "gutenberg_manasseh_source_markers",
    "gutenberg_manasseh_local_markers",
    "hakkaac_exact_normalized_verse_matches",
    "hakkaac_total_verses",
    "hakkaac_length_drift_verses",
    "split_source_role_rows",
    "split_source_blocker_rows",
    "fresh_terms_ready",
    "leakage_audit_ready",
    "fixed_controls_ready",
    "study_lock_ready",
    "claim_status",
]

CLAIM_BOUNDARY = "kjva_no_input_handoff_blocks_new_result"


class LoadedInputs:
    def __init__(
        self,
        *,
        next_result_summary: list[dict[str, str]],
        next_result_gates: list[dict[str, str]],
        source_policy_summary: list[dict[str, str]],
        source_policy_blockers: list[dict[str, str]],
        current_source_summary: list[dict[str, str]],
        gutenberg_blocker_summary: list[dict[str, str]],
        hakkaac_collation_summary: list[dict[str, str]],
        split_role_summary: list[dict[str, str]],
        prospective_term_summary: list[dict[str, str]],
        prospective_nonbible_summary: list[dict[str, str]],
    ) -> None:
        self.next_result_summary = next_result_summary
        self.next_result_gates = next_result_gates
        self.source_policy_summary = source_policy_summary
        self.source_policy_blockers = source_policy_blockers
        self.current_source_summary = current_source_summary
        self.gutenberg_blocker_summary = gutenberg_blocker_summary
        self.hakkaac_collation_summary = hakkaac_collation_summary
        self.split_role_summary = split_role_summary
        self.prospective_term_summary = prospective_term_summary
        self.prospective_nonbible_summary = prospective_nonbible_summary


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    inputs = LoadedInputs(
        next_result_summary=read_rows(args.next_result_summary),
        next_result_gates=read_rows(args.next_result_gates),
        source_policy_summary=read_rows(args.source_policy_summary),
        source_policy_blockers=read_rows(args.source_policy_blockers),
        current_source_summary=read_rows(args.current_source_summary),
        gutenberg_blocker_summary=read_rows(args.gutenberg_blocker_summary),
        hakkaac_collation_summary=read_rows(args.hakkaac_collation_summary),
        split_role_summary=read_rows(args.split_role_summary),
        prospective_term_summary=read_rows(args.prospective_term_summary),
        prospective_nonbible_summary=read_rows(args.prospective_nonbible_summary),
    )
    summary = build_summary(inputs)
    rows = build_status_rows(summary, inputs, args)
    write_csv(args.out, STATUS_FIELDNAMES, rows)
    write_csv(args.summary_out, SUMMARY_FIELDNAMES, [summary])
    write_markdown(args.markdown_out, summary, rows)
    write_manifest(args.manifest_out, args, summary, rows, started)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--next-result-summary", type=Path, default=DEFAULT_NEXT_RESULT_SUMMARY
    )
    parser.add_argument("--next-result-gates", type=Path, default=DEFAULT_NEXT_RESULT_GATES)
    parser.add_argument(
        "--source-policy-summary", type=Path, default=DEFAULT_SOURCE_POLICY_SUMMARY
    )
    parser.add_argument(
        "--source-policy-blockers", type=Path, default=DEFAULT_SOURCE_POLICY_BLOCKERS
    )
    parser.add_argument(
        "--current-source-summary", type=Path, default=DEFAULT_CURRENT_SOURCE_SUMMARY
    )
    parser.add_argument(
        "--gutenberg-blocker-summary",
        type=Path,
        default=DEFAULT_GUTENBERG_BLOCKER_SUMMARY,
    )
    parser.add_argument(
        "--hakkaac-collation-summary",
        type=Path,
        default=DEFAULT_HAKKAAC_COLLATION_SUMMARY,
    )
    parser.add_argument(
        "--split-role-summary", type=Path, default=DEFAULT_SPLIT_ROLE_SUMMARY
    )
    parser.add_argument(
        "--prospective-term-summary", type=Path, default=DEFAULT_PROSPECTIVE_TERM_SUMMARY
    )
    parser.add_argument(
        "--prospective-nonbible-summary",
        type=Path,
        default=DEFAULT_PROSPECTIVE_NONBIBLE_SUMMARY,
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MD)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_summary(inputs: LoadedInputs) -> dict[str, Any]:
    next_result = first_row(inputs.next_result_summary)
    policy = first_row(inputs.source_policy_summary)
    current = first_row(inputs.current_source_summary)
    gutenberg = first_row(inputs.gutenberg_blocker_summary)
    hakkaac = first_row(inputs.hakkaac_collation_summary)
    split = first_row(inputs.split_role_summary)
    return {
        "status_rows": 9,
        "handoff_ready_rows": 9,
        "manual_input_needed_rows": 8,
        "gate_rows": int_or_zero(next_result.get("gate_rows")),
        "rerun_only_ready_rows": int_or_zero(next_result.get("rerun_only_ready_rows")),
        "blocked_gate_rows": int_or_zero(next_result.get("blocked_rows")),
        "source_policy_blocker_rows": int_or_zero(
            next_result.get("source_policy_blocker_rows")
        ),
        "policy_option_rows": int_or_zero(policy.get("policy_option_rows")),
        "policy_ready_options": int_or_zero(policy.get("policy_ready_options")),
        "blocked_options": int_or_zero(policy.get("blocked_options")),
        "checksum_records_ready": int_or_zero(policy.get("checksum_records_ready")),
        "current_rerun_locked": truthy(current.get("rerun_baseline_locked")),
        "source_use_ready_pages": int_or_zero(policy.get("source_use_ready_pages")),
        "source_lock_ready": truthy(next_result.get("source_lock_ready")),
        "result_allowed": truthy(next_result.get("result_allowed")),
        "completed_lane_terms": int_or_zero(
            next_result.get("completed_lane_terms", len(inputs.prospective_term_summary))
        ),
        "completed_lane_observed_bridge_rows": int_or_zero(
            next_result.get("completed_lane_observed_bridge_rows")
        ),
        "completed_lane_significant_terms": int_or_zero(
            next_result.get("completed_lane_significant_terms")
        ),
        "nonbible_controls_at_or_above_observed": int_or_zero(
            next_result.get("nonbible_controls_at_or_above_observed")
        ),
        "gutenberg_sirach_gap_refs": (
            policy.get("gutenberg_sirach_gap_refs")
            or gutenberg.get("sirach_gap_refs")
        ),
        "gutenberg_manasseh_source_markers": int_or_zero(
            policy.get("gutenberg_manasseh_source_markers")
            or gutenberg.get("manasseh_source_markers")
        ),
        "gutenberg_manasseh_local_markers": int_or_zero(
            policy.get("gutenberg_manasseh_local_markers")
            or gutenberg.get("manasseh_local_markers")
        ),
        "hakkaac_exact_normalized_verse_matches": int_or_zero(
            hakkaac.get("exact_normalized_verse_matches")
        ),
        "hakkaac_total_verses": int_or_zero(hakkaac.get("local_verses")),
        "hakkaac_length_drift_verses": int_or_zero(
            policy.get("hakkaac_length_drift_verses")
            or hakkaac.get("length_drift_verses")
        ),
        "split_source_role_rows": int_or_zero(split.get("role_rows")),
        "split_source_blocker_rows": int_or_zero(split.get("blocker_rows")),
        "fresh_terms_ready": truthy(next_result.get("fresh_terms_ready")),
        "leakage_audit_ready": truthy(next_result.get("leakage_audit_ready")),
        "fixed_controls_ready": truthy(next_result.get("fixed_controls_ready")),
        "study_lock_ready": truthy(next_result.get("study_lock_ready")),
        "claim_status": CLAIM_BOUNDARY,
    }


def build_status_rows(
    summary: dict[str, Any], inputs: LoadedInputs, args: argparse.Namespace
) -> list[dict[str, str]]:
    gates = {row.get("gate_id", ""): row for row in inputs.next_result_gates}
    blockers = {row.get("blocker_id", ""): row for row in inputs.source_policy_blockers}
    return [
        status_row(
            "current_rerun_baseline",
            "current eBible KJVA rerun baseline",
            "rerun_only_ready",
            (
                f"current rerun locked {int(bool(summary['current_rerun_locked']))}; "
                f"checksum records ready {summary['checksum_records_ready']}"
            ),
            "yes",
            "no",
            "keep current-source reruns separate from independent replication",
            "rerun baseline is not independent KJVA replication",
            args.current_source_summary,
        ),
        status_row(
            "completed_prospective_lane",
            "completed KJVA prospective bridge lane",
            "review_material_only",
            (
                f"{summary['completed_lane_terms']} terms; "
                f"observed bridge rows {summary['completed_lane_observed_bridge_rows']}; "
                f"significant terms {summary['completed_lane_significant_terms']}; "
                "non-Bible controls at or above observed "
                f"{summary['nonbible_controls_at_or_above_observed']}"
            ),
            "yes",
            "yes",
            gates.get("completed_lane_claim_gate", {}).get(
                "next_action", "keep completed lane as review material only"
            ),
            "completed negative lane cannot be reused as new claim evidence",
            args.prospective_term_summary,
        ),
        status_row(
            "source_policy_lock",
            "source policy",
            "blocked",
            (
                f"{summary['policy_option_rows']} options; "
                f"{summary['policy_ready_options']} policy-ready; "
                f"{summary['blocked_options']} blocked; "
                f"{summary['source_policy_blocker_rows']} blocker rows"
            ),
            "yes",
            "yes",
            gates.get("source_policy_lock", {}).get(
                "next_action", "close source-use and source-role blockers first"
            ),
            "source-use policy must authorize any result-bearing source",
            args.source_policy_summary,
        ),
        status_row(
            "source_text_lock",
            "source text",
            "blocked",
            (
                f"source-use ready pages {summary['source_use_ready_pages']}; "
                f"source-lock ready {int(bool(summary['source_lock_ready']))}"
            ),
            "yes",
            "yes",
            gates.get("source_text_lock", {}).get(
                "next_action", "do not import or substitute source text silently"
            ),
            "no independent KJVA source text is locked for result-bearing use",
            args.source_policy_blockers,
        ),
        status_row(
            "verse_map_collation_lock",
            "verse map and collation",
            "blocked",
            (
                f"Hakkaac exact verses {summary['hakkaac_exact_normalized_verse_matches']}/"
                f"{summary['hakkaac_total_verses']}; "
                f"length-drift verses {summary['hakkaac_length_drift_verses']}"
            ),
            "yes",
            "yes",
            gates.get("verse_map_collation_lock", {}).get(
                "next_action", "finish source mapping before any run"
            ),
            "candidate collation evidence is not a selected-source verse map",
            args.hakkaac_collation_summary,
        ),
        status_row(
            "drift_boundary_lock",
            "drift and boundary",
            "blocked",
            (
                f"Sirach gap {summary['gutenberg_sirach_gap_refs']}; "
                f"Prayer of Manasseh markers "
                f"{summary['gutenberg_manasseh_source_markers']}/"
                f"{summary['gutenberg_manasseh_local_markers']}; "
                f"Hakkaac drift verses {summary['hakkaac_length_drift_verses']}"
            ),
            "yes",
            "yes",
            blockers.get("hakkaac_sirach_19_1_length_drift", {}).get(
                "required_before_result",
                "lock Sirach, Prayer of Manasseh, and drift policies before output",
            ),
            "do not patch, exclude, or split without citable policy",
            args.gutenberg_blocker_summary,
        ),
        status_row(
            "fresh_terms_leakage_controls",
            "fresh terms, leakage audit, and fixed controls",
            "blocked",
            (
                f"fresh terms ready {int(bool(summary['fresh_terms_ready']))}; "
                f"leakage audit ready {int(bool(summary['leakage_audit_ready']))}; "
                f"fixed controls ready {int(bool(summary['fixed_controls_ready']))}"
            ),
            "yes",
            "yes",
            gates.get("fresh_term_lock", {}).get(
                "next_action", "preregister fresh terms before new output"
            ),
            "new KJVA result needs terms and controls locked before seeing output",
            args.next_result_gates,
        ),
        status_row(
            "study_lock_manifest",
            "study lock",
            "blocked",
            (
                f"study-lock ready {int(bool(summary['study_lock_ready']))}; "
                f"split-source role rows {summary['split_source_role_rows']}; "
                f"split-source blockers {summary['split_source_blocker_rows']}"
            ),
            "yes",
            "yes",
            gates.get("study_lock_manifest", {}).get(
                "next_action", "write study lock only after source and study gates pass"
            ),
            "role sidecar alone never authorizes result-bearing output",
            args.split_role_summary,
        ),
        status_row(
            "result_permission",
            "result permission",
            "blocked",
            f"result allowed {int(bool(summary['result_allowed']))}",
            "yes",
            "yes",
            gates.get("result_allowed", {}).get(
                "next_action", "wait until all source and study gates pass"
            ),
            "new independent KJVA result-bearing output is not allowed",
            args.next_result_summary,
        ),
    ]


def write_markdown(
    path: Path, summary: dict[str, Any], rows: list[dict[str, str]]
) -> None:
    lines = [
        "# KJVA No-Input Handoff Status",
        "",
        "Status: consolidated KJVA no-input handoff.",
        "",
        "This is not an ELS result, not a corpus import, not a source-use approval, not a source lock, not a term lock, not a study lock, and not a new KJVA result.",
        "It gathers the current KJVA source-candidate, source-policy, collation, prospective-lane, and next-result gate status into one guarded handoff.",
        "It exists so the next work item starts from one status file without re-reading the whole KJVA packet chain.",
        "",
        "## Summary",
        "",
        f"- Status rows: {summary['status_rows']}.",
        f"- Handoff-ready rows: {summary['handoff_ready_rows']}.",
        f"- Manual-input-needed rows: {summary['manual_input_needed_rows']}.",
        f"- Gate rows: {summary['gate_rows']}.",
        f"- Rerun-only ready rows: {summary['rerun_only_ready_rows']}.",
        f"- Blocked gate rows: {summary['blocked_gate_rows']}.",
        f"- Source-policy blocker rows: {summary['source_policy_blocker_rows']}.",
        f"- Policy options: {summary['policy_option_rows']}.",
        f"- Policy-ready options: {summary['policy_ready_options']}.",
        f"- Blocked options: {summary['blocked_options']}.",
        f"- Checksum records ready: {summary['checksum_records_ready']}.",
        f"- Current rerun locked: {int(bool(summary['current_rerun_locked']))}.",
        f"- Source-use ready pages: {summary['source_use_ready_pages']}.",
        f"- Source-lock ready: {int(bool(summary['source_lock_ready']))}.",
        f"- Result allowed: {int(bool(summary['result_allowed']))}.",
        f"- Completed lane terms: {summary['completed_lane_terms']}.",
        f"- Completed lane observed bridge rows: {summary['completed_lane_observed_bridge_rows']}.",
        f"- Completed lane significant terms: {summary['completed_lane_significant_terms']}.",
        f"- Non-Bible controls at or above observed: {summary['nonbible_controls_at_or_above_observed']}.",
        f"- Gutenberg Sirach gap refs: `{summary['gutenberg_sirach_gap_refs']}`.",
        f"- Gutenberg Prayer of Manasseh markers: {summary['gutenberg_manasseh_source_markers']}/{summary['gutenberg_manasseh_local_markers']}.",
        f"- Hakkaac exact normalized verse matches: {summary['hakkaac_exact_normalized_verse_matches']}/{summary['hakkaac_total_verses']}.",
        f"- Hakkaac length-drift verses: {summary['hakkaac_length_drift_verses']}.",
        f"- Split-source role rows: {summary['split_source_role_rows']}.",
        f"- Split-source blocker rows: {summary['split_source_blocker_rows']}.",
        f"- Fresh terms ready: {int(bool(summary['fresh_terms_ready']))}.",
        f"- Leakage audit ready: {int(bool(summary['leakage_audit_ready']))}.",
        f"- Fixed controls ready: {int(bool(summary['fixed_controls_ready']))}.",
        f"- Study-lock ready: {int(bool(summary['study_lock_ready']))}.",
        f"- Claim status: `{summary['claim_status']}`.",
        "",
        "## Handoff Rows",
        "",
        "| Status id | Area | Status | Value | Manual input | Boundary |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['status_id']}` | {row['area']} | `{row['current_status']}` | {row['current_value']} | `{row['manual_input_needed']}` | {row['boundary']} |"
        )
    lines.extend(
        [
            "",
            "## Next Work",
            "",
            "The no-input path can keep source-candidate packets aligned, rebuild guard documents, and keep current-source reruns reproducible.",
            "It cannot approve source use, choose a final text stream, patch drift rows, create fresh terms, clear leakage, lock controls, or authorize a new KJVA result.",
            "The next result-bearing KJVA run remains blocked until the manual-input rows are resolved and a study-lock manifest exists.",
            "",
            "## Cautions",
            "",
            "- This handoff is a map of remaining work, not a new statistical result.",
            "- Current eBible KJVA remains a rerun baseline only, not an independent replication source.",
            "- Candidate-source metadata, marker coverage, and ignored-local collation are evidence lanes, not source locks.",
            "- Do not treat `SIR 44:23`, Prayer of Manasseh, or `SIR 19:1` as corrected until citable policy is locked.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    summary: dict[str, Any],
    rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "els_version": __version__,
        "tool": "scripts.build_kjva_no_input_handoff_status",
        "claim_boundary": "KJVA no-input handoff only; no new result",
        "text_retention": "no Bible text written to tracked outputs",
        "summary": summary,
        "status_rows": len(rows),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "inputs": {
            "next_result_summary": str(args.next_result_summary),
            "next_result_gates": str(args.next_result_gates),
            "source_policy_summary": str(args.source_policy_summary),
            "source_policy_blockers": str(args.source_policy_blockers),
            "current_source_summary": str(args.current_source_summary),
            "gutenberg_blocker_summary": str(args.gutenberg_blocker_summary),
            "hakkaac_collation_summary": str(args.hakkaac_collation_summary),
            "split_role_summary": str(args.split_role_summary),
            "prospective_term_summary": str(args.prospective_term_summary),
            "prospective_nonbible_summary": str(args.prospective_nonbible_summary),
        },
        "outputs": {
            "status": str(args.out),
            "summary": str(args.summary_out),
            "markdown": str(args.markdown_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def status_row(
    status_id: str,
    area: str,
    current_status: str,
    current_value: str,
    handoff_ready: str,
    manual_input_needed: str,
    next_action: str,
    boundary: str,
    source: Path,
) -> dict[str, str]:
    return {
        "status_id": status_id,
        "area": area,
        "current_status": current_status,
        "current_value": current_value,
        "handoff_ready": handoff_ready,
        "manual_input_needed": manual_input_needed,
        "next_action": next_action,
        "boundary": boundary,
        "source": str(source),
    }


def first_row(rows: list[dict[str, str]]) -> dict[str, str]:
    return rows[0] if rows else {}


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def int_or_zero(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
