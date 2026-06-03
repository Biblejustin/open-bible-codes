import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
from pathlib import Path

from scripts import check_kjva_hakkaac_apocrypha_boundary_candidate_doc as check


def test_current_hakkaac_boundary_candidate_doc_passes() -> None:
    assert check.validate_kjva_hakkaac_apocrypha_boundary_candidate_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    missing = tmp_path / "missing.md"

    failures = check.validate_kjva_hakkaac_apocrypha_boundary_candidate_doc(missing)

    assert failures == [f"{missing} is missing"]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8").replace(
        "Candidate resolves Sirach blocker: 1.",
        "Candidate resolves Sirach blocker: unknown.",
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_kjva_hakkaac_apocrypha_boundary_candidate_doc(
        doc,
        rows=None,
        summary=None,
        manifest=None,
    )

    assert any("missing phrase" in failure for failure in failures)


def test_rows_drift_fails(tmp_path: Path) -> None:
    rows_path = tmp_path / "rows.csv"
    rows = [
        {
            "page_id": "hakkaac_sirach_44",
            "source_url": "url",
            "source_status": "http_200",
            "bytes": "1",
            "sha256": "hash",
            "license_note_present": "True",
            "book": "SIR",
            "chapter": "44",
            "marker_count": "22",
            "markers_present": "1..22",
            "target_markers": "23",
            "target_status": "target_marker_missing",
            "candidate_status": "does_not_resolve_sirach_marker_gap",
            "notes": "",
        },
        {
            "page_id": "hakkaac_manasseh_1",
            "source_url": "url",
            "source_status": "http_200",
            "bytes": "1",
            "sha256": "hash",
            "license_note_present": "True",
            "book": "MAN",
            "chapter": "1",
            "marker_count": "15",
            "markers_present": "1..15",
            "target_markers": "1..15",
            "target_status": "all_target_markers_present",
            "candidate_status": "prayer_boundary_candidate_not_source_lock",
            "notes": "",
        },
    ]
    with rows_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=check.audit.ROW_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    failures = check.validate_rows_csv(rows_path)

    assert any("hakkaac_sirach_44 marker_count drifted" in failure for failure in failures)
    assert any("hakkaac_sirach_44 target_status drifted" in failure for failure in failures)


def test_summary_drift_fails(tmp_path: Path) -> None:
    summary_path = tmp_path / "summary.csv"
    row = {
        "pages_scanned": "2",
        "license_note_pages": "2",
        "sirach_44_marker_count": "22",
        "sirach_44_has_23": "False",
        "prayer_marker_count": "15",
        "prayer_has_1_to_15": "True",
        "candidate_resolves_sirach": "False",
        "candidate_resolves_prayer": "True",
        "source_lock_ready": "False",
        "result_ready": "False",
        "claim_status": "candidate_audit_only_not_result_bearing",
    }
    with summary_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=check.audit.SUMMARY_FIELDNAMES)
        writer.writeheader()
        writer.writerow(row)

    failures = check.validate_summary_csv(summary_path)

    assert any("sirach_44_marker_count drifted" in failure for failure in failures)
    assert any("candidate_resolves_sirach drifted" in failure for failure in failures)
