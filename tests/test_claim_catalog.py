import csv
import unittest
from pathlib import Path


CATALOG_PATH = Path("claims/claim_catalog.csv")
REQUIRED_FIELDS = {
    "claim_id",
    "claim_group",
    "source_label",
    "status",
    "language",
    "corpus_scope",
    "terms",
    "spellings_or_forms",
    "skip_or_rule",
    "layout_or_metric",
    "current_reproduction",
    "evidence",
    "notes",
}
ALLOWED_STATUSES = {
    "reproducible",
    "partially_reproducible",
    "controlled_review_candidate",
    "not_reproducible",
    "under_specified",
    "license_blocked",
}
ALLOWED_LANGUAGES = {"hebrew", "greek", "english", "michigan", "hebrew/greek", "hebrew/greek/english"}


class ClaimCatalogTests(unittest.TestCase):
    def test_claim_catalog_schema_and_ids(self) -> None:
        with CATALOG_PATH.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))

        self.assertGreater(len(rows), 0)
        self.assertGreaterEqual(set(rows[0]), REQUIRED_FIELDS)
        claim_ids = [row["claim_id"] for row in rows]
        self.assertEqual(len(claim_ids), len(set(claim_ids)))
        for row in rows:
            with self.subTest(claim_id=row["claim_id"]):
                self.assertNotIn(None, row)
                self.assertTrue(row["claim_id"].strip())
                self.assertTrue(row["claim_group"].strip())
                self.assertIn(row["status"], ALLOWED_STATUSES)
                self.assertIn(row["language"], ALLOWED_LANGUAGES)
                self.assertTrue(row["current_reproduction"].strip())
                self.assertTrue(Path(row["evidence"]).exists())

    def test_claim_catalog_keeps_core_statuses_visible(self) -> None:
        with CATALOG_PATH.open("r", encoding="utf-8", newline="") as handle:
            statuses = {row["status"] for row in csv.DictReader(handle)}

        self.assertIn("reproducible", statuses)
        self.assertIn("under_specified", statuses)
        self.assertIn("not_reproducible", statuses)

    def test_prior_art_implementation_audit_is_declared(self) -> None:
        with CATALOG_PATH.open("r", encoding="utf-8", newline="") as handle:
            rows = {row["claim_id"]: row for row in csv.DictReader(handle)}

        row = rows["amandasaurus_biblecode_prior_art"]
        self.assertEqual(row["status"], "under_specified")
        self.assertEqual(row["claim_group"], "methodology_source")
        self.assertEqual(row["evidence"], "docs/AMANDASAURUS_BIBLECODE_PRIOR_ART_AUDIT.md")

    def test_bible_codes_org_source_audit_is_declared(self) -> None:
        with CATALOG_PATH.open("r", encoding="utf-8", newline="") as handle:
            rows = {row["claim_id"]: row for row in csv.DictReader(handle)}

        expected_ids = {
            "bible_codes_org_intro_matrix",
            "bible_codes_org_pictogram_clusters",
            "bible_codes_org_authenticity_criteria",
            "bible_codes_org_prediction_claims",
            "bible_codes_org_warnings",
        }
        self.assertGreaterEqual(set(rows), expected_ids)
        for claim_id in expected_ids:
            with self.subTest(claim_id=claim_id):
                self.assertEqual(rows[claim_id]["status"], "under_specified")
                self.assertEqual(rows[claim_id]["evidence"], "docs/BIBLE_CODES_ORG_AUDIT.md")

    def test_wrr_claim_catalog_is_blocked_by_readiness_gate(self) -> None:
        with CATALOG_PATH.open("r", encoding="utf-8", newline="") as handle:
            rows = {row["claim_id"]: row for row in csv.DictReader(handle)}

        row = rows["wrr_1994_great_rabbis"]
        self.assertEqual(row["status"], "under_specified")
        self.assertEqual(row["evidence"], "docs/WRR_CLAIM_READINESS.md")
        self.assertIn("readiness gate", row["notes"])
        self.assertIn("docs/WRR_SOURCE_AUDIT.md", row["notes"])
        self.assertIn("visual triage notes do not exclude pairs automatically", row["notes"])

    def test_critical_omission_catalog_keeps_null_read_visible(self) -> None:
        with CATALOG_PATH.open("r", encoding="utf-8", newline="") as handle:
            rows = {row["claim_id"]: row for row in csv.DictReader(handle)}

        row = rows["critical_omission_breakage"]
        self.assertEqual(row["status"], "partially_reproducible")
        self.assertIn("558 broken TR hits", row["current_reproduction"])
        self.assertIn("p_ge 0.9910", row["current_reproduction"])
        self.assertIn("null median 657", row["current_reproduction"])

        doc = Path("docs/CLAIM_CATALOG.md").read_text(encoding="utf-8")
        normalized_doc = " ".join(doc.split())
        self.assertIn("558 observed broken TR hits versus null median 657", normalized_doc)
        self.assertIn("`p_ge=0.9910`", doc)


if __name__ == "__main__":
    unittest.main()
