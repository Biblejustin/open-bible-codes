import csv
import unittest
from pathlib import Path


DOOR43_CONTROLS = Path("configs/door43_english_controls.csv")


class Door43EnglishControlTests(unittest.TestCase):
    def test_door43_controls_have_source_and_license_metadata(self) -> None:
        rows = {row["label"]: row for row in read_rows(DOOR43_CONTROLS)}

        self.assertEqual(sorted(rows), ["ULT", "UST"])
        for label, row in rows.items():
            with self.subTest(label=label):
                self.assertTrue(row["source_id"].startswith("en_"))
                self.assertTrue(row["source_url"].startswith("https://git.door43.org/"))
                self.assertTrue(row["source_url"].endswith("/archive/master.zip"))
                self.assertTrue(row["details_url"].startswith("https://git.door43.org/"))
                self.assertIn("CC BY-SA 4.0", row["license_label"])
                self.assertEqual(row["basis_status"], "broad_tradition")
                self.assertTrue(row["local_csv"].startswith("data/processed/door43/"))


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    unittest.main()
