import csv
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import build_wrr_source_row_crop_packet as packet


class WrrSourceRowCropPacketTests(unittest.TestCase):
    def test_build_packet_rows_records_manual_crop_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manual_dir = root / "manual"
            manual_dir.mkdir()
            (manual_dir / "wrr_table2_row01.png").write_bytes(b"fake")
            args = args_for(root, manual_crop_dir=manual_dir)
            rows = packet.build_packet_rows(
                [row_checklist("1", "01", "2", "2")],
                {1: (10.0, 30.0)},
                args,
            )

            self.assertEqual(rows[0]["manual_crop_count"], 1)
            self.assertIn("wrr_table2_row01.png", rows[0]["manual_crop_paths"])
            self.assertEqual(rows[0]["crop_status"], "pending_write")
            self.assertIn("Crops are review aids only", rows[0]["no_input_boundary"])

    def test_write_crops_clamps_to_image_bounds(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "page.png"
            Image.new("RGB", (100, 80), "white").save(image)
            args = args_for(root, image=image, x_min=0, x_max=120, padding_y=4)
            rows = packet.build_packet_rows(
                [row_checklist("1", "01", "1", "1")],
                {1: (-5.0, 120.0)},
                args,
            )

            packet.write_crops(rows, args)

            crop = Path(str(rows[0]["crop_path"]))
            self.assertTrue(crop.exists())
            self.assertEqual(rows[0]["crop_status"], "written_review_aid_only")
            self.assertEqual(Image.open(crop).size, (100, 80))

    def test_write_contact_sheet_builds_local_review_image(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "page.png"
            Image.new("RGB", (100, 80), "white").save(image)
            args = args_for(root, image=image, x_min=0, x_max=100, padding_y=4)
            rows = packet.build_packet_rows(
                [row_checklist("1", "01", "1", "1")],
                {1: (20.0, 40.0)},
                args,
            )
            packet.write_crops(rows, args)

            summary = packet.write_contact_sheet(rows, args)

            self.assertTrue(args.contact_sheet_out.exists())
            self.assertEqual(summary["contact_sheet_rows"], 1)
            self.assertGreater(summary["contact_sheet_width"], 100)
            self.assertGreater(summary["contact_sheet_height"], 20)

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            checklist = root / "rows.csv"
            tsv = root / "rows.tsv"
            image = root / "page.png"
            out = root / "packet.csv"
            summary = root / "summary.csv"
            md = root / "packet.md"
            contact_sheet = root / "contact.png"
            contact_md = root / "contact.md"
            manifest = root / "manifest.json"
            Image.new("RGB", (120, 120), "white").save(image)
            write_csv(checklist, [row_checklist("1", "01", "1", "1")])
            write_tsv(tsv)

            rc = packet.main(
                [
                    "--row-checklist",
                    str(checklist),
                    "--tsv",
                    str(tsv),
                    "--image",
                    str(image),
                    "--crop-dir",
                    str(root / "crops"),
                    "--manual-crop-dir",
                    str(root / "manual"),
                    "--x-min",
                    "0",
                    "--x-max",
                    "120",
                    "--out",
                    str(out),
                    "--summary-out",
                    str(summary),
                    "--markdown-out",
                    str(md),
                    "--contact-sheet-out",
                    str(contact_sheet),
                    "--contact-sheet-markdown-out",
                    str(contact_md),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertEqual(len(list(csv.DictReader(out.open(encoding="utf-8")))), 1)
            self.assertIn("WRR Source Row Crop Packet", md.read_text(encoding="utf-8"))
            self.assertTrue(contact_sheet.exists())
            self.assertIn(
                "WRR Source Row Crop Contact Sheet",
                contact_md.read_text(encoding="utf-8"),
            )
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)
            self.assertEqual(payload["summary"]["auto_crops_available"], 1)
            self.assertEqual(payload["contact_sheet"]["contact_sheet_rows"], 1)


def args_for(
    root: Path,
    *,
    image: Path | None = None,
    manual_crop_dir: Path | None = None,
    x_min: int = 0,
    x_max: int = 100,
    padding_y: int = 2,
):
    return type(
        "Args",
        (),
        {
            "image": image or (root / "page.png"),
            "crop_dir": root / "crops",
            "manual_crop_dir": manual_crop_dir or (root / "manual"),
            "contact_sheet_out": root / "contact.png",
            "x_min": x_min,
            "x_max": x_max,
            "padding_y": padding_y,
        },
    )()


def row_checklist(
    row_rank: str, row_number: str, action_terms: str, frontier_pairs: str
) -> dict[str, str]:
    return {
        "run_label": "test",
        "row_rank": row_rank,
        "row_number": row_number,
        "concept": f"WRR2 {row_number}",
        "action_terms": action_terms,
        "frontier_pairs": frontier_pairs,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_tsv(path: Path) -> None:
    rows = [
        {
            "level": "5",
            "page_num": "1",
            "block_num": "1",
            "par_num": "1",
            "line_num": "1",
            "word_num": "1",
            "left": "550",
            "top": "40",
            "width": "10",
            "height": "10",
            "conf": "99",
            "text": "1",
        }
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
