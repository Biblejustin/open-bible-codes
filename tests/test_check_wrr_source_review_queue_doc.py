from pathlib import Path

from scripts import check_wrr_source_review_queue_doc as check


def test_current_wrr_source_review_queue_doc_passes() -> None:
    assert check.validate_source_review_queue_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_source_review_queue_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_queue_counts_fail(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_REVIEW_QUEUE.md"
    phrases = [
        phrase
        for phrase in check.REQUIRED_PHRASES
        if "ocr_not_matched_no_variant_lead" not in phrase
    ]
    doc.write_text("\n".join(phrases) + "\n", encoding="utf-8")

    failures = check.validate_source_review_queue_doc(doc)

    assert any("ocr_not_matched_no_variant_lead" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR source-review queue doc failure" in capsys.readouterr().err
