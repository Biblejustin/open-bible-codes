import csv
import tempfile
import unittest
from pathlib import Path

from scripts.export_dynamic_span_exact_center_rows import export_exact_center_rows


class ExportDynamicSpanExactCenterRowsTests(unittest.TestCase):
    def test_exports_exact_rows_from_partitions_and_hit_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            partition_hits = tmp_path / "partition.csv"
            partition_manifest = tmp_path / "partition.manifest.json"
            plan = tmp_path / "plan.csv"
            hit_file = tmp_path / "hits.csv"
            out = tmp_path / "exact.csv"
            write_hits(
                partition_hits,
                [
                    hit("TR_NT", "dyn_jesus_g", "ιησουσ", "ιησουσ", "MAT 1:1"),
                    hit("TR_NT", "dyn_jesus_g", "ιησουσ", "λογοσ", "MAT 1:2"),
                ],
            )
            partition_manifest.write_text("{}\n", encoding="utf-8")
            write_plan(plan, partition_hits, partition_manifest)
            write_hits(
                hit_file,
                [
                    hit("KJV", "dyn_jesus_e", "jesus", "jesus", "MAT 1:1"),
                    hit("KJV", "dyn_jesus_e", "jesus", "lord", "MAT 1:2"),
                ],
            )

            result = export_exact_center_rows([plan], [hit_file], out)
            exact_rows = list(csv.DictReader(out.open(encoding="utf-8", newline="")))

        self.assertEqual(result["totals"]["scanned_hit_rows"], 4)
        self.assertEqual(result["totals"]["exact_center_rows"], 2)
        self.assertEqual([row["center_ref"] for row in exact_rows], ["MAT 1:1", "MAT 1:1"])
        self.assertEqual([row["center_source"] for row in exact_rows], ["TR_NT", "KJV"])
        self.assertEqual([row["center_word_index"] for row in exact_rows], ["7", "7"])
        summaries = {key: value.to_row() for key, value in result["summaries"].items()}
        self.assertEqual(summaries[("TR_NT", "dyn_jesus_g", "ιησουσ", "partition")]["exact_center_rows"], "1")
        self.assertEqual(summaries[("KJV", "dyn_jesus_e", "jesus", "hit_file")]["exact_center_rows"], "1")


FIELDNAMES = [
    "corpus",
    "term_id",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "span_letters",
    "start_ref",
    "center_ref",
    "end_ref",
    "center_source",
    "center_word_index",
    "center_word",
    "center_normalized_word",
    "start_offset",
    "center_offset",
    "end_offset",
]


def write_hits(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_plan(path: Path, out: Path, manifest: Path) -> None:
    rows = [
        {
            "partition_id": "p1",
            "out": str(out),
            "manifest_out": str(manifest),
        }
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def hit(
    corpus: str,
    term_id: str,
    normalized_term: str,
    center_normalized_word: str,
    center_ref: str,
) -> dict[str, str]:
    return {
        "corpus": corpus,
        "term_id": term_id,
        "term": normalized_term,
        "normalized_term": normalized_term,
        "skip": "3",
        "direction": "forward",
        "span_letters": "9",
        "start_ref": "MAT 1:1",
        "center_ref": center_ref,
        "end_ref": "MAT 1:3",
        "center_source": corpus,
        "center_word_index": "7",
        "center_word": center_normalized_word,
        "center_normalized_word": center_normalized_word,
        "start_offset": "1",
        "center_offset": "2",
        "end_offset": "3",
    }


if __name__ == "__main__":
    unittest.main()
