from pathlib import Path

from scripts import check_manual_review_queue as check


def test_current_manual_review_queue_passes() -> None:
    assert check.validate_manual_review_queue(check.DEFAULT_DOC) == []


def test_missing_guard_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "MANUAL_REVIEW_QUEUE.md"
    doc.write_text("Status: navigation aid.\n", encoding="utf-8")

    failures = check.validate_manual_review_queue(doc)

    assert any("missing guard phrase" in failure for failure in failures)


def test_missing_evidence_link_fails(tmp_path: Path) -> None:
    doc = tmp_path / "MANUAL_REVIEW_QUEUE.md"
    text = "\n".join(check.REQUIRED_PHRASES + check.REQUIRED_ROW_FAMILIES)
    doc.write_text(text + "\n", encoding="utf-8")

    failures = check.validate_manual_review_queue(doc)

    assert any("missing evidence link" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "manual review queue failure" in capsys.readouterr().err
