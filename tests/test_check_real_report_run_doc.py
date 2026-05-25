from pathlib import Path

from scripts import check_real_report_run_doc as check


def test_current_real_report_run_doc_passes() -> None:
    assert check.validate_real_report_run_doc() == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    doc = tmp_path / "missing.md"

    failures = check.validate_real_report_run_doc(doc)

    assert failures == [f"{doc} is missing"]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "REAL_REPORT_RUN.md"
    doc.write_text("incomplete", encoding="utf-8")

    failures = check.validate_real_report_run_doc(doc)

    assert f"{doc} missing phrase: {check.REQUIRED_PHRASES[0]}" in failures


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    code = check.main(["--doc", str(tmp_path / "missing.md")])

    assert code == 1
    assert "real-report run doc failure" in capsys.readouterr().err
