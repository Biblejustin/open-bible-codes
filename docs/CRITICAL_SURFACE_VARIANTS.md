# Critical Surface Variants

Goal:

- Compare TR NT and SBLGNT content-word counts beyond whole missing verses.
- Identify common verses where content words differ.
- Show which word-count multiple patterns break or appear when moving from TR to SBLGNT.

Command:

```bash
python3 -m scripts.analyze_critical_surface_variants
```

Outputs:

- `reports/critical_surface_tr_vs_sbl_counts.csv`
- `reports/critical_surface_variant_verses.csv`
- `reports/critical_surface_variants.manifest.json`

Results:

- Common refs compared: 7,937.
- Common refs with surface content-word differences: 3,301.
- Word count delta rows: 4,296.
- Rows where a multiple state changed: 1,421.
- Rows where a TR multiple was broken in SBLGNT: 842.
- Rows where a SBLGNT multiple was newly created: 739.

Largest Count/Multiple Examples:

- `ευθεωσ`: TR 80, SBLGNT 35; breaks 40, creates 7.
- `ευθυσ`: TR 8, SBLGNT 51; creates 3.
- `μωυσησ`: TR 2, SBLGNT 42; creates 3 and 7.
- `ειπεν`: TR 643, SBLGNT 612; creates 3 and 12.
- `χριστου`: TR 270, SBLGNT 248; breaks 3.

Cautions:

- This is surface-form comparison, not lemma comparison.
- Some differences are spelling/inflectional normalization effects.
- Some SBLGNT bracketed text remains in the source files and is counted.
