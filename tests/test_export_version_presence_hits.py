import unittest

from scripts.export_version_presence_hits import parse_offsets_by_corpus, pattern_selected


class ExportVersionPresenceHitsTests(unittest.TestCase):
    def test_parse_offsets_by_corpus_handles_forward_and_backward_spans(self) -> None:
        offsets = parse_offsets_by_corpus("MT_WLC:10-22; UHB:105-81")
        self.assertEqual(offsets["MT_WLC"], (10, 22))
        self.assertEqual(offsets["UHB"], (105, 81))

    def test_pattern_selected_applies_optional_filters(self) -> None:
        pattern = {
            "presence_scope": "present_all_observed_sources",
            "term_id": "trump_h",
            "concept": "Trump",
            "category": "modern_names",
        }
        self.assertTrue(pattern_selected(pattern, {"present_all_observed_sources"}, set(), set(), set()))
        self.assertTrue(
            pattern_selected(
                pattern,
                {"present_all_observed_sources"},
                {"trump_h"},
                {"Trump"},
                {"modern_names"},
            )
        )
        self.assertFalse(
            pattern_selected(pattern, {"source_specific"}, {"trump_h"}, {"Trump"}, {"modern_names"})
        )
        self.assertFalse(
            pattern_selected(
                pattern,
                {"present_all_observed_sources"},
                {"netanyahu_h"},
                set(),
                set(),
            )
        )


if __name__ == "__main__":
    unittest.main()
