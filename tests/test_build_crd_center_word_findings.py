from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.build_crd_center_word_findings import main


class BuildCrdCenterWordFindingsTests(unittest.TestCase):
    def test_builds_tracked_findings_with_display_terms(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self_hits = root / "self_hits.csv"
            concept_hits = root / "concept_hits.csv"
            self_summary = root / "self_summary.csv"
            concept_summary = root / "concept_summary.csv"
            presence = root / "presence.csv"
            self_vs_concept = root / "self_vs_concept.md"
            version_presence = root / "version_presence.md"

            hit_text = "\n".join(
                [
                    "hit_id,term_id,term,concept,category,language,corpus,corpus_class,classifier_mode,is_relevant,relevance_type,surface_match_scope,matched_surface_keyword,matched_normalized_surface_keyword,confidence,skip,direction,start_ref,center_ref,end_ref,center_word,center_normalized_word,center_verse_text,span_text",
                    "h1,yhwh_h,יהוה,YHWH,divine,hebrew,MT_WLC,bible,deterministic,true,surface_keyword_match,center_word,יהוה,יהוה,,3,forward,Gen 1:1,Gen 1:1,Gen 1:1,יהוה,יהוה,verse,span",
                    "h1_alias,yhwh_alt_h,יהוה,YHWH Alt,divine,hebrew,MT_WLC,bible,deterministic,true,surface_keyword_match,center_word,יהוה,יהוה,,3,forward,Gen 1:1,Gen 1:1,Gen 1:1,יהוה,יהוה,verse,span",
                    "h2,wisdom_g,σοφια,Wisdom,wisdom,greek,SBLGNT,bible,deterministic,true,surface_keyword_match,center_word,σοφια,σοφια,,4,forward,Rev 1:1,Rev 1:1,Rev 1:1,σοφια,σοφια,verse,span",
                ]
            )
            self_hits.write_text(hit_text + "\n", encoding="utf-8")
            concept_hits.write_text(hit_text + "\n", encoding="utf-8")
            self_summary.write_text(
                "\n".join(
                    [
                        "classifier_mode,term_id,term,language,surface_match_scope,bible_max_density,bible_max_corpus,secular_max_density,secular_max_corpus,ratio,exceeds_secular_max",
                        "deterministic,yhwh_h,יהוה,hebrew,center_word,2,MT_WLC,0,CTRL,,true",
                        "deterministic,wisdom_g,σοφια,greek,center_word,3,SBLGNT,1,CTRL,3,true",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            concept_summary.write_text(
                "\n".join(
                    [
                        "classifier_mode,term_id,term,language,surface_match_scope,bible_max_density,bible_max_corpus,secular_max_density,secular_max_corpus,ratio,exceeds_secular_max",
                        "deterministic,yhwh_h,יהוה,hebrew,center_word,2,MT_WLC,0,CTRL,,true",
                        "deterministic,wisdom_g,σοφια,greek,center_word,3,SBLGNT,2,CTRL2,1.5,true",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            presence.write_text(
                "\n".join(
                    [
                        "term_id,term,concept,category,language,center_word_rows,corpus_count,corpora,center_refs_sample,bible_max_corpus,bible_max_density,secular_max_corpus,secular_max_density,ratio,exceeds_secular_max",
                        "yhwh_h,יהוה,YHWH,divine,hebrew,1,1,MT_WLC,MT_WLC:Gen 1:1,MT_WLC,2,CTRL,0,,true",
                        "yhwh_alt_h,יהוה,YHWH Alt,divine,hebrew,2,1,MT_WLC,MT_WLC:Exod 3:1,MT_WLC,4,CTRL,0,,true",
                        "wisdom_g,σοφια,Wisdom,wisdom,greek,1,1,SBLGNT,SBLGNT:Rev 1:1,SBLGNT,3,CTRL,1,3,true",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            result = main(
                [
                    "--self-hits",
                    str(self_hits),
                    "--concept-hits",
                    str(concept_hits),
                    "--self-summary",
                    str(self_summary),
                    "--concept-summary",
                    str(concept_summary),
                    "--self-presence",
                    str(presence),
                    "--self-vs-concept-out",
                    str(self_vs_concept),
                    "--version-presence-out",
                    str(version_presence),
                ]
            )

            self.assertEqual(result, 0)
            comparison_text = self_vs_concept.read_text(encoding="utf-8")
            self.assertIn("- matching row key set: true", comparison_text)
            self.assertIn("`σοφια` (sophia; English: Wisdom)<br>`wisdom_g`", comparison_text)
            presence_text = version_presence.read_text(encoding="utf-8")
            self.assertIn("`יהוה` (YHWH; English: YHWH)<br>`yhwh_h`", presence_text)
            self.assertIn("- distinct normalized surface forms: 2", presence_text)
            self.assertIn("- distinct normalized surface hit paths: 2", presence_text)
            self.assertIn("## Strongest Distinct Surface Forms", presence_text)
            self.assertIn("`יהוה` (YHWH; English: YHWH)<br>`yhwh_alt_h, yhwh_h`", presence_text)
            self.assertIn("| `יהוה` (YHWH; English: YHWH)<br>`yhwh_alt_h, yhwh_h` | hebrew | 2 | 1 |", presence_text)
            self.assertIn("`σοφια` (sophia; English: Wisdom)<br>`wisdom_g`", presence_text)


if __name__ == "__main__":
    unittest.main()
