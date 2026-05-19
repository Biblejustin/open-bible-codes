#!/usr/bin/env python3
"""Build ranked findings from the original-language exact-center packet."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els import __version__
from els.term_display import display_center, display_term


DEFAULT_REVIEW_PACKET = Path(
    "reports/dynamic_skip_focus/strong_full_span_exact_center_original_language_review_packet.csv"
)
DEFAULT_PATHS = Path(
    "reports/dynamic_skip_focus/strong_full_span_exact_center_original_language_review_paths.csv"
)
DEFAULT_OUT = Path(
    "reports/dynamic_skip_focus/strong_full_span_exact_center_original_language_findings.csv"
)
DEFAULT_MARKDOWN = Path(
    "docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_ORIGINAL_LANGUAGE_FINDINGS.md"
)
DEFAULT_MANIFEST = Path(
    "reports/dynamic_skip_focus/strong_full_span_exact_center_original_language_findings.manifest.json"
)

FIELDNAMES = [
    "finding_rank",
    "recommendation",
    "review_reason",
    "corpus",
    "term_id",
    "normalized_term",
    "center_ref",
    "center_word",
    "exact_center_paths",
    "path_rows_joined",
    "min_abs_skip",
    "max_abs_skip",
    "example_skip",
    "example_direction",
    "example_start_ref",
    "example_end_ref",
    "example_rows_spanned",
    "example_row_width",
    "surface_read",
    "control_read",
    "control_comparison",
    "manual_review_note",
    "center_word_context",
    "center_verse_excerpt",
]


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    review_rows = read_rows(args.review_packet)
    path_rows = read_rows(args.paths)
    findings = build_findings(review_rows, path_rows, limit=args.limit)
    write_csv(args.out, findings)
    write_markdown(args.markdown_out, findings, args)
    write_manifest(args.manifest_out, args, findings, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-packet", type=Path, default=DEFAULT_REVIEW_PACKET)
    parser.add_argument("--paths", type=Path, default=DEFAULT_PATHS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--markdown-row-limit", type=int, default=90)
    return parser


def build_findings(
    review_rows: list[dict[str, str]],
    path_rows: list[dict[str, str]],
    *,
    limit: int,
) -> list[dict[str, object]]:
    path_counts = Counter(row.get("review_rank", "") for row in path_rows)
    ranked = sorted(review_rows, key=lambda row: finding_sort_key(row, path_counts))
    if limit > 0:
        ranked = ranked[:limit]
    return [finding_row(index, row, path_counts) for index, row in enumerate(ranked, start=1)]


def finding_sort_key(row: dict[str, str], path_counts: Counter[str]) -> tuple[int, int, int, int]:
    recommendation = classify_recommendation(row)
    return (
        recommendation_order(recommendation),
        -interest_score(row, path_counts),
        -int_value(row.get("exact_center_paths", "")),
        int_value(row.get("review_rank", "")),
    )


def finding_row(index: int, row: dict[str, str], path_counts: Counter[str]) -> dict[str, object]:
    recommendation = classify_recommendation(row)
    return {
        "finding_rank": index,
        "recommendation": recommendation,
        "review_reason": review_reason(row, recommendation),
        "corpus": row.get("corpus", ""),
        "term_id": row.get("term_id", ""),
        "normalized_term": row.get("normalized_term", ""),
        "center_ref": row.get("center_ref", ""),
        "center_word": row.get("center_word", ""),
        "exact_center_paths": int_value(row.get("exact_center_paths", "")),
        "path_rows_joined": path_counts.get(row.get("review_rank", ""), 0),
        "min_abs_skip": int_value(row.get("min_abs_skip", "")),
        "max_abs_skip": int_value(row.get("max_abs_skip", "")),
        "example_skip": int_value(row.get("example_skip", "")),
        "example_direction": row.get("example_direction", ""),
        "example_start_ref": row.get("example_start_ref", ""),
        "example_end_ref": row.get("example_end_ref", ""),
        "example_rows_spanned": int_value(row.get("example_rows_spanned", "")),
        "example_row_width": int_value(row.get("example_row_width", "")),
        "surface_read": surface_read(row),
        "control_read": row.get("control_read", ""),
        "control_comparison": row.get("control_comparison", ""),
        "manual_review_note": manual_review_note(row, recommendation),
        "center_word_context": row.get("center_word_context", ""),
        "center_verse_excerpt": row.get("center_verse_excerpt", ""),
    }


def classify_recommendation(row: dict[str, str]) -> str:
    term = row.get("normalized_term", "")
    corpus = row.get("corpus", "")
    center_ref = row.get("center_ref", "")
    zero_control = has_zero_control_read(row)
    background_warning = has_background_warning(row)
    if term == "γωγ" and corpus == "TCG_NT" and center_ref == "REV 20:8" and zero_control:
        return "promote"
    if zero_control:
        return "hold"
    if term == "משיח" and center_ref == "DAN 9:26":
        return "hold"
    if background_warning:
        return "background"
    return "hold"


def interest_score(row: dict[str, str], path_counts: Counter[str]) -> int:
    score = min(int_value(row.get("exact_center_paths", "")), 100)
    score += min(path_counts.get(row.get("review_rank", ""), 0), 100)
    if has_zero_control_read(row):
        score += 150
    if has_background_warning(row):
        score -= 80
    if row.get("normalized_term") == "γωγ" and row.get("center_ref") == "REV 20:8":
        score += 80
    if row.get("normalized_term") == "משיח" and row.get("center_ref") == "DAN 9:26":
        score += 40
    if row.get("normalized_term") == "ιησουσ" and row.get("center_ref", "").startswith("JOS "):
        score += 20
    return score


def recommendation_order(value: str) -> int:
    if value == "promote":
        return 0
    if value == "hold":
        return 1
    if value == "background":
        return 2
    return 3


def review_reason(row: dict[str, str], recommendation: str) -> str:
    if recommendation == "promote":
        return "exact center on same surface term in thematically central passage, with zero observed language-matched control rows"
    if recommendation == "hold" and has_zero_control_read(row):
        return "zero observed language-matched control rows, but surface referent/version interpretation still needs manual review"
    if row.get("normalized_term") == "משיח" and row.get("center_ref") == "DAN 9:26":
        return "theologically important surface center; held because Hebrew controls also produce many exact-center rows"
    if recommendation == "background":
        return "surface-centered hit present, but language-matched controls also produce exact-center rows"
    return "review needed before classification"


def surface_read(row: dict[str, str]) -> str:
    term = row.get("normalized_term", "")
    corpus = row.get("corpus", "")
    if term == "ιησουσ" and corpus == "LXX":
        return "hidden term centers on open LXX Ιησους/Joshua form; read as Joshua/Yeshua surface anchor unless separately argued"
    if term == "ישוע":
        return "hidden term centers on open Hebrew Yeshua/Jeshua/Joshua surface word"
    if term == "משיח":
        return "hidden term centers on open Hebrew anointed/messiah surface word"
    if term == "γωγ":
        return "hidden term centers on open Greek Gog surface word"
    return "hidden term centers on matching surface word"


def manual_review_note(row: dict[str, str], recommendation: str) -> str:
    term = row.get("normalized_term", "")
    center_ref = row.get("center_ref", "")
    if recommendation == "promote":
        return (
            "Read all paths for Rev 20:8, then compare TR/BYZ/SBLGNT-style NT streams if available; "
            "this is the clearest current centered-self/contextual occurrence."
        )
    if term == "ιησουσ":
        return (
            "Check whether this is merely ordinary Joshua density in LXX Joshua/Deuteronomy/Nehemiah contexts; "
            "do not promote as a Jesus-of-Nazareth claim without separate contextual argument."
        )
    if term == "משיח" and center_ref == "DAN 9:26":
        return (
            "Manual-read Daniel 9:26 because the open surface term is theologically central; "
            "control background prevents claim promotion at this stage."
        )
    if term == "משיח":
        return "Review after Daniel 9:26; Bialik background rate for משיח is high."
    if term == "ישוע":
        return "Treat as background until source/version comparison and controls isolate something beyond Yeshua/Jeshua name density."
    return "Manual review required."


def has_zero_control_read(row: dict[str, str]) -> bool:
    return "zero exact-center rows" in row.get("control_read", "")


def has_background_warning(row: dict[str, str]) -> bool:
    return "background-rate warning" in row.get("control_read", "")


def int_value(value: object) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, object]], args: argparse.Namespace) -> None:
    lines = [
        "# Strong Full-Span Exact-Center Original-Language Findings",
        "",
        "This is a ranked findings writeup from the original-language exact-center",
        "review packet. It is not a claim report. The ranking keeps two questions",
        "separate: whether a hidden term centers on itself or a relevant surface",
        "word, and whether its frequency looks unusual under controls. `promote`",
        "means contextually ready for deeper manual/source comparison, `hold` means",
        "interesting but not claim-ready, and `background` means ordinary control",
        "pressure is currently the dominant frequency read.",
        "",
        "## Reproduce",
        "",
        "```bash",
        command_line(args),
        "```",
        "",
        "## Bottom Line",
        "",
    ]
    lines.extend(bottom_line(rows))
    lines.extend(scope_lines(rows, args))
    lines.extend(recommendation_lines(rows))
    lines.extend(findings_table_lines(rows[: args.markdown_row_limit]))
    lines.extend(read_lines())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def bottom_line(rows: list[dict[str, object]]) -> list[str]:
    promote = [row for row in rows if row["recommendation"] == "promote"]
    hold = [row for row in rows if row["recommendation"] == "hold"]
    background = [row for row in rows if row["recommendation"] == "background"]
    lines = [
        f"- `{len(promote)}` row is promoted for contextual centered-self review.",
        f"- `{len(hold)}` rows are held for manual/source comparison.",
        f"- `{len(background)}` rows are currently best read as background-pressure rows.",
        "- The promoted row is Greek "
        f"{display_term('γωγ', english='Gog')} in `TCG_NT` centered on open "
        f"{display_term('Γὼγ', english='Gog')} at `REV 20:8`; this is an existence/context finding, not a frequency claim.",
        "- LXX "
        f"{display_term('ιησουσ', english='Jesus/Joshua')} rows are control-zero in this run, "
        "but most center on ordinary Joshua/Yeshua surface contexts.",
        "- Hebrew "
        f"{display_term('ישוע', english='Yeshua/Jeshua')} and {display_term('משיח', english='Messiah/anointed one')} "
        "rows remain real exact-center rows, but Hebrew controls also produce exact-center rows for those normalized terms.",
        "",
    ]
    return lines


def scope_lines(rows: list[dict[str, object]], args: argparse.Namespace) -> list[str]:
    by_corpus = Counter(str(row["corpus"]) for row in rows)
    by_term = Counter(str(row["normalized_term"]) for row in rows)
    lines = [
        "## Scope",
        "",
        f"- findings rows: {len(rows):,}",
        f"- source review packet: `{args.review_packet}`",
        f"- findings CSV: `{args.out}`",
        "",
        "## Corpus Counts",
        "",
        "| Corpus | Rows |",
        "| --- | ---: |",
    ]
    for corpus, count in sorted(by_corpus.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {corpus} | {count:,} |")
    lines.extend(["", "## Term Counts", "", "| Term | Rows |", "| --- | ---: |"])
    for term, count in sorted(by_term.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {display_term(term)} | {count:,} |")
    lines.append("")
    return lines


def recommendation_lines(rows: list[dict[str, object]]) -> list[str]:
    by_recommendation = Counter(str(row["recommendation"]) for row in rows)
    lines = [
        "## Recommendation Counts",
        "",
        "| Recommendation | Rows |",
        "| --- | ---: |",
    ]
    for label in ["promote", "hold", "background"]:
        lines.append(f"| {label} | {by_recommendation[label]:,} |")
    lines.append("")
    return lines


def findings_table_lines(rows: list[dict[str, object]]) -> list[str]:
    lines = [
        "## Ranked Findings",
        "",
        "| Rank | Rec | Corpus | Term | Center | Paths | Example span | Control read | Manual note |",
        "| ---: | --- | --- | --- | --- | ---: | --- | --- | --- |",
    ]
    for row in rows:
        span = f"{row['example_start_ref']} -> {row['center_ref']} -> {row['example_end_ref']}"
        term = display_term(str(row["normalized_term"]))
        center = display_center(str(row["center_ref"]), str(row["center_word"]))
        lines.append(
            f"| {row['finding_rank']} | {row['recommendation']} | {row['corpus']} | "
            f"{term} | {center} | "
            f"{int(row['exact_center_paths']):,} | {md_cell(span)} | "
            f"{md_cell(row['control_read'])} | {md_cell(row['manual_review_note'])} |"
        )
    lines.append("")
    return lines


def read_lines() -> list[str]:
    return [
        "## Read",
        "",
        "- `promote` does not mean established; it means the row is worth the next manual/source-comparison pass.",
        "- Exact-center rows are intentionally broad: hidden term centered on the same open surface word, or on a related surface word, is meaningful enough to preserve as an occurrence.",
        "- Frequency counts and matched controls should travel with the row, but they should not erase the occurrence from the final report.",
        "- Hebrew "
        f"{display_term('ישוע', english='Yeshua/Jeshua')} and {display_term('משיח', english='Messiah/anointed one')} "
        "rows should not be discarded, but the Bialik control background must travel with every interpretation.",
        "- LXX "
        f"{display_term('ιησουσ', english='Jesus/Joshua')} rows need referent discipline because the same Greek spelling commonly represents Joshua/Yeshua in LXX contexts.",
        "- Next review should inspect the promoted "
        f"{display_term('γωγ', english='Gog')} row path-by-path, then sample the highest-ranked LXX "
        f"{display_term('ιησουσ', english='Jesus/Joshua')} rows by center passage.",
        "",
    ]


def command_line(args: argparse.Namespace) -> str:
    return (
        "python3 -m scripts.build_dynamic_span_exact_center_original_language_findings "
        f"--review-packet {args.review_packet} --paths {args.paths} --out {args.out} "
        f"--markdown-out {args.markdown_out} --manifest-out {args.manifest_out}"
    )


def md_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "tool": "build_dynamic_span_exact_center_original_language_findings",
        "edls_version": __version__,
        "generated_at": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "git_commit": git_commit(),
        "rows": len(rows),
        "inputs": {
            "review_packet": str(args.review_packet),
            "paths": str(args.paths),
        },
        "outputs": {
            "out": str(args.out),
            "markdown_out": str(args.markdown_out),
            "manifest_out": str(args.manifest_out),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git_commit() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


if __name__ == "__main__":
    raise SystemExit(main())
