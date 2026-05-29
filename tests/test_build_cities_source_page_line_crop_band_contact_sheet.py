import csv
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from scripts import build_cities_source_page_line_crop_band_contact_sheet as sheets
from scripts import build_cities_source_page_line_crop_band_review_worksheet as band_review
from scripts import build_cities_source_page_line_crop_packet as packet


class CitiesSourcePageLineCropBandContactSheetTests(unittest.TestCase):
    def test_write_contact_sheet_creates_png_for_band(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            crop = root / "line.png"
            make_image(crop)
            out = root / "band.png"
            args = make_args(root)

            summary = sheets.write_contact_sheet(
                out,
                band_row("1", first="1", last="1"),
                [packet_row(crop, "1")],
                args,
            )

            self.assertTrue(out.exists())
            self.assertGreater(summary["contact_sheet_width"], 0)
            self.assertGreater(summary["contact_sheet_height"], 0)

    def test_build_rows_keeps_zero_result_work(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            crop = root / "line.png"
            make_image(crop)
            args = make_args(root)

            rows = sheets.build_band_sheet_rows(
                [packet_row(crop, "1"), packet_row(crop, "2")],
                [band_row("1", first="1", last="1")],
                args,
            )

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["band_review_id"], "cities_source_band_review_001")
            self.assertEqual(rows[0]["line_crop_rows"], "1")
            self.assertEqual(rows[0]["source_row_import"], "0")
            self.assertEqual(rows[0]["city_name_normalization"], "0")
            self.assertEqual(rows[0]["els_runs"], "0")
            self.assertEqual(rows[0]["p_levels"], "0")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            crop = root / "line.png"
            packet_csv = root / "packet.csv"
            band_csv = root / "bands.csv"
            out = root / "sheets.csv"
            summary = root / "summary.csv"
            markdown = root / "sheets.md"
            manifest = root / "manifest.json"
            make_image(crop)
            write_csv(packet_csv, packet.FIELDNAMES, [packet_row(crop, "1")])
            write_csv(band_csv, band_review.FIELDNAMES, [band_row("1", first="1", last="1")])

            rc = sheets.main(
                [
                    "--packet",
                    str(packet_csv),
                    "--band-review",
                    str(band_csv),
                    "--base-dir",
                    str(root / "band_sheets"),
                    "--out",
                    str(out),
                    "--summary-out",
                    str(summary),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                    "--thumb-width",
                    "80",
                    "--thumb-height",
                    "40",
                ]
            )

            self.assertEqual(rc, 0)
            self.assertTrue(out.exists())
            self.assertIn(
                "Cities Source Page Line Crop Band Contact Sheet",
                markdown.read_text(encoding="utf-8"),
            )
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)
            self.assertEqual(payload["line_crop_rows"], 1)


def make_args(root: Path) -> Namespace:
    return Namespace(base_dir=root / "band_sheets", thumb_width=80, thumb_height=40, columns=1)


def make_image(path: Path) -> None:
    from PIL import Image

    Image.new("RGB", (100, 30), "white").save(path)


def packet_row(crop: Path, rank: str) -> dict[str, str]:
    return {
        "line_rank": rank,
        "transcription_decision_id": "cities_source_transcription_001",
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "3",
        "page_class": "table_candidate_page",
        "page_line_rank": rank,
        "crop_path": str(crop),
        "crop_exists": str(crop.exists()).lower(),
        "line_width": "500",
        "line_height": "24",
        "crop_height": "36",
        "ocr_word_count": "2",
        "ocr_hebrew_letters": "5",
        "next_manual_action": "review crop image",
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "no_input_boundary": packet.NO_INPUT_BOUNDARY,
    }


def band_row(rank: str, *, first: str, last: str) -> dict[str, str]:
    return {
        "review_rank": rank,
        "band_review_id": f"cities_source_band_review_{int(rank):03d}",
        "band_rank": rank,
        "band_id": f"cities_source_line_band_{int(rank):03d}",
        "transcription_decision_id": "cities_source_transcription_001",
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "3",
        "page_class": "table_candidate_page",
        "page_band_rank": rank,
        "gap_threshold_px": "40",
        "gap_before_band_px": "0",
        "first_line_rank": first,
        "last_line_rank": last,
        "first_page_line_rank": first,
        "last_page_line_rank": last,
        "line_crop_rows": str(int(last) - int(first) + 1),
        "crop_images_available": str(int(last) - int(first) + 1),
        "band_top": "10",
        "band_bottom": "50",
        "band_height": "40",
        "max_internal_gap_px": "5",
        "ocr_word_count": "2",
        "ocr_hebrew_letters": "5",
        "dominant_review_priority": "priority_1_dense_text",
        "review_state": band_review.REVIEW_STATE,
        "required_comparison": "compare before import",
        "allowed_without_input": "organize coordinate-band visual review only",
        "next_manual_action": "review only",
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "claim_boundary": band_review.CLAIM_BOUNDARY,
    }


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
