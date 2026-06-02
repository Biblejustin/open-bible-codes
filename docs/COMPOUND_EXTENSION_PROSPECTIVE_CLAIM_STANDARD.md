# Compound Extension Prospective Claim Standard

Status: preregistration scaffold; no result-producing run yet.

This document defines the minimum standard for a future compound-extension
study before any new extension candidates are inspected. It is stricter than
the current all-codes post-screen follow-up.

## Boundary

The current compound-extension rows are not prospective discoveries:

- the broad all-codes extension queue in
  `docs/ALL_CODES_FOLLOWUP_EXTENSIONS.md`;
- the 250/250 exploratory paired controls in
  `docs/ALL_CODES_COMPOUND_EXTENSION_CONTROLS.md`;
- the selected `יום יהוה` (yom YHWH; English: day of YHWH) ->
  `היומיהוה` (hayom YHWH; English: the day of YHWH) confirmatory follow-up in
  `docs/ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_CONTROLS.md`.

They may be used as calibration examples or prior evidence, but not as new
prospective discoveries under this standard.

## Required Lock Before Search

Before a future result-producing compound-extension run starts, these items
must be committed and referenced from the preregistration:

1. term file path and SHA256;
2. protocol path and SHA256;
3. source config paths and SHA256 values;
4. skip range;
5. direction rule;
6. normalized minimum base-term length;
7. allowed extension sides;
8. maximum extension length;
9. extension scoring rule;
10. candidate-selection rule;
11. control pools and control budgets;
12. correction method;
13. report status labels.

If any item changes after the search begins, the report must identify the run
as a new version and cannot describe it as the original prospective run.

Lock helper:

```bash
python3 -m scripts.build_study_lock_manifest \
  --name compound_extension_future_study \
  --path terms/[future-term-file].csv \
  --path protocols/[future-protocol].toml \
  --path configs/example_oshb_wlc.toml \
  --path configs/example_uxlc.toml \
  --path configs/example_ebible_hebwlc.toml \
  --path configs/example_mam.toml \
  --path configs/example_uhb.toml \
  --setting skip_range=2..50 \
  --setting direction=both \
  --setting min_normalized_length=5 \
  --setting extension_sides=before_plus_term,term_plus_after \
  --setting correction=benjamini_hochberg \
  --out reports/study_locks/compound_extension_future_study.manifest.json
```

The helper records SHA256 fingerprints for files and expands corpus config TOML
inputs to include their referenced source files. It also records git commit,
dirty-state, and locked non-file settings.

## Default Source Set

The default Hebrew MT-family source labels are:

- MT_WLC from `configs/example_oshb_wlc.toml`;
- UXLC from `configs/example_uxlc.toml`;
- EBIBLE_WLC from `configs/example_ebible_hebwlc.toml`;
- MAM from `configs/example_mam.toml`;
- UHB from `configs/example_uhb.toml`.

KJV or KJVA may be used for broad English comparison, but a Hebrew
compound-extension claim needs a Hebrew source-family rule fixed before the
run. English rows from the current all-codes queue cannot be mixed into the
same primary claim family unless the preregistration explicitly defines a
separate English stratum and correction family.

## Default Extension Rule

Unless the future preregistration explicitly overrides these values before the
run, the default compound-extension rule is:

- skip range: `2..50`;
- direction: both;
- normalized base-term length: at least 5;
- allowed extension sides: letters before the base term plus the base term, or
  the base term plus letters after it;
- maximum extension length: 12 letters on either side;
- extension phrase words: up to 4 visible words;
- the extension must form a normalized surface sequence present in the same
  corpus near the ELS lane;
- exact pattern key includes normalized base term, skip, direction, extension
  side, extended normalized sequence, source label, and reference path.

Same-skip hidden-path extension rows are valid review candidates. A visible
surface phrase using the same normalized extended sequence is a stronger
subtype, but it is not enough for claim-grade wording without controls.

## Control Standard

A future compound-extension row cannot move beyond review material unless all
registered controls pass.

Required real-word controls:

- same normalized base-term length;
- same source family and same extension side;
- selected target terms excluded from the control pool;
- at least 30 controls available per tested target;
- empirical add-one p-values and Benjamini-Hochberg q-values reported across
  every tested target.

Required randomized controls:

- shuffled-base-term controls using the same base-term letters;
- same-length same-corpus random controls;
- same extension-side controls;
- any-extension controls;
- same skip, direction, source labels, extension rule, and score rule;
- at least 5000 shuffled-base-term and 5000 random controls per tested target
  before any claim-grade wording is considered.

Suggested claim-grade statistical threshold:

- `q <= 0.01` for real-word, shuffled-base-term, same-length random,
  same-extension-side, and any-extension control families.

If fewer than 30 real-word controls exist for a target, the row is held for
review and cannot be claim-grade under this standard.

## Required Audit Outputs

Every surviving row must include:

- source-version distribution table;
- exact letter-path reconstruction for every source label;
- base-term references;
- extension start and end references;
- visible surface context for the extended sequence;
- whether the extension crosses a word, verse, chapter, or book boundary;
- control examples;
- p/q values for every registered control family;
- warning flags;
- plain-English interpretation boundary.

## Allowed Status Labels

Allowed maximum labels:

- `prospective_compound_extension_review_candidate`;
- `prospective_compound_extension_controlled_review_candidate`;
- `source_specific_review_candidate`;
- `review_hold`;
- `not_reproducible`.

Disallowed labels without a separate stronger standard:

- `confirmed_code`;
- `conclusive evidence`;
- `prophecy`;
- `statistical discovery`;
- `claim`.

## Current Project Implication

The `יום יהוה` (yom YHWH; English: day of YHWH) ->
`היומיהוה` (hayom YHWH; English: the day of YHWH) row remains useful as a
post-screen review candidate because it survived larger locked controls across
the MT-family sources. It still remains prior evidence. The next
result-producing step should not widen raw all-codes searches. It should first
commit a new term file, source-family rule, extension rule, controls, and
protocol under this standard.
