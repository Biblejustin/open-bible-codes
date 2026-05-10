# Doxa Four-Source Claim Follow-Up Preregistration

Status: post-discovery locked follow-up, not a claim.

This document freezes the next `δοξα` (doxa; English: glory) study before the stronger control run is
started. The candidate was already discovered in earlier exact-center Greek
extension screens, so this is not a prospective discovery. It is a locked
follow-up designed to test whether the currently strongest row remains unusual
under a higher control budget and the current four-source Greek NT source set.

## Registered Candidate

Only one candidate is registered for this follow-up:

| Field | Value |
| --- | --- |
| Base term | `δοξα` (doxa; English: glory) |
| Extension key | `δοξα|21|forward|term_plus_after|δοξανωσ|δοξανωσ` (doxa / doxanos; English: glory / hidden extension form from doxa) |
| Skip | `21` |
| Direction | `forward` |
| Extension type | `term_plus_after` |
| Extended normalized sequence | `δοξανωσ` (doxanos; English: hidden extension form from doxa) |
| Matched phrase | `δόξαν ὡς` (doxan hos; English: glory as) |
| Center passage | 2 Thessalonians 3:1 |
| Matched phrase reference | John 1:14 / JHN 1:14 |

No alternate spelling, skip, direction, extension type, extension length, or
nearby row is part of this follow-up.

## Source Texts

Primary source texts:

- TR_NT from `configs/example_ebible_grctr.toml`
- BYZ_NT from `configs/example_ebible_grcmt.toml`
- TCG_NT from `configs/example_ebible_grctcgnt.toml`
- SBLGNT from `configs/example_sblgnt.toml`

The result is source-distribution sensitive. A pattern does not need to appear
in every version to be worth recording, but this registered row is required to
remain present in all four current Greek NT source labels because that is the
reason it was selected for the follow-up.

## Locked Inputs

The follow-up depends on the already generated four-source exact-center top
files:

- `reports/greek_exact_center_four_source/extensions_tr_nt_top.csv`
- `reports/greek_exact_center_four_source/extensions_byz_nt_top.csv`
- `reports/greek_exact_center_four_source/extensions_tcg_nt_top.csv`
- `reports/greek_exact_center_four_source/extensions_sblgnt_top.csv`
- `reports/greek_exact_center_four_source/surface_context_hits.csv`

The locked protocol is:

- `protocols/doxa_four_source_claim_followup.toml`

If any input changes, the report must identify the run as a new version and
compare it against earlier four-source results.

## Primary Analysis

Run:

```bash
python3 -m scripts.run_protocol protocols/doxa_four_source_claim_followup.toml --resume
```

Locked settings:

- exact-center surface context required;
- only the registered overlap key included;
- one deduped row per corpus for the registered key;
- same skip, direction, corpus, and extension settings as the observed row;
- 5000 shuffled-term controls per row;
- 5000 same-length random controls per row;
- Benjamini-Hochberg correction across the rows in this locked run.

Primary outputs:

- `reports/doxa_four_source_claim_followup/paired_controls_summary.csv`
- `reports/doxa_four_source_claim_followup/paired_controls_examples.csv`
- `reports/doxa_four_source_claim_followup/paired_controls.md`
- `reports/doxa_four_source_claim_followup/context_review_summary.csv`
- `reports/doxa_four_source_claim_followup/context_review.md`
- `reports/doxa_four_source_claim_followup/letter_paths.md`
- `reports/doxa_four_source_claim_followup/protocol_run.manifest.json`

## Primary Outcome

The primary outcome is `combined_min_q` for the registered row in each of the
four Greek NT source labels.

The 5000/5000 p-value floor is:

- `1 / 5001 = 0.00019996`

## Promotion Criteria

The row remains review-only unless all required criteria pass:

1. The exact extension key remains present in TR_NT, BYZ_NT, TCG_NT, and
   SBLGNT.
2. All four rows retain exact-center base-term surface context.
3. All four rows have `combined_min_q <= 0.01` in the 5000/5000 control run.
4. Saved examples and letter paths are generated for manual audit.
5. The report says plainly whether the matched phrase is surface text in the hit
   span or hidden-path only.
6. Warning flags are reported.
7. The report says this is a post-discovery follow-up, not an original
   prospective discovery.

Passing these criteria allows only this status:

- `claim_followup_review_candidate`

It does not allow:

- `confirmed_code`
- `proof`
- `prophecy`
- `statistical discovery`

## Failure Criteria

The row fails this follow-up if any of these occur:

- the exact extension key is absent from any of the four registered Greek NT
  source labels;
- any row loses exact-center base-term surface context;
- any row has `combined_min_q > 0.01`;
- saved examples or letter paths cannot be reproduced;
- the result depends on unregistered alternate spellings, skip ranges,
  directions, or broadened matching rules;
- the matched phrase is described as open surface text in 2 Thessalonians 3:1
  when it is only a hidden-path extension.

## Reporting Rules

The follow-up report must include:

- command used;
- git commit;
- runtime;
- source text labels;
- control sample counts;
- p-value floor;
- exact `combined_min_p` and `combined_min_q`;
- warning flags;
- context and letter-path output locations;
- explicit statement that hidden-path-only is meaningful review material, not a
  failure;
- explicit statement that a same-span surface echo would be stronger but is not
  required by this registered study.

## Interpretation Boundary

This study can show whether the already-discovered four-source `δοξα` (doxa; English: glory) row
survives a stricter locked control run. It cannot prove theological meaning by
itself. A stronger claim would require an additional prospective study with the
candidate list and claim standard fixed before discovery.
