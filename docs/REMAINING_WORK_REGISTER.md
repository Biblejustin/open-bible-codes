# Remaining Work Register

Status: operational register after the 34-version English-source refresh, the
empty English seed survivor gate, the English source-basis audit, reader-report
hygiene, locked-report reruns, and volatility cleanup. This file tracks work
that remains outside the missing copyrighted/private English CSVs.

## Blocked

### Remaining BibleGateway English Corpora

The current BibleGateway refresh has 34 available English versions and skips
30 missing local CSVs. Missing rows are listed in:

```text
reports/biblegateway_english_versions/missing_versions.csv
```

AMPC, NLT, MSG, TPT, and NIV local hooks exist and their private CSVs are
ignored under `data/private/english/`. TPT is wired in the private protocol but
is not part of the BibleGateway manifest.

## Completed This Pass

### Locked Report Rerun And Volatility Cleanup

Completed locked reruns:

```bash
python3 -m scripts.run_protocol protocols/doxa_four_source_claim_followup.toml --resume
python3 -m scripts.run_protocol protocols/doxa_four_source_confirmatory_followup.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_compound_extension_confirmatory.toml --resume
python3 -m scripts.run_protocol protocols/kjv_apocrypha_bridge_confirmatory_controls_5000.toml --resume
python3 -m scripts.run_protocol protocols/gog_magog_pair_prospective.toml --resume
python3 -m scripts.run_protocol protocols/wrr_audit_counts.toml --resume
```

Guardrails added:

- Doxa four-source report builder now requires explicit
  `--preregistration-commit`, so locked reports do not drift with current
  `HEAD`.
- README Doxa rerun snippets include pinned preregistration commits.
- Gog/Magog prospective tracked report now records generated time in local
  manifests only, not tracked Markdown.
- Stale completed-follow-up sections in extension, pair-baseline, and public
  baseline docs now point to current follow-up reports instead of old rerun
  instructions.

Current pushed commits for this cleanup:

- `5850141` Require locked doxa prereg commits.
- `201a341` Refresh generated indexes.
- `4aac5c1` Stabilize Gog Magog prospective report.
- `bf48336` Update follow-up status docs.
- `d0ff0fb` Add WRR corrected-distance aggregate diagnostic.
- `c421b5d` Add WRR claim readiness gate.
- `fc07423` Link WRR readiness gate in reports.
- `59cce62` Gate WRR claim catalog on readiness.
- `cb24ceb` Require WRR readiness in report preflight.

### Formal Real Report Rerun

Command completed successfully after the worktree was cleaned:

```bash
python3 -m scripts.run_protocol protocols/real_report_run.toml --resume
```

Current summary:

- `reports/real_report_run/summary.md`
- generated UTC: `2026-05-19T19:20:50.699053+00:00`
- report commit recorded by the protocol: `b637bd5`

### Reader Report Refresh

Current tracked files:

- `docs/FINAL_REPORT.md`
- `docs/CONSOLIDATED_FINDINGS.md`
- `docs/FINAL_REPORT_OUTLINE.md`

Completed in this pass: refreshed stale centered-occurrence counts to the
current `docs/CENTERED_OCCURRENCE_INDEX.md` snapshot:

- 812 presence rows.
- 809 Bible presence rows.
- 3 control presence rows.
- 923 raw occurrence rows.
- 526 centered-self exact-word presence rows.

Also replaced stronger conclusion-language wording in these reader-facing docs.

### Claim-Language Hygiene

Goal: keep every public-facing file aligned with current status:

- occurrence finding
- review candidate
- post-screen confirmatory review candidate
- controlled review candidate
- under-specified
- not claim

Hygiene command:

```bash
rg -n "\\bprov[e]d\\b|\\bpro[o]f\\b|statistically[ -]impossible|prophecy[ -]confirmed|validation of inspirat[i]on|claim[- ]level" docs README.md claims protocols scripts tests
```

