#!/usr/bin/env python3
"""Validate English source-basis audit metadata and queue counts."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


DEFAULT_BIBLEGATEWAY_MANIFEST = Path("configs/biblegateway_english_versions.csv")
DEFAULT_EBIBLE_CONTROLS = Path("configs/ebible_english_controls.csv")
DEFAULT_DOOR43_CONTROLS = Path("configs/door43_english_controls.csv")
DEFAULT_OET_CONTROLS = Path("configs/oet_english_controls.csv")
DEFAULT_AUDIT_QUEUE = Path("docs/SOURCE_BASIS_AUDIT_QUEUE.md")
ALLOWED_BASIS_STATUSES = {"broad_tradition", "needs_audit"}
MANIFEST_LABELS = {
    "biblegateway": "BibleGateway English versions",
    "ebible": "eBible English controls",
    "door43": "Door43 English controls",
    "oet": "OET English controls",
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_basis_queue(
        biblegateway_manifest=args.biblegateway_manifest,
        ebible_controls=args.ebible_controls,
        door43_controls=args.door43_controls,
        oet_controls=args.oet_controls,
        audit_queue=args.audit_queue,
        allow_needs_audit=args.allow_needs_audit,
    )
    if failures:
        for failure in failures:
            print(f"source-basis validation failure: {failure}")
        return 1
    print(f"source-basis validation passed: {args.audit_queue}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--biblegateway-manifest", type=Path, default=DEFAULT_BIBLEGATEWAY_MANIFEST)
    parser.add_argument("--ebible-controls", type=Path, default=DEFAULT_EBIBLE_CONTROLS)
    parser.add_argument("--door43-controls", type=Path, default=DEFAULT_DOOR43_CONTROLS)
    parser.add_argument("--oet-controls", type=Path, default=DEFAULT_OET_CONTROLS)
    parser.add_argument("--audit-queue", type=Path, default=DEFAULT_AUDIT_QUEUE)
    parser.add_argument(
        "--allow-needs-audit",
        action="store_true",
        help="Allow manifest rows whose basis_status remains needs_audit.",
    )
    return parser


def validate_source_basis_queue(
    *,
    biblegateway_manifest: Path = DEFAULT_BIBLEGATEWAY_MANIFEST,
    ebible_controls: Path = DEFAULT_EBIBLE_CONTROLS,
    door43_controls: Path = DEFAULT_DOOR43_CONTROLS,
    oet_controls: Path = DEFAULT_OET_CONTROLS,
    audit_queue: Path = DEFAULT_AUDIT_QUEUE,
    allow_needs_audit: bool = False,
) -> list[str]:
    failures: list[str] = []
    try:
        biblegateway_rows = read_rows(biblegateway_manifest)
        ebible_rows = read_rows(ebible_controls)
        door43_rows = read_rows(door43_controls)
        oet_rows = read_rows(oet_controls)
        observed_counts = read_audit_queue_counts(audit_queue)
    except (OSError, csv.Error) as exc:
        return [f"could not read source-basis inputs: {exc}"]

    manifests = {
        "biblegateway": biblegateway_rows,
        "ebible": ebible_rows,
        "door43": door43_rows,
        "oet": oet_rows,
    }
    for manifest_key, rows in manifests.items():
        failures.extend(validate_manifest_rows(manifest_key, rows))

    expected_counts = {
        MANIFEST_LABELS["biblegateway"]: count_basis_rows(biblegateway_rows),
        MANIFEST_LABELS["ebible"]: count_basis_rows(ebible_rows),
        MANIFEST_LABELS["door43"]: count_basis_rows(door43_rows),
        MANIFEST_LABELS["oet"]: count_basis_rows(oet_rows),
    }
    if observed_counts != expected_counts:
        failures.append(
            "audit queue counts do not match manifests: "
            f"observed={observed_counts} expected={expected_counts}"
        )

    if not allow_needs_audit:
        needs_audit = [
            f"{MANIFEST_LABELS[manifest_key]}:{row['label']}"
            for manifest_key, rows in manifests.items()
            for row in rows
            if row.get("basis_status") == "needs_audit"
        ]
        if needs_audit:
            failures.append("needs_audit rows remain: " + ", ".join(needs_audit))
    return failures


def validate_manifest_rows(manifest_key: str, rows: list[dict[str, str]]) -> list[str]:
    failures: list[str] = []
    seen_labels: set[str] = set()
    for row_number, row in enumerate(rows, start=2):
        row_id = f"{MANIFEST_LABELS[manifest_key]} row {row_number}"
        label = row.get("label", "")
        if not label:
            failures.append(f"{row_id}: missing label")
        elif label in seen_labels:
            failures.append(f"{row_id}: duplicate label {label}")
        seen_labels.add(label)
        for field in ["coverage", "ot_basis", "nt_basis", "source_family", "basis_status"]:
            if not row.get(field, "").strip():
                failures.append(f"{row_id}: missing {field}")
        status = row.get("basis_status", "")
        if status and status not in ALLOWED_BASIS_STATUSES:
            failures.append(f"{row_id}: unknown basis_status {status}")
        if manifest_key == "ebible":
            failures.extend(validate_ebible_row(row, row_id))
        elif manifest_key == "door43":
            failures.extend(validate_door43_row(row, row_id))
        elif manifest_key == "oet":
            failures.extend(validate_oet_row(row, row_id))
    return failures


def validate_ebible_row(row: dict[str, str], row_id: str) -> list[str]:
    failures: list[str] = []
    if not row.get("source_id", "").strip():
        failures.append(f"{row_id}: missing source_id")
    source_url = row.get("source_url", "")
    if not source_url.startswith("https://ebible.org/Scriptures/"):
        failures.append(f"{row_id}: invalid source_url")
    details_url = row.get("details_url", "")
    if not details_url.startswith("https://ebible.org/") or "id=" not in details_url:
        failures.append(f"{row_id}: invalid details_url")
    if "eBible" not in row.get("license_label", ""):
        failures.append(f"{row_id}: missing eBible license_label")
    return failures


def validate_door43_row(row: dict[str, str], row_id: str) -> list[str]:
    failures: list[str] = []
    if not row.get("source_id", "").strip():
        failures.append(f"{row_id}: missing source_id")
    source_url = row.get("source_url", "")
    if not source_url.startswith("https://git.door43.org/"):
        failures.append(f"{row_id}: invalid source_url")
    details_url = row.get("details_url", "")
    if not details_url.startswith("https://git.door43.org/"):
        failures.append(f"{row_id}: invalid details_url")
    if "CC BY-SA 4.0" not in row.get("license_label", ""):
        failures.append(f"{row_id}: missing CC BY-SA 4.0 license_label")
    return failures


def validate_oet_row(row: dict[str, str], row_id: str) -> list[str]:
    failures: list[str] = []
    if not row.get("source_id", "").strip():
        failures.append(f"{row_id}: missing source_id")
    source_url = row.get("source_url", "")
    if not source_url.startswith("https://github.com/Freely-Given-org/"):
        failures.append(f"{row_id}: invalid source_url")
    details_url = row.get("details_url", "")
    if not details_url.startswith("https://OpenEnglishTranslation.Bible/"):
        failures.append(f"{row_id}: invalid details_url")
    if "CC BY-SA 4.0" not in row.get("license_label", ""):
        failures.append(f"{row_id}: missing CC BY-SA 4.0 license_label")
    if not row.get("source_path_prefix", "").startswith("exportedFiles/cleanedUSFM/"):
        failures.append(f"{row_id}: invalid source_path_prefix")
    return failures


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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
    raise SystemExit(main())
