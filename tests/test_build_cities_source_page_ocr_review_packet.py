import csv
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

from scripts import build_cities_source_page_ocr_review_packet as packet


class CitiesSourcePageOcrReviewPacketTests(unittest.TestCase):
    def test_build_rows_writes_local_sidecar_without_imports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "page.png"
            image.write_bytes(b"png")
            args = make_args(root)

            with patch.object(packet.shutil, "which", return_value="/usr/bin/tesseract"):
                with patch.object(packet, "run_tesseract", return_value="אבגדהוזחטיכלמנסעפצקרשת"):
                    rows = packet.build_ocr_packet_rows([bundle_row(image)], args)

            self.assertEqual(rows[0]["ocr_status"], "source_page_ocr_text_detected")
            self.assertEqual(rows[0]["ocr_text_exists"], "true")
            self.assertEqual(rows[0]["source_row_import"], "0")
            self.assertEqual(rows[0]["city_name_normalization"], "0")
            self.assertTrue(Path(rows[0]["ocr_text_path"]).exists())

    def test_missing_tessdata_blocks_without_ocr(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "page.png"
            image.write_bytes(b"png")
            args = make_args(root, create_tessdata=False)

            with patch.object(packet.shutil, "which", return_value="/usr/bin/tesseract"):
                with patch.object(packet, "run_tesseract") as run_ocr:
                    rows = packet.build_ocr_packet_rows([bundle_row(image)], args)

            self.assertEqual(rows[0]["ocr_status"], "blocked_missing_ocr_dependency")
            self.assertEqual(rows[0]["ocr_text_exists"], "false")
            run_ocr.assert_not_called()

    def test_summary_keeps_zero_result_work(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            args = make_args(Path(tmp))
            rows = [
                {
                    "ocr_status": "source_page_ocr_text_detected",
                    "page_image_exists": "true",
                    "ocr_text_exists": "true",
                    "ocr_text_signal_chars": "10",
                    "ocr_hebrew_letters": "9",
                    "ocr_word_count": "3",
                    "ocr_line_count": "2",
                }
            ]
            summary = {row["metric"]: row["value"] for row in packet.build_summary_rows(rows, args)}

            self.assertEqual(summary["source_row_imports"], "0")
            self.assertEqual(summary["city_name_normalization"], "0")
            self.assertEqual(summary["els_runs"], "0")
            self.assertEqual(summary["p_levels"], "0")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "page.png"
            image.write_bytes(b"png")
            bundle = root / "bundle.csv"
            out = root / "packet.csv"
            summary = root / "summary.csv"
            markdown = root / "packet.md"
            manifest = root / "manifest.json"
            write_csv(bundle, [bundle_row(image)])

            with patch.object(packet.shutil, "which", return_value="/usr/bin/tesseract"):
                with patch.object(packet, "run_tesseract", return_value="אבגדהוזחטיכלמנסעפצקרשת"):
                    rc = packet.main(
                        [
                            "--bundle",
                            str(bundle),
                            "--base-dir",
                            str(root / "ocr"),
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
            self.assertIn("Cities Source Page OCR Review Packet", markdown.read_text(encoding="utf-8"))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)


def make_args(root: Path, *, create_tessdata: bool = True) -> Namespace:
    return Namespace(
        base_dir=root / "ocr",
        tessdata_dir=make_tessdata(root) if create_tessdata else root / "missing_tessdata",
        language="heb",
        psm="4",
        refresh_ocr=True,
    )


def make_tessdata(root: Path) -> Path:
    tessdata = root / "tessdata"
    tessdata.mkdir(parents=True, exist_ok=True)
    (tessdata / "heb.traineddata").write_bytes(b"fake")
    return tessdata


def bundle_row(image: Path) -> dict[str, str]:
    return {
        "bundle_rank": "1",
        "transcription_decision_id": "cities_source_transcription_001",
        "source_lock_decision_id": "cities_source_row_lock_001",
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "3",
        "page_class": "table_candidate_page",
        "page_image_path": str(image),
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
