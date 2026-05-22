# Open Bible Codes

From-scratch Bible Codes / Equidistant Letter Sequence analysis toolkit for Hebrew, Greek, and English Bible texts.

## Scope

- Normalize Hebrew consonants: strip niqqud/cantillation, optionally fold final forms.
- Normalize Greek letters: strip accents/breathing, lowercase, fold final sigma.
- Normalize English letters: lowercase and remove punctuation, digits, and marks.
- Search signed skips across configured source texts.
- Preserve verse/source/word offsets for audit.
- Export CSV reports.
- Run simple shuffled-letter controls.

## Existing Python

- `els-engine`: small Hebrew ELS package on PyPI.
- `TorahBibleCodes`: larger Hebrew Bible Codes suite.
- `torahcodespython`: older ELS/gematria library.

This repo keeps its own MIT-licensed core so Hebrew, Greek, and English use same source mapping, reporting, and controls. Raw Bible texts stay outside git unless rights are clear.

Study framing is tracked in `docs/HYPOTHESIS_ANALYSIS_FRAMEWORK.md`: Hebrew
and Greek source texts are the primary hypothesis target, English versions are
secondary translation screens, and non-Bible controls are required comparison
backgrounds.

Project slug:

- `open-bible-codes`

Python command:

- `edls`
- `open-bible-codes`

## Quick Start

Tiny synthetic demo, no downloads required:

```bash
make demo
```

Repository navigation:

- documentation index: `docs/INDEX.md`
- protocol index: `protocols/INDEX.md`
- regenerate both: `make indexes`
- multi-machine dense partition workflow: `docs/PARTITION_WORKER_WORKFLOW.md`

Public-release hygiene check before publishing or pushing:

```bash
make public-release-check
```

This verifies the Git remote points at `Biblejustin/open-bible-codes`, rejects
tracked report/database/raw-source artifacts, scans tracked files for the
forbidden GitHub account text, and checks high-confidence secret-token patterns.

Full public source bootstrap:

```bash
python3 -m scripts.bootstrap_public_sources
```

This downloads MT OSHB WLC, MT UXLC, MT MAM, eBible Hebrew WLC, UHB, LXX
GRCLXX, TR GRCTR, Byzantine GRCMT, text-critical GRCTCGNT, English KJV, and
critical SBLGNT into ignored local data paths, then prints corpus stats.
Existing local source files are reused by default; pass `--refresh` to download again.

Corpus loads are cached under `data/cache/corpora/` by default. Set `EDLS_NO_CORPUS_CACHE=1` to force a fresh parse, or `EDLS_CORPUS_CACHE_DIR=/path/to/cache` to relocate the cache.

Performance benchmark:

```bash
python3 -m scripts.benchmark_performance
```

This runs a synthetic Aho/goto-table count benchmark plus real corpus load, find, batch-count, and surface-index benchmarks when local public sources exist. Missing real sources are skipped without downloading anything.

Observed optimization results are summarized in `docs/PERFORMANCE.md`.
WRR-style reproduction requirements are tracked in
`docs/WRR_REPLICATION_PLAN.md` and current blockers in
`docs/WRR_METHODOLOGY_GAPS.md`.

Parallel batch-count benchmark:

```bash
python3 -m scripts.benchmark_performance --jobs 4
```

Multiple term files can share each corpus scan:

```bash
python3 -m els batch-many \
  --term-set theological_terms=terms/theological_terms.csv \
  --term-set modern_names_dates=terms/modern_names_dates.csv \
  --term-set table_of_nations=terms/table_of_nations.csv \
  --term-set prophetic_terms=terms/prophetic_terms.csv \
  --corpus TR_NT=configs/example_ebible_grctr.toml \
  --min-skip 2 --max-skip 50 \
  --jobs 4 \
  --corpus-jobs 1 \
  --out-dir reports/batch_many
```

Keep `--corpus-jobs 1` unless local benchmarking shows corpus-level parallelism helps. Current public baseline is fastest with corpus-level serial execution and per-corpus count workers.

