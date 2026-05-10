import tempfile
import unittest
from pathlib import Path

from scripts import release_hygiene as hygiene


class PublicReleaseHygieneTests(unittest.TestCase):
    def test_remote_owner_accepts_biblejustin_https_remote(self) -> None:
        failures = hygiene.remote_owner_failures(
            ["origin\thttps://github.com/Biblejustin/open-bible-codes.git (fetch)"],
            owner="Biblejustin",
            repo="open-bible-codes",
        )

        self.assertEqual(failures, [])

    def test_remote_owner_accepts_biblejustin_ssh_remote(self) -> None:
        failures = hygiene.remote_owner_failures(
            ["origin\tgit@github.com:Biblejustin/open-bible-codes.git (push)"],
            owner="Biblejustin",
            repo="open-bible-codes",
        )

        self.assertEqual(failures, [])

    def test_remote_owner_rejects_forbidden_account_remote(self) -> None:
        account = "justin-" + ("sp" + "lunk")

        failures = hygiene.remote_owner_failures(
            [f"origin\tgit@github.com:{account}/open-bible-codes.git (push)"],
            owner="Biblejustin",
            repo="open-bible-codes",
        )

        self.assertTrue(any("forbidden account text" in failure for failure in failures))
        self.assertTrue(any("no remote points" in failure for failure in failures))

    def test_risky_tracked_paths_allow_reports_gitkeep_only(self) -> None:
        paths = [
            "reports/.gitkeep",
            "reports/run/output.csv",
            "reports/db/open_bible_codes.duckdb",
            "data/raw/source.xml",
            "data/study/churchages_claim_counts.csv",
            ".env",
            "docs/REPORT.md",
        ]

        self.assertEqual(
            hygiene.risky_tracked_paths(paths),
            [
                "reports/run/output.csv",
                "reports/db/open_bible_codes.duckdb",
                "data/raw/source.xml",
                ".env",
            ],
        )

    def test_secret_scan_detects_high_confidence_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "config.txt"
            token = "github_pat_" + "123456789012345678901234567890"
            path.write_text(
                "placeholder only\n"
                f"token={token}\n",
                encoding="utf-8",
            )

            hits = hygiene.scan_tracked_for_secret_patterns(root, ["config.txt"])

        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].path, "config.txt")
        self.assertEqual(hits[0].line, 2)
        self.assertEqual(hits[0].kind, "github_fine_grained_token")

    def test_secret_scan_skips_binary_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            token = ("github_pat_" + "123456789012345678901234567890").encode()
            (root / "binary.bin").write_bytes(b"\x00" + token)

            hits = hygiene.scan_tracked_for_secret_patterns(root, ["binary.bin"])

        self.assertEqual(hits, [])

    def test_forbidden_account_scan_checks_tracked_files_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "tracked.md").write_text("Biblejustin only", encoding="utf-8")
            (root / "ignored.md").write_text("justin-" + ("sp" + "lunk"), encoding="utf-8")

            hits = hygiene.scan_tracked_for_forbidden_account(root, ["tracked.md"])

        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()
