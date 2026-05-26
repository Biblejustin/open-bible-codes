import csv
from pathlib import Path

from scripts import check_cities_source_review_queue_doc as check


def test_current_cities_source_review_queue_doc_passes() -> None:
    assert check.validate_cities_source_review_queue_doc(check.DEFAULT_DOC) == []


def test_detects_missing_boundary_phrase(tmp_path: Path) -> None:
    queue = tmp_path / "queue.csv"
    summary = tmp_path / "summary.csv"
    doc = tmp_path / "queue.md"
    write_queue(queue)
    write_summary(summary)
    doc.write_text("# Cities Source Review Queue\n", encoding="utf-8")

    failures = check.validate_cities_source_review_queue_doc(doc, queue, summary)

    assert any("missing phrase" in failure for failure in failures)


def test_detects_lane_count_mismatch(tmp_path: Path) -> None:
    queue = tmp_path / "queue.csv"
    summary = tmp_path / "summary.csv"
    doc = tmp_path / "queue.md"
    write_queue(queue)
    write_summary(summary, review_extractable_text="99")
    doc.write_text(check.DEFAULT_DOC.read_text(encoding="utf-8"), encoding="utf-8")

    failures = check.validate_cities_source_review_queue_doc(doc, queue, summary)

    assert any("review_extractable_text=99" in failure for failure in failures)


def write_queue(path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["lane"])
        writer.writeheader()
        for lane in check.EXPECTED_LANES:
            writer.writerow({"lane": lane})


def write_summary(path: Path, *, review_extractable_text: str = "5") -> None:
    counts = {
        "review_extractable_text": review_extractable_text,
        "ocr_image_only_pdf": "4",
        "encoding_or_ocr_candidate": "3",
        "recover_missing_pdf": "23",
    }
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["lane", "rows"])
        writer.writeheader()
        for lane in check.EXPECTED_LANES:
            writer.writerow({"lane": lane, "rows": counts[lane]})
