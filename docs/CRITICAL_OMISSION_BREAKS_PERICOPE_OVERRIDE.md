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
`terms/pericope_adulterae_terms.csv`.

## Results

Current run:

- Term rows: 471.
- Deleted blocks used: 47.
- Deleted letters used: 3,607.
- Broken example rows: 1,251.

The inverse Pericope check confirms the documented John 8:6 centered Jesus hit:

- SBLGNT: 1 documented hit, destroyed after Pericope removal.
- BYZ_NT: 1 documented hit, destroyed after Pericope removal.

Length-control run:

- Term rows: 523.
- Broken example rows: 1,261.
- Control file: `terms/pericope_adulterae_length_controls.csv`.

## Other Disputed Passages

The same override file also includes:

- Longer Ending of Mark: Mark 16:9-20.
- Gethsemane angel and bloody sweat: Luke 22:43-44.
- Father forgive them: Luke 23:34a, kept as partial and skipped until sub-verse handling is explicit.
- Comma Johanneum: 1 John 5:7.

## Cautions

- Raw break counts are not significance tests.
- Treat-as-deleted rows are a study override, not a claim that every listed passage has identical textual status.
- Luke 23:34a is partial-verse and is not treated as a full deletion block by the current CLI.
- The thematic Pericope cohort is exploratory and needs length/frequency-matched controls before claim language.
- The current control cohort is length-matched only; frequency matching remains future tightening.
