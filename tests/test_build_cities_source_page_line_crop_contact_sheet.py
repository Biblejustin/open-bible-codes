import csv
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from scripts import build_cities_source_page_line_crop_contact_sheet as sheets


class CitiesSourcePageLineCropContactSheetTests(unittest.TestCase):
    def test_write_contact_sheet_creates_png(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            crop = root / "line.png"
            make_image(crop)
            out = root / "sheet.png"
            args = make_args(root)

            summary = sheets.write_contact_sheet(out, [packet_row(crop, "1")], args)

            self.assertTrue(out.exists())
            self.assertGreater(summary["contact_sheet_width"], 0)
            self.assertGreater(summary["contact_sheet_height"], 0)

    def test_build_rows_keeps_zero_result_work(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            crop = root / "line.png"
            make_image(crop)
            args = make_args(root)

            rows = sheets.build_contact_sheet_rows([packet_row(crop, "1")], args)

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["source_row_import"], "0")
            self.assertEqual(rows[0]["city_name_normalization"], "0")
            self.assertEqual(rows[0]["els_runs"], "0")
            self.assertEqual(rows[0]["p_levels"], "0")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            crop = root / "line.png"
            packet = root / "packet.csv"
            out = root / "sheets.csv"
            summary = root / "summary.csv"
            markdown = root / "sheets.md"
            manifest = root / "manifest.json"
            make_image(crop)
            write_csv(packet, [packet_row(crop, "1")])

            rc = sheets.main(
                [
                    "--packet",
                    str(packet),
                    "--base-dir",
                    str(root / "contact_sheets"),
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
                "Cities Source Page Line Crop Contact Sheet",
                markdown.read_text(encoding="utf-8"),
            )
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)
            self.assertEqual(payload["line_crop_rows"], 1)


def make_args(root: Path) -> Namespace:
    return Namespace(base_dir=root / "contact_sheets", thumb_width=80, thumb_height=40, columns=1)


def make_image(path: Path) -> None:
    from PIL import Image

    Image.new("RGB", (100, 30), "white").save(path)


def packet_row(crop: Path, line_rank: str) -> dict[str, str]:
    return {
        "line_rank": line_rank,
        "transcription_decision_id": "cities_source_transcription_001",
        "page_number": "3",
        "page_class": "table_candidate_page",
        "page_line_rank": line_rank,
        "crop_path": str(crop),
        "crop_exists": str(crop.exists()).lower(),
        "ocr_word_count": "2",
        "ocr_hebrew_letters": "5",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
