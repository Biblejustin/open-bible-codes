import csv
import tempfile
import unittest
from pathlib import Path

from scripts.audit_requested_term_expansion_coverage import (
    RequestedConcept,
    audit_requested_concepts,
    load_term_rows,
    main,
)


class RequestedTermExpansionCoverageTests(unittest.TestCase):
    def test_audit_marks_full_partial_and_missing_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            terms_dir = Path(tmp)
            write_terms(
                terms_dir / "demo.csv",
                [
                    ("babylon_h", "Babylon", "places", "hebrew", "בבל"),
                    ("babylon_g", "Babylon", "places", "greek", "βαβυλων"),
                    ("joshua_h", "Joshua", "names", "hebrew", "יהושע"),
                ],
            )

            rows = audit_requested_concepts(
                [
                    RequestedConcept("places", "Babylon", frozenset({"hebrew", "greek"})),
                    RequestedConcept("names", "Joshua", frozenset({"hebrew", "greek"})),
                    RequestedConcept("names", "Missing", frozenset({"hebrew"})),
                ],
                load_term_rows(terms_dir),
            )
            by_concept = {row["concept"]: row for row in rows}

            self.assertEqual(by_concept["Babylon"]["status"], "covered")
            self.assertEqual(by_concept["Joshua"]["status"], "partial")
            self.assertIn("missing languages: greek", by_concept["Joshua"]["notes"])
            self.assertEqual(by_concept["Missing"]["status"], "missing")

    def test_expected_spelling_matches_even_when_concept_name_differs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            terms_dir = Path(tmp)
            write_terms(
                terms_dir / "demo.csv",
                [("kapporet_h", "Kapporet", "temple", "hebrew", "כפרת")],
            )

            rows = audit_requested_concepts(
                [
                    RequestedConcept(
                        "temple",
                        "Mercy Seat",
                        frozenset({"hebrew"}),
                        (("hebrew", "כפרת"),),
                    )
                ],
                load_term_rows(terms_dir),
            )

            self.assertEqual(rows[0]["status"], "covered")
            self.assertIn("kapporet_h", rows[0]["matched_term_ids"])

    def test_main_writes_outputs_with_transliterated_markdown_terms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            terms_dir = root / "terms"
            terms_dir.mkdir()
            write_terms(
                terms_dir / "biblical_narrative_names.csv",
                [
                    ("joshua_h", "Joshua", "names", "hebrew", "יהושע"),
                    ("joshua_g", "Joshua", "names", "greek", "ιησους"),
                ],
            )
            out = root / "coverage.csv"
            markdown = root / "coverage.md"
            manifest = root / "manifest.json"

            code = main(
                [
                    "--terms-dir",
                    str(terms_dir),
                    "--out",
                    str(out),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(code, 0)
            with out.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertTrue(any(row["concept"] == "Joshua" and row["status"] == "covered" for row in rows))
            markdown_text = markdown.read_text(encoding="utf-8")
            self.assertIn("Requested Term Expansion Coverage", markdown_text)
            self.assertIn("Yehoshua", markdown_text)
            self.assertIn("Iesous", markdown_text)
            self.assertIn("audit_requested_term_expansion_coverage", manifest.read_text(encoding="utf-8"))


def write_terms(path: Path, rows: list[tuple[str, str, str, str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["term_id", "concept", "category", "language", "term", "notes"])
        for row in rows:
            writer.writerow([*row, ""])
