from pathlib import Path
from tempfile import TemporaryDirectory
import csv
import unittest

from scripts.build_crd_center_word_presence import main


class BuildCrdCenterWordPresenceTests(unittest.TestCase):
    def test_builds_presence_csv_and_markdown(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            hits = root / "hits.csv"
            summary = root / "summary.csv"
            output = root / "presence.csv"
            markdown = root / "presence.md"
            hits.write_text(
                "\n".join(
                    [
                        "term_id,term,concept,category,language,corpus,center_ref",
                        "beta_g,BETA,Beta,test,greek,SBLGNT,REV 20:8",
                        "alpha_h,ALPHA,Alpha,test,hebrew,MT_WLC,GEN 1:1",
                        "alpha_h,ALPHA,Alpha,test,hebrew,UHB,GEN 1:1",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            summary.write_text(
                "\n".join(
                    [
                        "term_id,bible_max_corpus,bible_max_density,secular_max_corpus,secular_max_density,ratio,exceeds_secular_max",
                        "alpha_h,UHB,2.0,CTRL,1.0,2.0,true",
                        "beta_g,SBLGNT,3.0,CTRL,0,,true",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            result = main(
                [
                    "--center-word-hits",
                    str(hits),
                    "--summary",
                    str(summary),
                    "--output",
                    str(output),
                    "--markdown-out",
                    str(markdown),
                ]
            )

            self.assertEqual(result, 0)
            with output.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["term_id"], "alpha_h")
            self.assertEqual(rows[0]["corpus_count"], "2")
            self.assertEqual(rows[0]["corpora"], "MT_WLC;UHB")
            self.assertEqual(rows[1]["term_id"], "beta_g")
            text = markdown.read_text(encoding="utf-8")
            self.assertIn("# CRD Exact Center-Word Version Presence", text)
            self.assertIn("- term rows: 2", text)
            self.assertIn("`alpha_h`", text)


if __name__ == "__main__":
    unittest.main()
