import argparse
import unittest
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.analyze_apocrypha_bridge_term_shuffled_controls import (
    manifest_args,
    run_samples,
    summarize_terms,
    term_sample_records,
    write_markdown,
)


class ApocryphaBridgeTermShuffledControlsTests(unittest.TestCase):
    def test_term_sample_records_summarize_bridge_types(self) -> None:
        rows = term_sample_records(
            2,
            20260510,
            {
                "alpha": Counter({"canonical_to_apocrypha": 2, "apocrypha_to_canonical": 1}),
                "beta": Counter({"multi_segment_bridge": 3}),
            },
        )

        self.assertEqual(
            rows,
            [
                {
                    "sample": 2,
                    "seed": 20260510,
                    "normalized_term": "alpha",
                    "bridge_rows": 3,
                    "canonical_to_apocrypha": 2,
                    "apocrypha_to_canonical": 1,
                    "multi_segment_bridge": 0,
                },
                {
                    "sample": 2,
                    "seed": 20260510,
                    "normalized_term": "beta",
                    "bridge_rows": 3,
                    "canonical_to_apocrypha": 0,
                    "apocrypha_to_canonical": 0,
                    "multi_segment_bridge": 3,
                },
            ],
        )

    def test_summarize_terms_uses_zero_for_missing_sample_terms(self) -> None:
        observed = [
            {"normalized_term": "alpha"},
            {"normalized_term": "alpha"},
            {"normalized_term": "beta"},
        ]
        term_samples = [
            {"sample": 1, "normalized_term": "alpha", "bridge_rows": 1},
            {"sample": 2, "normalized_term": "alpha", "bridge_rows": 3},
            {"sample": 1, "normalized_term": "beta", "bridge_rows": 2},
        ]
        term_records = {
            "alpha": [{"term_id": "eng_alpha", "concept": "Alpha", "category": "test"}],
            "beta": [{"term_id": "eng_beta", "concept": "Beta", "category": "test"}],
        }

        rows = summarize_terms(observed, term_samples, term_records, samples=3)
        by_term = {row["normalized_term"]: row for row in rows}

        self.assertEqual(by_term["alpha"]["sample_min"], 0)
        self.assertEqual(by_term["alpha"]["sample_max"], 3)
        self.assertEqual(by_term["alpha"]["samples_ge_observed"], 1)
        self.assertEqual(by_term["alpha"]["p_ge"], 0.5)
        self.assertEqual(by_term["alpha"]["q_ge"], 0.5)
        self.assertEqual(by_term["beta"]["sample_min"], 0)
        self.assertEqual(by_term["beta"]["samples_ge_observed"], 1)
        self.assertEqual(by_term["beta"]["q_ge"], 0.5)

    def test_summarize_terms_filters_to_declared_term_records(self) -> None:
        observed = [
            {"normalized_term": "alpha"},
            {"normalized_term": "alpha"},
            {"normalized_term": "outside"},
            {"normalized_term": "outside"},
        ]
        term_samples = [
            {"sample": 1, "normalized_term": "alpha", "bridge_rows": 1},
            {"sample": 1, "normalized_term": "outside", "bridge_rows": 99},
        ]
        term_records = {
            "alpha": [{"term_id": "eng_alpha", "concept": "Alpha", "category": "test"}],
        }

        rows = summarize_terms(observed, term_samples, term_records, samples=2)

        self.assertEqual([row["normalized_term"] for row in rows], ["alpha"])

    def test_run_samples_resumes_zero_term_sample_without_term_rows(self) -> None:
        cached_sample = {
            "sample": 1,
            "seed": 123,
            "bridge_rows": 0,
            "terms_with_bridge_rows": 0,
            "canonical_to_apocrypha": 0,
            "apocrypha_to_canonical": 0,
            "multi_segment_bridge": 0,
        }
        args = argparse.Namespace(
            samples=1,
            seed=123,
            min_skip=2,
            max_skip=4,
            direction="both",
            jobs=1,
            resume_samples=False,
        )

        sample_rows, term_rows = run_samples(
            "abc",
            "def",
            {},
            {},
            args,
            existing_sample_rows=[cached_sample],
            existing_term_sample_rows=[],
        )

        self.assertEqual(sample_rows, [cached_sample])
        self.assertEqual(term_rows, [])

    def test_manifest_args_converts_terms_paths(self) -> None:
        args = argparse.Namespace(terms=[Path("terms/a.csv")], samples=10)

        self.assertEqual(manifest_args(args), {"terms": ["terms/a.csv"], "samples": 10})

    def test_markdown_displays_transliteration_and_english_gloss(self) -> None:
        args = argparse.Namespace(
            canonical_label="Test",
            samples=1,
            seed=1,
            min_skip=2,
            max_skip=4,
            direction="both",
            min_term_length=3,
            jobs=1,
            resume_samples=False,
            canonical_config=Path("configs/test.toml"),
            observed=Path("observed.csv"),
            terms=[Path("terms/test.csv")],
            sample_out=Path("sample.csv"),
            term_sample_out=Path("term_samples.csv"),
            term_summary_out=Path("term_summary.csv"),
            markdown_out=Path("report.md"),
            manifest_out=Path("manifest.json"),
        )
        term_summary = [
            {
                "rank": 1,
                "normalized_term": "ישוע",
                "concepts": "Yeshua",
                "observed_bridge_rows": 2,
                "sample_max": 0,
                "sample_mean": 0,
                "samples_ge_observed": 0,
                "p_ge": 0.5,
                "q_ge": 0.5,
                "observed_minus_sample_max": 2,
                "observed_gt_sample_max": "True",
            }
        ]
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "bridge.md"
            write_markdown(
                path,
                term_summary,
                [{"bridge_rows": 0}],
                fake_corpus(),
                fake_boundary(),
                args,
            )

            text = path.read_text(encoding="utf-8")
        self.assertIn("`ישוע` (Yeshua; English: Yeshua)", text)


def fake_corpus() -> object:
    class Corpus:
        text = "abcdef"

    return Corpus()


def fake_boundary() -> dict[str, int]:
    return {"canonical_prefix_letters": 3, "apocrypha_block_letters": 3}
