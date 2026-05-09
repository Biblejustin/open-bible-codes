import unittest

from scripts.analyze_extension_cross_text_review import cross_text_status, refs_cell


class ExtensionCrossTextReviewTests(unittest.TestCase):
    def test_cross_text_status_marks_match_vs_source_only(self) -> None:
        self.assertEqual(cross_text_status(1), "cross_text_match")
        self.assertEqual(cross_text_status(0), "source_only")

    def test_refs_cell_dedupes_and_joins_refs(self) -> None:
        rows = [
            {"start_ref": "2Thess 3:1", "end_ref": "2Thess 3:1"},
            {"start_ref": "2Thess 3:1", "end_ref": "2Thess 3:1"},
            {"start_ref": "2Thess 3:1", "end_ref": "2Thess 3:2"},
        ]

        self.assertEqual(
            refs_cell(rows, "start_ref", "end_ref"),
            "2Thess 3:1-2Thess 3:1; 2Thess 3:1-2Thess 3:2",
        )


if __name__ == "__main__":
    unittest.main()
