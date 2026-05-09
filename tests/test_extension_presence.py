import unittest

from scripts.analyze_extension_presence import (
    complete_corpus_order,
    pattern_presence_rows,
    presence_pattern,
    read_label,
    selected_rows,
)


class ExtensionPresenceTests(unittest.TestCase):
    def test_presence_rows_group_by_exact_extension_key(self) -> None:
        rows = [
            row("TR_NT", "δοξα", "δοξανωσ", score="3211"),
            row("BYZ_NT", "δοξα", "δοξανωσ", score="3211"),
            row("TCG_NT", "δοξα", "δοξανωσ", score="3211"),
            row("SBLGNT", "δοξα", "δοξανωσ", score="3211"),
            row("SBLGNT", "υιοσ", "ουουιοσ", score="3214"),
        ]

        summary = pattern_presence_rows(
            selected_rows(rows, surface_context={}, require_center_exact=False, dedupe=True),
            ["TR_NT", "BYZ_NT", "TCG_NT", "SBLGNT"],
        )

        self.assertEqual(summary[0]["normalized_term"], "δοξα")
        self.assertEqual(summary[0]["present_corpora"], "TR_NT,BYZ_NT,TCG_NT,SBLGNT")
        self.assertEqual(summary[0]["presence_pattern"], "1111")
        self.assertEqual(summary[0]["scope"], "all_sources")
        self.assertEqual(summary[1]["normalized_term"], "υιοσ")
        self.assertEqual(summary[1]["present_corpora"], "SBLGNT")
        self.assertEqual(summary[1]["presence_pattern"], "0001")
        self.assertEqual(summary[1]["scope"], "source_only")

    def test_selected_rows_can_require_center_exact_and_dedupe(self) -> None:
        rows = [
            row("TR_NT", "δοξα", "δοξανωσ", start="1", end="85", center="43"),
            row("TR_NT", "δοξα", "δοξανωσ", start="1", end="85", center="43"),
            row("SBLGNT", "υιοσ", "ουουιοσ", start="3", end="78", center="41"),
        ]
        surface_context = {
            ("TR_NT", "δοξα", "δοξα", "21", "1", "85", "43"): {
                "center_exact": "True"
            },
            ("SBLGNT", "υιοσ", "υιοσ", "21", "3", "78", "41"): {
                "center_exact": "False"
            },
        }

        selected = selected_rows(
            rows,
            surface_context=surface_context,
            require_center_exact=True,
            dedupe=True,
        )

        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0]["corpus"], "TR_NT")
        self.assertEqual(selected[0]["overlap_key"], "δοξα|21|forward|term_plus_after|δοξανωσ|δοξανωσ")

    def test_corpus_order_and_read_labels(self) -> None:
        rows = [row("TCG_NT", "δοξα", "δοξανωσ"), row("EXTRA", "δοξα", "δοξανωσ")]

        self.assertEqual(
            complete_corpus_order(["TR_NT", "TCG_NT"], rows),
            ["TR_NT", "TCG_NT", "EXTRA"],
        )
        self.assertEqual(presence_pattern(["TCG_NT"], ["TR_NT", "TCG_NT"]), "01")
        self.assertEqual(
            read_label(["BYZ_NT", "TCG_NT"], ["TR_NT", "BYZ_NT", "TCG_NT", "SBLGNT"]),
            "related Byzantine-source pair; inspect as source-family pattern",
        )


def row(
    corpus: str,
    term: str,
    extension: str,
    *,
    score: str = "100",
    start: str = "10",
    end: str = "94",
    center: str = "52",
) -> dict[str, str]:
    return {
        "corpus": corpus,
        "term": term,
        "normalized_term": term,
        "skip": "21",
        "direction": "forward",
        "extension_type": "term_plus_after",
        "extension_length": "3",
        "extended_sequence": extension,
        "matched_normalized": extension,
        "extension_score": score,
        "matched_refs": "JHN 1:14",
        "center_ref": "2TH 3:1",
        "start_offset": start,
        "end_offset": end,
        "center_offset": center,
    }


if __name__ == "__main__":
    unittest.main()
