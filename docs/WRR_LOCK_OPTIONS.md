# WRR Lock Options

Status: decision aid, not a WRR reproduction.

This report does not lock disputed WRR method choices. It separates
current source-backed options from diagnostic shortcuts so the next
run can proceed without silently promoting an open decision.

## Options

| Area | Option | Status | Evidence | Recommendation | Claim boundary |
| --- | --- | --- | --- | --- | --- |
| Pair universe | all imported WRR2 same-record pairs | candidate_input_only | 182 imported same-record pairs; source-cited second-list defined distances = 163; raw imported count does not equal the cited distance count. | Use as the broad working input for diagnostics, not as the final claimed WRR pair universe. | not claim-ready |
| Pair universe | appellation length >= 5 rows | near_count_not_lock | 165 same-record pairs after appellation length filter; 86 after both-side 5..8 filter. | Keep as reconciliation evidence only; this still does not source-lock the final 163 distances. | not claim-ready |
| Pair universe | single Zacut appellation exclusion | diagnostic_only | One length-eligible Zacut appellation exclusion gives 163; all WNP-disputed Zacut appellations would remove 8 pairs. | Do not lock from this alone. The source critique explains a clue, not a WRR exclusion rule. | not claim-ready |
| Pair universe | defined-distance output interpretation | recommended_working_interpretation | The cited 163 is best treated as a corrected-distance output count, not a raw table count. | Next no-input path: compute corrected distances over the broad working input and report the defined set. | still blocked until source and formula locks |
| D(w) skip-cap formula | printed WRR formula | primary_text_default | 120 skip-cap rows; printed formula currently selected in the audit; 55 rows do not reach the expected-hit target. | Keep as the source-facing default because it is the printed WRR formula. | not claim-ready without final pair lock |
| D(w) skip-cap formula | reported WRR-program formula | sensitivity_variant | 13 program caps below printed; 107 equal; defined smoke rows printed/program/fixed250 = 28/28/28. | Carry as a required sensitivity run because MBBK reports the WRR programs used this formula. | not claim-ready without source decision |
| Permutation | repo-defined WNP-excluded 999,999 date-label diagnostic | best_current_diagnostic_not_reproduction | 999999 permutations; 174 observed rows; 48 defined c-values; rho0=0.00086. | Use for local diagnostic evidence while keeping exact WRR reproduction blocked. | diagnostic only |

## Current No-Input Path

Proceed with the broad imported same-record WRR2 pair input, keep the
printed formula as the source-facing default, carry the reported-program
formula as a sensitivity variant, and treat the WNP-excluded 999,999
date-label permutation as diagnostic evidence only.

Claim-grade language still requires a source-locked pair universe, a
source-locked `D(w)` formula decision, full corrected distances over that
locked universe, and a locked aggregate/permutation procedure.
