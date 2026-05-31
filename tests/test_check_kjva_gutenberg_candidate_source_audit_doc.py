from pathlib import Path

from scripts import check_kjva_gutenberg_candidate_source_audit_doc as check


def test_current_kjva_gutenberg_source_audit_doc_passes() -> None:
    assert check.validate_kjva_gutenberg_candidate_source_audit_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    missing = tmp_path / "missing.md"

    failures = check.validate_kjva_gutenberg_candidate_source_audit_doc(missing)

    assert failures == [f"{missing} is missing"]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8").replace(
        "KJV-complete metadata candidates: 1.",
        "KJV-complete metadata candidates: unknown.",
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_kjva_gutenberg_candidate_source_audit_doc(
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
        + "gutenberg_ebook_30_kjv_complete,"
        + check.analyzer.RDF_URL
        + ","
        + check.analyzer.RDF_URL
        + ",fetched,,10,sha,30,"
        + check.analyzer.EBOOK_PAGE_URL
        + ",The Bible, King James Version, Complete,Public domain in the USA.,1992-04-01,1,1,desc,"
        + "False,True,True,False,True,source_candidate_not_confirmed,"
        + "needs_source_use_policy_lock,False,not_source_lock_ready,not_result_ready\n",
        encoding="utf-8",
    )

    failures = check.validate_rows_csv(rows)

    assert any("plain_text_utf8_url_present drifted" in failure for failure in failures)
    assert any("source_audit_status drifted" in failure for failure in failures)
