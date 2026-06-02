import gzip
import tempfile
import unittest
from pathlib import Path

from scripts.analyze_wrr_text_source import (
    audit_text_source,
    fingerprint_source,
    sha256_bytes,
    source_paths,
)


class WrrTextSourceTests(unittest.TestCase):
    def test_source_paths_reports_invalid_toml(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "config.toml"
            config.write_text("[broken\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "invalid TOML"):
                source_paths(config)

    def test_source_paths_requires_sources_list(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "config.toml"
            config.write_text('sources = "bad"\n', encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "sources must be a list"):
                source_paths(config)

    def test_source_paths_requires_source_tables_with_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "config.toml"
            config.write_text("[[sources]]\nname = 'missing'\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "source 1 missing path"):
                source_paths(config)

    def test_fingerprint_source_hashes_raw_and_decompressed_gzip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "source.gz"
            raw = gzip.compress(b"abc")
            path.write_bytes(raw)

            row = fingerprint_source(path)

        self.assertEqual(row["raw_bytes"], len(raw))
        self.assertEqual(row["text_bytes"], 3)
        self.assertEqual(row["text_sha256"], sha256_bytes(b"abc"))

    def test_audit_text_source_fingerprints_loaded_corpus(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "genesis.gz"
            source.write_bytes(gzip.compress(b"1 1 1 BR)$YT\n"))
            config = root / "config.toml"
            config.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        'language = "michigan"',
                        "",
                        "[[sources]]",
                        'name = "Genesis"',
                        'format = "michigan_claremont"',
                        'path = "genesis.gz"',
                        'book = "Genesis"',
                        "book_number = 1",
                    ]
                ),
                encoding="utf-8",
            )

            row = audit_text_source(config)

        self.assertEqual(row["corpus_name"], "sample")
        self.assertEqual(row["source_count"], 1)
        self.assertEqual(row["source_text_sha256"], sha256_bytes(b"1 1 1 BR)$YT\n"))
        self.assertGreater(row["normalized_letters"], 0)
        self.assertEqual(row["verse_count"], 1)
        self.assertEqual(len(str(row["normalized_text_sha256"])), 64)


if __name__ == "__main__":
    unittest.main()
