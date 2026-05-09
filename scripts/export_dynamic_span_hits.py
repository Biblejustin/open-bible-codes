#!/usr/bin/env python3
"""Export full metadata for selected dynamic-span ELS hits."""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import tempfile
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

from els import __version__
from els.corpus import load_corpus
from els.search import build_hit, normalize_for_corpus


ROOT = Path(__file__).resolve().parents[1]
CPP_SOURCE = ROOT / "scripts/cpp/dynamic_span_hits.cpp"
DEFAULT_BINARY = ROOT / "data/cache/bin/dynamic_span_hits"
DEFAULT_TERMS = ROOT / "terms/dynamic_skip_focus_terms.csv"
DEFAULT_COUNTS = [
    ROOT / "reports/dynamic_skip_focus/english_full_span_pair_counts.csv",
    ROOT / "reports/dynamic_skip_focus/greek_full_span_pair_counts.csv",
    ROOT / "reports/dynamic_skip_focus/hebrew_full_span_pair_counts.csv",
    ROOT / "reports/dynamic_skip_focus/nonbible_english_full_span_pair_counts.csv",
    ROOT / "reports/dynamic_skip_focus/nonbible_greek_full_span_pair_counts.csv",
    ROOT / "reports/dynamic_skip_focus/nonbible_hebrew_full_span_pair_counts.csv",
]
DEFAULT_OUT = ROOT / "reports/dynamic_skip_focus/full_span_exported_hits.csv"
DEFAULT_SUMMARY_OUT = ROOT / "docs/DYNAMIC_SKIP_FULL_SPAN_HIT_EXPORT.md"
DEFAULT_MANIFEST = ROOT / "reports/dynamic_skip_focus/full_span_exported_hits.manifest.json"

DEFAULT_CORPORA = {
    "MT_WLC": "configs/example_oshb_wlc.toml",
    "UXLC": "configs/example_uxlc.toml",
    "MAM": "configs/example_mam.toml",
    "EBIBLE_WLC": "configs/example_ebible_hebwlc.toml",
    "UHB": "configs/example_uhb.toml",
    "LXX": "configs/example_ebible_grclxx.toml",
    "TR_NT": "configs/example_ebible_grctr.toml",
    "BYZ_NT": "configs/example_ebible_grcmt.toml",
    "TCG_NT": "configs/example_ebible_grctcgnt.toml",
    "SBLGNT": "configs/example_sblgnt.toml",
    "KJV": "configs/example_ebible_engkjv.toml",
    "HEB_PBY_BIALIK": "configs/nonbible_hebrew_pby_bialik.toml",
    "HEB_PBY_BRENNER": "configs/nonbible_hebrew_pby_brenner.toml",
    "HEB_PBY_AHAD_HAAM": "configs/nonbible_hebrew_pby_ahad_haam.toml",
    "GRC_PERSEUS_ILIAD": "configs/nonbible_greek_perseus_iliad.toml",
    "GRC_PERSEUS_ODYSSEY": "configs/nonbible_greek_perseus_odyssey.toml",
    "GRC_PERSEUS_HERODOTUS": "configs/nonbible_greek_perseus_herodotus.toml",
    "ENG_PG_SHAKESPEARE": "configs/nonbible_english_pg_shakespeare.toml",
    "ENG_PG_WAR_PEACE": "configs/nonbible_english_pg_war_and_peace.toml",
    "ENG_PG_MOBY_DICK": "configs/nonbible_english_pg_moby_dick.toml",
}

HIT_FIELDNAMES = [
    "corpus",
    "corpus_language",
    "term_id",
    "concept",
    "category",
    "term_language",
    "term",
    "normalized_term",
    "mode",
    "count_row_hit_count",
    "min_skip",
    "effective_max_skip",
    "skip",
    "direction",
    "start_offset",
    "end_offset",
    "span_letters",
    "sequence",
    "start_ref",
    "end_ref",
    "start_source",
    "end_source",
    "center_offset",
    "center_ref",
    "center_source",
    "center_word_index",
    "center_word",
    "center_normalized_word",
]

