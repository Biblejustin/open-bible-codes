# SBLGNT Source-Only Exact-Center Preregistration

Status: post-discovery source-specific follow-up.

This document freezes a weaker follow-up for the SBLGNT-only exact-center rows
that appeared in `docs/GREEK_EXACT_CENTER_COHORT_REPORT.md`.

This is not a cross-text study. It cannot promote a row to the same status as
the TR_NT/SBLGNT `δοξα` (doxa; English: glory) row. Its maximum status is source-specific review.

## Registered Rows

Only these two SBLGNT rows are registered:

| Term | Extension key | Center | Matched phrase ref |
| --- | --- | --- | --- |
| `αιμα` (haima; English: blood) | `αιμα|14|forward|before_plus_term_plus_after|ναιμανο|ναιμανο` (haima / naimano; English: blood / hidden extension form from haima) | Rev 17:6 | Luke 4:27 |
| `υιοσ` (huios; English: son) | `υιοσ|25|forward|before_plus_term|ουουιοσ|ουουιοσ` (huios / ouhuios; English: son / hidden extension form from huios) | Luke 19:9 | Matt 17:9; Matt 26:24; Mark 14:21; John 4:46 |

No alternate spellings, skips, directions, extension lengths, or nearby rows are
part of this source-only follow-up.

## Source Text

Primary source text:

- SBLGNT from `configs/example_sblgnt.toml`

TR_NT is intentionally not part of this follow-up because these rows did not
survive the cross-text requirement in the locked Greek cohort.

## Protocol

Run:

```bash
python3 -m scripts.run_protocol protocols/sblgnt_source_only_exact_center.toml --resume
```

Prerequisite:

- `protocols/greek_exact_center_cohort.toml` must already have produced the
  local ignored source files under `reports/greek_exact_center_cohort/`.

Locked control settings:

- exact-center surface context required
- only the two registered extension keys included
- 1000 shuffled-term controls
- 1000 same-length random controls
- same SBLGNT corpus, skip, direction, and extension settings
- context review filtered to rows present in the control summary

## Primary Outputs

- `reports/sblgnt_source_only_exact_center/paired_controls_summary.csv`
- `reports/sblgnt_source_only_exact_center/paired_controls_examples.csv`
- `reports/sblgnt_source_only_exact_center/context_review_summary.csv`
- `reports/sblgnt_source_only_exact_center/letter_paths.md`
- `reports/sblgnt_source_only_exact_center/protocol_run.manifest.json`

Tracked report:

- `docs/SBLGNT_SOURCE_ONLY_EXACT_CENTER_REPORT.md`

The first source-only follow-up report is tracked there.

## Primary Outcome

Primary row-level outcome:

- `combined_min_q`

The 1000/1000 p-value floor is:

- `1 / 1001 = 0.000999`

## Promotion Criteria

A row may be labeled only as `source_specific_review_candidate` if all criteria
pass:

1. exact-center base-term surface context remains present;
2. `combined_min_q <= 0.01`;
3. saved examples and letter paths exist;
4. full phrase location is reported plainly as surface or hidden-path only;
5. warning flags are reported;
6. the report states this is source-only and post-discovery.

No row may be promoted to:

- `controlled_cross_text_candidate`
- `confirmed_code`
- `conclusive evidence`
- `prophecy`
- `statistical discovery`

## Failure Criteria

The follow-up fails if:

- either registered row is missing;
- either row loses exact-center surface context;
- either row has `combined_min_q > 0.01`;
- examples or letter paths cannot be generated;
- the report implies cross-text support.

## Interpretation Boundary

This source-only study can decide whether `αιμα` (haima; English: blood) and `υιος` (huios; English: son) deserve internal
SBLGNT-specific review. It cannot make a public Bible-code claim.
