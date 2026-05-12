# Expanded Strata Tooling

This guide maps the expanded ELS match strata to the current repository tools.
It is an operator guide, not a claim report. Running one of these tools widens
or annotates the review surface; it does not promote any row to claim language
without a locked protocol, matched controls, and correction for the tested
family.

Check that this guide and its Makefile shortcuts still point at live tools with:

```bash
make expanded-strata-tooling-check
```

Run the post-search expanded-strata chain in dependency order with:

```bash
make expanded-strata-postprocess
```

## Post-Search Metadata

These strata annotate existing centered occurrence rows. They do not perform a
new ELS search by themselves.

```bash
python3 -m scripts.run_protocol protocols/match_strata_index.toml --resume
```

Shortcut:

```bash
make match-strata-index
```

Primary outputs:

- `reports/match_strata_index/occurrence_strata.csv`
- `reports/match_strata_index/strata_summary.csv`
- `reports/match_strata_index/manifest.json`

Current coverage:

- boundary endpoint flags
- first/last verse-in-chapter and verse-in-book flags
- forward-only, backward-only, and bidirectional direction strata
- canonical first occurrence within the centered occurrence family
- same-center cross-skip pair flags
- meaningful-constant skip flags
- term-gematria and center-word-gematria skip flags
- letter-frequency and bigram-surprise metadata

## Boundary Alignment

Boundary alignment summarizes whether ELS path starts and ends align with
verse, chapter, or book boundaries. It does not run a new ELS search.

Primary protocol: `protocols/boundary_alignment.toml`

```bash
python3 -m scripts.run_protocol protocols/boundary_alignment.toml --resume
```

Shortcut:

```bash
make boundary-alignment
```

Primary outputs:

- `reports/boundary_alignment/summary.csv`
- `docs/BOUNDARY_ALIGNMENT.md`
- `reports/boundary_alignment/manifest.json`

## Chapter Position Bias

Chapter-position bias summarizes the first/last chapter and book center-verse
flags from the match-strata index. It does not run a new ELS search.

Primary protocol: `protocols/chapter_position_bias.toml`

```bash
python3 -m scripts.run_protocol protocols/chapter_position_bias.toml --resume
```

Shortcut:

```bash
make chapter-position-bias
```

Primary outputs:

- `reports/chapter_position_bias/summary.csv`
- `docs/CHAPTER_POSITION_BIAS.md`
- `reports/chapter_position_bias/manifest.json`

## Direction Asymmetry

Direction asymmetry summarizes whether each term/corpus group is forward-only,
backward-only, or present in both directions. It does not run a new ELS search.

Primary protocol: `protocols/direction_asymmetry.toml`

```bash
python3 -m scripts.run_protocol protocols/direction_asymmetry.toml --resume
```

Shortcut:

```bash
make direction-asymmetry
```

Primary outputs:

- `reports/direction_asymmetry/summary.csv`
- `reports/direction_asymmetry/term_summary.csv`
- `docs/DIRECTION_ASYMMETRY.md`
- `reports/direction_asymmetry/manifest.json`

## Canonical First Summary

Canonical-first summary lists the first centered occurrence of each term/corpus
group in canonical order, using the flag already produced by the match-strata
index. It does not run a new ELS search.

Primary protocol: `protocols/canonical_first_summary.toml`

```bash
python3 -m scripts.run_protocol protocols/canonical_first_summary.toml --resume
```

Shortcut:

```bash
make canonical-first-summary
```

Primary outputs:

- `reports/canonical_first_summary/summary.csv`
- `reports/canonical_first_summary/first_occurrences.csv`
- `docs/CANONICAL_FIRST_SUMMARY.md`
- `reports/canonical_first_summary/manifest.json`

## Cross-Skip Summary

Cross-skip summary lists centered rows where another declared term appears at
the same center word, at a shared hidden-letter position, or within the
configured endpoint-letter distance at a different skip. It uses the flags
already produced by the match-strata index and does not run a new ELS search.

Primary protocol: `protocols/cross_skip_summary.toml`

```bash
python3 -m scripts.run_protocol protocols/cross_skip_summary.toml --resume
```

Shortcut:

```bash
make cross-skip-summary
```

Primary outputs:

- `reports/cross_skip_summary/summary.csv`
- `reports/cross_skip_summary/candidate_rows.csv`
- `docs/CROSS_SKIP_SUMMARY.md`
- `reports/cross_skip_summary/manifest.json`

## Review Flag Summary

Review-flag summary unpivots meaningful-skip, gematria-skip,
bigram-surprise, and letter-frequency anomaly flags from the match-strata
index. It does not run a new ELS search.

