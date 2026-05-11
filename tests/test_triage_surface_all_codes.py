import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pytest

from els.report_db import default_table_name, import_csv_table
from scripts import triage_surface_all_codes as triage
from scripts.triage_surface_all_codes import bucket_for_row, main


HIT_FIELDNAMES = [
    "corpus",
    "term_source",
    "term_id",
    "concept",
    "category",
    "term",
    "normalized_term",
    "skip",
    "direction",
    "start_offset",
    "end_offset",
    "span_letters",
    "sequence",
    "start_ref",
    "end_ref",
    "start_source",
    "end_source",
    "center_offset",
    "center_ref",
    "center_source",
    "center_word_index",
    "center_word",
    "center_normalized_word",
    "best_context",
    "center_word_exact",
    "center_word_same_concept",
    "center_word_same_category",
    "center_exact",
    "center_same_concept",
    "center_same_category",
    "span_exact",
    "span_same_concept",
    "span_same_category",
    "center_word_same_concept_terms",
    "center_word_same_category_terms",
    "center_same_concept_terms",
    "center_same_category_terms",
    "span_exact_refs",
    "span_same_concept_refs",
    "span_same_category_refs",
]


class TriageSurfaceAllCodesTests(unittest.TestCase):
    def test_bucket_priority_prefers_center_word_over_broader_context(self) -> None:
        self.assertEqual(
            bucket_for_row(
                {
                    "center_word_same_category": "true",
                    "center_exact": "true",
                    "span_exact": "true",
                }
            ),
            "center_word_same_category",
        )
        self.assertEqual(bucket_for_row({"span_same_category": "true"}), "span_same_category")
        self.assertEqual(bucket_for_row({}), "hidden_path_only")

    def test_main_writes_ranked_queue_markdown_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hits = root / "hits.csv"
            summary = root / "summary.csv"
            controls = root / "controls.csv"
            queue = root / "queue.csv"
            markdown = root / "triage.md"
            manifest = root / "manifest.json"

            write_csv(
                hits,
                HIT_FIELDNAMES,
                [
                    hit_row("A", "alpha_h", "alpha", "center_word_exact", "true"),
                    hit_row("B", "alpha_h", "alpha", "center_word_exact", "true"),
                    hit_row("A", "beta_h", "beta", "hidden_path_only", ""),
                ],
            )
            write_csv(
                summary,
                ["corpus", "term_id", "normalized_length"],
                [
                    {"corpus": "A", "term_id": "alpha_h", "normalized_length": "5"},
                    {"corpus": "B", "term_id": "beta_h", "normalized_length": "4"},
                ],
            )
            write_csv(
                controls,
                [
                    "term_id",
                    "representative_best_band",
                    "representative_best_p",
                    "representative_best_q",
                    "representative_best_read",
                ],
                [
                    {
                        "term_id": "alpha_h",
                        "representative_best_band": "not_unusual",
                        "representative_best_p": "0.5",
                        "representative_best_q": "1.0",
                        "representative_best_read": "control read",
                    }
                ],
            )

            exit_code = main(
                [
                    "--hits",
                    str(hits),
                    "--summary",
                    str(summary),
                    "--controlled-summary",
                    str(controls),
                    "--max-rows-per-bucket",
                    "2",
                    "--candidate-multiplier",
                    "2",
                    "--queue-out",
                    str(queue),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(exit_code, 0)
            rows = read_csv(queue)
            self.assertEqual(rows[0]["bucket"], "center_word_exact")
            self.assertEqual(rows[0]["presence_scope"], "all_source")
            self.assertEqual(rows[0]["present_corpora"], "A,B")
            self.assertEqual(rows[0]["offsets_by_corpus"], "A:1/3/5;B:1/3/5")
            self.assertEqual(rows[0]["center_words_by_corpus"], "A:alpha;B:alpha")
            self.assertEqual(rows[0]["control_read"], "control read")
            self.assertEqual(rows[1]["bucket"], "hidden_path_only")
            self.assertEqual(rows[1]["control_band"], "not_run")
            self.assertEqual(rows[1]["control_read"], "not run in exact controlled matrix")
            self.assertIn("center_word_exact", markdown.read_text(encoding="utf-8"))
            self.assertIn("not_run", markdown.read_text(encoding="utf-8"))
            data = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(data["scanned_rows"], 3)
            self.assertEqual(data["queue_rows"], 2)
            self.assertEqual(data["bucket_counts"]["center_word_exact"], 1)

    def test_markdown_displays_original_language_terms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hits = root / "hits.csv"
            summary = root / "summary.csv"
            queue = root / "queue.csv"
            markdown = root / "triage.md"
            manifest = root / "manifest.json"

            write_csv(
                hits,
                HIT_FIELDNAMES,
                [
                    {
                        **hit_row("A", "trump_h", "טראמפ", "center_word_exact", "true"),
                        "concept": "Trump",
                    }
                ],
            )
            write_csv(
                summary,
                ["corpus", "term_id", "normalized_length"],
                [{"corpus": "A", "term_id": "trump_h", "normalized_length": "5"}],
            )

            exit_code = main(
                [
                    "--hits",
                    str(hits),
                    "--summary",
                    str(summary),
                    "--max-rows-per-bucket",
                    "1",
                    "--candidate-multiplier",
                    "1",
                    "--queue-out",
                    str(queue),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(exit_code, 0)
            text = markdown.read_text(encoding="utf-8")
            self.assertIn("`טראמפ` (trmp; English: Trump)", text)

    def test_main_can_read_hits_from_duckdb(self) -> None:
        pytest.importorskip("duckdb")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hits = root / "hits.csv"
            summary = root / "summary.csv"
            queue = root / "queue.csv"
            markdown = root / "triage.md"
            manifest = root / "manifest.json"
            db = root / "reports" / "db.duckdb"

            write_csv(
                hits,
                HIT_FIELDNAMES,
                [
                    hit_row("A", "alpha_h", "alpha", "center_word_exact", "true"),
                    hit_row("B", "alpha_h", "alpha", "center_word_exact", "true"),
                    hit_row("A", "beta_h", "beta", "hidden_path_only", ""),
                ],
            )
            write_csv(
                summary,
                ["corpus", "term_id", "normalized_length"],
                [
                    {"corpus": "A", "term_id": "alpha_h", "normalized_length": "5"},
                    {"corpus": "B", "term_id": "beta_h", "normalized_length": "4"},
                ],
            )
            import_csv_table(db_path=db, csv_path=hits, table_name="hits")

            exit_code = main(
                [
                    "--hits",
                    str(hits),
                    "--summary",
                    str(summary),
                    "--db",
                    str(db),
                    "--hits-table",
                    "hits",
                    "--max-rows-per-bucket",
                    "2",
                    "--candidate-multiplier",
                    "2",
                    "--queue-out",
                    str(queue),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(exit_code, 0)
            rows = read_csv(queue)
            self.assertEqual(rows[0]["bucket"], "center_word_exact")
            self.assertEqual(rows[0]["presence_scope"], "all_source")
            self.assertEqual(rows[0]["present_corpora"], "A,B")
            data = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(data["scanned_rows"], 3)

    def test_main_auto_uses_current_default_duckdb(self) -> None:
        pytest.importorskip("duckdb")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hits = root / "hits.csv"
            summary = root / "summary.csv"
            queue = root / "queue.csv"
            markdown = root / "triage.md"
            manifest = root / "manifest.json"
            db = root / "reports" / "db.duckdb"

            write_csv(
                hits,
                HIT_FIELDNAMES,
                [
                    hit_row("A", "alpha_h", "alpha", "center_word_exact", "true"),
                    hit_row("B", "alpha_h", "alpha", "center_word_exact", "true"),
                    hit_row("A", "beta_h", "beta", "hidden_path_only", ""),
                ],
            )
            write_csv(
                summary,
                ["corpus", "term_id", "normalized_length"],
                [
                    {"corpus": "A", "term_id": "alpha_h", "normalized_length": "5"},
                    {"corpus": "B", "term_id": "beta_h", "normalized_length": "4"},
                ],
            )
            import_csv_table(db_path=db, csv_path=hits, table_name=default_table_name(hits))

            with patch.object(triage, "DEFAULT_REPORT_DB", db):
                exit_code = main(
                    [
                        "--hits",
                        str(hits),
                        "--summary",
                        str(summary),
                        "--max-rows-per-bucket",
                        "2",
                        "--candidate-multiplier",
                        "2",
                        "--queue-out",
                        str(queue),
                        "--markdown-out",
                        str(markdown),
                        "--manifest-out",
                        str(manifest),
                    ]
                )

            self.assertEqual(exit_code, 0)
            data = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(data["report_db"], str(db))
            self.assertEqual(data["scanned_rows"], 3)


def hit_row(
    corpus: str,
    term_id: str,
    normalized_term: str,
    best_context: str,
    center_word_exact: str,
) -> dict[str, str]:
    row = {field: "" for field in HIT_FIELDNAMES}
    row.update(
        {
            "corpus": corpus,
            "term_source": "terms.csv",
            "term_id": term_id,
            "concept": normalized_term.title(),
            "category": "letters",
            "term": normalized_term,
            "normalized_term": normalized_term,
            "skip": "2",
            "direction": "forward",
            "start_offset": "1",
            "center_offset": "3",
            "end_offset": "5",
            "span_letters": "9",
            "sequence": normalized_term,
            "start_ref": "Test 1:1",
            "center_ref": "Test 1:1",
            "end_ref": "Test 1:2",
            "center_word": normalized_term,
            "center_normalized_word": normalized_term,
            "best_context": best_context,
            "center_word_exact": center_word_exact,
        }
    )
    return row


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    unittest.main()
