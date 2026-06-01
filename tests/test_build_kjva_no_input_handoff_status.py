import csv
import json
from pathlib import Path

from scripts import build_kjva_no_input_handoff_status as handoff


def test_build_summary_consolidates_current_kjva_blockers() -> None:
    summary = handoff.build_summary(_inputs())

    assert summary["gate_rows"] == 11
    assert summary["blocked_gate_rows"] == 10
    assert summary["source_policy_blocker_rows"] == 7
    assert summary["policy_option_rows"] == 5
    assert summary["policy_ready_options"] == 2
    assert summary["blocked_options"] == 3
    assert summary["checksum_records_ready"] == 2
    assert summary["current_rerun_locked"] is True
    assert summary["source_use_ready_pages"] == 0
    assert summary["source_lock_ready"] is False
    assert summary["result_allowed"] is False
    assert summary["completed_lane_terms"] == 7
    assert summary["completed_lane_observed_bridge_rows"] == 1
    assert summary["completed_lane_significant_terms"] == 0
    assert summary["nonbible_controls_at_or_above_observed"] == 1
    assert summary["gutenberg_sirach_gap_refs"] == "SIR 44:23"
    assert summary["gutenberg_manasseh_source_markers"] == 0
    assert summary["gutenberg_manasseh_local_markers"] == 15
    assert summary["hakkaac_exact_normalized_verse_matches"] == 5719
    assert summary["hakkaac_total_verses"] == 5720
    assert summary["hakkaac_length_drift_verses"] == 1
    assert summary["split_source_role_rows"] == 7
    assert summary["split_source_blocker_rows"] == 6


def test_build_status_rows_keep_boundaries_visible() -> None:
    args = handoff.build_parser().parse_args([])
    summary = handoff.build_summary(_inputs())
    rows = handoff.build_status_rows(summary, _inputs(), args)

    by_id = {row["status_id"]: row for row in rows}
    assert len(rows) == 9
    assert by_id["current_rerun_baseline"]["manual_input_needed"] == "no"
    assert by_id["result_permission"]["current_status"] == "blocked"
    assert "not independent KJVA replication" in by_id["current_rerun_baseline"]["boundary"]
    assert "not allowed" in by_id["result_permission"]["boundary"]
    assert sum(row["manual_input_needed"] == "yes" for row in rows) == 8


def test_main_writes_csv_markdown_and_manifest(tmp_path: Path) -> None:
    paths = _write_inputs(tmp_path)
    out = tmp_path / "status.csv"
    summary = tmp_path / "summary.csv"
    markdown = tmp_path / "handoff.md"
    manifest = tmp_path / "manifest.json"

    code = handoff.main(
        [
            "--next-result-summary",
            str(paths["next_result_summary"]),
            "--next-result-gates",
            str(paths["next_result_gates"]),
            "--source-policy-summary",
            str(paths["source_policy_summary"]),
            "--source-policy-blockers",
            str(paths["source_policy_blockers"]),
            "--current-source-summary",
            str(paths["current_source_summary"]),
            "--gutenberg-blocker-summary",
            str(paths["gutenberg_blocker_summary"]),
            "--hakkaac-collation-summary",
            str(paths["hakkaac_collation_summary"]),
            "--split-role-summary",
            str(paths["split_role_summary"]),
            "--prospective-term-summary",
            str(paths["prospective_term_summary"]),
            "--prospective-nonbible-summary",
            str(paths["prospective_nonbible_summary"]),
            "--out",
            str(out),
            "--summary-out",
            str(summary),
            "--markdown-out",
            str(markdown),
            "--manifest-out",
            str(manifest),
        ]
    )

    assert code == 0
    rows = list(csv.DictReader(out.open(encoding="utf-8", newline="")))
    assert rows[0]["status_id"] == "current_rerun_baseline"
    summary_rows = list(csv.DictReader(summary.open(encoding="utf-8", newline="")))
    assert summary_rows[0]["claim_status"] == handoff.CLAIM_BOUNDARY
    text = markdown.read_text(encoding="utf-8")
    assert "Status: consolidated KJVA no-input handoff." in text
    assert "Result allowed: 0." in text
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["tool"] == "scripts.build_kjva_no_input_handoff_status"
    assert payload["status_rows"] == 9


