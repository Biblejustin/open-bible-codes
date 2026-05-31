# Real Report Run

Status: formal report assembly plan.

This document defines the first non-exploratory report assembly run. It does not
expand term lists or widen skip ranges. It refreshes locked outputs and produces
one local run summary.

Reader role: use this file to see what the report assembly is allowed to touch
and which guardrails must pass before the reader-facing report is considered
current. Use `docs/START_HERE.md` and `docs/FINAL_REPORT.md` for narrative
reading; use this file for reproducibility and preflight scope.

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
- clean-lock close-out and strict follow-up summary:
  `docs/CLEAN_LOCK_RESULTS_SUMMARY.md`,
  `docs/STRICT_FOLLOWUP_GATE_SUMMARY.md`, and
  `docs/GREEK_LEXICON_EXTENSION_PROSPECTIVE_REPORT.md`
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
  `docs/WRR_SOURCE_POLICY_REVIEW_CHECKLIST.md`,
  `docs/WRR_SOURCE_TRANSCRIPTION_EVIDENCE_PACKET.md`,
  `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md`,
  `docs/WRR_SOURCE_ROW_CROP_PACKET.md`,
  `docs/WRR_SOURCE_ROW_CROP_CONTACT_SHEET.md`,
  `docs/WRR_SOURCE_ROW_CROP_REVIEW_HTML.md`,
  `docs/WRR_SOURCE_ROW_OCR_WORD_PACKET.md`,
  `docs/WRR_SOURCE_ROW_REVIEW_BUNDLE.md`,
  `docs/WRR_POST_LOCK_REPORTING_BOUNDARY.md`,
  `docs/WRR_REMAINING_LANE_EVIDENCE_PACKETS.md`,
  `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md`,
  `docs/WRR_MANUAL_DECISION_REGISTER.md`,
  `docs/WRR_MANUAL_DECISION_RECORD_WORKSHEET.md`,
  `docs/WRR_METHOD_PAIR_UNIVERSE_EVIDENCE_PACKET.md`,
  `docs/WRR_DW_FORMULA_SENSITIVITY.md`, `docs/WRR_CLAIM_READINESS.md`, and
  `docs/WRR_CLAIM_BLOCKER_PACKET.md`,
  `docs/WRR_LOCKED_METHOD_REPORT.md`,
  `docs/WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md`, plus
  `docs/WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md`
- Cities source-row lock status:
  `docs/CITIES_SOURCE_ROW_LOCK_QUEUE.md`,
  `docs/CITIES_SOURCE_ROW_LOCK_WORKSHEET.md`, and
  `docs/CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md`
  plus `docs/CITIES_SOURCE_TRANSCRIPTION_REVIEW_WORKSHEET.md`,
  `docs/CITIES_SOURCE_PAGE_REVIEW_BUNDLE.md`,
  `docs/CITIES_SOURCE_PAGE_CONTACT_SHEET.md`,
  `docs/CITIES_SOURCE_PAGE_OCR_REVIEW_PACKET.md`,
  `docs/CITIES_SOURCE_PAGE_OCR_REVIEW_HTML.md`,
  `docs/CITIES_SOURCE_PAGE_LINE_CROP_PACKET.md`,
  `docs/CITIES_SOURCE_PAGE_LINE_CROP_BAND_MAP.md`,
  `docs/CITIES_SOURCE_PAGE_LINE_CROP_BAND_REVIEW_WORKSHEET.md`,
  `docs/CITIES_SOURCE_PAGE_LINE_CROP_BAND_CONTACT_SHEET.md`,
  `docs/CITIES_SOURCE_PAGE_LINE_CROP_BAND_REVIEW_HTML.md`,
  `docs/CITIES_SOURCE_PAGE_LINE_CROP_CONTACT_SHEET.md`,
  `docs/CITIES_SOURCE_PAGE_LINE_CROP_REVIEW_HTML.md`,
  `docs/CITIES_SOURCE_PAGE_LINE_CROP_TRIAGE.md`,
  `docs/CITIES_SOURCE_PAGE_LINE_CROP_TRIAGE_HTML.md`,
  `docs/CITIES_SOURCE_PAGE_LINE_CROP_PRIORITY_CONTACT_SHEET.md`,
  `docs/CITIES_SOURCE_PAGE_LINE_CROP_PRIORITY_REVIEW_HTML.md`,
  `docs/CITIES_SOURCE_PAGE_LINE_CROP_PRIORITY_REVIEW_WORKSHEET.md`,
  `docs/CITIES_SOURCE_PAGE_LINE_CROP_REVIEW_WORKSHEET.md`,
  `data/study/mappings/cities_source_row_lock_decisions.csv`, and
  `data/study/mappings/cities_source_transcription_decisions.csv`. Cities
  source-row lock handoff: 14 source-row lock candidate pages, 14 populated
  lock rows, 14 pending transcription-review rows, 14 local Hebrew OCR
  sidecars, a local ignored image/OCR HTML review aid, and 203 local line
  crops from the 4 table candidate pages plus a 16-row coordinate band map,
  a 16-row band review worksheet, 16 local band contact sheets, a local ignored
  band HTML review aid, 4 local line-crop contact sheets, a local ignored
  line-crop HTML review aid, a 203-row line-crop triage queue, a local ignored
  priority-order triage HTML aid, 4 local priority contact sheets, a local
  ignored priority contact-sheet HTML aid, a 203-row priority line-crop
  worksheet, and a 203-row line-crop review worksheet; no
  source rows imported, and no
  city-name normalization, ELS searches, compactness runs, or p-levels.
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
- KJVA source-candidate status rollup:
  `docs/KJVA_SOURCE_CANDIDATE_STATUS.md`
