import json
import tempfile
import time
import unittest
from pathlib import Path

import pytest

from els.report_db import default_table_name, import_csv_table
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
            first_markdown_mtime_ns = markdown.stat().st_mtime_ns
            first_json_mtime_ns = index_json.stat().st_mtime_ns
            time.sleep(0.01)
            write_markdown_index(entries, markdown, reports_root=root)
            write_json_index(entries, index_json)
            payload = json.loads(index_json.read_text(encoding="utf-8"))
            markdown_text = markdown.read_text(encoding="utf-8")
            second_markdown_mtime_ns = markdown.stat().st_mtime_ns
            second_json_mtime_ns = index_json.stat().st_mtime_ns

        csv_entry = next(entry for entry in entries if entry.kind == "csv")
        json_entry = next(entry for entry in entries if entry.kind == "json")
        self.assertEqual(csv_entry.rows, 2)
        self.assertEqual(csv_entry.columns, ("term", "count"))
        self.assertEqual(json_entry.label, "sample")
        self.assertEqual(payload["reports"][0]["path"], "a.csv")
        self.assertIn("Report Index", markdown_text)
        self.assertEqual(second_markdown_mtime_ns, first_markdown_mtime_ns)
        self.assertEqual(second_json_mtime_ns, first_json_mtime_ns)

    def test_scan_reports_skips_operational_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "real.csv").write_text("term,count\nθεος,7\n", encoding="utf-8")
            (root / "index.json").write_text("{}", encoding="utf-8")
            (root / "INDEX.md").write_text("# stale\n", encoding="utf-8")
            (root / "protocol_run.manifest.json").write_text("{}", encoding="utf-8")
            stamp_dir = root / "protocols" / "sample" / ".step-stamps"
            stamp_dir.mkdir(parents=True)
            (stamp_dir / "one.json").write_text("{}", encoding="utf-8")
            benchmark_dir = root / "benchmarks"
            benchmark_dir.mkdir()
            (benchmark_dir / "sample_benchmark.json").write_text("{}", encoding="utf-8")
            partition_dir = root / "dynamic_skip_focus" / "partitions"
            partition_dir.mkdir(parents=True)
            (partition_dir / "part.manifest.json").write_text("{}", encoding="utf-8")
            worker_dir = root / "dynamic_skip_focus" / "worker_batches"
            worker_dir.mkdir()
            (worker_dir / "worker.json").write_text("{}", encoding="utf-8")

            entries = scan_reports(root)

        self.assertEqual([entry.path for entry in entries], ["real.csv"])

    def test_scan_reports_uses_duckdb_row_count_when_current(self) -> None:
        pytest.importorskip("duckdb")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            csv_path = root / "a.csv"
            db = root / "db" / "open_bible_codes.duckdb"
            csv_path.write_text("term,count\nθεος,7\nκυριος,3\n", encoding="utf-8")
            import_csv_table(db_path=db, csv_path=csv_path, table_name=default_table_name(csv_path))

            entries = scan_reports(root, db_path=db)

        csv_entry = next(entry for entry in entries if entry.kind == "csv")
        self.assertEqual(csv_entry.rows, 2)
        self.assertEqual(csv_entry.sample_rows[0]["term"], "θεος")


if __name__ == "__main__":
    unittest.main()
