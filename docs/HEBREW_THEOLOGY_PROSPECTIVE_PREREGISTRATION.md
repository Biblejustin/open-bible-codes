# Hebrew Theology Prospective Preregistration

Status: registered follow-up candidate-discovery screen.

This document freezes a narrow Hebrew theology cohort before running the
result-producing protocol below. Earlier broad exploratory Hebrew screens exist,
so this is a registered follow-up, not an untouched discovery run. The fixed
value here is that the term list, source set, skip range, control budget, and
candidate rule are declared before this specific controlled report is run.

## Study Identity

| Field | Value |
| --- | --- |
| Study name | `hebrew_theology_prospective` |
| Study status | registered follow-up candidate-discovery screen |
| Preregistration commit | recorded by the lock manifest before the run |
| Lock manifest | `reports/study_locks/hebrew_theology_prospective.manifest.json` |
| Report document | `docs/HEBREW_THEOLOGY_PROSPECTIVE_REPORT.md` |

## Question

Do declared Hebrew divine-name, covenant, messianic, soteriology, and core
attribute terms produce exact ELS ref-key patterns across MT-family sources
under fixed `2..100`, `both`, and representative paired-control rules?

The study records which exact patterns appear in which Hebrew source. Absence
from a source is data, not automatic failure.

## Term List

Locked term file:

- `terms/hebrew_theology_prospective_terms.csv`

Fixed generation rules:

- Hebrew rows only;
- 20 declared terms;
- normalized length at least 4 for exact-version and control review;
- no duplicate term IDs inside the locked file;
- no extra spellings, transliterations, or post-run term additions.

## Source Texts

Compared Hebrew source labels:

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
| Candidate selection rule | exact ref-key version-presence rows joined to representative paired controls |
| Context rule | hidden-path-only rows and clear-text echo rows are both reportable; clear-text echo is stronger but not required |
| Control budget | `1000` term-shuffle samples and `1000` random same-length samples per selected MT_WLC/UHB target |
| Correction method | Benjamini-Hochberg correction across representative paired-control rows |

## Lock Manifest

Build after this document, the term file, and the protocol are committed:

```bash
python3 -m scripts.build_study_lock_manifest \
  --name hebrew_theology_prospective \
  --path docs/HEBREW_THEOLOGY_PROSPECTIVE_PREREGISTRATION.md \
  --path terms/hebrew_theology_prospective_terms.csv \
  --path protocols/hebrew_theology_prospective.toml \
  --path configs/example_oshb_wlc.toml \
  --path configs/example_uxlc.toml \
  --path configs/example_ebible_hebwlc.toml \
  --path configs/example_mam.toml \
  --path configs/example_uhb.toml \
  --setting skip_range=2..100 \
  --setting direction=both \
  --setting min_normalized_length=4 \
  --setting controls=1000_term_shuffle_plus_1000_random_same_length_per_selected_MT_WLC_UHB_target \
  --setting correction=benjamini_hochberg \
  --setting source_set=MT_WLC,UXLC,EBIBLE_WLC,MAM,UHB \
  --setting representative_control_corpora=MT_WLC,UHB \
  --setting selection_rule=exact_ref_key_version_presence_with_representative_controls \
  --out reports/study_locks/hebrew_theology_prospective.manifest.json
```

Validate:

```bash
python3 -m scripts.preflight_prospective_study \
  --preregistration docs/HEBREW_THEOLOGY_PROSPECTIVE_PREREGISTRATION.md \
  --manifest reports/study_locks/hebrew_theology_prospective.manifest.json \
  --protocol protocols/hebrew_theology_prospective.toml \
  --required-setting source_set \
  --required-setting representative_control_corpora \
  --required-setting selection_rule
```

Do not run the study if the preflight fails.

## Protocol

Run only after lock preflight passes:

```bash
python3 -m scripts.run_protocol protocols/hebrew_theology_prospective.toml --resume
```

Expected outputs:

- `reports/hebrew_theology_prospective/hit_patterns.csv`;
- `reports/hebrew_theology_prospective/term_summary.csv`;
- `reports/hebrew_theology_prospective/control_targets.csv`;
- `reports/hebrew_theology_prospective/paired_controls_summary.csv`;
- `reports/hebrew_theology_prospective/controlled_summary.csv`;
- `reports/hebrew_theology_prospective/protocol_run.manifest.json`;
- `docs/HEBREW_THEOLOGY_PROSPECTIVE_REPORT.md`.

## Primary Outcome

Primary row-level outcome:

- a term with exact-version rows and representative paired-control
  `combined_min_q_value <= 0.05`.

Primary study-level outcome:

- at least one selected row survives the registered representative-control rule
  after Benjamini-Hochberg correction.

Review-candidate threshold:

- uncorrected `combined_min_p_ge <= 0.05` may be reported as a follow-up prompt
  only when `combined_min_q_value > 0.05`; it is not claim-grade support.

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
- no candidate rows meet the registered exact-version rule;
- required controls fail the registered threshold;
- the result depends on unregistered terms, spellings, sources, skip ranges, or
  broadened matching rules.

## Reporting Rules

The report must include:

- command used;
- git commit from the lock manifest;
- lock manifest path;
- source text labels;
- term count;
- row counts at each stage;
- exact p/q values for every surviving row;
- examples and warning flags;
- pass/fail read against this preregistration;
- explicit statement that the run is review material, not conclusive evidence of meaning.

## Interpretation Boundary

This study may identify registered follow-up review candidates. It cannot
establish theological, prophetic, historical, or statistical claims by itself.
