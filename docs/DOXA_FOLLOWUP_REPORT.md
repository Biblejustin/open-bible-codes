# Doxa Follow-Up Report

Status: controlled review candidate, not a claim.

This report records the first locked follow-up run after
`docs/DOXA_FOLLOWUP_PREREGISTRATION.md` was added.

## Run

| Field | Value |
| --- | --- |
| Preregistration commit | `9f7a4ef` |
| Command | `python3 -m scripts.run_protocol protocols/extension_deep_controls.toml --resume` |
| Protocol | `protocols/extension_deep_controls.toml` |
| Started UTC | `2026-05-05T01:40:55.740611+00:00` |
| Ended UTC | `2026-05-05T01:47:57.503576+00:00` |
| Protocol runtime | 421.809s |
| Analysis runtime | 421.646s |
| Step return code | 0 |

Generated outputs:

- `reports/extension_exact_center_deep_controls_summary.csv`
- `reports/extension_exact_center_deep_controls_examples.csv`
- `reports/extension_exact_center_deep_controls.md`
- `reports/extension_exact_center_deep_controls.manifest.json`
- `reports/extension_exact_center_deep_controls/protocol_run.manifest.json`

The generated `reports/` files are local/ignored artifacts. This tracked document
records the result needed for review.

## Registered Candidate

| Field | Value |
| --- | --- |
| Base term | `δοξα` (doxa; English: glory) |
| Extension key | `δοξα|21|forward|term_plus_after|δοξανωσ|δοξανωσ` (doxa / doxanos; English: glory / hidden extension form from doxa) |
| Skip | `21` |
| Direction | `forward` |
| Extension type | `term_plus_after` |
| Extension side | `after` |
| Extended normalized sequence | `δοξανωσ` (doxanos; English: hidden extension form from doxa) |
| Matched phrase | `δόξαν ὡς` (doxan hos; English: glory as) |
| Matched phrase reference | John 1:14 / JHN 1:14 |

No alternate spelling, skip, direction, extension length, or nearby row was used.

## Source Texts

| Corpus | Config | Letters | Verses | Runtime |
| --- | --- | ---: | ---: | ---: |
| SBLGNT | `configs/example_sblgnt.toml` | 679,879 | 7,939 | 212.824s |
| TR_NT | `configs/example_ebible_grctr.toml` | 690,831 | 7,957 | 208.820s |

## Controls

Fixed control settings:

- 1000 shuffled-term controls per row
- 1000 same-length random controls per row
- same corpus
- same skip
- same direction
- same extension settings
- cross-corpus overlap required
- target list deduped

P-value floor:

- `1 / 1001 = 0.000999`

## Results

| Corpus | Center | Matched ref | Score | Term-any p | Random-any p | Combined p | Combined q | Flags |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| SBLGNT | 2Thess 3:1 | John 1:14 | 3211 | 0.043956 | 0.001998 | 0.000999 | 0.000999 | `extension_min_p_adjusted;low_random_same_type_variance;short_base_term` |
| TR_NT | 2TH 3:1 | JHN 1:14 | 3211 | 0.041958 | 0.007992 | 0.000999 | 0.000999 | `extension_min_p_adjusted;low_random_same_type_variance;short_base_term` |

Both rows remained at the 1000/1000 control floor.

## Context And Audit

The base term has exact-center surface context in both texts through
`δοξάζηται` (doxazetai; English: may be glorified) in 2 Thessalonians 3:1.

The full hidden extension sequence `δοξανωσ` (doxanos; English: hidden extension
form from doxa) maps to the phrase `δόξαν ὡς` (doxan hos; English: glory as),
but that phrase is not surface text in the 2 Thessalonians 3:1-2 hit/extension
passage. The matched phrase is surface text elsewhere, at John 1:14 / JHN 1:14.

Audit paths are saved in the existing exact-center cohort review output:

- `reports/extension_exact_center_cohort_letter_paths.md`
- `reports/extension_exact_center_cohort_review_summary.csv`

Those paths show the same 7-letter hidden sequence in both Greek NT texts:

| Corpus | Letter path |
| --- | --- |
| SBLGNT | `δ@2Thess 3:1:547432;ο@2Thess 3:1:547453;ξ@2Thess 3:1:547474;α@2Thess 3:1:547495;ν@2Thess 3:2:547516;ω@2Thess 3:2:547537;σ@2Thess 3:2:547558` (letters spell `δοξανωσ` [doxanos; English: hidden extension form from doxa]) |
| TR_NT | `δ@2TH 3:1:556748;ο@2TH 3:1:556769;ξ@2TH 3:1:556790;α@2TH 3:1:556811;ν@2TH 3:2:556832;ω@2TH 3:2:556853;σ@2TH 3:2:556874` (letters spell `δοξανωσ` [doxanos; English: hidden extension form from doxa]) |

## Preregistration Check

| Criterion | Result | Note |
| --- | --- | --- |
| Exact extension key appears in both TR_NT and SBLGNT | pass | Same key present in both rows |
| Both rows retain exact-center base-term surface context | pass | `δοξάζηται` (doxazetai; English: may be glorified) in 2 Thessalonians 3:1 |
| Both rows have `combined_min_q <= 0.01` | pass | Both are `0.000999` |
| Saved examples and letter paths exist | pass with dependency | Deep-control examples are saved; letter paths are from exact-center cohort review outputs |
| Full phrase location reported as hidden-path only when not surface text in hit passage | pass | Reported above |
| Synthetic extension baselines cited alongside result | pass | See `docs/SYNTHETIC_EXTENSION_BASELINES.md` and `docs/SYNTHETIC_EXTENSION_MATCH_REVIEW.md` |
| Report says this is post-discovery follow-up, not original prospective discovery | pass | Stated below |

## Interpretation

This is a post-discovery follow-up. It is not an original prospective discovery.

The locked run supports the limited status:

- `controlled_review_candidate`

It does not support:

- `confirmed_code`
- `proof`
- `prophecy`
- `statistical discovery`

The result remains interesting because it has exact-center base-term context,
cross-text Greek NT support, and 1000/1000 control-floor q values in both texts.
It remains limited because the full phrase is hidden-path only, the base term is
short, and synthetic extension controls show that same-skip phrase scoring can
produce convincing-looking hidden phrases from control strings.

## Next Step

The next defensible analysis is a broader prospective cohort, locked before any
new results are inspected. Good candidates:

- exact-center Greek theological terms;
- fixed TR_NT/SBLGNT cross-text requirement;
- same 1000/1000 controls;
- saved context and letter-path outputs;
- same promotion boundary: controlled review only unless a new claim standard is
  registered in advance.
