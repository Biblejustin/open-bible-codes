# Greek Lexicon Extension Prospective Report

Status: Stage B complete; context-cautioned review material, not claim evidence.

## Setup

This run used the locked Strong's Greek lexicon cohort from
`terms/greek_lexicon_extension_terms_clean_lock.csv`.

Pre-run lock state:

- source list: 5038 Greek headword rows;
- clean locked list after prior-evidence filtering: 5009 rows;
- clean prior-evidence audit: 0 overlap rows;
- clean preflight: passed after rebuilding the lock manifest on a clean tree.

Compared Greek New Testament source labels:

- `TR_NT`;
- `BYZ_NT`;
- `TCG_NT`;
- `SBLGNT`.

Protocol files:

- `protocols/greek_lexicon_extension_stage_a_screen.toml`;
- `protocols/greek_lexicon_extension_stage_a_controls.toml`;
- `protocols/greek_lexicon_extension_stage_b_confirmation.toml`.

## Method

Stage A screen:

1. Search the four Greek New Testament corpora for exact-center surface-context
   ELS hits from the locked lexicon terms.
2. Build same-skip phrase extensions in each source.
3. Keep exact-center extension keys and summarize source presence.

Stage A controls:

1. Keep only extension keys present in all four compared Greek sources.
2. Run 5000 shuffled-term controls and 5000 random controls.

Stage B confirmation:

1. Re-run the Stage A survivor rows with 20000 shuffled-term controls and
   20000 random controls.
2. Rebuild context and letter-path review for the confirmed rows.

## Results

Stage A screen:

| Metric | Value |
| --- | ---: |
| Surface-context summary rows | 20036 |
| TR_NT top extension rows | 59 |
| BYZ_NT top extension rows | 61 |
| TCG_NT top extension rows | 52 |
| SBLGNT top extension rows | 62 |
| Exact extension presence keys | 9 |
| All-source keys | 2 |
| Multi-source non-all-source keys | 3 |
| Source-only keys | 4 |

All-source keys:

| Key | Sources | Read |
| --- | --- | --- |
| `αυτου|8|forward|before_plus_term|καταυτου|καταυτου` | TR_NT, BYZ_NT, TCG_NT, SBLGNT | common-pronoun row; review only |
| `αυτου|8|forward|term_plus_after|αυτουσοι|αυτουσοι` | TR_NT, BYZ_NT, TCG_NT, SBLGNT | common-pronoun row; review only |

Stage A controls:

| Metric | Value |
| --- | ---: |
| Controlled corpus rows | 8 |
| Rows with `all_controls_q_le_0.05` | 8 |
| Conservative all-control q value | 0.018996 |

Stage B confirmation:

| Metric | Value |
| --- | ---: |
| Confirmed corpus rows | 8 |
| Rows with `all_controls_q_le_0.05` | 8 |
| Conservative all-control q value | 0.017749 |
| Context review rows | 8 |
| Context review gate | `promote_exact_center` on all 8 rows |

Stage B row family:

| Family | Corpus rows | Stage B all-control q | Context read |
| --- | ---: | ---: | --- |
| `αυτου` + `καταυτου` at skip 8 forward | 4 | 0.017749 | base string appears in the center verse surface text |
| `αυτου` + `αυτουσοι` at skip 8 forward | 4 | 0.017749 | base string appears in the center verse surface text |

## Interpretation

The numeric result survived Stage B controls. It is not discarded.

The interpretive read is still weak. Both all-source rows are based on
`αυτου`, a very common Greek pronoun form. The reviewed center passages also
contain the base normalized string in the surface verse. That means the rows are
best treated as common-pronoun, surface-context review material rather than as
claim-grade evidence.

## Outputs

Ignored report artifacts:

- `reports/greek_lexicon_extension_stage_a_screen/pattern_presence.csv`;
- `reports/greek_lexicon_extension_stage_a_screen/pattern_presence.md`;
- `reports/greek_lexicon_extension_stage_a_controls/paired_controls_summary.csv`;
- `reports/greek_lexicon_extension_stage_a_controls/context_review.md`;
- `reports/greek_lexicon_extension_stage_b_confirmation/paired_controls_summary.csv`;
- `reports/greek_lexicon_extension_stage_b_confirmation/context_review.md`;
- `reports/greek_lexicon_extension_stage_b_confirmation/letter_paths.md`.

## Cautions

Raw hit counts are not significance tests.

Stage B controls confirm that these rows beat the registered shuffled-term and
random controls under this scoring setup. They do not remove the obvious
common-word risk. `αυτου` is frequent, and the surface verses already contain
the base string.

This report should be cited as context-cautioned review material, not a
confirmed Bible-code claim.
