import csv
import unittest
from pathlib import Path

from scripts.download_supplemental_english_controls import (
    parse_usfm_archive,
    parse_akjv_text,
    scrub_structural_lines,
)


SUPPLEMENTAL_CONTROLS = Path("configs/supplemental_english_controls.csv")


class SupplementalEnglishControlTests(unittest.TestCase):
    def test_supplemental_controls_have_source_and_license_metadata(self) -> None:
        rows = {row["label"]: row for row in read_rows(SUPPLEMENTAL_CONTROLS)}

        self.assertEqual(sorted(rows), ["AKJV", "ANDERSON", "CPDV", "DEB", "PET"])
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

        self.assertEqual(rows["DEB"]["source_format"], "biblecorps_usfm_zip")
        self.assertEqual(rows["DEB"]["coverage"], "full_draft")
        self.assertIn("CC BY-SA 4.0", rows["DEB"]["license_label"])
        self.assertIn("checking/not ready", rows["DEB"]["notes"])

        self.assertEqual(rows["PET"]["source_format"], "biblecorps_usfm_zip")
        self.assertEqual(rows["PET"]["coverage"], "nt")
        self.assertIn("CC BY-SA 4.0", rows["PET"]["license_label"])
        self.assertEqual(rows["PET"]["source_path_prefix"], "")

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


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    unittest.main()
