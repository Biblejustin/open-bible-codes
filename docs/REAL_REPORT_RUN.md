# Real Report Run

Status: formal report assembly plan.

This document defines the first non-exploratory report assembly run. It does not
expand term lists or widen skip ranges. It refreshes locked outputs and produces
one local run summary.

## Command

```bash
python3 -m scripts.run_protocol protocols/real_report_run.toml --resume
```

Equivalent Make target:

```bash
make real-report
```

Generated local outputs:

- `reports/real_report_run/preflight.json`
- `reports/real_report_run/summary.md`
- `reports/real_report_run/manifest.json`
- `reports/real_report_run/protocol_run.manifest.json`
- `reports/INDEX.md`
- `reports/index.json`

## Included Tracks

This assembly run includes:

- STEP_TAHOT Hebrew source-family final gate:
  `docs/STEP_TAHOT_FINAL_GATE.md`
- Greek exact-center source-version pattern matrix:
  `docs/GREEK_PATTERN_VERSION_SUMMARY.md`
- Greek exact-center candidate-type final gate:
  `docs/GREEK_EXACT_CENTER_FINAL_GATE.md`
- Doxa four-source claim follow-up:
  `docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_REPORT.md`
- expanded Greek exact-center surface queue:
  `docs/GREEK_EXPANDED_SURFACE_QUEUE.md`
- expanded Greek exact-center surface triage:
  `docs/GREEK_EXPANDED_SURFACE_TRIAGE.md`
- expanded Greek exact-center surface letter-path audit:
  `docs/GREEK_EXPANDED_SURFACE_LETTER_PATHS.md`
- expanded Greek exact-center surface control pool:
  `docs/GREEK_EXPANDED_SURFACE_CONTROL_POOL.md`
- expanded Greek exact-center surface control evaluation:
  `docs/GREEK_EXPANDED_SURFACE_CONTROL_EVALUATION.md`
- expanded Greek exact-center surface all-available control evaluation:
  `docs/GREEK_EXPANDED_SURFACE_AVAILABLE_CONTROL_POOL.md` and
  `docs/GREEK_EXPANDED_SURFACE_AVAILABLE_CONTROL_EVALUATION.md`
- expanded Greek exact-center surface compact follow-up:
  `docs/GREEK_EXPANDED_SURFACE_FOLLOWUP_REPORT.md`
- locked Greek surface prospective run:
  `docs/GREEK_SURFACE_PROSPECTIVE_PREREGISTRATION.md` and
  `docs/GREEK_SURFACE_PROSPECTIVE_REPORT.md`
- post-discovery Greek surface length-4 follow-up:
  `docs/GREEK_SURFACE_LENGTH4_FOLLOWUP_TRIAGE.md`,
  `docs/GREEK_SURFACE_LENGTH4_CONTROL_POOL.md`,
  `docs/GREEK_SURFACE_LENGTH4_CONTROL_EVALUATION.md`, and
  `docs/GREEK_SURFACE_LENGTH4_LETTER_PATHS.md`
- generated Greek surface length-4 vocabulary controls:
  `docs/GREEK_SURFACE_LENGTH4_VOCABULARY_CONTROLS.md`,
  `docs/GREEK_SURFACE_LENGTH4_VOCABULARY_CONTROL_POOL.md`, and
  `docs/GREEK_SURFACE_LENGTH4_VOCABULARY_CONTROL_EVALUATION.md`
- WRR 1994 source/import/text-lock/count/pair-table/perturbation-boundary audit
  plus repo-defined cross-pair permutation diagnostic:
  `docs/WRR_SOURCE_AUDIT.md`, `docs/WRR_METHODOLOGY_GAPS.md`,
  `docs/WRR_CORRECTED_DISTANCE_NOTES.md`, `docs/WRR_CROSS_PAIR_GRID.md`, and
  `docs/WRR_LOCK_OPTIONS.md`, plus `docs/WRR_SOURCE_POLICY_SCENARIOS.md`,
  `docs/WRR_SOURCE_POLICY_EVIDENCE_PACKET.md`,
  `docs/WRR_DW_FORMULA_SENSITIVITY.md`, `docs/WRR_CLAIM_READINESS.md`, and
  `docs/WRR_CLAIM_BLOCKER_PACKET.md`, plus
  `docs/WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md`
- broader search/current findings writeup:
  `docs/BROADER_SEARCH_FINDINGS.md`
- broad Hebrew modern/geopolitical version-distribution run:
  `docs/HEBREW_MODERN_GEOPOLITICAL_VERSION_PRESENCE.md`
- broad Hebrew modern/geopolitical representative-control review:
  `docs/HEBREW_MODERN_GEOPOLITICAL_CONTROLLED_REVIEW.md`
