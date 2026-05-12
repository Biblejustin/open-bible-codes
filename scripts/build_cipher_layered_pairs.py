#!/usr/bin/env python3
"""Pair plain ELS hits with transformed-layer hits at the same anchor."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__

DEFAULT_ANCHOR_FIELDS = ("corpus_label", "term_id", "center_ref", "center_normalized_word")
DEFAULT_OUT = Path("reports/cipher_layered_pairs/pairs.csv")
DEFAULT_SUMMARY_OUT = Path("reports/cipher_layered_pairs/summary.csv")
DEFAULT_MANIFEST_OUT = Path("reports/cipher_layered_pairs/manifest.json")

FIELDNAMES = [
    "anchor_key",
    "corpus_label",
    "term_id",
    "concept",
    "center_ref",
    "center_word",
    "center_normalized_word",
    "plain_hit_index",
    "cipher_hit_index",
    "plain_skip",
    "cipher_skip",
    "plain_direction",
    "cipher_direction",
    "cipher_transform",
]

SUMMARY_FIELDS = ["bucket", "value", "pairs"]


@dataclass(frozen=True)
class LayerHit:
    hit_index: int
    layer: str
    row: dict[str, str]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    anchor_fields = tuple(args.anchor_field or DEFAULT_ANCHOR_FIELDS)
    plain_hits = read_layer_hits(args.plain_hits, layer="plain")
    cipher_hits = read_layer_hits(args.cipher_hits, layer="cipher")
    rows = cipher_layered_pair_rows(
        plain_hits,
        cipher_hits,
        anchor_fields=anchor_fields,
        max_pairs=args.max_pairs,
    )
    summary_rows = summarize_rows(rows)
    write_rows(args.out, rows)
    write_rows(args.summary_out, summary_rows, fieldnames=SUMMARY_FIELDS)
    write_manifest(
        args.manifest_out,
        args,
        anchor_fields=anchor_fields,
        plain_hits=plain_hits,
        cipher_hits=cipher_hits,
        rows=rows,
        summary_rows=summary_rows,
        started=started,
    )
    print(args.out)
    print(args.summary_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plain-hits", action="append", type=Path, required=True)
    parser.add_argument("--cipher-hits", action="append", type=Path, required=True)
    parser.add_argument(
        "--anchor-field",
        action="append",
        default=[],
        help="Field used in the pairing key. Repeatable. Defaults to corpus, term, center ref, and center word.",
    )
    parser.add_argument("--max-pairs", type=int, default=100_000)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST_OUT)
    return parser


def read_layer_hits(paths: list[Path], *, layer: str) -> list[LayerHit]:
    hits: list[LayerHit] = []
    for path in paths:
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                hits.append(LayerHit(hit_index=len(hits) + 1, layer=layer, row=dict(row)))
    return hits


def cipher_layered_pair_rows(
    plain_hits: list[LayerHit],
    cipher_hits: list[LayerHit],
    *,
    anchor_fields: tuple[str, ...] = DEFAULT_ANCHOR_FIELDS,
    max_pairs: int = 100_000,
) -> list[dict[str, object]]:
    if not anchor_fields:
        raise ValueError("at least one anchor field is required")
    if max_pairs < 1:
        raise ValueError("max_pairs must be >= 1")

    plain_by_key: dict[tuple[str, ...], list[LayerHit]] = defaultdict(list)
    for hit in plain_hits:
        plain_by_key[anchor_key(hit.row, anchor_fields)].append(hit)

    output: list[dict[str, object]] = []
    for cipher_hit in cipher_hits:
        key = anchor_key(cipher_hit.row, anchor_fields)
        for plain_hit in plain_by_key.get(key, []):
            output.append(pair_row(plain_hit, cipher_hit, key))
            if len(output) >= max_pairs:
                return output
    return output


def anchor_key(row: dict[str, str], fields: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(normalized_field_value(row, field) for field in fields)


def normalized_field_value(row: dict[str, str], field: str) -> str:
    if field == "corpus_label":
        return row.get("corpus_label", "") or row.get("corpus", "") or row.get("base_corpus", "")
    return row.get(field, "")


def pair_row(plain_hit: LayerHit, cipher_hit: LayerHit, key: tuple[str, ...]) -> dict[str, object]:
    plain = plain_hit.row
    cipher = cipher_hit.row
    return {
        "anchor_key": "|".join(key),
        "corpus_label": normalized_field_value(plain, "corpus_label"),
        "term_id": plain.get("term_id", "") or cipher.get("term_id", ""),
        "concept": plain.get("concept", "") or cipher.get("concept", ""),
        "center_ref": plain.get("center_ref", "") or cipher.get("center_ref", ""),
        "center_word": plain.get("center_word", "") or cipher.get("center_word", ""),
        "center_normalized_word": (
            plain.get("center_normalized_word", "") or cipher.get("center_normalized_word", "")
        ),
        "plain_hit_index": plain_hit.hit_index,
        "cipher_hit_index": cipher_hit.hit_index,
        "plain_skip": plain.get("skip", ""),
        "cipher_skip": cipher.get("skip", ""),
        "plain_direction": plain.get("direction", ""),
        "cipher_direction": cipher.get("direction", ""),
        "cipher_transform": cipher.get("transform", ""),
    }


def summarize_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    transform_counts = Counter(str(row.get("cipher_transform", "")) for row in rows)
    corpus_counts = Counter(str(row.get("corpus_label", "")) for row in rows)
    term_counts = Counter(str(row.get("term_id", "")) for row in rows)
    summary_rows: list[dict[str, object]] = []
    for bucket, counts in (
        ("cipher_transform", transform_counts),
        ("corpus_label", corpus_counts),
        ("term_id", term_counts),
    ):
        for value, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
            summary_rows.append({"bucket": bucket, "value": value, "pairs": count})
    return summary_rows


def write_rows(path: Path, rows: list[dict[str, object]], *, fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames or FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    *,
    anchor_fields: tuple[str, ...],
    plain_hits: list[LayerHit],
    cipher_hits: list[LayerHit],
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
) -> None:
    payload: dict[str, Any] = {
        "script": "scripts/build_cipher_layered_pairs.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "git_commit": git_commit(),
        "anchor_fields": list(anchor_fields),
        "max_pairs": args.max_pairs,
        "plain_hit_rows": len(plain_hits),
        "cipher_hit_rows": len(cipher_hits),
        "paired_rows": len(rows),
        "summary_rows": len(summary_rows),
        "inputs": {
            "plain_hits": [str(path) for path in args.plain_hits],
            "cipher_hits": [str(path) for path in args.cipher_hits],
        },
        "outputs": {
            "out": str(args.out),
            "summary_out": str(args.summary_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
