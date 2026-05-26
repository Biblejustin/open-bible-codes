import csv
from pathlib import Path

from scripts import check_wrr_source_row_ocr_word_packet_doc as check


def test_current_wrr_source_row_ocr_word_packet_doc_passes() -> None:
    assert check.validate_source_row_ocr_word_packet_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_source_row_ocr_word_packet_doc(tmp_path / "missing.md")
    assert any("is missing" in failure for failure in failures)


def test_missing_boundary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_ROW_OCR_WORD_PACKET.md"
    doc.write_text("# WRR Source Row OCR Word Packet\n", encoding="utf-8")
    failures = check.validate_source_row_ocr_word_packet_doc(
        doc,
        packet=None,
        summary=None,
    )
    assert any("not transcription verification" in failure for failure in failures)


def test_matching_csvs_pass(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)

    assert (
        check.validate_source_row_ocr_word_packet_doc(
            doc,
            packet=_packet_csv(tmp_path),
            summary=_summary_csv(tmp_path),
        )
        == []
    )


def test_summary_drift_fails(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)

    failures = check.validate_source_row_ocr_word_packet_doc(
        doc,
        packet=_packet_csv(tmp_path),
        summary=_summary_csv(tmp_path, total_words="336"),
    )

    assert any("total_ocr_words" in failure for failure in failures)


def test_packet_zero_word_row_fails(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)

    failures = check.validate_source_row_ocr_word_packet_doc(
        doc,
        packet=_packet_csv(tmp_path, zero_word_rank=1),
        summary=_summary_csv(tmp_path),
    )

    assert any("has no OCR words" in failure for failure in failures)


def _required_doc(root: Path) -> Path:
    doc = root / "packet.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    return doc


def _summary_csv(root: Path, *, total_words: str = "337") -> Path:
    path = root / "summary.csv"
    rows = {**check.EXPECTED_SUMMARY, "total_ocr_words": total_words}
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value", "read"])
        writer.writeheader()
        for metric, value in rows.items():
            writer.writerow({"metric": metric, "value": value, "read": "test"})
    return path


def _packet_csv(root: Path, *, zero_word_rank: int | None = None) -> Path:
    path = root / "packet.csv"
    fieldnames = [
        "run_label",
        "row_rank",
        "row_number",
        "concept",
        "frontier_pairs",
        "row_band_top",
        "row_band_bottom",
        "crop_path",
        "name_tokens_rtl",
        "name_normalized",
        "date_tokens_rtl",
        "date_normalized",
        "all_tokens_rtl",
        "all_normalized",
        "word_count",
        "hebrew_letter_count",
        "low_conf_word_count",
        "min_conf",
        "median_conf",
        "no_input_boundary",
        "next_manual_action",
    ]
    word_counts = [15] * 21 + [22]
    letter_counts = [44] * 20 + [46, 46]
    low_conf_counts = [3] * 20 + [9, 9]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index in range(1, 23):
            word_count = 0 if zero_word_rank == index else word_counts[index - 1]
            writer.writerow(
                {
                    "run_label": "all_lanes_cap1000",
                    "row_rank": str(index),
                    "row_number": f"{index:02d}",
                    "concept": f"WRR2 {index:02d}",
                    "frontier_pairs": "1" if index <= 19 else "0",
                    "row_band_top": "100.0",
                    "row_band_bottom": "200.0",
                    "crop_path": (
                        "reports/wrr_1994/source_review_crops_auto/"
                        f"wrr_table2_row{index:02d}_auto.png"
                    ),
                    "name_tokens_rtl": "שם",
                    "name_normalized": "שמ",
                    "date_tokens_rtl": "תאריך",
                    "date_normalized": "תאריכ",
                    "all_tokens_rtl": "שם תאריך",
                    "all_normalized": "שמתאריכ",
                    "word_count": str(word_count),
                    "hebrew_letter_count": str(letter_counts[index - 1]),
                    "low_conf_word_count": str(low_conf_counts[index - 1]),
                    "min_conf": "0",
                    "median_conf": "90",
                    "no_input_boundary": check.NO_INPUT_BOUNDARY,
                    "next_manual_action": "compare OCR words with crop",
                }
            )
    return path
