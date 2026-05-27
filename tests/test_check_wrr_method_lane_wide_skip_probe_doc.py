import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import analyze_wrr_method_lane_wide_skip as probe
from scripts import check_wrr_method_lane_wide_skip_probe_doc as checker


class CheckWrrMethodLaneWideSkipProbeDocTests(unittest.TestCase):
    def test_validate_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = root / "probe.md"
            out = root / "probe.csv"
            summary = root / "summary.csv"
            manifest = root / "manifest.json"
            rows = [row(term_id) for term_id in sorted(checker.EXPECTED_TERM_IDS)]
            summary_rows = [
                {
                    **checker.EXPECTED_SUMMARY,
                    "read": "All 11 OCR-matched method-lane terms remain absent.",
                }
            ]
            write_csv(out, probe.probe_fieldnames(list(probe.DEFAULT_PROFILE_SKIPS)), rows)
            write_csv(summary, probe.SUMMARY_FIELDNAMES, summary_rows)
            manifest.write_text(
                json.dumps(
                    {
                        "tool": "analyze_wrr_method_lane_wide_skip",
                        "parameters": {
                            "max_skip": probe.DEFAULT_MAX_SKIP,
                            "direction": "both",
                            "jobs": 1,
                            "profile_skips": list(probe.DEFAULT_PROFILE_SKIPS),
                        },
                        "inputs": {
                            "method_packet": str(probe.DEFAULT_METHOD_PACKET),
                            "config": str(probe.DEFAULT_CONFIG),
                        },
                        "outputs": {
                            "out": str(checker.DEFAULT_OUT),
                            "summary_out": str(checker.DEFAULT_SUMMARY),
                            "markdown_out": str(checker.DEFAULT_DOC),
                            "manifest_out": str(checker.DEFAULT_MANIFEST),
                        },
                        "probe_rows": 11,
                        "summary_rows": 1,
                    }
                ),
                encoding="utf-8",
            )
            doc.write_text(
                "\n".join(
                    [
                        "# WRR Method-Lane Wide-Skip Probe",
                        "Status: diagnostic probe for OCR-matched WRR method-lane terms.",
                        "It does not choose source corrections, method changes, or pair exclusions.",
                        "- method-lane terms: 11.",
                        "- max skip probed: 5000.",
                        "- terms with any wider-skip hit: 0.",
                        "- terms still zero through max skip: 11.",
                        "- total hits through max skip: 0.",
                        "Wide-skip hits are diagnostic only.",
                        "No row here changes the locked local WRR method report.",
                    ]
                ),
                encoding="utf-8",
            )

            self.assertEqual(
                checker.validate_wide_skip_probe_doc(doc, out, summary, manifest),
                [],
            )


def row(term_id: str) -> dict[str, object]:
    values: dict[str, object] = {
        "term_id": term_id,
        "term": "BGD",
        "normalized_term": "BGD",
        "concept": "WRR2 X",
        "row_number": "99",
        "pair_id": "pair_x",
        "date_term_id": "date_x",
        "max_skip": "5000",
        "direction": "both",
    }
    for profile in probe.DEFAULT_PROFILE_SKIPS:
        values[probe.profile_field(profile)] = "0"
    values.update(
        {
            "total_hits_through_max": "0",
            "found_within_max_skip": "false",
            "first_hit_skip": "",
            "first_hit_direction": "",
            "first_hit_start_offset": "",
            "first_hit_end_offset": "",
            "first_hit_start_ref": "",
            "first_hit_end_ref": "",
            "first_hit_span_letters": "",
            "read": "No ordinary Genesis ELS hit found through skip 5000.",
        }
    )
    return values


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