Primary protocol: `protocols/review_flag_summary.toml`

```bash
python3 -m scripts.run_protocol protocols/review_flag_summary.toml --resume
```

Shortcut:

```bash
make review-flag-summary
```

Primary outputs:

- `reports/review_flag_summary/summary.csv`
- `reports/review_flag_summary/flag_rows.csv`
- `docs/REVIEW_FLAG_SUMMARY.md`
- `reports/review_flag_summary/manifest.json`

## Thematic Chapter Absence

The notable-passage gap analyzer can run only locked
`data/study/mappings/thematic_chapters.csv` targets. Each generated passage is
filtered to its mapped term, so this is a term-to-chapter absence screen rather
than an all-terms/all-passages sweep.

```bash
python3 -m scripts.run_protocol protocols/thematic_chapter_absence.toml --resume
```

Shortcut:

```bash
make thematic-chapter-absence
```

Primary outputs:

- `reports/thematic_chapter_absence/term_gap_detail.csv`
- `reports/thematic_chapter_absence/passage_summary.csv`
- `reports/thematic_chapter_absence/cross_source_gap_summary.csv`
- `reports/thematic_chapter_absence/manifest.json`
- `docs/THEMATIC_CHAPTER_ABSENCE.md`

## Transformed Hebrew Text

Atbash and ALBAM are opt-in deterministic transform layers. They search a
transformed letter stream while preserving original corpus offsets and surface
references.

```bash
python3 -m scripts.run_protocol protocols/hebrew_atbash_audit.toml --resume
python3 -m scripts.run_protocol protocols/hebrew_albam_audit.toml --resume
```

Shortcuts:

```bash
make hebrew-atbash-audit
make hebrew-albam-audit
```

Primary outputs:

- `reports/hebrew_atbash_audit/summary.csv`
- `docs/HEBREW_ATBASH_AUDIT.md`
- `reports/hebrew_albam_audit/summary.csv`
- `docs/HEBREW_ALBAM_AUDIT.md`

Transform-layer rows must be compared with the same transform applied to
language-matched controls before any Bible-vs-control language is used.

## Cipher Layered Pairs

Cipher layered pairs compare ordinary ELS rows and transformed-layer ELS rows
at the same declared anchor.

Primary tool path: `scripts/build_cipher_layered_pairs.py`

```bash
python3 -m scripts.build_cipher_layered_pairs \
  --plain-hits reports/plain_hits.csv \
  --cipher-hits reports/hebrew_atbash_audit/MT_WLC_hits.csv \
  --out reports/cipher_layered_pairs/pairs.csv \
  --summary-out reports/cipher_layered_pairs/summary.csv \
  --manifest-out reports/cipher_layered_pairs/manifest.json
```

Shortcut:

```bash
make cipher-layered-pairs
```

Default anchor fields are corpus label, term id, center reference, and center
normalized word. Use repeated `--anchor-field` arguments only in a locked
protocol. The manifest records the anchor fields and row counts so downstream
reports can audit the pairing rule.

## Word-Edge Patterns

The word-edge scanner supports acrostic and telestic searches over first or
last letters of surface words, including optional word skips.

```bash
python3 -m scripts.run_protocol protocols/word_edge_pattern_audit.toml --resume
```

Shortcut:

```bash
make word-edge-pattern-audit
```

Primary outputs:

- `reports/word_edge_patterns/*_hits.csv`
- `reports/word_edge_patterns/summary.csv`
- `reports/word_edge_patterns/summary.manifest.json`
- `docs/WORD_EDGE_PATTERN_AUDIT.md`

## Word-Skip Term Patterns

The word-skip term scanner supports full normalized surface-word-token phrases
at every `K`th word. It is separate from word-edge acrostic/telestic scanning
and widens the search surface.

```bash
python3 -m scripts.run_protocol protocols/word_skip_term_audit.toml --resume
```

Shortcut:

```bash
make word-skip-term-audit
```

Primary outputs:

- `reports/word_skip_terms/*_hits.csv`
- `reports/word_skip_terms/summary.csv`
- `reports/word_skip_terms/summary.manifest.json`
- `docs/WORD_SKIP_TERM_AUDIT.md`

## Matrix Cluster Candidates

Matrix candidate extraction maps hit paths into a wrapped text matrix and
records nearest-cell relations between declared cohort terms.

Primary protocol: `protocols/matrix_cluster_candidates.toml`

```bash
python3 -m scripts.run_protocol protocols/matrix_cluster_candidates.toml --resume
```

