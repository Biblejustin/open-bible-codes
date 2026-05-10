# Protocols

Protocol files freeze run settings before analysis:

- input paths
- source configs
- term lists
- skip bounds
- direction
- output paths
- expected follow-up indexes/manifests

Run:

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml
```

Dry run:

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --dry-run
```

Formal report assembly run:

```bash
make real-report
# equivalent:
python3 -m scripts.run_protocol protocols/real_report_run.toml --resume
```

This runs preflight checks, refreshes locked STEP_TAHOT and Greek exact-center
final gates with resume, refreshes the WRR source-audit smoke track, builds the
generated report index, and writes `reports/real_report_run/summary.md`.
Tracked plan: `docs/REAL_REPORT_RUN.md`.

Run one step:

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --only batch_term_sets
```

Broader screening run:

```bash
python3 -m scripts.run_protocol protocols/broad_search.toml --resume
```

This keeps the fixed public baseline at skip `2..50` while also offering a
separate skip `2..100` sweep over every declared term list. Tracked summary:
`docs/BROAD_SEARCH_FINDINGS.md`.

Focused wide modern/prophetic screening run:

```bash
python3 -m scripts.run_protocol protocols/wide_focus_search.toml --resume
```

This keeps the broader all-list sweep at skip `2..100` while adding a focused
skip `2..250` run for modern/geopolitical/local and prophetic rows. Tracked
summary: `docs/WIDE_FOCUS_SEARCH.md`.

Focused wide exact-hit version-presence follow-up:

```bash
python3 -m scripts.run_protocol protocols/wide_focus_exact_presence.toml --resume
```

This exports capped exact ref-key patterns for length 4+ rows from the same
modern/geopolitical/local and prophetic focus set. Tracked summary:
`docs/WIDE_FOCUS_EXACT_PRESENCE.md`.

Focused wide paired-control follow-up:

```bash
python3 -m scripts.run_protocol protocols/wide_focus_paired_controls.toml --resume
```

This runs representative shuffled-term and same-length random controls for
nonzero wide-focus rows in MT_WLC, UHB, LXX, TR_NT, and SBLGNT. Tracked
summary: `docs/WIDE_FOCUS_PAIRED_CONTROLS.md`.

WRR source audit:

```bash
python3 -m scripts.run_protocol protocols/wrr_source_import.toml --resume
```

This downloads external WRR audit files into ignored reports output and converts
the WRR2 plain-text list into repo term rows without committing third-party
data. It also summarizes the raw ANU famous-rabbis source-list shapes so the
163-distance mismatch is visible before metric work. Tracked audit:
`docs/WRR_SOURCE_AUDIT.md`.

WRR imported-term Genesis count and pair smoke:

```bash
python3 -m scripts.run_protocol protocols/wrr_audit_counts.toml --resume
```

This counts the imported WRR2 appellation/date rows in Koren Genesis, emits a
same-record appellation/date pair audit, and control-screens the top raw pair
rows. It also repeats the pair audit/control screen with the WRR
appendix-compatible `5..8` length filter, audits expected-count skip caps, and
samples WRR-style perturbation boundary validity. It also fingerprints the
Koren Genesis source stream and emits a pair-table reconciliation for the
current imported-pair count versus the source-cited 163-distance WRR
second-list sample. It is not the WRR proximity statistic.

Hebrew MT-family version comparison:

```bash
python3 -m scripts.run_protocol protocols/mt_version_comparison.toml --resume
```

This aligns MT_WLC, UXLC, MAM, eBible WLC, and UHB by canonical book/chapter/verse
and reports normalized consonantal verse differences. Tracked summary:
`docs/MT_VERSION_COMPARISON.md`.

Hebrew exact-hit MT-family version-presence screen:

```bash
python3 -m scripts.run_protocol protocols/hebrew_hit_version_presence.toml --resume
python3 -m scripts.run_protocol protocols/hebrew_modern_geopolitical_version_presence.toml --resume
python3 -m scripts.run_protocol protocols/hebrew_modern_geopolitical_controlled_review.toml --resume
python3 -m scripts.run_protocol protocols/hebrew_screening_version_presence.toml --resume
python3 -m scripts.run_protocol protocols/hebrew_screening_controlled_review.toml --resume
```

The focused protocol compares selected modern/local Hebrew ELS hit ref-key
patterns across MT_WLC, UXLC, EBIBLE_WLC, MAM, and UHB. The broader
modern/geopolitical protocol applies the same check to every Hebrew row in
`terms/modern_names_dates.csv`. The controlled-review protocol runs
representative MT_WLC/UHB paired controls for the nonzero rows from that broad
modern/geopolitical matrix. The broader screening protocol applies the same
check to Hebrew rows from theological, modern, Table of Nations, prophetic,
Hebrew claim, tribe, festival, and calendar files. The broader screening
controlled-review protocol runs the same representative MT_WLC/UHB paired
controls over nonzero broader-screening rows. Tracked summaries:
`docs/HEBREW_HIT_VERSION_PRESENCE.md`,
`docs/HEBREW_MODERN_GEOPOLITICAL_VERSION_PRESENCE.md`,
`docs/HEBREW_MODERN_GEOPOLITICAL_CONTROLLED_REVIEW.md`,
`docs/HEBREW_MODERN_GEOPOLITICAL_CONTROLLED_FINDINGS.md`,
`docs/HEBREW_SCREENING_VERSION_PRESENCE.md`,
`docs/HEBREW_SCREENING_CONTROLLED_REVIEW.md`, and
`docs/HEBREW_SCREENING_CONTROLLED_FINDINGS.md`.

Compiled Hebrew claim-term version-presence screen:

```bash
python3 -m scripts.run_protocol protocols/hebrew_claim_version_presence.toml --resume
```

This compares exact hit ref-key patterns for `terms/hebrew_claim_terms.csv`
across the same Hebrew MT-family source set. Tracked summary:
`docs/HEBREW_CLAIM_VERSION_PRESENCE.md`.

Hebrew null/frequency control version-presence screen:

```bash
python3 -m scripts.run_protocol protocols/hebrew_control_version_presence.toml --resume
```

This compares exact hit ref-key patterns for `terms/null_controls.csv` and
`terms/frequency_anchors.csv` across the same Hebrew MT-family source set.
Tracked summary: `docs/HEBREW_CONTROL_VERSION_PRESENCE.md`.

STEP_TAHOT null/frequency control version-presence follow-up:

```bash
python3 -m scripts.run_protocol protocols/step_tahot_control_version_presence.toml --resume
```

This repeats the Hebrew null/frequency control screen with `STEP_TAHOT` added as
a selected sixth stream. Tracked summary:
`docs/STEP_TAHOT_CONTROL_VERSION_PRESENCE.md`.

STEP_TAHOT null/frequency control source-policy follow-up:

```bash
python3 -m scripts.run_protocol protocols/step_tahot_control_policy_hits.toml --resume
```

This audits the `STEP_TAHOT`-only control rows against TAHOT source-type paths.

STEP_TAHOT final gate:

```bash
python3 -m scripts.run_protocol protocols/step_tahot_final_gate.toml --resume
```

This joins the real-term and control-term source-only rates plus source-policy
audits into one held/review table. Tracked summary:
`docs/STEP_TAHOT_FINAL_GATE.md`.

Comparison across the Hebrew modern, claim, and control version-presence runs:
`docs/HEBREW_VERSION_PRESENCE_COMPARISON.md`.
Source-specific Hebrew distribution:
`docs/HEBREW_VERSION_SPECIFIC_DISTRIBUTION.md`.

Focused deep exact-center extension controls:

```bash
python3 -m scripts.run_protocol protocols/extension_deep_controls.toml --resume
```

This runs the slower 1000/1000 paired-control follow-up for the `δοξα`
cross-text exact-center extension row. Tracked summary:
`docs/EXTENSION_EXACT_CENTER_DEEP_CONTROLS.md`.

Locked Greek exact-center theological cohort:

```bash
python3 -m scripts.run_protocol protocols/greek_exact_center_cohort.toml --resume
```

This derives exact-center, cross-text Greek NT extension candidates from
`terms/greek_exact_center_cohort_terms.csv` and runs 1000/1000 controls.
Preregistration: `docs/GREEK_EXACT_CENTER_COHORT_PREREGISTRATION.md`.
Tracked report: `docs/GREEK_EXACT_CENTER_COHORT_REPORT.md`. It also emits
`reports/greek_exact_center_cohort/pattern_presence.csv` so source-specific
patterns remain visible.

Greek exact-center final gate:

```bash
python3 -m scripts.run_protocol protocols/greek_exact_center_final_gate.toml --resume
```

This consolidates version presence, row-local controls, context review, and
synthetic baselines into candidate-type labels. Hidden-path-only findings are
candidate types, not failures. Tracked summary:
`docs/GREEK_EXACT_CENTER_FINAL_GATE.md`.

Post-screen expanded Greek surface review:

```bash
python3 -m scripts.run_protocol protocols/greek_expanded_surface_queue.toml --resume
python3 -m scripts.run_protocol protocols/greek_expanded_surface_triage.toml --resume
python3 -m scripts.run_protocol protocols/greek_expanded_surface_letter_paths.toml --resume
python3 -m scripts.run_protocol protocols/greek_expanded_surface_available_control_evaluation.toml --resume
python3 -m scripts.run_protocol protocols/greek_expanded_surface_followup.toml --resume
```

This keeps exact-center surface rows visible even when no same-skip phrase
extension survives. The letter-path audit reconstructs the selected ELS paths
across TR_NT, BYZ_NT, TCG_NT, and SBLGNT. Tracked summaries:
`docs/GREEK_EXPANDED_SURFACE_TRIAGE.md`,
`docs/GREEK_EXPANDED_SURFACE_LETTER_PATHS.md`, and
`docs/GREEK_EXPANDED_SURFACE_AVAILABLE_CONTROL_EVALUATION.md`. Compact
selected-row follow-up:
`docs/GREEK_EXPANDED_SURFACE_FOLLOWUP_REPORT.md`.

Locked Greek surface prospective cohort:

```bash
python3 -m scripts.run_protocol protocols/greek_surface_prospective.toml --resume
```

This uses `terms/greek_surface_prospective_terms.csv`, which is the expanded
Greek prospective list after removing prior selected surface rows. It writes a
new prospective surface-context screen, queue, triage table, all-available
surface-frequency controls, and letter-path audit under
`reports/greek_surface_prospective/`. Preregistration:
`docs/GREEK_SURFACE_PROSPECTIVE_PREREGISTRATION.md`. Tracked compact report:
`docs/GREEK_SURFACE_PROSPECTIVE_REPORT.md`.

Registered Hebrew theology follow-up cohort:

```bash
python3 -m scripts.run_protocol protocols/hebrew_theology_prospective.toml --resume
```

This uses `terms/hebrew_theology_prospective_terms.csv` for a fixed 20-row
Hebrew theology cohort across MT_WLC, UXLC, EBIBLE_WLC, MAM, and UHB. It writes
exact version-presence rows, representative MT_WLC/UHB paired controls, and a
tracked report under `docs/HEBREW_THEOLOGY_PROSPECTIVE_REPORT.md`.
Preregistration: `docs/HEBREW_THEOLOGY_PROSPECTIVE_PREREGISTRATION.md`.
Findings summary: `docs/HEBREW_THEOLOGY_PROSPECTIVE_FINDINGS.md`.

Relaxed all-codes collection for the same Hebrew theology cohort:

```bash
python3 -m scripts.run_protocol protocols/hebrew_theology_all_codes_collection.toml --resume
```

This writes all hidden-path rows with `--include-all` under
`reports/hebrew_theology_all_codes/` and tracks a compact summary at
`docs/HEBREW_THEOLOGY_ALL_CODES_COLLECTION.md`. The row export now distinguishes
same center-word surface matches from broader center-verse surface matches. It
also tracks a ranked review queue at
`docs/HEBREW_THEOLOGY_ALL_CODES_TRIAGE.md`.

Broader relaxed all-codes collections:

```bash
python3 -m scripts.run_protocol protocols/hebrew_screening_all_codes_collection.toml --resume
python3 -m scripts.run_protocol protocols/greek_screening_all_codes_collection.toml --resume
python3 -m scripts.run_protocol protocols/english_screening_all_codes_collection.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_followup_selection.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_followup_letter_paths.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_followup_context.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_followup_extensions.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_compound_extension_controls.toml --resume
python3 -m scripts.run_protocol protocols/all_codes_followup_review.toml --resume
```

These retain every hidden-path row for the broader Hebrew, Greek, and English
KJV screening
cohorts and track compact summaries at
`docs/HEBREW_SCREENING_ALL_CODES_COLLECTION.md` and
`docs/GREEK_SCREENING_ALL_CODES_COLLECTION.md`, and
`docs/ENGLISH_SCREENING_ALL_CODES_COLLECTION.md`. Ranked review queues are
tracked at `docs/HEBREW_SCREENING_ALL_CODES_TRIAGE.md` and
`docs/GREEK_SCREENING_ALL_CODES_TRIAGE.md`, and
`docs/ENGLISH_SCREENING_ALL_CODES_TRIAGE.md`. The follow-up selection protocol
deduplicates those queues into `docs/ALL_CODES_FOLLOWUP_SELECTION.md`; the
letter-path audit protocol reconstructs every selected hidden path at
`docs/ALL_CODES_FOLLOWUP_LETTER_PATHS.md`; the context protocol exports
center/span excerpts at `docs/ALL_CODES_FOLLOWUP_CONTEXT.md`; the extension
protocol audits same-skip before/after lexicon matches at
`docs/ALL_CODES_FOLLOWUP_EXTENSIONS.md`; compound-extension paired controls
are tracked at `docs/ALL_CODES_COMPOUND_EXTENSION_CONTROLS.md`; the review
protocol packages the selected rows into `docs/ALL_CODES_FOLLOWUP_REVIEW.md`.

ChurchAges-style expected-count audit:

```bash
python3 -m scripts.run_protocol protocols/churchages_statistics_audit.toml --resume
```

This compares transcribed ChurchAges KJV observed counts against two
independent-letter expected-count baselines: the article's simplified
scatter-plot triangle and this repo's exact legal-window count. Tracked output:
`reports/churchages_statistics/audit.md`.

Post-discovery length-4 Greek surface follow-up:

```bash
python3 -m scripts.run_protocol protocols/greek_surface_length4_followup.toml --resume
```

This controls and audits the all-source length-4 bucket exposed by the locked
Greek surface prospective run. It is not prospective discovery. Tracked
summaries: `docs/GREEK_SURFACE_LENGTH4_FOLLOWUP_TRIAGE.md`,
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

This runs 1000/1000 controls for the SBLGNT-only `αιμα` and `υιος` exact-center
rows from the Greek exact-center cohort. Preregistration:
`docs/SBLGNT_SOURCE_ONLY_EXACT_CENTER_PREREGISTRATION.md`. Tracked report:
`docs/SBLGNT_SOURCE_ONLY_EXACT_CENTER_REPORT.md`.

Post-discovery BYZ_NT source-only exact-center follow-up:

```bash
python3 -m scripts.run_protocol protocols/byz_source_only_exact_center.toml --resume
```

This runs 1000/1000 controls for the BYZ_NT-only `υιος` exact-center row from
the four-source Greek pattern-presence matrix. Preregistration:
`docs/BYZ_SOURCE_ONLY_EXACT_CENTER_PREREGISTRATION.md`. Tracked report:
`docs/BYZ_SOURCE_ONLY_EXACT_CENTER_REPORT.md`.

Locked Greek exact-center independent-source follow-up:

```bash
python3 -m scripts.run_protocol protocols/greek_exact_center_three_source.toml --resume
```

This reruns the locked Greek exact-center cohort across TR_NT, BYZ_NT, and
SBLGNT, then controls only exact-center overlap groups that include the
independent Byzantine NT source. Preregistration:
`docs/GREEK_EXACT_CENTER_THREE_SOURCE_PREREGISTRATION.md`. Tracked report:
`docs/GREEK_EXACT_CENTER_THREE_SOURCE_REPORT.md`. It also emits
`reports/greek_exact_center_three_source/pattern_presence.csv` so
source-specific patterns remain visible.

Locked Greek exact-center added-source follow-up:

```bash
python3 -m scripts.run_protocol protocols/greek_exact_center_four_source.toml --resume
```

This reruns the locked Greek exact-center cohort across TR_NT, BYZ_NT, TCG_NT,
and SBLGNT, then controls only exact-center overlap groups that include the
added eBible Text-Critical Greek NT source. Preregistration:
`docs/GREEK_EXACT_CENTER_FOUR_SOURCE_PREREGISTRATION.md`. Tracked report:
`docs/GREEK_EXACT_CENTER_FOUR_SOURCE_REPORT.md`. It also emits
`reports/greek_exact_center_four_source/pattern_presence.csv` so source-specific
patterns remain visible.

Consolidated Greek pattern/version summary:

```bash
python3 -m scripts.run_protocol protocols/greek_pattern_versions.toml --resume
```

This merges the two-source, three-source, four-source, and source-only control
outputs into one current-status table. Tracked report:
`docs/GREEK_PATTERN_VERSION_SUMMARY.md`.

Version-distribution reporting methodology is tracked in
`docs/VERSION_DISTRIBUTION_METHOD.md`.

Targeted modern/geopolitical/local version-presence join:

```bash
python3 -m scripts.run_protocol protocols/targeted_version_presence.toml --resume
```

This joins the broader Hebrew and Greek exact-version summaries with available
paired controls and bounded version-presence extension summaries, then runs
representative `2..100` paired controls for nonzero target rows and regenerates
a final controlled summary. Tracked summary:
`docs/TARGETED_VERSION_PRESENCE_REVIEW.md`.

Greek NT exact-hit version-presence screens:

```bash
python3 -m scripts.run_protocol protocols/greek_nt_claim_version_presence.toml --resume
python3 -m scripts.run_protocol protocols/greek_control_version_presence.toml --resume
python3 -m scripts.run_protocol protocols/greek_screening_version_presence.toml --resume
```

These compare exact ELS hit ref-key patterns across TR_NT, BYZ_NT, TCG_NT, and
SBLGNT for Greek NT claim terms and Greek null/frequency controls. Tracked
summaries: `docs/GREEK_NT_CLAIM_VERSION_PRESENCE.md`,
`docs/GREEK_CONTROL_VERSION_PRESENCE.md`, and
`docs/GREEK_VERSION_PRESENCE_COMPARISON.md`. The broader screening run covers
Greek rows from theological, modern, Table of Nations, prophetic, Greek NT
claim, tribe, and festival files; tracked summary:
`docs/GREEK_SCREENING_VERSION_PRESENCE.md`.
LXX/NT corpus-presence read from the broad search:
`docs/GREEK_LXX_NT_CORPUS_PRESENCE.md`.

Resume completed outputs:

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume
```

