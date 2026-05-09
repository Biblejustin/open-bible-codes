import argparse
import tempfile
import unittest
from pathlib import Path

from scripts.run_dynamic_span_partitions import (
    archive_marker_path,
    command_for_partition,
    read_partition_id_file,
    run_partitions,
    select_partition_rows,
)


class DynamicSpanPartitionRunnerTests(unittest.TestCase):
    def test_select_partition_rows_filters_and_limits(self) -> None:
        rows = [
            partition_row("a", "TR_NT", "dyn_a", 1, 10, 20),
            partition_row("b", "TR_NT", "dyn_a", 2, 10, 30),
            partition_row("c", "LXX", "dyn_a", 1, 10, 10),
            partition_row("d", "TR_NT", "dyn_b", 1, 10, 10),
        ]
        args = argparse.Namespace(
            partition_id=[],
            term_id=["dyn_a"],
            corpus_label=["TR_NT"],
            min_partition_index=2,
            max_partition_index=None,
            partition_count=None,
            max_estimated_hits=40,
            bible_only=False,
            controls_only=False,
            limit=1,
        )

        selected = select_partition_rows(rows, args)

        self.assertEqual([row["partition_id"] for row in selected], ["b"])

    def test_select_partition_rows_supports_bible_only_and_partition_count(self) -> None:
        rows = [
            partition_row("a", "TR_NT", "dyn_a", 1, 1, 20),
            partition_row("b", "TR_NT", "dyn_a", 1, 2, 20),
            partition_row("c", "GRC_PERSEUS_ILIAD", "dyn_a", 1, 1, 20),
        ]
        args = argparse.Namespace(
            partition_id=[],
            term_id=[],
            corpus_label=[],
            min_partition_index=None,
            max_partition_index=None,
            partition_count=1,
            max_estimated_hits=None,
            bible_only=True,
            controls_only=False,
            limit=None,
        )

        selected = select_partition_rows(rows, args)

        self.assertEqual([row["partition_id"] for row in selected], ["a"])

    def test_select_partition_rows_supports_controls_only(self) -> None:
        rows = [
            partition_row("a", "TR_NT", "dyn_a", 1, 1, 20),
            partition_row("b", "GRC_PERSEUS_ILIAD", "dyn_a", 1, 1, 20),
            partition_row("c", "ENG_PG_SHAKESPEARE", "dyn_a", 1, 1, 20),
        ]
        args = argparse.Namespace(
            partition_id=[],
            term_id=[],
            corpus_label=[],
            min_partition_index=None,
            max_partition_index=None,
            partition_count=1,
            max_estimated_hits=None,
            bible_only=False,
            controls_only=True,
            limit=None,
        )

        selected = select_partition_rows(rows, args)

        self.assertEqual([row["partition_id"] for row in selected], ["c", "b"])

    def test_select_partition_rows_reads_partition_id_file(self) -> None:
        rows = [
            partition_row("a", "TR_NT", "dyn_a", 1, 1, 20),
            partition_row("b", "TR_NT", "dyn_a", 2, 1, 20),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "assignment.csv"
            path.write_text("partition_id\nb\n", encoding="utf-8")
            args = argparse.Namespace(
                partition_id=[],
                partition_id_file=[path],
                term_id=[],
                corpus_label=[],
                min_partition_index=None,
                max_partition_index=None,
                partition_count=None,
                max_estimated_hits=None,
                bible_only=False,
                controls_only=False,
                limit=None,
            )

            selected = select_partition_rows(rows, args)

        self.assertEqual([row["partition_id"] for row in selected], ["b"])

    def test_read_partition_id_file_accepts_plain_list(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ids.txt"
            path.write_text("# comment\na\n\nb\n", encoding="utf-8")

            self.assertEqual(read_partition_id_file(path), {"a", "b"})

    def test_select_partition_rows_rejects_conflicting_corpus_groups(self) -> None:
        args = argparse.Namespace(
            partition_id=[],
            term_id=[],
            corpus_label=[],
            min_partition_index=None,
            max_partition_index=None,
            partition_count=None,
            max_estimated_hits=None,
            bible_only=True,
            controls_only=True,
            limit=None,
        )

        with self.assertRaisesRegex(ValueError, "bible-only"):
            select_partition_rows([partition_row("a", "TR_NT", "dyn_a", 1, 1, 20)], args)

    def test_command_for_partition_uses_structured_fields(self) -> None:
        row = partition_row("a", "TR_NT", "dyn_a", 1, 10, 20)

        command = command_for_partition(row)

        self.assertEqual(command[1:3], ["-m", "scripts.export_dynamic_span_hits"])
        self.assertIn("--include-dense", command)
        self.assertIn("--max-export-hits", command)
        self.assertIn("0", command)
        self.assertIn("--min-abs-skip", command)
        self.assertIn("2", command)
        self.assertIn("--max-abs-skip", command)
        self.assertIn("9", command)
        self.assertIn("--counts", command)
        self.assertIn("reports/dynamic_skip_focus/sample.csv", command)

    def test_run_partitions_dry_run_writes_status_without_execution(self) -> None:
        args = argparse.Namespace(dry_run=True, rerun=False)

        statuses = run_partitions([partition_row("a", "TR_NT", "dyn_a", 1, 10, 20)], args)

        self.assertEqual(len(statuses), 1)
        self.assertEqual(statuses[0]["status"], "dry_run")
        self.assertEqual(statuses[0]["returncode"], "0")
        self.assertIn("scripts.export_dynamic_span_hits", statuses[0]["command"])

    def test_run_partitions_skips_existing_compressed_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / "partition.csv"
            manifest = root / "partition.manifest.json"
            out.with_suffix(out.suffix + ".gz").write_text("compressed\n", encoding="utf-8")
            manifest.write_text("{}\n", encoding="utf-8")
            row = partition_row("a", "TR_NT", "dyn_a", 1, 10, 20)
            row["out"] = str(out)
            row["manifest_out"] = str(manifest)
            args = argparse.Namespace(dry_run=False, rerun=False)

            statuses = run_partitions([row], args)

        self.assertEqual(statuses[0]["status"], "skipped_existing")
        self.assertEqual(statuses[0]["returncode"], "0")

    def test_run_partitions_skips_archived_output_marker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / "partition.csv"
            manifest = root / "partition.manifest.json"
            row = partition_row("a", "TR_NT", "dyn_a", 1, 10, 20)
            row["out"] = str(out)
            row["manifest_out"] = str(manifest)
            archive_marker_path(row).write_text("{}\n", encoding="utf-8")
            manifest.write_text("{}\n", encoding="utf-8")
            args = argparse.Namespace(dry_run=False, rerun=False)

            statuses = run_partitions([row], args)

        self.assertEqual(statuses[0]["status"], "skipped_existing")
        self.assertEqual(statuses[0]["returncode"], "0")


def partition_row(
    partition_id: str,
    corpus: str,
    term_id: str,
    partition_index: int,
    partition_count: int,
    estimated_hits: int,
) -> dict[str, str]:
    return {
        "partition_id": partition_id,
        "corpus": corpus,
        "term_id": term_id,
        "mode": "full-span",
        "partition_index": str(partition_index),
        "partition_count": str(partition_count),
        "min_abs_skip": "2",
        "max_abs_skip": "9",
        "estimated_partition_hits": str(estimated_hits),
        "out": f"reports/dynamic_skip_focus/partitions/{partition_id}.csv",
        "summary_out": f"reports/dynamic_skip_focus/partitions/{partition_id}.md",
        "manifest_out": f"reports/dynamic_skip_focus/partitions/{partition_id}.manifest.json",
        "count_source_file": "reports/dynamic_skip_focus/sample.csv",
    }


if __name__ == "__main__":
    unittest.main()
