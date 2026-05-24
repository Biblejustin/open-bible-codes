# Critical Omission Breaks Pericope Override

## Setup

Run:

```bash
python3 -m scripts.analyze_critical_omission_breaks \
  --treat-as-deleted protocols/treat_as_deleted/critical_consensus.csv \
  --extra-terms terms/pericope_adulterae_terms.csv \
  --out-suffix _pericope_override
```

Outputs:

- `reports/critical_omission_breaks_pericope_override_summary.csv`
- `reports/critical_omission_breaks_pericope_override_examples.csv`
- `reports/critical_omission_breaks_pericope_override_by_verse.csv`
- `reports/critical_omission_breaks_pericope_override.manifest.json`
- per-passage files named `reports/critical_omission_breaks_treat_as_deleted_*`

## Method

The override CSV marks disputed refs as deletion blocks even when SBLGNT keeps
them. The same shared break engine then counts removed-letter and spacing
breaks.

The generic four Greek term lists are run together with
`terms/pericope_adulterae_terms.csv` for the aggregate run. The protocol also
writes generic-only and Pericope-thematic-only runs so the targeted cohort can
be read separately.

## Results

Current run:

- Term rows: 471.
- Deleted blocks used: 46.
- Deleted letters used: 3,467.
- Broken example rows: 1,185.

Per-passage summaries are recomputed against each passage block set, so each
summary total matches its companion examples file:

- Pericope Adulterae: 35 term rows, 267 broken hits.
- Longer Ending of Mark: 36 term rows, 258 broken hits.
- Gethsemane angel and bloody sweat: 17 term rows, 56 broken hits.
- Father forgive them: 10 term rows, 22 broken hits.
- Comma Johanneum: 8 term rows, 24 broken hits.

Separate cohort runs:

- Generic-only run: 458 term rows, 1,184 broken example rows.
- Generic-only Pericope Adulterae passage summary: 34 term rows, 266 broken hits.
- Pericope-thematic-only run: 13 term rows, 1 broken example row.
- Pericope-thematic-only Pericope Adulterae passage summary: 1 term row, 1 broken hit.

The inverse Pericope check confirms the documented John 8:6 centered Jesus hit:

- SBLGNT: 1 documented hit, destroyed after Pericope removal.
- BYZ_NT: 1 documented hit, destroyed after Pericope removal.

Control run:

- Term rows: 518.
- Broken example rows: 1,192.
- Pericope Adulterae passage summary: 36 term rows, 268 broken hits.
- Longer Ending of Mark passage summary: 38 term rows, 260 broken hits.
- Frequency-control rows: 60.
- Frequency-control broken hits: 8.
- Control file: `terms/pericope_adulterae_frequency_controls.csv`.
- Controls are exact normalized-length matches chosen from existing non-Pericope
  Greek term rows by nearest TR hit frequency.
- `γῆ` has no useful frequency-control cohort because its normalized length is
  2 and the omission-break scripts skip terms below length 3.
- The older synthetic length-only file remains available at
  `terms/pericope_adulterae_length_controls.csv`.

## Other Disputed Passages

The same override file also includes:

- Longer Ending of Mark: Mark 16:9-20.
- Gethsemane angel and bloody sweat: Luke 22:43-44.
- Father forgive them: Luke 23:34a, treated as a 49-letter normalized subspan inside Luke 23:34.
- Comma Johanneum: 1 John 5:7.

## Cautions

- Raw break counts are not significance tests.
- Treat-as-deleted rows are a study override, not a claim that every listed passage has identical textual status.
- Luke 23:34a is partial-verse; the CLI treats only its explicit normalized subspan as deleted.
- The thematic Pericope cohort and matched controls are exploratory; they are not confirmatory claim language.