Shortcut:

```bash
make matrix-cluster-candidates
```

The default protocol uses `reports/crd/classified_hits.csv` after the locked
CRD run, because that file now retains raw path offsets for Bible editions and
language-matched secular controls. It locks `--row-width 50` with
`--max-cell-distance 1`. Matrix input rows must include enough path detail to
reconstruct letter cells: `sequence`, `start_offset`, and `skip`, or extension-style
`extended_sequence`, `extension_start_offset`, and `skip`. Add
`--require-parsed-hits` for locked runs so a missing path-detail column fails
instead of writing an empty candidate file. The manifest records input rows,
parsed hit rows, and skipped input rows.

The output labels nearest-cell relation as `same_cell`, `orthogonal`,
`diagonal`, or `neighborhood`. Width and distance are study-defining choices;
claim-grade use requires those values to be locked before looking at results
and repeated on matched controls.

Primary outputs:

- `reports/matrix_clusters/candidates.csv`
- `reports/matrix_clusters/summary.csv`
- `docs/MATRIX_CLUSTER_CANDIDATES.md`
- `reports/matrix_clusters/manifest.json`

Relation-specific control summary protocol:
`protocols/matrix_cluster_control_summary.toml`

```bash
python3 -m scripts.run_protocol protocols/matrix_cluster_control_summary.toml --resume
```

Shortcut:

```bash
make matrix-cluster-control-summary
```

This summary does not run a new search. It reads the matrix candidate CSV and
the same CRD hit file used to build those candidates, then compares same-cell,
orthogonal, diagonal, and neighborhood candidate counts between Bible editions
and secular controls. It reports both per-corpus ratios and opportunity ratios
normalized by the possible cross-term pair denominator. These are review aids
only; they are not p-values and do not promote a candidate to a claim.

Primary outputs:

- `reports/matrix_clusters/relation_control_summary.csv`
- `reports/matrix_clusters/term_pair_control_summary.csv`
- `docs/MATRIX_CLUSTER_CONTROL_SUMMARY.md`
- `reports/matrix_clusters/control_summary.manifest.json`

## Cohort Cluster Density

Cohort cluster density finds centered hits from a declared term file that land
within a word window in the same corpus. It uses existing centered occurrence
rows and does not run a new ELS search.

Primary tool path: `scripts/build_cohort_cluster_density.py`

```bash
python3 -m scripts.build_cohort_cluster_density \
  --occurrences reports/centered_occurrence_index/centered_occurrences.csv \
  --cohort terms/biblical_tribes.csv \
  --window-words 50 \
  --min-distinct-terms 2 \
  --out reports/cohort_cluster_density/windows.csv \
  --summary-out reports/cohort_cluster_density/summary.csv \
  --markdown-out docs/COHORT_CLUSTER_DENSITY_AUDIT.md \
  --manifest-out reports/cohort_cluster_density/manifest.json
```

Shortcut:

```bash
make cohort-cluster-density
```

Protocol wrapper:

```bash
python3 -m scripts.run_protocol protocols/cohort_cluster_density_audit.toml --resume
```

The default Makefile target uses `terms/biblical_tribes.csv` only as a concrete
declared cohort and supplies the common corpus config mappings needed to resolve
center refs to global word ordinals. If an occurrence file already includes
`center_word_ordinal`, direct script calls can omit `--corpus-config`.
Override `COHORT_CLUSTER_TERMS`, `COHORT_CLUSTER_WINDOW_WORDS`, and
`COHORT_CLUSTER_MIN_DISTINCT` for a locked study. Rows are review candidates
only; cohort choice and window width are study-defining inputs.

## Mapping-Dependent Strata

The following strata have schema support but no committed theological or
interpretive assignments:

- canonical first occurrence in a thematic chapter
- author in own book
- protagonist in own narrative
- OT-in-NT quotation anchors
- MT/LXX semantic divergence

Header-only templates live under `data/study/mappings/`. Validate them with:

```bash
python3 -m scripts.validate_study_mapping_schemas
```

or:

```bash
make study-mapping-schemas
```

Populated mapping files must be locked in a preregistration before they drive
density, promotion, or claim-level language.

## Suggested Review Order

1. Run `match_strata_index` over existing centered occurrence rows.
2. Review transformed-text audits separately from ordinary ELS rows.
3. Use cipher layered pairs only after the plain and transform hit files are
   generated under a declared anchor rule.
4. Treat word-edge and matrix candidates as expanded search families with their
   own controls.
5. Populate mapping-dependent files only through a locked study workflow.
