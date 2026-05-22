# Remaining Work Register

Status: operational register after the 34-version English-source refresh, the
empty English seed survivor gate, the English source-basis audit, reader-report
hygiene, locked-report reruns, volatility cleanup, WRR single-term
source-policy propagation, Torah-code research-model source-status cleanup,
Greek follow-up status refreshes, and Hebrew MT/STEP_TAHOT source-status
cleanup, prospective-lane validator tightening, source-audit preflight guard
coverage, prospective-lane validation in report preflight, source-basis audit
queue guarding, English source-basis preflight inputs, formal source-basis
queue validation, source-basis validation documentation, and formal preflight
metadata-check documentation, study-tooling preflight coverage, and
preregistration placeholder guarding, CRD relevance-lock guarding,
manual-review queue preflight guarding, WRR readiness-doc guarding, WRR
blocker-packet preflight guarding, WRR lock-options preflight guarding, and
WRR method-status preflight guarding, WRR source-recovery probing, WRR
source-recovery probe guarding, `.shtml` research-source alternate probing,
and hypothesis-testing source-status auditing/guarding, plus WRR
defined-distance diagnostic doc guarding, WRR variant-gap doc guarding, and
WRR variant-gap method-status evidence propagation, WRR source-review queue doc
guarding, WRR D(w) formula sensitivity doc guarding, and WRR source-policy
scenario doc guarding, WRR cross-pair grid doc guarding, and WRR direct
all-lane diagnostic doc guarding, and WRR source visual-review notes doc
guarding.
This file tracks work that remains outside the missing copyrighted/private
English CSVs.

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

Bolls currently adds no further missing BibleGateway labels beyond sources
already mapped separately. The Bolls `NASB` package remains tracked as
`NASB1995`; do not silently use it for the current BibleGateway `NASB` row. The
local NASB EPUB is PDF-derived/two-column and is not safe for verse-level CSV
import without a dedicated parser.

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
- `4b792d4` Surface WRR diagnostic in real report run.
- `d23b87d` Refresh WRR status after cross-pair diagnostics.
- `ac86fb5` Refresh all-codes reports with Hebrew theology DB.
- `883458d` Add WRR readiness evidence context.
- `4abb554` Add WRR single-term evidence to final reports.
- `d97f505` Propagate WRR single-term impacts to support docs.
- `097a5e0` Record adjacent Torah-code model sources.
- `1892dad` Refresh remaining work register.
- `920afcf` Update WRR claim catalog status.
- `5472de0` Refresh Greek prospective follow-up status.
- `9372126` Guard Greek prospective report follow-up text.
- `16ce0b7` Refresh Greek follow-up report statuses.
- `09ee224` Fix prospective preregistration checker command.
- `45c4ff6` Refresh SBLGNT source-only follow-up status.
- `7e4f9d6` Refresh Hebrew MT source candidate status.
- `abb499b` Clarify KJVA bridge lock basis.
- `f49521a` Tighten prospective lane validation.
- `1198262` Guard source audit docs in report preflight.
- `2250b7a` Run prospective lane validation in report preflight.
- `980cfb6` Guard completed source basis audit queue.
- `946e76d` Guard English source basis inputs in preflight.
- `dd777bc` Validate source basis audit queue in preflight.
- `381bcfb` Document source basis queue validation.
- `53c51b8` Document formal preflight metadata checks.
- `34ecc61` Wire study tooling checks into report preflight.
- `5782725` Document study tooling preflight coverage.
- `06e77b4` Guard preregistration placeholders in preflight.
- `3f60f7c` Document preregistration preflight guard.
- `8a6139f` Guard CRD relevance lock in preflight.
- `f70b9c6` Document CRD preflight lock guard.
- `021d7f9` List CRD findings in real report scope.
- `d2b3a4e` Refresh CRD report scope status.
- `c8f69b3` Guard manual review queue in preflight.
- `7709397` Document manual review queue guard.
- `4b5d5d5` Refresh manual queue guard status.
- `cd27c3e` Guard WRR readiness doc in preflight.
- `3a4fecc` Document WRR readiness doc guard.
- `40aeb28` Refresh WRR readiness doc guard status.
- `441d429` Guard WRR blocker packet in preflight.
- `061ba7e` Document WRR blocker packet guard.
- `d1aacc2` Refresh WRR blocker packet guard status.
- `123ca07` Guard WRR lock options in preflight.
- `71c6465` Document WRR lock options guard.
- `9c28769` Refresh WRR lock options guard status.
- `c9b1cf3` Guard WRR method status in preflight.
- `2fa41bd` Document WRR method status guard.
- `81cc9a1` Refresh WRR method status guard.
- `bc3e098` Record WRR source redirect metadata.
- `549faf4` Document WRR source recovery probes.
- `44cb7d9` Refresh WRR source recovery status.
- `87636a5` Add WRR source recovery probe.
- `cc1527c` Guard WRR source recovery probe doc.
- `d8864e8` Probe WRR source shtml alternates.
- `2eea419` Refresh WRR source recovery register.
- `60f6ba1` Audit Torah-code hypothesis source pages.
- `2822abe` Guard hypothesis source audit doc.
- `11d22fc` Guard WRR defined diagnostic docs.
- `34c240d` Guard WRR variant gap docs.
- `cb09f08` Surface WRR variant gap method evidence.
- `c94b991` Guard WRR source review queue doc.
- `2a700c8` Guard WRR D formula sensitivity doc.
- `61b8060` Guard WRR source policy scenario doc.
- `bf099f7` Guard WRR cross pair grid doc.
- `96de90a` Guard WRR direct all-lane diagnostic doc.

