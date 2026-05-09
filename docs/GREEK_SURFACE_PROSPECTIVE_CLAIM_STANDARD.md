# Greek Surface Prospective Claim Standard

Status: preregistration scaffold; no result-producing run yet.

This document defines the minimum standard for a future Greek exact-center
surface study before any new candidate results are inspected. It is stricter
than the current post-screen Greek surface follow-up.

## Boundary

The current rows are not prospective discoveries:

- `δοξα` exact-center phrase-extension follow-ups;
- `υιος` and `αιμα` source-specific exact-center rows;
- `ανομια`, `ισαακ`, and `τερασ` expanded surface follow-up rows.

They may be used as calibration examples or prior evidence, but not as new
prospective discoveries under this standard.

## Required Lock Before Search

Before a future result-producing run starts, these items must be committed and
referenced from the preregistration:

1. term file path and SHA256;
2. protocol path and SHA256;
3. source config paths and SHA256 values;
4. skip range;
5. direction rule;
6. normalized minimum term length;
7. candidate-selection rule;
8. control pools and control budgets;
9. correction method;
10. report status labels.

If any item changes after the search begins, the report must identify the run
as a new version and cannot describe it as the original prospective run.

Lock helper:

```bash
python3 -m scripts.build_study_lock_manifest \
  --name greek_surface_future_study \
  --path terms/<future-term-file>.csv \
  --path protocols/<future-protocol>.toml \
  --path configs/example_ebible_grctr.toml \
  --path configs/example_ebible_grcmt.toml \
  --path configs/example_ebible_grctcgnt.toml \
  --path configs/example_sblgnt.toml \
  --setting skip_range=2..50 \
  --setting direction=both \
  --setting min_normalized_length=5 \
  --setting correction=benjamini_hochberg \
  --out reports/study_locks/greek_surface_future_study.manifest.json
```

The helper records SHA256 fingerprints for files and expands corpus config TOML
inputs to include their referenced source files. It also records git commit,
dirty-state, and locked non-file settings.

## Default Source Set

The default aligned Greek NT source labels are:

- TR_NT from `configs/example_ebible_grctr.toml`;
- BYZ_NT from `configs/example_ebible_grcmt.toml`;
- TCG_NT from `configs/example_ebible_grctcgnt.toml`;
- SBLGNT from `configs/example_sblgnt.toml`.

LXX may be used for broad corpus-presence review, but it is not a Greek NT
version-support source because it is not verse-aligned to the NT.

## Default Search Rule

Unless the future preregistration explicitly overrides these values before the
run, the default exact-center surface rule is:

- skip range: `2..50`;
- direction: both;
- normalized Greek term length: at least 5;
- exact-center surface context required;
- exact pattern key includes normalized term, skip, direction, start ref,
  center ref, end ref, and compared source label;
- all-source candidate means the same normalized term, skip, direction, and
  center reference appear in TR_NT, BYZ_NT, TCG_NT, and SBLGNT.

Hidden-path-only rows are valid ELS candidate types. A same-span surface echo is
a stronger subtype, but it is not required for initial review-candidate status.

## Control Standard

A future surface row cannot move beyond review material unless all registered
controls pass.

Required real-word controls:

- same normalized length;
- all-source surface-present in the same four source labels;
- selected target terms excluded from the control pool;
- at least 30 controls available per tested target;
- empirical add-one p-values and Benjamini-Hochberg q-values reported across
  every tested target.

Required randomized controls:

- shuffled-term controls using the same term letters;
- same-length same-corpus random controls;
- same skip, direction, source labels, and exact-center surface rule;
- at least 5000 shuffled-term and 5000 random controls per tested target before
  any claim-level wording is considered.

Suggested claim-level statistical threshold:

- `q <= 0.01` for both real-word and randomized control families.

If fewer than 30 real-word controls exist for a target, the row is held for
review and cannot be claim-level under this standard.

## Required Audit Outputs

Every surviving row must include:

- source-version distribution table;
- exact letter-path reconstruction for every source label;
- center verse and center word;
- start and end references;
- visible surface-term context;
- whether any same-span surface echo exists;
- control examples;
- p/q values;
- warning flags;
- plain-English interpretation boundary.

## Allowed Status Labels

Allowed maximum labels:

- `prospective_review_queue_candidate`;
- `prospective_controlled_review_candidate`;
- `source_specific_review_candidate`;
- `review_hold`;
- `not_reproducible`.

Disallowed labels without a separate stronger standard:

- `confirmed_code`;
- `proof`;
- `prophecy`;
- `statistical discovery`;
- `claim`.

## Current Project Implication

The expanded Greek surface follow-up remains useful because it joins selected
rows, letter paths, and all-available real-word controls. It still remains
post-screen. The next result-producing step should not widen raw searches. It
should first commit a new term file and protocol under this standard.
