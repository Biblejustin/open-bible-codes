import csv
import unittest
from pathlib import Path

from scripts.download_supplemental_english_controls import (
    parse_usfm_archive,
    parse_akjv_text,
    parse_zefania_xml_zip,
    scrub_structural_lines,
)


SUPPLEMENTAL_CONTROLS = Path("configs/supplemental_english_controls.csv")


class SupplementalEnglishControlTests(unittest.TestCase):
    def test_supplemental_controls_have_source_and_license_metadata(self) -> None:
        rows = {row["label"]: row for row in read_rows(SUPPLEMENTAL_CONTROLS)}

        self.assertEqual(
            sorted(rows),
            [
                "ACV",
                "AKJV",
                "ANDERSON",
                "AV1611",
                "AV1811",
                "CPDV",
                "DEB",
                "DRC1750",
                "KENT",
                "MCFADYEN",
                "MOFFATT",
                "NHEB",
                "PET",
                "ROTHERHAM",
                "TCNT",
            ],
        )
        self.assertEqual(rows["AKJV"]["source_format"], "akjv_text_zip")
        self.assertEqual(rows["AKJV"]["source_url"], "https://cdn.akjv.us/akj.zip")
        self.assertEqual(rows["AKJV"]["details_url"], "https://akjv.us/")
        self.assertIn("Public domain", rows["AKJV"]["license_label"])
        self.assertIn("KJV", rows["AKJV"]["ot_basis"])
        self.assertIn("Textus Receptus", rows["AKJV"]["nt_basis"])

        self.assertEqual(rows["CPDV"]["source_format"], "crosswire_gitlab_usfm_zip")
        self.assertTrue(rows["CPDV"]["source_url"].startswith("https://gitlab.com/crosswire-bible-society/cpdv/"))
        self.assertEqual(
            rows["CPDV"]["details_url"],
            "https://www.crosswire.org/sword/modules/ModInfo.jsp?modName=CPDV",
        )
        self.assertIn("Public domain", rows["CPDV"]["license_label"])
        self.assertIn("Latin Vulgate", rows["CPDV"]["ot_basis"])
        self.assertIn("Latin Vulgate", rows["CPDV"]["nt_basis"])

        self.assertEqual(rows["ANDERSON"]["source_format"], "biblecorps_usfm_zip")
        self.assertEqual(rows["ANDERSON"]["coverage"], "nt")
        self.assertIn("Public domain", rows["ANDERSON"]["license_label"])
        self.assertIn("Greek NT", rows["ANDERSON"]["nt_basis"])

        self.assertEqual(rows["AV1611"]["source_format"], "biblecorps_usfm_zip")
        self.assertEqual(rows["AV1611"]["coverage"], "with_apocrypha")
        self.assertIn("Public domain", rows["AV1611"]["license_label"])
        self.assertEqual(rows["AV1611"]["source_path_prefix"], "PSFM/")

        self.assertEqual(rows["AV1811"]["source_format"], "biblecorps_usfm_zip")
        self.assertEqual(rows["AV1811"]["coverage"], "full")
        self.assertIn("Public domain", rows["AV1811"]["license_label"])
        self.assertEqual(rows["AV1811"]["source_path_prefix"], "")
        self.assertIn("KJV", rows["AV1811"]["source_family"])

        self.assertEqual(rows["DEB"]["source_format"], "biblecorps_usfm_zip")
        self.assertEqual(rows["DEB"]["coverage"], "full_draft")
        self.assertIn("CC BY-SA 4.0", rows["DEB"]["license_label"])
        self.assertIn("checking/not ready", rows["DEB"]["notes"])

        self.assertEqual(rows["DRC1750"]["source_format"], "biblecorps_usfm_zip")
        self.assertEqual(rows["DRC1750"]["coverage"], "with_apocrypha")
        self.assertIn("Public domain", rows["DRC1750"]["license_label"])
        self.assertIn("Latin Vulgate", rows["DRC1750"]["ot_basis"])

        self.assertEqual(rows["PET"]["source_format"], "biblecorps_usfm_zip")
        self.assertEqual(rows["PET"]["coverage"], "nt")
        self.assertIn("CC BY-SA 4.0", rows["PET"]["license_label"])
        self.assertEqual(rows["PET"]["source_path_prefix"], "")

        for label in ["ACV", "NHEB", "ROTHERHAM"]:
            self.assertEqual(rows[label]["source_format"], "zefania_xml_zip")
            self.assertIn("sourceforge.net/projects/zefania-sharp", rows[label]["source_url"])
            self.assertTrue(rows[label]["details_url"].startswith("https://crosswire.org/"))
            self.assertIn("Public domain", rows[label]["license_label"])
            self.assertEqual(rows[label]["coverage"], "full")

        for label in ["KENT", "MCFADYEN", "MOFFATT", "TCNT"]:
            self.assertEqual(rows[label]["source_format"], "openenglishbible_usfm_zip")
            self.assertEqual(
                rows[label]["source_url"],
                "https://github.com/openenglishbible/usfm-bibles/archive/refs/heads/master.zip",
            )
            self.assertIn("Freely distributable", rows[label]["license_label"])
            self.assertIn("OEB", rows[label]["source_family"])
        self.assertEqual(rows["TCNT"]["coverage"], "nt")
        self.assertIn("Westcott-Hort", rows["TCNT"]["nt_basis"])
        self.assertEqual(rows["MOFFATT"]["source_path_prefix"], "Moffat/")

    def test_parse_akjv_text_maps_books_and_verses(self) -> None:
        raw = """
        [Gen] The First Book of Moses
        1:1 In the beginning God created the heaven and the earth.
        1:2 And the earth was without form.
        [Jas] The General Epistle of James
        1:1 James, a servant of God.
        """

        verses = parse_akjv_text(raw)

        self.assertEqual([verse.ref for verse in verses], ["GEN 1:1", "GEN 1:2", "JAS 1:1"])
        self.assertEqual(verses[2].text, "James, a servant of God.")

    def test_scrub_structural_lines_preserves_verse_lines(self) -> None:
        raw = "\\id GEN demo\n\\c 1\n\\v 1 Verse text.\n\\mte The Book of Genesis\n\\q1 continuation"

        self.assertEqual(
            scrub_structural_lines(raw),
            "\\id GEN demo\n\\c 1\n\\v 1 Verse text.\n\\q1 continuation",
        )

    def test_parse_usfm_archive_allows_empty_prefix_for_root_files(self) -> None:
        import tempfile
        import zipfile

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "root-usfm.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr(
                    "demo-master/01-GEN.sfm",
                    "\\id GEN\n\\c 1\n\\v 1 Beginning.",
                )

            verses = parse_usfm_archive(path, "")

        self.assertEqual([verse.ref for verse in verses], ["GEN 1:1"])
        self.assertEqual(verses[0].text, "Beginning.")

    def test_parse_usfm_archive_uses_filename_book_fallback_and_ufsm_suffix(self) -> None:
        import tempfile
        import zipfile

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "oeb-style.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr(
                    "demo-master/Moffat/19-Psalms.usfm",
                    "\\c 75\n\\v 1 We offer thanks.",
                )
                archive.writestr(
                    "demo-master/Moffat/32-Jonah.ufsm",
                    "\\id JON\n\\c 1\n\\v 1 This message came.",
                )

            verses = parse_usfm_archive(path, "Moffat/")

        self.assertEqual([verse.ref for verse in verses], ["PSA 75:1", "JON 1:1"])

    def test_parse_zefania_xml_zip_maps_books_and_skips_notes(self) -> None:
        import tempfile
        import zipfile

        raw = """<?xml version="1.0" encoding="utf-8"?>
        <XMLBIBLE>
          <BIBLEBOOK bnumber="1">
            <CHAPTER cnumber="1">
              <VERS vnumber="1">Beginning <NOTE>not part</NOTE>text.</VERS>
            </CHAPTER>
          </BIBLEBOOK>
          <BIBLEBOOK bnumber="40">
            <CHAPTER cnumber="2">
              <VERS vnumber="3">Magi arrived.</VERS>
            </CHAPTER>
          </BIBLEBOOK>
          <BIBLEBOOK bnumber="22" bsname="1Ki">
            <CHAPTER cnumber="1">
              <VERS vnumber="1">David was old.</VERS>
            </CHAPTER>
          </BIBLEBOOK>
        </XMLBIBLE>
        """
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "zefania.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("demo.xml", raw)

            verses = parse_zefania_xml_zip(path)

        self.assertEqual([verse.ref for verse in verses], ["GEN 1:1", "MAT 2:3", "1KI 1:1"])
        self.assertEqual(verses[0].text, "Beginning text.")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    unittest.main()
