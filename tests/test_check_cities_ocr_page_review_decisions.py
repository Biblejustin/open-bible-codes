import csv
from pathlib import Path

from scripts import check_cities_ocr_page_review_decisions as check


def test_current_cities_ocr_page_review_decisions_pass() -> None:
    assert check.validate_decisions() == []


def test_rejects_schema_drift(tmp_path: Path) -> None:
    decisions, packet = write_fixture(tmp_path)
    decisions.write_text("wrong\nx\n", encoding="utf-8")

    failures = check.validate_decisions(decisions, packet)

    assert f"{decisions} fieldnames drifted" in failures


def test_rejects_source_row_use(tmp_path: Path) -> None:
    decisions, packet = write_fixture(tmp_path)
    fieldnames, rows = read_csv(decisions)
    rows[0]["source_row_use"] = "source_row_use"
    write_csv(decisions, fieldnames, rows)

    failures = check.validate_decisions(decisions, packet)

    assert f"{decisions}:2 source_row_use must be no_source_row_use" in failures


def test_rejects_source_script_text(tmp_path: Path) -> None:
    decisions, packet = write_fixture(tmp_path)
    fieldnames, rows = read_csv(decisions)
    rows[0]["notes"] = "OCR text אבג"
    write_csv(decisions, fieldnames, rows)

    failures = check.validate_decisions(decisions, packet)

    assert f"{decisions} appears to contain OCR/source-script body text" in failures


def test_rejects_missing_packet_page(tmp_path: Path) -> None:
    decisions, packet = write_fixture(tmp_path)
    fieldnames, rows = read_csv(packet)
    rows.clear()
    write_csv(packet, fieldnames, rows)

    failures = check.validate_decisions(decisions, packet)

    assert f"{decisions}:2 label/page not in OCR packet" in failures


def write_fixture(tmp_path: Path) -> tuple[Path, Path]:
    decisions = tmp_path / "decisions.csv"
    packet = tmp_path / "packet.csv"
    write_csv(
        decisions,
        list(check.EXPECTED_FIELDNAMES),
        [
            {
                "decision_id": "cities_ocr_page_review_001",
                "label": "cities_pdf_dp365a_p1_4",
                "page_number": "3",
                "visual_review_status": "reviewed",
                "visual_page_role": "appendix_toc_or_index_page",
                "visual_text_signal": "text_present",
                "ocr_read_status": "ocr_empty_but_visual_text_present",
                "source_row_use": "no_source_row_use",
                "decision": "no_source_row_import",
                "reviewed_by": "tester",
                "reviewed_at": "2026-05-26",
                "notes": "test page review",
            }
        ],
    )
    write_csv(
        packet,
        ["label", "page_number"],
        [{"label": "cities_pdf_dp365a_p1_4", "page_number": "3"}],
    )
    return decisions, packet


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def write_csv(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, str]],
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
