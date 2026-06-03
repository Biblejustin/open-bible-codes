import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
import json
import struct
from pathlib import Path

from scripts import check_wrr_source_row_crop_contact_sheet_doc as check


def test_current_wrr_source_row_crop_contact_sheet_doc_passes() -> None:
    assert check.validate_source_row_crop_contact_sheet_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_source_row_crop_contact_sheet_doc(tmp_path / "missing.md")
    assert any("is missing" in failure for failure in failures)


def test_missing_boundary_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_ROW_CROP_CONTACT_SHEET.md"
    doc.write_text("# WRR Source Row Crop Contact Sheet\n", encoding="utf-8")
    failures = check.validate_source_row_crop_contact_sheet_doc(doc, image=None)
    assert any("not transcription verification" in failure for failure in failures)


def test_matching_doc_and_png_pass(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)
    image = _png(tmp_path, check.EXPECTED_DIMENSIONS)

    assert (
        check.validate_source_row_crop_contact_sheet_doc(
            doc,
            image=image,
            rows=_rows_csv(tmp_path),
            summary=_summary_csv(tmp_path),
            manifest=_manifest(tmp_path),
        )
        == []
    )


def test_bad_png_dimensions_fail(tmp_path: Path) -> None:
    doc = _required_doc(tmp_path)
    image = _png(tmp_path, (100, 50))

    failures = check.validate_source_row_crop_contact_sheet_doc(
        doc,
        image=image,
        rows=None,
        summary=None,
        manifest=None,
    )

    assert any("expected" in failure for failure in failures)


def test_rows_csv_drift_fails(tmp_path: Path) -> None:
    failures = check.validate_source_row_crop_contact_sheet_doc(
        _required_doc(tmp_path),
        image=_png(tmp_path, check.EXPECTED_DIMENSIONS),
        rows=_rows_csv(tmp_path, bad_rank="1"),
        summary=_summary_csv(tmp_path),
        manifest=_manifest(tmp_path),
    )

    assert any("rank 1 action_terms drifted" in failure for failure in failures)


def test_summary_csv_drift_fails(tmp_path: Path) -> None:
    failures = check.validate_source_row_crop_contact_sheet_doc(
        _required_doc(tmp_path),
        image=_png(tmp_path, check.EXPECTED_DIMENSIONS),
        rows=_rows_csv(tmp_path),
        summary=_summary_csv(tmp_path, bad_metric="contact_sheet_rows"),
        manifest=_manifest(tmp_path),
    )

    assert any("contact_sheet_rows value drifted" in failure for failure in failures)


def test_manifest_drift_fails(tmp_path: Path) -> None:
    failures = check.validate_source_row_crop_contact_sheet_doc(
        _required_doc(tmp_path),
        image=_png(tmp_path, check.EXPECTED_DIMENSIONS),
        rows=_rows_csv(tmp_path),
        summary=_summary_csv(tmp_path),
        manifest=_manifest(tmp_path, bad_width=True),
    )

    assert any("contact_sheet contact_sheet_width drifted" in failure for failure in failures)


def _required_doc(root: Path) -> Path:
    doc = root / "WRR_SOURCE_ROW_CROP_CONTACT_SHEET.md"
    lines = list(check.REQUIRED_PHRASES)
    for rank, row_number, action_terms, frontier_pairs in check.EXPECTED_ROW_ORDER:
        lines.append(
            f"| {rank} | `{row_number}` | {action_terms} | {frontier_pairs} | "
            f"`{check.crop_path(row_number)}` |"
        )
    doc.write_text("\n".join(lines), encoding="utf-8")
    return doc


def _png(root: Path, dimensions: tuple[int, int]) -> Path:
    image = root / "contact.png"
    width, height = dimensions
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    image.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + struct.pack(">I4s", len(ihdr), b"IHDR")
        + ihdr
        + b"\x00\x00\x00\x00"
    )
    return image


def _rows_csv(tmp_path: Path, *, bad_rank: str | None = None) -> Path:
    path = tmp_path / "wrr_source_row_crop_packet.csv"
    rows = []
    for rank, row_number, action_terms, frontier_pairs in check.EXPECTED_ROW_ORDER:
        manual_count = check.EXPECTED_MANUAL_CROP_COUNTS.get(row_number, "0")
        next_action = (
            "keep crop as later review aid unless policy scope changes"
            if frontier_pairs == "0"
            else "inspect generated crop against source row before any frontier source decision"
        )
        rows.append(
            {
                "run_label": "all_lanes_cap1000",
                "row_rank": rank,
                "row_number": row_number,
                "concept": f"WRR2 {row_number}",
                "action_terms": "99" if rank == bad_rank else action_terms,
                "frontier_pairs": frontier_pairs,
                "row_band_top": "1.00",
                "row_band_bottom": "2.00",
                "crop_left": "500",
                "crop_top": "1",
                "crop_right": "2050",
                "crop_bottom": "2",
                "crop_width": "1550",
                "crop_height": "1",
                "crop_path": check.crop_path(row_number),
                "crop_exists": "true",
                "crop_status": "written_review_aid_only",
                "manual_crop_count": manual_count,
                "manual_crop_paths": (
                    f"reports/wrr_1994/source_review_crops/wrr_table2_row{row_number}.png"
                    if manual_count != "0"
                    else ""
                ),
                "no_input_boundary": check.NO_INPUT_BOUNDARY,
                "next_manual_action": next_action,
            }
        )
    return _write_csv(path, check.FIELDNAMES, rows)


def _summary_csv(tmp_path: Path, *, bad_metric: str | None = None) -> Path:
    path = tmp_path / "wrr_source_row_crop_packet_summary.csv"
    rows = []
    for metric, (value, read) in check.EXPECTED_SUMMARY.items():
        rows.append(
            {
                "metric": metric,
                "value": "99" if metric == bad_metric else value,
                "read": read,
            }
        )
    return _write_csv(path, check.SUMMARY_FIELDNAMES, rows)


def _manifest(tmp_path: Path, *, bad_width: bool = False) -> Path:
    path = tmp_path / "wrr_source_row_crop_packet.manifest.json"
    path.write_text(
        json.dumps(
            {
                "rows": len(check.EXPECTED_ROW_ORDER),
                "summary": {
                    metric: int(value) if value.isdigit() else value
                    for metric, (value, _read) in check.EXPECTED_SUMMARY.items()
                },
                "contact_sheet": {
                    "contact_sheet_exists": True,
                    "contact_sheet_path": str(check.DEFAULT_IMAGE),
                    "contact_sheet_rows": len(check.EXPECTED_ROW_ORDER),
                    "contact_sheet_width": (
                        99 if bad_width else check.EXPECTED_DIMENSIONS[0]
                    ),
                    "contact_sheet_height": check.EXPECTED_DIMENSIONS[1],
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def _write_csv(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, str]],
) -> Path:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path