- KJVA CrossWire candidate source-status audit:
  `docs/KJVA_CROSSWIRE_CANDIDATE_SOURCE_AUDIT.md`
- KJVA Gutenberg candidate source-status audit:
  `docs/KJVA_GUTENBERG_CANDIDATE_SOURCE_AUDIT.md`
- KJVA Gutenberg book-coverage probe:
  `docs/KJVA_GUTENBERG_BOOK_COVERAGE_PROBE.md`
- KJVA Wikisource candidate source-status audit:
  `docs/KJVA_WIKISOURCE_CANDIDATE_SOURCE_AUDIT.md`
- KJVA Wikisource book-coverage probe:
  `docs/KJVA_WIKISOURCE_BOOK_COVERAGE_PROBE.md`
- KJVA Open-Bibles candidate source-status audit:
  `docs/KJVA_OPEN_BIBLES_CANDIDATE_SOURCE_AUDIT.md`
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
- protocol TOML files pass runner schema and duplicate-name checks;
- corpus config TOML files pass required name/language/source schema checks;
- term CSV files pass schema, language, normalization, constants, and gematria
  checks;
- every `scripts/check_*.py` guard has a matching `tests/test_check_*.py`
  test module;
- every `scripts/check_*.py` guard is wired through Make, preflight, or a
  protocol input;
- final report, draft, outline, highlights, consolidated findings, and
  clean-lock summary support-doc references point at required local docs;
- `protocols/real_report_run.toml` preflight inputs match the preflight
  script's required-path list, so the runnable protocol and script do not drift;
- final report, draft, outline, and highlights keep their source-artifact and
  no-public-claim assembly boundary;
- project findings overview keeps its general-reader summary, caution language,
  and links to the fuller report docs;
- claim-catalog summary table stays aligned with `claims/claim_catalog.csv`;
- Cities claim-catalog row stays `under_specified`, source-review only, and
  aligned with the current Cities source-row lock decision records;
- Cities source-row lock evidence packet checks local recovered PDF and
  page-image artifact paths before any lock row can pass preflight;
- populated Cities source-row lock decision records must name the exact decision
  id in their evidence citation or summary;
- final report highlights markdown matches the deterministic builder output;
- centered occurrence index markdown matches the deterministic builder output;
- strongest candidate deep-dive markdown matches the deterministic builder
  output;
- prospective lane profiles valid, with registered term/protocol/report paths
  present, and the readiness, next-lock, and study-lock workflow docs agree
  with current lane state;
- KJVA apocrypha/deuterocanon prospective bridge output remains locked as a
  negative controlled result: 7 registered terms, 1 `tobit` bridge row, 0 terms
  with BH `q_ge <= 0.05`, and 1 of 3 non-Bible controls at or above the
  observed total;
