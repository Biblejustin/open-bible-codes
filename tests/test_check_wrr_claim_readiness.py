import csv
import tempfile
import unittest
from pathlib import Path

from scripts import check_wrr_claim_readiness as check


class WrrClaimReadinessTests(unittest.TestCase):
    def test_readiness_rows_flags_current_open_statuses(self) -> None:
        rows = check.readiness_rows(
            [
                {
                    "decision_area": "Pair universe",
                    "status": "open",
                    "current_read": "pair universe open",
                    "evidence": "source-policy evidence",
                },
                {"decision_area": "D(w) skip-cap formula", "status": "open"},
                {"decision_area": "Corrected distance c(w,w')", "status": "smoke_only"},
                {
                    "decision_area": "Aggregate statistic and permutation",
                    "status": "source_locked_not_built",
                },
            ]
        )

        self.assertFalse(check.all_ready(rows))
        self.assertEqual([row["ready"] for row in rows], ["false"] * 4)
        self.assertIn("status open is not claim-ready", rows[0]["blocker"])
        self.assertEqual(rows[0]["current_read"], "pair universe open")
        self.assertEqual(rows[0]["evidence"], "source-policy evidence")

    def test_readiness_rows_accepts_locked_statuses(self) -> None:
        rows = check.readiness_rows(
            [
                {"decision_area": "Pair universe", "status": "locked"},
                {"decision_area": "D(w) skip-cap formula", "status": "source_locked"},
                {"decision_area": "Corrected distance c(w,w')", "status": "defined_full_run"},
                {
                    "decision_area": "Aggregate statistic and permutation",
                    "status": "claim_grade_ready",
                },
            ]
        )

        self.assertTrue(check.all_ready(rows))
        self.assertEqual([row["blocker"] for row in rows], [""] * 4)

    def test_main_writes_blocked_report_and_require_ready_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            status = root / "status.csv"
            out = root / "readiness.csv"
            markdown = root / "readiness.md"
            manifest = root / "manifest.json"
            write_status_rows(
                status,
                [
                    {"decision_area": "Pair universe", "status": "open"},
                    {"decision_area": "D(w) skip-cap formula", "status": "open"},
                    {"decision_area": "Corrected distance c(w,w')", "status": "smoke_only"},
                    {
                        "decision_area": "Aggregate statistic and permutation",
                        "status": "source_locked_not_built",
                    },
                ],
            )

            rc = check.main(
                [
                    "--status",
                    str(status),
                    "--out",
                    str(out),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )
            fail_rc = check.main(
                [
                    "--status",
                    str(status),
                    "--out",
                    str(out),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                    "--require-ready",
                ]
            )

            self.assertEqual(rc, 0)
            self.assertEqual(fail_rc, 1)
            text = markdown.read_text(encoding="utf-8")
            self.assertIn("Status: blocked", text)
            self.assertIn("Current read", text)
            self.assertIn("Pair universe: status open is not claim-ready", text)


def write_status_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = sorted({field for row in rows for field in row})
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
