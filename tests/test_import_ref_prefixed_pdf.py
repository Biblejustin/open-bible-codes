import tempfile
import unittest
from pathlib import Path

from scripts.import_ref_prefixed_pdf import main, parse_extracted_text


class RefPrefixedPdfImportTests(unittest.TestCase):
    def test_parse_extracted_text_maps_books_and_continuations(self) -> None:
        rows, meta = parse_extracted_text(
            "\n".join(
                [
                    "The Holy Bible",
                    "Gen 1:1 Alpha",
                    "continued alpha",
                    "Exo 1:1 Beta",
                ]
            )
        )

        self.assertEqual(meta["anomalies"], [])
        self.assertEqual([row.ref for row in rows], ["GEN 1:1", "EXO 1:1"])
        self.assertEqual(rows[0].text, "Alpha continued alpha")
        self.assertEqual(rows[1].book, "EXO")

    def test_parse_extracted_text_reports_unknown_book(self) -> None:
        rows, meta = parse_extracted_text("Foo 1:1 Alpha")

        self.assertEqual(rows, [])
        self.assertIn("unknown book abbreviation: Foo", meta["anomalies"])

    def test_main_writes_csv_from_synthetic_pdf_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "nlt.pdf"
            out = Path(tmp) / "nlt.csv"
            manifest = Path(tmp) / "manifest.json"
            pdf.write_bytes(b"%PDF synthetic")

            import scripts.import_ref_prefixed_pdf as importer

            saved = importer.pdftotext_text
            importer.pdftotext_text = synthetic_full_text
            try:
                exit_code = main(
                    [
                        "--pdf",
                        str(pdf),
                        "--out",
                        str(out),
                        "--manifest",
                        str(manifest),
                    ]
                )
            finally:
                importer.pdftotext_text = saved

            self.assertEqual(exit_code, 0)
            text = out.read_text(encoding="utf-8")
            self.assertIn("GEN 1:1", text)
            self.assertTrue(manifest.exists())


def synthetic_full_text(_path: Path) -> str:
    abbreviations = [
        "Gen",
        "Exo",
        "Lev",
        "Num",
        "Deu",
        "Jos",
        "Jdg",
        "Rut",
        "1Sa",
        "2Sa",
        "1Ki",
        "2Ki",
        "1Ch",
        "2Ch",
        "Ezr",
        "Neh",
        "Est",
        "Job",
        "Psa",
        "Pro",
        "Ecc",
        "Sol",
        "Isa",
        "Jer",
        "Lam",
        "Eze",
        "Dan",
        "Hos",
        "Joe",
        "Amo",
        "Oba",
        "Jon",
        "Mic",
        "Nah",
        "Hab",
        "Zep",
        "Hag",
        "Zec",
        "Mal",
        "Mat",
        "Mar",
        "Luk",
        "Joh",
        "Act",
        "Rom",
        "1Co",
        "2Co",
        "Gal",
        "Eph",
        "Phi",
        "Col",
        "1Th",
        "2Th",
        "1Ti",
        "2Ti",
        "Tit",
        "Phm",
        "Heb",
        "Jam",
        "1Pe",
        "2Pe",
        "1Jo",
        "2Jo",
        "3Jo",
        "Jud",
        "Rev",
    ]
    return "\n".join(f"{abbreviation} 1:1 Body {index}" for index, abbreviation in enumerate(abbreviations, start=1))


if __name__ == "__main__":
    unittest.main()
