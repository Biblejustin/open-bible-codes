import csv
from pathlib import Path

from scripts import check_cities_source_transcription_decision_records as check
from scripts import build_cities_source_transcription_review_worksheet as builder


def test_current_transcription_decision_records_pass() -> None:
    assert check.validate_decision_records() == []


def test_rejects_schema_drift(tmp_path: Path) -> None:
    records = tmp_path / "records.csv"
    write_csv(records, ["wrong"], [])

    failures = check.validate_decision_records(records)

    assert failures == [f"{records} fieldnames drifted"]


def test_rejects_populated_rows(tmp_path: Path) -> None:
    records = tmp_path / "records.csv"
    write_csv(
        records,
        builder.RECORD_FIELDS,
        [
            {
                "transcription_decision_id": "cities_source_transcription_001",
                "source_lock_decision_id": "cities_source_row_lock_001",
                "source_label": "cities_pdf_dp365a_p5_11",
                "page_number": "3",
                "page_class": "table_candidate_page",
                "decision_status": "locked",
                "selected_action": "source_row_import_ready",
                "evidence_citation": "manual page review",
                "evidence_summary": "manual readable transcription locked",
                "locked_by": "tester",
                "locked_at": "2026-05-31",
                "notes": "test",
            }
        ],
    )

    failures = check.validate_decision_records(records)

    assert failures == [
        f"{records} has 1 populated transcription decision rows; "
        "readable transcription decisions are not locked yet"
    ]


def test_rejects_source_script_text(tmp_path: Path) -> None:
    records = tmp_path / "records.csv"
    write_csv(
        records,
        builder.RECORD_FIELDS,
        [
            {
                "transcription_decision_id": "cities_source_transcription_001",
                "source_lock_decision_id": "cities_source_row_lock_001",
                "source_label": "cities_pdf_dp365a_p5_11",
                "page_number": "3",
                "page_class": "table_candidate_page",
                "decision_status": "locked",
                "selected_action": "source_row_import_ready",
                "evidence_citation": "manual page review",
                "evidence_summary": "contains Hebrew אבג",
                "locked_by": "tester",
                "locked_at": "2026-05-31",
                "notes": "test",
            }
        ],
    )

    failures = check.validate_decision_records(records)

    assert f"{records} appears to contain source-script body text" in failures


def write_csv(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, str]],
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
