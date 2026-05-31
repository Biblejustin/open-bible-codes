# Study Mapping Schemas

Status: planning infrastructure. This document defines where future
interpretive mapping files live and how they are checked before use. It does
not populate any theological, authorial, quotation, or semantic-divergence
assignments.

## Files

Study mapping files live under `data/study/mappings/`:

- `thematic_chapters.csv`: term-to-chapter windows for
  `canonical_first_in_thematic_chapter` and
  `term_absence_at_thematic_chapter`.
- `author_book_mapping.csv`: author-name terms to attributed book or scope
  windows for `author_in_own_book`.
- `protagonist_narrative_mapping.csv`: protagonist terms to declared narrative
  windows for `protagonist_in_own_narrative`.
- `ot_in_nt_quotations.csv`: OT quotation spans, NT quotation spans, and anchor
  text for `nt_quotation_anchor` and `nt_quotation_span`.
- `mt_lxx_semantic_divergence.csv`: locked MT/LXX divergence anchors for
  `lxx_vs_mt_semantic_divergence`.
- `hebrew_root_policy.csv`: locked surface-form to root assignments for
  `root_only_match`. This is a policy file, not a root analyzer; it records
  which analyzer/source and root scheme the matcher is allowed to use.
- `wrr_manual_decision_records.csv`: populated lock ledger for current WRR
  manual decisions. It records decision rank, lane, target, source checklist,
  selected action, evidence citation, evidence summary, and reviewer lock
  fields. Current rows lock 26 `no_source_change` decisions and 11
  `method_lock` decisions without selecting source correction, row
  transcription, replacement lock, or pair exclusion.

## Validation

Run:

```bash
python3 -m scripts.validate_study_mapping_schemas
python3 -m scripts.check_wrr_manual_decision_records
python3 -m scripts.check_cities_ocr_page_review_decisions
python3 -m scripts.check_cities_source_row_lock_decision_records
python3 -m scripts.check_cities_source_transcription_decision_records
```

or:

```bash
make study-mapping-schemas
```

Header-only files pass so planning can remain public without implying content.
Populated files must also pass exact-column and non-empty lock-field checks,
unique `mapping_id` values where applicable, supported language labels, ordered
chapter ranges, scoped refs that match the declared book, ordered scoped-ref
ranges, and ISO `locked_at` dates.

For `wrr_manual_decision_records.csv`, the row-level checker also requires each
populated decision row to match the current WRR manual decision register by
rank, lane, state, target, and checklist, with non-placeholder evidence and an
ISO lock date.

For the Cities mapping files, the row-level checkers keep the current public
boundary explicit. OCR page decisions must remain tied to the OCR review packet
and must keep `no_source_row_import`; source-row lock decisions must remain tied
to the evidence packet; transcription decisions must stay schema-only until a
readable source row is deliberately locked.

## Lock Rule

A populated mapping file must be included in the study lock manifest and
preregistration before any density, promotion, or claim-grade language uses it.
If a populated mapping changes after results are inspected, the run is invalid
for prospective claim language and needs a new lock.
