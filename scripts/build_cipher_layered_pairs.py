#!/usr/bin/env python3
"""Pair plain ELS hits with transformed-layer hits at the same anchor."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


DEFAULT_ANCHOR_FIELDS = ("corpus_label", "term_id", "center_ref", "center_normalized_word")

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


@dataclass(frozen=True)
class LayerHit:
    hit_index: int
    layer: str
    row: dict[str, str]


def main(argv: list[str] | None = None) -> int:
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
    write_rows(args.out, rows)
    print(args.out)
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
    parser.add_argument("--out", type=Path, default=Path("reports/cipher_layered_pairs/pairs.csv"))
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


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