- KJVA apocrypha/deuterocanon next-replication planning stays planning-only,
  with fresh term/source lock and study-lock sidecar required before any new
  result-bearing output;
- KJVA source-candidate status rollup records 0 ready independent KJVA
  replication sources, 2 possible independent KJVA metadata candidates, 1
  public-domain split KJV+Apocrypha coverage candidate needing collation, 0
  result-ready sources, 0 source-lock ready sources, and identifies the current
  eBible KJVA source as a rerun source with 14 apocrypha/deuterocanon books;
- KJVA CrossWire candidate source audit stays metadata-only, with `kjva.osis.xml`
  and `kjvdc.xml` path names present, config-license/Crown-rights metadata
  captured, but no source-use clearance, corpus import, source lock, or
  result-bearing output;
- KJVA Gutenberg candidate source audit stays metadata-only, with Project
  Gutenberg eBook 30 RDF metadata recording `The Bible, King James Version,
  Complete`, `Public domain in the USA.`, and a plain-text UTF-8 format URL,
  but no Apocrypha/deuterocanon coverage confirmation, corpus import, source
  lock, or result-bearing output;
- KJVA Gutenberg book-coverage probe stays source-coverage only, with all 66
  KJV book headings found in eBook 30, all 14 tracked Apocrypha/deuterocanon
  coverage rows found in eBook 124, one extra Epistle of Jeremiah source
  heading, and no verse map, corpus import, source lock, or result-bearing
  output;
- KJVA Wikisource candidate source audit stays metadata-only, with no Bible
  text retained, no corpus import ready, and no result-bearing output;
- KJVA Wikisource book-coverage probe stays metadata-only, with 36 existing
  KJV book links, 30 KJV redlinks, 0 apocrypha/deuterocanon book links, and no
  source-lock readiness;
- KJVA Open-Bibles candidate source audit stays metadata-only and marks the
  repository as KJV-only for current KJVA/apocrypha bridge purposes;
- consolidated findings keep the current prospective-lane boundary tied to
  live profile state;
- prospective lane-status doc matches its generated output from the live lane
  profile JSON;
- Greek surface second-cohort readiness keeps the existing-pool rerun boundary
  visible;
- English source-basis manifests and audit-queue counts valid, with no current
  `needs_audit` rows unless the policy is explicitly changed;
- English seed survivor gate stays closed: the survivor term file is empty,
  and downstream survivor reports remain idle until a row clears the shuffle
  threshold;
- English corpus policy docs keep missing BibleGateway rows deferred unless a
  lawful local text or source package with clear permission is available;
- expanded-strata operator docs point at live scripts, protocol files, and
  Make targets;
- study-mapping CSV schemas retain exact columns, required locked values, ISO
  `locked_at` dates, supported language markers, tracked term IDs, and row-level
  guard links where direct guards exist;
- concrete preregistration docs contain no unresolved bracketed placeholders
  while the prospective-study template remains available as a template;
- CRD relevance dictionary, term coverage, reviewer metadata, and protocol
  hash lock are still consistent with the centered-relevance protocol;
- manual-review queue keeps required non-claim guardrails, evidence links, and
  live packet-shape counts;
- WRR method-status doc keeps local locks separated from open blockers and
  diagnostic-only rows;
- WRR lock-options doc remains a decision aid rather than a method lock;
- WRR claim-readiness doc records selected local-lock readiness while exact
  published WRR reproduction remains caveated by the residual source/method
  gap;
- WRR claim-blocker packet states no-input limits, keeps no-correction and
  no-exclusion boundaries visible, and summarizes the residual term, row,
  page-image, and method/pair-universe review lanes;
- WRR locked-method report gives the compact reader-facing selected local
  lock result while preserving exact-published-reproduction caveats;
- WRR source-policy checklist keeps the Chełm source-policy/pair-rule target
  as a review lane with required decision-record fields;
- WRR source-transcription row checklist keeps the 22 row clusters in review
  order with required decision-record fields;
- WRR source-row review bundle joins those 22 row clusters to generated crop
  paths, the contact sheet, ignored local row-crop HTML, and OCR word evidence
  as review aids only;
- WRR remaining-lane checklist keeps 3 page-image terms and 11
  method/pair-universe terms in review lanes with required decision-record
  fields;
- hypothesis-testing source audit doc keeps the source-status/no-result
  boundary visible;
