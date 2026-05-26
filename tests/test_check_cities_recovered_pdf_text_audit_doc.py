import csv
from pathlib import Path

from scripts import check_cities_recovered_pdf_text_audit_doc as check


def test_current_cities_recovered_pdf_text_audit_doc_passes() -> None:
    assert check.validate_cities_recovered_pdf_text_audit_doc(check.DEFAULT_DOC) == []


def test_detects_missing_boundary_phrase(tmp_path: Path) -> None:
    rows = tmp_path / "rows.csv"
    summary = tmp_path / "summary.csv"
    anchors = tmp_path / "anchors.csv"
    doc = tmp_path / "audit.md"
    write_rows(rows)
    write_summary(summary)
    write_anchors(anchors)
    doc.write_text("# Cities Recovered PDF Text Audit\n", encoding="utf-8")

    failures = check.validate_cities_recovered_pdf_text_audit_doc(
        doc,
        rows,
        summary,
        anchors,
    )

    assert any("missing phrase" in failure for failure in failures)


def test_detects_summary_count_mismatch(tmp_path: Path) -> None:
    rows = tmp_path / "rows.csv"
    summary = tmp_path / "summary.csv"
    anchors = tmp_path / "anchors.csv"
    doc = tmp_path / "audit.md"
    write_rows(rows)
    write_summary(summary, recovered_pdf_rows="99")
    write_anchors(anchors)
    doc.write_text(check.DEFAULT_DOC.read_text(encoding="utf-8"), encoding="utf-8")

    failures = check.validate_cities_recovered_pdf_text_audit_doc(
        doc,
        rows,
        summary,
        anchors,
    )

    assert any("recovered PDF rows audited=99" in failure for failure in failures)


def write_rows(path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["label", "text_status"])
        writer.writeheader()
        writer.writerows(
            [
                {"label": "cities_pdf_wrr", "text_status": "zero_extractable_text"},
                {
                    "label": "cities_pdf_dp365a_p1_4",
                    "text_status": "extractable_but_garbled_or_nonlatin",
                },
                {"label": "cities_pdf_communities_data", "text_status": "extractable_text"},
                {"label": "cities_pdf_gans", "text_status": "extractable_text"},
            ]
        )


def write_summary(path: Path, *, recovered_pdf_rows: str = "12") -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "recovered_pdf_rows",
                "extractable_text_rows",
                "zero_text_rows",
                "garbled_or_nonlatin_rows",
                "gans_family_rows",
                "aumann_family_rows",
                "other_family_rows",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "recovered_pdf_rows": recovered_pdf_rows,
                "extractable_text_rows": "5",
                "zero_text_rows": "4",
                "garbled_or_nonlatin_rows": "3",
                "gans_family_rows": "2",
                "aumann_family_rows": "9",
                "other_family_rows": "1",
            }
        )


def write_anchors(path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["anchor", "label", "status"])
        writer.writeheader()
        for index in range(5):
            writer.writerow(
                {
                    "anchor": f"anchor_{index}",
                    "label": "cities_pdf_gans",
                    "status": "found",
                }
            )
