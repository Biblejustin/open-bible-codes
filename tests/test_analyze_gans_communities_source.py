import tempfile
import unittest
from pathlib import Path

from scripts import analyze_gans_communities_source as gans


SAMPLE_TEXT = """Patterns of Equidistant Letters Sequence Pairs in Genesis
The personality names and appellations are taken without modification from WRR lists 1 and 2.
To obtain the list used for the experiment, simply add these prefixes l h q and tlhq and keep 5≤d≤8.
In addition, delete all personality names / appellations that begin with “ybr”.
An additional experiment was produced by using the additional prefix qq. It was not in conformity with WRR.
Trace word 1 indicates source one.
Trace word 2 indicates source two.
Trace word 3 is defined for each community.

3. The Data
         Trace 1         Personality names/appellations       Communities of birth/death (and trace)
         Trace 2                   from WRR
 1.   e0032e0044                     name one                     (bf0351u000000n) towna
      e0294e0294aa                                                (di0405u000000s) townb
 2.   e0071e0078                                -
      e0313e0313aa                                                d(1) townb
4. References
"""


class GansCommunitiesSourceTests(unittest.TestCase):
    def test_parse_records_counts_explicit_and_reused_rows(self) -> None:
        records = gans.parse_records(SAMPLE_TEXT)
        community_rows = gans.community_rows_from_records(records)

        self.assertEqual([record.record_index for record in records], [1, 2])
        self.assertEqual(records[0].trace1, "e0032e0044")
        self.assertEqual(records[0].trace2, "e0294e0294aa")
        self.assertEqual(records[0].explicit_community_rows, 2)
        self.assertEqual(records[1].reused_community_rows, 1)
        self.assertTrue(records[1].has_no_personality_marker)
        self.assertEqual(len(community_rows), 3)
        self.assertEqual(community_rows[0]["row_type"], "explicit")
        self.assertEqual(community_rows[0]["trace_code"], "bf0351u000000n")
        self.assertEqual(community_rows[0]["community"], "towna")
        self.assertEqual(community_rows[2]["row_type"], "reuse")
        self.assertEqual(community_rows[2]["reuse_prefix"], "d")
        self.assertEqual(community_rows[2]["reuse_record_index"], "1")

    def test_protocol_anchors_find_declared_rules(self) -> None:
        anchors = gans.protocol_anchors(SAMPLE_TEXT)

        self.assertEqual({row["status"] for row in anchors}, {"found"})

    def test_main_writes_source_shape_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.pdf"
            source.write_bytes(SAMPLE_TEXT.encode("utf-8"))

            original_extract = gans.extract_pdf_text
            try:
                gans.extract_pdf_text = lambda path: SAMPLE_TEXT  # type: ignore[assignment]
                rc = gans.main(
                    [
                        "--source",
                        str(source),
                        "--out",
                        str(root / "records.csv"),
                        "--communities-out",
                        str(root / "communities.csv"),
                        "--summary-out",
                        str(root / "summary.csv"),
                        "--anchors-out",
                        str(root / "anchors.csv"),
                        "--markdown-out",
                        str(root / "audit.md"),
                        "--manifest-out",
                        str(root / "manifest.json"),
                    ]
                )
            finally:
                gans.extract_pdf_text = original_extract  # type: ignore[assignment]

            self.assertEqual(rc, 0)
            markdown = (root / "audit.md").read_text(encoding="utf-8")
            self.assertIn("source-shape audit only", markdown)
            self.assertIn("data records | 2", markdown)
            self.assertIn("machine community rows extracted | 3", markdown)
            self.assertIn("not a claim-ready replication", markdown)
            self.assertTrue((root / "communities.csv").exists())
            self.assertTrue((root / "manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