Fixed public baseline protocol:

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml
```

This runs the tracked public-source protocol and writes a protocol manifest plus report index under ignored `reports/` paths.
Plain-English findings are tracked in `docs/PUBLIC_BASELINE_FINDINGS.md`, `docs/TARGETED_TERMS_FINDINGS.md`, `docs/TARGETED_PAIRED_CONTROLS.md`, `docs/GOG_MAGOG_PAIR_CONTROLS.md`, `docs/GOG_MAGOG_STRICT_PAIR_CONTROLS.md`, `docs/PAIR_BASELINES.md`, `docs/SYNTHETIC_PAIR_BASELINES.md`, `docs/BEAST_DRAGON_STRICT_CONTROLS.md`, `docs/EXTENSION_PAIRED_CONTROLS.md`, `docs/EXTENSION_OVERLAP_CONTROLS.md`, `docs/EXTENSION_CONTEXT_REVIEW.md`, `docs/EXTENSION_EXACT_CENTER_CONTROLS.md`, `docs/EXTENSION_EXACT_CENTER_COHORT_CONTROLS.md`, `docs/EXTENSION_EXACT_CENTER_COHORT_REVIEW.md`, `docs/EXTENSION_EXACT_CENTER_CROSS_TEXT.md`, `docs/EXTENSION_EXACT_CENTER_FINAL_GATE.md`, `docs/EXTENSION_EXACT_CENTER_DEEP_CONTROLS.md`, `docs/SYNTHETIC_EXTENSION_BASELINES.md`, and `docs/SYNTHETIC_EXTENSION_MATCH_REVIEW.md`.

Focused 1000/1000 follow-up controls for the strongest exact-center extension
review row are available separately:

```bash
python3 -m scripts.run_protocol protocols/extension_deep_controls.toml --resume
```

Tracked summary: `docs/EXTENSION_EXACT_CENTER_DEEP_CONTROLS.md`.
Follow-up interpretation rules are frozen in
`docs/DOXA_FOLLOWUP_PREREGISTRATION.md`; the first locked follow-up report is
tracked in `docs/DOXA_FOLLOWUP_REPORT.md`.

Broader skip `2..100` screening is available separately:

```bash
python3 -m scripts.run_protocol protocols/broad_search.toml --resume
```

Tracked summary: `docs/BROAD_SEARCH_FINDINGS.md`.
The broad-search protocol now includes `KJV=configs/example_ebible_engkjv.toml`
and generated English concept terms from `terms/english_search_terms.csv`.
Combined current read over broad search, wide focus, controls, and same-skip
extensions: `docs/BROADER_SEARCH_FINDINGS.md`.

Local-only English version comparison is available for user-supplied AMPC, NLT,
MSG, TPT, and NIV CSVs kept outside git:

```bash
python3 -m scripts.run_protocol protocols/private_english_versions.toml --resume
```

Setup notes: `docs/PRIVATE_ENGLISH_VERSIONS.md`.

Full BibleGateway English-version local hooks:

```bash
python3 -m scripts.run_protocol protocols/biblegateway_english_versions.toml --resume
```

Version manifest: `configs/biblegateway_english_versions.csv`.

Current broad refresh has 34 available BibleGateway-overlap English versions
and skips 30 missing local CSVs. Missing rows are listed in
`reports/biblegateway_english_versions/missing_versions.csv`.

Source-basis metadata queue:
`docs/SOURCE_BASIS_AUDIT_QUEUE.md`. Validate it with
`python3 -m scripts.check_source_basis_audit_queue`.

Additional open/CC eBible English control corpora:

```bash
python3 -m scripts.download_ebible_english_controls --skip-existing
python3 -m scripts.run_protocol protocols/ebible_english_controls.toml --resume
```

Control manifest: `configs/ebible_english_controls.csv`.

Compare the BibleGateway-overlap set against those controls and inspect the
strongest seed-term contexts:

```bash
python3 -m scripts.run_protocol protocols/english_version_control_triage.toml --resume
```

Exploratory shuffled-letter baseline for observed English seed-term hits:

```bash
python3 -m scripts.run_protocol protocols/english_seed_shuffle_baseline.toml --resume
```

100-sample follow-up for rows that reached the exploratory p-floor:

```bash
python3 -m scripts.run_protocol protocols/english_seed_shuffle_followup_100.toml --resume
```

1000-sample same-letter term-shuffle controls for English seed survivors.
Current 34-version refresh left `terms/english_seed_followup_survivors.csv`
empty, so leave these downstream survivor commands idle until that file has
data rows:

```bash
python3 -m scripts.run_protocol protocols/english_seed_term_shuffle_1000.toml --resume
```

Letter-path audit packet for English seed survivors:

```bash
python3 -m scripts.run_protocol protocols/english_seed_survivor_audit.toml --resume
```

Paired same-letter and corpus-random controls for English seed survivors:

```bash
python3 -m scripts.run_protocol protocols/english_seed_paired_controls_1000.toml --resume
```

MT/LXX reciprocal source-language presence gate:

```bash
python3 -m scripts.run_protocol protocols/mt_lxx_reciprocal_presence.toml --resume
```

Large non-Bible background controls are available for Hebrew, Greek, and
English:

```bash
python3 -m scripts.download_nonbible_controls
python3 -m scripts.run_protocol protocols/nonbible_control_counts.toml --resume
```

Tracked source/method notes: `docs/NONBIBLE_CONTROL_CORPORA.md`.

Full-distance dynamic-skip counts for selected focus terms can be run against
Bible and non-Bible corpora:

```bash
python3 -m scripts.run_protocol protocols/dynamic_skip_focus_counts.toml --resume
python3 -m scripts.summarize_dynamic_span_counts
python3 -m scripts.compare_dynamic_span_bible_controls
```

Tracked summaries: `docs/DYNAMIC_SKIP_FOCUS_COUNTS.md`,
`docs/DYNAMIC_SKIP_BIBLE_CONTROL_COMPARISON.md`, and
`docs/DYNAMIC_SKIP_FOCUS_EXPECTATIONS.md`.

Modern/local same-skip extension screen:

```bash
python3 -m scripts.run_protocol protocols/modern_focus_extensions.toml --resume
python3 -m scripts.run_protocol protocols/version_presence_extensions.toml --resume
python3 -m scripts.run_protocol protocols/targeted_version_presence.toml --resume
```

Tracked summary: `docs/MODERN_EXTENSION_SCREEN.md`.
Version-presence extension summary:
`docs/VERSION_PRESENCE_EXTENSION_SCREEN.md`. Targeted modern/geopolitical/local
version-presence join plus representative controls:
`docs/TARGETED_VERSION_PRESENCE_REVIEW.md`.

Hebrew exact-hit MT-family version-presence screen:

```bash
python3 -m scripts.run_protocol protocols/hebrew_hit_version_presence.toml --resume
python3 -m scripts.run_protocol protocols/hebrew_modern_geopolitical_version_presence.toml --resume
python3 -m scripts.run_protocol protocols/hebrew_modern_geopolitical_controlled_review.toml --resume
python3 -m scripts.run_protocol protocols/hebrew_modern_geopolitical_prospective.toml --resume
python3 -m scripts.run_protocol protocols/hebrew_screening_version_presence.toml --resume
python3 -m scripts.run_protocol protocols/hebrew_screening_controlled_review.toml --resume
```

Tracked summary: `docs/HEBREW_HIT_VERSION_PRESENCE.md`.
Broad all-Hebrew-row modern/geopolitical/local/date summary:
`docs/HEBREW_MODERN_GEOPOLITICAL_VERSION_PRESENCE.md`.
Representative paired-control review for that broad modern/geopolitical run:
`docs/HEBREW_MODERN_GEOPOLITICAL_CONTROLLED_REVIEW.md` and
`docs/HEBREW_MODERN_GEOPOLITICAL_CONTROLLED_FINDINGS.md`.
Locked prospective source-distribution follow-up:
`docs/HEBREW_MODERN_GEOPOLITICAL_PROSPECTIVE_REPORT.md` and
`docs/HEBREW_MODERN_GEOPOLITICAL_PROSPECTIVE_FINDINGS.md`.
Broader Hebrew screening summary:
`docs/HEBREW_SCREENING_VERSION_PRESENCE.md`. Broader Hebrew screening
representative-control follow-up:
`docs/HEBREW_SCREENING_CONTROLLED_REVIEW.md` and
`docs/HEBREW_SCREENING_CONTROLLED_FINDINGS.md`.

Compiled Hebrew claim-term version-presence screen:

```bash
python3 -m scripts.run_protocol protocols/hebrew_claim_version_presence.toml --resume
```

Tracked summary: `docs/HEBREW_CLAIM_VERSION_PRESENCE.md`.

Hebrew null/frequency control version-presence screen:

```bash
python3 -m scripts.run_protocol protocols/hebrew_control_version_presence.toml --resume
```

Tracked summary: `docs/HEBREW_CONTROL_VERSION_PRESENCE.md`.
Comparison across the Hebrew modern, claim, and control version-presence runs:
`docs/HEBREW_VERSION_PRESENCE_COMPARISON.md`.
Source-specific Hebrew distribution:
`docs/HEBREW_VERSION_SPECIFIC_DISTRIBUTION.md`.

Greek NT exact-hit version-presence screens:

```bash
python3 -m scripts.run_protocol protocols/greek_nt_claim_version_presence.toml --resume
python3 -m scripts.run_protocol protocols/greek_control_version_presence.toml --resume
python3 -m scripts.run_protocol protocols/greek_screening_version_presence.toml --resume
```

Tracked summaries: `docs/GREEK_NT_CLAIM_VERSION_PRESENCE.md`,
`docs/GREEK_CONTROL_VERSION_PRESENCE.md`, and
`docs/GREEK_VERSION_PRESENCE_COMPARISON.md`. Broader Greek screening summary:
`docs/GREEK_SCREENING_VERSION_PRESENCE.md`.
LXX/NT corpus-presence read from the broad search:
`docs/GREEK_LXX_NT_CORPUS_PRESENCE.md`.

Locked Greek exact-center theological cohort:

```bash
python3 -m scripts.run_protocol protocols/greek_exact_center_cohort.toml --resume
```

Preregistration: `docs/GREEK_EXACT_CENTER_COHORT_PREREGISTRATION.md`.
Tracked report: `docs/GREEK_EXACT_CENTER_COHORT_REPORT.md`.

Greek exact-center final gate:

```bash
python3 -m scripts.run_protocol protocols/greek_exact_center_final_gate.toml --resume
```

Tracked summary: `docs/GREEK_EXACT_CENTER_FINAL_GATE.md`.

Locked four-source `δοξα` claim follow-up:

```bash
python3 -m scripts.run_protocol protocols/doxa_four_source_claim_followup.toml --resume
python3 -m scripts.build_doxa_four_source_claim_followup_report \
  --paired-summary reports/doxa_four_source_claim_followup/paired_controls_summary.csv \
  --context-summary reports/doxa_four_source_claim_followup/context_review_summary.csv \
  --protocol-manifest reports/doxa_four_source_claim_followup/protocol_run.manifest.json \
  --report-out docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_REPORT.md \
  --manifest-out reports/doxa_four_source_claim_followup/report.manifest.json \
  --report-title "Doxa Four-Source Claim Follow-Up Report" \
  --preregistration-doc docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_PREREGISTRATION.md \
  --protocol-path protocols/doxa_four_source_claim_followup.toml \
  --term-control-samples 5000 \
  --random-control-samples 5000 \
  --preregistration-commit c91925b
