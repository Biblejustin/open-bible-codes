import csv
from pathlib import Path

from scripts import check_cities_unreadable_pdf_ocr_review_packet_doc as check


def test_current_cities_unreadable_pdf_ocr_review_packet_doc_passes() -> None:
    assert check.validate_cities_unreadable_pdf_ocr_review_packet_doc(check.DEFAULT_DOC) == []


def test_detects_missing_boundary_phrase(tmp_path: Path) -> None:
    rows = tmp_path / "rows.csv"
    summary = tmp_path / "summary.csv"
    doc = tmp_path / "review.md"
    write_rows(rows)
    write_summary(summary)
    doc.write_text("# Cities Unreadable PDF OCR Review Packet\n", encoding="utf-8")

    failures = check.validate_cities_unreadable_pdf_ocr_review_packet_doc(
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
    write_summary(summary, page_rows="99")
    doc.write_text(check.DEFAULT_DOC.read_text(encoding="utf-8"), encoding="utf-8")

    failures = check.validate_cities_unreadable_pdf_ocr_review_packet_doc(
        doc,
        rows,
        summary,
    )

    assert any("Page rows=99" in failure for failure in failures)


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
            writer.writerow({"label": label, "ocr_status": "page_ocr_text_detected"})
        writer.writerow({"label": labels[0], "ocr_status": "page_ocr_empty"})


def write_summary(path: Path, *, page_rows: str = "41") -> None:
    metrics = {
        "pdf_rows": "7",
        "page_rows": page_rows,
        "pages_with_ocr_text": "39",
        "pages_without_ocr_text": "2",
        "ocr_text_signal_chars": "54324",
        "ocr_words": "8500",
        "ocr_lines": "500",
        "image_sidecars": "41",
        "ocr_text_sidecars": "41",
        "status_page_ocr_text_detected": "39",
        "status_page_ocr_empty": "2",
    }
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        for metric, value in metrics.items():
            writer.writerow({"metric": metric, "value": value})
