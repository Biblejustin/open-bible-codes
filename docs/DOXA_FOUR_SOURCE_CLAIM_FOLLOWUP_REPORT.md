# Doxa Four-Source Claim Follow-Up Report

Status: claim_followup_review_candidate, not a claim.

This report records the locked 5000/5000
follow-up after
`docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_PREREGISTRATION.md` was added.

## Run

| Field | Value |
| --- | --- |
| Preregistration commit | `c91925b` |
| Local report build commit | recorded in local manifest only |
| Command | `python3 -m scripts.run_protocol protocols/doxa_four_source_claim_followup.toml --resume` |
| Protocol | `protocols/doxa_four_source_claim_followup.toml` |
| Paired controls completed UTC | `2026-05-10T13:41:46.089442+00:00` |
| Context review completed UTC | `2026-05-10T13:41:47.012075+00:00` |
| Analysis runtime | 7.269s |
| Protocol status | success |
| Paired-control runtime | 6.43s |
| Context-review runtime | 0.839s |

For resumed protocol runs, this subreport uses the paired-control and
context-review output manifests for stable analysis timing. The build
commit is recorded in the local manifest; the top-level
`reports/real_report_run/summary.md` records the current assembly commit.

Generated local outputs:

- `reports/doxa_four_source_claim_followup/paired_controls_summary.csv`
- `reports/doxa_four_source_claim_followup/paired_controls_examples.csv`
- `reports/doxa_four_source_claim_followup/paired_controls.md`
- `reports/doxa_four_source_claim_followup/context_review_summary.csv`
- `reports/doxa_four_source_claim_followup/context_review.md`
- `reports/doxa_four_source_claim_followup/letter_paths.md`
- `reports/doxa_four_source_claim_followup/protocol_run.manifest.json`

## Registered Candidate

| Field | Value |
| --- | --- |
| Base term | `δοξα` (doxa; English: glory) |
| Extension key | base=`δοξα` (doxa; English: glory); skip=21; direction=forward; type=term_plus_after; extended=`δοξανωσ` (doxanos; English: hidden extension form from doxa) |
| Skip | `21` |
| Direction | `forward` |
| Extension type | `term_plus_after` |
| Extended normalized sequence | `δοξανωσ` (doxanos; English: hidden extension form from doxa) |
| Matched phrase | `δόξαν ὡς` (doxanos; English: glory as) |
| Center passage | 2 Thessalonians 3:1 |
| Matched phrase reference | John 1:14 / JHN 1:14 |

No alternate spelling, skip, direction, extension length, or nearby row was used.

## Controls

Fixed control settings:

- 5000 shuffled-term controls per row
- 5000 same-length random controls per row
- same corpus
- same skip
- same direction
- same extension settings
- target list deduped

P-value floor:

- shuffled-term controls: `1 / 5001 = 0.00019996001`
- same-length random controls: `1 / 5001 = 0.00019996001`

## Results

| Corpus | Center | Matched ref | Score | Term-any p | Random-any p | Combined p | Combined q | All-control q | Flags |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| BYZ_NT | 2TH 3:1 | JHN 1:14 | 3211 | 0.043591 | 0.002 | 0.0006 | 0.0008 | 0.043591 | `extension_min_p_adjusted;short_base_term` |
| SBLGNT | 2Thess 3:1 | John 1:14 | 3211 | 0.039792 | 0.003599 | 0.0002 | 0.0008 | 0.043591 | `extension_min_p_adjusted;low_random_same_type_variance;short_base_term` |
| TCG_NT | 2TH 3:1 | JHN 1:14 | 3211 | 0.040992 | 0.002599 | 0.0006 | 0.0008 | 0.043591 | `extension_min_p_adjusted;short_base_term` |
| TR_NT | 2TH 3:1 | JHN 1:14 | 3211 | 0.038792 | 0.005199 | 0.0016 | 0.0016 | 0.043591 | `extension_min_p_adjusted;short_base_term` |

## Context And Audit

The base term has exact-center surface context through the surface form
`δοξάζηται` (doxazetai; English: may be glorified) in 2 Thessalonians 3:1.

The full hidden extension sequence `δοξανωσ` (doxanos; English: hidden extension form from doxa) maps to the phrase
`δόξαν ὡς` (doxanos; English: glory as). This follow-up treats hidden-path-only material as meaningful
review material, not as a failure. A same-span surface echo would be a
stronger subtype, but it is not required by this registered study.

Context reads:

| Corpus | Center | Hit refs | Context read |
| --- | --- | --- | --- |
| BYZ_NT | 2TH 3:1 `κυριου` (kuriou) | 2TH 3:1 | base normalized string appears in center verse surface text |
| SBLGNT | 2Thess 3:1 `κυρίου` (kuriou) | 2Thess 3:1 | base normalized string appears in center verse surface text |
| TCG_NT | 2TH 3:1 `Κυρίου` (kuriou) | 2TH 3:1 | base normalized string appears in center verse surface text |
| TR_NT | 2TH 3:1 `Κυρίου` (kuriou) | 2TH 3:1 | base normalized string appears in center verse surface text |

Audit paths are saved in:

- `reports/doxa_four_source_claim_followup/letter_paths.md`

## Preregistration Check

| Criterion | Result | Note |
| --- | --- | --- |
| Exact extension key remains present in all four sources | pass | BYZ_NT, SBLGNT, TCG_NT, TR_NT |
| All four rows retain exact-center base-term surface context | pass | BYZ_NT, SBLGNT, TCG_NT, TR_NT |
| `combined_min_q <= 0.01` in all four rows | pass | min 0.0008; max 0.0016 |
| Saved examples and letter paths generated | pass | `reports/doxa_four_source_claim_followup/letter_paths.md` |
| Full phrase location reported | pass | hidden-path-only unless a context row says otherwise |
| Warning flags reported | pass | extension_min_p_adjusted;low_random_same_type_variance;short_base_term; extension_min_p_adjusted;short_base_term |
| Post-discovery status stated | pass | reported as follow-up, not prospective discovery |

## Interpretation

This is a post-discovery follow-up. It is not an original prospective
discovery.

Current status: `claim_followup_review_candidate`.

This does not support:

- `confirmed_code`
- `proof`
- `prophecy`
- `statistical discovery`

The result remains limited even if the registered criteria pass. The base
term is short, the row was selected after discovery, and ELS phrase
extensions can produce convincing-looking hidden strings from controls.
