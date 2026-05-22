from pathlib import Path

from scripts import check_wrr_cross_pair_grid_doc as check


def test_current_wrr_cross_pair_grid_doc_passes() -> None:
    assert check.validate_cross_pair_grid_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_cross_pair_grid_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_permutation_summary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_CROSS_PAIR_GRID.md"
    doc.write_text(
        "\n".join(
            phrase
            for phrase in check.REQUIRED_PHRASES
            if phrase != "| rho P1 | 0.019722 |"
        )
        + "\n",
        encoding="utf-8",
    )

    failures = check.validate_cross_pair_grid_doc(doc)

    assert any("0.019722" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR cross-pair grid doc failure" in capsys.readouterr().err
