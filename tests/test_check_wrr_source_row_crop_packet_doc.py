import csv
from pathlib import Path

from scripts import check_wrr_source_row_crop_packet_doc as check


def test_current_wrr_source_row_crop_packet_doc_passes() -> None:
    assert check.validate_source_row_crop_packet_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_source_row_crop_packet_doc(tmp_path / "missing.md")
    assert any("is missing" in failure for failure in failures)


def test_missing_boundary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_ROW_CROP_PACKET.md"
    doc.write_text("# WRR Source Row Crop Packet\n", encoding="utf-8")
    failures = check.validate_source_row_crop_packet_doc(
        doc,
        packet=None,
        summary=None,
    )
    assert any(
        "Crop availability is not transcription verification" in failure
        for failure in failures
    )


def test_matching_csvs_pass(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)

    assert (
        check.validate_source_row_crop_packet_doc(
            doc,
            packet=_packet_csv(tmp_path),
            summary=_summary_csv(tmp_path),
        )
        == []
    )


def test_summary_drift_fails(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)

    failures = check.validate_source_row_crop_packet_doc(
        doc,
        packet=_packet_csv(tmp_path),
        summary=_summary_csv(tmp_path, auto_crops="21"),
    )

    assert any("auto_crops_available" in failure for failure in failures)


def test_packet_missing_crop_fails(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)

    failures = check.validate_source_row_crop_packet_doc(
        doc,
        packet=_packet_csv(tmp_path, missing_crop_rank=1),
        summary=_summary_csv(tmp_path),
    )

    assert any("auto crops available=21" in failure for failure in failures)


def _required_doc(root: Path) -> Path:
    doc = root / "packet.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    return doc


def _summary_csv(root: Path, *, auto_crops: str = "22") -> Path:
    path = root / "summary.csv"
    rows = {**check.EXPECTED_SUMMARY, "auto_crops_available": auto_crops}
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value", "read"])
        writer.writeheader()
        for metric, value in rows.items():
            writer.writerow({"metric": metric, "value": value, "read": "test"})
    return path


def _packet_csv(root: Path, *, missing_crop_rank: int | None = None) -> Path:
    path = root / "packet.csv"
    fieldnames = [
        "run_label",
        "row_rank",
        "row_number",
        "concept",
        "action_terms",
        "frontier_pairs",
        "row_band_top",
        "row_band_bottom",
        "crop_left",
        "crop_top",
        "crop_right",
        "crop_bottom",
        "crop_width",
        "crop_height",
        "crop_path",
        "crop_exists",
        "crop_status",
        "manual_crop_count",
        "manual_crop_paths",
        "no_input_boundary",
        "next_manual_action",
    ]
    action_counts = [4, 3, 3] + [2] * 10 + [1] * 6 + [4, 2, 1]
    frontier_counts = [4, 3, 3] + [2] * 9 + [1] * 7 + [0, 0, 0]
    manual_ranks = {11, 14, 20, 21}
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index in range(1, 23):
            manual_count = 1 if index in manual_ranks else 0
            writer.writerow(
                {
                    "run_label": "all_lanes_cap1000",
                    "row_rank": str(index),
                    "row_number": f"{index:02d}",
                    "concept": f"WRR2 {index:02d}",
                    "action_terms": str(action_counts[index - 1]),
                    "frontier_pairs": str(frontier_counts[index - 1]),
                    "row_band_top": "100.0",
                    "row_band_bottom": "200.0",
                    "crop_left": "500",
                    "crop_top": "100",
                    "crop_right": "2050",
                    "crop_bottom": "200",
                    "crop_width": "1550",
                    "crop_height": "100",
                    "crop_path": (
                        "reports/wrr_1994/source_review_crops_auto/"
                        f"wrr_table2_row{index:02d}_auto.png"
                    ),
                    "crop_exists": (
                        "false" if missing_crop_rank == index else "true"
                    ),
                    "crop_status": check.CROP_STATUS,
                    "manual_crop_count": str(manual_count),
                    "manual_crop_paths": (
                        f"reports/wrr_1994/source_review_crops/row{index:02d}.png"
                        if manual_count
                        else ""
                    ),
                    "no_input_boundary": check.NO_INPUT_BOUNDARY,
                    "next_manual_action": "inspect generated crop",
                }
            )
    return path
