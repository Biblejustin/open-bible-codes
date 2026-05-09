# Greek Surface Prospective Preregistration

Status: prospective candidate-discovery screen.

This document freezes a new Greek exact-center surface-context cohort before
running the new result-producing protocol. It uses the default lane identified
in `docs/PROSPECTIVE_STUDY_READINESS.md`: Greek surface rows, with prior
selected rows removed before locking.

## Study Identity

| Field | Value |
| --- | --- |
| Study name | `greek_surface_prospective` |
| Study status | prospective candidate-discovery screen |
| Preregistration commit | recorded by the lock manifest before the run |
| Lock manifest | `reports/study_locks/greek_surface_prospective.manifest.json` |
| Report documents | `docs/GREEK_SURFACE_PROSPECTIVE_REPORT.md`; `docs/GREEK_SURFACE_PROSPECTIVE_QUEUE.md`; `docs/GREEK_SURFACE_PROSPECTIVE_TRIAGE.md`; `docs/GREEK_SURFACE_PROSPECTIVE_CONTROL_EVALUATION.md`; `docs/GREEK_SURFACE_PROSPECTIVE_LETTER_PATHS.md` |

## Question

Do declared Greek theological, biblical, apocalyptic, festival, tribe, and
Table-of-Nations terms, after removing already-selected prior evidence rows,
produce exact-center surface-context ELS patterns under fixed `2..50`, `both`,
and all-source Greek NT version-presence rules?

## Term List

Locked term file:

- `terms/greek_surface_prospective_terms.csv`

Source term file before filtering:

- `terms/greek_expanded_prospective_terms.csv`

Prior evidence audit:

```bash
python3 -m scripts.audit_prospective_terms \
  --candidate terms/greek_expanded_prospective_terms.csv \
  --evidence reports/greek_expanded_surface_triage/selected_patterns.csv \
  --evidence reports/extension_exact_center_deep_controls_summary.csv \
  --min-normalized-length 5 \
  --out reports/study_locks/greek_surface_prospective_prior_evidence_audit.csv \
  --fail-on-match
```

The audit is expected to fail before filtering because it should find already
selected rows. The term file is then filtered:

```bash
python3 -m scripts.filter_prospective_terms \
  --candidate terms/greek_expanded_prospective_terms.csv \
  --audit reports/study_locks/greek_surface_prospective_prior_evidence_audit.csv \
  --out terms/greek_surface_prospective_terms.csv \
  --summary-out reports/study_locks/greek_surface_prospective_terms.filter.summary.json \
  --min-remaining 200
```

Fixed generation rules:

- Greek rows only;
- normalized length at least 4 in the source list;
- exact prior evidence overlaps removed before this preregistration is locked;
- dropped prior rows: `gpx_isaac_g`, `gpx_lawlessness_g`, `gpx_wonder_g`;
- final locked term count: 288 rows;
- primary analysis threshold: normalized length at least 5.

## Source Texts

Compared Greek NT source labels:

- `TR_NT` from `configs/example_ebible_grctr.toml`;
- `BYZ_NT` from `configs/example_ebible_grcmt.toml`;
- `TCG_NT` from `configs/example_ebible_grctcgnt.toml`;
- `SBLGNT` from `configs/example_sblgnt.toml`.

The study records which exact pattern appears in which source. Absence from a
source is data, not automatic failure.

## Locked Settings

| Setting | Value |
| --- | --- |
| Skip range | `2..50` |
| Direction | `both` |
| Minimum normalized length | `5` |
| Candidate selection rule | all-source exact-center surface-context rows with normalized length at least 5 |
| Context rule | center verse contains the normalized key term as surface text |
| Control budget | all available same-length, all-source real-word surface-frequency controls from the locked term file |
| Correction method | Benjamini-Hochberg correction across selected prospective rows |

## Lock Manifest

Build after this document, the term file, and the protocol are committed:

