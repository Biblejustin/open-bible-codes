import csv
import tempfile
import textwrap
import unittest
from pathlib import Path

from scripts.audit_apocrypha_coverage import audit_config, main


class ApocryphaCoverageTests(unittest.TestCase):
    def test_audit_config_counts_deuterocanon_books(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / "data.csv"
            data.write_text(
                "ref,book,chapter,verse,text\n"
                "TOB 1:1,TOB,1,1,λογος\n"
                "GEN 1:1,GEN,1,1,αρχη\n",
                encoding="utf-8",
            )
            config = root / "corpus.toml"
            config.write_text(
                textwrap.dedent(
                    f"""
                    name = "demo"
                    language = "greek"

                    [[sources]]
                    name = "demo"
                    format = "csv"
                    path = "{data.name}"
                    text_column = "text"
                    ref_column = "ref"
                    book_column = "book"
                    chapter_column = "chapter"
                    verse_column = "verse"
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            rows, total = audit_config("DEMO", config)
            by_book = {row["book"]: row for row in rows}

            self.assertEqual(by_book["TOB"]["present"], "yes")
            self.assertEqual(by_book["TOB"]["verses"], 1)
            self.assertNotIn("GEN", by_book)
            self.assertEqual(total["present_books"], 1)

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / "data.csv"
            data.write_text(
                "ref,book,chapter,verse,text\nTOB 1:1,TOB,1,1,λογος\n",
                encoding="utf-8",
            )
            config = root / "corpus.toml"
            config.write_text(
                textwrap.dedent(
                    f"""
                    name = "demo"
                    language = "greek"

                    [[sources]]
                    name = "demo"
                    format = "csv"
                    path = "{data.name}"
                    text_column = "text"
                    ref_column = "ref"
                    book_column = "book"
                    chapter_column = "chapter"
                    verse_column = "verse"
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )
            out = root / "coverage.csv"
            markdown = root / "coverage.md"
            manifest = root / "manifest.json"

            code = main(
                [
                    "--corpus",
                    f"DEMO={config}",
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
            self.assertTrue(any(row["book"] == "TOB" and row["present"] == "yes" for row in rows))
            markdown_text = markdown.read_text(encoding="utf-8")
            self.assertIn("Apocrypha Source Coverage", markdown_text)
            self.assertIn("completed apocrypha/deuterocanon", markdown_text)
            self.assertNotIn("planned apocrypha/deuterocanon", markdown_text)
            self.assertIn("audit_apocrypha_coverage", manifest.read_text(encoding="utf-8"))

    def test_main_renders_dynamic_corpus_columns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / "data.csv"
            data.write_text(
                "ref,book,chapter,verse,text\nTOB 1:1,TOB,1,1,word\n",
                encoding="utf-8",
            )
            config = root / "corpus.toml"
            config.write_text(
                textwrap.dedent(
                    f"""
                    name = "demo"
                    language = "english"

                    [[sources]]
                    name = "demo"
                    format = "csv"
                    path = "{data.name}"
                    text_column = "text"
                    ref_column = "ref"
                    book_column = "book"
                    chapter_column = "chapter"
                    verse_column = "verse"
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )
            markdown = root / "coverage.md"

            code = main(
                [
                    "--corpus",
                    f"A={config}",
                    "--corpus",
                    f"B={config}",
                    "--out",
                    str(root / "coverage.csv"),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(root / "manifest.json"),
                ]
            )

            self.assertEqual(code, 0)
            self.assertIn("| Book | Name | A | B |", markdown.read_text(encoding="utf-8"))