```

Preregistration:
`docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_PREREGISTRATION.md`.
Tracked report: `docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_REPORT.md`.

Stricter locked four-source `δοξα` confirmatory follow-up:

```bash
python3 -m scripts.run_protocol protocols/doxa_four_source_confirmatory_followup.toml --resume
python3 -m scripts.build_doxa_four_source_claim_followup_report \
  --paired-summary reports/doxa_four_source_confirmatory_followup/paired_controls_summary.csv \
  --context-summary reports/doxa_four_source_confirmatory_followup/context_review_summary.csv \
  --protocol-manifest reports/doxa_four_source_confirmatory_followup/protocol_run.manifest.json \
  --report-out docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md \
  --manifest-out reports/doxa_four_source_confirmatory_followup/report.manifest.json \
  --report-title "Doxa Four-Source Confirmatory Follow-Up Report" \
  --preregistration-doc docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_PREREGISTRATION.md \
  --protocol-path protocols/doxa_four_source_confirmatory_followup.toml \
  --term-control-samples 20000 \
  --random-control-samples 20000 \
  --preregistration-commit 79f3c73
```

Preregistration:
`docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_PREREGISTRATION.md`.
Tracked report: `docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md`.

Expanded prospective Greek exact-center review queue:

```bash
python3 -m scripts.build_greek_expanded_prospective_terms
python3 -m scripts.run_protocol protocols/greek_expanded_prospective_exact_center.toml --resume
```

Preregistration: `docs/GREEK_EXPANDED_PROSPECTIVE_PREREGISTRATION.md`.
Tracked report: `docs/GREEK_EXPANDED_PROSPECTIVE_REPORT.md`.

Post-screen expanded Greek exact-center surface queue:

```bash
python3 -m scripts.run_protocol protocols/greek_expanded_surface_queue.toml --resume
python3 -m scripts.run_protocol protocols/greek_expanded_surface_triage.toml --resume
python3 -m scripts.run_protocol protocols/greek_expanded_surface_letter_paths.toml --resume
python3 -m scripts.run_protocol protocols/greek_expanded_surface_control_pool.toml --resume
python3 -m scripts.run_protocol protocols/greek_expanded_surface_control_evaluation.toml --resume
python3 -m scripts.run_protocol protocols/greek_expanded_surface_available_control_evaluation.toml --resume
python3 -m scripts.run_protocol protocols/greek_expanded_surface_followup.toml --resume
```

Tracked queue: `docs/GREEK_EXPANDED_SURFACE_QUEUE.md`.
Tighter review triage: `docs/GREEK_EXPANDED_SURFACE_TRIAGE.md`.
Letter-path audit: `docs/GREEK_EXPANDED_SURFACE_LETTER_PATHS.md`.
Real-word control pool: `docs/GREEK_EXPANDED_SURFACE_CONTROL_POOL.md`.
Matched-control evaluation:
`docs/GREEK_EXPANDED_SURFACE_CONTROL_EVALUATION.md`.
All-available matched-control follow-up:
`docs/GREEK_EXPANDED_SURFACE_AVAILABLE_CONTROL_POOL.md` and
`docs/GREEK_EXPANDED_SURFACE_AVAILABLE_CONTROL_EVALUATION.md`.
Compact follow-up report: `docs/GREEK_EXPANDED_SURFACE_FOLLOWUP_REPORT.md`.
Prospective claim-grade standard:
`docs/GREEK_SURFACE_PROSPECTIVE_CLAIM_STANDARD.md`.
Future preregistration lock manifests can be produced with
`python3 -m scripts.build_study_lock_manifest`, checked with
`python3 -m scripts.check_study_lock_manifest`, placeholder-checked with
`python3 -m scripts.check_preregistration_placeholders`, term-leakage audited with
`python3 -m scripts.audit_prospective_terms`, filtered with
`python3 -m scripts.filter_prospective_terms`, preflighted with
`python3 -m scripts.preflight_prospective_study`, and drafted with
`python3 -m scripts.scaffold_prospective_study`; see
`docs/STUDY_LOCK_MANIFESTS.md`, `docs/PROSPECTIVE_STUDY_READINESS.md`, and
`docs/PROSPECTIVE_TERM_AUDITS.md`. Template:
`docs/PROSPECTIVE_STUDY_PREREGISTRATION_TEMPLATE.md`.
Current lane profiles are stored in `configs/prospective_study_lanes.json` and
can be checked with `python3 -m scripts.check_prospective_study_lanes` and listed
with `python3 -m scripts.scaffold_prospective_study --list-profiles`.
The existing expanded Greek surface pool cannot support a second clean
length >= 5 prospective cohort; see
`docs/GREEK_SURFACE_SECOND_COHORT_READINESS.md`.

Centered-Relevance Density scaffold:

```bash
make crd-review-scaffold
make crd-review-apply
make crd-review-check
make crd-check
shasum -a 256 terms/relevance_dictionary.toml \
  prompts/crd_classifier_v1/system.md \
  prompts/crd_classifier_v1/user_template.md \
  docs/CRD_PREREGISTRATION.md
