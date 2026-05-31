import csv
from pathlib import Path

from scripts import check_kjva_gutenberg_source_lock_decision_packet_doc as check


def test_current_kjva_gutenberg_source_lock_decision_packet_doc_passes() -> None:
    assert check.validate_kjva_gutenberg_source_lock_decision_packet_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    missing = tmp_path / "missing.md"

    failures = check.validate_kjva_gutenberg_source_lock_decision_packet_doc(missing)

    assert failures == [f"{missing} is missing"]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8").replace(
        "Decision rows: 10.",
        "Decision rows: unknown.",
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_kjva_gutenberg_source_lock_decision_packet_doc(
        doc,
        decisions=None,
        summary=None,
        manifest=None,
    )

    assert any("missing phrase" in failure for failure in failures)


def test_summary_status_drift_fails(tmp_path: Path) -> None:
    summary = tmp_path / "summary.csv"
    row = {
        "decision_rows": "10",
        "policy_ready_rows": "2",
        "recommended_policy_rows": "3",
        "blocked_rows": "3",
        "candidate_not_locked_rows": "2",
        "local_apocrypha_order": "TOB;JDT;ESG;WIS;SIR;BAR;S3Y;SUS;BEL;1MA;2MA;1ES;MAN;2ES",
        "gutenberg_apocrypha_order": "1ES;2ES;TOB;JDT;ESG;WIS;SIR;BAR;LJE_SOURCE;S3Y;SUS;BEL;MAN;1MA;2MA",
        "order_recommendation": "use_gutenberg_source_order_for_independent_replication",
        "baruch_epistle_recommendation": "roll_lje_source_into_bar_with_component_metadata",
        "sirach_blocker": "one_source_marker_short_needs_collation",
        "prayer_blocker": "unmarked_prose_needs_verse_boundary_policy",
        "source_lock_ready": "False",
        "result_ready": "False",
        "claim_status": "decision_packet_only_not_result_bearing",
    }
    with summary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=check.packet.SUMMARY_FIELDNAMES)
        writer.writeheader()
        writer.writerow(row)

    failures = check.validate_summary_csv(summary)

    assert any("blocked_rows drifted" in failure for failure in failures)
    assert any("candidate_not_locked_rows drifted" in failure for failure in failures)
