# Prospective Study Preregistration Template

Status: template; copy before use.

Copy this file to a study-specific preregistration document before any
result-producing run. Replace every bracketed placeholder, commit the
preregistration, build a lock manifest, validate it, then run the protocol.

## Study Identity

| Field | Value |
| --- | --- |
| Study name | `greek_surface_new_terms` |
| Study status | prospective candidate-discovery screen |
| Preregistration commit | `pending current preregistration commit` |
| Lock manifest | `reports/study_locks/greek_surface_new_terms.manifest.json` |
| Report document | `docs/GREEK_SURFACE_NEW_TERMS_REPORT.md` |

## Question

State the exact question in one paragraph.

Example shape:

Do declared `greek` terms produce `all-source exact-center surface rows` patterns
under fixed `2..50`, `both`, `ELS center verse contains normalized target as surface text`, and `all_available_same_length_real_word_controls`
rules?

## Term List

Locked term file:

- `terms/greek_surface_new_terms_clean_lock.csv`

Rules:

- source term files: `user-requested 2026-05-21 Greek term source, after prior-evidence screening`;
- language: `greek`;
- normalized minimum length: `5`;
- dedupe rule: `language + normalized term`;
- excluded prior rows/forms: `all terms and patterns already present in Greek expanded surface, Greek surface prospective evidence, and centered occurrence evidence`.

## Source Texts

Corpus/source labels:

- `TR_NT` from `configs/example_ebible_grctr.toml`;
- `BYZ_NT` from `configs/example_ebible_grcmt.toml`;
- `TCG_NT` from `configs/example_ebible_grctcgnt.toml`;
- `SBLGNT` from `configs/example_sblgnt.toml`.

State whether the sources are aligned version-comparison sources or broad
corpus-presence sources.

## Locked Settings

| Setting | Value |
| --- | --- |
| Skip range | `2..50` |
| Direction | `both` |
| Minimum normalized length | `5` |
| Candidate selection rule | `all four Greek NT sources have exact-center surface pattern with normalized length >= 5` |
| Context rule | `ELS center verse contains normalized target as surface text` |
| Control budget | `all_available_same_length_real_word_controls` |
| Correction method | `benjamini_hochberg_across_selected_rows` |

## Lock Manifest

Build:

```bash
python3 -m scripts.build_study_lock_manifest \
  --name greek_surface_new_terms \
  --path terms/greek_surface_new_terms_clean_lock.csv \
  --path protocols/greek_surface_new_terms.toml \
  --path configs/example_ebible_grctr.toml \
  --path configs/example_ebible_grcmt.toml \
  --path configs/example_ebible_grctcgnt.toml \
  --path configs/example_sblgnt.toml \
  --setting skip_range=2..50 \
  --setting direction=both \
  --setting min_normalized_length=5 \
  --setting controls=all_available_same_length_real_word_controls \
  --setting correction=benjamini_hochberg_across_selected_rows \
  --out reports/study_locks/greek_surface_new_terms.manifest.json
```

Validate:

```bash
python3 -m scripts.check_study_lock_manifest \
  reports/study_locks/greek_surface_new_terms.manifest.json \
  --required-setting skip_range \
  --required-setting direction \
  --required-setting min_normalized_length \
  --required-setting controls \
  --required-setting correction
```

Do not run the study if the checker fails.

## Protocol

Run:

```bash
python3 -m scripts.run_protocol protocols/greek_surface_new_terms.toml --resume
```

Expected outputs:

- `reports/greek_surface_new_terms/protocol_outputs.csv`;
- `reports/greek_surface_new_terms/protocol_run.manifest.json`;
- `docs/GREEK_SURFACE_NEW_TERMS_REPORT.md`.

## Primary Outcome

Primary row-level outcome:

- `selected row beats same-length controls by all-source exact-center surface-pattern count`

Primary study-level outcome:

- `BH q <= 0.05 across all tested selected rows`

## Candidate Labels

Allowed labels:

- `prospective_review_queue_candidate`;
- `prospective_controlled_review_candidate`;
- `source_specific_review_candidate`;
- `review_hold`;
- `not_reproducible`.

Disallowed labels:

- `confirmed_code`;
- `conclusive evidence`;
- `prophecy`;
- `statistical discovery`;
- `claim`.

## Failure Criteria

The study fails to produce a controlled review candidate if:

- required lock manifest validation fails;
- required inputs change after locking;
- no candidate rows meet the registered rule;
- required controls fail the registered threshold;
- required examples, context, or letter paths cannot be generated;
- the result depends on unregistered terms, spellings, sources, skip ranges, or
  broadened matching rules.

## Reporting Rules

The report must include:

- command used;
- git commit;
- lock manifest path;
- source text labels;
- term count;
- row counts at each stage;
- exact p/q values for every surviving row;
- examples and warning flags;
- context and letter-path output locations;
- pass/fail table against this preregistration;
- explicit statement that the run is review material, not conclusive evidence of meaning.

## Interpretation Boundary

This study may identify review candidates. It cannot establish theological,
prophetic, historical, or statistical claims by itself.