### Formal Real Report Rerun

Command completed successfully after the worktree was cleaned:

```bash
python3 -m scripts.run_protocol protocols/real_report_run.toml --resume
```

Current summary:

- `reports/real_report_run/summary.md`
- local generated report files under `reports/real_report_run/` are ignored by
  Git and record the commit active when the protocol last ran.
- after tracked planning-doc commits, rerun
  `python3 -m scripts.run_protocol protocols/real_report_run.toml --resume`
  if exact local manifest-to-HEAD alignment matters.

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

Current status: source/import work, corrected-distance diagnostics, a
lock-prep pair eligibility table, source-policy scenario diagnostics, and a
claim-readiness gate. Remaining claim-grade pieces:

- candidate pair source/reconciliation, with `163` treated as the
  source-defined corrected-distance output count rather than a raw pair table;
- source-policy lock for WNP/context rows. Single-term Zacut diagnostics now
  show `ZKWTA`, `ZKWTW`, `M$HZKWTA`, and `M$HZKWTW` each individually leave
  163 >=5 pairs with gap 0 if excluded, but that remains diagnostic count
  evidence only;
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
- `docs/WRR_CLAIM_BLOCKER_PACKET.md`
- `docs/WRR_LOCK_OPTIONS.md`
- `reports/wrr_1994/wrr2_pair_eligibility_table.csv`
- `reports/wrr_1994/wrr_source_policy_term_impacts.csv`
- `tests/test_wrr_stats.py`

Recent source-audit follow-up added a Torah-code.org geometric level-1
simulation harness and an ELS/cylinder level-1 analogue:

- `scripts/simulate_torah_code_research_model.py`
- `scripts/simulate_torah_code_research_els_model.py`
- `protocols/torah_code_research_geometric_model.toml`
- `docs/TORAH_CODE_RESEARCH_MODEL_SIMULATION.md`
- `docs/TORAH_CODE_RESEARCH_ELS_MODEL_SIMULATION.md`

The Gans/Inbal/Bombach communities data source now has a source-shape audit:

- `scripts/analyze_gans_communities_source.py`
- `protocols/gans_communities_source_audit.toml`
- `docs/GANS_COMMUNITIES_SOURCE_AUDIT.md`

The American presidents data/rule source also has a source-shape audit:

- `scripts/analyze_american_presidents_source.py`
- `protocols/american_presidents_source_audit.toml`
- `docs/AMERICAN_PRESIDENTS_SOURCE_AUDIT.md`

The Witztum Genesis birth-date source has a source-shape audit:

- `scripts/analyze_witztum_birth_dates_source.py`
- `protocols/witztum_birth_dates_source_audit.toml`
- `docs/WITZTUM_BIRTH_DATES_SOURCE_AUDIT.md`

The Israeli prime-ministers source has a source-shape audit:

- `scripts/analyze_israeli_prime_ministers_source.py`
- `protocols/israeli_prime_ministers_source_audit.toml`
- `docs/ISRAELI_PRIME_MINISTERS_SOURCE_AUDIT.md`

