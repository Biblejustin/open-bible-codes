import tempfile
import unittest
from pathlib import Path

from scripts.analyze_targeted_version_presence import (
    build_control_target_rows,
    build_summary_rows,
    example_row,
    exact_read,
    overall_read,
    parse_hit_counts,
    representative_current_read_lines,
    representative_read_counts,
    selected_term_ids,
    write_markdown,
)


class TargetedVersionPresenceTests(unittest.TestCase):
    def test_summary_row_joins_exact_control_and_extension_data(self) -> None:
        rows = build_summary_rows(
            ("trump_h",),
            {
                "trump_h": {
                    "term_id": "trump_h",
                    "concept": "Trump",
                    "category": "modern_names",
                    "language": "hebrew",
                    "term": "טראמפ",
                    "normalized_term": "טראמפ",
                    "normalized_length": "5",
                }
            },
            {
                "trump_h": {
                    "term_id": "trump_h",
                    "concept": "Trump",
                    "category": "modern_names",
                    "term": "טראמפ",
                    "normalized_term": "טראמפ",
                    "observed_corpora": "MT_WLC,UHB",
                    "hit_counts_by_corpus": "MT_WLC:2; UHB:2",
                    "total_hits": "4",
                    "unique_patterns": "2",
                    "all_observed_patterns": "1",
                    "all_leningrad_patterns": "0",
                    "multi_source_patterns": "1",
                    "source_specific_patterns": "0",
                }
            },
            {
                "trump_h": [
                    {
                        "corpus": "MT_WLC",
                        "paired_band": "not_unusual",
                        "combined_min_p_ge": "0.4",
                        "combined_min_q_value": "1.0",
                    }
                ]
            },
            {
                "trump_h": [
                    {
                        "corpus": "UHB",
                        "paired_band": "not_unusual",
                        "combined_min_p_ge": "0.5",
                        "combined_min_q_value": "1.0",
                    }
                ]
            },
            {
                "טראמפ": [
                    {
                        "corpus": "MT_WLC",
                        "extension_type": "after_match",
                        "skip": "4",
                        "match_kind": "phrase_2",
                        "max_extension_length": "3",
                    }
                ]
            },
            {},
        )

        self.assertEqual(rows[0]["exact_all_source_patterns"], 1)
        self.assertEqual(rows[0]["paired_control_available"], "yes")
        self.assertEqual(rows[0]["representative_control_available"], "yes")
        self.assertEqual(rows[0]["extension_summary_rows"], 1)
        self.assertIn("representative controls", rows[0]["overall_read"])

    def test_short_terms_are_marked_outside_exact_matrix(self) -> None:
        term = {"normalized_term": "גוג"}
        self.assertEqual(
            exact_read(term, {}),
            "below exact-version screen minimum length",
        )

    def test_missing_control_keeps_version_only_read(self) -> None:
        self.assertEqual(
            overall_read(
                "has all-source exact patterns",
                "not run in targeted paired controls",
                "no strict phrase-extension summary row",
            ),
            "version-distribution row only; needs paired controls before interpretation",
        )

    def test_source_specific_read_is_not_called_version_stable(self) -> None:
        self.assertEqual(
            overall_read(
                "source-specific exact patterns only",
                "not unusual under paired controls",
                "no strict phrase-extension summary row",
            ),
            "source-specific exact rows only; needs controls and context before interpretation",
        )

    def test_representative_uncorrected_read_stays_conservative(self) -> None:
        self.assertEqual(
            overall_read(
                "has all-source exact patterns",
                "not run in targeted paired controls",
                "no strict phrase-extension summary row",
                "uncorrected representative-control screen only",
            ),
            "uncorrected representative-control screen only; no adjusted support",
        )

    def test_example_row_formats_span(self) -> None:
        row = example_row(
            {
                "language": "greek",
                "concept": "Iran",
                "term_id": "iran_g",
                "term": "ιραν",
                "normalized_term": "ιραν",
                "presence_scope": "present_all_observed_sources",
                "skip": "7",
                "direction": "forward",
                "start_ref": "Matt 1:1",
                "center_ref": "Matt 1:1",
                "end_ref": "Matt 1:2",
                "present_corpora": "SBLGNT,TR_NT",
                "absent_corpora": "",
                "center_words_by_corpus": "TR_NT:test",
            }
        )
        self.assertEqual(row["span"], "Matt 1:1-Matt 1:2")

    def test_control_targets_use_representative_corpora(self) -> None:
        rows = build_control_target_rows(
            [
                {
                    "language": "hebrew",
                    "concept": "Iran",
                    "term_id": "iran_h",
                    "category": "modern_places",
                    "term": "איראן",
                    "normalized_term": "איראנ",
                    "exact_hit_counts_by_corpus": "MT_WLC:3; UHB:4; MAM:5",
                },
                {
                    "language": "greek",
                    "concept": "USA",
                    "term_id": "usa_abbrev_g",
                    "category": "modern_places",
                    "term": "ΗΠΑ",
                    "normalized_term": "ηπα",
                    "exact_hit_counts_by_corpus": "TR_NT:10; SBLGNT:10",
                },
            ]
        )
        self.assertEqual([row["corpus"] for row in rows], ["MT_WLC", "UHB"])

    def test_parse_hit_counts_handles_semicolon_cells(self) -> None:
        self.assertEqual(
            parse_hit_counts("MT_WLC:3; UHB:4"),
            {"MT_WLC": 3, "UHB": 4},
        )

    def test_all_exact_term_ids_uses_summary_order(self) -> None:
        class Args:
            all_exact_term_ids = True
            term_id = None

        self.assertEqual(
            selected_term_ids(
                Args(),
                {"vance_h": {}, "trump_h": {}, "netanyahu_h": {}},
            ),
            ("vance_h", "trump_h", "netanyahu_h"),
        )

    def test_all_exact_term_ids_can_be_filtered(self) -> None:
        class Args:
            all_exact_term_ids = True
            term_id = ["trump_h"]

        self.assertEqual(
            selected_term_ids(
                Args(),
                {"vance_h": {}, "trump_h": {}, "netanyahu_h": {}},
            ),
            ("trump_h",),
        )

    def test_representative_current_read_summarizes_controls_and_absences(self) -> None:
        rows = [
            {
                "term_id": "trump_h",
                "exact_total_hits": 31,
                "representative_best_read": "not unusual under representative controls",
                "representative_best_band": "not_unusual",
            },
            {
                "term_id": "germany_h",
                "exact_total_hits": 38,
                "representative_best_read": "uncorrected representative-control screen only",
                "representative_best_band": "paired_uncorrected_p_le_0.05",
            },
            {
                "term_id": "united_states_h",
                "exact_total_hits": 0,
                "representative_best_read": "not run in representative paired controls",
                "representative_best_band": "",
            },
        ]

        counts = representative_read_counts(rows)
        lines = representative_current_read_lines(rows, counts)

        self.assertEqual(counts["not_unusual"], 1)
        self.assertEqual(counts["uncorrected"], 1)
        self.assertEqual(counts["not_run"], 1)
        self.assertIn("adjusted representative-control support", lines[0])
        self.assertIn("`united_states_h`", lines[-1])

    def test_write_markdown_accepts_custom_description(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.md"
            write_markdown(
                path,
                [],
                [],
                title="Custom Title",
                description="Custom description.",
            )

            text = path.read_text(encoding="utf-8")
            self.assertIn("# Custom Title", text)
            self.assertIn("Custom description.", text)

    def test_write_markdown_displays_original_language_terms(self) -> None:
        rows = [
            {
                "language": "hebrew",
                "concept": "Trump",
                "term_id": "trump_h",
                "category": "modern_names",
                "term": "טראמפ",
                "normalized_term": "טראמפ",
                "exact_hit_counts_by_corpus": "",
                "exact_total_hits": 4,
                "exact_all_source_patterns": 1,
                "exact_source_specific_patterns": 0,
                "paired_control_available": "no",
                "representative_control_available": "no",
                "paired_best_band": "",
                "paired_best_read": "not run",
                "representative_best_band": "",
                "representative_best_read": "not run",
                "extension_summary_rows": 0,
                "extension_strong_plus_term_rows": 0,
                "overall_read": "screening row only",
            }
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.md"
            write_markdown(path, rows, [])

            text = path.read_text(encoding="utf-8")

        self.assertIn("`טראמפ` (trmp; English: Trump)", text)


if __name__ == "__main__":
    unittest.main()