def _inputs() -> handoff.LoadedInputs:
    return handoff.LoadedInputs(
        next_result_summary=[
            {
                "gate_rows": "11",
                "rerun_only_ready_rows": "1",
                "blocked_rows": "10",
                "source_policy_blocker_rows": "7",
                "completed_lane_terms": "7",
                "completed_lane_observed_bridge_rows": "1",
                "completed_lane_significant_terms": "0",
                "nonbible_controls_at_or_above_observed": "1",
                "source_lock_ready": "False",
                "fresh_terms_ready": "False",
                "leakage_audit_ready": "False",
                "fixed_controls_ready": "False",
                "study_lock_ready": "False",
                "result_allowed": "False",
            }
        ],
        next_result_gates=[
            _gate("completed_lane_claim_gate"),
            _gate("source_policy_lock"),
            _gate("source_text_lock"),
            _gate("verse_map_collation_lock"),
            _gate("fresh_term_lock"),
            _gate("study_lock_manifest"),
            _gate("result_allowed"),
        ],
        source_policy_summary=[
            {
                "policy_option_rows": "5",
                "blocker_rows": "7",
                "policy_ready_options": "2",
                "blocked_options": "3",
                "checksum_records_ready": "2",
                "source_use_ready_pages": "0",
                "gutenberg_sirach_gap_refs": "SIR 44:23",
                "gutenberg_manasseh_source_markers": "0",
                "gutenberg_manasseh_local_markers": "15",
                "hakkaac_length_drift_verses": "1",
            }
        ],
        source_policy_blockers=[
            {
                "blocker_id": "hakkaac_sirach_19_1_length_drift",
                "required_before_result": "lock drift policy before output",
            }
        ],
        current_source_summary=[{"rerun_baseline_locked": "True"}],
        gutenberg_blocker_summary=[
            {
                "sirach_gap_refs": "SIR 44:23",
                "manasseh_source_markers": "0",
                "manasseh_local_markers": "15",
            }
        ],
        hakkaac_collation_summary=[
            {
                "local_verses": "5720",
                "exact_normalized_verse_matches": "5719",
                "length_drift_verses": "1",
            }
        ],
        split_role_summary=[{"role_rows": "7", "blocker_rows": "6"}],
        prospective_term_summary=[{"normalized_term": f"t{i}"} for i in range(7)],
        prospective_nonbible_summary=[{"normalized_term": "tobit", "bridge_rows": "1"}],
    )


def _gate(gate_id: str) -> dict[str, str]:
    return {
        "gate_id": gate_id,
        "next_action": f"next action for {gate_id}",
        "required_before_result": f"required before {gate_id}",
    }


def _write_inputs(tmp_path: Path) -> dict[str, Path]:
    inputs = _inputs()
    paths = {
        "next_result_summary": tmp_path / "next_result_summary.csv",
        "next_result_gates": tmp_path / "next_result_gates.csv",
        "source_policy_summary": tmp_path / "source_policy_summary.csv",
        "source_policy_blockers": tmp_path / "source_policy_blockers.csv",
        "current_source_summary": tmp_path / "current_source_summary.csv",
        "gutenberg_blocker_summary": tmp_path / "gutenberg_blocker_summary.csv",
        "hakkaac_collation_summary": tmp_path / "hakkaac_collation_summary.csv",
        "split_role_summary": tmp_path / "split_role_summary.csv",
        "prospective_term_summary": tmp_path / "prospective_term_summary.csv",
        "prospective_nonbible_summary": tmp_path / "prospective_nonbible_summary.csv",
    }
    _write_csv(
        paths["next_result_summary"],
        list(inputs.next_result_summary[0]),
        inputs.next_result_summary,
    )
    _write_csv(paths["next_result_gates"], list(inputs.next_result_gates[0]), inputs.next_result_gates)
    _write_csv(
        paths["source_policy_summary"],
        list(inputs.source_policy_summary[0]),
        inputs.source_policy_summary,
    )
    _write_csv(
        paths["source_policy_blockers"],
        list(inputs.source_policy_blockers[0]),
        inputs.source_policy_blockers,
    )
    _write_csv(
        paths["current_source_summary"],
        list(inputs.current_source_summary[0]),
        inputs.current_source_summary,
    )
    _write_csv(
        paths["gutenberg_blocker_summary"],
        list(inputs.gutenberg_blocker_summary[0]),
        inputs.gutenberg_blocker_summary,
    )
    _write_csv(
        paths["hakkaac_collation_summary"],
        list(inputs.hakkaac_collation_summary[0]),
        inputs.hakkaac_collation_summary,
    )
    _write_csv(paths["split_role_summary"], list(inputs.split_role_summary[0]), inputs.split_role_summary)
    _write_csv(
        paths["prospective_term_summary"],
        list(inputs.prospective_term_summary[0]),
        inputs.prospective_term_summary,
    )
    _write_csv(
        paths["prospective_nonbible_summary"],
        list(inputs.prospective_nonbible_summary[0]),
        inputs.prospective_nonbible_summary,
    )
    return paths


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
