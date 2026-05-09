import unittest

from scripts.analyze_extension_context_review import (
    context_read,
    exact_center_rows,
    letter_roles,
    overlap_key,
    promotion_gate,
    rows_with_controls,
    strict_cross_corpus_overlap_rows,
    surface_context_key,
)


class ExtensionContextReviewTests(unittest.TestCase):
    def test_overlap_key_uses_strict_extension_fields(self) -> None:
        row = {
            "normalized_term": "υιοσ",
            "skip": "-4",
            "direction": "backward",
            "extension_type": "term_plus_after",
            "extended_sequence": "υιοστησ",
            "matched_normalized": "υιοστησ",
        }

        self.assertEqual(
            overlap_key(row),
            "υιοσ|-4|backward|term_plus_after|υιοστησ|υιοστησ",
        )

    def test_strict_cross_corpus_overlap_rows_dedupes_per_corpus(self) -> None:
        rows = [
            row("TR_NT", "υιοσ", "υιοστησ"),
            row("TR_NT", "υιοσ", "υιοστησ"),
            row("SBLGNT", "υιοσ", "υιοστησ"),
            row("SBLGNT", "θεοσ", "εισθεοσ"),
        ]

        selected = strict_cross_corpus_overlap_rows(rows)

        self.assertEqual([item["corpus"] for item in selected], ["TR_NT", "SBLGNT"])
        self.assertTrue(all(item["overlap_key"].startswith("υιοσ|-4") for item in selected))

    def test_exact_center_rows_filter_and_dedupe(self) -> None:
        rows = [
            row("SBLGNT", "αιμα", "ναιμανο"),
            row("SBLGNT", "αιμα", "ναιμανο"),
            row("TR_NT", "δοξα", "δοξανωσ"),
            row("SBLGNT", "υιοσ", "ουουιοσ"),
        ]
        for index, item in enumerate(rows, start=1):
            item.update(
                {
                    "term": item["normalized_term"],
                    "start_offset": str(index),
                    "end_offset": str(index + 20),
                    "center_offset": str(index + 10),
                }
            )
        surface_context = {
            surface_context_key(rows[0]): {"center_exact": "True"},
            surface_context_key(rows[1]): {"center_exact": "True"},
            surface_context_key(rows[2]): {"center_exact": "True"},
            surface_context_key(rows[3]): {"center_exact": "False"},
        }

        selected = exact_center_rows(rows, surface_context, dedupe=True)

        self.assertEqual([item["normalized_term"] for item in selected], ["αιμα", "δοξα"])
        self.assertTrue(all(item["overlap_key"] for item in selected))

    def test_rows_with_controls_filters_source_only_rows(self) -> None:
        rows = [
            row("SBLGNT", "αιμα", "ναιμανο"),
            row("SBLGNT", "δοξα", "δοξανωσ"),
            row("TR_NT", "δοξα", "δοξανωσ"),
        ]
        for item in rows:
            item["overlap_key"] = overlap_key(item)
        controls = {
            ("SBLGNT", rows[1]["overlap_key"]): {"combined_min_q": "0.000999"},
            ("TR_NT", rows[2]["overlap_key"]): {"combined_min_q": "0.000999"},
        }

        selected = rows_with_controls(rows, controls)

        self.assertEqual(
            [(item["corpus"], item["normalized_term"]) for item in selected],
            [("SBLGNT", "δοξα"), ("TR_NT", "δοξα")],
        )

    def test_context_read_prioritizes_surface_phrase(self) -> None:
        self.assertEqual(
            context_read(True, True, True),
            "matched phrase appears as surface text in extension span",
        )
        self.assertEqual(
            context_read(True, False, False),
            "base normalized string appears in center verse surface text",
        )
        self.assertEqual(
            context_read(False, False, False),
            "ELS-only at hit span; matched phrase appears elsewhere in corpus",
        )

    def test_letter_roles_mark_term_and_extension_segments(self) -> None:
        self.assertEqual(
            letter_roles(
                sequence="υιοστησ",
                normalized_term="υιοσ",
                extension_type="term_plus_after",
            ),
            ["term", "term", "term", "term", "after", "after", "after"],
        )
        self.assertEqual(
            letter_roles(
                sequence="εισθεοσ",
                normalized_term="θεοσ",
                extension_type="before_plus_term",
            ),
            ["before", "before", "before", "term", "term", "term", "term"],
        )
        self.assertEqual(
            letter_roles(
                sequence="ηοναοσο",
                normalized_term="ναοσ",
                extension_type="before_plus_term_plus_after",
            ),
            ["before", "before", "term", "term", "term", "term", "after"],
        )

    def test_surface_context_key_matches_extension_join_fields(self) -> None:
        row_data = row("TR_NT", "υιοσ", "υιοστησ")
        row_data.update(
            {
                "term": "υιος",
                "skip": "-4",
                "start_offset": "10",
                "end_offset": "2",
                "center_offset": "6",
            }
        )

        self.assertEqual(
            surface_context_key(row_data),
            ("TR_NT", "υιος", "υιοσ", "-4", "10", "2", "6"),
        )

    def test_promotion_gate_prioritizes_center_exact(self) -> None:
        self.assertEqual(
            promotion_gate({"center_exact": "True", "center_same_category": "True"}),
            "promote_exact_center",
        )
        self.assertEqual(
            promotion_gate({"center_same_concept": "True"}),
            "promote_same_concept_center",
        )
        self.assertEqual(
            promotion_gate({"center_same_category": "True"}),
            "hold_same_category_only",
        )
        self.assertEqual(promotion_gate({}), "hold_no_surface_context")


def row(corpus: str, term: str, extension: str) -> dict[str, str]:
    return {
        "corpus": corpus,
        "normalized_term": term,
        "skip": "-4",
        "direction": "backward",
        "extension_type": "term_plus_after",
        "extended_sequence": extension,
        "matched_normalized": extension,
    }


if __name__ == "__main__":
    unittest.main()
