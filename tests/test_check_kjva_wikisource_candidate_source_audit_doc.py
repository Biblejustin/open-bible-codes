from pathlib import Path

from scripts import check_kjva_wikisource_candidate_source_audit_doc as check


def test_current_kjva_wikisource_source_audit_doc_passes() -> None:
    assert check.validate_kjva_wikisource_candidate_source_audit_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    missing = tmp_path / "missing.md"

    failures = check.validate_kjva_wikisource_candidate_source_audit_doc(missing)

    assert failures == [f"{missing} is missing"]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8").replace(
        "corpus import",
        "corpus path ready",
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_kjva_wikisource_candidate_source_audit_doc(
        doc,
        rows=None,
        summary=None,
        anchors=None,
        manifest=None,
    )

    assert any("missing phrase" in failure for failure in failures)


def test_overclaim_wording_fails(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8") + "\nThis is a significant finding.\n"
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_kjva_wikisource_candidate_source_audit_doc(
        doc,
        rows=None,
        summary=None,
        anchors=None,
        manifest=None,
    )

    assert any("possible overclaim wording" in failure for failure in failures)


def test_rows_status_drift_fails(tmp_path: Path) -> None:
    rows = tmp_path / "rows.csv"
    rows.write_text(
        ",".join(check.analyzer.ROW_FIELDNAMES)
        + "\n"
        + "wikisource_ballantyne_1911_kjva,"
        + check.analyzer.WIKISOURCE_URL
        + ","
        + check.analyzer.WIKISOURCE_URL
        + ",fetched,,1,abc,title,True,True,True,True,True,"
        + "ready,True,ready\n",
        encoding="utf-8",
    )

    failures = check.validate_rows_csv(rows)

    assert any("verse_numbered_import_ready drifted" in failure for failure in failures)
    assert any("result_ready_status drifted" in failure for failure in failures)
