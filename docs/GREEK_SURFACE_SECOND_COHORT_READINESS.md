# Greek Surface Second Cohort Readiness

Status: blocked pending genuinely new terms. This is not a result-producing
search.

## Purpose

This note checks whether the existing expanded Greek prospective term pool can
support a second clean exact-center surface prospective cohort after the first
locked Greek surface prospective run.

The answer is no under the current length >= 5 prospective standard.

## Audit Commands

Selected-evidence-only audit:

```bash
python3 -m scripts.audit_prospective_terms \
  --candidate terms/greek_expanded_prospective_terms.csv \
  --evidence reports/greek_exact_center_final_gate/summary.csv \
  --evidence reports/greek_expanded_surface_triage/selected_patterns.csv \
  --evidence reports/greek_surface_prospective/selected_patterns.csv \
  --evidence reports/greek_surface_length4_followup/selected_patterns.csv \
  --evidence reports/greek_screening_all_codes/triage_queue.csv \
  --evidence reports/all_codes_followup_selection/selected_rows.csv \
  --min-normalized-length 5 \
  --out reports/study_locks/greek_surface_second_cohort_audit.csv
```

Full-prior audit, including the previously tested Greek surface cohort:

```bash
python3 -m scripts.audit_prospective_terms \
  --candidate terms/greek_expanded_prospective_terms.csv \
  --evidence reports/greek_surface_prospective/term_summary.csv \
  --evidence reports/greek_surface_prospective/term_cohort.csv \
  --evidence reports/greek_surface_prospective/surface_patterns.csv \
  --evidence reports/greek_exact_center_final_gate/summary.csv \
  --evidence reports/greek_expanded_surface_triage/selected_patterns.csv \
  --evidence reports/greek_surface_length4_followup/selected_patterns.csv \
  --evidence reports/greek_screening_all_codes/triage_queue.csv \
  --evidence reports/all_codes_followup_selection/selected_rows.csv \
  --min-normalized-length 5 \
  --out reports/study_locks/greek_surface_second_cohort_full_prior_audit.csv
```

Strict filter:

```bash
python3 -m scripts.filter_prospective_terms \
  --candidate terms/greek_expanded_prospective_terms.csv \
  --audit reports/study_locks/greek_surface_second_cohort_full_prior_audit.csv \
  --out reports/study_locks/greek_surface_second_cohort_full_prior.filtered.csv \
  --min-normalized-length 5 \
  --min-remaining 10
```

## Audit Read

Selected-evidence-only audit:

- candidate rows at length >= 5: 265
- skipped short rows: 26
- overlap rows: 454
- exact/block overlap rows: 28
- review/substring overlap rows: 426
- unique candidate terms with prior selected-evidence overlap: 25
- filtered rows before enforcing length: 266

Full-prior audit:

- candidate rows at length >= 5: 265
- skipped short rows: 26
- evidence values: 1256
- overlap rows: 800
- exact/block overlap rows: 317
- review/substring overlap rows: 483
- unique candidate terms with full-prior overlap: 265

Strict filter after full-prior audit:

- input rows: 291
- dropped by audit overlap: 265
- dropped as short rows under length >= 5: 26
- output rows: 0
- filter status: failed because `0 < min_remaining 10`

## Conclusion

The existing expanded Greek prospective term pool cannot support a second clean
length >= 5 prospective cohort. Every length >= 5 row was already tested or
overlaps prior evidence once the first Greek surface prospective run is treated
as prior evidence.

The 26 rows left by an older filter run were all length-4 rows. They belong in
the already documented length-4 post-discovery lane, not in a new length >= 5
prospective cohort.

## Next Valid Move

A second Greek surface prospective cohort requires a genuinely new term source
before lock:

- a new source term file not derived from `terms/greek_expanded_prospective_terms.csv`;
- clean `scripts.audit_prospective_terms` result against prior Greek exact-center
  and all-codes evidence;
- fixed length threshold, source set, skip range, direction, controls, and
  correction method;
- preregistration, lock manifest, and preflight before any result-producing run.

Until that exists, the next result-producing work should use another lane from
`docs/PROSPECTIVE_STUDY_READINESS.md`.
