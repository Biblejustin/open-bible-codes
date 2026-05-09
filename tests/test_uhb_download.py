import tempfile
import unittest
from pathlib import Path

from scripts import download_uhb


class UhbDownloadTests(unittest.TestCase):
    def test_source_paths_are_registered(self) -> None:
        self.assertEqual(download_uhb.SOURCE_ID, "hbo_uhb")
        self.assertIn("v2.1.30", download_uhb.SOURCE_URL)
        self.assertEqual(
            download_uhb.OUT_CSV,
            Path("data/processed/unfoldingword/hbo_uhb.csv"),
        )

    def test_manifest_writer_records_license_and_counts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            zip_path = Path(tmp) / "source.zip"
            csv_path = Path(tmp) / "out.csv"
            manifest_path = Path(tmp) / "manifest.json"
            zip_path.write_bytes(b"zip")
            csv_path.write_text("ref,book,chapter,verse,text\n", encoding="utf-8")
            verses = [
                download_uhb.UsfmVerse("GEN", "1", "1", "בראשית"),
                download_uhb.UsfmVerse("EXO", "1", "1", "שמות"),
            ]

            download_uhb._write_manifest(
                manifest_path,
                source_url="https://example.test/source.zip",
                zip_path=zip_path,
                csv_path=csv_path,
                verses=verses,
            )

            manifest = manifest_path.read_text(encoding="utf-8")

        self.assertIn("CC BY-SA 4.0", manifest)
        self.assertIn('"book_count": 2', manifest)
        self.assertIn('"verse_count": 2', manifest)


if __name__ == "__main__":
    unittest.main()
