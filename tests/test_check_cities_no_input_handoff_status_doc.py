import csv
import json
from pathlib import Path

from scripts import build_cities_no_input_handoff_status as builder
from scripts import check_cities_no_input_handoff_status_doc as check


def test_checker_accepts_generated_handoff_doc(tmp_path: Path) -> None:
    summary = _summary()
    rows = _rows()
    doc = tmp_path / "CITIES_NO_INPUT_HANDOFF_STATUS.md"
    status = tmp_path / "status.csv"
    summary_csv = tmp_path / "summary.csv"
    manifest = tmp_path / "manifest.json"

    builder.write_markdown(doc, summary, rows)
    _write_csv(status, builder.STATUS_FIELDNAMES, rows)
    _write_csv(summary_csv, builder.SUMMARY_FIELDNAMES, [summary])
    manifest.write_text(
        json.dumps(
            {
                "tool": "scripts.build_cities_no_input_handoff_status",
                "claim_boundary": "Cities no-input handoff only; no source import or result",
                "summary": {"claim_status": builder.CLAIM_BOUNDARY},
            }
        ),
        encoding="utf-8",
    )

    assert (
        check.validate_cities_no_input_handoff_doc(
            doc,
            status_path=status,
            summary_path=summary_csv,
            manifest_path=manifest,
        )
        == []
    )


def test_checker_rejects_result_allowed_overclaim(tmp_path: Path) -> None:
    doc = tmp_path / "handoff.md"
    doc.write_text(
        "# Cities No-Input Handoff Status\n\nResult allowed: 1.\n",
        encoding="utf-8",
    )

    failures = check.validate_cities_no_input_handoff_doc(
        doc,
        status_path=tmp_path / "missing_status.csv",
        summary_path=tmp_path / "missing_summary.csv",
        manifest_path=tmp_path / "missing_manifest.json",
    )

    assert any("is missing" in failure for failure in failures)


def test_checker_rejects_summary_drift(tmp_path: Path) -> None:
    summary = _summary()
    summary["result_allowed"] = True
    doc = tmp_path / "CITIES_NO_INPUT_HANDOFF_STATUS.md"
    status = tmp_path / "status.csv"
    summary_csv = tmp_path / "summary.csv"
    manifest = tmp_path / "manifest.json"

    builder.write_markdown(doc, _summary(), _rows())
    _write_csv(status, builder.STATUS_FIELDNAMES, _rows())
    _write_csv(summary_csv, builder.SUMMARY_FIELDNAMES, [summary])
    manifest.write_text(
        json.dumps(
            {
                "tool": "scripts.build_cities_no_input_handoff_status",
                "claim_boundary": "Cities no-input handoff only; no source import or result",
                "summary": {"claim_status": builder.CLAIM_BOUNDARY},
            }
        ),
        encoding="utf-8",
    )

    failures = check.validate_cities_no_input_handoff_doc(
        doc,
        status_path=status,
        summary_path=summary_csv,
        manifest_path=manifest,
    )

    assert any("result_allowed drifted" in failure for failure in failures)


def _summary() -> dict[str, object]:
    return {
        "status_rows": 8,
        "handoff_ready_rows": 8,
        "manual_input_needed_rows": 6,
        "queue_rows": 14,
        "evidence_rows": 14,
        "source_row_lock_decision_rows": 14,
        "locked_source_row_lock_decisions": 14,
        "transcription_review_rows": 14,
        "transcription_decision_rows": 0,
        "pending_transcription_rows": 14,
        "page_review_bundle_rows": 14,
        "page_images_found": 14,
        "ocr_review_rows": 14,
        "ocr_pages_with_text": 14,
        "ocr_text_sidecars": 14,
        "ocr_hebrew_letters": 14408,
        "line_crop_rows": 203,
        "line_crops_available": 203,
        "line_crop_ocr_words": 1511,
        "line_crop_hebrew_letters": 4934,
        "priority_review_rows": 203,
        "priority_contact_sheets": 4,
        "priority_contact_sheets_available": 4,
        "priority_dense_text_rows": 120,
        "priority_medium_text_rows": 71,
        "priority_short_text_rows": 12,
        "bucket_likely_row_or_header": 191,
        "bucket_short_label_or_marker": 12,
        "source_row_imports": 0,
        "city_name_normalization": 0,
        "els_runs": 0,
        "compactness_runs": 0,
        "p_levels": 0,
        "result_allowed": False,
        "claim_status": builder.CLAIM_BOUNDARY,
    }


def _rows() -> list[dict[str, str]]:
    rows = []
    manual_no = {"source_row_lock_queue", "source_row_lock_decisions"}
    for status_id in sorted(check.REQUIRED_STATUS_IDS):
        rows.append(
            {
                "status_id": status_id,
                "area": "area",
                "current_status": "status",
                "current_value": "value",
                "handoff_ready": "yes",
                "manual_input_needed": "no" if status_id in manual_no else "yes",
                "next_action": "next",
                "boundary": "boundary",
                "source": "source.csv",
            }
        )
    return rows


def _write_csv(
    path: Path, fieldnames: list[str], rows: list[dict[str, object]]
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
