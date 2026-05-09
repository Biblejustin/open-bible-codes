#!/usr/bin/env python3
"""Build a compact report for the Greek surface prospective run."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__


TERMS_IN = Path("terms/greek_surface_prospective_terms.csv")
QUEUE_IN = Path("reports/greek_surface_prospective/term_summary.csv")
PATTERNS_IN = Path("reports/greek_surface_prospective/surface_patterns.csv")
TRIAGE_IN = Path("reports/greek_surface_prospective/selected_patterns.csv")
COHORT_IN = Path("reports/greek_surface_prospective/term_cohort.csv")
CONTROL_IN = Path("reports/greek_surface_prospective/control_summary.csv")
LOCK_IN = Path("reports/study_locks/greek_surface_prospective.manifest.json")
PREFLIGHT_IN = Path("reports/study_locks/greek_surface_prospective.preflight.json")
REPORT_OUT = Path("docs/GREEK_SURFACE_PROSPECTIVE_REPORT.md")
MANIFEST_OUT = Path("reports/greek_surface_prospective/report.manifest.json")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    terms = read_rows(args.terms)
    queue = read_rows(args.queue)
    patterns = read_rows(args.patterns)
    selected = read_rows(args.selected)
    cohort = read_rows(args.cohort)
    controls = read_rows(args.control_summary)
    lock = read_json(args.lock_manifest)
    preflight = read_json(args.preflight)
    protocol = read_json(args.protocol_manifest) if args.protocol_manifest else {}
    report = build_report(
        terms=terms,
        queue=queue,
        patterns=patterns,
        selected=selected,
        cohort=cohort,
        controls=controls,
        lock=lock,
        preflight=preflight,
        protocol=protocol,
    )
    args.report_out.parent.mkdir(parents=True, exist_ok=True)
    args.report_out.write_text(report, encoding="utf-8")
    write_manifest(args, terms, patterns, selected, controls, lock, preflight, protocol)
    print(args.report_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", type=Path, default=TERMS_IN)
    parser.add_argument("--queue", type=Path, default=QUEUE_IN)
    parser.add_argument("--patterns", type=Path, default=PATTERNS_IN)
    parser.add_argument("--selected", type=Path, default=TRIAGE_IN)
    parser.add_argument("--cohort", type=Path, default=COHORT_IN)
    parser.add_argument("--control-summary", type=Path, default=CONTROL_IN)
    parser.add_argument("--lock-manifest", type=Path, default=LOCK_IN)
    parser.add_argument("--preflight", type=Path, default=PREFLIGHT_IN)
    parser.add_argument("--protocol-manifest", type=Path)
    parser.add_argument("--report-out", type=Path, default=REPORT_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def build_report(
    *,
    terms: list[dict[str, str]],
    queue: list[dict[str, str]],
    patterns: list[dict[str, str]],
    selected: list[dict[str, str]],
    cohort: list[dict[str, str]],
    controls: list[dict[str, str]],
    lock: dict[str, Any],
    preflight: dict[str, Any],
    protocol: dict[str, Any],
) -> str:
    scope_counts = Counter(row["presence_scope"] for row in patterns)
    cohort_counts = Counter(
        "selected" if row.get("selected") == "True" else row.get("read", "")
        for row in cohort
    )
    lock_commit = lock.get("git", {}).get("commit", "")
    lines = [
        "# Greek Surface Prospective Report",
        "",
        f"Status: {report_status(selected, controls)}.",
        "",
        "This is the first locked Greek surface prospective run after removing",
        "the prior selected surface rows from the expanded Greek term list.",
        "",
        "## Lock",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Lock commit | `{lock_commit}` |",
        f"| Lock dirty-state | `{lock.get('git', {}).get('dirty', '')}` |",
        f"| Preflight status | `{preflight.get('status', '')}` |",
        f"| Preflight artifact | `{preflight_artifact(preflight)}` |",
        f"| Protocol status | `{protocol_status(protocol)}` |",
        f"| Term rows | {len(terms):,} |",
        f"| Skip range | `{lock.get('settings', {}).get('skip_range', '')}` |",
        f"| Direction | `{lock.get('settings', {}).get('direction', '')}` |",
        f"| Minimum normalized length | `{lock.get('settings', {}).get('min_normalized_length', '')}` |",
        "",
        "## Result",
        "",
        "| Stage | Count |",
        "| --- | ---: |",
        f"| Exact-center surface hit rows | {sum_int(queue, 'total_exact_center_hits'):,} |",
        f"| Unique exact-center surface patterns | {len(patterns):,} |",
        f"| All-source patterns | {scope_counts.get('all_sources', 0):,} |",
        f"| Multi-source patterns | {scope_counts.get('multi_source', 0):,} |",
        f"| Source-only patterns | {scope_counts.get('source_only', 0):,} |",
        f"| Selected rows under registered all-source length-5 rule | {len(selected):,} |",
        f"| Control rows evaluated | {len(controls):,} |",
        "",
        "## Triage Buckets",
        "",
        "| Bucket | Terms |",
        "| --- | ---: |",
    ]
    for bucket, count in sorted(cohort_counts.items()):
        lines.append(f"| {bucket} | {count:,} |")
    lines.extend(
        [
            "",
            "## Top Queue Before Primary Filter",
            "",
            "| Term | Concept | Exact-center hits | All-source | Multi-source | Source-only |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in queue[:10]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['normalized_term']}`",
                    row["concept"],
                    row["total_exact_center_hits"],
                    row["all_source_patterns"],
                    row["multi_source_patterns"],
                    row["source_specific_patterns"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Registered Outcome",
            "",
            registered_outcome(selected, controls),
            "",
            "The primary filter was deliberately stricter than the exploratory queue:",
            "all-source exact-center surface rows had to have normalized length at",
            "least 5. The run found all-source rows only in the dense length-4 bucket",
            "after prior selected rows were removed.",
            "",
            "## Interpretation Boundary",
            "",
            "This is a valid negative result for the registered primary gate. It does",
            "not make a theological, prophetic, historical, or statistical claim. It",
            "does preserve lower-strength queue data for later separately locked",
            "studies, especially if a future study explicitly registers length-4 rows.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def report_status(selected: list[dict[str, str]], controls: list[dict[str, str]]) -> str:
    if not selected:
        return "negative_primary_filter_result; no claim"
    if controls:
        return "prospective_controlled_review_material; no claim"
    return "prospective_review_queue_material; no claim"


def protocol_status(protocol: dict[str, Any]) -> str:
    if protocol:
        return str(protocol.get("status", ""))
    return "written after report step"


def preflight_artifact(preflight: dict[str, Any]) -> str:
    return str(preflight.get("output_path") or PREFLIGHT_IN)


def registered_outcome(
    selected: list[dict[str, str]],
    controls: list[dict[str, str]],
) -> str:
    if not selected:
        return (
            "No row met the registered all-source exact-center surface plus "
            "length-5 rule. Therefore no control p/q values were computed and "
            "the study produced no prospective controlled review candidate."
        )
    if not controls:
        return "Rows reached triage, but no matched controls were available."
    passing = [
        row for row in controls if float(row.get("all_source_q_value") or "1") <= 0.05
    ]
    return f"Rows with all_source_q_value <= 0.05: {len(passing)}."


def sum_int(rows: list[dict[str, str]], field: str) -> int:
    total = 0
    for row in rows:
        try:
            total += int(row.get(field, "0") or "0")
        except ValueError:
            continue
    return total


def write_manifest(
    args: argparse.Namespace,
    terms: list[dict[str, str]],
    patterns: list[dict[str, str]],
    selected: list[dict[str, str]],
    controls: list[dict[str, str]],
    lock: dict[str, Any],
    preflight: dict[str, Any],
    protocol: dict[str, Any],
) -> None:
    payload = {
        "tool": "build_greek_surface_prospective_report",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "status": report_status(selected, controls),
        "lock_commit": lock.get("git", {}).get("commit", ""),
        "lock_manifest": str(args.lock_manifest),
        "preflight_status": preflight.get("status", ""),
        "preflight_artifact": preflight_artifact(preflight),
        "protocol_status": protocol_status(protocol),
        "term_rows": len(terms),
        "pattern_rows": len(patterns),
        "selected_rows": len(selected),
        "control_rows": len(controls),
        "outputs": [str(args.report_out), str(args.manifest_out)],
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