Resume uses per-step integrity stamps under the manifest directory. Existing files
alone are not enough; input, command, and output fingerprints must match a prior
successful step. This avoids treating partial CSV/JSON output from an interrupted
run as cached and prevents stale resumes after term/config edits.

Set `always_run = true` on cheap summary/report steps whose output includes
volatile run metadata such as the current commit. That keeps expensive upstream
steps cached while refreshing the final local report text.

Long parallel groups print active-step heartbeats. Set
`progress_interval_seconds = 0` in a protocol file to silence them.

Benchmark repeated protocol runs:

```bash
python3 -m scripts.benchmark_protocol protocols/public_baseline.toml --runs 3
```

The benchmark writes ignored local reports under `reports/benchmarks/`:

- `public_baseline_benchmark.json`
- `public_baseline_benchmark.md`
- per-run protocol manifests

The public baseline also includes `els_controls`, which compares observed ELS
counts against shuffled-letter and shuffled-term controls. See
`docs/ELS_CONTROLS.md`.

The broad search protocol also emits `reports/broad_search/broad_version_presence.csv`,
which groups broad count rows by term and records which observed corpora contain
at least one hit.

The modern focus extension protocol runs a capped same-skip extension screen for
modern names, places, and local terms:

```bash
python3 -m scripts.run_protocol protocols/modern_focus_extensions.toml --resume
python3 -m scripts.run_protocol protocols/version_presence_extensions.toml --resume
```

