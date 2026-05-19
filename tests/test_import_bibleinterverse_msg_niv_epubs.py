import csv
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.import_bibleinterverse_msg_niv_epubs import import_bundle, main


class BibleInterverseMsgNivImportTests(unittest.TestCase):
    def test_import_bundle_splits_interversed_msg_and_niv_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "bundle.zip"
            write_bundle(bundle)

            msg_rows, niv_rows, manifest = import_bundle(bundle)

            self.assertEqual([row.ref for row in msg_rows], ["JHN 1:1", "JHN 1:2"])
            self.assertEqual([row.text for row in msg_rows], ["msg one", "msg two"])
            self.assertEqual([row.text for row in niv_rows], ["niv one", "niv two"])
            self.assertEqual(manifest["msg_rows"], 2)
            self.assertEqual(manifest["niv_rows"], 2)
            self.assertEqual(manifest["anomaly_count"], 0)

    def test_import_bundle_keeps_unpaired_msg_rows_without_offsetting_niv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "bundle.zip"
            write_bundle(
                bundle,
                """
<h1>John 1</h1>
<p>MSG</p>
<p>NIV</p>
<p>1&nbsp; msg one</p>
<p>1&nbsp; niv one</p>
<p>2&nbsp; (OMITTED TEXT)</p>
<p>3&nbsp; msg three</p>
<p>3&nbsp; niv three</p>
""",
            )

            msg_rows, niv_rows, manifest = import_bundle(bundle)

            self.assertEqual([row.ref for row in msg_rows], ["JHN 1:1", "JHN 1:2", "JHN 1:3"])
            self.assertEqual([row.ref for row in niv_rows], ["JHN 1:1", "JHN 1:3"])
            self.assertEqual(manifest["unpaired_row_count"], 1)
            self.assertEqual(manifest["anomaly_count"], 0)

    def test_main_writes_private_csvs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "bundle.zip"
            out_dir = Path(tmp) / "private"
            write_bundle(bundle)

            exit_code = main(["--zip", str(bundle), "--out-dir", str(out_dir)])

            self.assertEqual(exit_code, 0)
            self.assertEqual(read_texts(out_dir / "msg.csv"), ["msg one", "msg two"])
            self.assertEqual(read_texts(out_dir / "niv.csv"), ["niv one", "niv two"])
            self.assertTrue((out_dir / "bibleinterverse_msg_niv_manifest.json").exists())


def write_bundle(path: Path, body: str | None = None) -> None:
    if body is None:
        body = """
<h1>John 1</h1>
<p>MSG</p>
<p>NIV</p>
<p>1&nbsp; msg one</p>
<p>1&nbsp; niv one</p>
<p>2&nbsp; msg two</p>
<p>2&nbsp; niv two</p>
"""
    html = f"""<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml">
<body>
{body}
</body>
</html>
"""
    epub_bytes = Path(path.parent / "book.epub")
    with zipfile.ZipFile(epub_bytes, "w") as epub:
        epub.writestr("index.html", html)
    with zipfile.ZipFile(path, "w") as outer:
        outer.write(epub_bytes, "BibInVs MN 43 John - God.epub")


def read_texts(path: Path) -> list[str]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [row["text"] for row in csv.DictReader(handle)]


if __name__ == "__main__":
    unittest.main()
