import csv
import json
from pathlib import Path

from scripts import build_cities_no_input_handoff_status as handoff


def test_build_summary_consolidates_current_cities_blockers() -> None:
    summary = handoff.build_summary(_inputs())

    assert summary["status_rows"] == 8
    assert summary["manual_input_needed_rows"] == 6
    assert summary["queue_rows"] == 14
    assert summary["evidence_rows"] == 14
    assert summary["source_row_lock_decision_rows"] == 14
    assert summary["locked_source_row_lock_decisions"] == 14
    assert summary["transcription_review_rows"] == 14
    assert summary["pending_transcription_rows"] == 14
    assert summary["transcription_decision_rows"] == 0
    assert summary["ocr_review_rows"] == 14
    assert summary["ocr_text_sidecars"] == 14
    assert summary["ocr_packet_pages"] == 61
    assert summary["ocr_packet_pages_reviewed"] == 41
    assert summary["ocr_packet_pages_unreviewed"] == 20
    assert summary["line_crop_rows"] == 203
    assert summary["priority_review_rows"] == 203
    assert summary["source_row_imports"] == 0
    assert summary["els_runs"] == 0
    assert summary["compactness_runs"] == 0
    assert summary["p_levels"] == 0
    assert summary["result_allowed"] is False


def test_build_status_rows_keep_boundaries_visible() -> None:
    args = handoff.build_parser().parse_args([])
    summary = handoff.build_summary(_inputs())
    rows = handoff.build_status_rows(summary, args)

    by_id = {row["status_id"]: row for row in rows}
    assert len(rows) == 8
    assert by_id["source_row_lock_decisions"]["manual_input_needed"] == "no"
    assert by_id["result_boundary"]["current_status"] == "blocked"
    assert "41/61 packet pages reviewed" in by_id["local_ocr_review_aids"][
        "current_value"
    ]
    assert "not row transcription" in by_id["source_row_lock_decisions"]["boundary"]
    assert "no Cities source-row import" in by_id["result_boundary"]["boundary"]
    assert sum(row["manual_input_needed"] == "yes" for row in rows) == 6


def test_main_writes_csv_markdown_and_manifest(tmp_path: Path) -> None:
    paths = _write_inputs(tmp_path)
    out = tmp_path / "status.csv"
    summary = tmp_path / "summary.csv"
    markdown = tmp_path / "handoff.md"
    manifest = tmp_path / "manifest.json"

    code = handoff.main(
        [
            "--queue-summary",
            str(paths["queue_summary"]),
            "--evidence-summary",
            str(paths["evidence_summary"]),
            "--row-lock-decisions",
            str(paths["row_lock_decisions"]),
            "--transcription-worksheet",
            str(paths["transcription_worksheet"]),
            "--transcription-decisions",
            str(paths["transcription_decisions"]),
            "--page-bundle-summary",
            str(paths["page_bundle_summary"]),
            "--ocr-summary",
            str(paths["ocr_summary"]),
            "--page-review-summary",
            str(paths["page_review_summary"]),
            "--line-crop-summary",
            str(paths["line_crop_summary"]),
            "--priority-contact-summary",
            str(paths["priority_contact_summary"]),
            "--priority-review-summary",
            str(paths["priority_review_summary"]),
            "--out",
            str(out),
            "--summary-out",
            str(summary),
            "--markdown-out",
            str(markdown),
            "--manifest-out",
            str(manifest),
        ]
    )

    assert code == 0
    rows = list(csv.DictReader(out.open(encoding="utf-8", newline="")))
    assert rows[0]["status_id"] == "source_row_lock_queue"
    summary_rows = list(csv.DictReader(summary.open(encoding="utf-8", newline="")))
    assert summary_rows[0]["claim_status"] == handoff.CLAIM_BOUNDARY
    text = markdown.read_text(encoding="utf-8")
    assert "Status: consolidated Cities no-input handoff." in text
    assert "Result allowed: 0." in text
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["tool"] == "scripts.build_cities_no_input_handoff_status"
    assert payload["status_rows"] == 8


