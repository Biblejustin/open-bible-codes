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

- `preserved_by_byz_and_tcg`: 193.
- `preserved_by_byz`: 0.
- `preserved_by_tcg`: 165.
- `tr_specific_under_equivalent_offsets`: 287.

Comparison status counts:

- BYZ_NT preserved equivalent offsets: 193.
- BYZ_NT ref missing: 192.
- BYZ_NT coordinate mismatch: 175.
- BYZ_NT not preserved equivalent offsets: 85.
- TCG_NT preserved equivalent offsets: 358.
- TCG_NT ref missing: 192.
- TCG_NT coordinate mismatch: 66.
- TCG_NT not preserved equivalent offsets: 29.

## Cautions

- Raw break counts are not significance tests.
- Equivalent-offset mapping is conservative and can miss preservation after local wording-length changes.
- This is a robustness screen, not a textual-critical stemma.
