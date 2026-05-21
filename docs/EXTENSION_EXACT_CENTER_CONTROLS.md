# Extension Exact-Center Controls

Source run:

- Protocol: `protocols/public_baseline.toml`
- Step: `extension_exact_center_controls`
- Command: `python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only extension_exact_center_controls`
- Generated summary: `reports/extension_exact_center_controls_summary.csv`
- Generated examples: `reports/extension_exact_center_controls_examples.csv`
- Generated markdown: `reports/extension_exact_center_controls.md`
- Generated manifest: `reports/extension_exact_center_controls.manifest.json`
- Output size: 2 summary rows; 2 example rows
- Runtime observed: 87.217s through the protocol runner

This is the deeper 200/200 control run for the only strict extension overlap that passes the exact-center promotion gate.

## Scope

Included overlap key:

- `δοξα|21|forward|term_plus_after|δοξανωσ|δοξανωσ` (doxa / doxanos; English: glory / hidden extension form from doxa)

Rows:

- TR_NT 2TH 3:1
- SBLGNT 2Thess 3:1

Controls:

- 200 shuffled-term controls preserving the target's normalized letters
- 200 random same-length strings drawn from same-corpus letter frequencies
- same corpus, same skip, same direction, same extension settings

## Main Read

Both exact-center `δοξα` (doxa; English: glory) rows crossed the deeper q <= 0.01 screen.

Band counts:

| Band | Rows |
| --- | ---: |
| `extension_q_le_0.01` | 2 |

Rows:

| Corpus | Center | Combined p | Combined q | Term-any p | Random-any p | Band |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| SBLGNT | 2Thess 3:1 | 0.004975 | 0.004975 | 0.044776 | 0.004975 | `extension_q_le_0.01` |
| TR_NT | 2TH 3:1 | 0.004975 | 0.004975 | 0.059701 | 0.014925 | `extension_q_le_0.01` |

Read:

- This is the strongest current extension row after controls and context gates.
- It survives TR_NT/SBLGNT overlap.
- It passes exact-center context because `δοξα` (doxa; English: glory) appears in the center verse surface text as part of `δοξάζηται` (doxazetai; English: may be glorified).
- The full matched phrase `δόξαν ὡς` (doxan hos; English: glory as) still does not appear as surface text in the hit/extension passage.
- This remains an internal review item, not an external claim.

## Caution

The exact-center gate is stronger than same-category context, but the full matched phrase `δόξαν ὡς` (doxan hos; English: glory as) does not appear as surface text in the hit/extension span. The term is also short (`δοξα` (doxa; English: glory)), and both rows still carry low random-variance warnings.

## Follow-Up Status

- Manual context and letter-path review is tracked in
  `docs/EXTENSION_EXACT_CENTER_COHORT_REVIEW.md`.
- Broader cohort checks are tracked in
  `docs/EXTENSION_EXACT_CENTER_COHORT_CONTROLS.md`.
- 1000/1000 follow-up controls are tracked in
  `docs/EXTENSION_EXACT_CENTER_DEEP_CONTROLS.md`.
- Four-source and confirmatory doxa follow-ups are tracked in
  `docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_REPORT.md` and
  `docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md`.

Avoid promotion unless a future prospective design is locked before any new
result-producing run.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only extension_exact_center_controls
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only report_index
```
