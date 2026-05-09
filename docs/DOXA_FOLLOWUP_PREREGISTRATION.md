# Doxa Follow-Up Preregistration

Status: post-discovery follow-up preregistration.

This document freezes the next `δοξα` extension study before additional
interpretive work is done. It does not make the original discovery
prospective. The `δοξα` / `δοξανωσ` row was already found by prior exploratory
screening, so all results from that discovery path remain review-level unless
the criteria below are met by a locked follow-up.

## Registered Candidate

Only one candidate is registered for this follow-up:

| Field | Value |
| --- | --- |
| Base term | `δοξα` |
| Extension key | `δοξα|21|forward|term_plus_after|δοξανωσ|δοξανωσ` |
| Skip | `21` |
| Direction | `forward` |
| Extension type | `term_plus_after` |
| Extension side | `after` |
| Extended normalized sequence | `δοξανωσ` |
| Matched phrase | `δόξαν ὡς` |
| Center passage | 2 Thessalonians 3:1 |
| Matched phrase reference | John 1:14 / JHN 1:14 |

No alternate spellings, skips, extension lengths, directions, or nearby rows are
part of the registered candidate.

## Source Texts

Primary source texts:

- TR_NT from `configs/example_ebible_grctr.toml`
- SBLGNT from `configs/example_sblgnt.toml`

The follow-up uses only public Greek NT sources already configured in the repo.
Any future Byzantine, Nestle-Aland, or other Greek NT source must be added by a
separate preregistration before it is searched.

## Locked Inputs

The follow-up depends on:

- `protocols/extension_deep_controls.toml`
- `scripts/analyze_extension_paired_controls.py`
- `reports/protocols/public_baseline/surface_context_extensions_tr_nt_top.csv`
- `reports/protocols/public_baseline/surface_context_extensions_sblgnt_top.csv`
- `configs/example_ebible_grctr.toml`
- `configs/example_sblgnt.toml`
- `els/corpus.py`
- `els/extensions.py`
- `els/search.py`
- `scripts/analyze_els_controls.py`

If any of these inputs change, the study must report that the run is a new
version and compare it against the previous version.

## Primary Analysis

Run:

```bash
python3 -m scripts.run_protocol protocols/extension_deep_controls.toml --resume
```

Fixed settings:

- require cross-corpus overlap
- dedupe targets
- include only the registered overlap key
- 1000 shuffled-term controls
- 1000 same-length random controls
- same corpus, same skip, same direction, same extension settings

Primary outputs:

- `reports/extension_exact_center_deep_controls_summary.csv`
- `reports/extension_exact_center_deep_controls_examples.csv`
- `reports/extension_exact_center_deep_controls.md`
- `reports/extension_exact_center_deep_controls.manifest.json`

## Primary Outcome

The primary outcome is:

- `combined_min_q` for the registered row in TR_NT
- `combined_min_q` for the registered row in SBLGNT

The current 1000/1000 p-value floor is:

- `1 / 1001 = 0.000999`

## Promotion Criteria

The row remains review-only unless all required criteria pass:

1. The exact extension key appears in both TR_NT and SBLGNT.
2. Both rows retain exact-center base-term surface context.
3. Both rows have `combined_min_q <= 0.01` in the 1000/1000 control run.
4. Both rows have saved examples and letter paths sufficient for manual audit.
5. The full phrase location is reported plainly as hidden-path only if it is not
   surface text in the hit passage.
6. Synthetic extension baselines are cited alongside the result.
7. The report says this was a post-discovery follow-up, not an original
   prospective discovery.

Passing those criteria allows only this status:

- `controlled_review_candidate`

It does not allow:

- `confirmed_code`
- `proof`
- `prophecy`
- `statistical discovery`

## Failure Criteria

The row fails the follow-up if any of these occur:

- the exact extension key is absent from either Greek NT text;
- either row loses exact-center surface context;
- either row has `combined_min_q > 0.01`;
- saved examples or letter paths cannot be reproduced;
- output depends on unregistered alternate spellings, different skips, different
  extension directions, or broadened matching rules;
- the matched phrase is described as surface text in 2 Thessalonians 3:1 when it
  is only a hidden-path extension.

## Reporting Rules

Every follow-up report must include:

- command used;
- git commit;
- runtime;
- source text labels;
- row table for TR_NT and SBLGNT;
- control sample counts;
- p-value floor;
- exact `combined_min_p` and `combined_min_q`;
- warning flags;
- explicit statement that this is post-discovery;
- explicit statement that `δόξαν ὡς` is not surface text in the 2 Thessalonians
  hit passage unless a future audit proves otherwise.

The first locked follow-up report is tracked in
`docs/DOXA_FOLLOWUP_REPORT.md`.

## Interpretation Boundary

This study can show whether the already-discovered `δοξα` row remains stable
under locked, deeper controls. It cannot prove theological meaning by itself.

Any stronger claim requires a new prospective study with either:

- a broader locked cohort of exact-center Greek theological terms before
  looking at results; or
- one or more independent Greek NT source texts added and registered before
  being searched.
