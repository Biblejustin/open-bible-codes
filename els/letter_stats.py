"""Letter-frequency helpers for post-search review metadata."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class BigramProfile:
    counts: Counter[str]
    rare_threshold: int
    common_threshold: int

    @classmethod
    def from_text(cls, text: str) -> "BigramProfile":
        counts = Counter(text[index : index + 2] for index in range(max(len(text) - 1, 0)))
        if not counts:
            return cls(counts=counts, rare_threshold=0, common_threshold=0)
        values = sorted(counts.values())
        rare_threshold = values[min(len(values) - 1, max(int(len(values) * 0.10) - 1, 0))]
        common_threshold = values[min(len(values) - 1, int(len(values) * 0.90))]
        return cls(counts=counts, rare_threshold=rare_threshold, common_threshold=common_threshold)

    def classify_term(self, term: str) -> "BigramSurprise":
        bigrams = tuple(term[index : index + 2] for index in range(max(len(term) - 1, 0)))
        if not bigrams or not self.counts:
            return BigramSurprise(stratum="", evidence="", min_count=None, max_count=None)

        counts = tuple(self.counts.get(bigram, 0) for bigram in bigrams)
        rare = tuple(bigram for bigram, count in zip(bigrams, counts, strict=True) if count <= self.rare_threshold)
        common = tuple(bigram for bigram, count in zip(bigrams, counts, strict=True) if count >= self.common_threshold)
        if rare:
            stratum = "high_bigram_surprise"
            evidence = ";".join(f"{bigram}:{self.counts.get(bigram, 0)}" for bigram in rare)
        elif len(common) == len(bigrams):
            stratum = "low_bigram_surprise"
            evidence = ";".join(f"{bigram}:{self.counts[bigram]}" for bigram in common)
        else:
            stratum = ""
            evidence = ""

        return BigramSurprise(
            stratum=stratum,
            evidence=evidence,
            min_count=min(counts),
            max_count=max(counts),
        )


@dataclass(frozen=True)
class BigramSurprise:
    stratum: str
    evidence: str
    min_count: int | None
    max_count: int | None


@dataclass(frozen=True)
class LetterFrequencyProfile:
    counts: Counter[str]
    rare_threshold: int

    @classmethod
    def from_text(cls, text: str) -> "LetterFrequencyProfile":
        counts = Counter(text)
        if not counts:
            return cls(counts=counts, rare_threshold=0)
        values = sorted(counts.values())
        rare_threshold = values[min(len(values) - 1, max(int(len(values) * 0.10) - 1, 0))]
        return cls(counts=counts, rare_threshold=rare_threshold)

    def classify_term(self, term: str) -> "LetterFrequencyAnomaly":
        letters = tuple(term)
        if not letters or not self.counts:
            return LetterFrequencyAnomaly(stratum="", evidence="", min_count=None, max_count=None)

        counts = tuple(self.counts.get(letter, 0) for letter in letters)
        rare = tuple(letter for letter, count in zip(letters, counts, strict=True) if count <= self.rare_threshold)
        if rare:
            stratum = "letter_frequency_anomaly"
            evidence = ";".join(f"{letter}:{self.counts.get(letter, 0)}" for letter in rare)
        else:
            stratum = ""
            evidence = ""

        return LetterFrequencyAnomaly(
            stratum=stratum,
            evidence=evidence,
            min_count=min(counts),
            max_count=max(counts),
        )


@dataclass(frozen=True)
class LetterFrequencyAnomaly:
    stratum: str
    evidence: str
    min_count: int | None
    max_count: int | None
