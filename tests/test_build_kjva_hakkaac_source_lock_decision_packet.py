from scripts import build_kjva_hakkaac_source_lock_decision_packet as packet


def test_build_decisions_records_boundaries_and_drift() -> None:
    collation = {
        "private_text_path": "data/private/hakkaac_kjva_apocrypha/verses.csv",
        "exact_normalized_verse_matches": "5719",
        "comparable_refs": "5720",
    }
    marker_summary = {"exact_book_marker_matches": "14", "local_books_compared": "14"}
    blocker_rows = [{"status": "exact_normalized_match"} for _ in range(16)]
    drift_rows = [
        {
            "ref": "SIR 19:1",
            "status": "length_drift",
            "local_norm_len": "107",
            "hakkaac_norm_len": "108",
            "norm_len_delta": "1",
        }
    ]

    decisions = packet.build_decisions(
        collation,
        marker_summary,
        blocker_rows,
        drift_rows,
    )
    by_id = {row["decision_id"]: row for row in decisions}

    assert len(decisions) == 9
    assert by_id["source_use_boundary"]["lock_status"] == "candidate_not_locked"
    assert by_id["gutenberg_blocker_rows"]["lock_status"] == "recommended_policy_not_locked"
    assert by_id["sirach_19_1_drift"]["lock_status"] == "blocked"
    assert "SIR 19:1" in by_id["sirach_19_1_drift"]["current_evidence"]
    assert by_id["result_boundary"]["result_boundary"] == "not_result_bearing"


def test_build_drift_rows_keeps_only_non_exact_rows() -> None:
    rows = [
        {"ref": "TOB 1:1", "status": "exact_normalized_match"},
        {
            "ref": "SIR 19:1",
            "book": "SIR",
            "status": "length_drift",
            "local_norm_len": "107",
            "hakkaac_norm_len": "108",
            "norm_len_delta": "1",
            "first_diff_offset": "17",
        },
    ]

    drift_rows = packet.build_drift_rows(rows)

    assert len(drift_rows) == 1
    assert drift_rows[0]["ref"] == "SIR 19:1"
    assert drift_rows[0]["recommendation"] == "keep_named_drift_until_source_policy_lock"


def test_build_summary_keeps_packet_non_result_bearing() -> None:
    decisions = [
        packet.decision("a", "area", "evidence", "rec", "policy_ready", "", "next"),
        packet.decision("b", "area", "evidence", "rec", "recommended_policy_not_locked", "blocker", "next"),
        packet.decision("c", "area", "evidence", "rec", "blocked", "blocker", "next"),
        packet.decision("d", "area", "evidence", "rec", "candidate_not_locked", "blocker", "next"),
    ]
    collation = {
        "local_verses": "5720",
        "exact_normalized_verse_matches": "5719",
        "length_drift_verses": "1",
        "exact_book_stream_matches": "13",
        "book_stream_drift_books": "1",
    }
    marker_summary = {"exact_book_marker_matches": "14"}
    blocker_rows = [{"status": "exact_normalized_match"} for _ in range(16)]

    summary = packet.build_summary(decisions, collation, marker_summary, blocker_rows)

    assert summary["decision_rows"] == 4
    assert summary["policy_ready_rows"] == 1
    assert summary["recommended_policy_rows"] == 1
    assert summary["blocked_rows"] == 1
    assert summary["candidate_not_locked_rows"] == 1
    assert summary["blocker_rows_exact"] == 16
    assert summary["source_lock_ready"] is False
    assert summary["result_ready"] is False
    assert summary["claim_status"] == "decision_packet_only_not_result_bearing"
