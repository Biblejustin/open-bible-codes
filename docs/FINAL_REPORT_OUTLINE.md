# Final Report Outline

Status: writing scaffold for the current completed report set. This is not a
new analysis run.

## Purpose

Use this outline to turn the current generated reports into a reader-facing
final report. The report should preserve two facts at the same time:

- hidden paths, centered occurrences, and relevant surface contexts should be
  listed when they exist;
- statistical strength, matched controls, source sensitivity, and post-screen
  status should travel with every listed row.

No current row should be labeled as a public claim.

## Source Artifacts

Primary summary artifacts:

- `reports/real_report_run/summary.md`
- `docs/CONSOLIDATED_FINDINGS.md`
- `docs/CENTERED_OCCURRENCE_INDEX.md`
- `docs/CLAIM_CATALOG.md`
- `reports/INDEX.md`

Methodology artifacts:

- `docs/HYPOTHESIS_ANALYSIS_FRAMEWORK.md`
- `docs/REAL_REPORT_RUN.md`
- `docs/PROSPECTIVE_STUDY_READINESS.md`
- `docs/GREEK_SURFACE_PROSPECTIVE_CLAIM_STANDARD.md`
- `docs/STUDY_LOCK_MANIFESTS.md`
- `docs/SOURCES_AND_LICENSES.md`

Post-baseline follow-on artifact:

- `docs/APOCRYPHA_BRIDGE_STUDY.md`

## Recommended Report Shape

### 1. Executive Summary

State plainly:

- the toolkit can search Hebrew, Greek, and English corpora with signed skips;
- the current run includes Bible and non-Bible controls;
- many hidden paths exist;
- centered-self and relevant-center occurrences exist and are worth listing;
- matched controls explain many high-count rows;
- no current result should be called a public claim.

### 2. Hypothesis And Scope

Frame the working hypothesis as a testable research hypothesis:

- original-language biblical texts are the primary target;
- English translations are secondary screens;
- patterns may be source-specific rather than expected in every version;
- non-Bible controls are required comparison background.

Do not imply that absence in one textual source automatically falsifies the
whole hypothesis. The source-presence question is: which patterns appear in
which witnesses?

### 3. Methods

Summarize:

- text normalization by language;
- continuous letter streams;
- forward and backward signed skips;
- full-span dynamic skip caps;
- centered-word and surface-context extraction;
- same-skip before/after extensions;
- source/version comparison;
- matched controls, non-Bible controls, shuffled controls, and q-values;
- preregistration and post-screen labels.

### 4. Main Findings

Use the categories already present in `reports/real_report_run/summary.md`:

- STEP_TAHOT Hebrew source-family final gate;
- Greek exact-center source/version gates;
- four-source `δοξα` (doxa; English: glory) follow-ups;
- Greek surface prospective and post-discovery rows;
- Hebrew modern/geopolitical controlled and prospective source-distribution
  rows;
- broader Hebrew screening controls;
- all-codes follow-up and compound-extension controls;
- centered occurrence index;
- WRR source/import/count smoke audit.

### 5. Occurrence-First Findings

Use `docs/CENTERED_OCCURRENCE_INDEX.md` as the source of truth.

Current snapshot:

- 812 unique term-center presence rows.
- 809 Bible presence rows.
- 3 control presence rows.
- 923 raw occurrence rows before presence grouping.
- 839 Bible occurrence rows.
- 84 control occurrence rows.
- 526 `centered_self_exact_word` presence rows.

Report `Gog` at Rev 20:8 carefully:

- Greek `γωγ` (Gog; English: Gog) is centered on open `Gog` at Rev 20:8 across BYZ_NT, SBLGNT,
  TCG_NT, and TR_NT.
- This is a real source-stable centered-self occurrence in a direct
  Gog/Magog verse.
- It is not frequency-promoted because all 24 matched length-3 non-target
  controls had more exact-center paths than `γωγ` (Gog; English: Gog).

### 6. Strongest Review Candidates

Treat these as review candidates, not claims:

- `δοξα` (doxa; English: glory) / `δοξανωσ` (doxanos; English: hidden extension form from doxa): strongest Greek cross-version controlled
  surface-anchored hidden candidate.
- `יום יהוה` (yom YHWH; English: day of YHWH) / `היומיהוה` (hayom YHWH; English: the day of YHWH): strongest locked post-discovery
  compound-extension review candidate.
- Greek `γωγ` (Gog; English: Gog) at Rev 20:8: strongest occurrence-first centered-self row by
  contextual relevance, with short-form frequency caution.
- LXX `ιησουσ` (Iesous; English: Jesus/Joshua) rows: real centered-self rows, but referent discipline is
  required because the surface referent is Joshua/Jesus depending on context.
- Hebrew `ישוע` (Yeshua; English: Yeshua/Jeshua) and `משיח` (Mashiach; English: Messiah/anointed one) rows: list occurrences, but carry control-background
  warnings because language-matched controls also produce centered rows.

### 7. Negative And Weak Results

State these visibly:

- modern/geopolitical/local terms mostly do not survive representative controls;
- full phrases such as United States, United Nations, European Union, Cowboy
  Catering, Catering, and Simscorner are absent or effectively absent in the
  observed Hebrew/Greek screens;
- short abbreviations and short forms are dense and should not be over-read;
- widening skip ranges increases raw counts predictably;
- non-Bible controls often match or exceed Bible raw-rate backgrounds.

### 8. WRR Status

Use cautious language:

- current WRR work is source/import/count smoke work;
- corrected distance and full permutation statistic are not implemented as a
  claim-grade reproduction;
- WRR remains under-specified in this project until the locked pair table,
  corrected-distance metric, and permutation procedure are complete.

### 9. Claim-Language Boundary

Use these labels consistently:

- `detected`
- `hidden_path_candidate`
- `surface_anchored_hidden_candidate`
- `surface_echo_candidate`
- `cross_version_controlled_candidate`
- `review_candidate_not_claim`

Avoid stronger theological or statistical conclusion language unless a later
locked prospective study earns that status under predeclared controls.

### 10. Future Work

Keep future work separate from the current report:

- finish any remaining locked reports before expanding source sets;
- then run the apocrypha/deuterocanon comparison as a new source-family study;
- include bridge-completion checks where partial canonical ELS paths become
  complete only after declared apocrypha/deuterocanon insertions;
- run comparable non-Bible insertion controls before interpreting bridge rows.

## Report Rule

Every highlighted row should include:

- searched term;
- normalized term;
- corpus/source;
- direction and skip;
- start, center, and end references;
- center word and context excerpt;
- whether it is hidden-only, centered-self, related-center, center-verse
  relevant, span-relevant, or compound-extension;
- source/version presence;
- control read;
- final status label.
