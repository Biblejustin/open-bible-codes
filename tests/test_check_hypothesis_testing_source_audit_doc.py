from pathlib import Path

from scripts import check_hypothesis_testing_source_audit_doc as check


def test_current_hypothesis_testing_source_audit_doc_passes() -> None:
    assert check.validate_hypothesis_testing_source_audit_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_hypothesis_testing_source_audit_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_no_usable_pages_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "HYPOTHESIS_TESTING_SOURCE_AUDIT.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[:9]) + "\n", encoding="utf-8")

    failures = check.validate_hypothesis_testing_source_audit_doc(doc)

    assert any("usable hypothesis-testing source pages" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "hypothesis-testing source audit doc failure" in capsys.readouterr().err
