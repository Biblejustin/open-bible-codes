import csv
import unittest
from pathlib import Path

from els.ebible_usfm import UsfmVerse
from scripts.download_odr_english_controls import (
    deduplicate_verses,
    sort_verses_canonically,
)


ODR_CONTROLS = Path("configs/odr_english_controls.csv")


class OdrEnglishControlTests(unittest.TestCase):
    def test_odr_control_has_source_and_license_metadata(self) -> None:
        rows = {row["label"]: row for row in read_rows(ODR_CONTROLS)}

        self.assertEqual(sorted(rows), ["ODR"])
        row = rows["ODR"]
        self.assertEqual(row["coverage"], "with_apocrypha")
        self.assertIn("Latin Vulgate", row["ot_basis"])
        self.assertIn("Latin Vulgate", row["nt_basis"])
        self.assertEqual(row["basis_status"], "broad_tradition")
        self.assertEqual(row["source_id"], "original-douay-rheims")
        self.assertTrue(row["source_url"].startswith("https://github.com/janvier-s/original-douay-rheims/"))
        self.assertEqual(row["details_url"], "https://github.com/janvier-s/original-douay-rheims")
        self.assertIn("CC0 1.0", row["license_label"])
        self.assertEqual(row["source_path_prefix"], "usfm/")

    def test_odr_deduplicates_identical_refs(self) -> None:
        verses = [
            UsfmVerse("MAN", "1", "1", "Prayer."),
            UsfmVerse("GEN", "1", "1", "Beginning."),
            UsfmVerse("MAN", "1", "1", "Prayer."),
        ]

        deduped, duplicate_refs = deduplicate_verses(verses)

        self.assertEqual(duplicate_refs, 1)
        self.assertEqual([verse.ref for verse in sort_verses_canonically(deduped)], ["GEN 1:1", "MAN 1:1"])

    def test_odr_merges_conflicting_duplicate_refs(self) -> None:
        verses = [
            UsfmVerse("1ES", "2", "1", "Cyrus heading."),
            UsfmVerse("1ES", "2", "1", "Cyrus verse."),
        ]

        deduped, duplicate_refs = deduplicate_verses(verses)

        self.assertEqual(duplicate_refs, 1)
        self.assertEqual(deduped[0].text, "Cyrus heading. Cyrus verse.")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    unittest.main()
