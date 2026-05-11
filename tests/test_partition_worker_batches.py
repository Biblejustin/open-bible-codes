import csv
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from scripts import export_partition_worker_bundle as export_bundle
from scripts import import_partition_worker_bundle as import_bundle
from scripts.plan_partition_worker_batches import (
    COUNT_FIELDNAMES,
    assign_rows,
    parse_worker_weights,
    select_remaining_rows,
    write_worker_files,
)


class PartitionWorkerBatchTests(unittest.TestCase):
    def test_select_remaining_rows_excludes_completed_and_filters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            completed = partition_row(root, "done", "TR_NT", "dyn_a", 1, 10, 20)
            Path(completed["out"]).write_text("x\n", encoding="utf-8")
            Path(completed["manifest_out"]).write_text("{}\n", encoding="utf-8")
            rows = [
                completed,
                partition_row(root, "keep", "TR_NT", "dyn_a", 2, 10, 20),
                partition_row(root, "too_big", "TR_NT", "dyn_a", 3, 10, 200),
                partition_row(root, "control", "ENG_PG_TEST", "dyn_a", 4, 10, 20),
            ]
            args = Namespace(
                workers=2,
                partition_count=[],
                min_partition_count=None,
                max_partition_count=None,
                max_estimated_hits=100,
                bible_only=True,
                controls_only=False,
                limit=None,
            )

            selected = select_remaining_rows(rows, args)

        self.assertEqual([row["partition_id"] for row in selected], ["keep"])

    def test_select_remaining_rows_treats_archived_marker_as_complete(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archived = partition_row(root, "archived", "TR_NT", "dyn_a", 1, 10, 20)
            Path(archived["manifest_out"]).write_text("{}\n", encoding="utf-8")
            gz_out = Path(archived["out"]).with_suffix(Path(archived["out"]).suffix + ".gz")
            marker = gz_out.with_suffix(gz_out.suffix + ".archived.json")
            marker.write_text(
                json.dumps({"archive_path": str(root / "offline-drive" / gz_out.name)}) + "\n",
                encoding="utf-8",
            )
            keep = partition_row(root, "keep", "TR_NT", "dyn_a", 2, 10, 20)
            args = Namespace(
                workers=2,
                partition_count=[],
                min_partition_count=None,
                max_partition_count=None,
                max_estimated_hits=100,
                bible_only=False,
                controls_only=False,
                limit=None,
            )

            selected = select_remaining_rows([archived, keep], args)

        self.assertEqual([row["partition_id"] for row in selected], ["keep"])

    def test_assign_rows_balances_estimated_hits_without_overlap(self) -> None:
        rows = [
            partition_stub("a", 100),
            partition_stub("b", 90),
            partition_stub("c", 80),
            partition_stub("d", 70),
        ]

        buckets = assign_rows(rows, workers=2, worker_prefix="box")

        assigned = [row["partition_id"] for bucket in buckets for row in bucket.rows]
        self.assertEqual(sorted(assigned), ["a", "b", "c", "d"])
        self.assertEqual(len(assigned), len(set(assigned)))
        self.assertEqual([bucket.label for bucket in buckets], ["box_01", "box_02"])

    def test_assign_rows_respects_worker_weights(self) -> None:
        rows = [
            partition_stub("a", 100),
            partition_stub("b", 100),
            partition_stub("c", 100),
            partition_stub("d", 100),
            partition_stub("e", 100),
            partition_stub("f", 100),
        ]

        buckets = assign_rows(
            rows,
            workers=2,
            worker_prefix="box",
            worker_weights={"box_01": 2.0, "box_02": 1.0},
        )

        by_label = {bucket.label: bucket for bucket in buckets}
        self.assertGreater(by_label["box_01"].estimated_hits, by_label["box_02"].estimated_hits)
        self.assertEqual(by_label["box_01"].estimated_hits, 400)
        self.assertEqual(by_label["box_02"].estimated_hits, 200)

    def test_parse_worker_weights_rejects_bad_values(self) -> None:
        self.assertEqual(
            parse_worker_weights(2, "box", ["box_01=2.5"]),
            {"box_01": 2.5, "box_02": 1.0},
        )
        with self.assertRaises(ValueError):
            parse_worker_weights(2, "box", ["box_03=2"])
        with self.assertRaises(ValueError):
            parse_worker_weights(2, "box", ["box_01=0"])
        with self.assertRaises(ValueError):
            parse_worker_weights(2, "box", ["box_01"])

    def test_write_worker_files_emits_local_count_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            count_source = root / "source_counts.csv"
            row = partition_row(root, "p1", "TR_NT", "dyn_a", 1, 1, 20)
            row["count_source_file"] = str(count_source)
            row["total_hit_count"] = "20"
            write_rows(count_source, [count_row_for_partition(row, status="counted")], COUNT_FIELDNAMES)
            bucket = assign_rows([row], workers=1, worker_prefix="worker")[0]
            out_dir = root / "worker_batches"

            write_worker_files(out_dir, [bucket], Namespace(), [row])

            worker_counts = read_rows(out_dir / "worker_01_counts.csv")
            worker_plan = read_rows(out_dir / "worker_01_partitions.csv")
            worker_readme = (out_dir / "worker_01_README.md").read_text(encoding="utf-8")

        self.assertEqual(worker_counts[0]["hit_count"], "20")
        self.assertEqual(worker_counts[0]["status"], "counted")
        self.assertTrue(worker_plan[0]["count_source_file"].endswith("worker_01_counts.csv"))
        self.assertNotIn("source_counts.csv", worker_plan[0]["export_command"])
        self.assertIn("--plan", worker_readme)
        self.assertIn("worker_01_counts.csv", worker_readme)

    def test_export_and_import_worker_bundle_round_trip(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path("reports/dynamic_skip_focus/partitions")) as tmp:
            root = Path(tmp)
            row = partition_row(root, "p1", "TR_NT", "dyn_a", 1, 1, 2)
            out = Path(row["out"])
            gz_out = out.with_suffix(out.suffix + ".gz")
            gz_out.write_text("compressed\n", encoding="utf-8")
            Path(row["manifest_out"]).write_text("{}\n", encoding="utf-8")
            Path(row["summary_out"]).write_text("# summary\n", encoding="utf-8")
            plan = root / "plan.csv"
            assignment = root / "assignment.csv"
            write_rows(plan, [row])
            write_rows(assignment, [{"worker": "worker_01", **row}])
            bundle = root / "worker_01.zip"
            manifest = root / "bundle.manifest.json"

            code = export_bundle.main(
                [
                    "--plan",
                    str(plan),
                    "--assignment",
                    str(assignment),
                    "--out",
                    str(bundle),
                    "--manifest-out",
                    str(manifest),
                ]
            )
            gz_out.unlink()
            Path(row["manifest_out"]).unlink()
            import_manifest = root / "import.manifest.json"
            import_code = import_bundle.main(
                [
                    str(bundle),
                    "--manifest-out",
                    str(import_manifest),
                ]
            )

            self.assertEqual(code, 0)
            self.assertEqual(import_code, 0)
            self.assertTrue(gz_out.exists())
            self.assertTrue(Path(row["manifest_out"]).exists())


def partition_stub(partition_id: str, estimated_hits: int) -> dict[str, str]:
    row = partition_row(Path("/tmp"), partition_id, "TR_NT", "dyn_a", 1, 1, estimated_hits)
    row["out"] = ""
    row["manifest_out"] = ""
    row["summary_out"] = ""
    return row


def partition_row(
    root: Path,
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
        "corpus_language": "greek",
        "term_id": term_id,
        "concept": "Demo",
        "category": "demo",
        "term_language": "greek",
        "term": "λογος",
        "normalized_term": "λογος",
        "normalized_length": "5",
        "mode": "full-span",
        "direction": "both",
        "total_hit_count": "10",
        "partition_index": str(partition_index),
        "partition_count": str(partition_count),
        "min_abs_skip": "2",
        "max_abs_skip": "9",
        "estimated_partition_hits": str(estimated_hits),
        "count_source_file": "",
        "out": str(root / f"{partition_id}.csv"),
        "summary_out": str(root / f"{partition_id}.md"),
        "manifest_out": str(root / f"{partition_id}.manifest.json"),
        "export_command": "",
    }


def write_rows(path: Path, rows: list[dict[str, str]], fieldnames: list[str] | None = None) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames or list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def count_row_for_partition(row: dict[str, str], *, status: str) -> dict[str, str]:
    return {
        "corpus": row["corpus"],
        "corpus_language": row["corpus_language"],
        "corpus_letters": "1000",
        "term_id": row["term_id"],
        "concept": row["concept"],
        "category": row["category"],
        "term_language": row["term_language"],
        "term": row["term"],
        "normalized_term": row["normalized_term"],
        "normalized_length": row["normalized_length"],
        "mode": row["mode"],
        "min_skip": "2",
        "effective_max_skip": "9",
        "search_space_positions": "100",
        "expected_hits": "1",
        "expected_hits_per_million_positions": "10",
        "direction": row["direction"],
        "forward_count": "11",
        "backward_count": "9",
        "hit_count": row["total_hit_count"],
        "hits_per_million_positions": "200",
        "counter_elapsed_seconds": "0.1",
        "status": status,
    }


if __name__ == "__main__":
    unittest.main()
