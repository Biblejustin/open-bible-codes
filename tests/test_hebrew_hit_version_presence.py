import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from els.corpus import Corpus, VerseSpan, WordSpan
from els.protocol_runner import load_protocol
from scripts.analyze_hebrew_hit_version_presence import (
    CorpusHitResult,
    CorpusMetadata,
    TermRow,
    canonical_ref,
    collect_hits,
    current_read_lines,
    merge_corpus_hit_results,
    presence_scope,
    read_terms,
    resolve_corpus_jobs,
    term_read,
    term_summary_rows,
)


class HebrewHitVersionPresenceTests(unittest.TestCase):
    def test_canonical_ref_normalizes_usfm_books(self) -> None:
        self.assertEqual(canonical_ref("GEN 1:1"), "Gen 1:1")
        self.assertEqual(canonical_ref("1SA 3:4"), "1Sam 3:4")
        self.assertEqual(canonical_ref("Song 2:1"), "Song 2:1")
        self.assertEqual(canonical_ref("MAT 1:1"), "Matt 1:1")
        self.assertEqual(canonical_ref("Matt 1:1"), "Matt 1:1")
        self.assertEqual(canonical_ref("1CO 13:1"), "1Cor 13:1")
        self.assertEqual(canonical_ref("1 Cor 13:1"), "1Cor 13:1")

    def test_presence_scope_labels_leningrad_stability(self) -> None:
        self.assertEqual(
            presence_scope(["MT_WLC", "UXLC", "EBIBLE_WLC"], ["MAM", "UHB"]),
            "present_all_leningrad_streams",
        )
        self.assertEqual(
            presence_scope(["MT_WLC", "UHB"], ["UXLC"]),
            "present_multiple_sources",
        )
        self.assertEqual(
            presence_scope(["UHB"], ["MT_WLC", "UXLC"]),
            "source_specific",
        )
        self.assertEqual(
            presence_scope(["TR_NT", "SBLGNT"], ["BYZ_NT"], stable_labels=set()),
            "present_multiple_sources",
        )

    def test_term_read_prefers_strongest_available_scope(self) -> None:
        self.assertIn(
            "all observed",
            term_read({"present_all_observed_sources": 1}, 3),
        )
        self.assertIn(
            "Leningrad",
            term_read({"present_all_leningrad_streams": 2}, 4),
        )
        self.assertIn("no exact", term_read({}, 0))

    def test_zero_hit_terms_keep_metadata(self) -> None:
        rows = term_summary_rows(
            pattern_rows=[],
            records=[],
            observed={"catering_h": {"MT_WLC", "UXLC"}},
            term_lookup={
                "catering_h": TermRow(
                    term_id="catering_h",
                    concept="Catering",
                    category="local_terms",
                    term="קייטרינג",
                )
            },
            normalized_terms={"catering_h": "קייטרינג"},
        )
        self.assertEqual(rows[0]["term_id"], "catering_h")
        self.assertEqual(rows[0]["concept"], "Catering")
        self.assertEqual(rows[0]["term"], "קייטרינג")
        self.assertEqual(rows[0]["normalized_term"], "קייטרינג")
        self.assertEqual(rows[0]["read"], "no exact patterns in capped scan")

    def test_read_terms_supports_category_filter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "terms.csv"
            path.write_text(
                "\n".join(
                    [
                        "term_id,concept,category,language,term,notes",
                        "torah_h,Torah,core,hebrew,תורה,",
                        "trump_h,Trump,modern,hebrew,טראמפ,",
                        "jesus_g,Jesus,core,greek,ιησους,",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            rows = read_terms([path], categories=["modern"])
        self.assertEqual([row.term_id for row in rows], ["trump_h"])

    def test_read_terms_supports_language_filter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "terms.csv"
            path.write_text(
                "\n".join(
                    [
                        "term_id,concept,category,language,term,notes",
                        "torah_h,Torah,core,hebrew,תורה,",
                        "jesus_g,Jesus,core,greek,ιησους,",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            rows = read_terms([path], language="greek")
        self.assertEqual([row.term_id for row in rows], ["jesus_g"])

    def test_read_terms_rejects_duplicate_selected_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            left = Path(tmp) / "left.csv"
            right = Path(tmp) / "right.csv"
            content = "\n".join(
                [
                    "term_id,concept,category,language,term,notes",
                    "torah_h,Torah,core,hebrew,תורה,",
                ]
            ) + "\n"
            left.write_text(content, encoding="utf-8")
            right.write_text(content, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate selected term_id"):
                read_terms([left, right])

    def test_read_terms_can_keep_first_duplicate_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            left = Path(tmp) / "left.csv"
            right = Path(tmp) / "right.csv"
            header = "term_id,concept,category,language,term,notes\n"
            left.write_text(header + "torah_h,Torah,core,hebrew,תורה,left\n", encoding="utf-8")
            right.write_text(header + "torah_h,Torah Later,core,hebrew,תרוה,right\n", encoding="utf-8")
            rows = read_terms([left, right], duplicate_policy="first")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].concept, "Torah")

    def test_collect_hits_caps_each_normalized_query_in_bulk(self) -> None:
        terms = [
            TermRow("alpha_beta_g", "Alpha Beta", "test", "αβ"),
            TermRow("beta_alpha_g", "Beta Alpha", "test", "βα"),
        ]
        records, observed, _lookup, normalized = collect_hits(
            {"TEST": sample_corpus()},
            terms,
            Namespace(
                min_skip=1,
                max_skip=2,
                direction="both",
                min_term_length=2,
                max_hits_per_term=2,
            ),
        )

        counts = {term.term_id: 0 for term in terms}
        for record in records:
            counts[record.term.term_id] += 1
        self.assertEqual(counts, {"alpha_beta_g": 2, "beta_alpha_g": 2})
        self.assertEqual(observed, {"alpha_beta_g": {"TEST"}, "beta_alpha_g": {"TEST"}})
        self.assertEqual(normalized, {"alpha_beta_g": "αβ", "beta_alpha_g": "βα"})

    def test_resolve_corpus_jobs_caps_to_corpus_count(self) -> None:
        self.assertEqual(resolve_corpus_jobs(0, 3), 3)
        self.assertEqual(resolve_corpus_jobs(8, 3), 3)
        self.assertEqual(resolve_corpus_jobs(1, 3), 1)

    def test_current_read_lines_summarizes_scope_and_absences(self) -> None:
        lines = current_read_lines(
            [
                {"presence_scope": "present_all_observed_sources"},
                {"presence_scope": "source_specific"},
            ],
            [
                {
                    "term_id": "usa_abbrev_h",
                    "unique_patterns": "2",
                    "all_observed_patterns": "2",
                    "total_hits": "10",
                },
                {
                    "term_id": "united_states_h",
                    "unique_patterns": "0",
                    "all_observed_patterns": "0",
                    "total_hits": "0",
                },
            ],
        )
        text = "\n".join(lines)
        self.assertIn("2 exact ref-key pattern rows", text)
        self.assertIn("`usa_abbrev_h`", text)
        self.assertIn("`united_states_h`", text)

    def test_modern_geopolitical_protocol_uses_all_hebrew_modern_rows(self) -> None:
        protocol = load_protocol("protocols/hebrew_modern_geopolitical_version_presence.toml")
        step = protocol["steps"][0]
        argv = step["argv"]

        self.assertEqual(protocol["name"], "hebrew_modern_geopolitical_version_presence")
        self.assertIn("terms/modern_names_dates.csv", argv)
        self.assertIn("--all-concepts", argv)
        self.assertIn("docs/HEBREW_MODERN_GEOPOLITICAL_VERSION_PRESENCE.md", step["outputs"])

    def test_merge_corpus_hit_results_preserves_source_order_normalization(self) -> None:
        first = CorpusHitResult(
            label="FIRST",
            metadata=CorpusMetadata("first", 1, 2),
            records=[],
            observed={"term": {"FIRST"}},
            normalized_by_term={"term": "אב"},
        )
        second = CorpusHitResult(
            label="SECOND",
            metadata=CorpusMetadata("second", 1, 2),
            records=[],
            observed={"term": {"SECOND"}},
            normalized_by_term={"term": "אב-final"},
        )

        _records, observed, normalized, metadata = merge_corpus_hit_results([first, second])

        self.assertEqual(observed, {"term": {"FIRST", "SECOND"}})
        self.assertEqual(normalized, {"term": "אב"})
        self.assertEqual(sorted(metadata), ["FIRST", "SECOND"])


def sample_corpus() -> Corpus:
    verse = VerseSpan(
        source="test",
        ref="Test 1:1",
        book="Test",
        chapter="1",
        verse="1",
        raw_text="αβ αβ αβ",
        norm_start=0,
        norm_end=5,
        norm_length=6,
    )
    words = (
        WordSpan("test", "Test 1:1", "Test", "1", "1", 1, "αβ", "αβ", 0, 1, 2),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 2, "αβ", "αβ", 2, 3, 2),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 3, "αβ", "αβ", 4, 5, 2),
    )
    return Corpus(
        name="test",
        language="greek",
        keep_hebrew_final_forms=False,
        text="αβαβαβ",
        verses=(verse,),
        position_to_verse=tuple(0 for _ in range(6)),
        words=words,
        position_to_word=(0, 0, 1, 1, 2, 2),
    )


if __name__ == "__main__":
    unittest.main()
