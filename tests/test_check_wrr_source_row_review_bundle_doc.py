import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
import json
from pathlib import Path

from scripts import check_wrr_source_row_review_bundle_doc as check


def test_current_wrr_source_row_review_bundle_doc_passes() -> None:
    assert check.validate_source_row_review_bundle_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_source_row_review_bundle_doc(tmp_path / "missing.md")
    assert any("is missing" in failure for failure in failures)


def test_missing_boundary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_ROW_REVIEW_BUNDLE.md"
    doc.write_text("# WRR Source Row Review Bundle\n", encoding="utf-8")
    failures = check.validate_source_row_review_bundle_doc(
        doc,
        packet=None,
        summary=None,
        manifest=None,
    )
    assert any(
        "Crop and OCR availability is not transcription verification" in failure
        for failure in failures
    )


def test_matching_csvs_pass(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)

    assert (
        check.validate_source_row_review_bundle_doc(
            doc,
            packet=_packet_csv(tmp_path),
            summary=_summary_csv(tmp_path),
        )
        == []
    )


def test_summary_drift_fails(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)

    failures = check.validate_source_row_review_bundle_doc(
        doc,
        packet=_packet_csv(tmp_path),
        summary=_summary_csv(tmp_path, total_words="336"),
    )

    assert any("total_ocr_words" in failure for failure in failures)


def test_packet_review_state_drift_fails(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)

    failures = check.validate_source_row_review_bundle_doc(
        doc,
        packet=_packet_csv(tmp_path, bad_state_rank=1),
        summary=_summary_csv(tmp_path),
    )

    assert any("review state drifted" in failure for failure in failures)


def test_manifest_drift_fails(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    payload = json.loads(check.DEFAULT_MANIFEST.read_text(encoding="utf-8"))
    payload["rows"] = 99
    manifest.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    failures = check.validate_source_row_review_bundle_doc(
        check.DEFAULT_DOC,
        packet=None,
        summary=None,
        manifest=manifest,
    )

    assert any("rows drifted" in failure for failure in failures)


def _required_doc(root: Path) -> Path:
    doc = root / "packet.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    return doc


def _summary_csv(root: Path, *, total_words: str = "337") -> Path:
    path = root / "summary.csv"
    rows = {**check.EXPECTED_SUMMARY, "total_ocr_words": total_words}
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=check.SUMMARY_FIELDNAMES)
        writer.writeheader()
        for metric, value in rows.items():
            writer.writerow({"metric": metric, "value": value, "read": "test"})
    return path


def _packet_csv(root: Path, *, bad_state_rank: int | None = None) -> Path:
    path = root / "packet.csv"
    fieldnames = check.PACKET_FIELDNAMES
    action_counts = [4, 3, 3] + [2] * 10 + [1] * 6 + [4, 2, 1]
    residual_counts = action_counts.copy()
    residual_counts[13] = 2
    frontier_counts = [4, 3, 3] + [2] * 9 + [1] * 7 + [0, 0, 0]
    word_counts = [15] * 21 + [22]
    letter_counts = [44] * 20 + [46, 46]
    low_conf_counts = [3] * 20 + [9, 9]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index in range(1, 23):
            action_terms = action_counts[index - 1]
            writer.writerow(
                {
                    "run_label": "all_lanes_cap1000",
                    "row_rank": str(index),
                    "row_number": f"{index:02d}",
                    "concept": f"WRR2 {index:02d}",
                    "review_state": (
                        "bad_state"
                        if bad_state_rank == index
                        else check.REVIEW_STATE
                    ),
                    "action_terms": str(action_terms),
                    "residual_pairs": str(residual_counts[index - 1]),
                    "frontier_pairs": str(frontier_counts[index - 1]),
                    "terms_to_verify": ";".join(
                        f"term_{index}_{offset}" for offset in range(action_terms)
                    ),
                    "crop_path": (
                        "reports/wrr_1994/source_review_crops_auto/"
                        f"wrr_table2_row{index:02d}_auto.png"
                    ),
                    "crop_exists": "true",
                    "word_count": str(word_counts[index - 1]),
                    "hebrew_letter_count": str(letter_counts[index - 1]),
                    "low_conf_word_count": str(low_conf_counts[index - 1]),
                    "min_conf": "0",
                    "median_conf": "90",
                    "name_column_ocr": "שם",
                    "date_column_ocr": "תאריך",
                    "table2_bridge_read": "Hebrew cells are not verified.",
                    "no_input_boundary": check.NO_INPUT_BOUNDARY,
                    "allowed_without_input": check.ALLOWED_WITHOUT_INPUT,
                    "next_manual_action": "review crop and OCR words together",
                }
            )
    return path
