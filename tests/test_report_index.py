import json
import tempfile
import unittest
from pathlib import Path

from els.report_index import scan_reports, write_json_index, write_markdown_index


class ReportIndexTests(unittest.TestCase):
    def test_scan_reports_summarizes_csv_and_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.csv").write_text("term,count\nθεος,7\nκυριος,3\n", encoding="utf-8")
            (root / "a.manifest.json").write_text(
                json.dumps({"tool": "sample", "rows": 2}),
                encoding="utf-8",
            )

            entries = scan_reports(root)
            markdown = root / "INDEX.md"
            index_json = root / "index.json"
            write_markdown_index(entries, markdown, reports_root=root)
            write_json_index(entries, index_json)
            payload = json.loads(index_json.read_text(encoding="utf-8"))
            markdown_text = markdown.read_text(encoding="utf-8")

        csv_entry = next(entry for entry in entries if entry.kind == "csv")
        json_entry = next(entry for entry in entries if entry.kind == "json")
        self.assertEqual(csv_entry.rows, 2)
        self.assertEqual(csv_entry.columns, ("term", "count"))
        self.assertEqual(json_entry.label, "sample")
        self.assertEqual(payload["reports"][0]["path"], "a.csv")
        self.assertIn("Report Index", markdown_text)

    def test_scan_reports_skips_operational_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "real.csv").write_text("term,count\nθεος,7\n", encoding="utf-8")
            (root / "index.json").write_text("{}", encoding="utf-8")
            (root / "INDEX.md").write_text("# stale\n", encoding="utf-8")
            stamp_dir = root / "protocols" / "sample" / ".step-stamps"
            stamp_dir.mkdir(parents=True)
            (stamp_dir / "one.json").write_text("{}", encoding="utf-8")
            benchmark_dir = root / "benchmarks"
            benchmark_dir.mkdir()
            (benchmark_dir / "sample_benchmark.json").write_text("{}", encoding="utf-8")

            entries = scan_reports(root)

        self.assertEqual([entry.path for entry in entries], ["real.csv"])


if __name__ == "__main__":
    unittest.main()
