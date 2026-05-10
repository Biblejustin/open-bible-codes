import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_dynamic_span_exact_center_extensions_report import (
    corpus_label_from_manifest_path,
    load_report_data,
    reproduce_command,
    shell_quote,
    top_sort_key,
    write_markdown,
)


class BuildDynamicSpanExactCenterExtensionsReportTests(unittest.TestCase):
    def test_load_report_data_reads_manifests_summaries_and_tops(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "extensions_kjv.manifest.json").write_text(
                json.dumps({"corpus_label": "KJV", "hit_count": 2, "extension_count": 3}),
                encoding="utf-8",
            )
            write_csv(
                root / "summary_kjv.csv",
                ["corpus", "term", "normalized_term", "skip", "direction", "extension_type", "extension_side", "match_kind", "rows", "unique_extended_sequences", "max_extension_length", "max_match_count"],
                [{"corpus": "KJV", "term": "Jesus", "normalized_term": "jesus", "skip": "3", "direction": "forward", "extension_type": "term_plus_after", "extension_side": "after", "match_kind": "phrase_2", "rows": "1", "unique_extended_sequences": "1", "max_extension_length": "3", "max_match_count": "4"}],
            )
            write_csv(
                root / "top_kjv.csv",
                ["corpus", "normalized_term", "center_ref", "extended_sequence", "extension_type", "match_kind", "match_count", "matched_examples", "extension_score", "extension_length"],
                [{"corpus": "KJV", "normalized_term": "jesus", "center_ref": "MAT 1:1", "extended_sequence": "jesusand", "extension_type": "term_plus_after", "match_kind": "phrase_2", "match_count": "4", "matched_examples": "Jesus and", "extension_score": "3219", "extension_length": "3"}],
            )

            data = load_report_data(root)

        self.assertEqual(len(data["manifests"]), 1)
        self.assertEqual(data["manifests"][0]["corpus_label"], "KJV")
        self.assertEqual(len(data["summary_rows"]), 1)
        self.assertEqual(len(data["top_rows"]), 1)

    def test_corpus_label_from_manifest_path_handles_multi_part_labels(self) -> None:
        self.assertEqual(
            corpus_label_from_manifest_path(Path("extensions_ebible_wlc.manifest.json")),
            "EBIBLE_WLC",
        )
        self.assertEqual(
            corpus_label_from_manifest_path(Path("extensions_tcg_nt.manifest.json")),
            "TCG_NT",
        )

    def test_top_sort_key_prefers_score_then_length_then_match_count(self) -> None:
        self.assertGreater(
            top_sort_key({"extension_score": "10", "extension_length": "3", "match_count": "1"}),
            top_sort_key({"extension_score": "9", "extension_length": "9", "match_count": "9"}),
        )

    def test_reproduce_command_includes_title_and_manifest(self) -> None:
        args = type(
            "Args",
            (),
            {
                "input_dir": "reports/extensions",
                "markdown_out": "docs/report.md",
                "manifest_out": "reports/extensions/report.manifest.json",
                "title": "Control Exact-Center Extensions",
                "top": 50,
                "summary_row_limit": 100,
            },
        )()

        command = reproduce_command(args)

        self.assertIn("--manifest-out reports/extensions/report.manifest.json", command)
        self.assertIn("--title 'Control Exact-Center Extensions'", command)
        self.assertIn("--top 50", command)
        self.assertIn("--summary-row-limit 100", command)

    def test_shell_quote_handles_single_quotes(self) -> None:
        self.assertEqual(shell_quote("Bob's Report"), "'Bob'\"'\"'s Report'")

    def test_write_markdown_displays_original_language_terms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / "extensions.md"
            args = type(
                "Args",
                (),
                {
                    "input_dir": root,
                    "markdown_out": out,
                    "manifest_out": root / "manifest.json",
                    "title": "Control Exact-Center Extensions",
                    "top": 25,
                    "summary_row_limit": 120,
                },
            )()

            write_markdown(
                out,
                {
                    "manifests": [
                        {"corpus_label": "HEB_PBY_BIALIK", "hit_count": "1", "extension_count": "1"}
                    ],
                    "summary_rows": [
                        {
                            "corpus": "HEB_PBY_BIALIK",
                            "normalized_term": "משיח",
                            "skip": "7",
                            "direction": "forward",
                            "extension_type": "term_plus_after",
                            "match_kind": "phrase_2",
                            "rows": "1",
                            "max_extension_length": "3",
                            "max_match_count": "2",
                        }
                    ],
                    "top_rows": [
                        {
                            "corpus": "HEB_PBY_BIALIK",
                            "normalized_term": "משיח",
                            "center_ref": "PBY",
                            "extended_sequence": "הממשיחימ",
                            "extension_type": "before_plus_term_plus_after",
                            "match_kind": "phrase_2",
                            "match_count": "3",
                            "matched_examples": "הם משיחים",
                        }
                    ],
                },
                args,
            )

            text = out.read_text(encoding="utf-8")

        self.assertIn("`משיח` (Mashiach; English: Messiah/anointed one)", text)
        self.assertIn("`הממשיחימ`", text)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
