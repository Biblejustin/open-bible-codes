import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_source_row_crop_packet as crop_packet
from scripts import build_wrr_source_row_crop_review_html as html_builder


class WrrSourceRowCropReviewHtmlTests(unittest.TestCase):
    def test_write_crop_review_html_uses_crop_images_without_source_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "row.png"
            image.write_bytes(b"not really png")
            rows = [crop_row("1", "06", image)]
            html_out = root / "row_review.html"
            args = argparse_like(html_out)

            summary = html_builder.write_crop_review_html(rows, args)

            text = html_out.read_text(encoding="utf-8")
            self.assertEqual(summary["html_rows"], 1)
            self.assertEqual(summary["html_crop_image_rows"], 1)
            self.assertIn("WRR2 06", text)
            self.assertNotIn("אבג", text)

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "row.png"
            image.write_bytes(b"not really png")
            packet_csv = root / "crop_packet.csv"
            html_out = root / "row_review.html"
            summary = root / "summary.csv"
            markdown = root / "row_review.md"
            manifest = root / "manifest.json"
            write_csv(packet_csv, [crop_row("1", "06", image)])

            rc = html_builder.main(
                [
                    "--crop-packet",
                    str(packet_csv),
                    "--html-out",
                    str(html_out),
                    "--summary-out",
                    str(summary),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertTrue(html_out.exists())
            self.assertIn(
                "WRR Source Row Crop Review HTML",
                markdown.read_text(encoding="utf-8"),
            )
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)
            self.assertEqual(payload["source_corrections"], 0)


def argparse_like(html_out: Path):
    class Args:
        pass

    args = Args()
    args.html_out = html_out
    return args


def crop_row(rank: str, row_number: str, image: Path) -> dict[str, str]:
    return {
        "run_label": "all_lanes_cap1000",
        "row_rank": rank,
        "row_number": row_number,
        "concept": f"WRR2 {row_number}",
        "action_terms": "4",
        "frontier_pairs": "4",
        "row_band_top": "1.00",
        "row_band_bottom": "2.00",
        "crop_left": "500",
        "crop_top": "1",
        "crop_right": "2050",
        "crop_bottom": "2",
        "crop_width": "1550",
        "crop_height": "1",
        "crop_path": str(image),
        "crop_exists": str(image.exists()).lower(),
        "crop_status": "written_review_aid_only",
        "manual_crop_count": "0",
        "manual_crop_paths": "",
        "no_input_boundary": crop_packet.NO_INPUT_BOUNDARY,
        "next_manual_action": "inspect generated crop against source row before any frontier source decision",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=crop_packet.FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
