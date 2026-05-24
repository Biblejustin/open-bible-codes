# Critical Omission Breaks Null

## Setup

Run:

```bash
python3 -m scripts.analyze_critical_omission_breaks_null --shuffles 1000 --seed 1
```

Outputs:

- `reports/critical_omission_breaks_null/summary.csv`
- `reports/critical_omission_breaks_null/null_distribution.csv`
- `reports/critical_omission_breaks_null/null_per_block.csv`
- `reports/critical_omission_breaks_null/manifest.json`

## Method

The observed analysis uses the same break engine as
`scripts.analyze_critical_omission_breaks`: a hit breaks if a deleted block
removes an ELS letter or changes spacing between retained letters.

The null shuffler places the same number of verse-aligned blocks in the TR
corpus, matching actual blocks by verse count and excluding actual omitted
refs. It currently matches verse count, not letter count.

## Results

Current 1000-shuffle protocol run:

- Observed breaks: 645.
- Null min/median/max: 556 / 727 / 913.
- Greater-or-equal tail: 0.9710.
- Lesser-or-equal tail: 0.0300.
- Per-block exploratory p-values and BH q-values are in
  `reports/critical_omission_breaks_null/null_per_block.csv`.

The protocol manifest is at:

- `reports/protocols/critical_omission_followups/protocol_run.manifest.json`

## Cautions

- Raw break counts are not significance tests.
- The default null matches verse count only; letter-count matching would answer a different question.
- Per-block p-values are exploratory and use BH q-values across blocks.
