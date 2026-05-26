from pathlib import Path

from scripts import check_wrr_source_row_crop_contact_sheet_doc as check


def test_current_wrr_source_row_crop_contact_sheet_doc_passes() -> None:
    assert check.validate_source_row_crop_contact_sheet_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_source_row_crop_contact_sheet_doc(tmp_path / "missing.md")
    assert any("is missing" in failure for failure in failures)


def test_missing_boundary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_ROW_CROP_CONTACT_SHEET.md"
    doc.write_text("# WRR Source Row Crop Contact Sheet\n", encoding="utf-8")
    failures = check.validate_source_row_crop_contact_sheet_doc(doc)
    assert any("not transcription verification" in failure for failure in failures)
