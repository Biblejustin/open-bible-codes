#!/usr/bin/env python3
"""Check whether the John 8:6 Jesus ELS is destroyed by Pericope removal."""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path

from els.corpus import Corpus, load_corpus
from els.critical import TermBreakStats, classify_missing_verses, count_breaks_for_blocks
from els.search import find_els, normalize_for_corpus
from scripts.analyze_critical_omission_breaks import normalize_ref_label


SBL_CONFIG = Path("configs/example_sblgnt.toml")
BYZ_CONFIG = Path("configs/example_ebible_grcmt.toml")
OVERRIDE = Path("protocols/treat_as_deleted/critical_consensus.csv")
OUT = Path("reports/critical_omission_breaks_pericope_inverse.csv")
MANIFEST = Path("reports/critical_omission_breaks_pericope_inverse.manifest.json")


def main() -> int:
    rows = []
    for label, config in [("SBLGNT", SBL_CONFIG), ("BYZ_NT", BYZ_CONFIG)]:
        corpus = load_corpus(config)
        refs = pericope_refs_for_corpus(corpus)
        blocks = [
            block
            for block in classify_missing_verses(corpus, corpus, extra_deleted_refs=refs)
            if block.used_as_deletion
        ]
        normalized = normalize_for_corpus(corpus, "Ἰησοῦς")
        stats = TermBreakStats(0, {"term": "Ἰησοῦς", "term_id": "iesous_g"}, normalized)
        total, _per_block, broken = count_breaks_for_blocks(
            corpus,
            {normalized: [stats]},
            blocks,
            min_skip=192,
            max_skip=192,
            direction="backward",
        )
        documented_hits = [
            hit
            for hit in find_els(corpus, "Ἰησοῦς", min_skip=192, max_skip=192, direction="backward")
            if hit.center_ref in refs and hit.center_ref.endswith("8:6")
        ]
        rows.append(
            {
                "corpus": label,
                "pericope_refs": len(refs),
                "documented_jesus_center_hits": len(documented_hits),
                "broken_after_removal": total,
                "status": "destroyed" if documented_hits and total else "not_confirmed",
            }
        )
    write_rows(OUT, rows)
    MANIFEST.write_text(
        json.dumps(
            {
                "tool": "pericope_inverse_check",
                "created_utc": datetime.now(UTC).isoformat(),
                "override": str(OVERRIDE.resolve()),
                "out": str(OUT.resolve()),
                "rows": len(rows),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUT)
    print(MANIFEST)
    return 0


def pericope_refs_for_corpus(corpus: Corpus) -> set[str]:
    style = "sbl" if any(verse.ref == "John 8:6" for verse in corpus.verses) else "ebible"
    refs = set()
    with OVERRIDE.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("passage") != "Pericope Adulterae":
                continue
            ref = row["ref"]
            refs.add(ref if style == "sbl" else normalize_ref_label(ref))
    return refs


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
