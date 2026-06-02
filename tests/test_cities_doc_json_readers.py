import importlib
from pathlib import Path
from typing import Callable


CITIES_DOC_JSON_READER_MODULES = (
    "scripts.check_cities_extractable_text_review_doc",
    "scripts.check_cities_pdf_recovery_probe_doc",
    "scripts.check_cities_recovered_pdf_text_audit_doc",
    "scripts.check_cities_source_page_contact_sheet_doc",
    "scripts.check_cities_source_page_line_crop_band_contact_sheet_doc",
    "scripts.check_cities_source_page_line_crop_band_map_doc",
    "scripts.check_cities_source_page_line_crop_band_review_worksheet_doc",
    "scripts.check_cities_source_page_line_crop_contact_sheet_doc",
    "scripts.check_cities_source_page_line_crop_priority_contact_sheet_doc",
    "scripts.check_cities_source_page_line_crop_priority_review_worksheet_doc",
    "scripts.check_cities_source_page_line_crop_review_worksheet_doc",
    "scripts.check_cities_source_page_line_crop_triage_doc",
    "scripts.check_cities_source_page_review_bundle_doc",
    "scripts.check_cities_source_review_queue_doc",
    "scripts.check_cities_source_row_lock_evidence_packet_doc",
    "scripts.check_cities_source_row_lock_queue_doc",
    "scripts.check_cities_source_row_lock_worksheet_doc",
    "scripts.check_cities_source_transcription_review_worksheet_doc",
    "scripts.check_cities_unreadable_pdf_ocr_feasibility_doc",
    "scripts.check_cities_unreadable_pdf_ocr_page_review_doc",
    "scripts.check_cities_unreadable_pdf_ocr_review_checklist_doc",
    "scripts.check_cities_unreadable_pdf_ocr_review_packet_doc",
    "scripts.check_cities_unreadable_pdf_review_doc",
)


def test_cities_doc_json_readers_reject_invalid_json(tmp_path: Path) -> None:
    for module_name in CITIES_DOC_JSON_READER_MODULES:
        path = tmp_path / f"{module_name.rsplit('.', 1)[-1]}.json"
        path.write_text("{", encoding="utf-8")

        failure = _reader(module_name)(path)

        assert isinstance(failure, str), module_name
        assert "is invalid JSON" in failure, module_name


def test_cities_doc_json_readers_reject_non_object_json(tmp_path: Path) -> None:
    for module_name in CITIES_DOC_JSON_READER_MODULES:
        path = tmp_path / f"{module_name.rsplit('.', 1)[-1]}.json"
        path.write_text("[]", encoding="utf-8")

        failure = _reader(module_name)(path)

        assert isinstance(failure, str), module_name
        assert "JSON root must be an object" in failure, module_name


def _reader(module_name: str) -> Callable[[Path], object]:
    module = importlib.import_module(module_name)
    reader = getattr(module, "_read_json", None) or getattr(module, "read_json", None)
    assert reader is not None, module_name
    return reader
