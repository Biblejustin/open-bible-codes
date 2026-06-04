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

Current output rows: 558, one per TR broken example row.

Classes:

- `preserved_by_byz_and_tcg`: 163.
- `preserved_by_byz`: 0.
- `preserved_by_tcg`: 157.
- `tr_specific_under_equivalent_offsets`: 238.

Comparison status counts:

- BYZ_NT preserved equivalent offsets: 163.
- BYZ_NT ref missing: 192.
- BYZ_NT coordinate mismatch: 150.
- BYZ_NT not preserved equivalent offsets: 53.
- TCG_NT preserved equivalent offsets: 320.
- TCG_NT ref missing: 192.
- TCG_NT coordinate mismatch: 36.
- TCG_NT not preserved equivalent offsets: 10.

## Stage 1 Proximity (added)

The strict equivalent-offset test maps each TR hit's letter offsets verse-locally
into the comparison corpus and requires an exact match. It miscounts when
upstream word-length deltas (movable nu, article presence, verb-ending variants)
shift every offset even though the same ELS is physically present at the same
skip. For BYZ_NT that conservative mapping put 150 hits in `coordinate_mismatch`
that may in fact be preserved.

The script now also emits a proximity classification that tolerates those
deltas: `byz_proximity_status`, `tcg_proximity_status`,
`cross_tradition_class_proximity`, and `window_verses`. A hit is
`preserved_within_verse_span` when the same query occurs at the same skip within
`--window-verses` (default 2) of the hit's verse span in the comparison corpus.
The mechanic is `els.critical.verse_span_preserved`, unit-tested on toy corpora;
the proximity test is a strict superset of the equivalent-offset test (any
`preserved_equivalent_offsets` hit is also `preserved_within_verse_span`).

The strict columns and counts above are unchanged. Reproduce with:

```bash
python3 -m scripts.analyze_critical_omission_breaks_cross_tradition --window-verses 2
```

Proximity status counts (window 2):

- BYZ_NT preserved within verse span: 260.
- BYZ_NT ref missing: 192.
- BYZ_NT not preserved within window: 106.
- TCG_NT preserved within verse span: 341.
- TCG_NT ref missing: 192.
- TCG_NT not preserved within window: 25.

Proximity cross-tradition classes:

- `preserved_by_byz_and_tcg`: 260.
- `preserved_by_tcg`: 81.
- `tr_specific_within_window`: 217.

Read: tolerating word-length deltas recovers 97 BYZ and 21 TCG hits the strict
test mislabelled. BYZ_NT preservation rises from 163 to 260, so a majority of
the "broken" TR hits demonstrably exist at the same skip in the Byzantine and/or
critical tradition. The "codes lost in the modern text" framing weakens further:
for most of these hits the change is SBL-specific spacing plus text-critical
word-form editing, not genuine loss. The remaining hard floor is the 192
`ref_missing` (versification) hits, which Stage 1 does not touch.

This is Stage 1 (word-length-delta tolerance). Versification cases (a ref
present under a shifted number, the `ref_missing` pool) are a separate Stage 2.

## Cautions

- Raw break counts are not significance tests.
- Equivalent-offset mapping is conservative and can miss preservation after local wording-length changes.
- This is a robustness screen, not a textual-critical stemma.
