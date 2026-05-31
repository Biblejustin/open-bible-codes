from pathlib import Path

from scripts import check_kjva_crosswire_candidate_source_audit_doc as check


def test_current_kjva_crosswire_source_audit_doc_passes() -> None:
    assert check.validate_kjva_crosswire_candidate_source_audit_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    missing = tmp_path / "missing.md"

    failures = check.validate_kjva_crosswire_candidate_source_audit_doc(missing)

    assert failures == [f"{missing} is missing"]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8").replace(
        "Possible independent KJVA metadata candidates: 1.",
        "Possible independent KJVA metadata candidates: unknown.",
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_kjva_crosswire_candidate_source_audit_doc(
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
        + "crosswire_gitlab_kjva_osis,"
        + check.analyzer.PROJECT_WEB_URL
        + ",fetched,fetched,fetched,master,9,"
        + "README.md;kjv.osis.xml;kjva.osis.xml;kjvdc.xml,"
        + "True,False,True,True,True,True,sha,100,True,True,True,"
        + "source_candidate_not_confirmed,False,not_source_lock_ready,not_result_ready\n",
        encoding="utf-8",
    )

    failures = check.validate_rows_csv(rows)

    assert any("kjva_osis_path_present drifted" in failure for failure in failures)
    assert any("source_audit_status drifted" in failure for failure in failures)
