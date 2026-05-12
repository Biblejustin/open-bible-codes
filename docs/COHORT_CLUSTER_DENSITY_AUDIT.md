# Cohort Cluster Density Audit

Status: post-search review aid, not claim promotion.

This report finds centered hits from a declared cohort that land inside
a fixed word window in the same corpus. Cohort choice and window size are
study-defining inputs and require matched controls for claim language.

## Settings

- Occurrences: `reports/centered_occurrence_index/centered_occurrences.csv`
- Cohorts: `terms/biblical_tribes.csv`
- Window words: `50`
- Minimum distinct terms: `2`
- Candidate windows: `0`

## Summary

No windows met the declared threshold.

## Candidate Windows

No candidate windows were produced.

## Caution

A cohort-window row is a review prioritization signal. It must be
rerun against language-matched controls with the same cohort, same
window width, same centered-occurrence source, and the same correction
family before it can support comparative claims.
