# Doxa Four-Source Confirmatory Follow-Up Preregistration

Status: post-discovery confirmatory follow-up, not an original discovery.

This freezes a stricter rerun for the already discovered Greek `δοξα` (doxa; English: glory) row. It
does not widen the search, add variants, or inspect nearby rows. The only goal
is to test whether the same exact row remains unusual under a larger locked
control budget.

## Registered Candidate

Only one candidate is registered:

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

No alternate spelling, skip, direction, extension length, extension type,
nearby row, source subset, or surface-context relaxation is registered.

## Source Texts

The four source labels are fixed:

- TR_NT from `configs/example_ebible_grctr.toml`
- BYZ_NT from `configs/example_ebible_grcmt.toml`
- TCG_NT from `configs/example_ebible_grctcgnt.toml`
- SBLGNT from `configs/example_sblgnt.toml`

This exact key must remain present in all four labels to pass. If it is missing
from any one label, the confirmatory follow-up fails.

## Locked Inputs

The run uses the already generated four-source exact-center top files:

- `reports/greek_exact_center_four_source/extensions_tr_nt_top.csv`
- `reports/greek_exact_center_four_source/extensions_byz_nt_top.csv`
- `reports/greek_exact_center_four_source/extensions_tcg_nt_top.csv`
- `reports/greek_exact_center_four_source/extensions_sblgnt_top.csv`
- `reports/greek_exact_center_four_source/surface_context_hits.csv`

The locked protocol is:

- `protocols/doxa_four_source_confirmatory_followup.toml`

## Primary Analysis

Run:

```bash
python3 -m scripts.run_protocol protocols/doxa_four_source_confirmatory_followup.toml --resume
```

Then build the tracked summary report from the completed protocol manifest:

```bash
python3 -m scripts.build_doxa_four_source_claim_followup_report \
  --paired-summary reports/doxa_four_source_confirmatory_followup/paired_controls_summary.csv \
  --context-summary reports/doxa_four_source_confirmatory_followup/context_review_summary.csv \
  --protocol-manifest reports/doxa_four_source_confirmatory_followup/protocol_run.manifest.json \
  --report-out docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md \
  --manifest-out reports/doxa_four_source_confirmatory_followup/report.manifest.json \
  --report-title "Doxa Four-Source Confirmatory Follow-Up Report" \
  --preregistration-doc docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_PREREGISTRATION.md \
  --protocol-path protocols/doxa_four_source_confirmatory_followup.toml \
  --term-control-samples 20000 \
  --random-control-samples 20000 \
  --preregistration-commit 79f3c73
```

Locked settings:

- exact-center surface context required;
- only the registered overlap key included;
- one deduped row per corpus for the registered key;
- same skip, direction, corpus, and extension settings as the observed row;
- 20000 shuffled-term controls per row;
- 20000 same-length random controls per row;
- Benjamini-Hochberg correction across the rows in this locked run.

Primary outputs:

- `reports/doxa_four_source_confirmatory_followup/paired_controls_summary.csv`
- `reports/doxa_four_source_confirmatory_followup/paired_controls_examples.csv`
- `reports/doxa_four_source_confirmatory_followup/paired_controls.md`
- `reports/doxa_four_source_confirmatory_followup/context_review_summary.csv`
- `reports/doxa_four_source_confirmatory_followup/context_review.md`
- `reports/doxa_four_source_confirmatory_followup/letter_paths.md`
- `reports/doxa_four_source_confirmatory_followup/protocol_run.manifest.json`
- `docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md`

## Primary Outcome

The primary outcome is `combined_min_q` for the registered row in each of the
four Greek NT source labels.

The p-value floor for each 20000-control family is:

- `1 / 20001 = 0.0000499975`

## Pass Criteria

The row remains review-only unless all criteria pass:

1. The exact extension key remains present in TR_NT, BYZ_NT, TCG_NT, and
   SBLGNT.
2. All four rows retain exact-center base-term surface context.
3. All four rows have `combined_min_q <= 0.01`.
4. Saved examples and letter paths are generated for manual audit.
5. The report states whether the matched phrase is surface text in the hit span
   or hidden-path only.
6. Warning flags are reported.
7. The report states this is a post-discovery confirmatory follow-up, not an
   original prospective discovery.

Passing these criteria allows only this status:

- `claim_followup_review_candidate`

It does not allow:

- `confirmed_code`
- `conclusive evidence`
- `prophecy`
- `statistical discovery`

## Failure Criteria

The row fails this follow-up if any of these occur:

- the exact extension key is absent from any registered source label;
- any row loses exact-center base-term surface context;
- any row has `combined_min_q > 0.01`;
- saved examples or letter paths cannot be reproduced;
- the result depends on unregistered alternate spellings, skip ranges,
  directions, extension settings, or broadened matching rules;
- the matched phrase is described as open surface text in 2 Thessalonians 3:1
  when it is only a hidden-path extension.

## Interpretation Boundary

This study can only stress-test an already discovered row. It cannot make the
row a theological conclusive evidence or an original statistical discovery. A stronger claim
would require a separate prospective study with the candidate list and claim
standard fixed before discovery.
