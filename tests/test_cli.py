import csv
import json
import os
import tempfile
import unittest
from pathlib import Path

from els.cli import main


class CliTests(unittest.TestCase):
    def test_search_full_span_max_skip_reaches_end_of_corpus(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.txt"
            config = root / "source.toml"
            out = root / "hits.csv"
            manifest = root / "manifest.json"

            source.write_text("αγγβ", encoding="utf-8")
            config.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        'language = "greek"',
                        "",
                        "[[sources]]",
                        'name = "sample"',
                        'format = "text"',
                        'path = "source.txt"',
                        'ref = "Sample 1:1"',
                    ]
                ),
                encoding="utf-8",
            )

            exit_code = main(
                [
                    "search",
                    "--config",
                    str(config),
                    "--term",
                    "αβ",
                    "--min-skip",
                    "3",
                    "--max-skip",
                    "1",
                    "--max-skip-mode",
                    "full-span",
                    "--direction",
                    "forward",
                    "--out",
                    str(out),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            rows = read_rows(out)
            manifest_data = json.loads(manifest.read_text(encoding="utf-8"))

        self.assertEqual(exit_code, 0)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["skip"], "3")
        self.assertEqual(manifest_data["max_skip_mode"], "full-span")
        self.assertEqual(manifest_data["effective_max_skips"], {"αβ": 3})

    def test_batch_full_span_records_effective_row_max_skip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.txt"
            config = root / "source.toml"
            terms = root / "terms.csv"
            out = root / "counts.csv"

            source.write_text("αγγβ", encoding="utf-8")
            config.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        'language = "greek"',
                        "",
                        "[[sources]]",
                        'name = "sample"',
                        'format = "text"',
                        'path = "source.txt"',
                        'ref = "Sample 1:1"',
                    ]
                ),
                encoding="utf-8",
            )
            write_terms(terms, "t1", "alpha_beta", "αβ")

            exit_code = main(
                [
                    "batch",
                    "--terms",
                    str(terms),
                    "--corpus",
                    f"SAMPLE={config}",
                    "--min-skip",
                    "3",
                    "--max-skip-mode",
                    "full-span",
                    "--direction",
                    "forward",
                    "--min-term-length",
                    "1",
                    "--out",
                    str(out),
                ]
            )

            rows = read_rows(out)

        self.assertEqual(exit_code, 0)
        self.assertEqual(rows[0]["hit_count"], "1")
        self.assertEqual(rows[0]["max_skip"], "3")

    def test_batch_many_splits_reports_after_shared_count(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cache_dir = root / "cache"
            source = root / "source.txt"
            config = root / "source.toml"
            second_config = root / "source2.toml"
            first_terms = root / "first.csv"
            second_terms = root / "second.csv"
            out_dir = root / "out"
            manifest = root / "combined.manifest.json"

            source.write_text("αβγδαβγδ", encoding="utf-8")
            config.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        'language = "greek"',
                        "",
                        "[[sources]]",
                        'name = "sample"',
                        'format = "text"',
                        'path = "source.txt"',
                        'ref = "Sample 1:1"',
                    ]
                ),
                encoding="utf-8",
            )
            second_config.write_text(config.read_text(encoding="utf-8"), encoding="utf-8")
            write_terms(first_terms, "t1", "alpha_beta", "αβ")
            write_terms(second_terms, "t2", "gamma_delta", "γδ")

            prior_cache = os.environ.get("EDLS_CORPUS_CACHE_DIR")
            os.environ["EDLS_CORPUS_CACHE_DIR"] = str(cache_dir)
            try:
                exit_code = main(
                    [
                        "batch-many",
                        "--term-set",
                        f"first={first_terms}",
                        "--term-set",
                        f"second={second_terms}",
                        "--corpus",
                        f"SAMPLE={config}",
                        "--corpus",
                        f"SAMPLE2={second_config}",
                        "--min-skip",
                        "1",
                        "--max-skip",
                        "1",
                        "--direction",
                        "forward",
                        "--min-term-length",
                        "1",
                        "--corpus-jobs",
                        "2",
                        "--out-dir",
                        str(out_dir),
                        "--manifest-out",
                        str(manifest),
                    ]
                )
            finally:
                if prior_cache is None:
                    os.environ.pop("EDLS_CORPUS_CACHE_DIR", None)
                else:
                    os.environ["EDLS_CORPUS_CACHE_DIR"] = prior_cache

            first_rows = read_rows(out_dir / "first_counts.csv")
            second_rows = read_rows(out_dir / "second_counts.csv")
            manifest_data = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(exit_code, 0)
            self.assertEqual(len(first_rows), 2)
            self.assertEqual(len(second_rows), 2)
            self.assertEqual(first_rows[0]["hit_count"], "2")
            self.assertEqual(first_rows[0]["term"], "αβ")
            self.assertEqual(second_rows[0]["hit_count"], "2")
            self.assertEqual(second_rows[0]["term"], "γδ")
            self.assertEqual(manifest_data["corpus_timings"][0]["label"], "SAMPLE")
            self.assertEqual(manifest_data["corpus_timings"][0]["counted_terms"], 2)
            self.assertEqual(manifest_data["corpus_timings"][1]["label"], "SAMPLE2")
            self.assertEqual(manifest_data["effective_corpus_jobs"], 2)
            self.assertIn("count_seconds", manifest_data["corpus_timings"][0])
            self.assertTrue((out_dir / "first_counts.manifest.json").exists())
            self.assertTrue((out_dir / "second_counts.manifest.json").exists())
            self.assertTrue(manifest.exists())

    def test_surface_context_jobs_writes_expected_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cache_dir = root / "cache"
            source = root / "source.txt"
            config = root / "source.toml"
            terms = root / "terms.csv"
            hits_out = root / "hits.csv"
            summary_out = root / "summary.csv"
            manifest = root / "manifest.json"

            source.write_text("αβγδαβγδ", encoding="utf-8")
            config.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        'language = "greek"',
                        "",
                        "[[sources]]",
                        'name = "sample"',
                        'format = "text"',
                        'path = "source.txt"',
                        'ref = "Sample 1:1"',
                    ]
                ),
                encoding="utf-8",
            )
            write_terms(terms, "t1", "alpha_beta", "αβ")

            prior_cache = os.environ.get("EDLS_CORPUS_CACHE_DIR")
            os.environ["EDLS_CORPUS_CACHE_DIR"] = str(cache_dir)
            try:
                exit_code = main(
                    [
                        "surface-context",
                        "--terms",
                        str(terms),
                        "--corpus",
                        f"SAMPLE={config}",
                        "--min-skip",
                        "1",
                        "--max-skip",
                        "1",
                        "--direction",
                        "forward",
                        "--min-term-length",
                        "1",
                        "--jobs",
                        "2",
                        "--out",
                        str(hits_out),
                        "--summary-out",
                        str(summary_out),
                        "--manifest-out",
                        str(manifest),
                    ]
                )
            finally:
                if prior_cache is None:
                    os.environ.pop("EDLS_CORPUS_CACHE_DIR", None)
                else:
                    os.environ["EDLS_CORPUS_CACHE_DIR"] = prior_cache

            hit_rows = read_rows(hits_out)
            summary_rows = read_rows(summary_out)
            manifest_data = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(exit_code, 0)
            self.assertEqual(len(hit_rows), 2)
            self.assertEqual(summary_rows[0]["hit_count"], "2")
            self.assertEqual(summary_rows[0]["context_hit_count"], "2")
            self.assertEqual(manifest_data["jobs"], 2)

    def test_batch_many_rejects_nested_parallel_workers(self) -> None:
        with self.assertRaises(SystemExit):
            main(
                [
                    "batch-many",
                    "--term-set",
                    "first=terms/theological_terms.csv",
                    "--corpus",
                    "TR_NT=configs/example_ebible_grctr.toml",
                    "--corpus",
                    "SBLGNT=configs/example_sblgnt.toml",
                    "--jobs",
                    "2",
                    "--corpus-jobs",
                    "2",
                    "--out-dir",
                    "/tmp/unused-edls-batch-many",
                ]
            )

    def test_batch_many_counts_english_terms_on_english_corpus_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.txt"
            config = root / "source.toml"
            terms = root / "terms.csv"
            out_dir = root / "out"

            source.write_text("Jesus said Jesus", encoding="utf-8")
            config.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        'language = "english"',
                        "",
                        "[[sources]]",
                        'name = "sample"',
                        'format = "text"',
                        'path = "source.txt"',
                        'ref = "Sample 1:1"',
                    ]
                ),
                encoding="utf-8",
            )
            terms.write_text(
                "\n".join(
                    [
                        "term_id,concept,category,language,term",
                        "jesus_e,Jesus,test,english,Jesus",
                        "jesus_g,Jesus,test,greek,ιησους",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            exit_code = main(
                [
                    "batch-many",
                    "--term-set",
                    f"english={terms}",
                    "--corpus",
                    f"EN={config}",
                    "--min-skip",
                    "1",
                    "--max-skip",
                    "1",
                    "--direction",
                    "forward",
                    "--min-term-length",
                    "1",
                    "--out-dir",
                    str(out_dir),
                ]
            )

            rows = read_rows(out_dir / "english_counts.csv")

        self.assertEqual(exit_code, 0)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["term_id"], "jesus_e")
        self.assertEqual(rows[0]["term_language"], "english")
        self.assertEqual(rows[0]["hit_count"], "2")

    def test_pairs_writes_compactness_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.txt"
            config = root / "source.toml"
            terms = root / "terms.csv"
            out = root / "pairs.csv"

            source.write_text("αβγδαβγδ", encoding="utf-8")
            config.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        'language = "greek"',
                        "",
                        "[[sources]]",
                        'name = "sample"',
                        'format = "text"',
                        'path = "source.txt"',
                        'ref = "Sample 1:1"',
                    ]
                ),
                encoding="utf-8",
            )
            terms.write_text(
                "\n".join(
                    [
                        "term_id,concept,category,language,term",
                        "left,Left,left,greek,αβ",
                        "right,Right,right,greek,γδ",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            exit_code = main(
                [
                    "pairs",
                    "--terms",
                    str(terms),
                    "--corpus",
                    f"SAMPLE={config}",
                    "--left-category",
                    "left",
                    "--right-category",
                    "right",
                    "--min-skip",
                    "1",
                    "--max-skip",
                    "1",
                    "--direction",
                    "forward",
                    "--min-term-length",
                    "1",
                    "--max-gap",
                    "10",
                    "--row-width",
                    "4",
                    "--out",
                    str(out),
                ]
            )

            rows = read_rows(out)

        self.assertEqual(exit_code, 0)
        self.assertGreaterEqual(len(rows), 1)
        self.assertEqual(rows[0]["span_gap"], "1")
        self.assertEqual(rows[0]["center_distance"], "2.0")
        self.assertEqual(rows[0]["same_signed_skip"], "True")
        self.assertEqual(rows[0]["same_abs_skip"], "True")
        self.assertEqual(rows[0]["compactness_score"], "3.0")
        self.assertEqual(rows[0]["cylindrical_row_width"], "4")
        self.assertEqual(rows[0]["cylindrical_distance"], "1.0")


def write_terms(path: Path, term_id: str, concept: str, term: str) -> None:
    path.write_text(
        "\n".join(
            [
                "term_id,concept,category,language,term",
                f"{term_id},{concept},test,greek,{term}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    unittest.main()
