from pathlib import Path

from scripts import check_wrr_method_status_doc as check


def test_current_wrr_method_status_doc_passes() -> None:
    assert check.validate_method_status_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_method_status_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_exact_published_reproduction_status_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_METHOD_STATUS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[2:]) + "\n", encoding="utf-8")

    failures = check.validate_method_status_doc(doc)

    assert any("not an exact published WRR reproduction" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR method-status doc failure" in capsys.readouterr().err
