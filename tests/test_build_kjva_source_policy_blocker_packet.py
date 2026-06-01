from scripts import build_kjva_source_policy_blocker_packet as packet


def _current_summary() -> dict[str, str]:
    return {
        "rerun_baseline_locked": "True",
        "book_count": "80",
        "verse_count": "37072",
    }


def _checksum_summary() -> dict[str, str]:
    return {
        "checksum_records_ready": "2",
        "source_use_ready_pages": "0",
    }


def _gutenberg_blocker_summary() -> dict[str, str]:
    return {
        "sirach_gap_refs": "SIR 44:23",
        "sirach_missing_source_marker_count": "1",
        "manasseh_source_markers": "0",
        "manasseh_local_markers": "15",
    }


def _hakkaac_summary() -> dict[str, str]:
    return {
        "exact_normalized_verse_matches": "5719",
        "total_verses": "5720",
        "marker_books_exact": "14",
        "length_drift_verses": "1",
        "exact_book_stream_matches": "13",
    }


def _split_role_summary() -> dict[str, str]:
    return {
        "split_source_role_sidecar_written": "True",
        "role_rows": "7",
        "blocker_rows": "6",
    }


def test_build_policy_options_marks_only_current_and_deferral_ready() -> None:
    options = packet.build_policy_options(
        _current_summary(),
        _checksum_summary(),
        _gutenberg_blocker_summary(),
        _hakkaac_summary(),
        _split_role_summary(),
    )

    assert len(options) == 5
    by_id = {row["option_id"]: row for row in options}
    assert by_id["current_ebible_rerun_only"]["status"] == "policy_ready"
    assert by_id["defer_new_kjva_replication"]["status"] == "policy_ready"
    assert by_id["project_gutenberg_only_candidate"]["status"] == "blocked"
    assert by_id["project_gutenberg_hakkaac_split_candidate"]["status"] == "blocked"
    assert by_id["hakkaac_primary_stream"]["status"] == "blocked"
    assert {row["result_boundary"] for row in options} == {"not_result_bearing"}


def test_build_blockers_keeps_source_and_study_locks_blocked() -> None:
    blockers = packet.build_blockers(
        _checksum_summary(),
        _gutenberg_blocker_summary(),
        _hakkaac_summary(),
        _split_role_summary(),
    )

    ids = {row["blocker_id"] for row in blockers}
    assert "source_use_policy_lock" in ids
    assert "term_control_study_lock" in ids
    assert "role_sidecar_complete_but_not_sufficient" in ids
    assert len(blockers) == 7
    assert {row["result_boundary"] for row in blockers} == {"not_result_bearing"}


def test_build_summary_remains_not_result_ready() -> None:
    options = packet.build_policy_options(
        _current_summary(),
        _checksum_summary(),
        _gutenberg_blocker_summary(),
        _hakkaac_summary(),
        _split_role_summary(),
    )
    blockers = packet.build_blockers(
        _checksum_summary(),
        _gutenberg_blocker_summary(),
        _hakkaac_summary(),
        _split_role_summary(),
    )
    summary = packet.build_summary(
        options,
        blockers,
        _current_summary(),
        _checksum_summary(),
        _gutenberg_blocker_summary(),
        _hakkaac_summary(),
        _split_role_summary(),
    )

    assert summary["policy_option_rows"] == 5
    assert summary["blocker_rows"] == 7
    assert summary["policy_ready_options"] == 2
    assert summary["blocked_options"] == 3
    assert summary["source_lock_ready"] is False
    assert summary["result_ready"] is False
    assert summary["claim_status"] == "source_policy_blocker_packet_only_not_result_bearing"