It uses `surface-context --include-all` to collect capped hits, then runs
`els extensions` per corpus and summarizes phrase-extension rows under
`reports/modern_extension_screen/`.

The version-presence extension protocol exports bounded all-source Hebrew and
Greek version-presence rows into ordinary hit rows, then runs the same extension
workflow against MT_WLC, UHB, TR_NT, and SBLGNT. Tracked summary:
`docs/VERSION_PRESENCE_EXTENSION_SCREEN.md`.

The public baseline also derives TR NT and SBLGNT same-skip extension reports
from `surface_context_hits.csv`. Raw extension rows stay separate by corpus, then
`extension-summary` writes grouped counts and strongest compound-extension rows
with short-term noise filters enabled. See `docs/ELS_EXTENSIONS.md`.

See `docs/PUBLIC_BASELINE_FINDINGS.md` for the current plain-English findings
from the public baseline reports.

The `targeted_terms_report` step joins raw counts, controls, NT surface context,
and filtered extension tops for the current focused target set under
`reports/targeted_terms.*`.

Tracked summary: `docs/TARGETED_TERMS_FINDINGS.md`.

The `targeted_paired_controls` step compares each focused target row against
term-shuffle controls and same-length same-corpus random controls. Tracked
summary: `docs/TARGETED_PAIRED_CONTROLS.md`.

