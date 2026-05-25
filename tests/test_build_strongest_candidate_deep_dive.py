import csv
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from scripts.build_strongest_candidate_deep_dive import build_candidates, main


class StrongestCandidateDeepDiveTests(unittest.TestCase):
    def test_build_candidates_ranks_and_reads_locked_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_fixture_set(Path(tmp))

            rows = build_candidates(Namespace(**paths))

            self.assertEqual([row["candidate_id"] for row in rows], [
                "doxa_exact_center_extension",
                "all_codes_yom_yhwh_compound_extension",
                "gog_rev_20_8_centered_occurrence",
                "greek_expanded_surface_followup",
                "kjva_apocrypha_bridge_boundary",
            ])
            self.assertIn("2 sources", rows[0]["control_read"])
            self.assertIn("max all-control q 0.04", rows[0]["control_read"])
            self.assertEqual(rows[0]["decision"], "hold_after_clean_lock_extension_followup")
            self.assertIn("post-discovery review material", rows[0]["next_action"])
            self.assertIn("stricter function-word and context gates", rows[0]["next_action"])
            self.assertIn("4 exact-center paths", rows[2]["context_read"])
            self.assertIn("Prospective lock: 1 bridge row, 0/2 terms", rows[4]["control_read"])

    def test_main_writes_csv_markdown_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = write_fixture_set(root)
            out = root / "candidates.csv"
            markdown = root / "deep_dive.md"
            manifest = root / "manifest.json"

            code = main(
                [
                    "--claim-catalog",
                    str(paths["claim_catalog"]),
                    "--doxa-paired",
                    str(paths["doxa_paired"]),
                    "--doxa-context",
                    str(paths["doxa_context"]),
                    "--compound-summary",
                    str(paths["compound_summary"]),
                    "--gog-occurrences",
                    str(paths["gog_occurrences"]),
                    "--greek-expanded-controls",
                    str(paths["greek_expanded_controls"]),
                    "--greek-expanded-selected",
                    str(paths["greek_expanded_selected"]),
                    "--kjva-confirmatory",
                    str(paths["kjva_confirmatory"]),
                    "--kjva-prospective",
                    str(paths["kjva_prospective"]),
                    "--kjva-prospective-bridge",
                    str(paths["kjva_prospective_bridge"]),
                    "--out",
                    str(out),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(code, 0)
            self.assertIn("doxa_exact_center_extension", out.read_text(encoding="utf-8"))
            markdown_text = markdown.read_text(encoding="utf-8")
            self.assertIn("Strongest Candidate Deep Dive", markdown_text)
            self.assertIn("use a new clean source and stricter gates", markdown_text)
            self.assertNotIn("lock the next prospective doxa-style", markdown_text)
            self.assertIn("build_strongest_candidate_deep_dive", manifest.read_text(encoding="utf-8"))


def write_fixture_set(root: Path) -> dict[str, Path]:
    paths = {
        "claim_catalog": root / "claims.csv",
        "doxa_paired": root / "doxa_paired.csv",
        "doxa_context": root / "doxa_context.csv",
        "compound_summary": root / "compound.csv",
        "gog_occurrences": root / "gog.csv",
        "greek_expanded_controls": root / "greek_controls.csv",
        "greek_expanded_selected": root / "greek_selected.csv",
        "kjva_confirmatory": root / "kjva_confirm.csv",
        "kjva_prospective": root / "kjva_prospect.csv",
        "kjva_prospective_bridge": root / "kjva_bridge.csv",
    }
    write_csv(
        paths["claim_catalog"],
        ["claim_id", "status", "current_reproduction", "notes"],
        [
            claim("doxa_exact_center_extension", "post-discovery doxa"),
            claim("all_codes_yom_yhwh_compound_extension", "post-screen compound"),
            claim("gog_rev_20_8_centered_occurrence", "short Gog"),
            claim("greek_expanded_surface_followup", "post-screen Greek"),
            claim("kjva_apocrypha_bridge_boundary", "post-screen KJVA"),
        ],
    )
    write_csv(
        paths["doxa_paired"],
        ["corpus", "combined_min_q", "all_controls_max_q", "term_control_samples", "random_control_samples"],
        [
            {"corpus": "TR_NT", "combined_min_q": "0.001", "all_controls_max_q": "0.03", "term_control_samples": "20", "random_control_samples": "20"},
            {"corpus": "SBLGNT", "combined_min_q": "0.002", "all_controls_max_q": "0.04", "term_control_samples": "20", "random_control_samples": "20"},
        ],
    )
    write_csv(paths["doxa_context"], ["center_ref", "center_word"], [{"center_ref": "2TH 3:1", "center_word": "κυριου"}])
    write_csv(
        paths["compound_summary"],
        [
            "corpus",
            "combined_min_q",
            "all_controls_max_q",
            "term_control_samples",
            "random_control_samples",
            "overlap_corpora",
            "skip",
            "direction",
            "extended_sequence",
            "matched_refs",
        ],
        [
            {
                "corpus": "UHB",
                "combined_min_q": "0.0002",
                "all_controls_max_q": "0.005",
                "term_control_samples": "50",
                "random_control_samples": "50",
                "overlap_corpora": "UHB,MT_WLC",
                "skip": "4",
                "direction": "forward",
                "extended_sequence": "היומיהוה",
                "matched_refs": "LEV 9:4",
            }
        ],
    )
    write_csv(
        paths["gog_occurrences"],
        [
            "source_family",
            "normalized_term",
            "occurrence_type",
            "corpus",
            "exact_center_paths",
            "frequency_read",
            "center_ref",
            "center_word",
            "context_excerpt",
        ],
        [
            {
                "source_family": "gog_source_review",
                "normalized_term": "γωγ",
                "occurrence_type": "centered_self_exact_word",
                "corpus": "TR_NT",
                "exact_center_paths": "2",
                "frequency_read": "length-3 caution",
                "center_ref": "REV 20:8",
                "center_word": "Gog",
                "context_excerpt": "Gog/Magog context",
            },
            {
                "source_family": "gog_source_review",
                "normalized_term": "γωγ",
                "occurrence_type": "centered_self_exact_word",
                "corpus": "SBLGNT",
                "exact_center_paths": "2",
                "frequency_read": "length-3 caution",
                "center_ref": "Rev 20:8",
                "center_word": "Gog",
                "context_excerpt": "Gog/Magog context",
            },
        ],
    )
    write_csv(
        paths["greek_expanded_controls"],
        ["target_normalized_term", "all_source_q_value", "observed_all_source_patterns"],
        [
            {"target_normalized_term": "ισαακ", "all_source_q_value": "0.032", "observed_all_source_patterns": "1"},
            {"target_normalized_term": "τερασ", "all_source_q_value": "0.031", "observed_all_source_patterns": "1"},
        ],
    )
    write_csv(paths["greek_expanded_selected"], ["present_corpora"], [{"present_corpora": "TR_NT,SBLGNT"}])
    write_csv(
        paths["kjva_confirmatory"],
        ["q_ge", "observed_gt_sample_max"],
        [
            {"q_ge": "0.001", "observed_gt_sample_max": "True"},
            {"q_ge": "0.009", "observed_gt_sample_max": "False"},
        ],
    )
    write_csv(paths["kjva_prospective"], ["q_ge"], [{"q_ge": "0.6"}, {"q_ge": "1.0"}])
    write_csv(paths["kjva_prospective_bridge"], ["metric", "value"], [{"metric": "bridge_rows", "value": "1"}])
    return paths


def claim(claim_id: str, notes: str) -> dict[str, str]:
    return {
        "claim_id": claim_id,
        "status": "controlled_review_candidate",
        "current_reproduction": f"{claim_id} evidence",
        "notes": notes,
    }


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
