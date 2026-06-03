import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

from pathlib import Path

from scripts import check_kjva_open_bibles_candidate_source_audit_doc as check


def test_current_kjva_open_bibles_source_audit_doc_passes() -> None:
    assert check.validate_kjva_open_bibles_candidate_source_audit_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    missing = tmp_path / "missing.md"

    failures = check.validate_kjva_open_bibles_candidate_source_audit_doc(missing)

    assert failures == [f"{missing} is missing"]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8").replace(
        "not a KJVA/apocrypha source candidate",
        "ready source candidate",
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_kjva_open_bibles_candidate_source_audit_doc(
        doc,
        rows=None,
        summary=None,
        anchors=None,
        manifest=None,
    )

    assert any("missing phrase" in failure for failure in failures)


def test_rows_status_drift_fails(tmp_path: Path) -> None:
    rows = tmp_path / "rows.csv"
    rows.write_text(
        ",".join(check.analyzer.ROW_FIELDNAMES)
        + "\n"
        + "seven1m_open_bibles_kjv_osis,"
        + check.analyzer.REPO_API
        + ",fetched,fetched,fetched,master,,52,False,24,1,eng-kjv.osis.xml,"
        + "1,0,sha,True,True,True,possible_kjva_candidate_needs_text_audit,"
        + "False,not_result_ready\n",
        encoding="utf-8",
    )

    failures = check.validate_rows_csv(rows)

    assert any("apocrypha_path_count drifted" in failure for failure in failures)
    assert any("source_audit_status drifted" in failure for failure in failures)