- locked Hebrew modern/geopolitical prospective source-distribution report:
  `docs/HEBREW_MODERN_GEOPOLITICAL_PROSPECTIVE_REPORT.md` and
  `docs/HEBREW_MODERN_GEOPOLITICAL_PROSPECTIVE_FINDINGS.md`
- locked KJVA apocrypha/deuterocanon bridge prospective run:
  `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_PREREGISTRATION.md`,
  `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CONTROLS_5000.md`, and
  `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_NONBIBLE_CONTROLS.md`
- broader Hebrew screening representative-control review:
  `docs/HEBREW_SCREENING_CONTROLLED_REVIEW.md`
- relaxed all-codes follow-up:
  `docs/ALL_CODES_FOLLOWUP_SELECTION.md`,
  `docs/ALL_CODES_FOLLOWUP_LETTER_PATHS.md`,
  `docs/ALL_CODES_FOLLOWUP_CONTEXT.md`,
  `docs/ALL_CODES_FOLLOWUP_EXTENSIONS.md`,
  `docs/ALL_CODES_COMPOUND_EXTENSION_CONTROLS.md`,
  `docs/ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_CONTROLS.md`, and
  `docs/ALL_CODES_FOLLOWUP_REVIEW.md`
- centered occurrence index:
  `docs/CENTERED_OCCURRENCE_INDEX.md`
- CRD exact center-word broad-screen findings:
  `docs/CRD_CENTER_WORD_SELF_VS_CONCEPT_FINDINGS.md` and
  `docs/CRD_CENTER_WORD_VERSION_PRESENCE_FINDINGS.md`
- prospective study readiness matrix:
  `docs/PROSPECTIVE_STUDY_READINESS.md`
- prospective term-leakage audit workflow:
  `docs/PROSPECTIVE_TERM_AUDITS.md`
- generated report index:
  `reports/INDEX.md`
- reader-facing final report scaffold:
  `docs/FINAL_REPORT_OUTLINE.md`
- reader-facing final report:
  `docs/FINAL_REPORT.md`

## Preflight Rules

The protocol starts with `scripts.preflight_real_report_run`.

It requires:

- clean git working tree;
- Git remotes pointing at `Biblejustin/open-bible-codes`;
- no forbidden non-`Biblejustin` account text in remotes or tracked/repository
  files checked by the guard;
- no tracked report/database/raw-source artifacts beyond allowed placeholders;
- no high-confidence secret-token patterns in tracked files;
- required protocols, docs, and term files present;
- prospective lane profiles valid, with registered term/protocol/report paths
  present;
- English source-basis manifests and audit-queue counts valid, with no current
  `needs_audit` rows unless the policy is explicitly changed;
- expanded-strata operator docs point at live scripts, protocol files, and
  Make targets;
- future study-mapping CSV schemas retain required columns, required locked
  values, and supported language markers;
- concrete preregistration docs contain no unresolved bracketed placeholders
  while the prospective-study template remains available as a template;
- CRD relevance dictionary, term coverage, reviewer metadata, and protocol
  hash lock are still consistent with the centered-relevance protocol;
- manual-review queue keeps required non-claim guardrails and evidence links;
- WRR method-status doc keeps local locks separated from open blockers and
  diagnostic-only rows;
- WRR lock-options doc remains a decision aid rather than a method lock;
- WRR claim-readiness doc still carries blocked status and all four blocker
  areas until source/method locks change;
- WRR claim-blocker packet still states no-input limits, open method decisions,
  and no pair-exclusion or `D(w)` formula choice;
- checked-in `docs/INDEX.md` and `protocols/INDEX.md` freshness;
- existing generated inputs needed by the final gates.

The protocol is meant to be run from a committed state. During development, run
the preflight directly with `--allow-dirty` only for local debugging.

The `preflight` and final `real_report_summary` steps are marked
`always_run = true`. Cached upstream reports can still be reused, but every
formal resume rechecks release hygiene and refreshes current commit/timestamp
metadata.

## Candidate Taxonomy

Reports should separate discovery from interpretation:

- `detected`: software found a row;
- `hidden_path_candidate`: hidden ELS term or phrase exists;
- `surface_anchored_hidden_candidate`: hidden path has related surface context;
- `surface_echo_candidate`: hidden phrase also appears openly in the same span
  or nearby passage;
- `cross_version_controlled_candidate`: exact key appears across source texts and
  survives row-local controls;
- `review_candidate_not_claim`: worth reading, but not a claim.

Hidden-path-only rows are normal ELS candidates, not failures. A same-span
surface echo is rarer and stronger, but it is not required for review-candidate
status.

For centered-self and relevant-center rows, occurrence is the primary review
fact: the row should be listed if it happens. Counts and controls describe
frequency strength, but they do not remove the occurrence from the findings
list.

## What This Run Does Not Do

This run does not:

- add or modify term lists;
- change skip ranges;
- treat capped exploratory scans as claim-grade statistics;
- promote any row to a claim;
- rerun all expensive upstream searches unless their existing protocol stamps
  require it.

## Current Report-Level Read

The report-run summary should currently say:

- STEP_TAHOT-only behavior is not meaningful by itself because the real-term and
  null/frequency-control source-only rates are nearly identical.
- `δοξα` (doxa; English: glory) is the strongest Greek row: a cross-version controlled
  surface-anchored hidden candidate.
- A later locked four-source 5000/5000 follow-up is tracked in
  `docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_REPORT.md`, and a stricter
  20000/20000 confirmatory follow-up is tracked in
  `docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md`; both keep `δοξα` (doxa; English: glory)
  at review candidate status, not claim status.
- The expanded Greek surface queue is tracked as post-screen review material:
  exact-center surface means center verse surface context, not necessarily a
  matching center word.
- Centered-self and relevant-center rows should be reported as occurrences
  first, with frequency/control strength reported separately.
- The centered occurrence index is the dedicated artifact for that
  occurrence-first final-report layer.
- The tighter surface triage keeps only all-source rows with normalized length
  >= 5 and treats them as review rows needing real-word matched controls.
- The selected surface letter-path audit reconstructs each selected ELS path in
  all four Greek NT source labels and confirms the normalized sequence.
- The surface control pool measures real-word normalized surface-substring
  frequency before any ELS surface-control statistic is run.
- The first surface control evaluation is exploratory only because 10 controls
  per target cannot produce add-one p <= 0.05.
- The all-available surface control evaluation excludes selected targets from
  the control pool; all three selected rows exceed the available same-length
  controls with q = 0.032258, but this is still post-screen.
- The compact surface follow-up joins selected rows, reconstructed letter
  paths, and all-available controls into one review sheet. Its status remains
  `post_screen_surface_followup_review_candidate`, not claim status.
- The locked Greek surface prospective run is negative at the registered
  length >= 5 primary gate. Its length-4 all-source bucket is kept as a
  separate post-discovery follow-up, not as prospective discovery.
- The length-4 Greek surface follow-up has rows that exceed available
  same-length controls, but the available pool bottoms out at p/q = 0.066667,
  so it remains triage evidence rather than claim-grade evidence.
- The generated length-4 vocabulary-control follow-up weakens that signal:
  200 matched controls are available per target, controls overlap every target,
  and no target survives study-level q <= 0.05.
- WRR now has locked local evidence: the accepted cap-1000 keep-all 999,999
  date-label permutation run reports Bonferroni `rho0 = 0.000404` over 182
  observed rows and 72 defined `c(w,w')` values. Exact published WRR
  reproduction remains caveated by source-transcription limits and the
  163-distance gap. The explicit readiness gate is tracked in
  `docs/WRR_CLAIM_READINESS.md`; `docs/WRR_CLAIM_BLOCKER_PACKET.md` records
  that no current claim-readiness blockers remain under the selected local lock
  policy; `docs/WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md` keeps the residual
  source/term/method evidence lanes visible without selecting corrections;
  `docs/WRR_SOURCE_POLICY_EVIDENCE_PACKET.md` ties the Chełm source-policy
  residual to WNP context, row OCR, and scenario status without changing the
  source lock.
- `υιοσ` (huios; English: son) and `αιμα` (haima; English: blood) remain weaker hidden-path candidates because their exact
  patterns are missing from one or more compared Greek NT sources.
- no row is claim-grade yet.
- The broad Hebrew modern/geopolitical controlled review adds representative
  MT_WLC/UHB controls for the new all-Hebrew-row modern/geopolitical run; no
  row has adjusted representative-control support.
- The broader Hebrew screening controlled review extends that control pass to
  theological, modern, Table of Nations, prophetic, Hebrew claim, tribe,
  festival, and calendar rows; no row has adjusted representative-control
  support.
- The relaxed all-codes follow-up keeps hidden-path-only rows and separately
  ranks surface-near rows. The locked 5000/5000 compound-extension
  confirmatory controls keep the selected `יום יהוה` (yom YHWH; English: day of YHWH) -> `היומיהוה` (hayom YHWH; English: the day of YHWH) key across
  all five MT-family sources at conservative all-control q = 0.003599. It is a
  post-discovery review candidate, not a claim.

## Before Claim-Level Reporting

A claim-grade report needs a narrower predeclared study:

- fixed term list;
- fixed source set;
- fixed skip range;
- fixed direction;
- fixed control budget;
- fixed correction method across all tested rows;
- interpretation labels decided before viewing results.

For Greek exact-center surface rows, the stricter prospective standard is
tracked in `docs/GREEK_SURFACE_PROSPECTIVE_CLAIM_STANDARD.md`.