make crd-deterministic
make crd-parallel
make crd-llm
make crd-self-surface-center-word-presence
make crd-concept-surface-center-word-presence
make crd-center-word-findings
```

CRD compares centered ELS-hit density against locked relevance criteria across
Bible editions and language-matched secular controls. The committed dictionary
currently locks the Gog/Magog prospective cohort with `gpt-5-assisted-draft`
provenance. New cohorts require review, hash-locking in
`protocols/centered_relevance_density.toml`, and a locked
`docs/CRD_PREREGISTRATION.md` before interpretation. Method notes:
`docs/CRD_FRAMEWORK.md`. Generated report: `docs/CRD_REPORT.md`. Exact
center-word summaries are tracked in
`docs/CRD_CENTER_WORD_VERSION_PRESENCE_FINDINGS.md` and
`docs/CRD_CENTER_WORD_SELF_VS_CONCEPT_FINDINGS.md`; those summaries distinguish
term rows, distinct normalized surface forms, and distinct surface hit paths so
duplicate term-list entries do not get mistaken for separate visible words.

Locked Greek surface prospective cohort:

```bash
python3 -m scripts.run_protocol protocols/greek_surface_prospective.toml --resume
```

Preregistration: `docs/GREEK_SURFACE_PROSPECTIVE_PREREGISTRATION.md`.
Tracked report: `docs/GREEK_SURFACE_PROSPECTIVE_REPORT.md`.
Term file: `terms/greek_surface_prospective_terms.csv`.
This run uses the expanded Greek term list after removing prior selected
surface rows with `scripts.audit_prospective_terms` and
`scripts.filter_prospective_terms`.

Registered Hebrew theology follow-up cohort:

```bash
python3 -m scripts.run_protocol protocols/hebrew_theology_prospective.toml --resume
```

Preregistration: `docs/HEBREW_THEOLOGY_PROSPECTIVE_PREREGISTRATION.md`.
Tracked report: `docs/HEBREW_THEOLOGY_PROSPECTIVE_REPORT.md`.
Findings summary: `docs/HEBREW_THEOLOGY_PROSPECTIVE_FINDINGS.md`.
Term file: `terms/hebrew_theology_prospective_terms.csv`.
This is a narrow registered follow-up, not an untouched discovery run: prior
broad Hebrew screens exist, but this protocol locks the term cohort, five
MT-family sources, `2..100` skip range, both directions, and 1000+1000
representative MT_WLC/UHB controls before producing the report.

Relaxed all-codes collection for the same Hebrew theology cohort:

```bash
python3 -m scripts.run_protocol protocols/hebrew_theology_all_codes_collection.toml --resume
```

Tracked summary: `docs/HEBREW_THEOLOGY_ALL_CODES_COLLECTION.md`.
Ranked review queue: `docs/HEBREW_THEOLOGY_ALL_CODES_TRIAGE.md`. This keeps
every hidden-path row and adds same-center-word, related-center-word,
center-verse, and span-context flags. The triage queue ranks surface-near rows
first but still retains hidden-path-only candidates. It is intentionally broad
and should be read separately from claim-grade controls.

Broader relaxed all-codes collections:

```bash
python3 -m scripts.run_protocol protocols/hebrew_screening_all_codes_collection.toml --resume
python3 -m scripts.run_protocol protocols/greek_screening_all_codes_collection.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_followup_selection.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_followup_letter_paths.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_followup_context.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_followup_extensions.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_compound_extension_controls.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_compound_extension_confirmatory.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_followup_review.toml --resume
```

Tracked summaries: `docs/HEBREW_SCREENING_ALL_CODES_COLLECTION.md` and
`docs/GREEK_SCREENING_ALL_CODES_COLLECTION.md`. Ranked review queues:
`docs/HEBREW_SCREENING_ALL_CODES_TRIAGE.md` and
`docs/GREEK_SCREENING_ALL_CODES_TRIAGE.md`. Compact manual-review selection:
`docs/ALL_CODES_FOLLOWUP_SELECTION.md`. Selected-row letter-path audit:
`docs/ALL_CODES_FOLLOWUP_LETTER_PATHS.md`. Center/span context excerpts:
`docs/ALL_CODES_FOLLOWUP_CONTEXT.md`. Same-skip extension audit:
`docs/ALL_CODES_FOLLOWUP_EXTENSIONS.md`. Compound-extension controls:
`docs/ALL_CODES_COMPOUND_EXTENSION_CONTROLS.md`. Locked 5000/5000
compound-extension confirmatory controls:
`docs/ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_CONTROLS.md`.
Manual-review packet:
`docs/ALL_CODES_FOLLOWUP_REVIEW.md`.

Post-discovery length-4 Greek surface follow-up:

```bash
python3 -m scripts.run_protocol protocols/greek_surface_length4_followup.toml --resume
```

This follows up the all-source length-4 bucket exposed by the locked
prospective run. It is explicitly not prospective discovery. Tracked summaries:
`docs/GREEK_SURFACE_LENGTH4_FOLLOWUP_TRIAGE.md`,
`docs/GREEK_SURFACE_LENGTH4_CONTROL_POOL.md`,
`docs/GREEK_SURFACE_LENGTH4_CONTROL_EVALUATION.md`, and
`docs/GREEK_SURFACE_LENGTH4_LETTER_PATHS.md`.

Generated vocabulary-control follow-up for those length-4 rows:

```bash
python3 -m scripts.run_protocol protocols/greek_surface_length4_vocabulary_controls.toml --resume
```

This builds a generated length-4 real Greek surface-vocabulary control universe
under ignored `reports/` output, then reruns exact-center surface controls.
Tracked summaries: `docs/GREEK_SURFACE_LENGTH4_VOCABULARY_CONTROLS.md`,
`docs/GREEK_SURFACE_LENGTH4_VOCABULARY_CONTROL_POOL.md`, and
`docs/GREEK_SURFACE_LENGTH4_VOCABULARY_CONTROL_EVALUATION.md`.

Post-discovery SBLGNT source-only exact-center follow-up:

```bash
python3 -m scripts.run_protocol protocols/sblgnt_source_only_exact_center.toml --resume
```

Preregistration: `docs/SBLGNT_SOURCE_ONLY_EXACT_CENTER_PREREGISTRATION.md`.
Tracked report: `docs/SBLGNT_SOURCE_ONLY_EXACT_CENTER_REPORT.md`.

Current consolidated read: `docs/CONSOLIDATED_FINDINGS.md`.
Version-distribution report index: `docs/VERSION_DISTRIBUTION_INDEX.md`.
Conservative claim catalog: `docs/CLAIM_CATALOG.md`.
Bible Code Digest source audit and screening additions:
`docs/BIBLE_CODE_DIGEST_AUDIT.md`.
CRI ELS critique audit and control-design guardrails:
`docs/CRI_ELS_CRITIQUE_AUDIT.md`.
TheWordNotes ELS PDF source audit and screening additions:
`docs/THEWORDNOTES_ELS_AUDIT.md`.
Cosmic Codes source audit and screening additions:
`docs/COSMIC_CODES_AUDIT.md`.
Mark Tabata Isaiah 53 ELS source audit and screening additions:
`docs/MARK_TABATA_ISAIAH53_AUDIT.md`.
Felcjo Ringo ELS algorithm/source-control audit:
`docs/FELCJO_RINGO_ALGORITHM_AUDIT.md`.
Amandasaurus/Rory Biblecode implementation prior-art audit:
`docs/AMANDASAURUS_BIBLECODE_PRIOR_ART_AUDIT.md`.
Bible-codes.org pictogram/source audit and screening additions:
`docs/BIBLE_CODES_ORG_AUDIT.md`.
Bible and Science ELS critique/source audit:
`docs/BIBLE_AND_SCIENCE_CODES_AUDIT.md`.
Religions Wiki scriptural-codes critique/source audit:
`docs/RELIGIONS_WIKI_SCRIPTURAL_CODES_AUDIT.md`.
External claim/source term count baseline:
`docs/EXTERNAL_CLAIM_SOURCE_COUNTS.md`.
External claim/source retained all-codes collection and triage:
`docs/EXTERNAL_CLAIM_SOURCE_ALL_CODES_COLLECTION.md` and
`docs/EXTERNAL_CLAIM_SOURCE_ALL_CODES_TRIAGE.md`.
Co-linear ELS source audit:
`docs/COLINEAR_ELS_SOURCE_AUDIT.md`.
Gans communities source-shape audit:
`docs/GANS_COMMUNITIES_SOURCE_AUDIT.md` (66 records and 210 raw pre-filter
community rows).
American presidents source-shape audit:
`docs/AMERICAN_PRESIDENTS_SOURCE_AUDIT.md` (42 records and 279 spelling rows).
Witztum birth-date source-shape audit:
`docs/WITZTUM_BIRTH_DATES_SOURCE_AUDIT.md`.
Israeli prime-ministers source-shape audit:
`docs/ISRAELI_PRIME_MINISTERS_SOURCE_AUDIT.md` (12 PDF rows, 43 PDF keyword
rows, 8 detail rows).
Cities source-chain audit:
`docs/CITIES_SOURCE_CHAIN_AUDIT.md` (6 PDF-named wrappers, 5 Wayback job
failures).
Event/object experiment source audit:
`docs/EVENT_OBJECT_EXPERIMENT_SOURCE_AUDIT.md` (65 machine-readable source rows).
Under-construction experiment source audit:
`docs/UNDER_CONSTRUCTION_EXPERIMENT_SOURCE_AUDIT.md`.
Research missing model pages audit:
`docs/RESEARCH_MISSING_MODEL_PAGES_AUDIT.md`.
Targeted recovery probes can refresh individual WRR/Torah-code source labels:
`python3 -m scripts.download_wrr_sources --refresh --label torah_code_research_model_overview`.
The source manifest records requested URLs, final URLs, redirect status, HTTP
status, bytes, and hashes.
Reader-facing final report scaffold: `docs/FINAL_REPORT_OUTLINE.md`.
Reader-facing final report draft: `docs/FINAL_REPORT_DRAFT.md`.
Reader-facing final report: `docs/FINAL_REPORT.md`.
Compact final-report highlight table: `docs/FINAL_REPORT_HIGHLIGHTS.md`.
Completed Gog/Magog prospective pair-control report:
`docs/GOG_MAGOG_PAIR_PROSPECTIVE_REPORT.md`. Result: target rows occurred in
MT_WLC and UHB, but no `prospective_controlled_review_candidate` was produced.
Prospective-study lock/readiness notes: `docs/PROSPECTIVE_STUDY_NEXT_LOCK.md`.
Apocrypha/deuterocanon source coverage audit: `docs/APOCRYPHA_SOURCE_COVERAGE.md`.
Initial apocrypha bridge-candidate scan: `docs/APOCRYPHA_BRIDGE_CANDIDATES.md`.
Initial apocrypha bridge context review: `docs/APOCRYPHA_BRIDGE_CONTEXT.md`.
Initial apocrypha bridge controls: `docs/APOCRYPHA_BRIDGE_CONTROLS.md`.
Initial apocrypha bridge shuffled controls:
`docs/APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS.md`.
Expanded 50-sample apocrypha bridge shuffled controls:
`docs/APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_50.md`.
Expanded 100-sample apocrypha bridge shuffled controls:
`docs/APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_100.md`.
Current bridge read: the first Malachi/Tobit boundary scan found 62 rows, while
same-length non-Bible Greek boundary controls found 59, 39, and 61 rows.
Ordinary apocrypha-only counts: `docs/APOCRYPHA_ONLY_COUNTS.md`.
KJV + Apocrypha ordinary counts: `docs/KJV_APOCRYPHA_ONLY_COUNTS.md`.
KJV + Apocrypha bridge candidates: `docs/KJV_APOCRYPHA_BRIDGE_CANDIDATES.md`.
KJV + Apocrypha bridge context review: `docs/KJV_APOCRYPHA_BRIDGE_CONTEXT.md`.
KJV + Apocrypha bridge controls: `docs/KJV_APOCRYPHA_BRIDGE_CONTROLS.md`.
KJV + Apocrypha bridge term-level review:
`docs/KJV_APOCRYPHA_BRIDGE_TERM_REVIEW.md`.
KJV + Apocrypha bridge term-level shuffled controls:
`docs/KJV_APOCRYPHA_BRIDGE_TERM_SHUFFLED_CONTROLS_1000.md`.
KJV + Apocrypha bridge confirmatory preregistration:
`docs/KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_PREREGISTRATION.md`.
KJV + Apocrypha bridge confirmatory shuffled controls:
`docs/KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_CONTROLS_5000.md`.
KJV + Apocrypha bridge prospective preregistration:
`docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_PREREGISTRATION.md`.
KJV + Apocrypha bridge prospective candidates:
`docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CANDIDATES.md`.
KJV + Apocrypha bridge prospective shuffled controls:
`docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CONTROLS_5000.md`.
KJV + Apocrypha bridge prospective non-Bible insertion controls:
`docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_NONBIBLE_CONTROLS.md`.
KJV + Apocrypha bridge prospective shuffled-control protocol:
`protocols/kjv_apocrypha_bridge_prospective_controls_5000.toml`.
KJV + Apocrypha bridge prospective non-Bible control protocol:
`protocols/kjv_apocrypha_bridge_prospective_nonbible_controls.toml`.
KJV + Apocrypha bridge shuffled controls:
`docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS.md`.
KJV + Apocrypha expanded 50-sample bridge shuffled controls:
`docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_50.md`.
KJV + Apocrypha expanded 100-sample bridge shuffled controls:
`docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_100.md`.
KJV + Apocrypha expanded 250-sample bridge shuffled controls:
`docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS_250.md`.
Apocrypha/deuterocanon study protocol: `protocols/apocrypha_bridge_study.toml`.
Expanded bridge shuffled-control protocol:
`protocols/apocrypha_bridge_shuffled_controls_50.toml`.
Expanded 100-sample bridge shuffled-control protocol:
`protocols/apocrypha_bridge_shuffled_controls_100.toml`.
KJV + Apocrypha expanded 250-sample bridge shuffled-control protocol:
`protocols/kjv_apocrypha_bridge_shuffled_controls_250.toml`.
KJV + Apocrypha bridge term-level review protocol:
`protocols/kjv_apocrypha_bridge_term_review.toml`.
KJV + Apocrypha bridge term-level shuffled-control protocol:
`protocols/kjv_apocrypha_bridge_term_shuffled_controls_1000.toml`.
KJV + Apocrypha bridge confirmatory shuffled-control protocol:
`protocols/kjv_apocrypha_bridge_confirmatory_controls_5000.toml`.

Locked post-screen KJVA bridge confirmatory read: the 5000-sample follow-up
over the 15 registered BH-passing bridge terms found all 15 with
Benjamini-Hochberg `q_ge <= 0.01`, and 3 terms stood above every shuffled
sample. This is a stronger follow-up signal, but it remains post-screen
confirmatory calibration rather than original prospective claim evidence.
Fresh prospective KJVA bridge lock: fixed 7 English apocrypha/deuterocanon
proper names before any observed/control outputs under
`protocols/kjv_apocrypha_bridge_prospective_controls_5000.toml`. The locked
run found 1 observed bridge row (`tobit`), 0 terms with
Benjamini-Hochberg `q_ge <= 0.05`, and 0 terms above every shuffled sample.
The secondary non-Bible insertion check found 1 of 3 controls at or above the
observed total because the Moby Dick replacement block also produced 1 `tobit`
bridge row.

Formal report assembly run:

```bash
make real-report
# equivalent:
python3 -m scripts.run_protocol protocols/real_report_run.toml --resume
```

Tracked plan: `docs/REAL_REPORT_RUN.md`.
The preflight now also validates source-basis metadata, expanded-strata tooling
references, future study-mapping CSV schemas, and concrete preregistration
placeholder cleanup, plus the locked CRD relevance-dictionary basis before
summary assembly. It also checks the manual-review queue guardrails and
evidence links, plus the WRR method-status, lock-options, readiness, and
blocker-packet wording.

Resume without rerunning completed outputs:

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume
```

