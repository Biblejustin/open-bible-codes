#!/usr/bin/env python3
"""Premise test: is centered-code density higher in the Bible than in known
human-authored text?

For each corpus, derive ITS OWN top content words (length >= 4, non-stopword,
by surface frequency: this auto-captures protagonist names and key topics), run
ELS, and measure how often an ELS of a word centers on a surface occurrence of
that same word (exact-center, the project's centered_self_exact_word). Compare
the Bible against language-matched secular controls (Homer/Herodotus in Greek;
Moby Dick / War and Peace / Shakespeare in English).

Same selection rule and same skip range for every corpus, so the comparison is
apples-to-apples. Pure data: the metric is exact-center density; no claim about
authorship is asserted, only measured.

Metrics per corpus (aggregated over its term set):
  exact_center_per_million_positions = 1e6 * exact_center_hits / legal_positions
  exact_center_per_1000_surface      = 1000 * exact_center_hits / surface_occurrences
  exact_center_fraction              = exact_center_hits / total_hits

Outputs under reports/centered_code_density/.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els.corpus import load_corpus
from els.search import find_els
from els.statistics import estimated_search_space
from els.word_counts import STOPWORDS_BY_LANGUAGE

OUT_DIR = Path("reports/centered_code_density")
MIN_SKIP, MAX_SKIP = 2, 15
TOP_N = 20
MIN_LEN = 4
MAX_HITS = 60000  # uniform per-term cap so common words don't blow up runtime

CORPORA = [
    ("BibleGreek_SBLGNT", "configs/example_sblgnt.toml", "greek"),
    ("Greek_Iliad", "configs/nonbible_greek_perseus_iliad.toml", "greek"),
    ("Greek_Odyssey", "configs/nonbible_greek_perseus_odyssey.toml", "greek"),
    ("Greek_Herodotus", "configs/nonbible_greek_perseus_herodotus.toml", "greek"),
    ("BibleEnglish_KJV", "configs/example_ebible_engkjv.toml", "english"),
    ("English_MobyDick", "configs/nonbible_english_pg_moby_dick.toml", "english"),
    ("English_WarAndPeace", "configs/nonbible_english_pg_war_and_peace.toml", "english"),
    ("English_Shakespeare", "configs/nonbible_english_pg_shakespeare.toml", "english"),
]

ENGLISH_STOP = {
    "that", "with", "this", "have", "from", "they", "were", "been", "their",
    "what", "when", "said", "which", "would", "there", "then", "them", "into",
    "your", "more", "than", "upon", "shall", "unto", "thou", "thee", "thy",
    "and", "the", "for", "not", "but", "you", "him", "her", "his", "its",
}


def top_terms(corpus, language: str) -> list[tuple[str, int]]:
    stop = set(STOPWORDS_BY_LANGUAGE.get(language, set())) | (ENGLISH_STOP if language == "english" else set())
    freq: Counter[str] = Counter()
    for w in corpus.words:
        nw = w.normalized_word
        if len(nw) >= MIN_LEN and nw not in stop:
            freq[nw] += 1
    return freq.most_common(TOP_N)


def analyze(label: str, config: str, language: str) -> dict:
    corpus = load_corpus(config)
    terms = top_terms(corpus, language)
    text_len = len(corpus.text)
    rows = []
    tot_hits = tot_center = tot_surface = tot_positions = 0
    for term, surface in terms:
        total = center = 0
        for hit in find_els(corpus, term, min_skip=MIN_SKIP, max_skip=MAX_SKIP,
                            direction="both", max_hits=MAX_HITS):
            total += 1
            if hit.center_normalized_word == term:
                center += 1
        legal = estimated_search_space(text_len, len(term), MIN_SKIP, MAX_SKIP, "both")
        rows.append({
            "corpus": label, "term": term, "surface_occurrences": surface,
            "total_els_hits": total, "exact_center_hits": center,
            "legal_positions": legal,
        })
        tot_hits += total; tot_center += center; tot_surface += surface; tot_positions += legal
    summary = {
        "corpus": label, "language": language, "letters": text_len,
        "terms": len(terms),
        "total_els_hits": tot_hits, "exact_center_hits": tot_center,
        "surface_occurrences": tot_surface,
        "exact_center_per_million_positions": round(1e6 * tot_center / tot_positions, 4) if tot_positions else 0.0,
        "exact_center_per_1000_surface": round(1000 * tot_center / tot_surface, 4) if tot_surface else 0.0,
        "exact_center_fraction": round(tot_center / tot_hits, 6) if tot_hits else 0.0,
    }
    return {"summary": summary, "rows": rows}


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summaries, detail = [], []
    for label, config, language in CORPORA:
        try:
            result = analyze(label, config, language)
        except Exception as exc:  # missing corpus / unsupported language
            print(f"  SKIP {label}: {type(exc).__name__}: {str(exc)[:80]}")
            continue
        summaries.append(result["summary"])
        detail.extend(result["rows"])
        s = result["summary"]
        print(f"  {label:24s} lang={language:7s} letters={s['letters']:>8} "
              f"center/Mpos={s['exact_center_per_million_positions']:>9} "
              f"center/1k_surf={s['exact_center_per_1000_surface']:>8} "
              f"center_frac={s['exact_center_fraction']}")

    with (OUT_DIR / "summary.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(summaries[0].keys())); w.writeheader(); w.writerows(summaries)
    with (OUT_DIR / "by_term.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(detail[0].keys())); w.writeheader(); w.writerows(detail)
    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "centered_code_density", "created_utc": datetime.now(UTC).isoformat(),
        "min_skip": MIN_SKIP, "max_skip": MAX_SKIP, "top_n_terms": TOP_N,
        "min_term_length": MIN_LEN, "max_hits_per_term": MAX_HITS,
        "selection": "each corpus's own top content words by surface frequency",
        "secular_sources": "Project Gutenberg / Perseus, language-matched",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n", OUT_DIR / "summary.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
