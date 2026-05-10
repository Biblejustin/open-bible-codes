# Version Distribution Index

Status: navigation index for current version-distribution reports.

Formal report assembly plan: `docs/REAL_REPORT_RUN.md`.

This project now tracks two related but different questions:

- exact ref-key version presence inside aligned source families;
- broad corpus presence across non-aligned corpora.

Use exact ref-key reports when sources share a reference coordinate system, such
as Hebrew MT-family editions or Greek NT editions. Use broad corpus reports when
the sources do not align verse-for-verse, such as LXX vs Greek NT.

## Hebrew MT-Family Exact-Hit Reports

Compared sources:

- `MT_WLC`
- `UXLC`
- `EBIBLE_WLC`
- `MAM`
- `UHB`

| Report | Term Scope | Runtime | Terms | Exact Patterns | All-Source Patterns | Source-Specific Patterns |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `docs/HEBREW_HIT_VERSION_PRESENCE.md` | focused modern/local Hebrew rows | 21.953s | 22 | 1,202 | 749 | 244 |
| `docs/HEBREW_MODERN_GEOPOLITICAL_VERSION_PRESENCE.md` | all Hebrew rows from modern names/dates/geopolitical/local list | 30.608s | 82 declared; 73 summarized | 7,567 | 4,612 | 1,577 |
| `docs/HEBREW_CLAIM_VERSION_PRESENCE.md` | compiled Hebrew claim rows | 23.037s | 143 declared; 125 summarized | 5,603 | 3,635 | 956 |
| `docs/HEBREW_CONTROL_VERSION_PRESENCE.md` | null/frequency controls | 22.086s | 23 declared; 13 summarized | 981 | 526 | 170 |
| `docs/HEBREW_SCREENING_VERSION_PRESENCE.md` | broader Hebrew screening rows | 23.257s | 557 selected; 417 summarized | 15,099 | 9,432 | 2,600 |

Interpretive comparison:

- `docs/HEBREW_VERSION_PRESENCE_COMPARISON.md`
- `docs/HEBREW_VERSION_SPECIFIC_DISTRIBUTION.md`

Current read:

- Hebrew exact-hit patterns are often stable across the MT-family sources.
- The all-row modern/geopolitical run keeps the same shape: short forms often
  survive across all five MT-family sources, while longer phrases are frequently
  absent.
- Its representative paired-control follow-up controlled 54 nonzero terms
  across MT_WLC/UHB: 50 read as not unusual, 4 were uncorrected-only prompts,
  and 0 had adjusted representative-control support.
- The broader Hebrew screening run also keeps the same shape: many short forms
  are stable, while most source-specific rows are still `MAM` or `UHB`.
- Its representative paired-control follow-up controlled 306 broader-screening
  terms across MT_WLC/UHB: 295 read as not unusual, 11 were uncorrected-only
  prompts, and 0 had adjusted representative-control support.
- Stability is therefore a reproducibility filter, not significance evidence.

Optional STEP/Tyndale selected-stream follow-up:

- `docs/STEP_TAHOT_SOURCE_AUDIT.md`
- `docs/STEP_TAHOT_VERSION_PRESENCE_REVIEW.md`
- `docs/STEP_TAHOT_SCREENING_VERSION_PRESENCE.md`
- `docs/STEP_TAHOT_POLICY_HIT_AUDIT.md`
- `docs/STEP_TAHOT_CONTROL_VERSION_PRESENCE.md`
- `docs/STEP_TAHOT_FINAL_GATE.md`

`STEP_TAHOT` is intentionally outside the Leningrad-family label because its
selected text may follow qere, restore missing text, and include LXX-preserved
additions converted to Hebrew. In the focused modern/local exact-hit pass, it
participated in 961 of 1,236 pattern rows, while 34 rows were `STEP_TAHOT`-only.
In the broader Hebrew screening pass, it participated in 12,084 of 15,478
pattern rows, while 379 rows were `STEP_TAHOT`-only. Use those rows for
source-family survival review, not as all-Leningrad evidence. The first
source-policy audit found that 80 of those 379 `STEP_TAHOT`-only rows touch
`Q`, `R`, or `X` words on the hidden-letter path. A matching null/frequency
control pass found 1,005 exact control patterns, with 749 including
`STEP_TAHOT` and 24 `STEP_TAHOT`-only. Of those 24 control-only rows, 3 touch
`Q` words and 21 are L-only paths. The final gate compares source-only rates:
real screening rows were `STEP_TAHOT`-only at 2.449%, while null/frequency
controls were `STEP_TAHOT`-only at 2.388%.

