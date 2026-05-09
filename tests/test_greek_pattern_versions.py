import unittest

from scripts.analyze_greek_pattern_versions import (
    ControlEntry,
    PresenceEntry,
    summarize_patterns,
)


class GreekPatternVersionTests(unittest.TestCase):
    def test_summary_promotes_four_source_controlled_rows(self) -> None:
        rows = summarize_patterns(
            [
                PresenceEntry(
                    "four_source",
                    presence_row(
                        "δοξα|21|forward|term_plus_after|δοξανωσ|δοξανωσ",
                        "δοξα",
                        "TR_NT,BYZ_NT,TCG_NT,SBLGNT",
                        "",
                        "all_sources",
                    ),
                )
            ],
            [
                ControlEntry(
                    "controls.csv",
                    control_row(
                        "δοξα|21|forward|term_plus_after|δοξανωσ|δοξανωσ",
                        "TR_NT",
                        "0.001",
                    ),
                )
            ],
        )

        self.assertEqual(rows[0]["status"], "four_source_controlled_review_candidate")
        self.assertEqual(rows[0]["best_q"], "0.001")

    def test_summary_prefers_controls_matching_current_presence(self) -> None:
        key = "δοξα|21|forward|term_plus_after|δοξανωσ|δοξανωσ"
        rows = summarize_patterns(
            [
                PresenceEntry(
                    "three_source",
                    presence_row(
                        key,
                        "δοξα",
                        "TR_NT,BYZ_NT,SBLGNT",
                        "",
                        "all_sources",
                    ),
                ),
                PresenceEntry(
                    "four_source",
                    presence_row(
                        key,
                        "δοξα",
                        "TR_NT,BYZ_NT,TCG_NT,SBLGNT",
                        "",
                        "all_sources",
                    ),
                ),
            ],
            [
                ControlEntry(
                    "three.csv",
                    control_row(key, "TR_NT", "0.000999", "TR_NT,BYZ_NT,SBLGNT"),
                ),
                ControlEntry(
                    "four.csv",
                    control_row(key, "TR_NT", "0.001332", "TR_NT,BYZ_NT,TCG_NT,SBLGNT"),
                ),
            ],
        )

        self.assertEqual(rows[0]["best_q"], "0.001332")
        self.assertEqual(rows[0]["controlled_corpora"], "TR_NT")

    def test_summary_keeps_source_specific_rows_visible(self) -> None:
        rows = summarize_patterns(
            [
                PresenceEntry(
                    "four_source",
                    presence_row(
                        "αιμα|14|forward|before_plus_term_plus_after|ναιμανο|ναιμανο",
                        "αιμα",
                        "SBLGNT",
                        "TR_NT,BYZ_NT,TCG_NT",
                        "source_only",
                    ),
                )
            ],
            [
                ControlEntry(
                    "controls.csv",
                    control_row(
                        "αιμα|14|forward|before_plus_term_plus_after|ναιμανο|ναιμανο",
                        "SBLGNT",
                        "0.000999",
                    ),
                )
            ],
        )

        self.assertEqual(rows[0]["status"], "source_specific_review_candidate")
        self.assertIn("version-specific", rows[0]["read"])
        self.assertEqual(rows[0]["current_absent_corpora"], "TR_NT,BYZ_NT,TCG_NT")


def presence_row(
    key: str,
    term: str,
    present: str,
    absent: str,
    scope: str,
) -> dict[str, str]:
    return {
        "overlap_key": key,
        "normalized_term": term,
        "skip": key.split("|")[1],
        "direction": key.split("|")[2],
        "extension_type": key.split("|")[3],
        "extended_sequence": key.split("|")[4],
        "present_corpora": present,
        "absent_corpora": absent,
        "scope": scope,
    }


def control_row(
    key: str,
    corpus: str,
    q: str,
    overlap_corpora: str = "",
) -> dict[str, str]:
    return {
        "overlap_key": key,
        "corpus": corpus,
        "combined_min_q": q,
        "overlap_corpora": overlap_corpora,
    }


if __name__ == "__main__":
    unittest.main()
