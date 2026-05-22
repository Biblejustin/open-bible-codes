from pathlib import Path

from scripts import check_wrr_claim_blocker_packet_doc as check


def test_current_wrr_claim_blocker_packet_doc_passes() -> None:
    assert check.validate_blocker_packet_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_blocker_packet_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_no_input_status_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_CLAIM_BLOCKER_PACKET.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[2:]) + "\n", encoding="utf-8")

    failures = check.validate_blocker_packet_doc(doc)

    assert any("no-input diagnostics exhausted" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR claim-blocker packet failure" in capsys.readouterr().err