## Greek NT Exact-Hit Reports

Compared sources:

- `TR_NT`
- `BYZ_NT`
- `TCG_NT`
- `SBLGNT`

| Report | Term Scope | Runtime | Terms | Exact Patterns | All-Source Patterns | Source-Specific Patterns |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `docs/GREEK_NT_CLAIM_VERSION_PRESENCE.md` | Greek NT claim rows | 12.495s | 32 | 787 | 109 | 428 |
| `docs/GREEK_CONTROL_VERSION_PRESENCE.md` | Greek controls | 12.366s | 20 declared; 19 summarized | 826 | 270 | 319 |
| `docs/GREEK_SCREENING_VERSION_PRESENCE.md` | broader Greek screening rows | 13.238s | 413 selected; 398 summarized | 11,103 | 2,192 | 5,495 |

Interpretive comparison:

- `docs/GREEK_VERSION_PRESENCE_COMPARISON.md`

Current read:

- Greek NT exact-hit patterns are more version-sensitive than Hebrew MT-family
  patterns in the current screens.
- Control rows had a higher all-source rate than claim rows.
- Broader Greek screening rows confirm that short forms create many exact
  all-source patterns, while source-specific rows remain common.
- Source-specific Greek rows are review queues, not claims.
- Hidden-path-only rows are normal ELS candidate types, not failures. A
  same-span surface echo is a rarer stronger subtype.
- Greek exact-center final gate: `docs/GREEK_EXACT_CENTER_FINAL_GATE.md`.
- Strongest current Greek row: `δοξα` (doxa; English: glory) four-source confirmatory follow-up in
  `docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md`; status remains
  review candidate, not claim.
- Expanded prospective exact-center screen:
  `docs/GREEK_EXPANDED_PROSPECTIVE_REPORT.md`; zero exact-center
  phrase-extension patterns after locked filters.
- Post-screen expanded Greek surface queue:
  `docs/GREEK_EXPANDED_SURFACE_QUEUE.md`; 161 exact-center surface patterns
  without phrase-extension controls, including 27 all-source rows. This is a
  review queue, not a claim set.
- Tighter expanded Greek surface triage:
  `docs/GREEK_EXPANDED_SURFACE_TRIAGE.md`; all-source plus normalized length
  >= 5 leaves `ανομια` (anomia; English: lawlessness), `ισαακ` (Isaak; English: Isaac), and `τερασ` (teras; English: wonder) as review rows needing real-word,
  surface-frequency-matched controls.
- Expanded Greek surface letter-path audit:
  `docs/GREEK_EXPANDED_SURFACE_LETTER_PATHS.md`; reconstructs each selected
  ELS path across TR_NT, BYZ_NT, TCG_NT, and SBLGNT for manual audit.
- Expanded Greek surface control pool:
  `docs/GREEK_EXPANDED_SURFACE_CONTROL_POOL.md`; 291 terms measured for
  normalized surface-substring frequency, 165 all-source surface-present terms,
  and 10 same-length matched control candidates per selected target.
- Expanded Greek surface control evaluation:
  `docs/GREEK_EXPANDED_SURFACE_CONTROL_EVALUATION.md`; selected rows beat their
  10 matched controls on all-source surface-pattern count, but q = 0.090909
  because the control pool is small.
- Expanded Greek all-available surface control evaluation:
  `docs/GREEK_EXPANDED_SURFACE_AVAILABLE_CONTROL_EVALUATION.md`; selected
  targets are excluded from the controls, and `ισαακ` (Isaak; English: Isaac), `τερασ` (teras; English: wonder), and `ανομια` (anomia; English: lawlessness)
  all exceed their available same-length controls with q = 0.032258.
- Expanded Greek surface compact follow-up:
  `docs/GREEK_EXPANDED_SURFACE_FOLLOWUP_REPORT.md`; joins the selected rows,
  reconstructed letter paths, and all-available controls into one
  post-screen review sheet.

## Greek LXX / NT Corpus Presence

Compared corpora:

- `LXX`
- `TR_NT`
- `BYZ_NT`
- `TCG_NT`
- `SBLGNT`

Report:

- `docs/GREEK_LXX_NT_CORPUS_PRESENCE.md`

Current broad-presence result for Greek NT claim rows:

| Scope | Terms |
| --- | ---: |
| Present in all observed corpora | 14 |
| Present in multiple observed corpora | 4 |
| Source-specific | 2 |
| Absent in all observed corpora | 12 |

