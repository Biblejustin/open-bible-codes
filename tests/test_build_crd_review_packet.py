from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.build_crd_review_packet import main


class BuildCrdReviewPacketTests(unittest.TestCase):
    def test_builds_grouped_markdown_packet(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            queue = root / "queue.csv"
            output = root / "packet.md"
            queue.write_text(
                "\n".join(
                    [
                        "selection_reason,selection_rank,term_id,term,concept,language,category,corpus,bible_max_corpus,bible_max_density,secular_max_corpus,secular_max_density,ratio,hit_id,relevance_type,surface_match_scope,matched_surface_keyword,matched_normalized_surface_keyword,skip,direction,start_ref,center_ref,end_ref,center_word,center_normalized_word,center_verse_text,span_text",
                        "top_finite_ratio,1,alpha_h,ALPHA,Alpha,hebrew,test,MT_WLC,MT_WLC,2.0,CTRL,1.0,2.0,h1,surface_keyword_match,center_word,ALPHA,alpha,7,forward,Gen 1:1,Gen 1:2,Gen 1:3,ALPHA,alpha,Center verse text,Span text",
                        "top_finite_ratio,1,alpha_h,ALPHA,Alpha,hebrew,test,UHB,MT_WLC,2.0,CTRL,1.0,2.0,h2,surface_keyword_match,center_word,ALPHA,alpha,-9,backward,Gen 2:1,Gen 2:2,Gen 2:3,ALPHA,alpha,Second center verse,Span text",
                        "bible_positive_secular_zero,1,beta_g,BETA,Beta,greek,test,SBLGNT,SBLGNT,3.0,,0,,h3,surface_keyword_match,center_word,BETA,beta,5,forward,John 1:1,John 1:2,John 1:3,BETA,beta,Greek center verse,Span text",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            result = main(
                [
                    "--queue",
                    str(queue),
                    "--output",
                    str(output),
                    "--title",
                    "Packet",
                    "--examples-per-term",
                    "1",
                ]
            )

            self.assertEqual(result, 0)
            text = output.read_text(encoding="utf-8")
            self.assertIn("# Packet", text)
            self.assertIn("- queue rows: 3", text)
            self.assertIn("- selected terms: 2", text)
            self.assertIn("### `alpha_h`", text)
            self.assertIn("### `beta_g`", text)
            self.assertIn("| MT_WLC | Gen 1:2 | 7 | forward | ALPHA | ALPHA | Gen 1:1 to Gen 1:3 |", text)
            self.assertNotIn("| UHB | Gen 2:2 |", text)


if __name__ == "__main__":
    unittest.main()
