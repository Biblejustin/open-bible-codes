# Extension Exact-Center Final Gate

Source run:

- Protocol: `protocols/public_baseline.toml`
- Step: `extension_exact_center_final_gate`
- Command: `python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only extension_exact_center_final_gate`
- Generated summary: `reports/extension_exact_center_final_gate_summary.csv`
- Generated markdown: `reports/extension_exact_center_final_gate.md`
- Generated manifest: `reports/extension_exact_center_final_gate.manifest.json`
- Output size: 4 summary rows
- Runtime observed: 0.049s through the protocol runner

This combines exact-center context, controls, and cross-text support into one final review table.

## Main Read

`δοξα` (doxa; English: glory) is the only row that passes all three filters:

- exact-center surface context
- exact extension-key support in both TR_NT and SBLGNT
- deep 200/200 controls at q <= 0.01
- focused 1000/1000 follow-up controls at q = 0.000999 in both texts

Rows:

| Corpus | Term | Extension | Control q | Cross-text | Final gate | Claim status |
| --- | --- | --- | ---: | --- | --- | --- |
| SBLGNT | `αιμα` (haima; English: blood) | `ναιμανο` (naimano; English: hidden extension form from haima) | 0.019608 | source-only | `hold_source_only` | `hold` |
| SBLGNT | `δοξα` (doxa; English: glory) | `δοξανωσ` (doxanos; English: hidden extension form from doxa) | 0.004975 | cross-text | `review_cross_text_exact_center_hidden_phrase` | `review_only_not_claim` |
| TR_NT | `δοξα` (doxa; English: glory) | `δοξανωσ` (doxanos; English: hidden extension form from doxa) | 0.004975 | cross-text | `review_cross_text_exact_center_hidden_phrase` | `review_only_not_claim` |
| SBLGNT | `υιος` (huios; English: son) | `ουουιοσ` (ouhuios; English: hidden extension form from huios) | 0.019608 | source-only | `hold_source_only` | `hold` |

## Verdict

The final gate keeps only `δοξα` (doxa; English: glory) as a review row. It is still not a claim because the full extension phrase is hidden-path only, not surface text in the passage.

Focused 1000/1000 follow-up controls are tracked in
`docs/EXTENSION_EXACT_CENTER_DEEP_CONTROLS.md`.

## Follow-Up Status

- Focused 1000/1000 controls are tracked in
  `docs/EXTENSION_EXACT_CENTER_DEEP_CONTROLS.md`.
- Synthetic extension baselines are tracked in
  `docs/SYNTHETIC_EXTENSION_BASELINES.md`.
- Four-source and confirmatory doxa follow-ups are tracked in
  `docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_REPORT.md` and
  `docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md`.

Future extension work should review only `δοξα` (doxa; English: glory) unless a
new prospective rule explicitly admits source-specific rows.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only extension_exact_center_final_gate
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only report_index
```

Same-length synthetic Greek extension baselines are tracked in
`docs/SYNTHETIC_EXTENSION_BASELINES.md`.