Current read:

- LXX often has higher raw counts because it is larger than NT corpora.
- LXX/NT rows are corpus-presence rows, not Greek NT version-support rows.
- Use Greek NT exact-hit reports for version-support questions.

## Targeted Modern / Geopolitical / Local Join

Focused report:

- `docs/TARGETED_VERSION_PRESENCE_REVIEW.md`
- `docs/HEBREW_MODERN_GEOPOLITICAL_CONTROLLED_REVIEW.md`
- `docs/HEBREW_MODERN_GEOPOLITICAL_CONTROLLED_FINDINGS.md`
- `docs/HEBREW_SCREENING_CONTROLLED_REVIEW.md`
- `docs/HEBREW_SCREENING_CONTROLLED_FINDINGS.md`

Generated controlled table:

- `reports/targeted_version_presence_controlled_summary.csv`

Current focused result:

| Scope | Rows |
| --- | ---: |
| Target rows | 59 |
| Rows with all-source exact patterns | 25 |
| Rows absent or unsummarized | 31 |
| Rows with representative controls joined | 28 |
| Strong plus-term extension top rows | 0 |

Current read:

- Some short modern/geopolitical forms are stable where present.
- Representative paired controls do not support a claim for those stable rows.
- The broad Hebrew modern/geopolitical controlled review found no adjusted
  representative-control support across the nonzero rows it controlled.
- The broader Hebrew screening controlled review also found no adjusted
  representative-control support across the nonzero rows it controlled.
- Longer phrase and local rows such as United States, United Nations, European
  Union, Cowboy Catering, Simsberry, and Simscorner remain absent in the capped
  exact-version screen. The broader Hebrew modern/geopolitical run confirms the
  same absence pattern while adding more date, place, leader, and local rows.

## Relaxed All-Codes Follow-Up

Reports:

- `docs/ALL_CODES_FOLLOWUP_SELECTION.md`
- `docs/ALL_CODES_FOLLOWUP_LETTER_PATHS.md`
- `docs/ALL_CODES_FOLLOWUP_CONTEXT.md`
- `docs/ALL_CODES_FOLLOWUP_EXTENSIONS.md`
- `docs/ALL_CODES_COMPOUND_EXTENSION_CONTROLS.md`
- `docs/ALL_CODES_FOLLOWUP_REVIEW.md`

Current result:

| Scope | Rows |
| --- | ---: |
| Selected follow-up rows | 59 |
| Reconstructed path rows | 274 |
| Hidden-letter rows | 1,264 |
| Sequence mismatches | 0 |
| Selected rows with same-skip extensions | 52 |
| Selected rows with compound same-skip extensions | 8 |
| Deduped compound-extension control targets | 43 |
| Term/random controls per target | 250 / 250 |
| Compound-control q <= 0.05 rows | 14 |
| Compound-control q <= 0.10 rows | 7 |
| Compound-control not-unusual rows | 22 |
| Conservative all-control q <= 0.05 rows | 0 |
| Conservative all-control q <= 0.10 rows | 2 |

Current read:

- Hidden-path-only rows are retained as valid review candidates.
- Same-center-word and related-context rows are ranked higher for manual
  review, but open surface echo is not required.
- Same-skip extensions are now split into adjacent-only rows and compound rows
  that contain the hidden term plus before/after letters.
- Row-local compound-extension controls are now available. They reduce the
  initial all-floor signal after score-scale alignment: 14 rows remain at
  min-q <= 0.05, 7 more at min-q <= 0.10, and 22 read not unusual. The
  conservative all-control companion has no q <= 0.05 rows and only 2
  q <= 0.10 rows.

## Method Boundary

Main methodology note:

- `docs/VERSION_DISTRIBUTION_METHOD.md`
- `docs/GREEK_SURFACE_PROSPECTIVE_CLAIM_STANDARD.md`
- `docs/STUDY_LOCK_MANIFESTS.md`
- `docs/PROSPECTIVE_STUDY_PREREGISTRATION_TEMPLATE.md`
- `docs/VERSION_PRESENCE_HIT_EXPORT.md`
- `docs/VERSION_PRESENCE_EXTENSION_SCREEN.md`
- `docs/TARGETED_VERSION_PRESENCE_REVIEW.md`

Version distribution can move a row into a review queue. It does not establish
meaning, prophecy, theology, or statistical significance by itself. Claims need
predeclared terms, exact source-distribution tables, row-local controls, context
review, and letter-path audit.
