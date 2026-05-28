import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_source_page_line_crop_triage as triage


class CitiesSourcePageLineCropTriageTests(unittest.TestCase):
    def test_classify_line_crop_uses_counts_without_transcription(self) -> None:
        self.assertEqual(
            triage.classify_line_crop(
                word_count=8,
                hebrew_letters=31,
                line_width=500,
                line_height=25,
                crop_height=40,
            )[0],
            "priority_1_dense_text",
        )
        self.assertEqual(
            triage.classify_line_crop(
                word_count=0,
                hebrew_letters=0,
                line_width=0,
                line_height=0,
                crop_height=0,
            )[1],
            "noise_or_blank",
        )

    def test_build_triage_rows_sorts_dense_first_and_keeps_zero_result_fields(self) -> None:
        rows = triage.build_triage_rows(
            [
                packet_row("1", words="1", letters="4"),
                packet_row("2", words="7", letters="28"),
            ]
        )

        self.assertEqual(rows[0]["line_rank"], "2")
        self.assertEqual(rows[0]["review_priority"], "priority_1_dense_text")
        self.assertEqual(rows[0]["source_row_import"], "0")
        self.assertEqual(rows[0]["city_name_normalization"], "0")
        self.assertEqual(rows[0]["els_runs"], "0")
        self.assertEqual(rows[0]["p_levels"], "0")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packet = root / "packet.csv"
            out = root / "triage.csv"
            summary = root / "summary.csv"
            markdown = root / "triage.md"
            manifest = root / "manifest.json"
            write_csv(packet, [packet_row("1"), packet_row("2", words="0", letters="0")])

            rc = triage.main(
                [
                    "--packet",
                    str(packet),
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
            self.assertIn(
                "Cities Source Page Line Crop Triage",
                markdown.read_text(encoding="utf-8"),
            )
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 2)
            self.assertEqual(payload["source_row_imports"], 0)


def packet_row(line_rank: str, *, words: str = "4", letters: str = "16") -> dict[str, str]:
    return {
        "line_rank": line_rank,
        "transcription_decision_id": "cities_source_transcription_001",
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "3",
        "page_class": "table_candidate_page",
        "page_line_rank": line_rank,
        "crop_path": f"line{line_rank}.png",
        "crop_exists": "true",
        "line_width": "500",
        "line_height": "24",
        "crop_height": "36",
        "ocr_word_count": words,
        "ocr_hebrew_letters": letters,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
