# Extension Exact-Center Deep Controls

Source run:

- Protocol: `protocols/extension_deep_controls.toml`
- Step: `extension_exact_center_deep_controls`
- Command: `python3 -m scripts.run_protocol protocols/extension_deep_controls.toml --resume`
- Generated summary: `reports/extension_exact_center_deep_controls_summary.csv`
- Generated examples: `reports/extension_exact_center_deep_controls_examples.csv`
- Generated markdown: `reports/extension_exact_center_deep_controls.md`
- Generated manifest: `reports/extension_exact_center_deep_controls.manifest.json`
- Output size: 2 summary rows; 2 example rows
- Runtime observed: 431.620s direct script run

This is the slower 1000/1000 paired-control follow-up for the only exact-center
cross-text NT extension row that survived the final gate.

## Scope

Included overlap key:

- `δοξα|21|forward|term_plus_after|δοξανωσ|δοξανωσ` (doxa / doxanos; English: glory / hidden extension form from doxa)

Rows:

- SBLGNT center: 2Thess 3:1
- TR_NT center: 2TH 3:1

Controls:

- 1000 shuffled-term controls preserving the target's normalized letters
- 1000 random same-length strings drawn from same-corpus letter frequencies
- same corpus, same skip, same direction, same extension settings

The p-value floor for this run is 1 / 1001 = 0.000999.

## Main Read

Both exact-center `δοξα` (doxa; English: glory) rows stayed at the control floor after increasing from
200/200 to 1000/1000 controls.

| Corpus | Center | Matched phrase ref | Score | Term-any p | Random-any p | Combined p | Combined q |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| SBLGNT | 2Thess 3:1 | John 1:14 | 3211 | 0.043956 | 0.001998 | 0.000999 | 0.000999 |
| TR_NT | 2TH 3:1 | JHN 1:14 | 3211 | 0.041958 | 0.007992 | 0.000999 | 0.000999 |

Compared with the earlier 200/200 run:

| Corpus | 200/200 q | 1000/1000 q | Read |
| --- | ---: | ---: | --- |
| SBLGNT | 0.004975 | 0.000999 | stronger floor result |
| TR_NT | 0.004975 | 0.000999 | stronger floor result |

## Interpretation

This is the strongest current extension-control screen in the project, but it
still should not be promoted as a claim.

Reasons it remains review-only:

- the base term `δοξα` (doxa; English: glory) has exact-center surface context through `δοξάζηται` (doxazetai; English: may be glorified);
- the full extension sequence `δοξανωσ` (doxanos; English: hidden extension form from doxa) maps to the phrase `δόξαν ὡς` (doxan hos; English: glory as), but that
  phrase is not surface text in the hit passage;
- the same phrase is attested elsewhere, at John 1:14 / JHN 1:14;
- the base term is short;
- same-type random controls have low variance, which makes the floor result
  worth inspecting but not self-interpreting;
- synthetic extension baselines already show that hidden same-skip phrase
  scoring can create convincing-looking control rows.

Current read: keep `δοξα` (doxa; English: glory) as the top review row. Do not present it externally as
evidence unless a predeclared study design and broader matched-control cohort
support the same result.

The follow-up study design is frozen in
`docs/DOXA_FOLLOWUP_PREREGISTRATION.md`. It explicitly treats this as
post-discovery follow-up, not original prospective discovery.

The first locked follow-up run after that document is summarized in
`docs/DOXA_FOLLOWUP_REPORT.md`.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/extension_deep_controls.toml --resume
```

This protocol is separate from `protocols/public_baseline.toml` because the run
takes several minutes and is a focused follow-up, not part of the routine public
baseline.
