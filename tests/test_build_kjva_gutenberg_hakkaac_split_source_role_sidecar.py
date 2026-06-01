from scripts import build_kjva_gutenberg_hakkaac_split_source_role_sidecar as sidecar


def _current_summary() -> dict[str, str]:
    return {
        "rerun_baseline_locked": "True",
        "apocrypha_book_count": "14",
        "apocrypha_verse_count": "5720",
        "csv_sha256": "a" * 64,
    }


def _gutenberg_summary() -> dict[str, str]:
    return {
        "local_apocrypha_order": "TOB;JDT",
        "gutenberg_apocrypha_order": "1ES;2ES",
        "order_recommendation": "use_gutenberg_source_order_for_independent_replication",
        "baruch_epistle_recommendation": "roll_lje_source_into_bar_with_component_metadata",
    }


def _blocker_summary() -> dict[str, str]:
    return {
        "sirach_gap_refs": "SIR 44:23",
        "manasseh_source_markers": "0",
        "manasseh_local_markers": "15",
    }


def _hakkaac_summary() -> dict[str, str]:
    return {
        "marker_books_exact": "14",
        "exact_normalized_verse_matches": "5719",
        "total_verses": "5720",
        "length_drift_verses": "1",
        "blocker_rows_exact": "16",
    }


def test_build_roles_keeps_hakkaac_witness_only() -> None:
    roles = sidecar.build_roles(
        _current_summary(),
        _gutenberg_summary(),
        _blocker_summary(),
        _hakkaac_summary(),
    )

    assert len(roles) == 7
    by_id = {row["role_id"]: row for row in roles}
    assert by_id["current_ebible_rerun_baseline"]["lock_status"] == "policy_ready"
    assert by_id["hakkaac_marker_collation_witness"]["source_role"] == (
        "marker_and_collation_witness_only"
    )
    assert by_id["hakkaac_marker_collation_witness"]["lock_status"] == (
        "candidate_not_locked"
    )
    assert by_id["split_stream_boundary"]["result_boundary"] == "not_result_bearing"


def test_build_blockers_names_letter_stream_blockers() -> None:
    blockers = sidecar.build_blockers(
        _blocker_summary(),
        [{"option_id": "manasseh_defer_until_citable_marked_source"}],
        [{"local_ref": "SIR 44:23"}],
        _hakkaac_summary(),
        [{"ref": "SIR 19:1"}],
        [
            {
                "decision_id": "source_use_boundary",
                "blocker": "candidate only",
            },
            {
                "decision_id": "split_source_policy",
                "blocker": "split source needs policy",
            },
        ],
        [
            {
                "decision_id": "source_stream",
                "blocker": "needs source lock",
            }
        ],
    )

    ids = {row["blocker_id"] for row in blockers}
    assert "sirach_44_23_gutenberg_marker_gap" in ids
    assert "sirach_19_1_hakkaac_length_drift" in ids
    assert all(row["affects_letter_stream"] for row in blockers)


def test_build_summary_is_not_result_ready() -> None:
    roles = sidecar.build_roles(
        _current_summary(),
        _gutenberg_summary(),
        _blocker_summary(),
        _hakkaac_summary(),
    )
    blockers = sidecar.build_blockers(
        _blocker_summary(),
        [],
        [],
        _hakkaac_summary(),
        [],
        [],
        [],
    )

    summary = sidecar.build_summary(
        roles,
        blockers,
        _current_summary(),
        _gutenberg_summary(),
        _blocker_summary(),
        _hakkaac_summary(),
    )

    assert summary["role_rows"] == 7
    assert summary["blocker_rows"] == 6
    assert summary["split_source_role_sidecar_written"] is True
    assert summary["source_lock_ready"] is False
    assert summary["result_ready"] is False
    assert summary["claim_status"] == "split_source_role_sidecar_only_not_result_bearing"
