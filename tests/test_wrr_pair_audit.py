import unittest

from els.corpus import Corpus, VerseSpan
from scripts.analyze_gog_magog_pairs import HitLite
from scripts.analyze_wrr_pair_audit import (
    APP_CATEGORY,
    DATE_CATEGORY,
    WrrTerm,
    audit_pair,
    collect_pair_terms,
    example_row,
    summarize_concepts,
)


class WrrPairAuditTests(unittest.TestCase):
    def test_collect_pair_terms_keeps_same_concept_pairs(self) -> None:
        rows = [
            row("app", "WRR2 01", APP_CATEGORY, "greek", "αβγ"),
            row("date", "WRR2 01", DATE_CATEGORY, "greek", "δεζ"),
            row("orphan", "WRR2 02", APP_CATEGORY, "greek", "ηθι"),
            row("short", "WRR2 03", DATE_CATEGORY, "greek", "κ"),
        ]

        terms = collect_pair_terms(rows, sample_corpus(), min_term_length=2)

        self.assertEqual(list(terms), ["WRR2 01"])
        self.assertEqual({term.term_id for term in terms["WRR2 01"]}, {"app", "date"})

    def test_collect_pair_terms_applies_max_length(self) -> None:
        rows = [
            row("app", "WRR2 01", APP_CATEGORY, "greek", "αβγδε"),
            row("date", "WRR2 01", DATE_CATEGORY, "greek", "ζηθικ"),
            row("long", "WRR2 02", APP_CATEGORY, "greek", "αβγδεζηθι"),
            row("date2", "WRR2 02", DATE_CATEGORY, "greek", "αβγδε"),
        ]

        terms = collect_pair_terms(
            rows,
            sample_corpus(),
            min_term_length=5,
            max_term_length=8,
        )

        self.assertEqual(list(terms), ["WRR2 01"])

    def test_audit_pair_reports_strict_same_chapter_same_skip_pair(self) -> None:
        corpus = sample_corpus()
        app = WrrTerm("app", "WRR2 01", APP_CATEGORY, "αβ", "αβ")
        date = WrrTerm("date", "WRR2 01", DATE_CATEGORY, "γδ", "γδ")
        hits_by_query = {
            "αβ": [HitLite("αβ", 1, 0, 1)],
            "γδ": [HitLite("γδ", 1, 2, 3)],
        }

        pair_row, examples = audit_pair(
            "SAMPLE",
            corpus,
            app,
            date,
            hits_by_query,
            max_gap=5,
            chapter_cache={},
        )

        self.assertEqual(pair_row["all_pairs_within_gap"], 1)
        self.assertEqual(pair_row["same_chapter_pairs_within_gap"], 1)
        self.assertEqual(pair_row["same_signed_skip_pairs_within_gap"], 1)
        self.assertEqual(pair_row["strict_pairs_within_gap"], 1)
        self.assertEqual(pair_row["best_span_gap"], 1)
        self.assertGreater(float(pair_row["best_example_wrr_alpha"]), 0)
        self.assertEqual(len(examples), 1)
        self.assertGreater(float(example_row(corpus, app, date, pair_row, examples[0])["wrr_alpha"]), 0)

    def test_summarize_concepts_uses_best_gap(self) -> None:
        rows = [
            pair_summary("WRR2 01", "app_a", "date", 3, 8),
            pair_summary("WRR2 01", "app_b", "date", 1, 2),
        ]

        concepts = summarize_concepts("SAMPLE", rows)

        self.assertEqual(concepts[0]["pair_rows"], 2)
        self.assertEqual(concepts[0]["all_pairs_within_gap"], 4)
        self.assertEqual(concepts[0]["best_span_gap"], 2)
        self.assertEqual(concepts[0]["best_appellation_term_id"], "app_b")
        self.assertEqual(concepts[0]["best_wrr_alpha"], 3.4)


def sample_corpus() -> Corpus:
    return Corpus(
        name="sample",
        language="greek",
        keep_hebrew_final_forms=False,
        text="αβγδεζηθι",
        verses=(
            VerseSpan("sample", "Sample 1:1", "Sample", "1", "1", "αβγδεζηθι", 0, 8, 9),
        ),
        position_to_verse=tuple(0 for _index in range(9)),
    )


def row(term_id: str, concept: str, category: str, language: str, term: str) -> dict[str, str]:
    return {
        "term_id": term_id,
        "concept": concept,
        "category": category,
        "language": language,
        "term": term,
    }


def pair_summary(
    concept: str,
    app_id: str,
    date_id: str,
    close_pairs: int,
    best_gap: int,
) -> dict[str, object]:
    return {
        "corpus": "SAMPLE",
        "concept": concept,
        "appellation_term_id": app_id,
        "date_term_id": date_id,
        "all_pairs_within_gap": close_pairs,
        "all_overlap_pairs": 0,
        "same_chapter_pairs_within_gap": 0,
        "same_signed_skip_pairs_within_gap": 0,
        "strict_pairs_within_gap": 0,
        "best_span_gap": best_gap,
        "best_center_distance": best_gap + 0.5,
        "best_example_wrr_alpha": 3.4 if app_id == "app_b" else 1.2,
    }


if __name__ == "__main__":
    unittest.main()
