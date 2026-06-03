import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
from pathlib import Path

from scripts import check_kjva_hakkaac_source_lock_decision_packet_doc as check


def test_current_kjva_hakkaac_source_lock_decision_packet_doc_passes() -> None:
    assert check.validate_kjva_hakkaac_source_lock_decision_packet_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    missing = tmp_path / "missing.md"

    failures = check.validate_kjva_hakkaac_source_lock_decision_packet_doc(missing)

    assert failures == [f"{missing} is missing"]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8").replace(
        "Decision rows: 9.",
        "Decision rows: unknown.",
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_kjva_hakkaac_source_lock_decision_packet_doc(
        doc,
        decisions=None,
        drift_rows=None,
        summary=None,
        manifest=None,
    )

    assert any("missing phrase" in failure for failure in failures)


def test_summary_status_drift_fails(tmp_path: Path) -> None:
    summary = tmp_path / "summary.csv"
    row = {
        "decision_rows": "9",
        "policy_ready_rows": "3",
        "recommended_policy_rows": "2",
        "blocked_rows": "2",
        "candidate_not_locked_rows": "2",
        "total_verses": "5720",
        "exact_normalized_verse_matches": "5719",
        "length_drift_verses": "1",
        "exact_book_stream_matches": "13",
        "book_stream_drift_books": "1",
        "blocker_rows_exact": "16",
        "marker_books_exact": "14",
        "source_policy_recommendation": "candidate_evidence_only_until_source_use_lock",
        "drift_recommendation": "keep_sir_19_1_named_drift_do_not_patch_automatically",
        "split_source_recommendation": "do_not_combine_gutenberg_and_hakkaac_without_sidecar",
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
