import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.import_amplified_epub import BOOKS, main, parse_chapter_html


class AmplifiedEpubImportTests(unittest.TestCase):
    def test_parse_chapter_html_removes_linked_crossrefs_only(self) -> None:
        rows, anomalies = parse_chapter_html(
            """<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml">
  <body>
    <p><a>Genesis 1</a></p>
    <p><sup>1</sup> Alpha [<a>Ref 1:1</a>.] [kept note]</p>
  </body>
</html>
"""
        )

        self.assertEqual(anomalies, [])
        self.assertEqual(rows[0].ref, "GEN 1:1")
        self.assertEqual(rows[0].text, "Alpha [kept note]")

    def test_main_writes_csv_from_synthetic_epub(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            epub = Path(tmp) / "amp.epub"
            out = Path(tmp) / "amp.csv"
            manifest = Path(tmp) / "manifest.json"
            with zipfile.ZipFile(epub, "w") as archive:
                for index, (_code, name) in enumerate(BOOKS):
                    archive.writestr(
                        f"index_split_{index:03d}.html",
                        synthetic_chapter_html(name),
                    )

            exit_code = main(
                [
                    "--epub",
                    str(epub),
                    "--out",
                    str(out),
                    "--manifest",
                    str(manifest),
                ]
            )

            self.assertEqual(exit_code, 0)
            text = out.read_text(encoding="utf-8")
            self.assertIn("GEN 1:1", text)
            self.assertIn("REV 1:1", text)
            self.assertTrue(manifest.exists())


def synthetic_chapter_html(book_name: str) -> str:
    return f"""<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml">
  <body>
    <p><a>{book_name} 1</a></p>
    <p><sup>1</sup> Body text</p>
  </body>
</html>
"""


if __name__ == "__main__":
    unittest.main()
