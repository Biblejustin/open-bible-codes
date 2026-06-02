import csv
import unittest
from pathlib import Path

from scripts.download_otb_english_controls import (
    canonical_book_name,
    clean_verse_text,
    parse_otb_chapter_json,
    source_path_sort_key,
)


OTB_CONTROLS = Path("configs/otb_english_controls.csv")


class OtbEnglishControlTests(unittest.TestCase):
    def test_otb_controls_have_source_and_license_metadata(self) -> None:
        rows = {row["label"]: row for row in read_rows(OTB_CONTROLS)}

        self.assertEqual(sorted(rows), ["OTB"])
        row = rows["OTB"]
        self.assertEqual(row["source_id"], "otb-en-gb")
        self.assertTrue(row["source_url"].startswith("https://github.com/OpenTranslationBible/"))
        self.assertTrue(row["details_url"].startswith("https://github.com/OpenTranslationBible/"))
        self.assertIn("CC BY-SA 4.0", row["license_label"])
        self.assertEqual(row["basis_status"], "broad_tradition")
        self.assertIn("does not state", row["ot_basis"])
        self.assertIn("does not state", row["nt_basis"])
        self.assertTrue(row["local_csv"].startswith("data/processed/otb/"))
        self.assertEqual(row["source_path_prefix"], "lang/en-GB/")

    def test_book_name_mapping_and_sorting(self) -> None:
        self.assertEqual(canonical_book_name("Genesis"), "GEN")
        self.assertEqual(canonical_book_name("Psalm"), "PSA")
        self.assertEqual(canonical_book_name("1 Corinthians"), "1CO")
        self.assertEqual(canonical_book_name("Revelation"), "REV")

        paths = [
            "lang/en-GB/46.1 Corinthians/json/1-corinthians-01.json",
            "lang/en-GB/01.Genesis/json/genesis-01.json",
            "lang/en-GB/40.Matthew/json/matthew-01.json",
        ]
        self.assertEqual(
            sorted(paths, key=source_path_sort_key),
            [
                "lang/en-GB/01.Genesis/json/genesis-01.json",
                "lang/en-GB/40.Matthew/json/matthew-01.json",
                "lang/en-GB/46.1 Corinthians/json/1-corinthians-01.json",
            ],
        )

    def test_parse_otb_chapter_json_skips_separators_and_strips_quotes(self) -> None:
        raw = """
        {
          "book": "Genesis",
          "chapter": 1,
          "verses": [
            {"verse": 1, "text": ["In beginning."]},
            {"text": ["---"]},
            {"verse": 2, "text": ["> line one", "> line two"]}
          ]
        }
        """

        verses = parse_otb_chapter_json(raw, path="lang/en-GB/01.Genesis/json/genesis-01.json")

        self.assertEqual([verse.ref for verse in verses], ["GEN 1:1", "GEN 1:2"])
        self.assertEqual(verses[1].text, "line one line two")

    def test_clean_verse_text_skips_markdown_separator(self) -> None:
        self.assertEqual(clean_verse_text(["> Alpha", "---", "Beta"]), "Alpha Beta")

    def test_parse_otb_chapter_json_rejects_non_object_root(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "OTB chapter JSON root must be an object"
        ):
            parse_otb_chapter_json("[]", path="chapter.json")

    def test_parse_otb_chapter_json_rejects_non_list_verses(self) -> None:
        raw = '{"book": "Genesis", "chapter": 1, "verses": {"verse": 1}}'

        with self.assertRaisesRegex(ValueError, "OTB chapter verses must be a list"):
            parse_otb_chapter_json(raw, path="chapter.json")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    unittest.main()
