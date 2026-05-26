import struct
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
    failures = check.validate_source_row_crop_contact_sheet_doc(doc, image=None)
    assert any("not transcription verification" in failure for failure in failures)


def test_matching_doc_and_png_pass(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)
    image = _png(tmp_path, check.EXPECTED_DIMENSIONS)

    assert check.validate_source_row_crop_contact_sheet_doc(doc, image=image) == []


def test_bad_png_dimensions_fail(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)
    image = _png(tmp_path, (100, 50))

    failures = check.validate_source_row_crop_contact_sheet_doc(doc, image=image)

    assert any("expected" in failure for failure in failures)


def _required_doc(root: Path) -> Path:
    doc = root / "WRR_SOURCE_ROW_CROP_CONTACT_SHEET.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    return doc


def _png(root: Path, dimensions: tuple[int, int]) -> Path:
    image = root / "contact.png"
    width, height = dimensions
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    image.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + struct.pack(">I4s", len(ihdr), b"IHDR")
        + ihdr
        + b"\x00\x00\x00\x00"
    )
    return image
