#!/usr/bin/env python3
"""Validate WRR source visual-review notes stay scoped to triage."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_VISUAL_REVIEW_NOTES.md")
DEFAULT_QUEUE = Path("reports/wrr_1994/wrr_source_review_queue.csv")

EXPECTED_VISUAL_ROWS = {
    "wrr2_23_app_04": {
        "priority_rank": "1",
        "term": "Y@QBHLWY",
        "row_numbers": "23",
        "review_bucket": "ocr_not_matched_with_variant_lead",
        "row_ocr_status": "not_matched",
        "visual_review_note": "primary page row visibly contains Yaakov Ha-Levi wording; row OCR missed it",
        "visual_review_action": "treat as visual OCR miss until a locked transcription says otherwise",
        "source_review_flags": "",
        "source_review_action": "",
    },
    "wrr2_30_app_05": {
        "priority_rank": "2",
        "term": "B@LY$RLBB",
        "row_numbers": "30",
        "review_bucket": "ocr_not_matched_with_variant_lead",
        "row_ocr_status": "not_matched",
        "visual_review_note": "primary Hebrew name cell visibly contains Yosher Levav text without visible B@L prefix",
        "visual_review_action": "review title-prefix/appellation rule before any source correction",
        "source_review_flags": "wnp_book_title_appellation_dispute",
        "source_review_action": "source/title-prefix rule review; visual notes show title text without visible B@L prefix",
    },
    "wrr2_23_app_05": {
        "priority_rank": "3",
        "term": "MHRYSGL",
        "row_numbers": "23",
        "review_bucket": "ocr_not_matched_with_variant_lead",
        "row_ocr_status": "not_matched",
        "visual_review_note": "primary page row visibly contains Maharil Segal wording; row OCR missed it",
        "visual_review_action": "treat as visual OCR miss until a locked transcription says otherwise",
        "source_review_flags": "",
        "source_review_action": "",
    },
    "wrr2_28_app_04": {
        "priority_rank": "4",
        "term": "B@LPNYM$H",
        "row_numbers": "28",
        "review_bucket": "ocr_not_matched_with_variant_lead",
        "row_ocr_status": "not_matched",
        "visual_review_note": "primary Hebrew name cell visibly contains Pnei Moshe text without visible B@L prefix",
        "visual_review_action": "review title-prefix/appellation rule before any source correction",
        "source_review_flags": "",
        "source_review_action": "",
    },
    "wrr2_32_app_04": {
        "priority_rank": "5",
        "term": "$LMHMXLMA",
        "row_numbers": "32",
        "review_bucket": "ocr_not_matched_with_variant_lead",
        "row_ocr_status": "not_matched",
        "visual_review_note": "English label says of-Chelm; visible primary Hebrew cell supports Rabbi Shelomo only in this pass",
        "visual_review_action": "review source/pair rule before using this as a Hebrew-cell match",
        "source_review_flags": "wnp_chelm_spelling_context",
        "source_review_action": "source/pair-rule review; visual notes show English of-Chelm label but primary Hebrew cell only supports RBY$LMH in this pass",
    },
    "wrr2_27_date_01": {
        "priority_rank": "6",
        "term": "/+Z/T$RY",
        "row_numbers": "27",
        "review_bucket": "ocr_near_match_with_variant_lead",
        "row_ocr_status": "not_matched",
        "visual_review_note": "primary page row visibly contains 16 Tishri date forms; row OCR has near match",
        "visual_review_action": "check page image before treating as source difference",
        "source_review_flags": "",
        "source_review_action": "",
    },
    "wrr2_27_app_06": {
        "priority_rank": "7",
        "term": "M$HZKWTW",
        "row_numbers": "27",
        "review_bucket": "ocr_near_match_with_variant_lead",
        "row_ocr_status": "not_matched",
        "visual_review_note": "primary page row visibly contains Moshe/Zacut forms; row OCR has near match",
        "visual_review_action": "check WNP Zacut dispute and page image before treating as source difference",
        "source_review_flags": "wnp_disputed_zacut_appellation",
        "source_review_action": "diagnostic flag only; do not exclude without source-lock policy",
    },
    "wrr2_19_app_11": {
        "priority_rank": "84",
        "term": "YWSP+RANY",
        "row_numbers": "19",
        "review_bucket": "ocr_near_match_no_variant_lead",
        "row_ocr_status": "not_matched",
        "visual_review_note": "primary page row visibly contains Maharit/Trani forms including Yosef Trani; row OCR has one-edit near match",
        "visual_review_action": "keep as page-image near-match until a locked transcription resolves the aleph spelling",
        "source_review_flags": "",
        "source_review_action": "",
    },
    "wrr2_19_app_12": {
        "priority_rank": "85",
        "term": "YWSPM+RANY",
        "row_numbers": "19",
        "review_bucket": "ocr_near_match_no_variant_lead",
        "row_ocr_status": "not_matched",
        "visual_review_note": "primary page row visibly contains Maharit/Trani forms including Matrani/Mitrani variants; row OCR has one-edit near match",
        "visual_review_action": "keep as page-image near-match until a locked transcription resolves the aleph spelling",
        "source_review_flags": "",
        "source_review_action": "",
    },
    "wrr2_31_app_07": {
        "priority_rank": "86",
        "term": "$M$",
        "row_numbers": "31",
        "review_bucket": "ocr_near_match_no_variant_lead",
        "row_ocr_status": "not_matched",
        "visual_review_note": "primary page row visibly contains Rabbi Shalom Sharabi forms including Sar Shalom and MaharaSHaSH; exact SMSh form is not settled by this crop",
        "visual_review_action": "keep as page-image or pair-rule review before any source correction",
        "source_review_flags": "",
        "source_review_action": "",
    },
}

REQUIRED_PHRASES = (
    "# WRR Source Visual Review Notes",
    "Status: visual triage notes only. These are not a locked primary transcription and not a WRR reproduction.",
    "Source reviewed: `reports/wrr_1994/wrr_1994_paper.pdf`, Table 2 page render `reports/wrr_1994/wrr_primary_table2_page-06.png`.",
    "| `wrr2_23_app_04` `Y@QBHLWY` | 23 | Row visibly contains",
    "| `wrr2_23_app_05` `MHRYSGL` | 23 | Row visibly contains",
    "| `wrr2_30_app_05` `B@LY$RLBB` | 30 | Full page visibly contains",
    "Row OCR normalizes the name cell as `אחהערישרלבב`, not `בעלישרלבב`.",
    "| `wrr2_28_app_04` `B@LPNYM$H` | 28 | Full page visibly contains",
    "Row OCR contains `רבי משה`, `מרגלית`, and `פני משה`, not `בעלפנימשה`.",
    "| `wrr2_32_app_04` `$LMHMXLMA` | 32 | Full page and bottom row crop visibly show",
    "Row OCR normalizes the name cell as `רבישלמהה`.",
    "| `wrr2_27_date_01` `/+Z/T$RY` | 27 | Row visibly contains",
    "| `wrr2_27_app_06` `M$HZKWTW` | 27 | Row visibly contains",
    "| `wrr2_19_app_11` `YWSP+RANY` | 19 | Row crop visibly contains Maharit/Trani forms",
    "| `wrr2_19_app_12` `YWSPM+RANY` | 19 | Row crop visibly contains Maharit/Trani forms",
    "| `wrr2_31_app_07` `$M$` | 31 | Row crop visibly contains Rabbi Shalom Sharabi forms",
    "keep as page-image review until a locked transcription resolves the aleph spelling.",
    "the exact imported `שמש` form is not settled by this crop.",
    "OCR miss, not obvious source absence.",
    "Source/title-prefix rule needs review.",
    "Source/pair-rule review needed; the English row label says `of Chelm`, but the primary Hebrew cell is not enough by itself to verify this secondary Hebrew appellation.",
    "## Local WNP Critique Context",
    "Rabbi II-27 Zacut forms",
    "Rabbi II-30 Yosher-Levav",
    "Rabbi II-32 Chelma",
    "The current `ocr_not_matched_with_variant_lead` bucket is mixed.",
    "Some top rows are plain OCR misses against visible primary-page text.",
    "Some rows are not simple source errors; they look like title/prefix normalization questions",
    "Row 32 is a separate Hebrew-cell versus English-label issue",
    "Row 19 is a page-image spelling issue",
    "Row 31 is not a simple OCR miss from this crop",
    "None of these notes authorize changing WRR terms or claiming reproduction.",
    "No visual-review note excludes a pair automatically; pair exclusion still requires an explicit source-policy decision.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_visual_review_notes_doc(args.doc, queue=args.queue)
    if failures:
        for failure in failures:
            print(f"WRR source visual-review notes doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source visual-review notes doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    return parser


def validate_source_visual_review_notes_doc(
    doc: Path,
    *,
    queue: Path | None = DEFAULT_QUEUE,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized_text = normalize_space(text)
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text and normalize_space(phrase) not in normalized_text
    ]
    missing_terms = sorted(set(EXPECTED_VISUAL_ROWS) - visual_doc_terms(text))
    if missing_terms:
        failures.append(f"{doc} missing visual-review rows: " + ", ".join(missing_terms))
    if queue is not None:
        failures.extend(validate_queue_csv(queue))
    return failures


def visual_doc_terms(text: str) -> set[str]:
    terms: set[str] = set()
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and cells[0].startswith("`wrr2_"):
            term_id = cells[0].split("`", 2)[1]
            terms.add(term_id)
    return terms


def validate_queue_csv(path: Path) -> list[str]:
    rows = _read_csv(path)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    visual_rows = [row for row in rows if row.get("visual_review_note")]
    if len(visual_rows) != len(EXPECTED_VISUAL_ROWS):
        failures.append(
            f"{path} has {len(visual_rows)} visual rows; expected "
            f"{len(EXPECTED_VISUAL_ROWS)}"
        )
    by_term = {row.get("term_id", ""): row for row in visual_rows}
    if set(by_term) != set(EXPECTED_VISUAL_ROWS):
        failures.append(f"{path} visual term set drifted")
    for term_id, expected in EXPECTED_VISUAL_ROWS.items():
        row = by_term.get(term_id)
        if row is None:
            failures.append(f"{path} missing visual term {term_id}")
            continue
        if row.get("run_label") != "all_lanes_cap1000":
            failures.append(f"{path} {term_id} run_label drifted")
        if row.get("term_side") not in {"appellation", "date"}:
            failures.append(f"{path} {term_id} term_side drifted")
        for key, value in expected.items():
            if row.get(key) != value:
                failures.append(f"{path} {term_id} {key} drifted")
    return failures


def _read_csv(path: Path) -> list[dict[str, str]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
