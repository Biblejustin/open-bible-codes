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
| Pair universe | WNP/context flagged source-review queue | diagnostic_source_review_context | Source-review queue flags 5 WNP/context queued terms: 1 wnp_book_title_appellation_dispute, 2 wnp_chelm_spelling_context, 2 wnp_disputed_zacut_appellation. | Use these flags to prioritize source-lock review; do not change the pair universe automatically. | diagnostic only |
| Pair universe | source-policy scenario impact | diagnostic_scenario_only | baseline: 165 >=5 pairs (gap -2), 86 in 5..8 lane; exclude WNP Zacut: 157 >=5 pairs (gap 6), 78 in 5..8 lane; exclude all flags: 154 >=5 pairs (gap 9), 78 in 5..8 lane; no source policy selected. | Use this to frame the source-policy decision; do not promote any scenario automatically. | diagnostic only |
| Pair universe | defined-distance output interpretation | recommended_working_interpretation | The cited 163 is best treated as a corrected-distance output count, not a raw table count. Broad all-lane diagnostics now define 50 distances at cap 250 and 72 at cap 1000. | Use the defined set as diagnostic pressure only; it still does not reproduce the source-cited 163 distances. | still blocked until source and formula locks |
| D(w) skip-cap formula | printed WRR formula | primary_text_default | 120 skip-cap rows; printed formula currently selected in the audit; 55 rows do not reach the expected-hit target. | Keep as the source-facing default because it is the printed WRR formula. | not claim-ready without final pair lock |
| D(w) skip-cap formula | reported WRR-program formula | sensitivity_variant | 13 program caps below printed; 107 equal; defined smoke rows printed/program/fixed250 = 28/28/28. All-lane cap-1000 program formula defines 72 rows and changes 0 pair rows versus printed. | Carry as a required sensitivity run because MBBK reports the WRR programs used this formula. | not claim-ready without source decision |
| Permutation | repo-defined WNP-excluded 999,999 date-label diagnostic | best_current_diagnostic_not_reproduction | 999999 permutations; 174 observed rows; 48 defined c-values; rho0=0.00086. | Use for local diagnostic evidence while keeping exact WRR reproduction blocked. | diagnostic only |

## Current No-Input Path

Proceeding no-input work has now wired the broad imported same-record
WRR2 pair input, kept the printed formula as the source-facing default,
carried the reported-program formula as a sensitivity variant, and
treated the WNP-excluded 999,999 date-label permutation as diagnostic
evidence only.

Current broad-input result: the all-lane cap-1000 program-formula
sensitivity run changes 0 pair rows versus the printed-formula run.
This lowers the current diagnostic risk from the printed-vs-program
formula choice, but it does not lock the WRR source method.

Claim-grade language still requires a source-locked pair universe, a
source-locked `D(w)` formula decision, full corrected distances over that
locked universe, and a locked aggregate/permutation procedure.
