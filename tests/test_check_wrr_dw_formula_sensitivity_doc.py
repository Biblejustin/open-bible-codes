from pathlib import Path

from scripts import check_wrr_dw_formula_sensitivity_doc as check


def test_current_wrr_dw_formula_sensitivity_doc_passes() -> None:
    assert check.validate_dw_formula_sensitivity_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_dw_formula_sensitivity_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_all_lanes_summary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_DW_FORMULA_SENSITIVITY.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[:-6]) + "\n", encoding="utf-8")

    failures = check.validate_dw_formula_sensitivity_doc(doc)

    assert any("all_lanes_cap1000" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR D(w) formula sensitivity doc failure" in capsys.readouterr().err
