# Greek Pattern Version Summary

Status: consolidated current review queue.

This report merges exact-center extension pattern-presence matrices and
row-local control summaries. It asks which exact patterns appear in which Greek
NT source texts, not whether every pattern appears in every source.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/greek_pattern_versions.toml --resume
```

Local generated outputs:

- `reports/greek_pattern_versions/summary.csv`
- `reports/greek_pattern_versions/summary.md`
- `reports/greek_pattern_versions/manifest.json`

## Inputs

- Two-source presence: `reports/greek_exact_center_cohort/pattern_presence.csv`
- Three-source presence: `reports/greek_exact_center_three_source/pattern_presence.csv`
- Four-source presence: `reports/greek_exact_center_four_source/pattern_presence.csv`
- Four-source controls: `reports/greek_exact_center_four_source/paired_controls_summary.csv`
- Three-source controls: `reports/greek_exact_center_three_source/paired_controls_summary.csv`
- SBLGNT source-only controls: `reports/sblgnt_source_only_exact_center/paired_controls_summary.csv`
- BYZ_NT source-only controls: `reports/byz_source_only_exact_center/paired_controls_summary.csv`

## Current Pattern Status

| Pattern | Current presence | Missing | Controlled corpora | Best q | Status | Read |
| --- | --- | --- | --- | ---: | --- | --- |
| `δοξα|21|forward|term_plus_after|δοξανωσ|δοξανωσ` (doxa / doxanos; English: glory / hidden extension form from doxa) | TR_NT, BYZ_NT, TCG_NT, SBLGNT | none | BYZ_NT, SBLGNT, TCG_NT, TR_NT | 0.001332 | `four_source_controlled_review_candidate` | strongest review queue item; still hidden-path and not a claim |
| `υιοσ|25|forward|before_plus_term|ουουιοσ|ουουιοσ` (huios / ouhuios; English: son / hidden extension form from huios) | BYZ_NT, SBLGNT | TR_NT, TCG_NT | BYZ_NT, SBLGNT | 0.001249 | `multi_source_controlled_review_candidate` | multi-source review queue item; inspect source-family distribution |
| `αιμα|14|forward|before_plus_term_plus_after|ναιμανο|ναιμανο` (haima / naimano; English: blood / hidden extension form from haima) | SBLGNT | TR_NT, BYZ_NT, TCG_NT | SBLGNT | 0.000999 | `source_specific_review_candidate` | version-specific review queue item; source-only boundary applies |
| `υιοσ|-46|backward|before_plus_term|ειουιοσ|ειουιοσ` (huios / eiouios; English: son / hidden extension form from huios) | BYZ_NT | TR_NT, TCG_NT, SBLGNT | BYZ_NT | 0.000999 | `source_specific_review_candidate` | version-specific review queue item; source-only boundary applies |

## Interpretation

The current Greek exact-center review queue has four exact extension keys:

- one appears in every compared Greek NT source;
- one appears in BYZ_NT and SBLGNT but not TR_NT or TCG_NT;
- one is SBLGNT-specific;
- one is BYZ_NT-specific.

This supports the version-distribution framing: source-specific rows should not
be promoted as cross-text evidence, but they also should not be discarded simply
because another source lacks the same exact pattern.

## Caution

This is a review-queue summary. A source-specific row can be worth examining
inside that source while still being much weaker than a cross-source row.
Hidden-path rows are not claims.