SUMMARY_FIELDNAMES = [
    "corpus",
    "term_id",
    "mode",
    "hit_count",
    "status",
    "exported_hits",
    "out",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    binary = build_binary(args.binary)
    terms = {row["term_id"]: row for row in read_rows(args.terms)}
    corpus_configs = corpus_config_map(args.corpus)
    selected, skipped = select_count_rows(read_many(args.counts or DEFAULT_COUNTS), args)
    summary_rows: list[dict[str, str]] = []
    exported_hits = 0

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HIT_FIELDNAMES)
        writer.writeheader()
        for (corpus_label, mode, direction, min_skip), rows in grouped_selected_rows(selected):
            if corpus_label not in corpus_configs:
                for row in rows:
                    summary_rows.append(summary_row(row, "skipped_missing_corpus_config", 0, args.out))
                continue
            corpus = load_corpus(corpus_configs[corpus_label])
            term_rows = prepared_terms(corpus, terms, rows)
            if not term_rows:
                for row in rows:
                    summary_rows.append(summary_row(row, "skipped_missing_term", 0, args.out))
                continue
            raw_hits = run_hit_exporter(
                binary,
                corpus.text,
                term_rows,
                min_skip=max(int(min_skip), args.min_abs_skip or int(min_skip)),
                max_skip=args.max_abs_skip,
                mode=mode,
                direction=direction,
                max_hits_per_term=args.max_export_hits,
            )
            raw_hits_by_term = group_by(raw_hits, "term_id")
            count_rows_by_term = {row["term_id"]: row for row in rows}
            term_meta_by_id = {row["term_id"]: row for row in term_rows}
            for term_id, hit_rows in raw_hits_by_term.items():
                count_row = count_rows_by_term[term_id]
                term_meta = term_meta_by_id[term_id]
                for raw_hit in hit_rows:
                    hit = build_hit(
                        corpus,
                        term_meta["term"],
                        term_meta["normalized_term"],
                        int(raw_hit["skip"]),
                        int(raw_hit["start_offset"]),
                        int(raw_hit["end_offset"]),
                    )
                    writer.writerow(export_row(corpus_label, corpus, term_meta, count_row, raw_hit, hit))
                exported_hits += len(hit_rows)
                status = "exported_all_hits"
                if args.max_export_hits > 0 and len(hit_rows) >= args.max_export_hits:
                    status = "exported_hit_cap_reached"
                summary_rows.append(summary_row(count_row, status, len(hit_rows), args.out))
            for row in rows:
                if row["term_id"] not in raw_hits_by_term:
                    summary_rows.append(summary_row(row, "exported_zero_hits", 0, args.out))

    summary_rows.extend(skipped)
    write_summary(args.summary_out, summary_rows, selected, skipped, exported_hits, args)
    write_manifest(args.manifest_out, args, summary_rows, exported_hits, started)
    print(args.out)
    print(args.summary_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--counts", type=Path, action="append", default=[])
    parser.add_argument("--terms", type=Path, default=DEFAULT_TERMS)
    parser.add_argument("--corpus", action="append", default=[])
    parser.add_argument("--mode", action="append", default=["full-span"])
    parser.add_argument("--term-id", action="append", default=[])
    parser.add_argument("--corpus-label", action="append", default=[])
    parser.add_argument("--max-count-row-hits", type=int, default=50_000)
    parser.add_argument("--max-export-hits", type=int, default=50_000)
    parser.add_argument("--min-abs-skip", type=int)
    parser.add_argument("--max-abs-skip", type=int)
    parser.add_argument("--include-dense", action="store_true")
    parser.add_argument("--include-zero", action="store_true")
    parser.add_argument("--binary", type=Path, default=DEFAULT_BINARY)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY_OUT)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    return parser


