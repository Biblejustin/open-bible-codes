import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts.classify_centered_relevance import sha256_file
from scripts.build_crd_comparison import build_crd_comparison
from scripts.run_crd_density import run_crd_density
from tests.test_classify_centered_relevance import MockLLMClient


class CRDDensityRunnerTests(unittest.TestCase):
    def test_deterministic_mode_computes_density(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = build_synthetic_run(Path(tmp), "deterministic")

            run_crd_density(root / "protocol.toml")
            rows = read_csv(root / "reports" / "crd" / "density_matrix.csv")

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["classifier_mode"], "deterministic")
        self.assertEqual(rows[0]["total_centered_hits"], "1")
        self.assertEqual(rows[0]["relevant_centered_hits"], "1")
        self.assertEqual(rows[0]["relevance_rate"], "1")

    def test_llm_mode_computes_density(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = build_synthetic_run(Path(tmp), "llm")

            run_crd_density(root / "protocol.toml", api_client=MockLLMClient())
            rows = read_csv(root / "reports" / "crd" / "density_matrix.csv")

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["classifier_mode"], "llm")
        self.assertEqual(rows[0]["relevant_centered_hits"], "1")

    def test_parallel_mode_produces_agreement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = build_synthetic_run(Path(tmp), "parallel")

            run_crd_density(root / "protocol.toml", api_client=MockLLMClient())
            build_crd_comparison(
                density_matrix=root / "reports" / "crd" / "density_matrix.csv",
                classified_hits=root / "reports" / "crd" / "classified_hits.csv",
                manifest=root / "reports" / "crd" / "manifest.json",
                out_dir=root / "reports" / "crd",
                markdown_out=root / "CRD_REPORT.md",
            )
            rows = read_csv(root / "reports" / "crd" / "density_matrix.csv")
            agreement_rows = read_csv(root / "reports" / "crd" / "classifier_agreement_summary.csv")

        self.assertEqual({row["classifier_mode"] for row in rows}, {"deterministic", "llm"})
        self.assertTrue(all(row["agreement_rate"] for row in rows))
        self.assertEqual(rows[0]["agreement_rate"], "1")
        self.assertGreater(len(agreement_rows), 0)


def build_synthetic_run(root: Path, mode: str) -> Path:
    (root / "reports" / "crd").mkdir(parents=True)
    source = root / "source.txt"
    source.write_text("abcde", encoding="utf-8")
    config = root / "corpus.toml"
    config.write_text(
        "\n".join(
            [
                'name = "synthetic"',
                'language = "english"',
                "",
                "[[sources]]",
                'name = "synthetic"',
                'format = "text"',
                f'path = "{source}"',
                'ref = "Test 1:1"',
                'book = "Test"',
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    terms = root / "terms.csv"
    terms.write_text(
        "term_id,concept,category,language,term,notes\nterm,Example,example,english,ace,test\n",
        encoding="utf-8",
    )
    dictionary = root / "dictionary.toml"
    dictionary.write_text(
        "\n".join(
            [
                "[metadata]",
                'schema_version = "1"',
                'locked_by = "test"',
                'locked_at = "2026-01-01"',
                'sha256 = "template"',
                'drafted_with = "human"',
                "",
                "[[entries]]",
                'term_id = "term"',
                'surface_keywords = ["abcde"]',
                'concept_codes = ["example"]',
                'verse_refs = []',
                "",
                "[entries.provenance]",
                'author = "test"',
                'lock_date = "2026-01-01"',
                'reviewer = "test"',
                'notes = "test"',
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    system = root / "system.md"
    user = root / "user.md"
    system.write_text("Return JSON.\n", encoding="utf-8")
    user.write_text(
        "Term: {term}\nLanguage: {language}\nRef: {center_verse_ref}\n{center_verse_text}\n{span_text}\n",
        encoding="utf-8",
    )
    prereg = root / "CRD_PREREGISTRATION.md"
    prereg.write_text(prereg_text(), encoding="utf-8")
    protocol = root / "protocol.toml"
    protocol.write_text(
        "\n".join(
            [
                'name = "synthetic_crd"',
                f'term_file = "{terms}"',
                f'relevance_dictionary = "{dictionary}"',
                f'relevance_dictionary_sha256 = "{sha256_file(dictionary)}"',
                'skip_range = "2..2"',
                'direction = "forward"',
                'min_term_length = 3',
                'max_hits_per_term = 10',
                f'classifier_mode = "{mode}"',
                'llm_model = "mock"',
                'llm_model_version = "mock-v1"',
                'llm_provider = "mock"',
                f'system_prompt_path = "{system}"',
                f'system_prompt_sha256 = "{sha256_file(system)}"',
                f'user_prompt_template_path = "{user}"',
                f'user_prompt_template_sha256 = "{sha256_file(user)}"',
                'llm_temperature = 0',
                'llm_max_tokens = 100',
                'max_api_calls = 10',
                'max_estimated_cost_usd = 1',
                'estimated_cost_per_call_usd = 0',
                f'output_dir = "{root / "reports" / "crd"}"',
                f'preregistration_doc = "{prereg}"',
                f'preregistration_sha256 = "{sha256_file(prereg)}"',
                "",
                "[[corpus_list]]",
                'label = "SYN"',
                f'config = "{config}"',
                'corpus_class = "bible"',
                'language = "english"',
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return root


def prereg_text() -> str:
    sections = [
        "# CRD Preregistration",
        "## Hypothesis\nTest hypothesis.",
        "## Term List Path\nterms.csv",
        "## Relevance Dictionary Path And Hash\ndictionary.toml",
        "## Classifier Mode And Locked Parameters\nlocked",
        "## Corpora\nsynthetic",
        "## Skip Range\n2..2",
        "## Direction\nforward",
        "## Decision Rule\none hit",
        "## Multiple Comparisons Correction\nBenjamini-Hochberg q <= 0.05",
        "## Lock Date\n2026-01-01",
        "## Locked By\ntest",
        "## Reviewers\ntest",
        "## Locked Hash\ntest",
        "## Sample Audit Log Review\nreviewed",
    ]
    return "\n\n".join(sections) + "\n"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    unittest.main()