The `gog_magog_pairs` step checks Gog/Magog ELS proximity against paired
controls. Tracked summary: `docs/GOG_MAGOG_PAIR_CONTROLS.md`.

The `gog_magog_strict_pairs` step reruns Gog/Magog proximity requiring same
chapter and same signed skip. Tracked summary:
`docs/GOG_MAGOG_STRICT_PAIR_CONTROLS.md`.

The `pair_baselines` step compares strict observed pair counts for Gog/Magog
against unrelated declared prophetic pairs. Tracked summary:
`docs/PAIR_BASELINES.md`.

The `synthetic_pair_baselines` step compares short Hebrew strict pair density
against length-matched synthetic 3+4 letter strings sampled from MT_WLC letter
frequencies. Tracked summary: `docs/SYNTHETIC_PAIR_BASELINES.md`.

The `beast_dragon_strict_controls` step runs full strict paired controls for
the Hebrew baseline pair that exceeded Gog/Magog in observed strict close
pairs. Tracked summary: `docs/BEAST_DRAGON_STRICT_CONTROLS.md`.

The `extension_paired_controls` step checks filtered NT same-skip extension top
rows against shuffled-term and same-length random controls. Tracked summary:
`docs/EXTENSION_PAIRED_CONTROLS.md`.

The `extension_overlap_controls` step narrows that screen to strict TR/SBLGNT
overlap rows and raises the paired-control samples. Tracked summary:
`docs/EXTENSION_OVERLAP_CONTROLS.md`.