def build_binary(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    compiler = os.environ.get("CXX", "clang++")
    command = [compiler, "-O3", "-std=c++17", str(CPP_SOURCE), "-o", str(path)]
    source_mtime = CPP_SOURCE.stat().st_mtime_ns
    binary_mtime = path.stat().st_mtime_ns if path.exists() else -1
    if binary_mtime < source_mtime:
        subprocess.run(command, check=True)
    return path


def corpus_config_map(values: list[str]) -> dict[str, Path]:
    configs = {label: ROOT / path for label, path in DEFAULT_CORPORA.items()}
    for value in values:
        if "=" not in value:
            raise ValueError(f"expected LABEL=CONFIG for --corpus, got {value!r}")
        label, config = value.split("=", 1)
        configs[label] = Path(config)
    return configs


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_many(paths: Iterable[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        if not path.exists():
            continue
        for row in read_rows(path):
            item = dict(row)
            item["count_source_file"] = str(path)
            rows.append(item)
    return rows


def select_count_rows(
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    modes = set(args.mode)
    term_ids = set(args.term_id)
    corpus_labels = set(args.corpus_label)
    selected: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    for row in rows:
        if row.get("mode") not in modes:
            continue
        if term_ids and row.get("term_id") not in term_ids:
            continue
        if corpus_labels and row.get("corpus") not in corpus_labels:
            continue
        hit_count = int(row.get("hit_count") or 0)
        if hit_count == 0 and not args.include_zero:
            skipped.append(summary_row(row, "skipped_zero_hits", 0, Path("")))
        elif hit_count > args.max_count_row_hits and not args.include_dense:
            skipped.append(summary_row(row, "skipped_above_hit_threshold", 0, Path("")))
        else:
            selected.append(row)
    return selected, skipped


def grouped_selected_rows(rows: list[dict[str, str]]):
    groups: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[
            (
                row["corpus"],
                row["mode"],
                row.get("direction", "both") or "both",
                row.get("min_skip", "2") or "2",
            )
        ].append(row)
    return sorted(groups.items())


def prepared_terms(
    corpus,
    terms: dict[str, dict[str, str]],
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    output = []
    for row in rows:
        term = terms.get(row["term_id"])
        if term is None:
            continue
        normalized = normalize_for_corpus(corpus, term["term"])
        if not normalized:
            continue
        item = dict(term)
        item["normalized_term"] = normalized
        output.append(item)
    return output


def run_hit_exporter(
    binary: Path,
    text: str,
    terms: list[dict[str, str]],
    *,
    min_skip: int,
    max_skip: int | None = None,
    mode: str,
    direction: str,
    max_hits_per_term: int,
) -> list[dict[str, str]]:
    with tempfile.TemporaryDirectory(prefix="edls_dynamic_hits_") as tmp:
        tmp_path = Path(tmp)
        text_path = tmp_path / "text.txt"
        terms_path = tmp_path / "terms.tsv"
        out_path = tmp_path / "hits.csv"
        text_path.write_text(text, encoding="utf-8")
        with terms_path.open("w", encoding="utf-8", newline="") as handle:
            for term in terms:
                handle.write(f"{term['term_id']}\t{term['normalized_term']}\n")
        command = [
            str(binary),
            str(text_path),
            str(terms_path),
            str(min_skip),
            mode,
            direction,
            str(max_hits_per_term),
            str(out_path),
        ]
        if max_skip is not None:
            command.append(str(max_skip))
        subprocess.run(command, check=True)
        return read_rows(out_path)


def group_by(rows: list[dict[str, str]], key: str) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row[key]].append(row)
    return grouped


def export_row(
    corpus_label: str,
    corpus,
    term: dict[str, str],
    count_row: dict[str, str],
    raw_hit: dict[str, str],
    hit,
) -> dict[str, str | int]:
    row = hit.as_row()
    return {
        "corpus": corpus_label,
        "corpus_language": corpus.language,
        "term_id": term["term_id"],
        "concept": term.get("concept", ""),
        "category": term.get("category", ""),
        "term_language": term.get("language", ""),
        "term": term.get("term", ""),
        "normalized_term": term["normalized_term"],
        "mode": raw_hit["mode"],
        "count_row_hit_count": count_row.get("hit_count", ""),
        "min_skip": raw_hit["min_skip"],
        "effective_max_skip": raw_hit["effective_max_skip"],
        **row,
    }


def summary_row(row: dict[str, str], status: str, exported_hits: int, out: Path) -> dict[str, str]:
    return {
        "corpus": row.get("corpus", ""),
        "term_id": row.get("term_id", ""),
        "mode": row.get("mode", ""),
        "hit_count": row.get("hit_count", ""),
        "status": status,
        "exported_hits": str(exported_hits),
        "out": "" if not str(out) else str(out),
    }


def write_summary(
    path: Path,
    rows: list[dict[str, str]],
    selected: list[dict[str, str]],
    skipped: list[dict[str, str]],
    exported_hits: int,
    args: argparse.Namespace,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    status_counts = Counter(row["status"] for row in rows)
    lines = [
        "# Dynamic Full-Span Hit Export",
        "",
        "This report exports full hit metadata for dynamic-span count rows whose",
        "observed count is below the configured threshold. High-density rows are",
        "not discarded; they are deferred for partitioned export because they can",
        "contain millions or billions of paths.",
        "",
        "## Reproduce",
        "",
        "```bash",
        "python3 -m scripts.export_dynamic_span_hits --max-count-row-hits 50000",
        "```",
        "",
        "## Run Counts",
        "",
        f"- selected count rows: {len(selected):,}",
        f"- skipped count rows: {len(skipped):,}",
        f"- exported hit rows: {exported_hits:,}",
        f"- max count row hits: {args.max_count_row_hits:,}",
        f"- max export hits per term/corpus/mode: {args.max_export_hits:,}",
        f"- min abs skip override: {args.min_abs_skip or ''}",
        f"- max abs skip override: {args.max_abs_skip or ''}",
        f"- hit CSV: `{display_path(args.out)}`",
        "",
        "## Status Counts",
        "",
        "| Status | Rows |",
        "| --- | ---: |",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"| `{status}` | {count:,} |")
    lines.extend(
        [
            "",
            "## Exported Rows",
            "",
            "| Corpus | Term | Mode | Count row hits | Exported hits | Status |",
            "| --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in sorted(rows, key=lambda item: (item["status"], item["corpus"], item["term_id"], item["mode"])):
        if not row["status"].startswith("exported"):
            continue
        lines.append(
            f"| {row['corpus']} | `{row['term_id']}` | `{row['mode']}` "
            f"| {row['hit_count']} | {row['exported_hits']} | `{row['status']}` |"
        )
    lines.extend(
        [
            "",
            "## Deferred Rows",
            "",
            "| Corpus | Term | Mode | Count row hits | Status |",
            "| --- | --- | --- | ---: | --- |",
        ]
    )
    for row in sorted(rows, key=lambda item: (-int(item["hit_count"] or 0), item["corpus"], item["term_id"])):
        if row["status"] == "exported_all_hits":
            continue
        lines.append(
            f"| {row['corpus']} | `{row['term_id']}` | `{row['mode']}` "
            f"| {row['hit_count']} | `{row['status']}` |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    exported_hits: int,
    started: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {
        "script": "scripts/export_dynamic_span_hits.py",
        "version": __version__,
        "created_at": datetime.now(UTC).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "rows": len(rows),
        "exported_hits": exported_hits,
        "max_count_row_hits": args.max_count_row_hits,
        "max_export_hits": args.max_export_hits,
        "min_abs_skip": args.min_abs_skip,
        "max_abs_skip": args.max_abs_skip,
        "include_dense": args.include_dense,
        "git_commit": git_commit(),
    }
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return ""


if __name__ == "__main__":
    raise SystemExit(main())