```bash
python3 -m scripts.build_study_lock_manifest \
  --name greek_surface_prospective \
  --path docs/GREEK_SURFACE_PROSPECTIVE_PREREGISTRATION.md \
  --path terms/greek_surface_prospective_terms.csv \
  --path protocols/greek_surface_prospective.toml \
  --path configs/example_ebible_grctr.toml \
  --path configs/example_ebible_grcmt.toml \
  --path configs/example_ebible_grctcgnt.toml \
  --path configs/example_sblgnt.toml \
  --path reports/study_locks/greek_surface_prospective_prior_evidence_audit.csv \
  --path reports/study_locks/greek_surface_prospective_prior_evidence_audit.csv.summary.json \
  --path reports/study_locks/greek_surface_prospective_terms.filter.summary.json \
  --setting skip_range=2..50 \
  --setting direction=both \
  --setting min_normalized_length=5 \
  --setting controls=all_available_same_length_surface_frequency_controls \
  --setting correction=benjamini_hochberg \
  --setting source_set=TR_NT,BYZ_NT,TCG_NT,SBLGNT \
  --setting selection_rule=all_source_exact_center_surface_min_length_5 \
  --setting prior_evidence_exclusion=gpx_isaac_g,gpx_lawlessness_g,gpx_wonder_g \
  --out reports/study_locks/greek_surface_prospective.manifest.json
```

Validate:

```bash
python3 -m scripts.preflight_prospective_study \
  --preregistration docs/GREEK_SURFACE_PROSPECTIVE_PREREGISTRATION.md \
  --manifest reports/study_locks/greek_surface_prospective.manifest.json \
  --protocol protocols/greek_surface_prospective.toml \
  --clean-term-audit reports/study_locks/greek_surface_prospective_clean_audit.csv.summary.json
```

The clean audit is run against the filtered term file and must pass:

```bash
python3 -m scripts.audit_prospective_terms \
  --candidate terms/greek_surface_prospective_terms.csv \
  --evidence reports/greek_expanded_surface_triage/selected_patterns.csv \
  --evidence reports/extension_exact_center_deep_controls_summary.csv \
  --min-normalized-length 5 \
  --out reports/study_locks/greek_surface_prospective_clean_audit.csv \
  --fail-on-match
```

Do not run the study if the preflight fails.

## Protocol

Run only after lock preflight passes:

```bash
python3 -m scripts.run_protocol protocols/greek_surface_prospective.toml --resume
```

Expected outputs:

- `reports/greek_surface_prospective/surface_context_hits.csv`;
- `reports/greek_surface_prospective/surface_patterns.csv`;
- `reports/greek_surface_prospective/selected_patterns.csv`;
- `reports/greek_surface_prospective/matched_controls.csv`;
- `reports/greek_surface_prospective/control_summary.csv`;
- `reports/greek_surface_prospective/path_summary.csv`;
- `reports/greek_surface_prospective/protocol_run.manifest.json`;
- `docs/GREEK_SURFACE_PROSPECTIVE_REPORT.md`;
- `docs/GREEK_SURFACE_PROSPECTIVE_QUEUE.md`;
- `docs/GREEK_SURFACE_PROSPECTIVE_TRIAGE.md`;
- `docs/GREEK_SURFACE_PROSPECTIVE_CONTROL_POOL.md`;
- `docs/GREEK_SURFACE_PROSPECTIVE_CONTROL_EVALUATION.md`;
- `docs/GREEK_SURFACE_PROSPECTIVE_LETTER_PATHS.md`.

## Primary Outcome

Primary row-level outcome:

- all-source exact-center surface-context row with `all_source_q_value <= 0.05`
  under the all-available same-length real-word control evaluation.

Primary study-level outcome:

- at least one selected row survives the registered all-source control rule
  after Benjamini-Hochberg correction.

## Candidate Labels

Allowed labels:

- `prospective_review_queue_candidate`;
- `prospective_controlled_review_candidate`;
- `source_specific_review_candidate`;
- `review_hold`;
- `not_reproducible`.

Disallowed labels:

- `confirmed_code`;
- `proof`;
- `prophecy`;
- `statistical discovery`;
- `claim`.

## Failure Criteria

The study fails to produce a controlled review candidate if:

- required lock manifest validation fails;
- the clean term audit fails;
- required inputs change after locking;
- no candidate rows meet the registered all-source exact-center surface rule;
- required controls fail the registered threshold;
- required letter paths cannot be generated;
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
- letter-path output locations;
- pass/fail read against this preregistration;
- explicit statement that the run is review material, not proof of meaning.

## Interpretation Boundary

This study may identify prospective review candidates. It cannot establish
theological, prophetic, historical, or statistical claims by itself.
