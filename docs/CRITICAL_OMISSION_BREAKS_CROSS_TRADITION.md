# Critical Omission Breaks Cross Tradition

## Setup

Run:

```bash
python3 -m scripts.analyze_critical_omission_breaks_cross_tradition
```

Outputs:

- `reports/critical_omission_breaks_cross_tradition.csv`
- `reports/critical_omission_breaks_cross_tradition.manifest.json`

## Method

The script reads `reports/critical_omission_breaks_examples.csv`, then checks
each TR broken hit against:

- eBible Greek Majority Text NT (`configs/example_ebible_grcmt.toml`)
- eBible Text-Critical Greek NT (`configs/example_ebible_grctcgnt.toml`)

It maps start/end refs and verse-local offsets into the comparison corpus and
checks whether the same normalized term appears at the same skip.

## Results

Current output rows: 645, one per TR broken example row.

Classes:

- `preserved_by_byz_and_tcg`
- `preserved_by_byz`
- `preserved_by_tcg`
- `tr_specific_under_equivalent_offsets`

## Cautions

- Raw break counts are not significance tests.
- Equivalent-offset mapping is conservative and can miss preservation after local wording-length changes.
- This is a robustness screen, not a textual-critical stemma.