def _inputs() -> handoff.LoadedInputs:
    return handoff.LoadedInputs(
        queue_summary=_metric_rows(
            {
                "queue_rows": "14",
                "source_row_imports": "0",
                "els_runs": "0",
                "compactness_runs": "0",
            }
        ),
        evidence_summary=_metric_rows(
            {
                "evidence_rows": "14",
                "source_row_imports": "0",
                "els_runs": "0",
                "compactness_runs": "0",
            }
        ),
        row_lock_decisions=[{"decision_status": "locked"} for _ in range(14)],
        transcription_worksheet=[
            {"current_transcription_status": "unrecorded"} for _ in range(14)
        ],
        transcription_decisions=[],
        page_bundle_summary=_metric_rows(
            {
                "bundle_rows": "14",
                "page_images_found": "14",
                "city_name_normalization": "0",
                "p_levels": "0",
            }
        ),
        ocr_summary=_metric_rows(
            {
                "source_page_ocr_rows": "14",
                "pages_with_ocr_text": "14",
                "ocr_text_sidecars": "14",
                "ocr_hebrew_letters": "14408",
            }
        ),
        page_review_summary=_metric_rows(
            {
                "packet_pages": "61",
                "reviewed_packet_pages": "41",
                "unreviewed_packet_pages": "20",
            }
        ),
        line_crop_summary=_metric_rows(
            {
                "line_crop_rows": "203",
                "line_crops_available": "203",
                "ocr_words": "1511",
                "ocr_hebrew_letters": "4934",
            }
        ),
        priority_contact_summary=_metric_rows(
            {"priority_sheets": "4", "priority_sheets_available": "4"}
        ),
        priority_review_summary=_metric_rows(
            {
                "priority_review_rows": "203",
                "priority_1_dense_text": "120",
                "priority_2_medium_text": "71",
                "priority_3_short_text": "12",
                "bucket_likely_row_or_header": "191",
                "bucket_short_label_or_marker": "12",
            }
        ),
    )


def _write_inputs(tmp_path: Path) -> dict[str, Path]:
    paths = {
        "queue_summary": tmp_path / "queue.csv",
        "evidence_summary": tmp_path / "evidence.csv",
        "row_lock_decisions": tmp_path / "locks.csv",
        "transcription_worksheet": tmp_path / "worksheet.csv",
        "transcription_decisions": tmp_path / "decisions.csv",
        "page_bundle_summary": tmp_path / "bundle.csv",
        "ocr_summary": tmp_path / "ocr.csv",
        "page_review_summary": tmp_path / "page_review.csv",
        "line_crop_summary": tmp_path / "line_crop.csv",
        "priority_contact_summary": tmp_path / "priority_contact.csv",
        "priority_review_summary": tmp_path / "priority_review.csv",
    }
    inputs = _inputs()
    _write_csv(paths["queue_summary"], ["metric", "value"], inputs.queue_summary)
    _write_csv(paths["evidence_summary"], ["metric", "value"], inputs.evidence_summary)
    _write_csv(paths["row_lock_decisions"], ["decision_status"], inputs.row_lock_decisions)
    _write_csv(
        paths["transcription_worksheet"],
        ["current_transcription_status"],
        inputs.transcription_worksheet,
    )
    _write_csv(paths["transcription_decisions"], ["decision_status"], [])
    _write_csv(
        paths["page_bundle_summary"], ["metric", "value"], inputs.page_bundle_summary
    )
    _write_csv(paths["ocr_summary"], ["metric", "value"], inputs.ocr_summary)
    _write_csv(
        paths["page_review_summary"],
        ["metric", "value"],
        inputs.page_review_summary,
    )
    _write_csv(
        paths["line_crop_summary"], ["metric", "value"], inputs.line_crop_summary
    )
    _write_csv(
        paths["priority_contact_summary"],
        ["metric", "value"],
        inputs.priority_contact_summary,
    )
    _write_csv(
        paths["priority_review_summary"],
        ["metric", "value"],
        inputs.priority_review_summary,
    )
    return paths


def _metric_rows(metrics: dict[str, str]) -> list[dict[str, str]]:
    return [{"metric": key, "value": value} for key, value in metrics.items()]


def _write_csv(
    path: Path, fieldnames: list[str], rows: list[dict[str, str]]
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
