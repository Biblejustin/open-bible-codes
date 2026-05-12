# Broader Search Findings

Status: screening/reporting summary, not claim material.

This writeup summarizes the current broader-count and extension runs. It is a
map of what was detected in which source families, where controls weakened the
raw counts, and which rows remain worth review.

## Runs Covered

| Protocol | Scope | Main outputs |
| --- | --- | --- |
| `protocols/broad_search.toml` | all declared term lists, skip `2..100`, direction `both` | `reports/broad_search/broad_search.md`; `reports/broad_search/broad_version_presence.md` |
| `protocols/wide_focus_search.toml` | modern/geopolitical/local and prophetic terms, skip `2..250` | `reports/wide_focus_search/wide_focus.md`; `reports/wide_focus_search/wide_focus_version_presence.md` |
| `protocols/wide_focus_paired_controls.toml` | representative wide-focus rows, 100 shuffled-term plus 100 random controls | `reports/wide_focus_paired_controls.md` |
| `protocols/modern_focus_extensions.toml` | same-skip before/after extension checks for modern terms | `reports/modern_extension_screen/` |
| `protocols/version_presence_extensions.toml` | same-skip extension checks for all-source Hebrew and Greek version-presence queues | `reports/version_presence_extensions/` |
| `protocols/extension_deep_controls.toml` | 1000/1000 follow-up for the strongest exact-center Greek extension row | `reports/extension_exact_center_deep_controls.md` |

Recent local runtimes were about 21 seconds for the broad run, 40 seconds for
the wide-focus run, 32 seconds for wide-focus paired controls, and 7 seconds for
the deep `δοξα` (doxa; English: glory) extension control follow-up.

## Main Read

- Raw ELS counts scale strongly with skip range and term length. Short terms,
  acronyms, and common letter clusters dominate.
- Hidden-path-only rows are valid detection rows. They are not failures.
- Same-span or same-passage surface echoes are rarer and stronger, but they are
  not required before a row can be reviewed.
- Version presence matters. Several terms appear in every compatible Hebrew or
  Greek source family, while longer modern phrases often remain absent even when
  abbreviations are dense.
- The strongest controlled row remains Greek `δοξα` (doxa; English: glory) with same-skip extension
  `δοξανωσ` (doxanos; English: hidden extension form from doxa), supported across Greek NT sources and surviving deeper row-local
  controls. Its status remains review material, not a claim.

## Broad Search, Skip 2..100

The all-list broad search counted 5375 rows across 11 term sets. Version
presence grouped terms into:

- `present_all_observed_sources`: 700 terms;
- `present_multiple_sources`: 43 terms;
- `source_specific`: 33 terms;
- `absent_all_observed_sources`: 299 terms.

Important observations:

- United Nations and USA abbreviations are extremely dense, but only as short
  acronym forms such as Hebrew `אומ` (UM; English: United Nations abbreviation) and Greek `οηε` (OHE; English: United Nations abbreviation) / `ηπα` (HPA; English: USA abbreviation).
- Longer phrases such as United Nations, United States, United States of
  America, European Union, and Cowboy Catering are absent at this range.
- `Trump`, `Netanyahu`, `Russia`, `Europe`, `Germany`, `Turkey`, `Gog`, and
  `Magog` have detected rows in compatible source families, but most are short
  or moderately short forms that require controls.
- Local terms mostly remain absent at skip `2..100`; Hebrew `Cowboy` has
  low-count all-source presence, while `Catering`, `Simsberry`, and `Simscorner`
  are absent in the broad run.

## Wide Focus, Skip 2..250

The focused wide run counted 2365 rows across modern/geopolitical/local and
prophetic terms. Version presence grouped terms into:

- `present_all_observed_sources`: 290 terms;
- `present_multiple_sources`: 23 terms;
- `source_specific`: 19 terms;
- `absent_all_observed_sources`: 141 terms.

Important observations:

- Widening to skip `250` mostly multiplies already-dense short forms by about
  five. That is expected from the larger search space.
- Full phrases still remain weak or absent. United Nations, United States,
  United States of America, and European Union remain absent in both Hebrew and
  Greek forms at this range.
- `Simsberry` Hebrew appears once in MAM only at skip `2..250`, making it a
  source-specific screen, not a stable cross-version row.
- `Cowboy` Hebrew appears in every compatible Hebrew source family, but paired
  controls classify it as `not_unusual`.
- `Trump` Greek and `Turkey` Hebrew produced uncorrected paired-control screens
  only. After correction, the wide-focus control report does not promote them.

## Controls

The wide-focus paired-control report classified 66 representative rows:

- `not_unusual`: 63 rows;
- `paired_uncorrected_p_le_0.05`: 3 rows;
- corrected review rows: 0 rows.

This is the practical control result for modern/geopolitical/local screening:
raw detections are common, but the representative controlled screen does not
support claim-level promotion.

## Same-Skip Extensions

The same-skip extension tools check whether letters immediately before or after
an ELS hit at the same interval form a surface word or phrase in the same
language. This addresses compound hidden words and before/after phrases without
requiring the hidden word to appear openly in the same passage.

Current read:

- Modern-term extension tops are mostly ordinary biblical short forms such as
  Israel, Egypt, and Grace. They are useful as sanity checks, not claim rows.
- The stricter version-presence extension top files are empty at the current
  phrase-top threshold, though lower-level summaries contain ordinary phrase
  matches.
- The strong controlled extension row remains Greek `δοξα` (doxa; English: glory), skip `21`,
  forward, `term_plus_after`, hidden extension `δοξανωσ` (doxanos; English: hidden extension form from doxa), matching surface
  phrase `δόξαν ὡς` (doxan hos; English: glory as) at John 1:14. Deep controls give q = `0.000999` in both
  SBLGNT and TR_NT for the locked two-row follow-up.

## Current Claim Boundary

No broader-search modern, geopolitical, local, Gog/Magog, or prophetic row is
claim-level material. The current strongest rows are review candidates only:

- `δοξα` (doxa; English: glory) / `δοξανωσ` (doxanos; English: hidden extension form from doxa): strongest controlled Greek extension review candidate;
- `ανομια` (anomia; English: lawlessness), `ισαακ` (Isaak; English: Isaac), `τερασ` (teras; English: wonder): post-screen Greek surface review candidates;
- broad and wide modern/geopolitical rows: raw screens or control-weakened
  screens.

Before any external claim-level report, use the preregistration template,
placeholder checker, lock manifest builder, and lock checker:

```bash
python3 -m scripts.scaffold_prospective_study --name STUDY_NAME
python3 -m scripts.check_preregistration_placeholders docs/PROSPECTIVE_STUDY_PREREGISTRATION_TEMPLATE.md
python3 -m scripts.build_study_lock_manifest --name STUDY_NAME --path ...
python3 -m scripts.check_study_lock_manifest reports/study_locks/STUDY_NAME.manifest.json
```
