import unittest

from scripts.import_wrr_terms import clean_wrr_text, parse_wrr_records, term_rows


class ImportWrrTermsTests(unittest.TestCase):
    def test_parse_wrr_records_skips_leading_comment_tokens(self) -> None:
        records = parse_wrr_records(
            "# WRR second list 2 1 RBYABRHM HRABD /K/X$WN 1 0 ABRHM 3 2 A B C /A/NYSN /B/AYR"
        )

        self.assertEqual(len(records), 3)
        self.assertEqual(records[0].appellations, ("RBYABRHM", "HRABD"))
        self.assertEqual(records[0].dates, ("/K/X$WN",))
        self.assertEqual(records[1].dates, ())
        self.assertEqual(records[2].appellations, ("A", "B", "C"))
        self.assertEqual(records[2].dates, ("/A/NYSN", "/B/AYR"))

    def test_term_rows_drop_undated_records_by_default(self) -> None:
        records = parse_wrr_records("1 1 APP /A/NYSN 1 0 NODATE")

        rows = term_rows(records, list_label="wrr2", language="michigan", source_note="source")

        self.assertEqual([row["term_id"] for row in rows], ["wrr2_01_app_01", "wrr2_01_date_01"])
        self.assertEqual(rows[0]["category"], "wrr_appellation")
        self.assertEqual(rows[1]["category"], "wrr_date")

    def test_term_rows_can_keep_undated_appellations(self) -> None:
        records = parse_wrr_records("1 0 NODATE")

        rows = term_rows(
            records,
            list_label="wrr2",
            language="michigan",
            source_note="source",
            include_undated=True,
        )

        self.assertEqual([row["term_id"] for row in rows], ["wrr2_01_app_01"])

    def test_parse_wrr_records_ignores_inline_note_marker_and_trailing_note(self) -> None:
        records = parse_wrr_records("1 1 APP /A/NYSN [See note] Note: prose not data 9 9 BAD")

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].appellations, ("APP",))
        self.assertEqual(records[0].dates, ("/A/NYSN",))

    def test_clean_wrr_text_removes_known_annotations(self) -> None:
        self.assertEqual(clean_wrr_text("1 1 APP DATE [See note] Note: trailing").strip(), "1 1 APP DATE")


if __name__ == "__main__":
    unittest.main()
