import argparse
import json
import tempfile
import time
import unittest
from pathlib import Path

from scripts.summarize_kjv_apocrypha_bridge_terms import (
    FIELDNAMES,
    display_summary_term,
    manifest_args,
    sample_refs,
    write_csv,
    write_manifest,
    summarize_term_shuffled,
    summarize_terms,
)


class KJVAapocryphaBridgeTermReviewTests(unittest.TestCase):
    def test_summarize_terms_ranks_observed_above_controls_first(self) -> None:
        candidates = [
            candidate("alpha", "canonical_to_apocrypha", "MAL 4:6", "TOB 1:1", "TOB 1:2"),
            candidate("alpha", "apocrypha_to_canonical", "TOB 1:1", "MAL 4:6", "MAL 4:5"),
            candidate("beta", "canonical_to_apocrypha", "MAL 4:6", "TOB 1:1", "TOB 1:1"),
        ]
        context = [
            context_row("alpha", "span_exact"),
            context_row("alpha", "hidden_path_only"),
            context_row("beta", "center_verse_same_category"),
        ]
        controls = [
            control("SHAKESPEARE", "alpha", 1),
            control("WAR_PEACE", "alpha", 0),
            control("MOBY_DICK", "alpha", 0),
            control("SHAKESPEARE", "beta", 3),
        ]

        rows = summarize_terms(candidates, context, controls)

        self.assertEqual(rows[0]["normalized_term"], "alpha")
        self.assertEqual(rows[0]["observed_bridge_rows"], 2)
        self.assertEqual(rows[0]["canonical_to_apocrypha"], 1)
        self.assertEqual(rows[0]["apocrypha_to_canonical"], 1)
        self.assertEqual(rows[0]["control_max_bridge_rows"], 1)
        self.assertEqual(rows[0]["observed_minus_control_max"], 1)
        self.assertEqual(rows[0]["observed_gt_all_controls"], "True")
        self.assertEqual(rows[0]["span_exact"], 1)
        self.assertEqual(rows[0]["hidden_path_only"], 1)
        self.assertEqual(rows[1]["normalized_term"], "beta")
        self.assertEqual(rows[1]["observed_gt_all_controls"], "False")

    def test_sample_refs_deduplicates_and_limits_refs(self) -> None:
        rows = [
            candidate("alpha", "canonical_to_apocrypha", "A", "B", "C"),
            candidate("alpha", "canonical_to_apocrypha", "A", "B", "C"),
            candidate("alpha", "canonical_to_apocrypha", "D", "E", "F"),
        ]

        self.assertEqual(sample_refs(rows), "A->B->C; D->E->F")

    def test_summarize_term_shuffled_reports_bh_q_counts(self) -> None:
        rows = [
            {
                "normalized_term": "alpha",
                "observed_gt_sample_max": "True",
                "samples": "300",
                "p_ge": "0.01",
                "q_ge": "0.04",
            },
            {
                "normalized_term": "beta",
                "observed_gt_sample_max": "False",
                "samples": "300",
                "p_ge": "0.04",
                "q_ge": "0.08",
            },
        ]

        summary = summarize_term_shuffled(rows)

        self.assertEqual(summary["observed_gt_sample_max"], 1)
        self.assertEqual(summary["p_le_0_05"], 2)
        self.assertEqual(summary["q_le_0_05"], 1)
        self.assertEqual(summary["min_q"], 0.04)
        self.assertEqual(summary["samples"], "300")

    def test_manifest_args_converts_paths(self) -> None:
        args = argparse.Namespace(candidates=Path("reports/candidates.csv"), sample_count=10)

        self.assertEqual(
            manifest_args(args),
            {"candidates": "reports/candidates.csv", "sample_count": 10},
        )

    def test_display_summary_term_adds_transliteration_and_english_gloss(self) -> None:
        rendered = display_summary_term({"normalized_term": "ישוע", "concepts": "Yeshua"})

        self.assertEqual(rendered, "`ישוע` (Yeshua; English: Yeshua)")

    def test_writers_do_not_rewrite_unchanged_content(self) -> None:
        with self.subTest("csv"):
            with tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp) / "term_review.csv"
                rows = [{"rank": 1, **{field: "" for field in FIELDNAMES if field != "rank"}}]
                write_csv(out, rows)
                first_mtime_ns = out.stat().st_mtime_ns
                time.sleep(0.01)
                write_csv(out, rows)
                self.assertEqual(out.stat().st_mtime_ns, first_mtime_ns)

        with self.subTest("manifest"):
            with tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp) / "manifest.json"
                args = argparse.Namespace(
                    candidates=Path("candidates.csv"),
                    context=Path("context.csv"),
                    controls=Path("controls.csv"),
                    shuffled_summary=Path("shuffled.csv"),
                    term_shuffled_summary=Path("term_shuffled.csv"),
                    out=Path("out.csv"),
                    markdown_out=Path("out.md"),
                    manifest_out=out,
                )
                rows = [{"observed_gt_all_controls": "True"}]
                write_manifest(out, rows, {}, {}, args, time.perf_counter())
                first_payload = json.loads(out.read_text(encoding="utf-8"))
                first_mtime_ns = out.stat().st_mtime_ns
                time.sleep(0.01)
                write_manifest(out, rows, {}, {}, args, time.perf_counter())
                second_payload = json.loads(out.read_text(encoding="utf-8"))
                self.assertEqual(second_payload, first_payload)
                self.assertEqual(out.stat().st_mtime_ns, first_mtime_ns)

        with self.subTest("manifest_non_object_cache"):
            with tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp) / "manifest.json"
                out.write_text("[]", encoding="utf-8")
                args = argparse.Namespace(
                    candidates=Path("candidates.csv"),
                    context=Path("context.csv"),
                    controls=Path("controls.csv"),
                    shuffled_summary=Path("shuffled.csv"),
                    term_shuffled_summary=Path("term_shuffled.csv"),
                    out=Path("out.csv"),
                    markdown_out=Path("out.md"),
                    manifest_out=out,
                )
                rows = [{"observed_gt_all_controls": "True"}]

                write_manifest(out, rows, {}, {}, args, time.perf_counter())

                payload = json.loads(out.read_text(encoding="utf-8"))
                self.assertEqual(payload["tool"], "summarize_kjv_apocrypha_bridge_terms")
                self.assertEqual(payload["term_rows"], 1)


def candidate(
    term: str,
    bridge_type: str,
    start_ref: str,
    center_ref: str,
    end_ref: str,
) -> dict[str, str]:
    return {
        "normalized_term": term,
        "term_ids": f"eng_{term}",
        "concepts": term.title(),
        "categories": "test",
        "bridge_type": bridge_type,
        "start_ref": start_ref,
        "center_ref": center_ref,
        "end_ref": end_ref,
    }


def context_row(term: str, bucket: str) -> dict[str, str]:
    return {"normalized_term": term, "context_bucket": bucket}


def control(label: str, term: str, rows: int) -> dict[str, str]:
    return {"control_label": label, "normalized_term": term, "bridge_rows": str(rows)}
