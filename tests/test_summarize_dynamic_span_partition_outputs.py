import csv
import gzip
import json
import tempfile
import unittest
from pathlib import Path

from scripts.compress_dynamic_span_partition_outputs import compress_rows
from scripts.summarize_dynamic_span_partition_outputs import (
    build_term_summary,
    completed_plan_rows,
    load_summary_cache,
    summarize_partition_output,
    summarize_partitions,
    write_summary_cache,
)


class DynamicSpanPartitionOutputSummaryTests(unittest.TestCase):
    def test_completed_plan_rows_requires_csv_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            out = tmp_path / "partition.csv"
            manifest = tmp_path / "partition.manifest.json"
            out.write_text("header\n", encoding="utf-8")
            row = plan_row(out, manifest)

            self.assertEqual(completed_plan_rows([row]), [])

            manifest.write_text("{}\n", encoding="utf-8")
            self.assertEqual([item["partition_id"] for item in completed_plan_rows([row])], ["p1"])

    def test_completed_plan_rows_accepts_compressed_csv_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            out = tmp_path / "partition.csv"
            gz_out = tmp_path / "partition.csv.gz"
            manifest = tmp_path / "partition.manifest.json"
            with gzip.open(gz_out, "wt", encoding="utf-8", newline="") as handle:
                handle.write("header\n")
            row = plan_row(out, manifest)

            self.assertEqual(completed_plan_rows([row]), [])

            manifest.write_text("{}\n", encoding="utf-8")
            self.assertEqual([item["partition_id"] for item in completed_plan_rows([row])], ["p1"])

    def test_summarize_partition_output_counts_hits_and_exact_centers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            out = tmp_path / "partition.csv"
            manifest = tmp_path / "partition.manifest.json"
            write_partition_hits(out)
            manifest.write_text("{}\n", encoding="utf-8")
            row = plan_row(out, manifest)

            summary, examples = summarize_partition_output(row, examples_per_partition=2)

        self.assertEqual(summary["exported_hits"], "2")
        self.assertEqual(summary["forward_hits"], "1")
        self.assertEqual(summary["backward_hits"], "1")
        self.assertEqual(summary["exact_center_word_hits"], "1")
        self.assertIn("MAT 1:1=1", summary["top_center_refs"])
        self.assertEqual({example["example_type"] for example in examples}, {"exact_center_word", "low_abs_skip"})

    def test_summarize_partition_output_manifest_only_uses_manifest_count(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            out = tmp_path / "partition.csv"
            manifest = tmp_path / "partition.manifest.json"
            write_partition_hits(out)
            manifest.write_text(json.dumps({"exported_hits": 123}) + "\n", encoding="utf-8")
            row = plan_row(out, manifest)

            summary, examples = summarize_partition_output(row, examples_per_partition=2, manifest_only=True)

        self.assertEqual(summary["exported_hits"], "123")
        self.assertEqual(summary["exact_center_word_hits"], "not_computed")
        self.assertEqual(summary["forward_hits"], "not_computed")
        self.assertEqual(examples, [])

    def test_summarize_partition_output_reads_compressed_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            out = tmp_path / "partition.csv"
            manifest = tmp_path / "partition.manifest.json"
            write_partition_hits(out)
            with out.open("rb") as src, gzip.open(str(out) + ".gz", "wb") as dst:
                dst.write(src.read())
            out.unlink()
            manifest.write_text("{}\n", encoding="utf-8")
            row = plan_row(out, manifest)

            summary, _examples = summarize_partition_output(row, examples_per_partition=2)

        self.assertEqual(summary["exported_hits"], "2")
        self.assertTrue(summary["out"].endswith("partition.csv.gz"))

    def test_summarize_partition_output_reads_archived_compressed_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            out = tmp_path / "partition.csv"
            gz_out = out.with_suffix(out.suffix + ".gz")
            archive_out = tmp_path / "archive" / "partition.csv.gz"
            manifest = tmp_path / "partition.manifest.json"
            marker = gz_out.with_suffix(gz_out.suffix + ".archived.json")
            write_partition_hits(out)
            archive_out.parent.mkdir(parents=True)
            with out.open("rb") as src, gzip.open(archive_out, "wb") as dst:
                dst.write(src.read())
            out.unlink()
            manifest.write_text("{}\n", encoding="utf-8")
            marker.write_text(json.dumps({"archive_path": str(archive_out)}) + "\n", encoding="utf-8")
            row = plan_row(out, manifest)

            self.assertEqual([item["partition_id"] for item in completed_plan_rows([row])], ["p1"])
            summary, _examples = summarize_partition_output(row, examples_per_partition=2)

        self.assertEqual(summary["exported_hits"], "2")
        self.assertEqual(summary["out"], str(archive_out))

    def test_compress_rows_updates_cache_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            out = tmp_path / "partition.csv"
            manifest = tmp_path / "partition.manifest.json"
            write_partition_hits(out)
            manifest.write_text("{}\n", encoding="utf-8")
            row = plan_row(out, manifest)
            cache: dict[str, dict] = {}
            summarize_partitions([row], examples_per_partition=2, cache=cache)

            results = compress_rows([row], cache=cache, examples_per_partition=2, dry_run=False)
            second_rows, _examples, stats = summarize_partitions([row], examples_per_partition=2, cache=cache)

            self.assertEqual(results[0]["status"], "compressed")
            self.assertFalse(out.exists())
            self.assertTrue(Path(str(out) + ".gz").exists())
            self.assertEqual(stats["hits"], 1)
            self.assertEqual(second_rows[0]["exported_hits"], "2")

    def test_build_term_summary_marks_complete_and_partial_rows(self) -> None:
        plan_rows = [
            plan_template("TR_NT", "dyn_a", "1", "2"),
            plan_template("TR_NT", "dyn_a", "2", "2"),
            plan_template("KJV", "dyn_b", "1", "1"),
        ]
        partition_rows = [
            partition_summary("TR_NT", "dyn_a", "1", "2", "3", "10"),
            partition_summary("KJV", "dyn_b", "1", "1", "0", "5"),
        ]

        rows = build_term_summary(plan_rows, partition_rows)
        by_key = {(row["corpus"], row["term_id"]): row for row in rows}

        self.assertEqual(by_key[("TR_NT", "dyn_a")]["coverage_status"], "partial")
        self.assertEqual(by_key[("KJV", "dyn_b")]["coverage_status"], "complete")
        self.assertEqual(by_key[("TR_NT", "dyn_a")]["exact_center_word_hits"], "3")

    def test_summarize_partitions_reuses_matching_cache_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            out = tmp_path / "partition.csv"
            manifest = tmp_path / "partition.manifest.json"
            write_partition_hits(out)
            manifest.write_text("{}\n", encoding="utf-8")
            row = plan_row(out, manifest)
            cache: dict[str, dict] = {}

            first_rows, first_examples, first_stats = summarize_partitions(
                [row],
                examples_per_partition=2,
                cache=cache,
            )
            second_rows, second_examples, second_stats = summarize_partitions(
                [row],
                examples_per_partition=2,
                cache=cache,
            )

        self.assertEqual(first_stats["misses"], 1)
        self.assertEqual(first_stats["hits"], 0)
        self.assertEqual(second_stats["misses"], 0)
        self.assertEqual(second_stats["hits"], 1)
        self.assertEqual(first_rows, second_rows)
        self.assertEqual(first_examples, second_examples)

    def test_summary_cache_round_trips_json_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "cache.json"
            cache = {"p1": {"fingerprint": {"out": "x"}, "summary": {"a": "b"}, "examples": []}}

            write_summary_cache(cache_path, cache)
            loaded = load_summary_cache(cache_path)

        self.assertEqual(loaded, cache)


def plan_row(out: Path, manifest: Path) -> dict[str, str]:
    row = plan_template("TR_NT", "dyn_a", "1", "1")
    row["partition_id"] = "p1"
    row["out"] = str(out)
    row["manifest_out"] = str(manifest)
    row["estimated_partition_hits"] = "2"
    return row


def plan_template(corpus: str, term_id: str, index: str, count: str) -> dict[str, str]:
    return {
        "partition_id": f"{corpus}_{term_id}_{index}",
        "corpus": corpus,
        "term_id": term_id,
        "mode": "full-span",
        "total_hit_count": "10",
        "partition_index": index,
        "partition_count": count,
        "min_abs_skip": "2",
        "max_abs_skip": "9",
        "estimated_partition_hits": "5",
        "out": "",
        "manifest_out": "",
    }


def partition_summary(
    corpus: str,
    term_id: str,
    index: str,
    count: str,
    exact_hits: str,
    exported_hits: str,
) -> dict[str, str]:
    return {
        "partition_id": f"{corpus}_{term_id}_{index}",
        "corpus": corpus,
        "term_id": term_id,
        "mode": "full-span",
        "partition_index": index,
        "partition_count": count,
        "min_abs_skip": "2",
        "max_abs_skip": "9",
        "exported_hits": exported_hits,
        "exact_center_word_hits": exact_hits,
    }


def write_partition_hits(path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "normalized_term",
                "term",
                "skip",
                "direction",
                "span_letters",
                "start_ref",
                "center_ref",
                "end_ref",
                "center_word",
                "center_normalized_word",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "normalized_term": "λογος",
                "term": "λογος",
                "skip": "2",
                "direction": "forward",
                "span_letters": "10",
                "start_ref": "MAT 1:1",
                "center_ref": "MAT 1:1",
                "end_ref": "MAT 1:2",
                "center_word": "λογος",
                "center_normalized_word": "λογος",
            }
        )
        writer.writerow(
            {
                "normalized_term": "λογος",
                "term": "λογος",
                "skip": "-3",
                "direction": "backward",
                "span_letters": "15",
                "start_ref": "MAT 2:1",
                "center_ref": "MAT 2:1",
                "end_ref": "MAT 1:1",
                "center_word": "και",
                "center_normalized_word": "και",
            }
        )


if __name__ == "__main__":
    unittest.main()
