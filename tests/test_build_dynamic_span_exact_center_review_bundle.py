import unittest

from scripts.build_dynamic_span_exact_center_review_bundle import (
    aggregate_extensions,
    aggregate_matrix,
    build_bundle,
    bundle_markdown_row,
    bundle_sort_key,
    reproduce_command,
)


class BuildDynamicSpanExactCenterReviewBundleTests(unittest.TestCase):
    def test_build_bundle_joins_context_extensions_and_matrix(self) -> None:
        queue_rows = [
            {
                "rank": "1",
                "corpus_class": "bible",
                "corpus": "KJV",
                "term_id": "dyn_jesus_e",
                "normalized_term": "jesus",
                "center_ref": "MAT 1:1",
                "center_source": "KJV",
                "center_word_index": "3",
                "center_word": "Jesus",
                "exact_center_paths": "2",
                "min_abs_skip": "5",
                "max_abs_skip": "9",
                "review_bucket": "bible",
            }
        ]
        context_rows = [
            {
                "corpus": "KJV",
                "normalized_term": "jesus",
                "center_ref": "MAT 1:1",
                "center_word_index": "3",
                "center_word_context": "before [Jesus] after",
                "center_verse_text": "Now Jesus was named in this demo verse.",
            }
        ]
        extension_rows = [
            {
                "corpus": "KJV",
                "normalized_term": "jesus",
                "center_ref": "MAT 1:1",
                "center_word_index": "3",
                "extended_sequence": "jesusand",
                "extension_type": "term_plus_after",
                "match_kind": "phrase_2",
                "match_count": "4",
                "matched_examples": "Jesus and",
                "extension_score": "3004",
            }
        ]
        matrix_rows = [
            {
                "corpus": "KJV",
                "normalized_term": "jesus",
                "center_ref": "MAT 1:1",
                "rows_spanned": "5",
            },
            {
                "corpus": "KJV",
                "normalized_term": "jesus",
                "center_ref": "MAT 1:1",
                "rows_spanned": "7",
            },
        ]

        rows = build_bundle(queue_rows, context_rows, extension_rows, matrix_rows)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["priority"], "bible_exact_center_with_strong_extension")
        self.assertEqual(rows[0]["strong_extension_rows"], 1)
        self.assertEqual(rows[0]["best_extension"], "jesusand")
        self.assertEqual(rows[0]["matrix_paths"], 2)
        self.assertEqual(rows[0]["matrix_min_rows_spanned"], 5)
        self.assertEqual(rows[0]["matrix_max_rows_spanned"], 7)
        self.assertEqual(rows[0]["center_word_context"], "before [Jesus] after")

    def test_aggregate_extensions_picks_highest_score(self) -> None:
        grouped = aggregate_extensions(
            [
                {
                    "corpus": "KJV",
                    "normalized_term": "jesus",
                    "center_ref": "MAT 1:1",
                    "center_word_index": "3",
                    "extended_sequence": "low",
                    "extension_type": "term_plus_after",
                    "match_kind": "phrase_2",
                    "match_count": "9",
                    "matched_examples": "low",
                    "extension_score": "10",
                },
                {
                    "corpus": "KJV",
                    "normalized_term": "jesus",
                    "center_ref": "MAT 1:1",
                    "center_word_index": "3",
                    "extended_sequence": "high",
                    "extension_type": "term_plus_after",
                    "match_kind": "phrase_2",
                    "match_count": "1",
                    "matched_examples": "high",
                    "extension_score": "20",
                },
            ]
        )

        self.assertEqual(grouped[("KJV", "jesus", "MAT 1:1", "3")]["extended_sequence"], "high")

    def test_aggregate_matrix_groups_by_corpus_term_and_center_ref(self) -> None:
        grouped = aggregate_matrix(
            [
                {"corpus": "KJV", "normalized_term": "jesus", "center_ref": "MAT 1:1", "rows_spanned": "2"},
                {"corpus": "KJV", "normalized_term": "jesus", "center_ref": "MAT 1:1", "rows_spanned": "4"},
            ]
        )

        summary = grouped[("KJV", "jesus", "MAT 1:1")]
        self.assertEqual(summary["paths"], 2)
        self.assertEqual(summary["min_rows_spanned"], 2)
        self.assertEqual(summary["max_rows_spanned"], 4)

    def test_bundle_sort_prioritizes_bible_extension_rows(self) -> None:
        bible = {"priority": "bible_exact_center_with_strong_extension", "exact_center_paths": "1", "rank": "5"}
        control = {"priority": "control_exact_center_with_strong_extension", "exact_center_paths": "99", "rank": "1"}

        self.assertLess(bundle_sort_key(bible), bundle_sort_key(control))

    def test_bundle_sort_keeps_control_extension_above_plain_bible_rows(self) -> None:
        control = {"priority": "control_exact_center_with_strong_extension", "exact_center_paths": "1", "rank": "5"}
        bible = {"priority": "bible_exact_center", "exact_center_paths": "99", "rank": "1"}

        self.assertLess(bundle_sort_key(control), bundle_sort_key(bible))

    def test_bundle_markdown_row_displays_original_language_terms(self) -> None:
        row = {
            "rank": "1",
            "priority": "bible_exact_center_with_strong_extension",
            "corpus": "SBLGNT",
            "normalized_term": "δοξα",
            "center_ref": "2TH 3:1",
            "exact_center_paths": "3",
            "strong_extension_rows": "1",
            "best_extension": "δοξανωσ",
            "matrix_paths": "3",
            "center_word_context": "short context",
        }

        line = bundle_markdown_row(row)

        self.assertIn("`δοξα` (doxa; English: glory)", line)
        self.assertIn("`δοξανωσ` (doxanos; English: hidden extension form from doxa)", line)

    def test_reproduce_command_includes_all_inputs(self) -> None:
        args = type(
            "Args",
            (),
            {
                "queue": "queue.csv",
                "context": "context.csv",
                "matrix_dir": "matrix",
                "bible_extension_dir": "bible_ext",
                "control_extension_dir": "control_ext",
                "out": "bundle.csv",
                "markdown_out": "bundle.md",
                "manifest_out": "bundle.manifest.json",
                "markdown_row_limit": 80,
            },
        )()

        command = reproduce_command(args)

        self.assertIn("--queue queue.csv", command)
        self.assertIn("--context context.csv", command)
        self.assertIn("--matrix-dir matrix", command)
        self.assertIn("--bible-extension-dir bible_ext", command)
        self.assertIn("--control-extension-dir control_ext", command)


if __name__ == "__main__":
    unittest.main()