Report index only:

```bash
python3 -m scripts.build_report_index
```

ELS hit extensions:

```bash
python3 -m els extensions \
  --config configs/example_oshb_wlc.toml \
  --hits reports/search_hits.csv \
  --max-before 12 --max-after 12 \
  --phrase-words 4 \
  --out reports/search_hit_extensions.csv

python3 -m els extension-summary \
  --extensions reports/search_hit_extensions.csv \
  --out reports/search_hit_extensions_summary.csv \
  --top-out reports/search_hit_extensions_top.csv
```

This checks same-skip letters before and after hits against corpus-derived words and short phrases. See `docs/ELS_EXTENSIONS.md`.
Exact version-presence pattern rows can be exported into ordinary hit rows for
the same extension workflow; see `docs/VERSION_PRESENCE_HIT_EXPORT.md`.

Matrix/table coordinates:

```bash
python3 -m els matrix \
  --config configs/example_oshb_wlc.toml \
  --hits reports/search_hits.csv \
  --out reports/search_hit_matrix_letters.csv \
  --summary-out reports/search_hit_matrix_summary.csv
```

This exports row/column coordinates and per-letter paths for hit audit. See
`docs/MATRIX_TABLES.md`.

Skip planning by expected hit count:

```bash
python3 -m els skip-plan \
  --config configs/example_oshb_wlc.toml \
  --term משיח \
  --target-expected-hits 100 \
  --out reports/skip_plan.csv
```

