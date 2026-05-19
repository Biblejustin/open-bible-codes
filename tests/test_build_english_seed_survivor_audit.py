import argparse
import tempfile
import unittest
from pathlib import Path

from scripts.build_english_seed_survivor_audit import (
    survivor_context_hits,
    survivor_term_rows,
    write_markdown,
)


class EnglishSeedSurvivorAuditTests(unittest.TestCase):
    def test_empty_survivor_inputs_are_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            term_shuffle = root / "term_shuffle.csv"
            term_shuffle.write_text(
                "corpus,term_id,observed_hits,term_q_value\n",
                encoding="utf-8",
            )
            context_hits = root / "context_hits.csv"
            context_hits.write_text("corpus,term_id\nERV,eng_demo\n", encoding="utf-8")

            self.assertEqual(survivor_term_rows(term_shuffle, max_q=0.05), {})
            self.assertEqual(survivor_context_hits(context_hits, {}), [])

    def test_empty_markdown_reports_no_current_survivors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            out = Path(tmp_dir) / "audit.md"
            args = argparse.Namespace(
                context_hits="context_hits.csv",
                triage="triage.csv",
                corpus_shuffle="corpus_shuffle.csv",
                term_shuffle="term_shuffle.csv",
                max_term_q=0.05,
            )

            write_markdown(out, [], [], [], args)

            text = out.read_text(encoding="utf-8")
            self.assertIn("Status: no current survivor rows.", text)
            self.assertIn("survivor hit rows: 0", text)


if __name__ == "__main__":
    unittest.main()
