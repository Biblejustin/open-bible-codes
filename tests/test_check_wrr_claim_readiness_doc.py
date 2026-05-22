from pathlib import Path

from scripts import check_wrr_claim_readiness_doc as check


def test_current_wrr_claim_readiness_doc_passes() -> None:
    assert check.validate_readiness_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_readiness_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_ready_status_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_CLAIM_READINESS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[1:]) + "\n", encoding="utf-8")

    failures = check.validate_readiness_doc(doc)

    assert any("Status: ready" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR claim-readiness doc failure" in capsys.readouterr().err