The `extension_context_review` step joins those strict overlap rows back to
center, hit-span, and extension-span verse context. Tracked summary:
`docs/EXTENSION_CONTEXT_REVIEW.md`.

The `extension_exact_center_controls` step reruns deeper 200/200 controls for
the exact-center `δοξα` overlap only. Tracked summary:
`docs/EXTENSION_EXACT_CENTER_CONTROLS.md`.

The separate `extension_deep_controls` protocol reruns that same exact-center
`δοξα` overlap with 1000/1000 controls. It stays outside the routine public
baseline because it is a slower focused follow-up.

The `extension_exact_center_cohort_controls` step broadens that follow-up to
all NT extension top rows whose center verse has exact surface context. Tracked
summary: `docs/EXTENSION_EXACT_CENTER_COHORT_CONTROLS.md`.

The `extension_exact_center_cohort_review` step builds the matching context and
letter-path sheets. Tracked summary:
`docs/EXTENSION_EXACT_CENTER_COHORT_REVIEW.md`.

The `extension_exact_center_cross_text` step checks exact-center cohort rows
against the opposite Greek NT text by exact extension key. Tracked summary:
`docs/EXTENSION_EXACT_CENTER_CROSS_TEXT.md`.

The `extension_exact_center_final_gate` step combines context, controls, and
cross-text status into one promotion/hold table. Tracked summary:
`docs/EXTENSION_EXACT_CENTER_FINAL_GATE.md`.

The `synthetic_extension_baselines` step compares exact-center NT extension rows
against same-length synthetic Greek strings. Tracked summary:
`docs/SYNTHETIC_EXTENSION_BASELINES.md`.

The `synthetic_extension_match_review` step reviews the synthetic controls that
match or exceed target any-type extension scores. Tracked summary:
`docs/SYNTHETIC_EXTENSION_MATCH_REVIEW.md`.
