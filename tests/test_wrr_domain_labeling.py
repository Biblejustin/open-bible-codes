import unittest

from scripts.analyze_wrr_domain_labeling import (
    DomainHit,
    DomainTerm,
    build_assignment_rows,
    hit_offsets,
    label_hits,
    summarize_terms,
)


class WrrDomainLabelingTests(unittest.TestCase):
    def test_hit_offsets_follow_signed_skip(self) -> None:
        self.assertEqual(hit_offsets(20, -3, 4), (20, 17, 14, 11))

    def test_label_hits_marks_undefined_and_defined_domains(self) -> None:
        hits = [
            DomainHit((20, 30, 40), 10, 20, 40),
            DomainHit((25, 35), 5, 25, 35),
        ]

        assignments = label_hits(hits, text_length=100)

        self.assertEqual(
            [assignment.status for assignment in assignments],
            ["undefined", "defined"],
        )
        self.assertEqual(assignments[0].reason, "blocked_by_inner_shorter_skip")
        self.assertEqual(assignments[1].domain_start, 0)
        self.assertEqual(assignments[1].domain_end, 100)

    def test_assignment_and_summary_rows_report_domain_counts(self) -> None:
        term = DomainTerm("term_1", "Concept", "wrr_appellation", "TERM", "TERM")
        hits = [
            DomainHit((20, 30, 40), 10, 20, 40),
            DomainHit((25, 35), 5, 25, 35),
        ]
        assignments = label_hits(hits, text_length=100)

        assignment_rows = build_assignment_rows(
            "TEST",
            [term],
            {"TERM": hits},
            {"TERM": assignments},
        )
        summary_rows = summarize_terms("TEST", [term], {"TERM": assignments})

        self.assertEqual(len(assignment_rows), 2)
        self.assertEqual(assignment_rows[0]["domain_status"], "undefined")
        self.assertEqual(
            assignment_rows[0]["domain_reason"],
            "blocked_by_inner_shorter_skip",
        )
        self.assertEqual(assignment_rows[1]["domain_length"], 100)
        self.assertEqual(summary_rows[0]["hit_count"], 2)
        self.assertEqual(summary_rows[0]["defined_domains"], 1)
        self.assertEqual(summary_rows[0]["undefined_domains"], 1)
        self.assertEqual(summary_rows[0]["blocked_by_inner_shorter_skip"], 1)
        self.assertEqual(summary_rows[0]["ambiguous_enclosing_shorter_skip"], 0)
        self.assertEqual(summary_rows[0]["read"], "mixed defined and undefined domains")


if __name__ == "__main__":
    unittest.main()
