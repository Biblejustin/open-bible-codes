#!/usr/bin/env python3
"""Validate generated strongest-candidate deep-dive markdown freshness."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_strongest_candidate_deep_dive as builder


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_strongest_candidate_deep_dive_doc(args)
    if failures:
        for failure in failures:
            print(f"strongest-candidate deep-dive doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"strongest-candidate deep-dive doc ok: {args.markdown_out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claim-catalog", type=Path, default=builder.DEFAULT_CLAIM_CATALOG)
    parser.add_argument("--doxa-paired", type=Path, default=builder.DEFAULT_DOXA_PAIRED)
    parser.add_argument("--doxa-context", type=Path, default=builder.DEFAULT_DOXA_CONTEXT)
    parser.add_argument("--compound-summary", type=Path, default=builder.DEFAULT_COMPOUND_SUMMARY)
    parser.add_argument("--gog-occurrences", type=Path, default=builder.DEFAULT_GOG_OCCURRENCES)
    parser.add_argument(
        "--greek-expanded-controls",
        type=Path,
        default=builder.DEFAULT_GREEK_EXPANDED_CONTROLS,
    )
    parser.add_argument(
        "--greek-expanded-selected",
        type=Path,
        default=builder.DEFAULT_GREEK_EXPANDED_SELECTED,
    )
    parser.add_argument("--kjva-confirmatory", type=Path, default=builder.DEFAULT_KJVA_CONFIRMATORY)
    parser.add_argument("--kjva-prospective", type=Path, default=builder.DEFAULT_KJVA_PROSPECTIVE)
    parser.add_argument(
        "--kjva-prospective-bridge",
        type=Path,
        default=builder.DEFAULT_KJVA_PROSPECTIVE_BRIDGE,
    )
    parser.add_argument("--out", type=Path, default=builder.DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=builder.DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=builder.DEFAULT_MANIFEST)
    return parser


def validate_strongest_candidate_deep_dive_doc(
    args: argparse.Namespace | None = None,
) -> list[str]:
    args = args or build_parser().parse_args([])
    inputs = [
        args.claim_catalog,
        args.doxa_paired,
        args.doxa_context,
        args.compound_summary,
        args.gog_occurrences,
        args.greek_expanded_controls,
        args.greek_expanded_selected,
        args.kjva_confirmatory,
        args.kjva_prospective,
        args.kjva_prospective_bridge,
        args.out,
        args.markdown_out,
        args.manifest_out,
    ]
    for path in inputs:
        if not path.exists():
            return [f"{path} is missing"]
    candidates = builder.build_candidates(args)
    failures: list[str] = []
    failures.extend(validate_candidates_csv(args.out, candidates))
    failures.extend(validate_manifest(args.manifest_out, args, candidates))
    expected = builder.render_markdown(candidates, args)
    actual = args.markdown_out.read_text(encoding="utf-8")
    if actual != expected:
        failures.append(
            f"{args.markdown_out} is stale; rerun python3 -m scripts.build_strongest_candidate_deep_dive"
        )
    return failures


def validate_candidates_csv(
    path: Path,
    candidates: list[dict[str, str]],
) -> list[str]:
    data = _read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != builder.FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if rows != candidates:
        failures.append(f"{path} candidate rows drifted")
    return failures


def validate_manifest(
    path: Path,
    args: argparse.Namespace,
    candidates: list[dict[str, str]],
) -> list[str]:
    data = _read_json(path)
    if isinstance(data, str):
        return [data]
    failures: list[str] = []
    checks: dict[str, Any] = {
        "tool": "build_strongest_candidate_deep_dive",
        "inputs": {
            "claim_catalog": str(args.claim_catalog),
            "doxa_paired": str(args.doxa_paired),
            "doxa_context": str(args.doxa_context),
            "compound_summary": str(args.compound_summary),
            "gog_occurrences": str(args.gog_occurrences),
            "greek_expanded_controls": str(args.greek_expanded_controls),
            "greek_expanded_selected": str(args.greek_expanded_selected),
            "kjva_confirmatory": str(args.kjva_confirmatory),
            "kjva_prospective": str(args.kjva_prospective),
            "kjva_prospective_bridge": str(args.kjva_prospective_bridge),
        },
        "outputs": {
            "candidates": str(args.out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "candidate_rows": len(candidates),
        "candidate_ids": [row["candidate_id"] for row in candidates],
    }
    for key, expected in checks.items():
        if data.get(key) != expected:
            failures.append(f"{path} {key} drifted")
    return failures


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def _read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
