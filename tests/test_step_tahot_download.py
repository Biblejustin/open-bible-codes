import json
import tempfile
import time
import unittest
from pathlib import Path

from scripts import download_step_tahot


class StepTahotDownloadTests(unittest.TestCase):
    def test_source_paths_are_registered(self) -> None:
        self.assertEqual(download_step_tahot.SOURCE_ID, "step_tahot")
        self.assertEqual(
            download_step_tahot.OUT_CSV,
            Path("data/processed/step/tahot.csv"),
        )
        self.assertEqual(len(download_step_tahot.SOURCE_FILES), 4)
        self.assertIn("%20", download_step_tahot.tahot_raw_url("a b.txt"))

    def test_parser_groups_word_rows_by_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / download_step_tahot.SOURCE_FILES[0]
            path.write_text(
                "\n".join(
                    [
                        "header",
                        "Eng (Heb) Ref & Type\tHebrew\tTransliteration",
                        "Gen.1.1#01=L\tבְּ/רֵאשִׁ֖ית\tbe.re.Shit",
                        "Gen.1.1#02=L\tבָּרָ֣א\\׃\\ \\פ\tba.Ra'",
                        "Gen.1.2#01=Q(K)\tהָיְתָ֥ה\tha.ye.Tah",
                        "# Gen.1.2\tignored summary row",
                        "Exo.002.003#01=L\tמֹשֶׁה\tmo.Sheh",
                        "1Sa.003.010#01=L\tשְׁמוּאֵל\tshe.mu.El",
                    ]
                ),
                encoding="utf-8",
            )

            verses = download_step_tahot.parse_tahot_files([path])

        self.assertEqual(
            [verse.ref for verse in verses],
            ["Gen 1:1", "Gen 1:2", "Exod 2:3", "1Sam 3:10"],
        )
        self.assertEqual(verses[0].text, "בְּ/רֵאשִׁ֖ית בָּרָ֣א")
        self.assertEqual(verses[1].source_types, ["Q(K)"])

    def test_manifest_records_selected_text_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_path = Path(tmp) / download_step_tahot.SOURCE_FILES[0]
            raw_path.write_text("raw", encoding="utf-8")
            csv_path = Path(tmp) / "tahot.csv"
            csv_path.write_text("ref,book,chapter,verse,text\n", encoding="utf-8")
            manifest_path = Path(tmp) / "manifest.json"
            verses = [
                download_step_tahot.TahotVerse(
                    book="Gen",
                    chapter="1",
                    verse="1",
                    words=["בְּ/רֵאשִׁ֖ית"],
                    source_types=["L"],
                )
            ]

            download_step_tahot.write_manifest(
                manifest_path,
                raw_files=[raw_path],
                csv_path=csv_path,
                verses=verses,
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest_mtime_ns = manifest_path.stat().st_mtime_ns

            time.sleep(0.01)
            download_step_tahot.write_manifest(
                manifest_path,
                raw_files=[raw_path],
                csv_path=csv_path,
                verses=verses,
            )

            self.assertEqual(manifest["license"], download_step_tahot.LICENSE_LABEL)
            self.assertEqual(manifest["book_count"], 1)
            self.assertIn("paragraph markers", manifest["normalization"])
            self.assertIn("Do not treat as a pure Leningrad ketiv stream", manifest["text_policy"])
            self.assertEqual(manifest_path.stat().st_mtime_ns, manifest_mtime_ns)

    def test_write_csv_does_not_rewrite_unchanged_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "tahot.csv"
            verses = [
                download_step_tahot.TahotVerse(
                    book="Gen",
                    chapter="1",
                    verse="1",
                    words=["בראשית"],
                    source_types=["L"],
                )
            ]

            download_step_tahot.write_csv(csv_path, verses)
            first_mtime_ns = csv_path.stat().st_mtime_ns
            time.sleep(0.01)
            download_step_tahot.write_csv(csv_path, verses)

            self.assertEqual(csv_path.stat().st_mtime_ns, first_mtime_ns)


if __name__ == "__main__":
    unittest.main()
