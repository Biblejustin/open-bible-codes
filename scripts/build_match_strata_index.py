#!/usr/bin/env python3
"""Annotate centered occurrences with post-search match strata."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from els import __version__
from els.corpus import load_corpus
from els.gematria import standard_gematria_value
from els.match_strata import (
    BoundaryIndex,
    boundary_strata_for_offsets,
    build_boundary_index,
    canonical_first_keys,
    direction_counts_by_key,
    direction_strata_by_key,
    parse_skip_values,
    row_identity,
)
from els.term_display import display_term


DEFAULT_OCCURRENCES = Path("reports/centered_occurrence_index/centered_occurrences.csv")
DEFAULT_OUT = Path("reports/match_strata_index/occurrence_strata.csv")
DEFAULT_SUMMARY_OUT = Path("reports/match_strata_index/strata_summary.csv")
DEFAULT_MARKDOWN = Path("docs/MATCH_STRATA_INDEX.md")
DEFAULT_MANIFEST = Path("reports/match_strata_index/manifest.json")
DEFAULT_MEANINGFUL_CONSTANTS = Path("terms/meaningful_constants.csv")

GROUP_FIELDS = ("source_family", "source_queue", "corpus", "present_corpora", "term_id", "normalized_term")
DEFAULT_CORPUS_CONFIGS = (
    "MT_WLC=configs/example_oshb_wlc.toml",
    "UXLC=configs/example_uxlc.toml",
    "EBIBLE_WLC=configs/example_ebible_hebwlc.toml",
    "MAM=configs/example_mam.toml",
    "UHB=configs/example_uhb.toml",
    "LXX=configs/example_ebible_grclxx.toml",
    "KJV=configs/example_ebible_engkjv.toml",
    "KJVA=configs/example_ebible_engkjv_apocrypha.toml",
    "TR_NT=configs/example_ebible_grctr.toml",
    "SBLGNT=configs/example_sblgnt.toml",
    "BYZ_NT=configs/example_ebible_grcmt.toml",
    "TCG_NT=configs/example_ebible_grctcgnt.toml",
)
LETTER_PATH_RE = re.compile(r"^\d+:.+@.+:(?:canonical|apocrypha):(?P<position>-?\d+)$")

FIELDNAMES = [
    "occurrence_rank",
    "source_family",
    "source_queue",
    "corpus_class",
    "corpus",
    "present_corpora",
    "term_id",
    "concept",
    "category",
    "normalized_term",
    "center_ref",
    "center_word",
    "center_normalized_word",
    "occurrence_type",
    "skip",
    "direction",
    "skip_equals_meaningful_constant",
    "meaningful_constant_skips",
    "meaningful_constant_labels",
    "gematria_scheme",
    "term_gematria_value",
    "skip_equals_term_gematria",
    "term_gematria_matching_skips",
    "forward_direction_count",
    "backward_direction_count",
    "direction_stratum",
    "direction_imbalance_score",
    "canonical_first_centered_occurrence",
    "canonical_first_group",
    "boundary_strata",
    "boundary_corpora",
    "boundary_evidence",
    "cross_skip_pair_at_word",
    "cross_skip_pair_count",
    "cross_skip_pair_terms",
    "cross_skip_pair_skips",
    "extended_strata",
    "review_note",
    "source_record",
]

SUMMARY_FIELDNAMES = ["stratum", "rows"]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    input_rows = read_rows(args.occurrences)
    meaningful_constants = read_meaningful_constants(args.meaningful_constants)
    corpus_configs = corpus_config_map(args.corpus_config)
    boundary_indexes = load_boundary_indexes(corpus_configs)
    rows = build_strata_rows(
        input_rows,
        boundary_indexes=boundary_indexes,
        meaningful_constants=meaningful_constants,
    )
    summary_rows = build_summary_rows(rows)
    write_rows(args.out, FIELDNAMES, rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    write_markdown(args.markdown_out, rows, summary_rows, args)
    write_manifest(args.manifest_out, args, rows, summary_rows, started, corpus_configs=corpus_configs)
    print(args.out)
    print(args.summary_out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--occurrences", type=Path, default=DEFAULT_OCCURRENCES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--meaningful-constants", type=Path, default=DEFAULT_MEANINGFUL_CONSTANTS)
    parser.add_argument("--markdown-row-limit", type=int, default=80)
    parser.add_argument(
        "--corpus-config",
        action="append",
        default=[],
        help="Corpus label to config mapping, e.g. MT_WLC=configs/example_oshb_wlc.toml.",
    )
    return parser


def build_strata_rows(
    input_rows: list[dict[str, str]],
    *,
    boundary_indexes: dict[str, BoundaryIndex] | None = None,
    meaningful_constants: dict[int, str] | None = None,
) -> list[dict[str, object]]:
    direction_counts = direction_counts_by_key(input_rows, key_fields=GROUP_FIELDS)
    direction_by_key = direction_strata_by_key(input_rows, key_fields=GROUP_FIELDS)
    canonical_first = canonical_first_keys(input_rows, group_fields=GROUP_FIELDS)
    boundary_indexes = boundary_indexes or {}
    meaningful_constants = meaningful_constants or {}
    cross_skip = cross_skip_annotations(input_rows)
    output = []
    for row in input_rows:
        key = tuple(row.get(field, "") for field in GROUP_FIELDS)
        is_first = row_identity(row) in canonical_first
        counts = direction_counts[key]
        boundary_strata, boundary_corpora, boundary_evidence = boundary_annotations(row, boundary_indexes)
        cross = cross_skip.get(row_identity(row), {})
        skip_values = sorted({abs(value) for value in parse_skip_values(row.get("skip", ""))})
        constant_skips = [value for value in skip_values if value in meaningful_constants]
        gematria_scheme, term_gematria_value = standard_gematria_value(
            row.get("normalized_term", ""),
            row.get("language", ""),
        )
        gematria_skips = [value for value in skip_values if term_gematria_value > 0 and value == term_gematria_value]
        strata = [
            row.get("occurrence_type", ""),
            direction_by_key.get(key, ""),
            *boundary_strata,
        ]
        if is_first:
            strata.append("canonical_first_occurrence")
        if cross:
            strata.append("cross_skip_pair_at_word")
        if constant_skips:
            strata.append("skip_equals_meaningful_constant")
        if gematria_skips:
            strata.append("skip_equals_term_gematria")
        output.append(
            {
                "occurrence_rank": row.get("occurrence_rank", ""),
                "source_family": row.get("source_family", ""),
                "source_queue": row.get("source_queue", ""),
                "corpus_class": row.get("corpus_class", ""),
                "corpus": row.get("corpus", ""),
                "present_corpora": row.get("present_corpora", ""),
                "term_id": row.get("term_id", ""),
                "concept": row.get("concept", ""),
                "category": row.get("category", ""),
                "normalized_term": row.get("normalized_term", ""),
                "center_ref": row.get("center_ref", ""),
                "center_word": row.get("center_word", ""),
                "center_normalized_word": row.get("center_normalized_word", ""),
                "occurrence_type": row.get("occurrence_type", ""),
                "skip": row.get("skip", ""),
                "direction": row.get("direction", ""),
                "skip_equals_meaningful_constant": "yes" if constant_skips else "no",
                "meaningful_constant_skips": ";".join(str(value) for value in constant_skips),
                "meaningful_constant_labels": ";".join(meaningful_constants[value] for value in constant_skips),
                "gematria_scheme": gematria_scheme,
                "term_gematria_value": str(term_gematria_value) if term_gematria_value else "",
                "skip_equals_term_gematria": "yes" if gematria_skips else "no",
                "term_gematria_matching_skips": ";".join(str(value) for value in gematria_skips),
                "forward_direction_count": counts.forward,
                "backward_direction_count": counts.backward,
                "direction_stratum": direction_by_key.get(key, ""),
                "direction_imbalance_score": direction_imbalance_score(counts.forward, counts.backward),
                "canonical_first_centered_occurrence": "yes" if is_first else "no",
                "canonical_first_group": "|".join(key),
                "boundary_strata": ";".join(boundary_strata),
                "boundary_corpora": ";".join(boundary_corpora),
                "boundary_evidence": ";".join(boundary_evidence),
                "cross_skip_pair_at_word": "yes" if cross else "no",
                "cross_skip_pair_count": cross.get("pair_count", "") if cross else "",
                "cross_skip_pair_terms": cross.get("terms", "") if cross else "",
                "cross_skip_pair_skips": cross.get("skips", "") if cross else "",
                "extended_strata": ";".join(value for value in strata if value),
                "review_note": row.get("review_note", ""),
                "source_record": row.get("source_record", ""),
            }
        )
    return output


def build_summary_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    counts: Counter[str] = Counter()
    for row in rows:
        for stratum in str(row.get("extended_strata", "")).split(";"):
            if stratum:
                counts[stratum] += 1
    return [{"stratum": key, "rows": value} for key, value in sorted(counts.items(), key=lambda item: (-item[1], item[0]))]


def direction_imbalance_score(forward: int, backward: int) -> str:
    total = forward + backward
    if total == 0:
        return ""
    return f"{(forward - backward) / total:.6f}"


def cross_skip_annotations(rows: list[dict[str, str]]) -> dict[tuple[str, ...], dict[str, str]]:
    groups: dict[tuple[str, ...], list[dict[str, str]]] = {}
    for row in rows:
        groups.setdefault(cross_skip_group_key(row), []).append(row)

    annotations: dict[tuple[str, ...], dict[str, str]] = {}
    for group_rows in groups.values():
        if len({row.get("normalized_term", "") for row in group_rows}) < 2:
            continue
        skip_sets = {row_identity(row): set(parse_skip_values(row.get("skip", ""))) for row in group_rows}
        for row in group_rows:
            row_key = row_identity(row)
            row_skips = skip_sets[row_key]
            peer_rows = [
                peer
                for peer in group_rows
                if peer is not row
                and peer.get("normalized_term", "") != row.get("normalized_term", "")
                and has_different_skip(row_skips, skip_sets[row_identity(peer)])
            ]
            if not peer_rows:
                continue
            annotations[row_key] = {
                "pair_count": str(len(peer_rows)),
                "terms": ";".join(sorted({peer.get("normalized_term", "") for peer in peer_rows if peer.get("normalized_term")})),
                "skips": ";".join(
                    str(value)
                    for value in sorted({skip for peer in peer_rows for skip in skip_sets[row_identity(peer)]})
                ),
            }
    return annotations


def cross_skip_group_key(row: dict[str, str]) -> tuple[str, str, str, str, str, str, str]:
    return (
        row.get("source_family", ""),
        row.get("source_queue", ""),
        row.get("corpus", ""),
        row.get("present_corpora", ""),
        row.get("center_ref", ""),
        row.get("center_normalized_word", ""),
        row.get("center_word", ""),
    )


def has_different_skip(left: set[int], right: set[int]) -> bool:
    if not left or not right:
        return False
    return any(left_skip != right_skip for left_skip in left for right_skip in right)


def write_markdown(
    path: Path,
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    args: argparse.Namespace,
) -> None:
    lines = [
        "# Extended Match Strata Index",
        "",
        "This index annotates the current centered occurrence index with cheap",
        "post-search strata. It does not promote any row to claim status. The",
        "extra flags are review-prioritization metadata that still require the",
        "same preregistered controls described in `docs/HYPOTHESIS_ANALYSIS_FRAMEWORK.md`.",
        "",
        "## Reproduce",
        "",
        "```bash",
        reproduce_command(args),
        "```",
        "",
        "## Bottom Line",
        "",
        f"- annotated occurrence rows: {len(rows):,}",
        "- materialized now: `forward_only`, `backward_only`, `bidirectional_present`, `canonical_first_occurrence`, and available `boundary_*` endpoint strata.",
        "- meaningful skip strata use the locked constants file and standard Hebrew/Greek gematria only as review flags.",
        "- boundary strata are exact only when the source occurrence row retains endpoint offsets for a mapped corpus.",
        "",
        "## Strata Counts",
        "",
        "| Stratum | Rows |",
        "| --- | ---: |",
    ]
    for row in summary_rows:
        lines.append(f"| `{row['stratum']}` | {int(row['rows']):,} |")
    lines.extend(
        [
            "",
            "## Top Annotated Rows",
            "",
            "| Rank | Term | Center | Existing type | Direction stratum | Boundary strata | Canonical first | Source |",
            "| ---: | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows[: args.markdown_row_limit]:
        lines.append(markdown_row(row))
    if len(rows) > args.markdown_row_limit:
        lines.append(
            f"| ... | ... | ... | ... | ... | ... | ... | {len(rows) - args.markdown_row_limit:,} more rows in CSV |"
        )
    boundary_rows = [row for row in rows if row.get("boundary_strata")]
    if boundary_rows:
        lines.extend(
            [
                "",
                "## Boundary Rows",
                "",
                "| Rank | Term | Center | Boundary strata | Evidence | Source |",
                "| ---: | --- | --- | --- | --- | --- |",
            ]
        )
        for row in boundary_rows[: args.markdown_row_limit]:
            lines.append(boundary_markdown_row(row))
        if len(boundary_rows) > args.markdown_row_limit:
            lines.append(
                f"| ... | ... | ... | ... | ... | {len(boundary_rows) - args.markdown_row_limit:,} more boundary rows in CSV |"
            )
    cross_skip_rows = [row for row in rows if row.get("cross_skip_pair_at_word") == "yes"]
    if cross_skip_rows:
        lines.extend(
            [
                "",
                "## Cross-Skip Center Rows",
                "",
                "| Rank | Term | Center | Pair count | Peer terms | Skip values | Source |",
                "| ---: | --- | --- | ---: | --- | --- | --- |",
            ]
        )
        for row in cross_skip_rows[: args.markdown_row_limit]:
            lines.append(cross_skip_markdown_row(row))
        if len(cross_skip_rows) > args.markdown_row_limit:
            lines.append(
                f"| ... | ... | ... | ... | ... | ... | {len(cross_skip_rows) - args.markdown_row_limit:,} more cross-skip rows in CSV |"
            )
    meaningful_rows = [
        row
        for row in rows
        if row.get("skip_equals_meaningful_constant") == "yes" or row.get("skip_equals_term_gematria") == "yes"
    ]
    if meaningful_rows:
        lines.extend(
            [
                "",
                "## Meaningful Skip Rows",
                "",
                "| Rank | Term | Center | Skip | Constant match | Term gematria match | Source |",
                "| ---: | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in meaningful_rows[: args.markdown_row_limit]:
            lines.append(meaningful_skip_markdown_row(row))
        if len(meaningful_rows) > args.markdown_row_limit:
            lines.append(
                f"| ... | ... | ... | ... | ... | ... | {len(meaningful_rows) - args.markdown_row_limit:,} more meaningful-skip rows in CSV |"
            )
    lines.extend(
        [
            "",
            "## Read",
            "",
            "- `canonical_first_occurrence` means first centered occurrence within the current indexed family, not first hidden occurrence in every raw hit export.",
            "- Direction strata are computed per source family / queue / corpus set / term group.",
            "- Boundary strata are computed only from retained endpoint offsets, so blank boundary fields mean unavailable evidence, not proven absence.",
            "- `cross_skip_pair_at_word` means at least one other normalized term shares the same center word/reference in the indexed family at a different skip.",
            "- `skip_equals_meaningful_constant` and `skip_equals_term_gematria` are metadata flags; they do not change the search space or promote claim status.",
            "- Matrix, cipher, broader cross-skip, and cohort-density strata widen the review surface and need separate locked controls before claim language.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def boundary_markdown_row(row: dict[str, object]) -> str:
    term = display_term(str(row.get("normalized_term", "")), english=str(row.get("concept", "")))
    center = f"{row.get('center_ref', '')} {display_term(str(row.get('center_word', '')))}"
    return (
        f"| {row.get('occurrence_rank', '')} | {term} | {md_cell(center)} | "
        f"{md_cell(row.get('boundary_strata', ''))} | "
        f"{md_cell(row.get('boundary_evidence', ''))} | `{row.get('source_family', '')}` |"
    )


def cross_skip_markdown_row(row: dict[str, object]) -> str:
    term = display_term(str(row.get("normalized_term", "")), english=str(row.get("concept", "")))
    center = f"{row.get('center_ref', '')} {display_term(str(row.get('center_word', '')))}"
    return (
        f"| {row.get('occurrence_rank', '')} | {term} | {md_cell(center)} | "
        f"{row.get('cross_skip_pair_count', '')} | {md_cell(row.get('cross_skip_pair_terms', ''))} | "
        f"{md_cell(row.get('cross_skip_pair_skips', ''))} | `{row.get('source_family', '')}` |"
    )


def meaningful_skip_markdown_row(row: dict[str, object]) -> str:
    term = display_term(str(row.get("normalized_term", "")), english=str(row.get("concept", "")))
    center = f"{row.get('center_ref', '')} {display_term(str(row.get('center_word', '')))}"
    constant_match = ""
    if row.get("skip_equals_meaningful_constant") == "yes":
        constant_match = (
            f"{row.get('meaningful_constant_skips', '')}: "
            f"{row.get('meaningful_constant_labels', '')}"
        )
    gematria_match = ""
    if row.get("skip_equals_term_gematria") == "yes":
        gematria_match = (
            f"{row.get('term_gematria_matching_skips', '')} "
            f"({row.get('gematria_scheme', '')})"
        )
    return (
        f"| {row.get('occurrence_rank', '')} | {term} | {md_cell(center)} | "
        f"{md_cell(row.get('skip', ''))} | {md_cell(constant_match)} | "
        f"{md_cell(gematria_match)} | `{row.get('source_family', '')}` |"
    )


def markdown_row(row: dict[str, object]) -> str:
    term = display_term(str(row.get("normalized_term", "")), english=str(row.get("concept", "")))
    center = f"{row.get('center_ref', '')} {display_term(str(row.get('center_word', '')))}"
    return (
        f"| {row.get('occurrence_rank', '')} | {term} | {md_cell(center)} | "
        f"`{row.get('occurrence_type', '')}` | `{row.get('direction_stratum', '')}` | "
        f"{md_cell(row.get('boundary_strata', ''))} | "
        f"{row.get('canonical_first_centered_occurrence', '')} | `{row.get('source_family', '')}` |"
    )


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    started: float,
    *,
    corpus_configs: dict[str, str],
) -> None:
    payload: dict[str, Any] = {
        "script": "scripts/build_match_strata_index.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "git_commit": git_commit(),
        "rows": len(rows),
        "summary_rows": len(summary_rows),
        "materialized_strata": [row["stratum"] for row in summary_rows],
        "corpus_configs": corpus_configs,
        "inputs": {
            "occurrences": str(args.occurrences),
            "meaningful_constants": str(args.meaningful_constants),
        },
        "outputs": {
            "out": str(args.out),
            "summary_out": str(args.summary_out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_meaningful_constants(path: Path) -> dict[int, str]:
    constants: dict[int, str] = {}
    if not path.exists():
        return constants
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            try:
                value = int(row["value"])
            except (KeyError, ValueError):
                continue
            constants[value] = row.get("label", str(value)).strip() or str(value)
    return constants


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def corpus_config_map(overrides: list[str]) -> dict[str, str]:
    values = list(DEFAULT_CORPUS_CONFIGS)
    values.extend(overrides)
    output = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"invalid --corpus-config value: {value}")
        label, path = value.split("=", 1)
        output[label.strip()] = path.strip()
    return output


def load_boundary_indexes(configs: dict[str, str]) -> dict[str, BoundaryIndex]:
    indexes = {}
    for label, path in configs.items():
        try:
            indexes[label] = build_boundary_index(load_corpus(path))
        except FileNotFoundError:
            continue
    return indexes


def boundary_annotations(
    row: dict[str, str],
    boundary_indexes: dict[str, BoundaryIndex],
) -> tuple[list[str], list[str], list[str]]:
    strata_by_corpus: dict[str, tuple[str, ...]] = {}
    for corpus, start, end in offset_records(row):
        index = boundary_indexes.get(corpus)
        if index is None:
            continue
        strata = boundary_strata_for_offsets(start_offset=start, end_offset=end, boundary_index=index)
        if strata:
            strata_by_corpus[corpus] = strata
    strata = sorted({value for values in strata_by_corpus.values() for value in values})
    corpora = sorted(strata_by_corpus)
    evidence = [f"{corpus}:{','.join(strata_by_corpus[corpus])}" for corpus in corpora]
    return strata, corpora, evidence


def offset_records(row: dict[str, str]) -> list[tuple[str, int, int]]:
    records = parse_offset_triplets(row.get("offset_triplets", ""))
    if records:
        return records
    letter_path = row.get("letter_path", "")
    if not letter_path:
        return []
    positions = []
    for part in letter_path.split(";"):
        match = LETTER_PATH_RE.match(part.strip())
        if match:
            positions.append(int(match.group("position")))
    corpus = row.get("corpus", "")
    if not corpus or not positions:
        return []
    return [(corpus, positions[0], positions[-1])]


def parse_offset_triplets(value: str) -> list[tuple[str, int, int]]:
    records = []
    for part in str(value or "").split(";"):
        if ":" not in part or "/" not in part:
            continue
        corpus, offsets = part.split(":", 1)
        pieces = offsets.split("/")
        if len(pieces) != 3:
            continue
        try:
            records.append((corpus.strip(), int(pieces[0]), int(pieces[2])))
        except ValueError:
            continue
    return records


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def reproduce_command(args: argparse.Namespace) -> str:
    return (
        "python3 -m scripts.build_match_strata_index "
        f"--occurrences {args.occurrences} "
        f"--meaningful-constants {args.meaningful_constants} "
        f"--out {args.out} "
        f"--summary-out {args.summary_out} "
        f"--markdown-out {args.markdown_out} "
        f"--manifest-out {args.manifest_out}"
    )


def md_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
