import csv
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

from scripts import build_cities_source_page_line_crop_packet as crops


TSV_TEXT = """level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext
5\t1\t1\t1\t1\t1\t10\t20\t30\t8\t90\tאבג
5\t1\t1\t1\t1\t2\t50\t21\t20\t8\t90\tדה
5\t1\t1\t1\t2\t1\t15\t50\t25\t8\t90\tוזח
"""


class CitiesSourcePageLineCropPacketTests(unittest.TestCase):
    def test_build_line_boxes_groups_tsv_words(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "page.tsv"
            path.write_text(TSV_TEXT, encoding="utf-8")

            boxes = crops.build_line_boxes(crops.read_tsv_words(path))

            self.assertEqual(len(boxes), 2)
            self.assertEqual(boxes[0].word_count, 2)
            self.assertEqual(boxes[0].hebrew_letters, 5)
            self.assertEqual((boxes[0].left, boxes[0].top, boxes[0].right), (10, 20, 70))

    def test_build_page_crop_rows_writes_crops_without_imports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "page.png"
            make_image(image)
            args = make_args(root)

            def fake_tsv(_image_path: Path, tsv_path: Path, _args: Namespace) -> None:
                tsv_path.parent.mkdir(parents=True, exist_ok=True)
                tsv_path.write_text(TSV_TEXT, encoding="utf-8")

            with patch.object(crops.shutil, "which", return_value="/usr/bin/tesseract"):
                with patch.object(crops, "run_tesseract_tsv", side_effect=fake_tsv):
                    rows = crops.build_crop_rows([packet_row(image)], args)

            self.assertEqual(len(rows), 2)
            self.assertTrue(Path(rows[0]["crop_path"]).exists())
            self.assertEqual(rows[0]["source_row_import"], "0")
            self.assertEqual(rows[0]["city_name_normalization"], "0")
            self.assertEqual(rows[0]["els_runs"], "0")

    def test_summary_keeps_zero_result_work(self) -> None:
        args = make_args(Path("/tmp"))
        rows = [
            {
                "crop_exists": "true",
                "tsv_path": "a.tsv",
                "tsv_exists": "true",
                "ocr_word_count": "2",
                "ocr_hebrew_letters": "5",
            }
        ]
        summary = {row["metric"]: row["value"] for row in crops.build_summary_rows([{}], rows, args)}

        self.assertEqual(summary["source_row_imports"], "0")
        self.assertEqual(summary["city_name_normalization"], "0")
        self.assertEqual(summary["els_runs"], "0")
        self.assertEqual(summary["p_levels"], "0")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "page.png"
            packet = root / "packet.csv"
            out = root / "packet_out.csv"
            summary = root / "summary.csv"
            markdown = root / "line_crops.md"
            manifest = root / "manifest.json"
            make_image(image)
            write_csv(packet, [packet_row(image)])

            def fake_tsv(_image_path: Path, tsv_path: Path, _args: Namespace) -> None:
                tsv_path.parent.mkdir(parents=True, exist_ok=True)
                tsv_path.write_text(TSV_TEXT, encoding="utf-8")

            with patch.object(crops.shutil, "which", return_value="/usr/bin/tesseract"):
                with patch.object(crops, "run_tesseract_tsv", side_effect=fake_tsv):
                    rc = crops.main(
                        [
                            "--packet",
                            str(packet),
                            "--base-dir",
                            str(root / "crops"),
                            "--tessdata-dir",
                            str(make_tessdata(root)),
                            "--out",
                            str(out),
                            "--summary-out",
                            str(summary),
                            "--markdown-out",
                            str(markdown),
                            "--manifest-out",
                            str(manifest),
                        ]
                    )

            self.assertEqual(rc, 0)
            self.assertTrue(out.exists())
            self.assertIn("Cities Source Page Line Crop Packet", markdown.read_text(encoding="utf-8"))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 2)


def make_args(root: Path) -> Namespace:
    return Namespace(
        base_dir=root / "line_crops",
        tessdata_dir=make_tessdata(root),
        language="heb",
        psm="4",
        refresh_ocr=True,
        line_padding_y=6,
    )


def make_tessdata(root: Path) -> Path:
    tessdata = root / "tessdata"
    tessdata.mkdir(parents=True, exist_ok=True)
    (tessdata / "heb.traineddata").write_bytes(b"fake")
    return tessdata


def make_image(path: Path) -> None:
    from PIL import Image

    Image.new("RGB", (120, 100), "white").save(path)


def packet_row(image: Path) -> dict[str, str]:
    return {
        "transcription_decision_id": "cities_source_transcription_001",
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "3",
        "page_class": "table_candidate_page",
        "page_image_path": str(image),
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
