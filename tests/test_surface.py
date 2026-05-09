import unittest

from els.cli import process_surface_term, process_surface_term_group
from els.corpus import Corpus, VerseSpan, WordSpan
from els.search import find_els
from els.surface import (
    SurfaceTerm,
    build_surface_context_index,
    normalize_verses,
    surface_context_for_hit,
    surface_context_for_hit_indexed,
)


def sample_corpus() -> Corpus:
    verses = (
        VerseSpan("test", "Test 1:1", "Test", "1", "1", "αβ γδ", 0, 3, 4),
        VerseSpan("test", "Test 1:2", "Test", "1", "2", "εζ ηθ", 4, 7, 4),
    )
    words = (
        WordSpan("test", "Test 1:1", "Test", "1", "1", 1, "αβ", "αβ", 0, 1, 2),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 2, "γδ", "γδ", 2, 3, 2),
        WordSpan("test", "Test 1:2", "Test", "1", "2", 1, "εζ", "εζ", 4, 5, 2),
        WordSpan("test", "Test 1:2", "Test", "1", "2", 2, "ηθ", "ηθ", 6, 7, 2),
    )
    return Corpus(
        name="test",
        language="greek",
        keep_hebrew_final_forms=False,
        text="αβγδεζηθ",
        verses=verses,
        position_to_verse=(0, 0, 0, 0, 1, 1, 1, 1),
        words=words,
        position_to_word=(0, 0, 1, 1, 2, 2, 3, 3),
    )


def capped_order_corpus() -> Corpus:
    text = "ξαξαβξβ"
    return Corpus(
        name="capped",
        language="greek",
        keep_hebrew_final_forms=False,
        text=text,
        verses=(
            VerseSpan("test", "Test 1:1", "Test", "1", "1", text, 0, len(text) - 1, len(text)),
        ),
        position_to_verse=tuple(0 for _char in text),
    )


class SurfaceTests(unittest.TestCase):
    def test_surface_context_flags_center_and_span(self) -> None:
        corpus = sample_corpus()
        hit = list(find_els(corpus, "αγε", min_skip=2, max_skip=2))[0]
        term = SurfaceTerm("terms.csv", "alpha", "Alpha", "letters", "γδ", "γδ")
        related = [
            term,
            SurfaceTerm("terms.csv", "epsilon", "Epsilon", "letters", "εζ", "εζ"),
        ]

        normalized_verses = normalize_verses(corpus)
        context = surface_context_for_hit(
            corpus,
            hit,
            term,
            related,
            normalized_verses,
        )
        indexed_context = surface_context_for_hit_indexed(
            corpus,
            hit,
            term,
            related,
            build_surface_context_index(corpus, related, normalized_verses),
        )

        self.assertEqual(context.best_context, "exact_center")
        self.assertEqual(indexed_context, context)
        self.assertTrue(context.center_word_exact)
        self.assertTrue(context.center_exact)
        self.assertTrue(context.span_exact)
        self.assertEqual(context.span_exact_refs, "Test 1:1")
        self.assertFalse(context.center_word_same_category)
        self.assertFalse(context.center_same_category)
        self.assertTrue(context.span_same_category)
        self.assertIn("epsilon@Test 1:2", context.span_same_category_refs)

    def test_surface_context_flags_related_center_word(self) -> None:
        corpus = sample_corpus()
        hit = list(find_els(corpus, "αγε", min_skip=2, max_skip=2))[0]
        term = SurfaceTerm("terms.csv", "alpha", "Alpha", "letters", "αβ", "αβ")
        same_concept = SurfaceTerm("terms.csv", "gamma", "Alpha", "letters", "γδ", "γδ")
        same_category = SurfaceTerm("terms.csv", "gamma2", "Gamma", "letters", "γδ", "γδ")

        context = surface_context_for_hit_indexed(
            corpus,
            hit,
            term,
            [term, same_concept, same_category],
            build_surface_context_index(
                corpus,
                [term, same_concept, same_category],
                normalize_verses(corpus),
            ),
        )

        self.assertFalse(context.center_word_exact)
        self.assertTrue(context.center_word_same_concept)
        self.assertTrue(context.center_word_same_category)
        self.assertIn("gamma", context.center_word_same_concept_terms)
        self.assertIn("gamma2", context.center_word_same_category_terms)

    def test_surface_group_matches_single_term_path_with_hit_cap(self) -> None:
        corpus = sample_corpus()
        terms = [
            SurfaceTerm("terms.csv", "forward", "Forward", "letters", "αγε", "αγε"),
            SurfaceTerm("terms.csv", "backward", "Backward", "letters", "εγα", "εγα"),
        ]
        context_index = build_surface_context_index(
            corpus,
            terms,
            normalize_verses(corpus),
        )
        options = {
            "min_skip": 2,
            "max_skip": 2,
            "direction": "both",
            "min_term_length": 1,
            "max_hits_per_term": 1,
            "include_all": True,
        }

        expected = [
            process_surface_term("TEST", corpus, term, terms, context_index, options)
            for term in terms
        ]
        grouped = process_surface_term_group(
            "TEST",
            corpus,
            terms,
            terms,
            context_index,
            options,
        )

        self.assertEqual(
            [result.summary_row for result in grouped],
            [result.summary_row for result in expected],
        )
        self.assertEqual(
            [result.surface_rows for result in grouped],
            [result.surface_rows for result in expected],
        )

    def test_surface_group_hit_cap_preserves_start_order(self) -> None:
        corpus = capped_order_corpus()
        terms = [
            SurfaceTerm("terms.csv", "alpha_beta", "Alpha Beta", "letters", "αβ", "αβ"),
        ]
        context_index = build_surface_context_index(
            corpus,
            terms,
            normalize_verses(corpus),
        )
        options = {
            "min_skip": 3,
            "max_skip": 3,
            "direction": "forward",
            "min_term_length": 1,
            "max_hits_per_term": 1,
            "include_all": True,
        }

        expected = process_surface_term("TEST", corpus, terms[0], terms, context_index, options)
        grouped = process_surface_term_group("TEST", corpus, terms, terms, context_index, options)[0]

        self.assertEqual(grouped.surface_rows, expected.surface_rows)
        self.assertEqual(grouped.surface_rows[0]["start_offset"], 1)


if __name__ == "__main__":
    unittest.main()