- Israeli prime-ministers detail recovery doc keeps the live-source recovery
  boundary, redirected-root status, and no-result-bearing-work limit visible;
- research missing model pages audit doc keeps the missing level-2/3 model page
  boundary visible;
- WRR adjacent source audit and simulation docs keep source-shape and
  simulation-only boundaries visible;
- critical-omission follow-up docs keep Setup, Method, Results, and Cautions
  sections plus current headline counts visible;
- Cities source-row lock decision records stay aligned to the 14-row evidence
  packet before any populated source-row lock can pass preflight;
- Cities source-row lock handoff stays source-review only: 14 source-row lock
  candidate pages, 14 populated lock rows, 14 pending transcription-review
  rows, no source rows imported, and no city-name normalization, ELS searches,
  compactness runs, or p-levels;
- WRR manual decision register consolidates 37 manual-decision inventory rows,
  representing 58 action terms, 59 residual pair links, and 40
  minimum-frontier pair links without selecting corrections or exclusions;
- WRR manual decision-record checker keeps 37 populated lock rows aligned to
  the current register with cited evidence and ISO lock dates;
- WRR manual decision-record worksheet lists the exact rank/lane/target fields
  plus current record status, selected action, and evidence prompt for all 37
  lock rows;
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
  reproduction remains caveated by the source-defined 163-distance gap; current
  manual decision records keep the working source unchanged and lock
  method-lane rows. The explicit readiness gate is tracked in
  `docs/WRR_CLAIM_READINESS.md`; `docs/WRR_LOCKED_METHOD_REPORT.md` is the
  compact locked local method summary; `docs/WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md`
  maps the exact-published 163 vs 72 defined-distance gap and post-lock report
  boundary; `docs/WRR_POST_LOCK_REPORTING_BOUNDARY.md` locks allowed local
  locked-method wording versus forbidden exact-published reproduction wording;
  `docs/WRR_CLAIM_BLOCKER_PACKET.md`
  records that no current claim-readiness blockers remain under the selected
  local lock policy; `docs/WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md` keeps the residual
  source/term/method evidence lanes visible without selecting corrections;
  `docs/WRR_CLAIM_BLOCKER_PACKET.md` mirrors those residual lanes as a compact
  no-input handoff with term targets, source-transcription row clusters,
  page-image near matches, and method/pair-universe counts;
  `docs/WRR_SOURCE_POLICY_EVIDENCE_PACKET.md` ties the Chełm source-policy
  residual to WNP context, row OCR, and scenario status without changing the
  source lock; `docs/WRR_SOURCE_POLICY_REVIEW_CHECKLIST.md` keeps that
  source-policy/pair-rule target as a review lane;
  `docs/WRR_SOURCE_TRANSCRIPTION_EVIDENCE_PACKET.md` groups the
  43 transcription/alignment terms into 22 row clusters for primary row review;
  `docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md` keeps those 22 row
  clusters in review order with required decision-record fields;
  `docs/WRR_SOURCE_ROW_REVIEW_BUNDLE.md` joins the row checklist, generated
  crop paths, contact sheet, ignored local row-crop HTML, and OCR word evidence
  as review aids only;
  `docs/WRR_REMAINING_LANE_EVIDENCE_PACKETS.md` covers the 14 remaining
  page-image and method/pair-universe terms without selecting source edits;
  `docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md` keeps those terms in
  page-image and method/pair-universe review lanes;
  `docs/WRR_MANUAL_DECISION_REGISTER.md` consolidates the 37 manual-decision
  inventory rows, and `data/study/mappings/wrr_manual_decision_records.csv`
  locks them as 26 `no_source_change` rows and 11 `method_lock` rows; and
  `docs/WRR_METHOD_PAIR_UNIVERSE_EVIDENCE_PACKET.md` isolates the 11
  OCR-matched method-lane terms with zero current appellation hits;
  `docs/WRR_METHOD_LANE_WIDE_SKIP_PROBE.md` shows that the same 11 terms still
  have 0 ordinary Genesis hits through skip 5000, so the method lane is not a
  near-cap miss.
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
  all five MT-family sources at conservative all-control q = 0.004799. It is a
  post-discovery review candidate, not a claim.

## Before Claim-Grade Reporting

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
