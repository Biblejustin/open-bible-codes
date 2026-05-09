import gzip
import json
import tempfile
import unittest
from pathlib import Path

from scripts.archive_dynamic_span_partition_outputs import archive_candidates, archive_rows
from scripts.run_dynamic_span_partitions import archive_marker_path


class DynamicSpanPartitionArchiveTests(unittest.TestCase):
    def test_archive_rows_moves_compressed_output_and_leaves_marker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive_root = tmp_path / "archive"
            out = tmp_path / "reports/dynamic_skip_focus/partitions/p1.csv"
            gz_out = out.with_suffix(out.suffix + ".gz")
            manifest = tmp_path / "reports/dynamic_skip_focus/partitions/p1.manifest.json"
            gz_out.parent.mkdir(parents=True)
            with gzip.open(gz_out, "wt", encoding="utf-8") as handle:
                handle.write("header\n")
            manifest.write_text("{}\n", encoding="utf-8")
            row = plan_row("p1", out, manifest)

            self.assertEqual([item["partition_id"] for item in archive_candidates([row])], ["p1"])
            results = archive_rows([row], archive_root=archive_root, dry_run=False, min_free_gib=10_000)

            marker = archive_marker_path(row)
            self.assertEqual(results[0]["status"], "archived")
            self.assertFalse(gz_out.exists())
            self.assertTrue(marker.exists())
            marker_payload = json.loads(marker.read_text(encoding="utf-8"))
            archived_path = Path(marker_payload["archive_path"])
            self.assertTrue(archived_path.exists())
            with gzip.open(archived_path, "rt", encoding="utf-8") as handle:
                self.assertEqual(handle.read(), "header\n")


def plan_row(partition_id: str, out: Path, manifest: Path) -> dict[str, str]:
    return {
        "partition_id": partition_id,
        "corpus": "TR_NT",
        "term_id": "dyn_a",
        "mode": "full-span",
        "partition_index": "1",
        "partition_count": "1",
        "min_abs_skip": "2",
        "max_abs_skip": "9",
        "estimated_partition_hits": "1",
        "out": str(out),
        "manifest_out": str(manifest),
    }


if __name__ == "__main__":
    unittest.main()
