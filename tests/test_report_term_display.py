import re
import unittest
from pathlib import Path


REPORT_PATHS = [
    Path("docs/FINAL_REPORT.md"),
    Path("docs/FINAL_REPORT_DRAFT.md"),
    Path("docs/FINAL_REPORT_HIGHLIGHTS.md"),
    Path("docs/ALL_CODES_FOLLOWUP_REVIEW.md"),
    Path("docs/ALL_CODES_COMPOUND_EXTENSION_CONTROLS.md"),
    Path("docs/ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_CONTROLS.md"),
    Path("docs/APOCRYPHA_BRIDGE_CONTEXT.md"),
    Path("docs/CONSOLIDATED_FINDINGS.md"),
    Path("docs/CRD_CENTER_WORD_SELF_VS_CONCEPT_FINDINGS.md"),
    Path("docs/CRD_CENTER_WORD_VERSION_PRESENCE_FINDINGS.md"),
    Path("docs/CRD_CONCEPT_SURFACE_BROAD_SCREENING_FINDINGS.md"),
    Path("docs/CRD_REPORT.md"),
    Path("docs/CRD_SELF_SURFACE_BROAD_SCREENING_FINDINGS.md"),
    Path("docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_REPORT.md"),
    Path("docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md"),
    Path("docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_ORIGINAL_LANGUAGE_FINDINGS.md"),
    Path("docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_ORIGINAL_LANGUAGE_REVIEW_PACKET.md"),
    Path("docs/GREEK_EXPANDED_SURFACE_FOLLOWUP_REPORT.md"),
    Path("docs/HEBREW_VERSION_PRESENCE_COMPARISON.md"),
]


class ReportTermDisplayTests(unittest.TestCase):
    def test_original_language_code_terms_include_english_gloss_nearby(self) -> None:
        pattern = re.compile(r"`([^`]*[\u0590-\u05ff\u0370-\u03ff\u1f00-\u1fff][^`]*)`")
        for path in REPORT_PATHS:
            text = path.read_text(encoding="utf-8")
            for match in pattern.finditer(text):
                with self.subTest(path=str(path), term=match.group(1)):
                    nearby = text[match.end() : match.end() + 140]
                    self.assertIn("English:", nearby)


if __name__ == "__main__":
    unittest.main()
