# Study Mapping Schemas

Status: planning infrastructure. This document defines where future
interpretive mapping files live and how they are checked before use. It does
not populate any theological, authorial, quotation, or semantic-divergence
assignments.

## Files

Header-only templates live under `data/study/mappings/`:

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

## Validation

Run:

```bash
python3 -m scripts.validate_study_mapping_schemas
```

or:

```bash
make study-mapping-schemas
```

Header-only files pass so planning can remain public without implying content.
Once rows are added, the validator checks required columns, non-empty lock
fields, unique `mapping_id` values, supported language labels, and ordered
chapter ranges.

## Lock Rule

A populated mapping file must be included in the study lock manifest and
preregistration before any density, promotion, or claim-level language uses it.
If a populated mapping changes after results are inspected, the run is invalid
for prospective claim language and needs a new lock.