The Cities/Aumann/Simon-McKay source chain has a source-shape audit:

- `scripts/analyze_cities_source_chain.py`
- `protocols/cities_source_chain_audit.toml`
- `docs/CITIES_SOURCE_CHAIN_AUDIT.md`

The Sons of Haman, Pumbedita, Auschwitz, and Ark source pages have a
source-shape audit:

- `scripts/analyze_event_object_experiments_source.py`
- `protocols/event_object_experiments_source_audit.toml`
- `docs/EVENT_OBJECT_EXPERIMENT_SOURCE_AUDIT.md`

The Chumash, Twin Towers, Tsunami, Katrina, Great Rabbis, and Son Rabbis
placeholder pages have a source-status audit:

- `scripts/analyze_under_construction_experiments_source.py`
- `protocols/under_construction_experiments_source_audit.toml`
- `docs/UNDER_CONSTRUCTION_EXPERIMENT_SOURCE_AUDIT.md`

The Torah-code.org hypothesis-testing overview and linked subpages have a
source-status audit:

- `scripts/analyze_hypothesis_testing_source.py`
- `protocols/hypothesis_testing_source_audit.toml`
- `docs/HYPOTHESIS_TESTING_SOURCE_AUDIT.md`

The Bombach/Gans co-linear ELS/verse paper and attachment files have a
source-shape audit:

- `scripts/analyze_colinear_els_source.py`
- `protocols/colinear_els_source_audit.toml`
- `docs/COLINEAR_ELS_SOURCE_AUDIT.md`

The co-linear ELS source audit confirms the paper PDF, 8 linked attachment
PDFs, 515 attachment pages, 6 attachments with explicit row-count expectations,
8,260 expected and observed source rows, 6,060 raw PLS pair rows extracted from
the PLS PDF, 12,830 raw roots rows extracted from the roots PDF, 1,698 raw
all_1698 phrase/verse rows extracted from the all_1698 PDF, 502 raw reviewed
subset rows extracted from the four reviewed subset PDFs, 7 Hebrew-method
appendix anchors, and 21/21 protocol anchors. The
communities audit confirms 66 data records and 210 machine-readable pre-filter
community rows. The presidents audit confirms 42 data records and 279
machine-readable spelling rows. The birth-date audit confirms two S1/S2
tables, 14 rows per table, and 51 date forms per table. The Israeli
prime-ministers audit confirms 12 PDF rows, 43 machine-readable PDF keyword
rows, and 8 downloaded detail-page rows, leaving a 4-page detail-source coverage
gap. The Cities audit confirms 13 source-chain files,
6 `.pdf`-named HTML wrappers, 5 Wayback job-failed wrappers, 1 parse-error PDF,
1 no-text PDF, and 7/7 source anchors. The event/object audit confirms 8 source
files, 20 Pumbedita rows, 32 Auschwitz rows, 12 Sons-of-Haman keyword rows, 1
Auschwitz topic row, 65 machine-readable source rows, a 57-page Ark tutorial
PDF, one reported significant follow-up page, two reported non-significant
pages, and one under-construction page.
The under-construction audit confirms six placeholder pages, no PDF data links,
four copied-title mismatches, and the Katrina page mislabeled as Tsunami.
The hypothesis-testing source audit confirms four hypothesis-testing URLs now
redirect to the Torah-code root, share the same spam-root hash prefix
`d60a59519b55bcff`, contain no expected labels, and provide zero usable method
source pages in the current live crawl.
The missing-model-pages audit confirms that four linked Torah-code.org
level-2/3 geometric and ELS model pages currently download as root-canonical
pages with unrelated slot/gambling content, no expected model labels, and zero
usable model pages. The adjacent level-1 geometric and ELS model pages are
usable source context, but they do not supply the missing level-2/3 rules.
The WRR source downloader now supports targeted `--label` refreshes and records
requested URL, final URL, redirect status, HTTP status, bytes, and hash in the
source manifest. A local targeted refresh can check source recovery without
overwriting the whole ignored source bundle.
The isolated WRR source recovery probe now refreshes selected Torah-code
research labels into `reports/wrr_source_recovery_probe/` and writes
`docs/WRR_SOURCE_RECOVERY_PROBE.md`, so live recovery checks no longer risk
overwriting cached `reports/wrr_1994/` source files. The current live probe
finds 15/15 selected research URLs, including stale-indexed `.shtml`
alternates, redirecting to the Torah-code root, 15/15 root canonical rows,
15/15 unrelated slot/gambling-marker rows, and zero usable current source rows.
These lanes stay non-result-bearing. The
research-program ELS harness now includes a split-fit Fisher order-statistic
row plus two transparent row-width modes: strict shared-intersection
candidates and broader combined WRR-series candidates. Next research-program
upgrade: recover a citable fuller source-method reconstruction and
source-published Fisher weights if available; only then consider real
Torah-code source data, communities compactness runs, American-presidents
transliteration experiments, or Witztum birth-date ELS/SL-proximity tests. Do
not run an Israeli prime-ministers result protocol until the missing
detail-page coverage is resolved or explicitly scoped out in a new
preregistration. Do not import Cities city-name rows until the wrapped or
missing PDF sources are recovered, or the usable HTML-only source boundary is
explicitly locked. Do not promote the event/object pages beyond source-shape
status until each lane has its own preregistered term normalization and
control design. Do not use under-construction placeholder pages as data-bearing
protocols unless future source recovery finds real data pages. Do not use the
four level-2/3 research model downloads as method sources unless clean
Torah-code pages are recovered and checksummed. Do not promote the co-linear
ELS/verse source lane until Hebrew term/root normalization, verse-link scoring,
and controls are preregistered separately.

