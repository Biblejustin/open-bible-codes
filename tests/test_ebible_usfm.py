import tempfile
import unittest
import zipfile
from pathlib import Path

from els.ebible_usfm import parse_usfm, parse_usfm_zip
from scripts.download_ebible_usfm import SOURCES


class EbibleUsfmTests(unittest.TestCase):
    def test_parse_usfm_extracts_verses_and_strips_markers(self) -> None:
        text = "\n".join(
            [
                "\\id GEN",
                "\\c 1",
                "\\p",
                "\\v 1 ΕΝ \\w ἀρχῇ|strong=\"G0746\" x-morph=\"N-DSF\"\\w* ἐποίησεν.",
                "\\v 2 γῆ \\f + \\ft note\\f* ἦν.",
            ]
        )

        verses = parse_usfm(text)

        self.assertEqual(len(verses), 2)
        self.assertEqual(verses[0].ref, "GEN 1:1")
        self.assertEqual(verses[0].text, "ΕΝ ἀρχῇ ἐποίησεν.")
        self.assertEqual(verses[1].text, "γῆ ἦν.")

    def test_parse_usfm_strips_standalone_hebrew_paragraph_markers(self) -> None:
        verses = parse_usfm("\\id GEN\n\\c 1\n\\v 5 וַיְהִי עֶרֶב׃ פ\n\\v 6 רָקִיעַ׃ ס")

        self.assertEqual(verses[0].text, "וַיְהִי עֶרֶב׃")
        self.assertEqual(verses[1].text, "רָקִיעַ׃")

    def test_parse_usfm_strips_attached_hebrew_paragraph_markers(self) -> None:
        verses = parse_usfm("\\id GEN\n\\c 1\n\\v 5 וַיְהִי עֶרֶב׃פ\n\\v 6 רָקִיעַ׃ס")

        self.assertEqual(verses[0].text, "וַיְהִי עֶרֶב׃")
        self.assertEqual(verses[1].text, "רָקִיעַ׃")

    def test_parse_usfm_zip_uses_archive_book_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("03-EXOgrclxx.usfm", "\\id EXO\n\\c 1\n\\v 1 Β")
                archive.writestr("02-GENgrclxx.usfm", "\\id GEN\n\\c 1\n\\v 1 Α")

            verses = parse_usfm_zip(path)

        self.assertEqual([verse.ref for verse in verses], ["GEN 1:1", "EXO 1:1"])

    def test_grcmt_source_is_registered(self) -> None:
        source = SOURCES["grcmt"]

        self.assertEqual(source.source_id, "grcmt")
        self.assertEqual(source.source_url, "https://ebible.org/Scriptures/grcmt_usfm.zip")
        self.assertEqual(source.out_csv, Path("data/processed/ebible/grcmt.csv"))

    def test_grctcgnt_source_is_registered(self) -> None:
        source = SOURCES["grctcgnt"]

        self.assertEqual(source.source_id, "grctcgnt")
        self.assertEqual(
            source.source_url,
            "https://ebible.org/Scriptures/grctcgnt_usfm.zip",
        )
        self.assertEqual(source.out_csv, Path("data/processed/ebible/grctcgnt.csv"))

    def test_hebwlc_source_is_registered(self) -> None:
        source = SOURCES["hebwlc"]

        self.assertEqual(source.source_id, "hebwlc")
        self.assertEqual(source.source_url, "https://ebible.org/Scriptures/hebwlc_usfm.zip")
        self.assertEqual(source.out_csv, Path("data/processed/ebible/hebwlc.csv"))

    def test_eng_kjv_source_is_registered(self) -> None:
        source = SOURCES["eng-kjv2006"]

        self.assertEqual(source.source_id, "eng-kjv2006")
        self.assertEqual(
            source.source_url,
            "https://ebible.org/Scriptures/eng-kjv2006_usfm.zip",
        )
        self.assertEqual(source.out_csv, Path("data/processed/ebible/eng-kjv2006.csv"))

    def test_eng_kjv_apocrypha_source_is_registered(self) -> None:
        source = SOURCES["eng-kjv"]

        self.assertEqual(source.source_id, "eng-kjv")
        self.assertEqual(
            source.source_url,
            "https://ebible.org/Scriptures/eng-kjv_usfm.zip",
        )
        self.assertEqual(source.out_csv, Path("data/processed/ebible/eng-kjv.csv"))


if __name__ == "__main__":
    unittest.main()
