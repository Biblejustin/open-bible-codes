import csv
from pathlib import Path

from scripts import check_cities_extractable_text_review_doc as check


def test_current_cities_extractable_text_review_doc_passes() -> None:
    assert check.validate_cities_extractable_text_review_doc(check.DEFAULT_DOC) == []


def test_detects_missing_boundary_phrase(tmp_path: Path) -> None:
    rows = tmp_path / "rows.csv"
    summary = tmp_path / "summary.csv"
    doc = tmp_path / "review.md"
    write_rows(rows)
    write_summary(summary)
    doc.write_text("# Cities Extractable Text Review\n", encoding="utf-8")

    failures = check.validate_cities_extractable_text_review_doc(doc, rows, summary)

    assert any("missing phrase" in failure for failure in failures)


def test_detects_summary_mismatch(tmp_path: Path) -> None:
    rows = tmp_path / "rows.csv"
    summary = tmp_path / "summary.csv"
    doc = tmp_path / "review.md"
    write_rows(rows)
    write_summary(summary, extractable_rows_reviewed="99")
    doc.write_text(check.DEFAULT_DOC.read_text(encoding="utf-8"), encoding="utf-8")

    failures = check.validate_cities_extractable_text_review_doc(doc, rows, summary)

    assert any("Extractable rows reviewed=99" in failure for failure in failures)


def write_rows(path: Path) -> None:
    rows = [
        ("cities_pdf_communities_data", "data_bearing_candidate"),
        ("cities_pdf_gans", "method_context_candidate"),
        ("cities_pdf_dp_365_1", "commentary_or_perspective"),
        ("cities_pdf_dp_365_2", "commentary_or_perspective"),
        ("cities_pdf_dp_365_4", "critique_or_response"),
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["label", "data_bearing_status"])
        writer.writeheader()
        for label, status in rows:
            writer.writerow({"label": label, "data_bearing_status": status})


def write_summary(path: Path, *, extractable_rows_reviewed: str = "5") -> None:
    metrics = {
        "extractable_rows_reviewed": extractable_rows_reviewed,
        "anchors_found": "5",
        "status_data_bearing_candidate": "1",
        "data_candidates_with_existing_source_shape_audit": "1",
        "gans_source_records": "66",
        "gans_source_community_rows": "210",
        "status_method_context_candidate": "1",
    }
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        for metric, value in metrics.items():
            writer.writerow({"metric": metric, "value": value})
