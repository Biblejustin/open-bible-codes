# WRR Method Status

Status: current audit matrix; not a WRR reproduction.

This file summarizes what the current local WRR work has locked and what
still needs source or implementation work before any reproduction claim.

## Reproduce

```bash
python3 -m scripts.build_wrr_method_status --text-source reports/wrr_1994/koren_genesis_text_source.csv --pair-summary reports/wrr_1994/wrr2_pair_table_reconciliation_summary.csv --table2-bridge-summary reports/wrr_1994/wrr_table2_source_bridge_summary.csv --table2-ocr-summary reports/wrr_1994/wrr_primary_table2_ocr_probe_summary.csv --table2-row-ocr-summary reports/wrr_1994/wrr_primary_table2_row_ocr_probe_summary.csv --skip-summary reports/wrr_1994/wrr2_skip_caps_summary.csv --corrected-distance-variants reports/wrr_1994/wrr2_corrected_distance_variant_comparison.csv --corrected-distance-aggregate reports/wrr_1994/wrr2_corrected_distance_aggregate.csv --highcap-corrected-distance-summary reports/wrr_1994/highcap_1000/wrr2_corrected_distance_merged_summary.csv --highcap-perturbation-summary reports/wrr_1994/highcap_1000/wrr2_perturbation_diagnostics_summary.csv --highcap-pair-readiness-summary reports/wrr_1994/highcap_1000/wrr2_perturbation_pair_readiness_summary.csv --primary-result-table reports/wrr_1994/wrr_primary_result_table.csv --out reports/wrr_1994/wrr_method_status.csv --markdown-out docs/WRR_METHOD_STATUS.md --manifest-out reports/wrr_1994/wrr_method_status.manifest.json
```

## Matrix

| Area | Status | Current read | Evidence | Next action |
| --- | --- | --- | --- | --- |
| Genesis text stream | `locally_locked` | Koren Genesis stream has stable local fingerprint for smoke work. | 78064 normalized letters; 2075 verses; normalized SHA-256 b26028e02b921fd18a3f5669fa6db38aa500e516926e9f19ad65a6e32ddc3540 | Cross-check against primary WRR text-source statement before claiming reproduction. |
| WRR2 term source | `working_source_locked` | User authorized ANU/McKay WRR2 plain text as the working machine-readable source; it remains secondary-source, not primary-paper ground truth. | 32/32 primary Table 2 English row labels found; 32 secondary records; 0 primary Hebrew cells verified; OCR probe matched 132/205 secondary Hebrew terms (103/174 appellations, 29/31 dates); ocr_probe_not_verification; row OCR probe matched 128/205 row-specific secondary Hebrew terms (99/174 appellations, 29/31 dates); 31 detected row markers; 1 inferred row marker; row_ocr_probe_not_verification; 32 source records; 174 appellations; 31 date rows; 2 undated records skipped | Use this source for working corrected-distance runs while keeping primary/OCR bridge evidence as provenance caveat. |
| Pair universe | `open` | The 163 count is best treated as defined-distance output, not raw pair count. | 182 raw same-record pairs; 165 after appellation length >= 5; 86 in current length 5..8 smoke lane; 163 cited second-list distances; 298 paper-stated candidate word pairs | Derive final pair set from source-backed corrected-distance eligibility, not raw counts alone. |
| D(w) skip-cap formula | `open` | Printed and reported-program formulas are both implemented; final choice remains source decision. | 120 length-filtered rows; 13 program caps below printed; 107 equal caps; 55 rows do not reach target expected hits | Choose printed-paper formula or reported-program formula before final corrected-distance run. |
| Corrected distance c(w,w') | `smoke_only` | Direct perturbed-letter smoke driver now produces defined corrected distances in the current candidate lane, but this remains diagnostic until the pair universe and D(w) formula are locked. | term_printed: 28 defined, term_program: 28 defined, fixed_250: 28 defined; maximum valid perturbation count 125; total defined 84; high-cap 1000 split: 46 defined over 86 pairs, max valid 125; legacy ordinary-hit perturbation diagnostic: 80/120 rows with hits, max row-min exact 2, 80 rows under 10 exact; legacy ordinary-hit pair readiness: 0 ready, 40 missing hits, 46 under exact | Extend direct perturbed search over final pair universe after D(w) and source rows are locked. |
| Aggregate statistic and permutation | `source_locked_not_built` | Published Table 3 ranks are source-audited; local P1..P4 aggregate diagnostics exist, but the date-permutation runner is not built. | Source Table 3: G min P4 rank 4, p0=0.000016; controls: R p0=1.459436, T p0=1.108412, I p0=3.599320, W p0=2.064392, U p0=1.102964, V p0=0.847108; local P1=0.000373062903552, P2=5.981029379e-05, P3=0.000349191888979, P4=7.69538206457e-05 from 28 defined c-values; P3/P4 smaller sample has 22 defined c-values | Implement only after final pair universe and corrected-distance values are locked. |

## Source Anchors

| Topic | Source | Current read |
| --- | --- | --- |
| WRR printed D(w) formula | WRR 1994 Appendix A.4 | Uses a term-specific skip bound chosen so the expected ELS count is 10; printed window count uses (D - 1)(2L - (k - 1)(D + 2)). |
| WRR second-list filtered sample | WRR 1994 Appendix A.3 | Restricts words to length 5..8 for the corrected-distance calculation and reports 298 word pairs before later defined-distance filtering. |
| WRR permutation count | WRR 1994 main text and Appendix A.6 | Uses 999,999 random permutations of the 32 personalities for significance calculations. |
| Program formula mismatch | MBBK 1999 Appendix A | Reports that WRR programs used (D - 1)(2L - (k - 1)D), not the printed WRR 1994 formula. |
| Corrected-distance definedness | MBBK 1999 Appendix A and Gans communities method section | Treats c(w,w') as defined only when the ordinary perturbation is defined and at least 10 perturbation values are defined; MBBK uses greater-than-or-equal ranking while extracted WRR 1994 text has strict greater-than wording in one passage. |