Expected result: no public-facing reader-doc hits except historical filenames or
implementation/test identifiers that explicitly encode legacy claim-follow-up
workflow names.

## Highest-Value Non-Blocked Work

### 1. WRR Reproduction Upgrade

Current status: smoke/source/import work plus a lock-prep pair eligibility
table. Remaining claim-grade pieces:

- candidate pair source/reconciliation, with `163` treated as the
  source-defined corrected-distance output count rather than a raw pair table;
- printed-formula vs WRR-program `D(w)` choice, now side-by-side audited but
  not locked;
- real-pair perturbed `Q` and corrected distance `c(w,w')`, enforcing
  source-backed undefined conditions;
- term-specific skip-cap logic;
- permutation-rank procedure;
- study-level report over fixed terms and sources.

Tracked references:

- `docs/WRR_REPLICATION_PLAN.md`
- `docs/WRR_METHODOLOGY_GAPS.md`
- `docs/WRR_CORRECTED_DISTANCE_NOTES.md`
- `docs/WRR_CLAIM_READINESS.md`
- `reports/wrr_1994/wrr2_pair_eligibility_table.csv`
- `tests/test_wrr_stats.py`

Recent source-audit follow-up added a Torah-code.org geometric level-1
simulation harness and an ELS/cylinder level-1 analogue:

- `scripts/simulate_torah_code_research_model.py`
- `scripts/simulate_torah_code_research_els_model.py`
- `protocols/torah_code_research_geometric_model.toml`
- `docs/TORAH_CODE_RESEARCH_MODEL_SIMULATION.md`
- `docs/TORAH_CODE_RESEARCH_ELS_MODEL_SIMULATION.md`

The research-program ELS harness now includes a split-fit Fisher
order-statistic row. Next research-program upgrade: replace the current
transparent resonant row-width proxy with a fuller source-method reconstruction,
recover source-published Fisher weights if a citable source becomes available,
and only then consider real Torah-code source data.

WRR aggregate work now has a diagnostic P1..P4 bridge:

- `scripts/analyze_wrr_corrected_distance_aggregate.py`
- `reports/wrr_1994/wrr2_corrected_distance_aggregate.csv`
- `scripts/check_wrr_claim_readiness.py`
- `docs/WRR_CLAIM_READINESS.md`

Current read: the length-5..8 direct-search corrected-distance smoke output has
28 defined `c(w,w')` values at cap 250 and 46 defined values in the cap-1000
split diagnostic, so P1..P4 diagnostic rows now populate. The readiness gate
still stays blocked until pair universe, `D(w)`, full corrected distance, and
permutation/aggregate statuses are locked. This is not yet the claim-grade
P1..P4/permutation driver.

All-lane diagnostic follow-up now exists:
`protocols/wrr_corrected_distance_direct_all_lanes.toml` and
`docs/WRR_DIRECT_ALL_LANES_DIAGNOSTIC.md`. It defines 50 values at cap 250 and
72 at cap 1000 over all 182 imported same-record pairs, still far below the
source-cited 163 defined second-list distances.

### 2. Source-Basis Audit Queue

The English manifests already track broad source-basis metadata:

- `ot_basis`
- `nt_basis`
- `source_family`
- `basis_status`

Rows with `basis_status=needs_audit` should stay coarse until publisher
introductions or official source notes are checked. Do not upgrade them to
edition-level textual-critical claims from memory.

Current queue after the BibleGateway/eBible audit pass:

- BibleGateway English versions: 0 `needs_audit`, 64 `broad_tradition`.
- eBible English controls: 0 `needs_audit`, 37 `broad_tradition`.
- eBible rows moved to broad grouping: `ASVBT`, `BSB`, `MSB`, `OEBCW`, `OEB`,
  `BBE`, `NOY`, `PEV`, and `OJB`.
