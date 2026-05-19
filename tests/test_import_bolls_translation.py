import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.import_bolls_translation import (
    build_book_maps,
    clean_html_text,
    import_translation,
    main,
)


class BollsTranslationImportTests(unittest.TestCase):
    def test_clean_html_text_removes_sup_and_strong_numbers(self) -> None:
        text = clean_html_text("Alpha<sup>[1]</sup> <S>7225</S><i>Beta</i><br>Gamma")

        self.assertEqual(text, "Alpha Beta Gamma")

    def test_build_book_maps_disambiguates_apocrypha_by_name(self) -> None:
        books = [
            {"bookid": 1, "name": "Genesis", "chapters": 1},
            {"bookid": 76, "name": "3 Maccabees", "chapters": 1},
            {"bookid": 83, "name": "Prayer of Manasseh", "chapters": 1},
        ]

        book_id_to_code, book_order, _book_names, anomalies = build_book_maps(books)

        self.assertEqual(anomalies, [])
        self.assertEqual(book_id_to_code[76], "3MA")
        self.assertEqual(book_id_to_code[83], "MAN")
        self.assertEqual(list(book_order), ["GEN", "3MA", "MAN"])

    def test_import_translation_reads_zip_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / "sample.zip"
            books = base / "books.json"
            languages = base / "languages.json"
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr(
                    "sample.json",
                    json.dumps(
                        [
                            {
                                "translation": "TEST",
                                "book": 1,
                                "chapter": 1,
                                "verse": 1,
                                "text": "Alpha<sup>1</sup>",
                            },
                            {
                                "translation": "TEST",
                                "book": 68,
                                "chapter": 1,
                                "verse": 1,
                                "text": "Beta",
                            },
                        ]
                    ),
                )
            books.write_text(
                json.dumps(
                    {
                        "TEST": [
                            {"bookid": 1, "name": "Genesis", "chapters": 1},
                            {"bookid": 68, "name": "Tobit", "chapters": 1},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            languages.write_text(
                json.dumps(
                    [
                        {
                            "language": "English",
                            "translations": [
                                {
                                    "short_name": "TEST",
                                    "full_name": "Test Translation",
                                    "updated": 1,
                                }
                            ],
                        }
                    ]
                ),
                encoding="utf-8",
            )

            rows, manifest = import_translation(
                slug="TEST",
                label="TEST",
                source_file=source,
                source_url="https://example.test/source.zip",
                books_file=books,
                books_url="https://example.test/books.json",
                languages_file=languages,
                languages_url="https://example.test/languages.json",
            )

        self.assertEqual([row.ref for row in rows], ["GEN 1:1", "TOB 1:1"])
        self.assertEqual(rows[0].text, "Alpha")
        self.assertEqual(manifest["bolls_full_name"], "Test Translation")

    def test_main_writes_csv_and_manifest_without_network(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / "sample.json"
            books = base / "books.json"
            languages = base / "languages.json"
            out = base / "out.csv"
            manifest = base / "manifest.json"
            source.write_text(
                json.dumps(
                    [
                        {
                            "translation": "TEST",
                            "book": 1,
                            "chapter": 1,
                            "verse": 1,
                            "text": "Alpha",
                        }
                    ]
                ),
                encoding="utf-8",
            )
            books.write_text(
                json.dumps({"TEST": [{"bookid": 1, "name": "Genesis", "chapters": 1}]}),
                encoding="utf-8",
            )
            languages.write_text(
                json.dumps([{"language": "English", "translations": [{"short_name": "TEST"}]}]),
                encoding="utf-8",
            )

            exit_code = main(
                [
                    "--slug",
                    "TEST",
                    "--label",
                    "TEST",
                    "--source-file",
                    str(source),
                    "--books-file",
                    str(books),
                    "--languages-file",
                    str(languages),
                    "--out",
                    str(out),
                    "--manifest",
                    str(manifest),
                    "--skip-download",
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertIn("GEN 1:1", out.read_text(encoding="utf-8"))
            self.assertTrue(manifest.exists())


if __name__ == "__main__":
    unittest.main()