WRR aggregate work now has a diagnostic P1..P4 bridge:

- `scripts/analyze_wrr_corrected_distance_aggregate.py`
- `reports/wrr_1994/wrr2_corrected_distance_aggregate.csv`
- `scripts/check_wrr_claim_readiness.py`
- `docs/WRR_CLAIM_READINESS.md`

Current read: the length-5..8 direct-search corrected-distance smoke output has
28 defined `c(w,w')` values at cap 250 and 46 defined values in the cap-1000
split diagnostic, so P1..P4 diagnostic rows now populate. The cross-pair
cap-250 matrix now also supports two date-label permutation diagnostics: the
older 1,000-sample all-row diagnostic and the current repo-defined
WNP-excluded 999,999-permutation diagnostic. The current repo-defined run has
174 observed rows, 48 defined `c(w,w')` values, and Bonferroni rho0 `0.00086`.
The readiness gate still stays blocked until pair universe, `D(w)`, full
corrected distance, and claim-grade permutation/aggregate statuses are locked.

All-lane diagnostic follow-up now exists:
`protocols/wrr_corrected_distance_direct_all_lanes.toml` and
`docs/WRR_DIRECT_ALL_LANES_DIAGNOSTIC.md`. It defines 50 values at cap 250 and
72 at cap 1000 over all 182 imported same-record pairs, still far below the
source-cited 163 defined second-list distances. The tracked protocol now also
runs the cap-1000 reported-program `D(w)` formula sensitivity check; it changes
0 pair rows versus the printed-formula diagnostic.
`docs/WRR_DEFINED_PAIR_SET_AUDIT.md` now joins those outputs back to
candidate-lane, review-status, and WNP-Zacut labels: best current direct run
defines 72 of 163, leaving a 91-distance gap, with ordinary-not-valid rows as
the dominant missing mass.
`docs/WRR_DEFINED_GAP_REASON_AUDIT.md` now classifies that missing mass: in the
best cap-1000 run, 83 rows lack appellation ordinary hits, 12 lack date
ordinary hits, 15 lack both, and 0 are under-minimum perturbation cases. The
method-status matrix now also surfaces the variant-gap impact over those
blocked pairs: in the best cap-1000 run, 51 blocked pairs have all blocking
terms with simple variant leads, 9 have partial variant leads, and 50 have no
simple variant lead. The next WRR work is therefore source/term/pair-rule
reconciliation before any claim-grade permutation language.

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
The KJVA prospective lane used a preregistration/protocol/term-file lock before
producing result-bearing outputs:

- `terms/kjv_apocrypha_bridge_prospective_terms.csv`
- `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_PREREGISTRATION.md`
- `protocols/kjv_apocrypha_bridge_prospective_controls_5000.toml`
- `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CANDIDATES.md`
- `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CONTROLS_5000.md`
- `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_NONBIBLE_CONTROLS.md`
- `protocols/kjv_apocrypha_bridge_prospective_nonbible_controls.toml`