This estimates a max skip before running a search. See `docs/SKIP_PLANNING.md`.
For exhaustive full-corpus skip bounds, supported search/count commands also
accept `--max-skip-mode full-span`, which computes
`floor((corpus_letters - 1) / (term_letters - 1))` per term. The related
`--max-skip-mode letters-per-term` option computes the rough
`floor(corpus_letters / term_letters)` cap used in some simple ELS
scatter-plot explanations. Use `--max-skip-limit N` as a safety cap.

Pair compactness and cylindrical table distance:

```bash
python3 -m els pairs \
  --terms terms/modern_names_dates.csv \
  --corpus MT_WLC=configs/example_oshb_wlc.toml \
  --left-category modern_names \
  --right-category dates \
  --row-width 50 \
  --out reports/modern_name_date_pairs.csv
```

See `docs/PAIR_COMPACTNESS.md`.

Public LXX:

```bash
python3 -m scripts.download_ebible_grclxx
python3 -m els stats --config configs/example_ebible_grclxx.toml
python3 -m els search --config configs/example_ebible_grclxx.toml --term θεος --min-skip 2 --max-skip 50 --out reports/grclxx_theos.csv
```

This uses eBible's public-domain-marked GRCLXX USFM package and writes a local checksum manifest.

Public TR NT:

