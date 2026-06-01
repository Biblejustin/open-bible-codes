from scripts import build_kjva_next_result_gate as gate


def _source_policy() -> dict[str, str]:
    return {
        "current_rerun_locked": "True",
        "checksum_records_ready": "2",
        "source_lock_ready": "False",
        "gutenberg_sirach_gap_refs": "SIR 44:23",
        "gutenberg_manasseh_source_markers": "0",
        "gutenberg_manasseh_local_markers": "15",
        "hakkaac_length_drift_verses": "1",
    }


def _source_blockers() -> list[dict[str, str]]:
    return [{"blocker_id": f"b{i}"} for i in range(7)]


def _term_summary() -> list[dict[str, str]]:
    return [
        {"observed_bridge_rows": "1", "q_ge": "0.680267"},
        *[{"observed_bridge_rows": "0", "q_ge": "1.0"} for _ in range(6)],
    ]


def _controls() -> list[dict[str, str]]:
    return [
        {"bridge_rows": "0"},
        {"bridge_rows": "0"},
        {"bridge_rows": "1"},
    ]


def test_build_gates_blocks_new_result_but_allows_rerun_only() -> None:
    gates = gate.build_gates(
        _source_policy(),
        _source_blockers(),
        _term_summary(),
        _controls(),
    )

    by_id = {row["gate_id"]: row for row in gates}
    assert len(gates) == 11
    assert by_id["current_rerun_reproducibility"]["status"] == "rerun_only_ready"
    assert by_id["result_allowed"]["status"] == "blocked"
    assert by_id["fresh_term_lock"]["status"] == "blocked"
    assert {row["result_boundary"] for row in gates} == {"not_result_bearing"}


def test_build_summary_records_completed_lane_and_closed_gate_counts() -> None:
    gates = gate.build_gates(
        _source_policy(),
        _source_blockers(),
        _term_summary(),
        _controls(),
    )
    summary = gate.build_summary(
        gates,
        _source_policy(),
        _source_blockers(),
        _term_summary(),
        _controls(),
    )

    assert summary["gate_rows"] == 11
    assert summary["rerun_only_ready_rows"] == 1
    assert summary["blocked_rows"] == 10
    assert summary["completed_lane_terms"] == 7
    assert summary["completed_lane_observed_bridge_rows"] == 1
    assert summary["completed_lane_significant_terms"] == 0
    assert summary["nonbible_controls_at_or_above_observed"] == 1
    assert summary["result_allowed"] is False
    assert summary["claim_status"] == "kjva_next_result_gate_blocks_new_output"
