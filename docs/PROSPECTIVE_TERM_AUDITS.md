# Prospective Term Audits

Status: pre-run guard. This is not a search protocol and does not inspect Bible
texts.

Use the audit before locking a new prospective term list. It checks whether a
candidate term reuses already-seen evidence by normalized Hebrew/Greek spelling.
It catches exact reuse and longer/shorter containment, including cases such as a
future candidate that contains prior `δοξα` (doxa; English: glory).

## Command

```bash
python3 -m scripts.audit_prospective_terms \
  --candidate terms/[new_prospective_terms].csv \
  --evidence reports/greek_expanded_surface_triage/selected_patterns.csv \
  --evidence reports/extension_exact_center_deep_controls_summary.csv \
  --min-normalized-length 5 \
  --out reports/study_locks/new_prospective_term_audit.csv \
  --fail-on-match
```

The script accepts CSV files or directories. Directory inputs are expanded to
all nested `*.csv` files.

## Output

The CSV report writes one row per overlap:

- `block`: exact normalized reuse.
- `review`: substring reuse, where either the candidate contains prior evidence
  or prior evidence contains the candidate.

The sidecar summary is written to `<out>.summary.json` unless `--summary-out` is
provided. A summary with `status = "passed"` means no overlaps were detected.

## Preflight Hook

Require a clean audit during prospective preflight:

```bash
python3 -m scripts.preflight_prospective_study \
  --preregistration docs/[STUDY_PREREGISTRATION].md \
  --manifest reports/study_locks/STUDY.manifest.json \
  --protocol protocols/[study].toml \
  --clean-term-audit reports/study_locks/new_prospective_term_audit.csv.summary.json
```

This fails if the audit summary is missing or has any status other than
`passed`.

## Filtering

After an audit, write a clean candidate file with matched rows removed:

```bash
python3 -m scripts.filter_prospective_terms \
  --candidate terms/[new_prospective_terms].csv \
  --audit reports/study_locks/new_prospective_term_audit.csv \
  --out terms/[new_prospective_terms_clean].csv \
  --min-remaining 10
```

By default this removes both `block` and `review` rows. To remove exact reuse
only and keep substring-overlap rows for manual follow-up, pass
`--drop-severity block`.

## Interpretation

A match does not establish a result is invalid. It means the row is not cleanly new
for prospective discovery language. It can still be used for a confirmatory
follow-up, a known-pattern replication, or a transparent post-discovery review.
