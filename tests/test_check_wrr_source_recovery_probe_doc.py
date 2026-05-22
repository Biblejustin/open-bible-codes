from pathlib import Path

from scripts import check_wrr_source_recovery_probe_doc as check


def test_current_wrr_source_recovery_probe_doc_passes() -> None:
    assert check.validate_source_recovery_probe_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_source_recovery_probe_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_probe_only_status_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_RECOVERY_PROBE.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[2:]) + "\n", encoding="utf-8")

    failures = check.validate_source_recovery_probe_doc(doc)

    assert any("live-source recovery probe only" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR source-recovery probe doc failure" in capsys.readouterr().err
