from collections import OrderedDict

from scripts import build_kjva_gutenberg_source_lock_decision_packet as packet


def test_build_decisions_records_blockers_and_recommendations() -> None:
    prep_rows = [
        {
            "book": "SIR",
            "gutenberg_marker_count": "1392",
            "local_kjva_verse_count": "1393",
            "delta": "-1",
        },
        {
            "book": "MAN",
            "gutenberg_marker_count": "0",
            "local_kjva_verse_count": "15",
            "delta": "-15",
        },
        {
            "book": "BAR",
            "gutenberg_marker_count": "213",
            "local_kjva_verse_count": "213",
            "delta": "0",
        },
        {
            "book": "LJE_SOURCE",
            "gutenberg_marker_count": "73",
            "local_kjva_verse_count": "",
            "delta": "",
        },
    ]
    prep_summary = {
        "raw_text_retained": "False",
        "kjv_books_exact_count_matches": "66",
        "kjv_books_compared": "66",
        "apocrypha_books_exact_count_matches": "12",
        "apocrypha_books_compared": "14",
    }

    decisions = packet.build_decisions(prep_rows, prep_summary, ["TOB", "SIR", "BAR"])
    by_id = {row["decision_id"]: row for row in decisions}

    assert len(decisions) == 10
    assert by_id["book_order"]["recommendation"].startswith("Use Gutenberg source order")
    assert by_id["baruch_epistle"]["recommendation"].startswith("Roll the separate")
    assert by_id["sirach_count_drift"]["lock_status"] == "blocked"
    assert by_id["prayer_count_drift"]["lock_status"] == "blocked"
    assert by_id["result_boundary"]["result_boundary"] == "not_result_bearing"


def test_build_summary_keeps_packet_non_result_bearing() -> None:
    decisions = [
        packet.decision("a", "area", "evidence", "rec", "policy_ready", "", "next"),
        packet.decision("b", "area", "evidence", "rec", "recommended_policy_not_locked", "blocker", "next"),
        packet.decision("c", "area", "evidence", "rec", "blocked", "blocker", "next"),
        packet.decision("d", "area", "evidence", "rec", "candidate_not_locked", "blocker", "next"),
    ]

    summary = packet.build_summary(decisions, ["TOB", "BAR"])

    assert summary["decision_rows"] == 4
    assert summary["policy_ready_rows"] == 1
    assert summary["recommended_policy_rows"] == 1
    assert summary["blocked_rows"] == 1
    assert summary["candidate_not_locked_rows"] == 1
    assert summary["source_lock_ready"] is False
    assert summary["result_ready"] is False
    assert summary["claim_status"] == "decision_packet_only_not_result_bearing"


def test_local_apocrypha_order_preserves_first_seen_order(tmp_path) -> None:
    csv_path = tmp_path / "kjva.csv"
    csv_path.write_text(
        "ref,book,chapter,verse,text\n"
        "Tobit 1:1,TOB,1,1,x\n"
        "Tobit 1:2,TOB,1,2,x\n"
        "Baruch 1:1,BAR,1,1,x\n"
        "Genesis 1:1,GEN,1,1,x\n"
        "Sirach 1:1,SIR,1,1,x\n",
        encoding="utf-8",
    )

    assert packet.local_apocrypha_order(csv_path) == ["TOB", "BAR", "SIR"]
