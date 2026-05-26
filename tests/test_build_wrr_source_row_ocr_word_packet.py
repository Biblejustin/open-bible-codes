import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_source_row_ocr_word_packet as packet


class WrrSourceRowOcrTokenPacketTests(unittest.TestCase):
    def test_build_token_rows_splits_name_and_date_columns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            crop_packet = root / "crop.csv"
            tsv = root / "ocr.tsv"
            write_crop_packet(crop_packet)
            write_tsv(tsv)
            args = args_for(root, crop_packet, tsv)

            rows = packet.build_token_rows(
                packet.read_csv(crop_packet),
                packet.read_tsv_words(tsv),
                args,
            )

            self.assertEqual(len(rows), 1)
            self.assertIn("שם", rows[0]["name_tokens_rtl"])
            self.assertIn("תאריך", rows[0]["date_tokens_rtl"])
            self.assertEqual(rows[0]["word_count"], 2)
            self.assertEqual(rows[0]["low_conf_word_count"], 1)
            self.assertIn("OCR words are review aids only", rows[0]["no_input_boundary"])

    def test_unbalanced_quote_tsv_token_does_not_merge_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tsv = root / "ocr.tsv"
            write_tsv_with_unbalanced_quote(tsv)

            words = packet.read_tsv_words(tsv)

            self.assertEqual([word.text for word in words], ['"bad', "next"])

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            crop_packet = root / "crop.csv"
            tsv = root / "ocr.tsv"
            out = root / "packet.csv"
            summary = root / "summary.csv"
            md = root / "packet.md"
            manifest = root / "manifest.json"
            write_crop_packet(crop_packet)
            write_tsv(tsv)

            rc = packet.main(
                [
                    "--crop-packet",
                    str(crop_packet),
                    "--tsv",
                    str(tsv),
                    "--out",
                    str(out),
                    "--summary-out",
                    str(summary),
                    "--markdown-out",
                    str(md),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertEqual(len(list(csv.DictReader(out.open(encoding="utf-8")))), 1)
            self.assertIn("WRR Source Row OCR Word Packet", md.read_text(encoding="utf-8"))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)
            self.assertEqual(payload["summary"]["source_rows"], 1)


def args_for(root: Path, crop_packet: Path, tsv: Path):
    return type(
        "Args",
        (),
        {
            "crop_packet": crop_packet,
            "tsv": tsv,
            "low_conf_threshold": 50.0,
            "out": root / "packet.csv",
            "summary_out": root / "summary.csv",
            "markdown_out": root / "packet.md",
            "manifest_out": root / "manifest.json",
        },
    )()


def write_crop_packet(path: Path) -> None:
    rows = [
        {
            "run_label": "test",
            "row_rank": "1",
            "row_number": "01",
            "concept": "WRR2 01",
            "frontier_pairs": "1",
            "row_band_top": "100",
            "row_band_bottom": "200",
            "crop_left": "500",
            "crop_right": "2050",
            "crop_path": "row01.png",
        }
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_tsv(path: Path) -> None:
    rows = [
        tsv_word("900", "120", "100", "20", "80", "שם"),
        tsv_word("1500", "130", "120", "20", "45", "תאריך"),
        tsv_word("2100", "130", "80", "20", "90", "outside"),
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def write_tsv_with_unbalanced_quote(path: Path) -> None:
    path.write_text(
        "\t".join(
            [
                "level",
                "page_num",
                "block_num",
                "par_num",
                "line_num",
                "word_num",
                "left",
                "top",
                "width",
                "height",
                "conf",
                "text",
            ]
        )
        + "\n"
        + "5\t1\t1\t1\t1\t1\t100\t100\t20\t20\t40\t\"bad\n"
        + "5\t1\t1\t1\t1\t2\t130\t100\t20\t20\t80\tnext\n",
        encoding="utf-8",
    )


def tsv_word(left: str, top: str, width: str, height: str, conf: str, text: str) -> dict[str, str]:
    return {
        "level": "5",
        "page_num": "1",
        "block_num": "1",
        "par_num": "1",
        "line_num": "1",
        "word_num": "1",
        "left": left,
        "top": top,
        "width": width,
        "height": height,
        "conf": conf,
        "text": text,
    }


if __name__ == "__main__":
    unittest.main()