Boundary note: this older lane does not have a
`reports/study_locks/*.manifest.json` or preflight sidecar. Its negative result
can be rerun for reproducibility, but any future KJVA bridge follow-up should
use the current full study-lock-manifest and preflight workflow before
producing new result-bearing output.

Candidate inputs:

- `docs/KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_PREREGISTRATION.md`
- `docs/KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_CONTROLS_5000.md`
- `terms/kjv_apocrypha_bridge_confirmatory_terms.csv`

Prospective result: 7 registered terms, 1 observed bridge row (`tobit`), 0
terms with Benjamini-Hochberg `q_ge <= 0.05`, and 0 terms above every shuffled
sample. This is negative under the registered shuffled-insertion control rule.
The secondary non-Bible insertion control is also cautionary: 1 of 3 non-Bible
controls is at or above the observed total because the Moby Dick replacement
block also produced 1 `tobit` bridge row.
The lane is now recorded in `configs/prospective_study_lanes.json` and
`docs/PROSPECTIVE_LANE_STATUS.md` as a completed negative controlled result.

Current next step: look for independent replication designs or define a new
locked prospective lane. No KJVA prospective bridge claim language is supported
by the current controls, and there is no remaining `ready_for_preflight` lane in
`configs/prospective_study_lanes.json`.

Covered by the prospective lock:

- fixed prospective term list;
- fixed insertion/control design;
- fixed skip range;
- fixed correction rule.

Still needed before claim language:

- independent replication or a new locked prospective design that survives
  shuffled and non-Bible insertion controls.

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

Current observed result after the WRR gap-reason audit, readiness gate,
single-term source-policy propagation, missing-model adjacent-source audit,
preflight guard pass, Greek follow-up status refresh, Hebrew MT/STEP_TAHOT
status refresh, KJVA bridge lock-basis clarification, prospective-lane
validator tightening, source-audit preflight guard coverage, prospective-lane
validation in report preflight, source-basis audit queue guarding, and English
source-basis preflight inputs, formal source-basis queue validation, and
source-basis validation documentation, plus formal preflight metadata-check
documentation, study-tooling preflight coverage, and preregistration
placeholder guarding, CRD relevance-lock guarding, manual-review queue
preflight guarding, WRR readiness-doc guarding, WRR blocker-packet preflight
guarding, WRR lock-options preflight guarding, and WRR method-status preflight
guarding, WRR source-recovery probing, WRR source-recovery probe guarding, and
`.shtml` research-source alternate probing, hypothesis-testing source-status
guarding, WRR defined-distance diagnostic doc guarding, and WRR variant-gap
doc guarding, and WRR variant-gap method-status evidence propagation:

- `python3 -m pytest -q` passed: 1211 tests and 13961 subtests.
- `python3 -m pytest tests/test_download_wrr_sources.py tests/test_build_wrr_source_recovery_probe.py tests/test_check_wrr_source_recovery_probe_doc.py tests/test_real_report_run.py -q` passed: 50 tests and 42 subtests.
- `python3 -m pytest tests/test_analyze_hypothesis_testing_source.py tests/test_download_wrr_sources.py -q` passed: 9 tests and 46 subtests.
- `python3 -m pytest tests/test_check_hypothesis_testing_source_audit_doc.py tests/test_real_report_run.py -q` passed: 42 tests.
- `python3 -m pytest tests/test_check_wrr_defined_diagnostic_docs.py tests/test_real_report_run.py -q` passed: 45 tests.
- `python3 -m pytest tests/test_check_wrr_variant_gap_docs.py tests/test_real_report_run.py -q` passed: 46 tests.
- `python3 -m pytest tests/test_wrr_method_status.py tests/test_wrr_cross_pair_grid.py tests/test_check_wrr_method_status_doc.py tests/test_check_wrr_claim_readiness_doc.py -q` passed: 15 tests.
- `python3 -m pytest tests/test_check_wrr_claim_readiness_doc.py tests/test_real_report_run.py -q` passed: 38 tests.
- `python3 -m pytest tests/test_check_wrr_claim_blocker_packet_doc.py tests/test_real_report_run.py -q` passed: 39 tests.
- `python3 -m pytest tests/test_check_wrr_lock_options_doc.py tests/test_real_report_run.py -q` passed: 40 tests.
- `python3 -m pytest tests/test_check_wrr_method_status_doc.py tests/test_real_report_run.py -q` passed: 41 tests.
- `python3 -m pytest tests/test_check_manual_review_queue.py tests/test_real_report_run.py -q` passed: 37 tests.
- `python3 -m pytest tests/test_real_report_run.py tests/test_crd_dictionary_tools.py -q` passed: 40 tests.
- `python3 -m pytest tests/test_real_report_run.py tests/test_check_preregistration_placeholders.py -q` passed: 36 tests.
- `python3 -m pytest tests/test_real_report_run.py tests/test_check_expanded_strata_tooling.py tests/test_validate_study_mapping_schemas.py -q` passed: 38 tests.
- `python3 -m pytest tests/test_import_bolls_translation.py tests/test_english_version_manifests.py -q` passed: 12 tests and 117 subtests.
- `python3 -m pytest tests/test_english_version_manifests.py -q` passed: 8 tests and 117 subtests.
- `python3 -m pytest tests/test_check_source_basis_audit_queue.py tests/test_english_version_manifests.py tests/test_real_report_run.py -q` passed: 39 tests and 117 subtests.
- `python3 -m scripts.check_source_basis_audit_queue` passed.
- `python3 -m scripts.check_expanded_strata_tooling --report /tmp/edls_expanded_tooling_after_patch.json` passed.
- `python3 -m scripts.validate_study_mapping_schemas` passed.
- `python3 -m scripts.check_crd_relevance_dictionary --dictionary terms/relevance_dictionary.toml --term-file terms/gog_magog_pair_prospective_terms.csv --expected-sha256 a6406048b9953ca50715d99100994b9065394d9db31b35867666d365a3bd0f99 --require-reviewed` passed.
- `python3 -m scripts.check_manual_review_queue` passed.
- `python3 -m scripts.check_wrr_claim_readiness_doc` passed.
- `python3 -m scripts.check_wrr_claim_blocker_packet_doc` passed.
- `python3 -m scripts.check_wrr_lock_options_doc` passed.
- `python3 -m scripts.check_wrr_method_status_doc` passed.
- `python3 -m scripts.check_wrr_defined_diagnostic_docs` passed.
- `python3 -m scripts.check_wrr_variant_gap_docs` passed.
- `python3 -m scripts.run_protocol protocols/wrr_source_recovery_probe.toml --resume` passed.
- `python3 -m scripts.run_protocol protocols/hypothesis_testing_source_audit.toml --resume` passed.
- `python3 -m scripts.check_wrr_source_recovery_probe_doc` passed.
- `python3 -m scripts.check_hypothesis_testing_source_audit_doc` passed.
- `python3 -m pytest tests/test_doxa_four_source_report.py tests/test_gog_magog_pair_prospective_report.py tests/test_wrr_method_status.py -q` passed: 13 tests.
- `python3 -m pytest tests/test_real_report_run.py tests/test_claim_catalog.py tests/test_wrr_claim_readiness.py -q` passed: 32 tests and 60 subtests.
- `python3 -m pytest tests/test_real_report_run.py -q` passed: 25 tests.
- `python3 -m pytest tests/test_check_prospective_study_lanes.py tests/test_build_prospective_lane_status.py -q` passed: 10 tests.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_check.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_source_audit_guard.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_english_source_basis.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_source_basis_docs.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_run_docs_source_basis.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_expanded_mapping_fullgate.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_prereg_placeholders.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_crd_lock.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_manual_queue.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_wrr_readiness_doc.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_wrr_blocker_packet_doc.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_wrr_lock_options_doc.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_wrr_method_status_doc.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_hypothesis_source_guard.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_wrr_defined_diag_docs.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_wrr_variant_gap_docs.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_variant_gap_method_status.json` passed.
- `python3 -m scripts.preflight_real_report_run --allow-dirty --out /tmp/edls_preflight_variant_gap_method_status_cross_pair.json` passed.
- `python3 -m scripts.check_prospective_study_lanes` passed.
- `git diff --check` passed.
- `python3 -m scripts.check_public_release_hygiene --allow-dirty` passed.
- `python3 -m scripts.run_protocol protocols/real_report_run.toml --resume` passed clean after each tracked WRR/report update.