```bash
python3 -m scripts.download_ebible_grctr
python3 -m els stats --config configs/example_ebible_grctr.toml
python3 -m els search --config configs/example_ebible_grctr.toml --term ιησους --min-skip 2 --max-skip 50 --out reports/grctr_iesous.csv
```

This uses eBible's public-domain-marked Greek Textus Receptus USFM package and writes a local checksum manifest.

Public KJV:

```bash
python3 -m scripts.download_ebible_engkjv
python3 -m els stats --config configs/example_ebible_engkjv.toml
python3 -m els search --config configs/example_ebible_engkjv.toml --term Jesus --min-skip 2 --max-skip 50 --out reports/kjv_jesus.csv
```

This uses eBible's public-domain-marked English KJV USFM package and writes a local checksum manifest. Generated English search terms are tracked in `terms/english_search_terms.csv`; rebuild them with:

```bash
python3 -m scripts.build_english_search_terms
```

Public KJV + Apocrypha:

```bash
python3 -m scripts.download_ebible_engkjv_apocrypha
python3 -m els stats --config configs/example_ebible_engkjv_apocrypha.toml
```

This keeps the KJV Apocrypha/Deuterocanon source in a separate `KJVA` corpus
path so existing 66-book KJV baselines do not change silently.

Private English comparison hooks:

- `configs/local_ampc.toml`
- `configs/local_nlt.toml`
- `configs/local_msg.toml`
- `configs/local_tpt.toml`
- `configs/local_niv.toml`

These expect local CSV files under `data/private/english/`, which is ignored by
git. No AMPC, NLT, MSG, TPT, or NIV source text is bundled in this repo.

Compiled Hebrew claim terms:

- `terms/hebrew_claim_terms.csv`
- `docs/HEBREW_CLAIM_TERMS.md`

Current wiring:

- `protocols/hebrew_claim_version_presence.toml` compares exact hit-pattern
  presence across the MT-family Hebrew corpora.
- `protocols/broad_search.toml`, `protocols/hebrew_screening_version_presence.toml`,
  `protocols/hebrew_screening_all_codes_collection.toml`, and
  `protocols/nonbible_control_counts.toml` include this list in broader
  screening and control runs.

Compiled Greek NT claim terms:

- `terms/greek_nt_claim_terms.csv`
- `docs/GREEK_NT_CLAIM_TERMS.md`

Current wiring:

- `protocols/greek_nt_claim_version_presence.toml` compares exact hit-pattern
  presence across Greek NT corpora.
- `protocols/broad_search.toml`, `protocols/greek_screening_version_presence.toml`,
  `protocols/greek_screening_all_codes_collection.toml`,
  `protocols/nonbible_control_counts.toml`, and
  `protocols/apocrypha_bridge_study.toml` include this list in broader
  screening, control, and bridge runs.

Additional declared screening/control lists:

- `terms/null_controls.csv` and `docs/NULL_CONTROLS.md`
- `terms/frequency_anchors.csv` and `docs/FREQUENCY_ANCHORS.md`
- `terms/biblical_tribes.csv` and `docs/BIBLICAL_TRIBES.md`
- `terms/biblical_festivals.csv` and `docs/BIBLICAL_FESTIVALS.md`
- `terms/biblical_calendar.csv` and `docs/BIBLICAL_CALENDAR.md`
- `terms/greek_exact_center_cohort_terms.csv` and `docs/GREEK_EXACT_CENTER_COHORT_PREREGISTRATION.md`

Current wiring:

- `terms/null_controls.csv` and `terms/frequency_anchors.csv` are used by
  Hebrew, Greek, STEP_TAHOT, broad-search, non-Bible-control, and real-report
  control protocols.
- `terms/biblical_tribes.csv`, `terms/biblical_festivals.csv`, and
  `terms/biblical_calendar.csv` are included in broader screening, all-codes,
  non-Bible-control, and real-report protocols where language-appropriate.
- `terms/greek_exact_center_cohort_terms.csv` is a locked follow-up cohort for
  the Greek exact-center protocol family, not a general baseline term list.

Greek:

```bash
mkdir -p data/raw
# Put Greek CSV at data/raw/greek.csv.
python3 -m els stats --config configs/example_greek.toml
python3 -m els search --config configs/example_greek.toml --term θεος --min-skip 2 --max-skip 50 --out reports/greek_theos.csv
```

Hebrew source:

```bash
mkdir -p data/raw
# Put consonantal Hebrew CSV at data/raw/hebrew.csv.
python3 -m els stats --config configs/example_hebrew.toml
python3 -m els search --config configs/example_hebrew.toml --term אלהים --min-skip 2 --max-skip 100 --out reports/hebrew_elohim.csv
```

UXLC Hebrew MT source:

```bash
python3 -m scripts.download_uxlc
python3 -m els stats --config configs/example_uxlc.toml
```

MAM Hebrew MT source:

```bash
python3 -m scripts.download_mam
python3 -m els stats --config configs/example_mam.toml
```