- BibleGateway rows moved to broad grouping in the second audit pass include
  `AMP`, `AMPC`, `CJB`, `CEV`, `DLNT`, `ERV`, `EASY`, `EXB`, `GW`, `ICB`,
  `ISV`, `JUB`, `PHILLIPS`, `MSG`, `MOUNCE`, `NOG`, `NCB`, `NCV`, `NLV`,
  `NTFE`, `VOICE`, and `WE`.
- `PEV` license metadata corrected to CC BY-SA 4.0; local source package says
  the translation used Hebrew and Greek language study aids but not exact
  editions.
- `BBE` and `NOY` moved to broad grouping only. `BBE` has broad Hebrew/Greek
  source evidence; `NOY` NT title metadata identifies Tischendorf's Greek text.
- No English source-basis rows remain in `needs_audit`.

Suggested local queue command:

```bash
awk -F, 'NR == 1 || /needs_audit/' configs/biblegateway_english_versions.csv configs/ebible_english_controls.csv
```

### 3. English Seed Survivor Gate

Current status: no English seed rows survive the 100-sample corpus-letter
shuffle gate after the 34-version BibleGateway refresh.

Current gate files:

- `reports/english_seed_shuffle_followup_100/summary.csv`
- `terms/english_seed_followup_survivors.csv`
- `docs/ENGLISH_SEED_SHUFFLE_FOLLOWUP_REPORT.md`

Leave these downstream survivor protocols idle unless
`terms/english_seed_followup_survivors.csv` has data rows:

```bash
python3 -m scripts.run_protocol protocols/english_seed_term_shuffle_1000.toml --resume
python3 -m scripts.run_protocol protocols/english_seed_survivor_audit.toml --resume
python3 -m scripts.run_protocol protocols/english_seed_paired_controls_1000.toml --resume
```

### 4. Apocrypha/Deuterocanon Prospective Study

KJVA bridge results are strong post-screen review material, not claims.
Remaining next step is a fresh prospective lock before producing new
result-bearing outputs.

Candidate inputs:

- `docs/KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_PREREGISTRATION.md`
- `docs/KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_CONTROLS_5000.md`
- `terms/kjv_apocrypha_bridge_confirmatory_terms.csv`

Needed before claim language:

- fixed prospective term list;
- fixed insertion/control design;
- fixed skip range;
- fixed correction rule;
- non-Bible insertion controls.

### 5. Manual Review Queue

Carry these with controls attached:

- Greek `δοξα` / `δοξανωσ` four-source row.
- Hebrew `יום יהוה` / `היומיהוה` compound extension.
- Greek `γωγ` at Rev 20:8.
- LXX `ιησουσ` rows with Joshua/Jesus referent discipline.
- Hebrew `ישוע` and `משיח` centered rows with background-pressure cautions.

Navigation aid:

- `docs/MANUAL_REVIEW_QUEUE.md`
- `docs/PROSPECTIVE_LANE_STATUS.md`

## Validation Commands

Current fast validation:

```bash
python3 -m pytest -q
git diff --check
python3 -m scripts.build_docs_index --docs-dir docs --out docs/INDEX.md
python3 -m scripts.build_protocol_index --protocols-dir protocols --out protocols/INDEX.md
python3 -m scripts.check_public_release_hygiene --allow-dirty
```

Current observed result after the WRR readiness gate and preflight guard pass:

- `python3 -m pytest -q` passed: 1025 tests and 5730 subtests.
- `python3 -m pytest tests/test_import_bolls_translation.py tests/test_english_version_manifests.py -q` passed: 11 tests and 117 subtests.
- `python3 -m pytest tests/test_doxa_four_source_report.py tests/test_gog_magog_pair_prospective_report.py tests/test_wrr_method_status.py -q` passed: 13 tests.
- `python3 -m pytest tests/test_real_report_run.py tests/test_claim_catalog.py tests/test_wrr_claim_readiness.py -q` passed: 32 tests and 60 subtests.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_check.json` passed.
- `git diff --check` passed.
- `python3 -m scripts.check_public_release_hygiene --allow-dirty` passed.
