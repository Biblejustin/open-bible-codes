import csv
import tomllib
import unittest
from pathlib import Path


BIBLEGATEWAY_MANIFEST = Path("configs/biblegateway_english_versions.csv")
EBIBLE_CONTROLS = Path("configs/ebible_english_controls.csv")
PRIVATE_PROTOCOL = Path("protocols/private_english_versions.toml")
SOURCE_BASIS_AUDIT_QUEUE = Path("docs/SOURCE_BASIS_AUDIT_QUEUE.md")


class EnglishVersionManifestTests(unittest.TestCase):
    def test_biblegateway_manifest_tracks_all_current_english_rows(self) -> None:
        rows = read_rows(BIBLEGATEWAY_MANIFEST)

        self.assertEqual(len(rows), 64)
        self.assertEqual(len({row["label"] for row in rows}), len(rows))

    def test_biblegateway_manifest_has_source_basis_metadata(self) -> None:
        rows = read_rows(BIBLEGATEWAY_MANIFEST)

        for row in rows:
            with self.subTest(label=row["label"]):
                self.assertTrue(row["coverage"])
                self.assertTrue(row["ot_basis"])
                self.assertTrue(row["nt_basis"])
                self.assertTrue(row["source_family"])
                self.assertIn(row["basis_status"], {"broad_tradition", "needs_audit"})

    def test_requested_private_versions_have_local_configs_and_protocol_entries(self) -> None:
        protocol = read_toml(PRIVATE_PROTOCOL)
        argv = " ".join(protocol["steps"][0]["argv"])

        for label in ["NIV", "NLT", "MSG", "TPT"]:
            config_path = Path(f"configs/local_{label.lower()}.toml")
            config = read_toml(config_path)
            with self.subTest(label=label):
                self.assertTrue(config_path.exists())
                self.assertIn(f"{label}={config_path}", argv)
                self.assertEqual(config["language"], "english")
                self.assertEqual(
                    config["sources"][0]["path"],
                    f"../data/private/english/{label.lower()}.csv",
                )

    def test_configured_public_or_open_configs_exist(self) -> None:
        rows = read_rows(BIBLEGATEWAY_MANIFEST)

        for row in rows:
            config_path = row["config_path"]
            if not config_path:
                continue
            with self.subTest(label=row["label"]):
                self.assertTrue(Path(config_path).exists())

    def test_ebible_controls_have_source_and_license_metadata(self) -> None:
        rows = read_rows(EBIBLE_CONTROLS)

        self.assertGreaterEqual(len(rows), 30)
        for row in rows:
            with self.subTest(label=row["label"]):
                self.assertTrue(row["source_id"])
                self.assertTrue(row["source_url"].startswith("https://ebible.org/Scriptures/"))
                self.assertTrue(row["details_url"].startswith("https://ebible.org/"))
                self.assertIn("id=", row["details_url"])
                self.assertIn("eBible", row["license_label"])
                self.assertTrue(row["source_family"])
                self.assertIn(row["basis_status"], {"broad_tradition", "needs_audit"})

    def test_source_basis_audit_queue_counts_match_manifests(self) -> None:
        expected = {
            "BibleGateway English versions": count_basis_rows(read_rows(BIBLEGATEWAY_MANIFEST)),
            "eBible English controls": count_basis_rows(read_rows(EBIBLE_CONTROLS)),
        }
        observed = read_audit_queue_counts(SOURCE_BASIS_AUDIT_QUEUE)

        self.assertEqual(observed, expected)

    def test_source_basis_audit_queue_has_no_current_needs_audit_rows(self) -> None:
        rows = [*read_rows(BIBLEGATEWAY_MANIFEST), *read_rows(EBIBLE_CONTROLS)]

        self.assertEqual(
            [row["label"] for row in rows if row["basis_status"] == "needs_audit"],
            [],
        )

    def test_known_ebible_license_overrides_remain_tracked(self) -> None:
        rows = {row["label"]: row for row in read_rows(EBIBLE_CONTROLS)}

        self.assertIn("CC BY-SA 4.0", rows["PEV"]["license_label"])


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_toml(path: Path) -> dict[str, object]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def count_basis_rows(rows: list[dict[str, str]]) -> tuple[int, int, int]:
    return (
        len(rows),
        sum(row["basis_status"] == "needs_audit" for row in rows),
        sum(row["basis_status"] == "broad_tradition" for row in rows),
    )


def read_audit_queue_counts(path: Path) -> dict[str, tuple[int, int, int]]:
    counts = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| "):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if len(cells) != 4 or not cells[1].isdigit():
            continue
        counts[cells[0]] = (int(cells[1]), int(cells[2]), int(cells[3]))
    return counts


if __name__ == "__main__":
    unittest.main()
