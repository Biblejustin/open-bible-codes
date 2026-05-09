import tempfile
import unittest
from pathlib import Path

from scripts.check_crd_relevance_dictionary import check_dictionary
from scripts.classify_centered_relevance import CRDConfigurationError, sha256_file
from scripts.apply_crd_relevance_review import main as apply_main
from scripts.scaffold_crd_relevance_dictionary import main as scaffold_main


class CRDDictionaryToolTests(unittest.TestCase):
    def test_scaffold_writes_blank_entries_and_queue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            terms = root / "terms.csv"
            terms.write_text(
                "term_id,concept,category,language,term,notes\n"
                "gog_h,Gog,target_pair,hebrew,גוג,test\n"
                "magog_h,Magog,target_pair,hebrew,מגוג,test\n",
                encoding="utf-8",
            )
            out = root / "dictionary.toml"
            queue = root / "queue.csv"

            exit_code = scaffold_main(["--term-file", str(terms), "--out", str(out), "--queue-out", str(queue)])

            dictionary_text = out.read_text(encoding="utf-8")
            queue_text = queue.read_text(encoding="utf-8")

        self.assertEqual(exit_code, 0)
        self.assertIn('term_id = "gog_h"', dictionary_text)
        self.assertIn("surface_keywords = []", dictionary_text)
        self.assertIn("surface_keywords_reviewed", queue_text)

    def test_check_dictionary_reports_missing_entries_without_review_requirement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            terms = write_terms(root)
            dictionary = write_dictionary(root, include_entry=False)

            report = check_dictionary(dictionary=dictionary, term_files=[terms])

        self.assertEqual(report["entries"], 0)
        self.assertEqual(report["missing_entries"], 1)

    def test_check_dictionary_requires_reviewed_criteria(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            terms = write_terms(root)
            dictionary = write_dictionary(root, include_entry=True, criteria=False)

            with self.assertRaises(CRDConfigurationError):
                check_dictionary(dictionary=dictionary, term_files=[terms], require_reviewed=True)

    def test_check_dictionary_accepts_reviewed_entry_with_expected_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            terms = write_terms(root)
            dictionary = write_dictionary(root, include_entry=True, criteria=True)

            report = check_dictionary(
                dictionary=dictionary,
                term_files=[terms],
                require_reviewed=True,
                expected_sha256=sha256_file(dictionary),
            )

        self.assertEqual(report["entries"], 1)
        self.assertEqual(report["missing_entries"], 0)

    def test_apply_review_queue_writes_reviewed_dictionary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            queue = root / "queue.csv"
            queue.write_text(
                "review_rank,source_file,term_id,concept,category,language,term,notes,"
                "surface_keywords_reviewed,concept_codes_reviewed,verse_refs_reviewed,"
                "book_scope_reviewed,reviewer,review_notes\n"
                "1,terms/demo.csv,gog_h,Gog,target_pair,hebrew,גוג,test,"
                "גוג;מגוג,gog;magog,Ezek 38:2;Ezek 39:1,Ezek,Justin,reviewed\n",
                encoding="utf-8",
            )
            out = root / "reviewed.toml"

            exit_code = apply_main(
                [
                    "--queue",
                    str(queue),
                    "--out",
                    str(out),
                    "--locked-by",
                    "Justin",
                    "--reviewer",
                    "Justin",
                    "--require-reviewer",
                ]
            )
            text = out.read_text(encoding="utf-8")

        self.assertEqual(exit_code, 0)
        self.assertIn('term_id = "gog_h"', text)
        self.assertIn('surface_keywords = ["גוג", "מגוג"]', text)
        self.assertIn('concept_codes = ["gog", "magog"]', text)
        self.assertIn('verse_refs = ["Ezek 38:2", "Ezek 39:1"]', text)
        self.assertIn('reviewer = "Justin"', text)

    def test_apply_review_queue_requires_reviewer_when_requested(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            queue = root / "queue.csv"
            queue.write_text(
                "review_rank,source_file,term_id,concept,category,language,term,notes,"
                "surface_keywords_reviewed,concept_codes_reviewed,verse_refs_reviewed,"
                "book_scope_reviewed,reviewer,review_notes\n"
                "1,terms/demo.csv,gog_h,Gog,target_pair,hebrew,גוג,test,גוג,gog,,, ,reviewed\n",
                encoding="utf-8",
            )
            out = root / "reviewed.toml"

            exit_code = apply_main(["--queue", str(queue), "--out", str(out), "--require-reviewer"])

        self.assertEqual(exit_code, 1)


def write_terms(root: Path) -> Path:
    terms = root / "terms.csv"
    terms.write_text(
        "term_id,concept,category,language,term,notes\nterm,Term,category,english,term,test\n",
        encoding="utf-8",
    )
    return terms


def write_dictionary(root: Path, *, include_entry: bool, criteria: bool = False) -> Path:
    dictionary = root / "dictionary.toml"
    lines = [
        "[metadata]",
        'schema_version = "1"',
        'locked_by = "reviewer"',
        'locked_at = "2026-05-09"',
        'sha256 = "locked-later"',
        'drafted_with = "human"',
        "",
    ]
    if include_entry:
        lines.extend(
            [
                "[[entries]]",
                'term_id = "term"',
                'surface_keywords = ["term"]' if criteria else "surface_keywords = []",
                "concept_codes = []",
                "verse_refs = []",
                "",
                "[entries.provenance]",
                'author = "reviewer"',
                'lock_date = "2026-05-09"',
                'reviewer = "Justin"',
                'notes = "reviewed"',
            ]
        )
    dictionary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return dictionary


if __name__ == "__main__":
    unittest.main()
