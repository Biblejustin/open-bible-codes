from pathlib import Path

from scripts import check_wrr_locked_method_report_doc as check


def test_current_wrr_locked_method_report_doc_passes() -> None:
    assert check.validate_locked_method_report_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_locked_method_report_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_status_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCKED_METHOD_REPORT.md"
    doc.write_text(
        "\n".join(
            phrase
            for phrase in check.REQUIRED_PHRASES
            if "Status: locked local WRR method report" not in phrase
        )
        + "\n",
        encoding="utf-8",
    )

    failures = check.validate_locked_method_report_doc(doc)

    assert any("locked local WRR method report" in failure for failure in failures)


def test_forbidden_phrase_outside_list_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCKED_METHOD_REPORT.md"
    text = "\n".join(check.REQUIRED_PHRASES)
    doc.write_text(text + "\nThis proves WRR now.\n", encoding="utf-8")

    failures = check.validate_locked_method_report_doc(doc)

    assert any("forbidden phrase outside forbidden-language list" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR locked-method report failure" in capsys.readouterr().err
