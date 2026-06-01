#!/usr/bin/env python3
"""Validate Cities recovered-PDF text audit doc matches generated CSVs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from scripts import analyze_cities_recovered_pdf_text as analyzer


DEFAULT_DOC = analyzer.DEFAULT_MD
DEFAULT_ROWS = analyzer.DEFAULT_OUT
DEFAULT_SUMMARY = analyzer.DEFAULT_SUMMARY_OUT
DEFAULT_ANCHORS = analyzer.DEFAULT_ANCHORS_OUT
DEFAULT_MANIFEST = analyzer.DEFAULT_MANIFEST

REQUIRED_PHRASES = (
    "# Cities Recovered PDF Text Audit",
    "Status: source-shape audit only.",
    "does not run OCR",
    "normalize city names",
    "ELS searches",
    "compute compactness",
    "verify p-levels",
    "Rows with extractable text are now separated from image-only or garbled",
    "does not decide which texts are admissible for a result-bearing protocol",
)

EXPECTED_SUMMARY_ROW = {
    "recovered_pdf_rows": "17",
    "extractable_text_rows": "5",
    "zero_text_rows": "9",
    "garbled_or_nonlatin_rows": "3",
    "gans_family_rows": "2",
    "aumann_family_rows": "14",
    "other_family_rows": "1",
    "anchor_rows": "5",
    "anchors_found": "5",
    "claim_status": "source_shape_only_not_result_bearing",
}

EXPECTED_MANIFEST_SUMMARY = {
    "recovered_pdf_rows": 17,
    "extractable_text_rows": 5,
    "zero_text_rows": 9,
    "garbled_or_nonlatin_rows": 3,
    "gans_family_rows": 2,
    "aumann_family_rows": 14,
    "other_family_rows": 1,
    "anchor_rows": 5,
    "anchors_found": 5,
    "claim_status": "source_shape_only_not_result_bearing",
}

EXPECTED_ROW_LOCKS = (
    {
        "label": "cities_pdf_wrr",
        "source_pages": "torah_code_experiment_cities_aumann",
        "url": "https://www.torah-code.org/experiments/WRR.pdf",
        "selected_source": "archive",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_wrr.pdf",
        "sha256": "a63419d9f20ba23f86970c0765b3b73b40e6158b524d4f9e561697b6b00aaec1",
        "bytes": "820618",
        "pdf_pages": "10",
        "text_chars": "0",
        "normalized_text_chars": "0",
        "latin_letter_ratio": "0.000",
        "text_status": "zero_extractable_text",
        "family": "other",
        "title_guess_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    },
    {
        "label": "cities_pdf_dp364_short",
        "source_pages": "torah_code_experiment_cities_aumann",
        "url": "https://www.torah-code.org/experiments/dp364_short.pdf",
        "selected_source": "archive",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_dp364_short.pdf",
        "sha256": "e66ad829b18e92688fdc458d9b2c75c345f41f76600e211ec0aa4132fc566741",
        "bytes": "190088",
        "pdf_pages": "6",
        "text_chars": "0",
        "normalized_text_chars": "0",
        "latin_letter_ratio": "0.000",
        "text_status": "zero_extractable_text",
        "family": "aumann_committee",
        "title_guess_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    },
    {
        "label": "cities_pdf_dp365a_appendix_2",
        "source_pages": "torah_code_experiment_cities_aumann",
        "url": "https://www.torah-code.org/experiments/dp365A_appendix_2.pdf",
        "selected_source": "archive",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_dp365a_appendix_2.pdf",
        "sha256": "40153b5d0b0cbdf5393d6dfd83533c8bda66b72a1fc718f946ec71ff27391ba6",
        "bytes": "249350",
        "pdf_pages": "10",
        "text_chars": "0",
        "normalized_text_chars": "0",
        "latin_letter_ratio": "0.000",
        "text_status": "zero_extractable_text",
        "family": "aumann_committee",
        "title_guess_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    },
    {
        "label": "cities_pdf_dp365a_appendix_3",
        "source_pages": "torah_code_experiment_cities_aumann",
        "url": "https://www.torah-code.org/experiments/dp365A_appendix_3.pdf",
        "selected_source": "archive",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_dp365a_appendix_3.pdf",
        "sha256": "e232ad6a69a82bab7517f69a5e48476e6c6cc5aded25d75cbd43401e332f4288",
        "bytes": "1715168",
        "pdf_pages": "",
        "text_chars": "0",
        "normalized_text_chars": "0",
        "latin_letter_ratio": "0.000",
        "text_status": "zero_extractable_text",
        "family": "aumann_committee",
        "title_guess_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    },
    {
        "label": "cities_pdf_dp365a_appendix_4",
        "source_pages": "torah_code_experiment_cities_aumann",
        "url": "https://www.torah-code.org/experiments/dp365A_appendix_4.pdf",
        "selected_source": "archive",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_dp365a_appendix_4.pdf",
        "sha256": "e22c44cde47408a5e21a75cd5491f88e48ab4bf6a46e1f307fa311ce417ff502",
        "bytes": "53308",
        "pdf_pages": "2",
        "text_chars": "0",
        "normalized_text_chars": "0",
        "latin_letter_ratio": "0.000",
        "text_status": "zero_extractable_text",
        "family": "aumann_committee",
        "title_guess_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    },
    {
        "label": "cities_pdf_dp365a_appendix_5",
        "source_pages": "torah_code_experiment_cities_aumann",
        "url": "https://www.torah-code.org/experiments/dp365A_appendix_5.pdf",
        "selected_source": "archive",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_dp365a_appendix_5.pdf",
        "sha256": "d7fd31e8312f0906e6c79a0fb39c17fe7497e62bfc3a520fc05fed88f6a1c9de",
        "bytes": "43165",
        "pdf_pages": "2",
        "text_chars": "0",
        "normalized_text_chars": "0",
        "latin_letter_ratio": "0.000",
        "text_status": "zero_extractable_text",
        "family": "aumann_committee",
        "title_guess_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    },
    {
        "label": "cities_pdf_dp365a_appendix_6",
        "source_pages": "torah_code_experiment_cities_aumann",
        "url": "https://www.torah-code.org/experiments/dp365A_appendix_6.pdf",
        "selected_source": "archive",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_dp365a_appendix_6.pdf",
        "sha256": "5d9949a0a348bcd98e5293fdb2c02d7ab13fe10e4e409a53a40c77abe898938a",
        "bytes": "43143",
        "pdf_pages": "2",
        "text_chars": "0",
        "normalized_text_chars": "0",
        "latin_letter_ratio": "0.000",
        "text_status": "zero_extractable_text",
        "family": "aumann_committee",
        "title_guess_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    },
    {
        "label": "cities_pdf_dp365a_appendix_7",
        "source_pages": "torah_code_experiment_cities_aumann",
        "url": "https://www.torah-code.org/experiments/dp365A_appendix_7.pdf",
        "selected_source": "archive",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_dp365a_appendix_7.pdf",
        "sha256": "7b7e2015bb62841738267b57644c0a6c289f353fbad411a37aa1b4c10a05dc91",
        "bytes": "58835",
        "pdf_pages": "5",
        "text_chars": "0",
        "normalized_text_chars": "0",
        "latin_letter_ratio": "0.000",
        "text_status": "zero_extractable_text",
        "family": "aumann_committee",
        "title_guess_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    },
    {
        "label": "cities_pdf_dp365a_p1_4",
        "source_pages": "torah_code_experiment_cities_aumann",
        "url": "https://www.torah-code.org/experiments/dp365A_p1-4.pdf",
        "selected_source": "archive",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_dp365a_p1_4.pdf",
        "sha256": "90fb6ff653d2fc972663abe34926dac0f6fa2a694d3e8f1cd979edc444e08472",
        "bytes": "400106",
        "pdf_pages": "4",
        "text_chars": "6115",
        "normalized_text_chars": "460",
        "latin_letter_ratio": "1.000",
        "text_status": "extractable_but_garbled_or_nonlatin",
        "family": "aumann_committee",
        "title_guess_sha256": "4a0b2ab8a6fb1345de15641dad0fcee8d9afbd6936cab0a5daf25bff5daddd8a",
    },
    {
        "label": "cities_pdf_dp365a_p12_17",
        "source_pages": "torah_code_experiment_cities_aumann",
        "url": "https://www.torah-code.org/experiments/dp365A_p12-17.pdf",
        "selected_source": "archive",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_dp365a_p12_17.pdf",
        "sha256": "127d829147cbc1ecc6894ce99399593af456eefd5bf6c62aafcae5ab63144472",
        "bytes": "1477130",
        "pdf_pages": "6",
        "text_chars": "37639",
        "normalized_text_chars": "1991",
        "latin_letter_ratio": "1.000",
        "text_status": "extractable_but_garbled_or_nonlatin",
        "family": "aumann_committee",
        "title_guess_sha256": "16c236d8cb06a200e590e26c8c800ab0f5848920eb631d9da99a8aebf23104c5",
    },
    {
        "label": "cities_pdf_dp365a_p5_11",
        "source_pages": "torah_code_experiment_cities_aumann",
        "url": "https://www.torah-code.org/experiments/dp365A_p5-11.pdf",
        "selected_source": "archive",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_dp365a_p5_11.pdf",
        "sha256": "e89e869d452f429403845d82037d5b4be5c549c3f1ba124b62e49542551cfb67",
        "bytes": "1126607",
        "pdf_pages": "7",
        "text_chars": "18107",
        "normalized_text_chars": "2913",
        "latin_letter_ratio": "1.000",
        "text_status": "extractable_but_garbled_or_nonlatin",
        "family": "aumann_committee",
        "title_guess_sha256": "21104cfee403c21aabd6296627cd1ef7ee6b9ce94a486c0e9765f9fc624e1f8b",
    },
    {
        "label": "cities_pdf_dp365a_part_2_p105_111",
        "source_pages": "torah_code_experiment_cities_aumann",
        "url": "https://www.torah-code.org/experiments/dp365A_part_2_p105-111.pdf",
        "selected_source": "archive",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_dp365a_part_2_p105_111.pdf",
        "sha256": "248d3ff6a9fd104219864116d29e8d24c15bef7e37858397741b9dcc52707aba",
        "bytes": "249529",
        "pdf_pages": "7",
        "text_chars": "0",
        "normalized_text_chars": "0",
        "latin_letter_ratio": "0.000",
        "text_status": "zero_extractable_text",
        "family": "aumann_committee",
        "title_guess_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    },
    {
        "label": "cities_pdf_dp_365_1",
        "source_pages": "torah_code_experiment_cities_aumann",
        "url": "https://www.torah-code.org/experiments/dp_365_1.pdf",
        "selected_source": "archive",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_dp_365_1.pdf",
        "sha256": "ae09dc718ad2e7980249d3cf5668b783ee7d95746353414c1d9d85b571b53a97",
        "bytes": "105651",
        "pdf_pages": "2",
        "text_chars": "7044",
        "normalized_text_chars": "6903",
        "latin_letter_ratio": "1.000",
        "text_status": "extractable_text",
        "family": "aumann_committee",
        "title_guess_sha256": "29993972931f9968e9c76fcd2b8cce888a6e22027a09fc2fb7c32cda80769db3",
    },
    {
        "label": "cities_pdf_dp_365_2",
        "source_pages": "torah_code_experiment_cities_aumann",
        "url": "https://www.torah-code.org/experiments/dp_365_2.pdf",
        "selected_source": "archive",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_dp_365_2.pdf",
        "sha256": "5301f21fa3c1b5b82fd5ae1a67e1791b136549b817fdc4ff34bdb451a92acb5b",
        "bytes": "84614",
        "pdf_pages": "2",
        "text_chars": "6248",
        "normalized_text_chars": "6087",
        "latin_letter_ratio": "1.000",
        "text_status": "extractable_text",
        "family": "aumann_committee",
        "title_guess_sha256": "7182cab7ec838dc621351db67e6f9a8c6bffd33de086ec8397558086f7f24d38",
    },
    {
        "label": "cities_pdf_dp_365_4",
        "source_pages": "torah_code_experiment_cities_aumann",
        "url": "https://www.torah-code.org/experiments/dp_365_4.pdf",
        "selected_source": "archive",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_dp_365_4.pdf",
        "sha256": "4dc4119f30430dc294fe3bee5e00b3465a9b0b033bd4edf96a97330d0c3e75d7",
        "bytes": "123854",
        "pdf_pages": "2",
        "text_chars": "5759",
        "normalized_text_chars": "5456",
        "latin_letter_ratio": "0.991",
        "text_status": "extractable_text",
        "family": "aumann_committee",
        "title_guess_sha256": "31e9c1ee245cae24bd5c10a55366eb5413382769f88fedc6e8f885fcc4175379",
    },
    {
        "label": "cities_pdf_communities_data",
        "source_pages": "torah_code_experiment_cities_gans",
        "url": "https://www.torah-code.org/papers/communities_data.pdf",
        "selected_source": "archive",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_communities_data.pdf",
        "sha256": "ac0b221064e144ca9a70d616064bcd58f7d8e68cd2fe6bedb202dd81991feb86",
        "bytes": "349586",
        "pdf_pages": "8",
        "text_chars": "30281",
        "normalized_text_chars": "18135",
        "latin_letter_ratio": "0.990",
        "text_status": "extractable_text",
        "family": "gans_communities",
        "title_guess_sha256": "f1c887813644cc65258a9bb4ac74a11a5e6f8f99aee16d9affc5c9111e99cf47",
    },
    {
        "label": "cities_pdf_gans",
        "source_pages": "torah_code_experiment_cities_gans",
        "url": "https://www.torah-code.org/papers/gans.pdf",
        "selected_source": "archive",
        "selected_path": "reports/cities_pdf_recovery_probe/snapshots/archive/cities_pdf_gans.pdf",
        "sha256": "212cb24f918b9a417a6837ce5f1d6c6af3c80abba77bac084d6cd068c572adf0",
        "bytes": "126543",
        "pdf_pages": "5",
        "text_chars": "25846",
        "normalized_text_chars": "19499",
        "latin_letter_ratio": "0.997",
        "text_status": "extractable_text",
        "family": "gans_communities",
        "title_guess_sha256": "29095f46e38136838194c87aa2ae61ac4ce33d3a89793acf593f3f0d67353f05",
    },
)

EXPECTED_ANCHORS = (
    {
        "anchor": "gans_communities_data_title",
        "label": "cities_pdf_communities_data",
        "status": "found",
        "diagnostic": "Gans/Inbal/Bombach communities data title found",
    },
    {
        "anchor": "gans_paper_title",
        "label": "cities_pdf_gans",
        "status": "found",
        "diagnostic": "Gans/Inbal/Bombach paper title found",
    },
    {
        "anchor": "aumann_personal_perspective",
        "label": "cities_pdf_dp_365_1",
        "status": "found",
        "diagnostic": "Aumann personal-perspective title found",
    },
    {
        "anchor": "furstenberg_personal_perspective",
        "label": "cities_pdf_dp_365_2",
        "status": "found",
        "diagnostic": "Furstenberg personal-perspective title found",
    },
    {
        "anchor": "witztum_critique_title",
        "label": "cities_pdf_dp_365_4",
        "status": "found",
        "diagnostic": "Witztum critique title found",
    },
)

EXPECTED_STATUSES = tuple(
    sorted({row["text_status"] for row in EXPECTED_ROW_LOCKS})
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_recovered_pdf_text_audit_doc(
        args.doc,
        args.rows,
        args.summary,
        args.anchors,
        args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"Cities recovered-PDF text audit doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities recovered-PDF text audit doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--anchors", type=Path, default=DEFAULT_ANCHORS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_cities_recovered_pdf_text_audit_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    summary_csv: Path = DEFAULT_SUMMARY,
    anchors_csv: Path = DEFAULT_ANCHORS,
    manifest_json: Path = DEFAULT_MANIFEST,
) -> list[str]:
    missing_files = [
        str(path)
        for path in (doc, rows_csv, summary_csv, anchors_csv, manifest_json)
        if not path.exists()
    ]
    if missing_files:
        return ["missing required files: " + ", ".join(missing_files)]

    text = doc.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    rows_data = read_csv(rows_csv)
    summary_data = read_csv(summary_csv)
    anchors_data = read_csv(anchors_csv)
    if isinstance(rows_data, str):
        return [rows_data]
    if isinstance(summary_data, str):
        return [summary_data]
    if isinstance(anchors_data, str):
        return [anchors_data]
    _, rows = rows_data
    _, summary_rows = summary_data
    _, anchors = anchors_data
    if len(summary_rows) != 1:
        return [f"{summary_csv} must have exactly one summary row"]
    summary = summary_rows[0]

    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized
    ]
    failures.extend(validate_rows_csv(rows_csv, rows_data))
    failures.extend(validate_summary_csv(summary_csv, summary_data))
    failures.extend(validate_anchors_csv(anchors_csv, anchors_data))
    failures.extend(validate_manifest(manifest_json))
    failures.extend(validate_summary_counts(doc, normalized, summary, anchors))
    failures.extend(validate_rows_in_doc(doc, normalized))
    return failures


def validate_summary_counts(
    doc: Path,
    normalized_doc: str,
    summary: dict[str, str],
    anchors: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    count_expectations = {
        "recovered PDF rows audited": summary.get("recovered_pdf_rows", ""),
        "extractable text rows": summary.get("extractable_text_rows", ""),
        "zero-text rows": summary.get("zero_text_rows", ""),
        "garbled/non-Latin extract rows": summary.get("garbled_or_nonlatin_rows", ""),
        "Gans/community family rows": summary.get("gans_family_rows", ""),
        "Aumann committee family rows": summary.get("aumann_family_rows", ""),
        "other family rows": summary.get("other_family_rows", ""),
    }
    for label, value in count_expectations.items():
        expected = normalize_space(f"| {label} | {value} |")
        if expected not in normalized_doc:
            failures.append(f"{doc} missing summary count: {label}={value}")

    anchor_total = str(len(anchors))
    anchor_found = str(sum(1 for row in anchors if row.get("status") == "found"))
    found_phrase = normalize_space(f"Found anchors: {anchor_found} of {anchor_total}.")
    if found_phrase not in normalized_doc:
        failures.append(
            f"{doc} missing anchor count: found={anchor_found} total={anchor_total}"
        )
    return failures


def validate_rows_csv(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != analyzer.ROW_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    actual = [row_lock(row) for row in rows]
    expected = list(EXPECTED_ROW_LOCKS)
    if actual != expected:
        failures.append(f"{path} row data drifted")
    return failures


def validate_summary_csv(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != analyzer.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if rows != [EXPECTED_SUMMARY_ROW]:
        failures.append(f"{path} summary row drifted")
    return failures


def validate_anchors_csv(
    path: Path,
    data: tuple[list[str], list[dict[str, str]]],
) -> list[str]:
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != analyzer.ANCHOR_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if rows != list(EXPECTED_ANCHORS):
        failures.append(f"{path} anchor rows drifted")
    return failures


def validate_manifest(path: Path) -> list[str]:
    data = read_json(path)
    if isinstance(data, str):
        return [data]
    checks: dict[str, Any] = {
        "tool": "analyze_cities_recovered_pdf_text.py",
        "input_recovery_csv": str(analyzer.DEFAULT_RECOVERY_CSV),
        "rows": len(EXPECTED_ROW_LOCKS),
        "summary": EXPECTED_MANIFEST_SUMMARY,
        "outputs": {
            "csv": str(DEFAULT_ROWS),
            "summary": str(DEFAULT_SUMMARY),
            "anchors": str(DEFAULT_ANCHORS),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "claim_boundary": "source-shape audit only; no ELS result",
    }
    failures: list[str] = []
    for key, expected in checks.items():
        if data.get(key) != expected:
            failures.append(f"{path} {key} drifted")
    return failures


def validate_rows_in_doc(
    doc: Path,
    normalized_doc: str,
) -> list[str]:
    labels = {row["label"] for row in EXPECTED_ROW_LOCKS}
    statuses = {row["text_status"] for row in EXPECTED_ROW_LOCKS}
    failures: list[str] = []
    for label in labels:
        if label not in normalized_doc:
            failures.append(f"{doc} missing row label: {label}")
    for status in EXPECTED_STATUSES:
        if status not in statuses:
            failures.append(f"expected status lock missing text status: {status}")
        if status not in normalized_doc:
            failures.append(f"{doc} missing text status: {status}")
    return failures


def row_lock(row: dict[str, str]) -> dict[str, str]:
    locked = {
        key: row.get(key, "")
        for key in analyzer.ROW_FIELDNAMES
        if key != "title_guess"
    }
    locked["title_guess_sha256"] = hashlib.sha256(
        row.get("title_guess", "").encode("utf-8")
    ).hexdigest()
    return locked


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
