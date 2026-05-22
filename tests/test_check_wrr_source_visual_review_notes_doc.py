from pathlib import Path

from scripts import check_wrr_source_visual_review_notes_doc as check


def test_current_wrr_source_visual_review_notes_doc_passes() -> None:
    assert check.validate_source_visual_review_notes_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_source_visual_review_notes_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_scope_warning_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_VISUAL_REVIEW_NOTES.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[:-1]) + "\n", encoding="utf-8")

    failures = check.validate_source_visual_review_notes_doc(doc)

    assert any("visual-review note excludes" in failure for failure in failures)


def test_missing_term_change_warning_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_VISUAL_REVIEW_NOTES.md"
    text = "\n".join(
        phrase
        for phrase in check.REQUIRED_PHRASES
        if phrase != "None of these notes authorize changing WRR terms or claiming reproduction."
    )
    doc.write_text(text + "\n", encoding="utf-8")

    failures = check.validate_source_visual_review_notes_doc(doc)

    assert any("authorize changing WRR terms" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR source visual-review notes doc failure" in capsys.readouterr().err
