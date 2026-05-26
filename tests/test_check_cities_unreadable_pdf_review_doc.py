import csv
from pathlib import Path

from scripts import check_cities_unreadable_pdf_review_doc as check


def test_current_cities_unreadable_pdf_review_doc_passes() -> None:
    assert check.validate_cities_unreadable_pdf_review_doc(check.DEFAULT_DOC) == []


def test_detects_missing_boundary_phrase(tmp_path: Path) -> None:
    rows = tmp_path / "rows.csv"
    summary = tmp_path / "summary.csv"
    doc = tmp_path / "review.md"
    write_rows(rows)
    write_summary(summary)
    doc.write_text("# Cities Unreadable PDF Review\n", encoding="utf-8")

    failures = check.validate_cities_unreadable_pdf_review_doc(doc, rows, summary)

    assert any("missing phrase" in failure for failure in failures)


def test_detects_summary_mismatch(tmp_path: Path) -> None:
    rows = tmp_path / "rows.csv"
    summary = tmp_path / "summary.csv"
    doc = tmp_path / "review.md"
    write_rows(rows)
    write_summary(summary, unreadable_rows_reviewed="99")
    doc.write_text(check.DEFAULT_DOC.read_text(encoding="utf-8"), encoding="utf-8")

    failures = check.validate_cities_unreadable_pdf_review_doc(doc, rows, summary)

    assert any("Unreadable rows reviewed=99" in failure for failure in failures)


def write_rows(path: Path) -> None:
    rows = [
        ("cities_pdf_dp365a_appendix_6", "ocr_image_only_pdf"),
        ("cities_pdf_dp365a_appendix_7", "ocr_image_only_pdf"),
        ("cities_pdf_dp365a_part_2_p105_111", "ocr_image_only_pdf"),
        ("cities_pdf_wrr", "ocr_image_only_pdf"),
        ("cities_pdf_dp365a_p12_17", "encoding_or_ocr_candidate"),
        ("cities_pdf_dp365a_p1_4", "encoding_or_ocr_candidate"),
        ("cities_pdf_dp365a_p5_11", "encoding_or_ocr_candidate"),
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["label", "lane"])
        writer.writeheader()
        for label, lane in rows:
            writer.writerow({"label": label, "lane": lane})


def write_summary(path: Path, *, unreadable_rows_reviewed: str = "7") -> None:
    metrics = {
        "unreadable_rows_reviewed": unreadable_rows_reviewed,
        "ocr_image_only_rows": "4",
        "encoding_or_ocr_candidate_rows": "3",
        "aumann_committee_rows": "6",
        "other_family_rows": "1",
        "total_pages_needing_review": "41",
        "garbled_text_chars": "5364",
    }
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        for metric, value in metrics.items():
            writer.writerow({"metric": metric, "value": value})
