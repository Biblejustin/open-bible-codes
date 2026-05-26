import csv
from pathlib import Path

from scripts import check_cities_unreadable_pdf_ocr_feasibility_doc as check


def test_current_cities_unreadable_pdf_ocr_feasibility_doc_passes() -> None:
    assert check.validate_cities_unreadable_pdf_ocr_feasibility_doc(check.DEFAULT_DOC) == []


def test_detects_missing_boundary_phrase(tmp_path: Path) -> None:
    rows = tmp_path / "rows.csv"
    summary = tmp_path / "summary.csv"
    doc = tmp_path / "review.md"
    write_rows(rows)
    write_summary(summary)
    doc.write_text("# Cities Unreadable PDF OCR Feasibility\n", encoding="utf-8")

    failures = check.validate_cities_unreadable_pdf_ocr_feasibility_doc(
        doc,
        rows,
        summary,
    )

    assert any("missing phrase" in failure for failure in failures)


def test_detects_summary_mismatch(tmp_path: Path) -> None:
    rows = tmp_path / "rows.csv"
    summary = tmp_path / "summary.csv"
    doc = tmp_path / "review.md"
    write_rows(rows)
    write_summary(summary, rows_reviewed="99")
    doc.write_text(check.DEFAULT_DOC.read_text(encoding="utf-8"), encoding="utf-8")

    failures = check.validate_cities_unreadable_pdf_ocr_feasibility_doc(
        doc,
        rows,
        summary,
    )

    assert any("Rows reviewed=99" in failure for failure in failures)


def write_rows(path: Path) -> None:
    labels = [
        "cities_pdf_dp365a_appendix_6",
        "cities_pdf_dp365a_appendix_7",
        "cities_pdf_dp365a_part_2_p105_111",
        "cities_pdf_wrr",
        "cities_pdf_dp365a_p12_17",
        "cities_pdf_dp365a_p1_4",
        "cities_pdf_dp365a_p5_11",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["label", "ocr_status"])
        writer.writeheader()
        for label in labels:
            writer.writerow({"label": label, "ocr_status": "ocr_text_detected"})


def write_summary(path: Path, *, rows_reviewed: str = "7") -> None:
    metrics = {
        "rows_reviewed": rows_reviewed,
        "rows_with_ocr_text": "7",
        "pages_attempted": "41",
        "pages_with_ocr_text": "39",
        "ocr_text_signal_chars": "54324",
        "status_ocr_text_detected": "7",
    }
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        for metric, value in metrics.items():
            writer.writerow({"metric": metric, "value": value})
