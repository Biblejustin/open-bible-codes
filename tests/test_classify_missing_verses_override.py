import tempfile
import unittest
from pathlib import Path

from els.corpus import load_corpus
from els.critical import BlockPlacement, OmittedBlock, classify_missing_verses


class ClassifyMissingVersesOverrideTests(unittest.TestCase):
    def test_extra_deleted_refs_adds_present_ref_without_downgrade(self) -> None:
        tr, sbl = _corpora(
            [
                ("MAT 1:1", "MAT", "1", "1", "αβγ"),
                ("MAT 1:2", "MAT", "1", "2", "δεζ"),
            ],
            [
                ("Matt 1:1", "Matt", "1", "1", "αβγ"),
                ("Matt 1:2", "Matt", "1", "2", "δεζ"),
            ],
        )

        omitted = classify_missing_verses(tr, sbl, extra_deleted_refs={"MAT 1:1"})

        self.assertEqual([block.ref for block in omitted], ["MAT 1:1"])
        self.assertEqual(omitted[0].status, "explicit_deleted_ref")
        self.assertTrue(omitted[0].used_as_deletion)

    def test_deleted_blocks_override_bypasses_ref_diff(self) -> None:
        tr, sbl = _corpora(
            [("MAT 1:1", "MAT", "1", "1", "αβγ")],
            [("Matt 1:1", "Matt", "1", "1", "αβγ")],
        )
        override = [OmittedBlock("manual", 0, 2, 3, "manual", True)]

        omitted = classify_missing_verses(tr, sbl, deleted_blocks_override=override)

        self.assertIs(omitted, override)

    def test_deleted_blocks_override_accepts_block_placements(self) -> None:
        tr, sbl = _corpora(
            [("MAT 1:1", "MAT", "1", "1", "αβγ")],
            [("Matt 1:1", "Matt", "1", "1", "αβγ")],
        )
        override = [BlockPlacement("manual", 0, 2, 3, 1)]

        omitted = classify_missing_verses(tr, sbl, deleted_blocks_override=override)

        self.assertIs(omitted, override)

    def test_default_behavior_still_ref_diffs(self) -> None:
        tr, sbl = _corpora(
            [
                ("MAT 1:1", "MAT", "1", "1", "αβγ"),
                ("MAT 1:2", "MAT", "1", "2", "δεζ"),
            ],
            [("Matt 1:1", "Matt", "1", "1", "αβγ")],
        )

        omitted = classify_missing_verses(tr, sbl)

        self.assertEqual([block.ref for block in omitted], ["MAT 1:2"])
        self.assertEqual(omitted[0].status, "deleted_block")


def _corpora(tr_rows, sbl_rows):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write_csv(root / "tr.csv", tr_rows)
        _write_csv(root / "sbl.csv", sbl_rows)
        tr = load_corpus(_write_config(root, "tr", "tr.csv"))
        sbl = load_corpus(_write_config(root, "sbl", "sbl.csv"))
    return tr, sbl


def _write_csv(path: Path, rows) -> None:
    lines = ["ref,book,chapter,verse,text"]
    lines.extend(",".join(row) for row in rows)
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_config(root: Path, name: str, csv_name: str) -> Path:
    path = root / f"{name}.toml"
    path.write_text(
        "\n".join(
            [
                f'name = "{name}"',
                'language = "greek"',
                "",
                "[[sources]]",
                f'name = "{name}"',
                'format = "csv"',
                f'path = "{csv_name}"',
                'text_column = "text"',
                'ref_column = "ref"',
                'book_column = "book"',
                'chapter_column = "chapter"',
                'verse_column = "verse"',
            ]
        ),
        encoding="utf-8",
    )
    return path


if __name__ == "__main__":
    unittest.main()
