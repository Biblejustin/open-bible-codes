# WRR Locked Method Report

Status: locked local WRR method report; not an exact published WRR reproduction.

This report is the compact handoff for the selected local WRR policy. It
records what is locked, what the selected-policy run reports, and where
exact published WRR reproduction remains outside the current evidence.

## Reproduce

```bash
python3 -m scripts.build_wrr_locked_method_report --method-status reports/wrr_1994/wrr_method_status.csv --readiness reports/wrr_1994/wrr_claim_readiness.csv --lock-options reports/wrr_1994/wrr_lock_options.csv --manual-worksheet reports/wrr_1994/wrr_manual_decision_record_worksheet.csv --corrected-distance-summary reports/wrr_1994/direct_all/highcap_1000/wrr2_corrected_distance_all_lanes_merged_summary.csv --corrected-distance-aggregate reports/wrr_1994/direct_all/highcap_1000/wrr2_corrected_distance_all_lanes_aggregate.csv --permutation-summary reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_permutations_999999_summary.csv --primary-result-table reports/wrr_1994/wrr_primary_result_table.csv --defined-pair-summary reports/wrr_1994/wrr_defined_pair_set_audit_summary.csv --out reports/wrr_1994/wrr_locked_method_report.csv --markdown-out docs/WRR_LOCKED_METHOD_REPORT.md --manifest-out reports/wrr_1994/wrr_locked_method_report.manifest.json
```

## Selected Locks

| Lock | Status | Evidence |
| --- | --- | --- |
| Pair universe: keep_all_working_source | `source_locked` | 182 imported same-record pairs; source-cited second-list defined distances = 163; raw imported count does not equal the cited distance count. |
| D(w): printed WRR formula main; reported-program formula sensitivity | `source_locked` | 120 skip-cap rows; printed formula currently selected in the audit; 55 rows do not reach the expected-hit target. |
| Corrected distance: full selected universe cap1000; undefined ordinary-not-valid | `defined_full_run` | term_printed: 28 defined, term_program: 28 defined, fixed_250: 28 defined; maximum valid perturbation count 125; total defined 84; full all-lane cap 1000 run: 72 defined over 182 selected pairs, 110 ordinary-not-valid, 0 under-minimum, max valid 125; status diagnostic_only_not_wrr_reproduction; legacy ordinary-hit perturbation diagnostic: 80/120 rows with hits, max row-min exact 2, 80 rows under 10 exact; legacy ordinary-hit pair readiness: 0 ready, 40 missing hits, 46 under exact |
| Permutation: 999,999 date-label shuffles | `permutation_locked` | 999999 permutations; 182 observed rows; 72 defined c-values; rho0=0.000404. |
| Manual decisions: 37 locked rows: 26 no_source_change; 11 method_lock | `locked` | Manual worksheet rows counted by selected action. |

## Main Local Result

| Metric | Value |
| --- | --- |
| Observed rows | 182 |
| Defined c-values | 72 |
| Ordinary-not-valid rows | 110 |
| P1 | 0.00252257011468 |
| P2 | 1.16472976875e-05 |
| P3 | 0.0184584022574 |
| P4 | 0.000274264355592 |
| rho P1 | 0.019722 |
| rho P2 | 0.000101 |
| rho P3 | 0.0506065 |
| rho P4 | 0.000535 |
| rho0 | 0.000404 |

## Published Anchor

- Primary Table 3 Genesis anchor: min statistic P4; rank 4; p0=0.000016.
- This anchor is shown for comparison only. The local selected-policy run is not an exact published WRR reproduction.

## Exact Published WRR Boundary

- Exact published WRR reproduction remains caveated by the source-defined 163-distance gap and primary-source transcription limits.
- Current source-defined gap: defined 72 of 163; gap 91.
- Source-review and visual-review flags remain diagnostic unless a separate manual source-policy record changes them.
- Do not describe this as an exact published WRR reproduction.

## Allowed Language

- Locked local WRR method report under keep_all_working_source.
- Repo-defined selected-policy result with printed D(w) as main and reported-program D(w) as sensitivity.
- Exact published WRR reproduction remains caveated.

## Forbidden Language

- exact published WRR reproduced
- proves WRR
- source correction selected

## Readiness Gate

| Area | Ready | Status | Read |
| --- | --- | --- | --- |
| Pair universe | `true` | `source_locked` | User selected keep_all_working_source: all imported WRR2 same-record pairs remain the working candidate universe; visual/source-review flags do not exclude pairs automatically, and 163 remains a defined-distance output target rather than a raw pair count. |
| D(w) skip-cap formula | `true` | `source_locked` | User selected the printed WRR formula as the main skip-cap rule; the reported WRR-program formula remains required sensitivity output. |
| Corrected distance c(w,w') | `true` | `defined_full_run` | Full selected keep_all_working_source corrected-distance output exists for all imported same-record pairs using printed D(w); undefined rows remain ordinary-not-valid rather than missing work. |
| Aggregate statistic and permutation | `true` | `permutation_locked` | Full selected-universe cap1000 aggregate/permutation is locked under the repo policy: keep_all_working_source, printed D(w), and 999,999 date-label shuffles. This supports locked-method local evidence, not an exact published WRR reproduction claim. |
