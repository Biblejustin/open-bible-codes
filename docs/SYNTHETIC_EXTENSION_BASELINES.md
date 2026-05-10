# Synthetic Extension Baselines

Source run:

- Protocol: `protocols/public_baseline.toml`
- Step: `synthetic_extension_baselines`
- Command: `python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only synthetic_extension_baselines`
- Generated summary: `reports/synthetic_extension_baselines_summary.csv`
- Generated examples: `reports/synthetic_extension_baselines_examples.csv`
- Generated matches: `reports/synthetic_extension_baselines_matches.csv`
- Generated markdown: `reports/synthetic_extension_baselines.md`
- Generated manifest: `reports/synthetic_extension_baselines.manifest.json`
- Output size: 4 summary rows; 4 example rows; 3 synthetic match rows
- Runtime observed: 47.220s through the protocol runner

This compares the exact-center NT extension rows against same-length synthetic Greek strings sampled from each corpus letter distribution. It uses the same skip, direction, extension filters, and extension scoring as the paired extension controls.

## Main Read

Same-type synthetic controls did not match any target extension score, but any-type controls did match or exceed 2 of 4 target rows.

| Corpus | Target | Score | Synthetic same-type >= target | Same-type p_ge | Synthetic any >= target | Any p_ge |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| SBLGNT | `αιμα` (haima; English: blood), skip 14, before_plus_term_plus_after, `ναιμανο` (naimano; English: hidden extension form from haima) | 3311 | 0 / 100 | 0.009901 | 0 / 100 | 0.009901 |
| SBLGNT | `υιος` (huios; English: son), skip 25, before_plus_term, `ουουιοσ` (ouhuios; English: hidden extension form from huios) | 3214 | 0 / 100 | 0.009901 | 2 / 100 | 0.029703 |
| SBLGNT | `δοξα` (doxa; English: glory), skip 21, term_plus_after, `δοξανωσ` (doxanos; English: hidden extension form from doxa) | 3211 | 0 / 100 | 0.009901 | 0 / 100 | 0.009901 |
| TR_NT | `δοξα` (doxa; English: glory), skip 21, term_plus_after, `δοξανωσ` (doxanos; English: hidden extension form from doxa) | 3211 | 0 / 100 | 0.009901 | 1 / 100 | 0.019802 |

## Verdict

This narrows the exact-center extension read:

- Exact same extension type remains uncommon under sampled synthetic strings.
- Broad any-extension scoring can still produce synthetic rows at or above the target score.
- The `δοξα` (doxa; English: glory) row remains the strongest review item only because it also survives cross-text support and deeper shuffled-term controls.
- These rows remain review-only, not claims.

## Synthetic Match Rows

The match-detail report lists synthetic any-type rows that equal or exceed target scores:

| Target | Synthetic matches | Read |
| --- | ---: | --- |
| SBLGNT `υιος` (huios; English: son) | 2 | broad any-type synthetic extensions can compete with target score |
| TR_NT `δοξα` (doxa; English: glory) | 1 | broad any-type synthetic extensions can compete with target score |
| SBLGNT `αιμα` (haima; English: blood) | 0 | target exceeds sampled synthetic any-type density |
| SBLGNT `δοξα` (doxa; English: glory) | 0 | target exceeds sampled synthetic any-type density |

Detailed synthetic matches:

| Target | Synthetic query | Synthetic phrase | Synthetic refs | Score |
| --- | --- | --- | --- | ---: |
| SBLGNT `υιος` (huios; English: son) | `οθει` (othei; English: synthetic query) | `τὸ θεῖον` (to theion; English: the divine thing) | Acts 17:29 | 3311 |
| SBLGNT `υιος` (huios; English: son) | `ασατ` (asat; English: synthetic query) | `πᾶσα⸃ τοῦ` (pasa tou; English: every/of the) | Acts 27:20 | 3311 |
| TR_NT `δοξα` (doxa; English: glory) | `τινα` (tina; English: someone/something) | `ἀπ ἄρτι Ναὶ` (ap arti nai; English: from now yes) | REV 14:13 | 5311 |

Surface-context review for these synthetic match rows is tracked in
`docs/SYNTHETIC_EXTENSION_MATCH_REVIEW.md`.

## Caution

Synthetic strings are density controls, not lexical controls. Existing shuffled-term controls are still the stronger comparison for real Greek word rows. This report is useful mainly as a pressure test against pure letter-distribution effects.

## Next Check

- inspect the synthetic examples that matched/exceeded any-type scores
- keep `δοξα` (doxa; English: glory) under final-gate review only
- avoid promoting source-only exact-center rows without cross-text support

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only synthetic_extension_baselines
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only report_index
```