eBible Hebrew WLC source:

```bash
python3 -m scripts.download_ebible_hebwlc
python3 -m els stats --config configs/example_ebible_hebwlc.toml
```

unfoldingWord Hebrew Bible source:

```bash
python3 -m scripts.download_uhb
python3 -m els stats --config configs/example_uhb.toml
```

Optional STEP Bible TAHOT selected Hebrew OT source:

```bash
python3 -m scripts.download_step_tahot
python3 -m els stats --config configs/example_step_tahot.toml
```

This is a selected translator stream, not a pure Leningrad ketiv stream; see
`docs/HEBREW_MT_SOURCE_CANDIDATES.md` before using it in version-presence
reports.

STEP TAHOT source audit:

```bash
python3 -m scripts.run_protocol protocols/step_tahot_source_audit.toml --resume
```

Tracked summary: `docs/STEP_TAHOT_SOURCE_AUDIT.md`.

Focused modern/local exact-hit version presence with STEP TAHOT:

```bash
python3 -m scripts.run_protocol protocols/step_tahot_version_presence.toml --resume
```

Tracked summary: `docs/STEP_TAHOT_VERSION_PRESENCE_REVIEW.md`.

Broader Hebrew screening exact-hit version presence with STEP TAHOT:

```bash
python3 -m scripts.run_protocol protocols/step_tahot_screening_version_presence.toml --resume
```

Tracked summary: `docs/STEP_TAHOT_SCREENING_VERSION_PRESENCE.md`.

STEP_TAHOT-only source-policy audit:

```bash
python3 -m scripts.run_protocol protocols/step_tahot_policy_hits.toml --resume
```

Tracked summary: `docs/STEP_TAHOT_POLICY_HIT_AUDIT.md`.

Hebrew null/frequency control version presence with STEP TAHOT:

```bash
python3 -m scripts.run_protocol protocols/step_tahot_control_version_presence.toml --resume
```

Tracked summary: `docs/STEP_TAHOT_CONTROL_VERSION_PRESENCE.md`.

STEP_TAHOT-only null/frequency control source-policy audit:

```bash
python3 -m scripts.run_protocol protocols/step_tahot_control_policy_hits.toml --resume
```

STEP_TAHOT final gate:

```bash
python3 -m scripts.run_protocol protocols/step_tahot_final_gate.toml --resume
```

Tracked summary: `docs/STEP_TAHOT_FINAL_GATE.md`.

Hebrew MT-family version comparison:

```bash
python3 -m scripts.run_protocol protocols/mt_version_comparison.toml --resume
```

Current MT source coverage and candidate intake ranking:

- `docs/HEBREW_MT_SOURCE_CANDIDATES.md`

Michigan-Claremont Hebrew source:

```bash
python3 -m els stats --config configs/example_michigan_torah.toml
python3 -m els search --config configs/example_michigan_torah.toml --term תורה --min-skip 50 --max-skip 50 --out reports/torah_skip50.csv
```

Search direction:

- Default direction is `both`.
- Forward skips are positive.
- Backward skips are negative.
- Use `--direction forward` or `--direction backward` to restrict a run.

Hit rows include:

- `start_ref`, `end_ref`, `start_offset`, `end_offset`.
- `center_ref`, `center_offset`.
- `center_word_index`, `center_word`, `center_normalized_word`.
- `direction` and signed `skip`.

Surface-context hits:

```bash
python3 -m els surface-context \
  --terms terms/theological_terms.csv \
  --terms terms/modern_names_dates.csv \
  --terms terms/table_of_nations.csv \
  --terms terms/prophetic_terms.csv \
  --corpus TR_NT=configs/example_ebible_grctr.toml \
  --corpus SBLGNT=configs/example_sblgnt.toml \
  --min-skip 2 --max-skip 50 \
  --jobs 0 \
  --out reports/surface_context_hits.csv \
  --summary-out reports/surface_context_summary.csv \
  --manifest-out reports/surface_context.manifest.json
```

`surface-context` flags when a hit's key term appears in the center verse or span as surface text. It also flags same-concept and same-category terms from the term list.

Word counts and multiples:

```bash
python3 -m scripts.analyze_word_counts
```

This writes content-word counts by total/book/chapter/verse, flags multiples of 3, 7, 12, 40, and 70, and checks whether TR verse blocks absent from SBLGNT break those multiple counts.

Morphology counts:

```bash
python3 -m scripts.download_morphgnt_sblgnt
python3 -m scripts.analyze_morphology_counts
```

This counts lemma/POS rows for OSHB MT and MorphGNT SBLGNT. Content POS currently means nouns, verbs, and adjectives.

Critical surface variants:

```bash
python3 -m scripts.analyze_critical_surface_variants
```

This compares TR NT and SBLGNT content-word counts across common refs and flags multiple-pattern changes.

Theological batch counts:

```bash
python3 -m scripts.download_koren_torah
python3 -m scripts.download_oshb_wlc
python3 -m scripts.download_uxlc
python3 -m scripts.download_mam
python3 -m scripts.download_ebible_hebwlc
python3 -m scripts.download_uhb
python3 -m scripts.download_sblgnt
python3 -m scripts.download_ebible_grclxx
python3 -m scripts.download_ebible_grctr
python3 -m els batch \
  --terms terms/theological_terms.csv \
  --corpus MT_WLC=configs/example_oshb_wlc.toml \
  --corpus UXLC=configs/example_uxlc.toml \
  --corpus MAM=configs/example_mam.toml \
  --corpus EBIBLE_WLC=configs/example_ebible_hebwlc.toml \
  --corpus UHB=configs/example_uhb.toml \
  --corpus LXX=configs/example_ebible_grclxx.toml \
  --corpus TR_NT=configs/example_ebible_grctr.toml \
  --corpus SBLGNT=configs/example_sblgnt.toml \
  --min-skip 2 --max-skip 50 \
  --jobs 4 \
  --out reports/theological_terms_counts.csv \
  --manifest-out reports/theological_terms_counts.manifest.json
```

## Input CSV

Required:

- `ref`
- `text`

Recommended:

- `book`
- `chapter`
- `verse`

See `data/README.md`.

## Notes

ELS search is easy to cherry-pick. Treat results as descriptive until tested against fixed terms, fixed text, fixed skip bounds, and a documented null model.

See:

- `NOTICE.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `docs/SOURCES_AND_LICENSES.md`
