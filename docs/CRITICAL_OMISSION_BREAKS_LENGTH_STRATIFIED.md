# Critical Omission Breaks Length Stratified

## Setup

Run:

```bash
python3 -m scripts.analyze_critical_omission_breaks_length_stratified
```

Outputs:

- `reports/critical_omission_breaks_length_stratified.csv`
- `reports/critical_omission_breaks_length_stratified.manifest.json`

## Method

This post-processes the omission-break summary and recomputes total TR hits
for the same Greek term lists and skip range. For each term it writes:

- `total_tr_hits`
- `broken_hits`
- `break_rate`
- `naive_expected_break_rate`
- `ratio`

`naive_expected_break_rate = L * D / N`, where `L` is normalized term length,
`D` is deleted letters, and `N` is TR normalized letters.

## Results

Current output rows: 458.

Use high `ratio` rows as review prompts only. They show where observed break
rate is above a simple deleted-letter exposure baseline.

## Cautions

- Raw break counts are not significance tests.
- The naive expected rate ignores clustering, term frequency, lane structure, and verse-position effects.
- Short normalized terms can dominate both hit counts and apparent rates.
