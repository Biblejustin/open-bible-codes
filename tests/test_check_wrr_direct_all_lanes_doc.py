from pathlib import Path

from scripts import check_wrr_direct_all_lanes_doc as check


def test_current_wrr_direct_all_lanes_doc_passes() -> None:
    assert check.validate_direct_all_lanes_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_direct_all_lanes_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_cap1000_summary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_DIRECT_ALL_LANES_DIAGNOSTIC.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[:-8]) + "\n", encoding="utf-8")

    failures = check.validate_direct_all_lanes_doc(doc)

    assert any("cap 1000" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR direct all-lane doc failure" in capsys.readouterr().err
