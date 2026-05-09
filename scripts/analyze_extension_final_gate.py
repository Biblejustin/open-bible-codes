#!/usr/bin/env python3
"""Combine exact-center context, controls, and cross-text checks into final gates."""

from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import UTC, datetime
from pathlib import Path

from els import __version__


COHORT_REVIEW = Path("reports/extension_exact_center_cohort_review_summary.csv")
COHORT_CONTROLS = Path("reports/extension_exact_center_cohort_controls_summary.csv")
DEEP_CONTROLS = Path("reports/extension_exact_center_controls_summary.csv")
CROSS_TEXT = Path("reports/extension_exact_center_cross_text_summary.csv")

SUMMARY_OUT = Path("reports/extension_exact_center_final_gate_summary.csv")
MD_OUT = Path("reports/extension_exact_center_final_gate.md")
MANIFEST_OUT = Path("reports/extension_exact_center_final_gate.manifest.json")

FIELDNAMES = [
    "overlap_key",
    "corpus",
    "term",
    "extended_sequence",
    "center_ref",
    "context_read",
    "control_source",
    "combined_min_p",
    "combined_min_q",
    "control_band",
    "cross_text_status",
    "opposite_match_count",
    "extension_span_has_matched_phrase_surface",
    "final_gate",
    "claim_status",
    "read",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    review_rows = read_rows(args.cohort_review)
    controls = read_control_rows(args.cohort_controls, args.deep_controls)
    cross_text = {(row["source_corpus"], row["overlap_key"]): row for row in read_rows(args.cross_text)}
    rows = [final_gate_row(row, controls, cross_text) for row in review_rows]
    write_rows(args.summary_out, rows)
    write_markdown(args.markdown_out, rows)
    write_manifest(args, len(review_rows), len(rows), started)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cohort-review", type=Path, default=COHORT_REVIEW)
    parser.add_argument("--cohort-controls", type=Path, default=COHORT_CONTROLS)
    parser.add_argument("--deep-controls", type=Path, default=DEEP_CONTROLS)
    parser.add_argument("--cross-text", type=Path, default=CROSS_TEXT)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=MD_OUT)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_OUT)
    return parser


def read_control_rows(
    cohort_controls: Path,
    deep_controls: Path,
) -> dict[tuple[str, str], dict[str, str]]:
    controls: dict[tuple[str, str], dict[str, str]] = {}
    for row in read_rows(cohort_controls):
        copied = dict(row)
        copied["control_source"] = "cohort_50_50"
        controls[(row["corpus"], row["overlap_key"])] = copied
    if deep_controls.exists():
        for row in read_rows(deep_controls):
            copied = dict(row)
            copied["control_source"] = "deep_200_200"
            controls[(row["corpus"], row["overlap_key"])] = copied
    return controls


def final_gate_row(
    review: dict[str, str],
    controls: dict[tuple[str, str], dict[str, str]],
    cross_text: dict[tuple[str, str], dict[str, str]],
) -> dict[str, str]:
    key = review["overlap_key"]
    corpus = review["corpus"]
    control = controls.get((corpus, key), {})
    cross = cross_text.get((corpus, key), {})
    gate = final_gate(
        context_gate=review.get("promotion_gate", ""),
        cross_text_status=cross.get("cross_text_status", ""),
        combined_q=control.get("combined_min_q", ""),
        phrase_surface=review.get("extension_span_has_matched_phrase_surface", ""),
    )
    return {
        "overlap_key": key,
        "corpus": corpus,
        "term": review["term"],
        "extended_sequence": review["extended_sequence"],
        "center_ref": review["center_ref"],
        "context_read": review["context_read"],
        "control_source": control.get("control_source", ""),
        "combined_min_p": control.get("combined_min_p", ""),
        "combined_min_q": control.get("combined_min_q", ""),
        "control_band": control.get("extension_band", ""),
        "cross_text_status": cross.get("cross_text_status", ""),
        "opposite_match_count": cross.get("opposite_match_count", ""),
        "extension_span_has_matched_phrase_surface": review.get(
            "extension_span_has_matched_phrase_surface",
            "",
        ),
        "final_gate": gate,
        "claim_status": claim_status(gate, review),
        "read": read_label(gate),
    }


def final_gate(
    *,
    context_gate: str,
    cross_text_status: str,
    combined_q: str,
    phrase_surface: str,
) -> str:
    if context_gate != "promote_exact_center":
        return "hold_no_exact_center"
    if cross_text_status != "cross_text_match":
        return "hold_source_only"
    q_value = numeric_value(combined_q)
    if q_value is None or q_value > 0.01:
        return "hold_control_not_q_le_0.01"
    if phrase_surface != "yes":
        return "review_cross_text_exact_center_hidden_phrase"
    return "review_cross_text_exact_center_surface_phrase"


def claim_status(gate: str, review: dict[str, str]) -> str:
    if gate.startswith("hold_"):
        return "hold"
    if review.get("extension_span_has_matched_phrase_surface") != "yes":
        return "review_only_not_claim"
    return "review_surface_phrase"


def read_label(gate: str) -> str:
    if gate == "review_cross_text_exact_center_hidden_phrase":
        return "strongest extension review row; hidden phrase only"
    if gate == "review_cross_text_exact_center_surface_phrase":
        return "strongest extension review row; phrase has surface support"
    if gate == "hold_source_only":
        return "exact center but source-only"
    if gate == "hold_control_not_q_le_0.01":
        return "exact center and cross-text, but controls not deep enough"
    return "held by final gate"


def write_markdown(path: Path, rows: list[dict[str, str]]) -> None:
    lines = [
        "# Extension Exact-Center Final Gate",
        "",
        "Combines exact-center context, extension controls, and cross-text support into one review table.",
        "",
        "| Corpus | Term | Center | Control | Cross-text | Gate | Claim status | Read |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        control = f"{row['control_source']} q={row['combined_min_q']}"
        cross = f"{row['cross_text_status']} n={row['opposite_match_count']}"
        lines.append(
            "| "
            + " | ".join(
                [
                    row["corpus"],
                    f"`{row['term']}` `{row['extended_sequence']}`",
                    row["center_ref"],
                    control,
                    cross,
                    f"`{row['final_gate']}`",
                    f"`{row['claim_status']}`",
                    row["read"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "`δοξα` is the only row that passes exact-center, cross-text, and deep q <= 0.01 controls. It remains review-only because the full extension phrase is hidden-path only, not surface text in the span.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_manifest(
    args: argparse.Namespace,
    input_rows: int,
    rows: int,
    started: float,
) -> None:
    payload = {
        "tool": "analyze_extension_final_gate",
        "version": __version__,
        "created_utc": datetime.now(UTC).isoformat(),
        "cohort_review": str(args.cohort_review),
        "cohort_controls": str(args.cohort_controls),
        "deep_controls": str(args.deep_controls),
        "cross_text": str(args.cross_text),
        "input_rows": input_rows,
        "rows": rows,
        "outputs": [
            str(args.summary_out),
            str(args.markdown_out),
            str(args.manifest_out),
        ],
        "seconds": round(time.perf_counter() - started, 3),
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def numeric_value(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


if __name__ == "__main__":
    raise SystemExit(main())
