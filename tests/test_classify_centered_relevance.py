import json
import tempfile
import unittest
from pathlib import Path

from scripts.classify_centered_relevance import (
    CRDBudgetExceeded,
    CRDConfigurationError,
    DeterministicClassifier,
    LLMClassifier,
    load_relevance_dictionary,
    parse_relevance_entry,
    sha256_file,
)


class MockLLMClient:
    def __init__(self, raw_response: str | None = None):
        self.raw_response = raw_response or json.dumps(
            {
                "is_relevant": True,
                "relevance_type": "llm_judged_relevant",
                "rationale": "direct match",
            }
        )
        self.calls = 0

    def classify(self, **kwargs):
        self.calls += 1
        return {
            "raw_response": self.raw_response,
            "model_version": "mock-v1",
        }


class DeterministicClassifierTests(unittest.TestCase):
    def test_surface_keyword_present(self) -> None:
        classifier = DeterministicClassifier(entries={"term": entry(surface_keywords=["מלך"])})

        result = classifier.classify(
            {
                "term_id": "term",
                "language": "hebrew",
                "center_word": "מֶלֶךְ",
                "center_verse_text": "מֶלֶךְ",
                "span_text": "",
            },
            {"term_id": "term"},
        )

        self.assertTrue(result.is_relevant)
        self.assertEqual(result.relevance_type, "surface_keyword_match")
        self.assertEqual(result.audit_payload["surface_match_scope"], "center_word")
        self.assertEqual(result.audit_payload["matched_normalized_surface_keyword"], "מלכ")

    def test_surface_keyword_match_reports_center_verse_scope(self) -> None:
        classifier = DeterministicClassifier(entries={"term": entry(surface_keywords=["king"])})

        result = classifier.classify(
            {
                "term_id": "term",
                "language": "english",
                "center_word": "servant",
                "center_verse_text": "the king spoke",
                "span_text": "",
            },
            {"term_id": "term"},
        )

        self.assertTrue(result.is_relevant)
        self.assertEqual(result.audit_payload["surface_match_scope"], "center_verse")
        self.assertEqual(result.audit_payload["matched_surface_keyword"], "king")

    def test_surface_keyword_in_verse_requires_exact_token(self) -> None:
        classifier = DeterministicClassifier(entries={"term": entry(surface_keywords=["דב"])})

        absent = classifier.classify(
            {
                "term_id": "term",
                "language": "hebrew",
                "center_word": "תַּחְתָּ֜יו",
                "center_verse_text": "תַּחְתָּ֜יו",
                "span_text": "",
            },
            {"term_id": "term"},
        )
        present = classifier.classify(
            {
                "term_id": "term",
                "language": "hebrew",
                "center_word": "וַיֹּאמֶר",
                "center_verse_text": "וַיֹּאמֶר דב",
                "span_text": "",
            },
            {"term_id": "term"},
        )

        self.assertFalse(absent.is_relevant)
        self.assertTrue(present.is_relevant)
        self.assertEqual(present.audit_payload["surface_match_scope"], "center_verse")

    def test_surface_keyword_phrase_requires_contiguous_tokens(self) -> None:
        classifier = DeterministicClassifier(entries={"term": entry(surface_keywords=["בית יהוה"])})

        present = classifier.classify(
            {
                "term_id": "term",
                "language": "hebrew",
                "center_word": "בית",
                "center_verse_text": "אל בית יהוה",
                "span_text": "",
            },
            {"term_id": "term"},
        )
        absent = classifier.classify(
            {
                "term_id": "term",
                "language": "hebrew",
                "center_word": "בית",
                "center_verse_text": "בית גדול יהוה",
                "span_text": "",
            },
            {"term_id": "term"},
        )

        self.assertTrue(present.is_relevant)
        self.assertFalse(absent.is_relevant)

    def test_surface_keyword_absent(self) -> None:
        classifier = DeterministicClassifier(entries={"term": entry(surface_keywords=["מלך"])})

        result = classifier.classify(
            {
                "term_id": "term",
                "language": "hebrew",
                "center_word": "כהן",
                "center_verse_text": "כהן",
                "span_text": "",
            },
            {"term_id": "term"},
        )

        self.assertFalse(result.is_relevant)
        self.assertEqual(result.relevance_type, "none")

    def test_book_scope_does_not_block_surface_keyword_match(self) -> None:
        classifier = DeterministicClassifier(
            entries={"term": entry(surface_keywords=["מלך"], book_scope=["Dan"])}
        )

        result = classifier.classify(
            {
                "term_id": "term",
                "language": "hebrew",
                "center_ref": "PBY Bialik",
                "center_word": "מֶלֶךְ",
                "center_verse_text": "מֶלֶךְ",
                "span_text": "",
            },
            {"term_id": "term"},
        )

        self.assertTrue(result.is_relevant)
        self.assertEqual(result.relevance_type, "surface_keyword_match")

    def test_book_scope_reports_no_match_reason_without_hard_filtering(self) -> None:
        classifier = DeterministicClassifier(
            entries={"term": entry(surface_keywords=["מלך"], book_scope=["Dan"])}
        )

        result = classifier.classify(
            {
                "term_id": "term",
                "language": "hebrew",
                "center_ref": "PBY Bialik",
                "center_word": "כהן",
                "center_verse_text": "כהן",
                "span_text": "",
            },
            {"term_id": "term"},
        )

        self.assertFalse(result.is_relevant)
        self.assertEqual(result.audit_payload["reason"], "outside_book_scope_no_match")

    def test_verse_ref_match(self) -> None:
        classifier = DeterministicClassifier(entries={"term": entry(verse_refs=["Gen 1:1"])})

        result = classifier.classify(
            {"term_id": "term", "language": "english", "center_ref": "Gen 1:1"},
            {"term_id": "term"},
        )

        self.assertTrue(result.is_relevant)
        self.assertEqual(result.relevance_type, "verse_ref_match")

    def test_verse_ref_absent(self) -> None:
        classifier = DeterministicClassifier(entries={"term": entry(verse_refs=["Gen 1:1"])})

        result = classifier.classify(
            {"term_id": "term", "language": "english", "center_ref": "Exod 1:1"},
            {"term_id": "term"},
        )

        self.assertFalse(result.is_relevant)

    def test_concept_match_uses_explicit_surface_codes_only(self) -> None:
        classifier = DeterministicClassifier(entries={"term": entry(concept_codes=["gog"])})

        hidden_term_only = classifier.classify(
            {"term_id": "term", "language": "hebrew"},
            {"term_id": "term", "concept": "Gog", "category": "target_pair"},
        )
        explicit_surface_code = classifier.classify(
            {"term_id": "term", "language": "hebrew", "surface_concept_codes": "gog;magog"},
            {"term_id": "term", "concept": "Gog", "category": "target_pair"},
        )

        self.assertFalse(hidden_term_only.is_relevant)
        self.assertTrue(explicit_surface_code.is_relevant)
        self.assertEqual(explicit_surface_code.relevance_type, "concept_match")

    def test_normalization_edge_cases(self) -> None:
        classifier = DeterministicClassifier(
            entries={
                "hebrew": entry(term_id="hebrew", surface_keywords=["מלך"]),
                "greek": entry(term_id="greek", surface_keywords=["λογος"]),
                "english": entry(term_id="english", surface_keywords=["king"]),
            }
        )

        self.assertTrue(
            classifier.classify(
                {
                    "term_id": "hebrew",
                    "language": "hebrew",
                    "center_word": "מֶלֶךְ",
                    "center_verse_text": "",
                    "span_text": "",
                },
                {"term_id": "hebrew"},
            ).is_relevant
        )
        self.assertTrue(
            classifier.classify(
                {
                    "term_id": "greek",
                    "language": "greek",
                    "center_word": "λόγος",
                    "center_verse_text": "",
                    "span_text": "",
                },
                {"term_id": "greek"},
            ).is_relevant
        )
        self.assertTrue(
            classifier.classify(
                {
                    "term_id": "english",
                    "language": "english",
                    "center_word": "KING",
                    "center_verse_text": "",
                    "span_text": "",
                },
                {"term_id": "english"},
            ).is_relevant
        )

    def test_missing_required_dictionary_fields_raise(self) -> None:
        with self.assertRaises(CRDConfigurationError):
            parse_relevance_entry({"term_id": "bad"})

    def test_dictionary_list_fields_must_be_lists(self) -> None:
        base = {
            "term_id": "bad",
            "surface_keywords": [],
            "concept_codes": [],
            "verse_refs": [],
            "book_scope": [],
            "provenance": {
                "author": "test",
                "lock_date": "2026-01-01",
                "reviewer": "test",
                "notes": "test",
            },
        }
        for field in ("surface_keywords", "concept_codes", "verse_refs", "book_scope"):
            with self.subTest(field=field):
                row = dict(base)
                row[field] = "bad"
                with self.assertRaisesRegex(CRDConfigurationError, f"{field} must be a list"):
                    parse_relevance_entry(row)

    def test_dictionary_entries_must_be_list(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dictionary = Path(tmp) / "dictionary.toml"
            dictionary.write_text('entries = "bad"\n', encoding="utf-8")

            with self.assertRaisesRegex(CRDConfigurationError, "entries must be a list"):
                load_relevance_dictionary(dictionary)

    def test_dictionary_entry_must_be_table(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dictionary = Path(tmp) / "dictionary.toml"
            dictionary.write_text('entries = ["bad"]\n', encoding="utf-8")

            with self.assertRaisesRegex(
                CRDConfigurationError,
                "relevance dictionary entry 1 must be a table",
            ):
                load_relevance_dictionary(dictionary)


class LLMClassifierTests(unittest.TestCase):
    def test_cache_hit_reuses_prior_response(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            classifier, client = build_llm_classifier(Path(tmp))
            hit_row = llm_hit_row()

            first = classifier.classify(hit_row, {"term": "ace", "language": "english"})
            second = classifier.classify(hit_row, {"term": "ace", "language": "english"})

        self.assertTrue(first.is_relevant)
        self.assertTrue(second.is_relevant)
        self.assertEqual(client.calls, 1)

    def test_cache_miss_calls_api(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            classifier, client = build_llm_classifier(Path(tmp))

            result = classifier.classify(llm_hit_row(), {"term": "ace", "language": "english"})

        self.assertTrue(result.is_relevant)
        self.assertEqual(client.calls, 1)

    def test_malformed_api_response_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            classifier, _ = build_llm_classifier(Path(tmp), client=MockLLMClient("not-json"))

            with self.assertRaises(ValueError):
                classifier.classify(llm_hit_row(), {"term": "ace", "language": "english"})

    def test_prompt_hash_mismatch_refuses_to_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            system, user = write_prompts(root)

            with self.assertRaises(CRDConfigurationError):
                LLMClassifier(
                    model_id="mock",
                    model_version="mock-v1",
                    system_prompt_path=system,
                    user_prompt_template_path=user,
                    expected_system_prompt_sha256="bad",
                    expected_user_prompt_template_sha256=sha256_file(user),
                    temperature=0,
                    max_tokens=100,
                    provider="mock",
                    cache_dir=root / "cache",
                    audit_log_path=root / "audit.jsonl",
                    max_api_calls=1,
                    max_estimated_cost_usd=1,
                    api_client=MockLLMClient(),
                )

    def test_budget_exceeded_aborts_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            classifier, _ = build_llm_classifier(Path(tmp), max_api_calls=0)

            with self.assertRaises(CRDBudgetExceeded):
                classifier.classify(llm_hit_row(), {"term": "ace", "language": "english"})


def entry(
    *,
    term_id: str = "term",
    surface_keywords: list[str] | None = None,
    concept_codes: list[str] | None = None,
    verse_refs: list[str] | None = None,
    book_scope: list[str] | None = None,
):
    return parse_relevance_entry(
        {
            "term_id": term_id,
            "surface_keywords": surface_keywords or [],
            "concept_codes": concept_codes or [],
            "verse_refs": verse_refs or [],
            "book_scope": book_scope or [],
            "provenance": {
                "author": "test",
                "lock_date": "2026-01-01",
                "reviewer": "test",
                "notes": "test",
            },
        }
    )


def write_prompts(root: Path) -> tuple[Path, Path]:
    system = root / "system.md"
    user = root / "user.md"
    system.write_text("Return strict JSON.\n", encoding="utf-8")
    user.write_text(
        "Term: {term}\nLanguage: {language}\nRef: {center_verse_ref}\n{center_verse_text}\n{span_text}\n",
        encoding="utf-8",
    )
    return system, user


def build_llm_classifier(
    root: Path,
    *,
    client: MockLLMClient | None = None,
    max_api_calls: int = 2,
) -> tuple[LLMClassifier, MockLLMClient]:
    system, user = write_prompts(root)
    mock = client or MockLLMClient()
    return (
        LLMClassifier(
            model_id="mock",
            model_version="mock-v1",
            system_prompt_path=system,
            user_prompt_template_path=user,
            expected_system_prompt_sha256=sha256_file(system),
            expected_user_prompt_template_sha256=sha256_file(user),
            temperature=0,
            max_tokens=100,
            provider="mock",
            cache_dir=root / "cache",
            audit_log_path=root / "audit.jsonl",
            max_api_calls=max_api_calls,
            max_estimated_cost_usd=1,
            api_client=mock,
        ),
        mock,
    )


def llm_hit_row() -> dict[str, str]:
    return {
        "term_id": "term",
        "term": "ace",
        "language": "english",
        "center_ref": "Test 1:1",
        "center_verse_text": "abcde",
        "span_text": "abcde",
    }


if __name__ == "__main__":
    unittest.main()
