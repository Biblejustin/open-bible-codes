import argparse
import unittest
from pathlib import Path

from els.surface import SurfaceContext, SurfaceTerm
from scripts.analyze_apocrypha_bridge_context import (
    TermLookup,
    bucket_for_context,
    choose_surface_term,
    letter_positions,
    manifest_args,
)


class ApocryphaBridgeContextTests(unittest.TestCase):
    def test_letter_positions_extracts_offsets(self) -> None:
        self.assertEqual(
            letter_positions("1:h@2ES 16:78:apocrypha:3076409;2:e@MAT 1:1:canonical:3076412"),
            [3076409, 3076412],
        )

    def test_bucket_prefers_center_word_flags(self) -> None:
        context = surface_context(
            center_word_same_category=True,
            center_exact=True,
            span_exact=True,
        )

        self.assertEqual(bucket_for_context(context), "center_word_same_category")

    def test_choose_surface_term_prefers_declared_term_id(self) -> None:
        by_id_term = SurfaceTerm("terms.csv", "specific", "Specific", "category", "Alpha", "alpha")
        fallback_term = SurfaceTerm("terms.csv", "fallback", "Fallback", "category", "Alpha", "alpha")
        lookup = TermLookup(
            terms=(by_id_term, fallback_term),
            by_id={"specific": by_id_term, "fallback": fallback_term},
            by_normalized={"alpha": (fallback_term, by_id_term)},
        )

        self.assertIs(
            choose_surface_term(
                {"term_ids": "specific;other", "normalized_term": "alpha"},
                lookup,
            ),
            by_id_term,
        )

    def test_choose_surface_term_falls_back_to_normalized(self) -> None:
        fallback_term = SurfaceTerm("terms.csv", "fallback", "Fallback", "category", "Alpha", "alpha")
        lookup = TermLookup(
            terms=(fallback_term,),
            by_id={"fallback": fallback_term},
            by_normalized={"alpha": (fallback_term,)},
        )

        self.assertIs(
            choose_surface_term({"term_ids": "missing", "normalized_term": "alpha"}, lookup),
            fallback_term,
        )

    def test_manifest_args_converts_paths(self) -> None:
        args = argparse.Namespace(
            config=Path("configs/example.toml"),
            terms=[Path("terms/a.csv"), Path("terms/b.csv")],
            jobs=0,
        )

        self.assertEqual(
            manifest_args(args),
            {
                "config": "configs/example.toml",
                "terms": ["terms/a.csv", "terms/b.csv"],
                "jobs": 0,
            },
        )


def surface_context(**overrides: bool) -> SurfaceContext:
    values = {
        "best_context": "",
        "center_word_exact": False,
        "center_word_same_concept": False,
        "center_word_same_category": False,
        "center_exact": False,
        "center_same_concept": False,
        "center_same_category": False,
        "span_exact": False,
        "span_same_concept": False,
        "span_same_category": False,
        "center_word_same_concept_terms": "",
        "center_word_same_category_terms": "",
        "center_same_concept_terms": "",
        "center_same_category_terms": "",
        "span_exact_refs": "",
        "span_same_concept_refs": "",
        "span_same_category_refs": "",
    }
    values.update(overrides)
    return SurfaceContext(**values)
