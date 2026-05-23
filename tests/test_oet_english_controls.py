import csv
import unittest
from pathlib import Path

from scripts.download_oet_english_controls import (
    canonical_book_from_path,
    parse_oet_usfm,
    source_path_sort_key,
)


OET_CONTROLS = Path("configs/oet_english_controls.csv")


class OetEnglishControlTests(unittest.TestCase):
    def test_oet_controls_have_source_and_license_metadata(self) -> None:
        rows = {row["label"]: row for row in read_rows(OET_CONTROLS)}

        self.assertEqual(sorted(rows), ["OET-LV", "OET-RV"])
        for label, row in rows.items():
            with self.subTest(label=label):
                self.assertTrue(row["source_id"].startswith("oet-"))
                self.assertTrue(row["source_url"].startswith("https://github.com/Freely-Given-org/"))
                self.assertTrue(row["details_url"].startswith("https://OpenEnglishTranslation.Bible/"))
                self.assertIn("CC BY-SA 4.0", row["license_label"])
                self.assertEqual(row["basis_status"], "broad_tradition")
                self.assertTrue(row["local_csv"].startswith("data/processed/oet/"))
                self.assertTrue(row["source_path_prefix"].startswith("exportedFiles/cleanedUSFM/"))

    def test_book_aliases_match_existing_usfm_ids(self) -> None:
        self.assertEqual(canonical_book_from_path("OET-RV_Gen.USFM"), "GEN")
        self.assertEqual(canonical_book_from_path("OET-RV_1Co.USFM"), "1CO")
        self.assertEqual(canonical_book_from_path("OET-RV_Jas.USFM"), "JAS")
        self.assertEqual(canonical_book_from_path("OET-RV_Ezk.USFM"), "EZK")
        self.assertEqual(canonical_book_from_path("OET-RV_1Ma.USFM"), "1MA")

    def test_source_sort_uses_canonical_order(self) -> None:
        paths = [
            "exportedFiles/cleanedUSFM/ReadersVersion/OET-RV_1Co.USFM",
            "exportedFiles/cleanedUSFM/ReadersVersion/OET-RV_Gen.USFM",
            "exportedFiles/cleanedUSFM/ReadersVersion/OET-RV_Mat.USFM",
            "exportedFiles/cleanedUSFM/ReadersVersion/OET-RV_Tob.USFM",
        ]

        self.assertEqual(
            sorted(paths, key=source_path_sort_key),
            [
                "exportedFiles/cleanedUSFM/ReadersVersion/OET-RV_Gen.USFM",
                "exportedFiles/cleanedUSFM/ReadersVersion/OET-RV_Tob.USFM",
                "exportedFiles/cleanedUSFM/ReadersVersion/OET-RV_Mat.USFM",
                "exportedFiles/cleanedUSFM/ReadersVersion/OET-RV_1Co.USFM",
            ],
        )

    def test_parse_oet_usfm_normalizes_book_and_strips_notes(self) -> None:
        usfm = "\n".join(
            [
                r"\id Gen",
                r"\c 1",
                r"\v 1 In \add the\add* beginning\f + \fr 1:1 \ft note\f*.",
                r"\v 2 And \nd YHWH\nd* spoke.",
            ]
        )

        verses = parse_oet_usfm(usfm, path="OET-LV_Gen.USFM")

        self.assertEqual([verse.ref for verse in verses], ["GEN 1:1", "GEN 1:2"])
        self.assertEqual(verses[0].text, "In the beginning .")
        self.assertEqual(verses[1].text, "And YHWH spoke.")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    unittest.main()
