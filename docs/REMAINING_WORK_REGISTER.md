# Remaining Work Register

Status: operational register after the 34-version English-source refresh and
the empty English seed survivor gate. This file tracks work that remains
outside the missing copyrighted/private English CSVs.

## Blocked

### Formal Real Report Rerun

Command:

```bash
python3 -m scripts.run_protocol protocols/real_report_run.toml --resume
```

Current blocker: preflight requires a clean git worktree. The attempted rerun
stopped at preflight with `git working tree is not clean`.

Next action: decide commit/stage boundary for the current large worktree, then
rerun the formal report protocol.

### Remaining BibleGateway English Corpora

The current BibleGateway refresh has 34 available English versions and skips
30 missing local CSVs. Missing rows are listed in:

```text
reports/biblegateway_english_versions/missing_versions.csv
```

AMPC, NLT, MSG, TPT, and NIV local hooks exist and their private CSVs are
ignored under `data/private/english/`. TPT is wired in the private protocol but
is not part of the BibleGateway manifest.

## Highest-Value Non-Blocked Work

### 1. Reader Report Refresh

Current tracked file: `docs/FINAL_REPORT.md`.

Completed in this pass: refreshed stale centered-occurrence counts to the
current `docs/CENTERED_OCCURRENCE_INDEX.md` snapshot:

- 812 presence rows.
- 809 Bible presence rows.
- 3 control presence rows.
- 923 raw occurrence rows.
- 526 centered-self exact-word presence rows.

Remaining action after clean worktree: rerun `protocols/real_report_run.toml`
and recheck `docs/FINAL_REPORT.md`, `docs/CONSOLIDATED_FINDINGS.md`, and
`docs/FINAL_REPORT_OUTLINE.md` against `reports/real_report_run/summary.md`.

### 2. Claim-Language Hygiene

Goal: keep every public-facing file aligned with current status:

- occurrence finding
- review candidate
- post-screen confirmatory review candidate
- controlled review candidate
- under-specified
- not claim

Disallowed language unless a later locked prospective study earns it:

- proof
- statistically impossible
- prophecy confirmed
- validation of inspiration
- claim-level

Suggested command:

```bash
rg -n "proved|proof|statistically impossible|prophecy confirmed|validation of inspiration|claim-level|claim level" docs README.md claims protocols scripts tests
```

### 3. Source-Basis Audit Queue

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

### 4. English Seed Survivor Gate

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

### 5. WRR Reproduction Upgrade

Current status: smoke/source/import work only. Remaining claim-grade pieces:

- locked pair eligibility table;
- corrected distance `c(w,w')`;
- term-specific skip-cap logic;
- permutation-rank procedure;
- study-level report over fixed terms and sources.

Tracked references:

- `docs/WRR_REPLICATION_PLAN.md`
- `docs/WRR_METHODOLOGY_GAPS.md`
- `docs/WRR_CORRECTED_DISTANCE_NOTES.md`
- `tests/test_wrr_stats.py`

### 6. Apocrypha/Deuterocanon Prospective Study

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

### 7. Manual Review Queue

Carry these with controls attached:

- Greek `δοξα` / `δοξανωσ` four-source row.
- Hebrew `יום יהוה` / `היומיהוה` compound extension.
- Greek `γωγ` at Rev 20:8.
- LXX `ιησουσ` rows with Joshua/Jesus referent discipline.
- Hebrew `ישוע` and `משיח` centered rows with background-pressure cautions.

## Validation Commands

Current fast validation:

```bash
python3 -m unittest discover -v
git diff --check
python3 -m scripts.build_docs_index --docs-dir docs --out docs/INDEX.md
python3 -m scripts.build_protocol_index --protocols-dir protocols --out protocols/INDEX.md
python3 -m scripts.check_public_release_hygiene --allow-dirty
```

Current observed result after the English-source refresh:

- `python3 -m unittest discover -v` passed: 586 tests.
- `python3 -m pytest tests/test_import_bolls_translation.py tests/test_english_version_manifests.py -q` passed: 11 tests and 117 subtests.
- `git diff --check` passed.
- `python3 -m scripts.check_public_release_hygiene --allow-dirty` passed.
