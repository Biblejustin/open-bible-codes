import random
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from els.corpus import Corpus, VerseSpan, WordSpan
from els.extensions import build_extension_lexicon, extensions_for_hit
from els.search import build_hit
from scripts.analyze_extension_paired_controls import (
    ControlScores,
    ExtensionTarget,
    all_controls_band,
    extension_band,
    extension_score,
    normalize_target_row,
    prepare_targets,
    require_overlap_corpora_targets,
    sample_random_controls,
    sample_term_controls,
    score_control_sets,
    score_controls,
    score_hit_extensions,
    stable_seed,
    summary_row,
    write_markdown,
)


class ExtensionPairedControlsTests(unittest.TestCase):
    def test_extension_score_matches_expected_priority_shape(self) -> None:
        self.assertEqual(
            extension_score("before_plus_term_plus_after", 3, "phrase_3", 4),
            3314,
        )
        self.assertEqual(
            extension_score("term_plus_after", 4, "word", 12),
            4209,
        )
        self.assertEqual(
            extension_score(
                "before_plus_term",
                2,
                "phrase_2+word",
                6,
                high_priority_scale=True,
            ),
            302016,
        )

    def test_term_controls_preserve_letter_multiset(self) -> None:
        samples = sample_term_controls("abcd", samples=20, rng=random.Random(1))

        self.assertEqual(len(samples), 20)
        self.assertTrue(all(sorted(sample) == ["a", "b", "c", "d"] for sample in samples))

    def test_random_controls_preserve_length_and_alphabet(self) -> None:
        samples = sample_random_controls(
            length=4,
            corpus_text="aabbcc",
            samples=20,
            rng=random.Random(1),
        )

        self.assertEqual(len(samples), 20)
        self.assertTrue(all(len(sample) == 4 for sample in samples))
        self.assertTrue(all(set(sample) <= {"a", "b", "c"} for sample in samples))

    def test_extension_band_prefers_adjusted_values(self) -> None:
        self.assertEqual(
            extension_band({"combined_min_p": 0.001, "combined_min_q": 0.04}),
            "extension_q_le_0.05",
        )
        self.assertEqual(
            extension_band({"combined_min_p": 0.04, "combined_min_q": 0.50}),
            "extension_uncorrected_p_le_0.05",
        )

    def test_all_controls_band_prefers_adjusted_values(self) -> None:
        self.assertEqual(
            all_controls_band({"all_controls_max_p": 0.001, "all_controls_max_q": 0.04}),
            "all_controls_q_le_0.05",
        )
        self.assertEqual(
            all_controls_band({"all_controls_max_p": 0.04, "all_controls_max_q": 0.50}),
            "all_controls_uncorrected_p_le_0.05",
        )

    def test_stable_seed_is_repeatable(self) -> None:
        self.assertEqual(stable_seed(1, "TR_NT", "row"), stable_seed(1, "TR_NT", "row"))
        self.assertNotEqual(stable_seed(1, "TR_NT", "row"), stable_seed(1, "SBLGNT", "row"))

    def test_normalize_target_row_accepts_audit_corpus_exports(self) -> None:
        row = normalize_target_row({"audit_corpus": "MT_WLC", "normalized_term": "יהוה"})

        self.assertEqual(row["corpus"], "MT_WLC")
        self.assertEqual(row["audit_corpus"], "MT_WLC")

    def test_summary_row_reports_control_max_and_ge_counts(self) -> None:
        row = summary_row(
            ExtensionTarget(
                target_id="MT_WLC_001",
                source_file="test.csv",
                row={
                    "corpus": "MT_WLC",
                    "term": "יהוה",
                    "normalized_term": "יהוה",
                    "skip": "3",
                    "direction": "forward",
                    "extension_type": "before_plus_term",
                    "extension_side": "before",
                    "extension_length": "2",
                    "extended_sequence": "עדיהוה",
                    "matched_examples": "עד יהוה",
                    "matched_refs": "DEU 4:30",
                    "matched_normalized": "עדיהוה",
                    "match_count": "6",
                    "extension_score": "302016",
                },
            ),
            ControlScores((0, 302016), (1200, 302015), ("א", "ב")),
            ControlScores((1,), (302016,), ("ג",)),
        )

        self.assertEqual(row["term_same_type_score_max"], 302016)
        self.assertEqual(row["term_same_type_ge_observed"], 1)
        self.assertEqual(row["term_any_score_max"], 302015)
        self.assertEqual(row["term_any_ge_observed"], 0)
        self.assertEqual(row["random_any_score_max"], 302016)
        self.assertEqual(row["random_any_ge_observed"], 1)
        self.assertEqual(row["combined_min_p"], 0.333333)
        self.assertEqual(row["all_controls_max_p"], 1.0)

    def test_write_markdown_accepts_custom_title_and_lead(self) -> None:
        row = {
            "extension_band": "not_unusual",
            "corpus": "MT_WLC",
            "term": "יהוה",
            "concept": "YHWH",
            "skip": "7",
            "extension_type": "term_plus_after",
            "extended_sequence": "יהוהאלהים",
            "observed_score": "1",
            "combined_min_p": "0.5",
            "combined_min_q": "0.5",
            "all_controls_max_q": "0.8",
            "all_controls_band": "not_unusual",
            "read": "not unusual under extension controls",
            "all_controls_read": "not unusual under all-control check",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "report.md"
            write_markdown(
                path,
                [row],
                title="Custom Control Report",
                lead="Custom lead text.",
                caution="Custom caution text.",
            )

            text = path.read_text(encoding="utf-8")

        self.assertIn("# Custom Control Report", text)
        self.assertIn("Custom lead text.", text)
        self.assertIn("Custom caution text.", text)
        self.assertNotIn("Controls are row-local and exploratory.", text)
        self.assertIn("floor-limited", text)
        self.assertIn("All-Control Band Counts", text)
        self.assertIn("Conservative All-Control Screens", text)
        self.assertIn("All-control q", text)
        self.assertNotIn("filtered NT", text)
        self.assertIn("`יהוה` (yhwh; English: YHWH)", text)
        self.assertIn("`יהוהאלהים` (yhwhlhym)", text)

    def test_prepare_targets_keeps_cross_corpus_overlaps(self) -> None:
        targets = [
            target("TR_NT", "υιος", "-4", "υιοστησ"),
            target("SBLGNT", "υιος", "-4", "υιοστησ"),
            target("SBLGNT", "θεος", "36", "εισθεοσ"),
        ]

        prepared = prepare_targets(
            targets,
            SimpleNamespace(
                require_cross_corpus_overlap=True,
                include_overlap_key=[],
                require_center_exact=False,
                dedupe_targets=True,
            ),
        )

        self.assertEqual([row.corpus for row in prepared], ["TR_NT", "SBLGNT"])
        self.assertTrue(all(row.row["overlap_corpora"] == "SBLGNT,TR_NT" for row in prepared))
        self.assertTrue(all(row.row["overlap_group_size"] == "2" for row in prepared))

    def test_prepare_targets_can_filter_to_specific_overlap_key(self) -> None:
        targets = [
            target("TR_NT", "υιος", "-4", "υιοστησ"),
            target("SBLGNT", "υιος", "-4", "υιοστησ"),
            target("TR_NT", "δοξα", "21", "δοξανωσ"),
            target("SBLGNT", "δοξα", "21", "δοξανωσ"),
        ]

        prepared = prepare_targets(
            targets,
            SimpleNamespace(
                require_cross_corpus_overlap=True,
                include_overlap_key=[
                    "δοξα|21|forward|term_plus_after|δοξανωσ|δοξανωσ",
                ],
                require_center_exact=False,
                dedupe_targets=True,
            ),
        )

        self.assertEqual([row.normalized_term for row in prepared], ["δοξα", "δοξα"])

    def test_require_overlap_corpora_filters_to_independent_source_groups(self) -> None:
        targets = [
            target("TR_NT", "δοξα", "21", "δοξανωσ"),
            target("SBLGNT", "δοξα", "21", "δοξανωσ"),
            target("BYZ_NT", "δοξα", "21", "δοξανωσ"),
            target("TR_NT", "υιος", "-4", "υιοστησ"),
            target("SBLGNT", "υιος", "-4", "υιοστησ"),
        ]

        prepared = require_overlap_corpora_targets(targets, {"BYZ_NT"})

        self.assertEqual(
            [(row.corpus, row.normalized_term) for row in prepared],
            [("TR_NT", "δοξα"), ("SBLGNT", "δοξα"), ("BYZ_NT", "δοξα")],
        )

    def test_prepare_targets_can_filter_to_exact_center_context(self) -> None:
        targets = [
            target("TR_NT", "δοξα", "21", "δοξανωσ", start="1", end="85", center="43"),
            target("SBLGNT", "δοξα", "21", "δοξανωσ", start="2", end="86", center="44"),
            target("SBLGNT", "υιος", "25", "ουουιοσ", start="3", end="78", center="41"),
        ]
        surface_context = {
            ("TR_NT", "δοξα", "δοξα", "21", "1", "85", "43"): {"center_exact": "True"},
            ("SBLGNT", "δοξα", "δοξα", "21", "2", "86", "44"): {
                "center_exact": "True"
            },
            ("SBLGNT", "υιος", "υιος", "25", "3", "78", "41"): {"center_exact": "False"},
        }

        prepared = prepare_targets(
            targets,
            SimpleNamespace(
                require_cross_corpus_overlap=False,
                include_overlap_key=[],
                require_center_exact=True,
                dedupe_targets=True,
            ),
            surface_context=surface_context,
        )

        self.assertEqual([row.normalized_term for row in prepared], ["δοξα", "δοξα"])

    def test_score_controls_batches_queries_and_preserves_duplicate_samples(self) -> None:
        corpus = extension_corpus()
        lexicon = build_extension_lexicon(corpus, max_phrase_words=2)
        control_scores = score_controls(
            corpus,
            lexicon,
            target("TR_NT", "αβ", "1", "αβγδ"),
            ("αβ", "αβ", "βγ"),
            SimpleNamespace(
                max_before=2,
                max_after=2,
                include_both_sided=True,
                max_extensions_per_hit=20,
                min_extension_length=1,
                match_kind_prefix="phrase_",
            ),
        )

        self.assertEqual(control_scores.same_type_scores[0], 2211)
        self.assertEqual(control_scores.same_type_scores[1], 2211)
        self.assertEqual(control_scores.same_type_scores[2], 0)
        self.assertEqual(control_scores.any_scores[:2], (2211, 2211))
        self.assertGreater(control_scores.any_scores[2], control_scores.same_type_scores[2])

    def test_score_control_sets_matches_separate_scans(self) -> None:
        corpus = extension_corpus()
        lexicon = build_extension_lexicon(corpus, max_phrase_words=2)
        args = SimpleNamespace(
            max_before=2,
            max_after=2,
            include_both_sided=True,
            max_extensions_per_hit=20,
            min_extension_length=1,
            match_kind_prefix="phrase_",
        )
        row_target = target("TR_NT", "αβ", "1", "αβγδ")
        term_queries = ("αβ", "αβ")
        random_queries = ("βγ",)

        combined_term, combined_random = score_control_sets(
            corpus,
            lexicon,
            row_target,
            term_queries,
            random_queries,
            args,
        )

        self.assertEqual(
            combined_term,
            score_controls(corpus, lexicon, row_target, term_queries, args),
        )
        self.assertEqual(
            combined_random,
            score_controls(corpus, lexicon, row_target, random_queries, args),
        )

    def test_score_hit_extensions_matches_full_extension_path(self) -> None:
        corpus = extension_corpus()
        lexicon = build_extension_lexicon(corpus, max_phrase_words=2)
        args = SimpleNamespace(
            max_before=2,
            max_after=2,
            include_both_sided=True,
            max_extensions_per_hit=20,
            min_extension_length=1,
            match_kind_prefix="phrase_",
        )
        hit = build_hit(corpus, "αβ", "αβ", 1, 0, 1)
        expected_scores = [
            extension_score(
                extension.extension_type,
                extension.extension_length,
                extension.match_kind,
                extension.match_count,
            )
            for extension in extensions_for_hit(
                corpus,
                hit,
                lexicon,
                max_before=args.max_before,
                max_after=args.max_after,
                include_both_sided=args.include_both_sided,
                max_extensions=args.max_extensions_per_hit,
            )
            if extension.extension_type == "term_plus_after"
            and extension.extension_length >= args.min_extension_length
            and extension.match_kind.startswith(args.match_kind_prefix)
        ]

        any_score, same_type_scores = score_hit_extensions(
            corpus,
            lexicon,
            query="αβ",
            signed_skip=1,
            start=0,
            end=1,
            extension_types={"term_plus_after"},
            high_priority_scale=False,
            args=args,
        )

        self.assertEqual(any_score, max(expected_scores))
        self.assertEqual(same_type_scores["term_plus_after"], max(expected_scores))


def extension_corpus() -> Corpus:
    return Corpus(
        name="extension",
        language="greek",
        keep_hebrew_final_forms=False,
        text="αβγδ",
        verses=(
            VerseSpan("test", "Test 1:1", "Test", "1", "1", "αβ γδ", 0, 3, 4),
        ),
        position_to_verse=(0, 0, 0, 0),
        words=(
            WordSpan("test", "Test 1:1", "Test", "1", "1", 1, "αβ", "αβ", 0, 1, 2),
            WordSpan("test", "Test 1:1", "Test", "1", "1", 2, "γδ", "γδ", 2, 3, 2),
        ),
        position_to_word=(0, 0, 1, 1),
    )


def target(
    corpus: str,
    term: str,
    skip: str,
    extended_sequence: str,
    *,
    start: str = "10",
    end: str = "20",
    center: str = "15",
) -> ExtensionTarget:
    return ExtensionTarget(
        target_id=f"{corpus}_{term}",
        source_file="test.csv",
        row={
            "corpus": corpus,
            "term": term,
            "normalized_term": term,
            "skip": skip,
            "direction": "backward" if skip.startswith("-") else "forward",
            "extension_type": "term_plus_after",
            "extended_sequence": extended_sequence,
            "matched_normalized": extended_sequence,
            "start_offset": start,
            "end_offset": end,
            "center_offset": center,
        },
    )


if __name__ == "__main__":
    unittest.main()
