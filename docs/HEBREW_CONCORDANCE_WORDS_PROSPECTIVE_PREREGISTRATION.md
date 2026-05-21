# Prospective Study Preregistration Template

Status: template; copy before use.

Copy this file to a study-specific preregistration document before any
result-producing run. Replace every bracketed placeholder, commit the
preregistration, build a lock manifest, validate it, then run the protocol.

## Study Identity

| Field | Value |
| --- | --- |
| Study name | `hebrew_concordance_words_prospective` |
| Study status | prospective candidate-discovery screen |
| Preregistration commit | `pending current preregistration commit` |
| Lock manifest | `reports/study_locks/hebrew_concordance_words_prospective.manifest.json` |
| Report document | `docs/HEBREW_CONCORDANCE_WORDS_PROSPECTIVE_REPORT.md` |

## Question

State the exact question in one paragraph.

Example shape:

Do declared `hebrew` terms produce `open-concordance Hebrew headword rows` patterns
under fixed `2..100`, `both`, `version-presence matrix; no surface-context promotion before clean lock`, and `representative MT_WLC and UHB shuffled-term/random controls after clean lock`
rules?

## Term List

Locked term file:

- `terms/hebrew_concordance_prospective_terms_clean_lock.csv`

Rules:

- source term files: `OpenScriptures StrongHebrewG headwords cross-checked against STEP Bible TAHOT main lexical tags`;
- language: `hebrew`;
- normalized minimum length: `4`;
- dedupe rule: `language + normalized term`;
- excluded prior rows/forms: `all exact/review overlaps from prior term pools and centered occurrence evidence`.

## Source Texts

Corpus/source labels:

- `MT_WLC` from `configs/example_oshb_wlc.toml`;
- `UXLC` from `configs/example_uxlc.toml`;
- `EBIBLE_WLC` from `configs/example_ebible_hebwlc.toml`;
- `MAM` from `configs/example_mam.toml`;
- `UHB` from `configs/example_uhb.toml`.

State whether the sources are aligned version-comparison sources or broad
corpus-presence sources.

## Locked Settings

| Setting | Value |
| --- | --- |
| Skip range | `2..100` |
| Direction | `both` |
| Minimum normalized length | `4` |
| Candidate selection rule | `headword is in StrongHebrewG, normalized length >= 4, and appears as STEP TAHOT main lexical tag` |
| Context rule | `version-presence matrix; no surface-context promotion before clean lock` |
| Control budget | `representative MT_WLC and UHB shuffled-term/random controls after clean lock` |
| Correction method | `benjamini_hochberg_across_representative_control_rows` |

## Lock Manifest

Build:

```bash
python3 -m scripts.build_study_lock_manifest \
  --name hebrew_concordance_words_prospective \
  --path terms/hebrew_concordance_prospective_terms_clean_lock.csv \
  --path protocols/hebrew_concordance_words_prospective.toml \
  --path configs/example_oshb_wlc.toml \
  --path configs/example_uxlc.toml \
  --path configs/example_ebible_hebwlc.toml \
  --path configs/example_mam.toml \
  --path configs/example_uhb.toml \
  --setting skip_range=2..100 \
  --setting direction=both \
  --setting min_normalized_length=4 \
  --setting 'controls=representative MT_WLC and UHB shuffled-term/random controls after clean lock' \
  --setting correction=benjamini_hochberg_across_representative_control_rows \
  --out reports/study_locks/hebrew_concordance_words_prospective.manifest.json
```

Validate:

```bash
python3 -m scripts.check_study_lock_manifest \
  reports/study_locks/hebrew_concordance_words_prospective.manifest.json \
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
python3 -m scripts.run_protocol protocols/hebrew_concordance_words_prospective.toml --resume
```

Expected outputs:

- `reports/hebrew_concordance_words_prospective/protocol_outputs.csv`;
- `reports/hebrew_concordance_words_prospective/protocol_run.manifest.json`;
- `docs/HEBREW_CONCORDANCE_WORDS_PROSPECTIVE_REPORT.md`.

## Primary Outcome

Primary row-level outcome:

- `version-presence scope plus representative-control q value`

Primary study-level outcome:

- `source-distribution report until a clean locked cohort is promoted`

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
