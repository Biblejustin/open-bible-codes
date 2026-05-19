# Hebrew Modern Geopolitical Presence Preregistration

Status: registered source-distribution follow-up.

This document freezes a Hebrew modern/geopolitical source-distribution cohort
before the result-producing protocol below. Earlier broad screens exist, so
this is not an untouched discovery run and must not be relabeled as such. The
fixed value here is that the term list, source set, skip range, and
representative-control rules are declared before this specific report is run.

## Study Identity

| Field | Value |
| --- | --- |
| Study name | `hebrew_modern_geopolitical_presence` |
| Study status | registered source-distribution follow-up |
| Preregistration commit | recorded by the lock manifest before the run |
| Lock manifest | `reports/study_locks/hebrew_modern_geopolitical_presence.manifest.json` |
| Report document | `docs/HEBREW_MODERN_GEOPOLITICAL_PROSPECTIVE_REPORT.md` |

## Question

Do declared Hebrew modern leader, country, organization, event, and Israeli
prime-minister terms produce exact ELS ref-key patterns across MT-family sources
under fixed `2..100`, `both`, and representative paired-control rules?

The study records which exact patterns appear in which Hebrew source. Absence
from a source is data, not automatic failure. This lane is source-distribution
review material, not claim promotion.

## Term List

Locked term file:

- `terms/hebrew_modern_geopolitical_prospective_terms.csv`

Rules:

- source term file: `terms/hebrew_modern_geopolitical_prospective_terms.csv`;
- source rows: Hebrew `modern_names`, `modern_places`, `modern_events`, and
  `israeli_prime_ministers` rows copied from `terms/modern_names_dates.csv`;
- locked row count: `77`;
- normalized minimum length: `4`;
- dedupe rule: `language + normalized term`;
- excluded prior rows/forms: `full broad-screen result rows are prior evidence and must not be relabeled as discovery`.

## Source Texts

Corpus/source labels:

- `MT_WLC` from `configs/example_oshb_wlc.toml`;
- `UXLC` from `configs/example_uxlc.toml`;
- `EBIBLE_WLC` from `configs/example_ebible_hebwlc.toml`;
- `MAM` from `configs/example_mam.toml`;
- `UHB` from `configs/example_uhb.toml`.

The Leningrad-family comparison labels are `MT_WLC`, `UXLC`, and `EBIBLE_WLC`.
The representative control corpora are `MT_WLC` and `UHB`.

## Locked Settings

| Setting | Value |
| --- | --- |
| Skip range | `2..100` |
| Direction | `both` |
| Minimum normalized length | `4` |
| Candidate selection rule | `predeclared exact ref-key source-version presence, reported as distribution not claim support` |
| Context rule | `version-presence matrix; no surface-context promotion` |
| Hit cap | `200` hits per term per corpus for version-presence pattern collection |
| Control budget | `1000` term-shuffle samples and `1000` random same-length samples per selected MT_WLC/UHB target |
| Correction method | `benjamini_hochberg_across_representative_control_rows` |

## Lock Manifest

Build:

```bash
python3 -m scripts.build_study_lock_manifest \
  --name hebrew_modern_geopolitical_presence \
  --path docs/HEBREW_MODERN_GEOPOLITICAL_PRESENCE_PREREGISTRATION.md \
  --path terms/hebrew_modern_geopolitical_prospective_terms.csv \
  --path protocols/hebrew_modern_geopolitical_prospective.toml \
  --path configs/example_oshb_wlc.toml \
  --path configs/example_uxlc.toml \
  --path configs/example_ebible_hebwlc.toml \
  --path configs/example_mam.toml \
  --path configs/example_uhb.toml \
  --setting skip_range=2..100 \
  --setting direction=both \
  --setting min_normalized_length=4 \
  --setting max_hits_per_term=200 \
  --setting controls=1000_term_shuffle_plus_1000_random_same_length_per_selected_MT_WLC_UHB_target \
  --setting correction=benjamini_hochberg_across_representative_control_rows \
  --setting source_set=MT_WLC,UXLC,EBIBLE_WLC,MAM,UHB \
  --setting representative_control_corpora=MT_WLC,UHB \
  --setting selection_rule=exact_ref_key_version_presence_with_representative_controls \
  --out reports/study_locks/hebrew_modern_geopolitical_presence.manifest.json
```

Validate:

```bash
python3 -m scripts.preflight_prospective_study \
  --preregistration docs/HEBREW_MODERN_GEOPOLITICAL_PRESENCE_PREREGISTRATION.md \
  --manifest reports/study_locks/hebrew_modern_geopolitical_presence.manifest.json \
  --protocol protocols/hebrew_modern_geopolitical_prospective.toml \
  --required-setting max_hits_per_term \
  --required-setting source_set \
  --required-setting representative_control_corpora \
  --required-setting selection_rule
```

Do not run the study if the preflight fails.

## Protocol

Run:

```bash
python3 -m scripts.run_protocol protocols/hebrew_modern_geopolitical_prospective.toml --resume
```

Expected outputs:

- `reports/hebrew_modern_geopolitical_prospective/hit_patterns.csv`;
- `reports/hebrew_modern_geopolitical_prospective/term_summary.csv`;
- `reports/hebrew_modern_geopolitical_prospective/control_targets.csv`;
- `reports/hebrew_modern_geopolitical_prospective/paired_controls_summary.csv`;
- `reports/hebrew_modern_geopolitical_prospective/controlled_summary.csv`;
- `reports/hebrew_modern_geopolitical_prospective/protocol_run.manifest.json`;
- `docs/HEBREW_MODERN_GEOPOLITICAL_PROSPECTIVE_REPORT.md`.

## Primary Outcome

Primary row-level outcome:

- `version-presence scope plus representative-control q value`

Primary study-level outcome:

- `source-distribution report; no claim-grade promotion`

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
- generated report and control output locations;
- pass/fail table against this preregistration;
- explicit statement that the run is review material, not conclusive evidence of meaning.

## Interpretation Boundary

This study may identify review candidates. It cannot establish theological,
prophetic, historical, or statistical claims by itself.
