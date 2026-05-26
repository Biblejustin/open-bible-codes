from pathlib import Path

from scripts import check_wrr_source_row_review_bundle_doc as check


def test_current_wrr_source_row_review_bundle_doc_passes() -> None:
    assert check.validate_source_row_review_bundle_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_source_row_review_bundle_doc(tmp_path / "missing.md")
    assert any("is missing" in failure for failure in failures)


def test_missing_boundary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_ROW_REVIEW_BUNDLE.md"
    doc.write_text("# WRR Source Row Review Bundle\n", encoding="utf-8")
    failures = check.validate_source_row_review_bundle_doc(doc)
    assert any(
        "Crop and OCR availability is not transcription verification" in failure
        for failure in failures
    )
