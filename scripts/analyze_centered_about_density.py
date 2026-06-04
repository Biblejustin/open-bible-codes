#!/usr/bin/env python3
"""Premise test, stronger form: density of centered codes whose local context is
ABOUT the centered term, Bible vs language-matched human-authored text.

Refines analyze_centered_code_density. A hit counts as "centered_about" when:
  1. it is exact-center (the ELS center lands on a surface token equal to the
     term W), AND
  2. the term is locally repeated: W occurs as surface text >= ABOUT_MIN times
     within +/-WINDOW words of the center (the surrounding passage is about W).

A fixed word window is used as the common "sentence-scale" unit because the
secular control texts load as one segment with no verse structure; the same rule
is applied to every corpus, so the comparison is fair. Each corpus is searched
with its OWN top content words (auto-captures protagonists/topics).

Pure data. Outputs under reports/centered_code_density/ (about_* files).
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
MAX_HITS = 60000
WINDOW = 10      # words on each side of the center
ABOUT_MIN = 2    # surface occurrences of the term within the window (incl. center)

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
}


def top_terms(corpus, language):
    stop = set(STOPWORDS_BY_LANGUAGE.get(language, set())) | (ENGLISH_STOP if language == "english" else set())
    freq: Counter[str] = Counter()
    for w in corpus.words:
        nw = w.normalized_word
        if len(nw) >= MIN_LEN and nw not in stop:
            freq[nw] += 1
    return freq.most_common(TOP_N)


def about(corpus, center_offset: int, term: str) -> bool:
    """True if `term` recurs as surface text within +/-WINDOW words of center."""
    if not corpus.position_to_word:
        return False
    idx = corpus.position_to_word[center_offset]
    lo, hi = max(0, idx - WINDOW), min(len(corpus.words) - 1, idx + WINDOW)
    count = sum(1 for j in range(lo, hi + 1) if corpus.words[j].normalized_word == term)
    return count >= ABOUT_MIN


def analyze(label, config, language):
    corpus = load_corpus(config)
    terms = top_terms(corpus, language)
    text_len = len(corpus.text)
    tot_hits = tot_center = tot_about = tot_surface = tot_positions = 0
    rows = []
    for term, surface in terms:
        total = center = about_n = 0
        for hit in find_els(corpus, term, min_skip=MIN_SKIP, max_skip=MAX_SKIP,
                            direction="both", max_hits=MAX_HITS):
            total += 1
            if hit.center_normalized_word == term:
                center += 1
                if about(corpus, hit.center_offset, term):
                    about_n += 1
        legal = estimated_search_space(text_len, len(term), MIN_SKIP, MAX_SKIP, "both")
        rows.append({"corpus": label, "term": term, "surface_occurrences": surface,
                     "total_els_hits": total, "exact_center_hits": center,
                     "centered_about_hits": about_n, "legal_positions": legal})
        tot_hits += total; tot_center += center; tot_about += about_n
        tot_surface += surface; tot_positions += legal
    summary = {
        "corpus": label, "language": language, "letters": text_len, "terms": len(terms),
        "exact_center_hits": tot_center, "centered_about_hits": tot_about,
        "about_per_million_positions": round(1e6 * tot_about / tot_positions, 5) if tot_positions else 0.0,
        "about_per_1000_surface": round(1000 * tot_about / tot_surface, 5) if tot_surface else 0.0,
        "about_fraction_of_centered": round(tot_about / tot_center, 4) if tot_center else 0.0,
    }
    return summary, rows


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summaries, detail = [], []
    for label, config, language in CORPORA:
        try:
            summary, rows = analyze(label, config, language)
        except Exception as exc:
            print(f"  SKIP {label}: {type(exc).__name__}: {str(exc)[:80]}")
            continue
        summaries.append(summary); detail.extend(rows)
        print(f"  {label:24s} centered={summary['exact_center_hits']:>5} "
              f"centered_about={summary['centered_about_hits']:>4} "
              f"about/Mpos={summary['about_per_million_positions']:>9} "
              f"about/1k_surf={summary['about_per_1000_surface']:>8} "
              f"about_frac={summary['about_fraction_of_centered']}")
    with (OUT_DIR / "about_summary.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(summaries[0].keys())); w.writeheader(); w.writerows(summaries)
    with (OUT_DIR / "about_by_term.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(detail[0].keys())); w.writeheader(); w.writerows(detail)
    (OUT_DIR / "about_manifest.json").write_text(json.dumps({
        "tool": "centered_about_density", "created_utc": datetime.now(UTC).isoformat(),
        "min_skip": MIN_SKIP, "max_skip": MAX_SKIP, "top_n_terms": TOP_N, "min_term_length": MIN_LEN,
        "window_words": WINDOW, "about_min_occurrences": ABOUT_MIN, "max_hits_per_term": MAX_HITS,
        "about_definition": "exact-center hit where the term recurs >= ABOUT_MIN times within +/-WINDOW words of center",
        "selection": "each corpus's own top content words by surface frequency",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n", OUT_DIR / "about_summary.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
