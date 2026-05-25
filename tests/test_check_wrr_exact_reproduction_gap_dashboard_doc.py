from pathlib import Path

from scripts import check_wrr_exact_reproduction_gap_dashboard_doc as check


def test_current_wrr_exact_gap_dashboard_doc_passes() -> None:
    assert check.validate_gap_dashboard_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_gap_dashboard_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_status_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md"
    doc.write_text(
        "\n".join(
            phrase
            for phrase in check.REQUIRED_PHRASES
            if "Status: exact published WRR reproduction" not in phrase
        )
        + "\n",
        encoding="utf-8",
    )

    failures = check.validate_gap_dashboard_doc(doc)

    assert any("Status: exact published WRR reproduction" in failure for failure in failures)


def test_forbidden_phrase_outside_list_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md"
    text = "\n".join(check.REQUIRED_PHRASES)
    doc.write_text(text + "\nsource correction selected now.\n", encoding="utf-8")

    failures = check.validate_gap_dashboard_doc(doc)

    assert any("forbidden phrase outside boundary list" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR exact gap dashboard failure" in capsys.readouterr().err
