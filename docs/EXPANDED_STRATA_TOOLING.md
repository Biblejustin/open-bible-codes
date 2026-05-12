# Expanded Strata Tooling

This guide maps the expanded ELS match strata to the current repository tools.
It is an operator guide, not a claim report. Running one of these tools widens
or annotates the review surface; it does not promote any row to claim language
without a locked protocol, matched controls, and correction for the tested
family.

## Post-Search Metadata

These strata annotate existing centered occurrence rows. They do not perform a
new ELS search by themselves.

```bash
python3 -m scripts.run_protocol protocols/match_strata_index.toml --resume
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

## Transformed Hebrew Text

Atbash and ALBAM are opt-in deterministic transform layers. They search a
transformed letter stream while preserving original corpus offsets and surface
references.

```bash
python3 -m scripts.run_protocol protocols/hebrew_atbash_audit.toml --resume
python3 -m scripts.run_protocol protocols/hebrew_albam_audit.toml --resume
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

```bash
python3 -m scripts.build_cipher_layered_pairs \
  --plain-hits reports/plain_hits.csv \
  --cipher-hits reports/hebrew_atbash_audit/MT_WLC_hits.csv \
  --out reports/cipher_layered_pairs/pairs.csv \
  --summary-out reports/cipher_layered_pairs/summary.csv \
  --manifest-out reports/cipher_layered_pairs/manifest.json
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

Primary outputs:

- `reports/word_edge_patterns/*_hits.csv`
- `reports/word_edge_patterns/summary.csv`
- `reports/word_edge_patterns/summary.manifest.json`
- `docs/WORD_EDGE_PATTERN_AUDIT.md`

Current support is word-edge letter paths, not full token-level every-Kth-word
ELS. Full word-token ELS remains a separate definition problem.

## Matrix Cluster Candidates

Matrix candidate extraction maps hit paths into a wrapped text matrix and
records nearest-cell relations between declared cohort terms.

```bash
python3 -m scripts.build_matrix_cluster_candidates \
  --hits reports/centered_occurrence_index/centered_occurrences.csv \
  --width 50 \
  --max-cell-distance 1 \
  --out reports/matrix_clusters/candidates.csv \
  --summary-out reports/matrix_clusters/summary.csv \
  --manifest-out reports/matrix_clusters/manifest.json
```

The output labels nearest-cell relation as `same_cell`, `orthogonal`,
`diagonal`, or `neighborhood`. Width and distance are study-defining choices;
claim-grade use requires those values to be locked before looking at results
and repeated on matched controls.

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
