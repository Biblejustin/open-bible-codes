# Report Database

Status: optional analytics backend for large ignored report artifacts.

Some dense hit-level CSVs are now large enough that repeated CSV scans are the
wrong working format. The broad CRD classified-hit outputs are currently about
5.3 GB each, and the Hebrew all-codes surface table is about 946 MB. Final
reader-facing summaries remain CSV and Markdown, but dense/intermediate tables
can be imported into DuckDB for faster filtering, grouping, and review-queue
generation.

The default import also includes word-count and morphology-count outputs. These
are not huge individually, but together they currently add about 1.9 million
rows and are much easier to compare, filter by multiple, and join from DuckDB
than by repeatedly scanning CSVs.

The expanded post-search strata outputs are also imported by default. They are
small today, but keeping them in DuckDB makes final-report audit joins consistent
with the larger CRD, all-codes, matrix-cluster, and passage-gap tables.

## Install

DuckDB is optional. The command-line DuckDB installed by Homebrew is useful, but
the Python scripts use the Python package:

```bash
python3 -m pip install --user --break-system-packages duckdb
```

In a virtual environment, use:

```bash
python3 -m pip install '.[analytics]'
```

## Build

```bash
make report-db
```

Default database:

```text
reports/db/open_bible_codes.duckdb
```

The database is ignored by git. It can be rebuilt from ignored report CSVs.
DB-backed report commands verify the imported source size and mtime before
querying. If a source CSV changed after import, rebuild with `make report-db`.
The import command is idempotent: tables whose source size and mtime already
match the import metadata are reported as `current` and skipped.

To reimport every configured table even when metadata is current:

```bash
python3 -m scripts.build_report_db --skip-missing --force
```

## Default Imported Tables

- `crd_self_surface_classified_hits`
- `crd_self_surface_density_matrix`
- `crd_concept_surface_classified_hits`
- `crd_concept_surface_density_matrix`
- `crd_classified_hits`
- `crd_density_matrix`
- `hebrew_screening_surface_all_codes`
- `hebrew_screening_surface_all_codes_summary`
- `english_screening_surface_all_codes`
- `english_screening_surface_all_codes_summary`
- `greek_screening_surface_all_codes`
- `greek_screening_surface_all_codes_summary`
- `hebrew_theology_surface_all_codes`
- `hebrew_theology_surface_all_codes_summary`
- `dynamic_skip_focus_full_span_exported_hits`
- `matrix_cluster_candidates`
- `matrix_cluster_summary`
- `matrix_cluster_relation_control_summary`
- `matrix_cluster_term_pair_control_summary`
- `notable_passage_gap_detail`
- `notable_passage_gap_passage_summary`
- `notable_passage_gap_cross_source_summary`
- `thematic_chapter_absence_detail`
- `thematic_chapter_absence_passage_summary`
- `thematic_chapter_absence_cross_source_summary`
- `match_strata_occurrence_strata`
- `match_strata_summary`
- `boundary_alignment_summary`
- `chapter_position_bias_summary`
- `direction_asymmetry_summary`
- `direction_asymmetry_term_summary`
- `canonical_first_summary`
- `canonical_first_occurrences`
- `cross_skip_summary`
- `cross_skip_candidate_rows`
- `review_flag_summary`
- `review_flag_rows`
- `cohort_cluster_density_windows`
- `cohort_cluster_density_summary`
- `word_counts_by_word`
- `word_counts_by_book`
- `word_counts_by_chapter`
- `word_counts_by_verse`
- `word_count_multiples`
- `morph_counts_by_lemma`
- `morph_counts_by_book`
- `morph_counts_by_chapter`
- `morph_counts_by_verse`
- `morph_count_multiples`

## DB-Backed Commands

The CRD follow-up commands can read dense classified-hit rows from DuckDB and
still write the existing CSV outputs. The Make targets below use DuckDB when
`reports/db/open_bible_codes.duckdb` exists and fall back to the original CSV
scan when it does not. Run `make report-db` first, then run the follow-up target
in a separate `make` invocation to use the fast path.

The all-codes summary and triage scripts also auto-detect a current default DB
for standard report paths. Use `--no-db` on those scripts when comparing against
the original CSV-only path.

```bash
make crd-self-surface-report
make crd-self-surface-queue
make crd-self-surface-center-word
make crd-self-surface-center-word-density
make crd-self-surface-center-word-queue
make crd-self-surface-center-word-packet
make crd-self-surface-center-word-presence
make crd-concept-surface-report
make crd-concept-surface-queue
make crd-concept-surface-center-word
make crd-concept-surface-center-word-density
make crd-concept-surface-center-word-queue
make crd-concept-surface-center-word-packet
make crd-concept-surface-center-word-presence
make crd-center-word-findings
```

For ad hoc import:

```bash
python3 -m scripts.build_report_db --table reports/example/hits.csv:example_hits
```

For DB-backed all-codes collection summaries:

```bash
python3 -m scripts.summarize_surface_all_codes \
  --hits reports/hebrew_screening_all_codes/surface_all_codes.csv \
  --summary reports/hebrew_screening_all_codes/surface_all_codes_summary.csv \
  --db reports/db/open_bible_codes.duckdb \
  --hits-table hebrew_screening_surface_all_codes \
  --summary-table hebrew_screening_surface_all_codes_summary
```

For DB-backed all-codes triage:

```bash
python3 -m scripts.triage_surface_all_codes \
  --hits reports/hebrew_screening_all_codes/surface_all_codes.csv \
  --summary reports/hebrew_screening_all_codes/surface_all_codes_summary.csv \
  --db reports/db/open_bible_codes.duckdb \
  --hits-table hebrew_screening_surface_all_codes
```

For DB-backed dynamic full-span hit findings:

```bash
make dynamic-full-span-hit-findings
```

Equivalent direct command:

```bash
python3 -m scripts.summarize_dynamic_span_hits \
  --db reports/db/open_bible_codes.duckdb \
  --hits-table dynamic_skip_focus_full_span_exported_hits
```

For ad hoc SQL:

```bash
duckdb reports/db/open_bible_codes.duckdb
```

The report index uses current DB import metadata for large CSV row counts and a
local `reports/.report_index_cache.json` size/mtime cache for medium CSVs. It
also excludes operational partition, worker-batch, worker-import, and DB folders
from the reader-facing report index.

## Policy

- Keep report summaries in CSV/Markdown for portability.
- Use DuckDB for dense hit tables, repeated joins, filters, and group-bys.
- Keep DB files under `reports/db/`; do not commit them.
- Rebuild DB files from CSV when switching machines or restoring artifacts.
