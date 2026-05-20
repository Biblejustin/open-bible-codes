# WRR Method Status

Status: current audit matrix; not a WRR reproduction.

This file summarizes what the current local WRR work has locked and what
still needs source or implementation work before any reproduction claim.

## Reproduce

```bash
python3 -m scripts.build_wrr_method_status --text-source reports/wrr_1994/koren_genesis_text_source.csv --pair-summary reports/wrr_1994/wrr2_pair_table_reconciliation_summary.csv --skip-summary reports/wrr_1994/wrr2_skip_caps_summary.csv --corrected-distance-variants reports/wrr_1994/wrr2_corrected_distance_variant_comparison.csv --out reports/wrr_1994/wrr_method_status.csv --markdown-out docs/WRR_METHOD_STATUS.md --manifest-out reports/wrr_1994/wrr_method_status.manifest.json
```

## Matrix

| Area | Status | Current read | Evidence | Next action |
| --- | --- | --- | --- | --- |
| Genesis text stream | `locally_locked` | Koren Genesis stream has stable local fingerprint for smoke work. | 78064 normalized letters; 2075 verses; normalized SHA-256 b26028e02b921fd18a3f5669fa6db38aa500e516926e9f19ad65a6e32ddc3540 | Cross-check against primary WRR text-source statement before claiming reproduction. |
| WRR2 term source | `secondary_source_imported` | ANU/McKay WRR2 plain text is imported for audit, not treated as primary-paper ground truth. | 32 source records; 174 appellations; 31 date rows; 2 undated records skipped | Cross-check imported spellings and dates against primary paper table or citable transcription. |
| Pair universe | `open` | The 163 count is best treated as defined-distance output, not raw pair count. | 182 raw same-record pairs; 165 after appellation length >= 5; 86 in current length 5..8 smoke lane; 163 cited second-list distances; 298 paper-stated candidate word pairs | Derive final pair set from source-backed corrected-distance eligibility, not raw counts alone. |
| D(w) skip-cap formula | `open` | Printed and reported-program formulas are both implemented; final choice remains source decision. | 120 length-filtered rows; 13 program caps below printed; 107 equal caps; 55 rows do not reach target expected hits | Choose printed-paper formula or reported-program formula before final corrected-distance run. |
| Corrected distance c(w,w') | `smoke_only` | Smoke driver exists, but current candidate lane produces no defined corrected distances. | term_printed: 0 defined, term_program: 0 defined, fixed_250: 0 defined; maximum valid perturbation count 4; total defined 0 | Optimize and rerun over final pair universe after D(w) and source rows are locked. |
| Aggregate statistic and permutation | `not_built` | P1/P2 arithmetic helpers exist, but no claim-grade P1..P4 or date-permutation runner exists. | No current protocol step computes full WRR aggregate scores or permutation ranks from defined c-values. | Implement only after final pair universe and corrected-distance values are locked. |
