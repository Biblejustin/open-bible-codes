import tempfile
import unittest
from pathlib import Path

from els.project_index import (
    doc_category,
    scan_markdown_docs,
    scan_protocols,
    write_docs_index,
    write_protocol_index,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


class ProjectIndexTests(unittest.TestCase):
    def test_docs_index_groups_markdown_by_category(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "INDEX.md").write_text("# stale\n", encoding="utf-8")
            (root / "ALPHA_REPORT.md").write_text("# Alpha Report\n", encoding="utf-8")
            (root / "BETA_FINDINGS.md").write_text("# Beta Findings\n", encoding="utf-8")
            out = root / "INDEX.md"

            entries = scan_markdown_docs(root)
            write_docs_index(entries, out, docs_root=root)
            text = out.read_text(encoding="utf-8")

        self.assertEqual([entry.path for entry in entries], ["ALPHA_REPORT.md", "BETA_FINDINGS.md"])
        self.assertIn("Documents indexed: 2", text)
        self.assertIn("## Reports", text)
        self.assertIn("## Findings", text)
        self.assertIn("Alpha Report", text)

    def test_doc_category_prefers_preregistration_suffix(self) -> None:
        self.assertEqual(doc_category("GREEK_CONTROL_PREREGISTRATION.md"), "Preregistrations")

    def test_checked_in_docs_index_is_current(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "INDEX.md"
            docs_root = REPO_ROOT / "docs"

            write_docs_index(scan_markdown_docs(docs_root), out, docs_root=Path("docs"))

            self.assertEqual(
                out.read_text(encoding="utf-8"),
                (docs_root / "INDEX.md").read_text(encoding="utf-8"),
            )

    def test_protocol_index_extracts_terms_and_output_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "sample.toml").write_text(
                "\n".join(
                    [
                        'name = "sample_control"',
                        'description = "Demo control protocol."',
                        "",
                        "[[steps]]",
                        'id = "batch"',
                        'argv = ["-m", "els", "batch-many", "--term-set", "demo=terms/demo.csv"]',
                        'outputs = ["reports/protocols/sample/demo.csv", "reports/sample/out.csv", "reports/INDEX.md"]',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            out = root / "INDEX.md"

            entries = scan_protocols(root)
            write_protocol_index(entries, out, protocols_root=root)
            text = out.read_text(encoding="utf-8")

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].phase, "Controls")
        self.assertEqual(entries[0].term_paths, ("terms/demo.csv",))
        self.assertEqual(
            entries[0].output_roots,
            ("reports", "reports/protocols/sample", "reports/sample"),
        )
        self.assertIn("Protocols indexed: 1", text)
        self.assertIn("sample_control", text)

    def test_checked_in_protocol_index_is_current(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "INDEX.md"
            protocols_root = REPO_ROOT / "protocols"

            write_protocol_index(
                scan_protocols(protocols_root),
                out,
                protocols_root=Path("protocols"),
            )

            self.assertEqual(
                out.read_text(encoding="utf-8"),
                (protocols_root / "INDEX.md").read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
