import tempfile
import unittest
from pathlib import Path

from scripts import check_kjva_source_candidate_status_doc as checker


class KJVASourceCandidateStatusDocTests(unittest.TestCase):
    def test_current_doc_passes(self) -> None:
        self.assertEqual(checker.validate_kjva_source_candidate_status_doc(), [])

    def test_missing_required_phrase_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            doc = Path(tmp) / "status.md"
            linked = Path(tmp) / "linked.md"
            linked.write_text("linked\n", encoding="utf-8")
            text = checker.DEFAULT_DOC.read_text(encoding="utf-8").replace(
                "Ready independent KJVA replication sources: 0.",
                "Ready independent KJVA replication sources: unknown.",
            )
            doc.write_text(text, encoding="utf-8")

            failures = checker.validate_kjva_source_candidate_status_doc(
                doc,
                linked_docs=(linked,),
            )

        self.assertTrue(
            any("Ready independent KJVA replication sources: 0." in failure for failure in failures)
        )

    def test_overclaim_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            doc = Path(tmp) / "status.md"
            linked = Path(tmp) / "linked.md"
            linked.write_text("linked\n", encoding="utf-8")
            text = checker.DEFAULT_DOC.read_text(encoding="utf-8")
            doc.write_text(
                text + "\nResult-bearing replication is ready.\n",
                encoding="utf-8",
            )

            failures = checker.validate_kjva_source_candidate_status_doc(
                doc,
                linked_docs=(linked,),
            )

        self.assertTrue(any("overclaim phrase" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
