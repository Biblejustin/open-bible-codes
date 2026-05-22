# WRR Corrected Distance Notes

Status: source-backed implementation notes, not a completed reproduction.

Primary source:

- WRR 1994 paper PDF:
  `https://academicweb.nd.edu/~rwilliam/ndonly/readings/Methods/06-ContentAnalysis/Equidistant%20Letter%20Sequences%20in%20the%20Book%20of%20Genesis%201994.pdf`

Related methodology source:

- WRR2/Nations methodology page:
  `https://www.math.toronto.edu/drorbn/Codes/Nations/WRR2/index.html`
- McKay/Bar-Natan/Bar-Hillel/Kalai 1999 response, Appendix A:
  `https://users.cecs.anu.edu.au/~bdm/codes/StatSci/StatSci.pdf`
- Gans communities paper:
  `https://www.torah-code.org/papers/gans.pdf`

## What Is Clear Enough To Implement

The paper's Appendix A.1 and A.2 define these pieces:

- Genesis is treated as a cylindrical array with variable row width `h`.
- Letter distance is Euclidean distance on that cylinder, using the shorter
  wrapped column distance.
- For two fixed ELS rows `e` and `e'`, the raw distance term is based on:
  distance between consecutive letters of `e`, distance between consecutive
  letters of `e'`, and the nearest letter-to-letter distance between the two
  ELS rows.
- The proximity term is an inverse distance. Larger proximity means closer
  configurations.
- Relevant row widths are the first ten integer widths nearest to `|d| / i`
  for each ELS skip.
- ELS rows are weighted by the intersection of their domains of minimality.
- Skip caps are term-specific: choose `D(w)` so the expected ELS count is about
  10. The `els/wrr.py` helpers support both the printed WRR formula and the
  reported WRR-program formula for expected-count arithmetic and skip-cap
  selection.
- Corrected distance `c(w,w')` is based on ranking the ordinary proximity
  against 125 perturbation proximities from triples `(x,y,z)` with each element
  in `{-2,-1,0,1,2}`.
- Perturbed ELS offsets keep the early letters on the ordinary progression and
  perturb the last three gaps:
  `n, n+d, ..., n+(k-4)d, n+(k-3)d+x, n+(k-2)d+x+y, n+(k-1)d+x+y+z`.
- The exact perturbed letters must spell the word, but the source descriptions
  say distance measurements use the unperturbed `(n,d,k)` positions for the
  perturbed ELS.
- MBBK Appendix A defines `c(w,w')` as the fraction of valid perturbation values
  greater than or equal to the ordinary proximity; the extracted WRR 1994 text
  uses strict greater-than wording in one passage. The current source-count
  helper follows the later MBBK `>=` description and keeps tie-sensitive
  behavior isolated in separate helper tests.
- The corrected distance is undefined if the ordinary `(0,0,0)` case is not in
  the valid perturbation set or if `m(w,w') < 10`.
- MBBK Appendix A notes a formula mismatch for the ELS-window count: the printed
  WRR formula uses `(D - 1)(2L - (k - 1)(D + 2))`, while the WRR programs used
  `(D - 1)(2L - (k - 1)D)`. The helper can now compute either formula; the
  current skip-cap audit keeps the printed formula selected while reporting
  program-formula caps side by side. A reproduction driver must explicitly
  choose one before final `D(w)` runs.

## Current Repo Coverage

Already implemented:

- cylindrical point and hit distance helpers in `els/pairing.py`;
- matrix coordinates in `els/matrix.py`;
- expected ELS count and skip-cap helpers in `els/wrr.py`;
- low-level WRR 1994 ELS-vs-ELS distance/proximity helpers in `els/wrr.py`.
  These implement the paper's fixed-row-width distance `f^2 + f'^2 + l^2`
  and the `alpha(e,e')` row-width sum across the first ten widths from each
  ELS skip.
- WRR domain-overlap weighting and `Q(w,w')` summation helpers in `els/wrr.py`
  for ELS occurrences that already have half-open domains of minimality
  attached. These implement the `omega(e,e') * alpha(e,e')` sum, but do not yet
  derive the domains from the full ELS set.
- conservative WRR domain-of-minimality interval helper in `els/wrr.py` for
  unambiguous shorter-skip boundary cases, plus a candidate-domain helper that
  exposes multiple incomparable maximal segments when a shorter-skip row
  strictly encloses the target span.
- full supplied-row domain-labeling helper in `els/wrr.py` that applies the
  conservative interval helper across all ELS rows supplied for one word and
  separates defined from undefined domain assignments with reason labels.
- real-corpus WRR2 Genesis domain-labeling diagnostic in
  `scripts/analyze_wrr_domain_labeling.py` and `protocols/wrr_audit_counts.toml`.
  Current ignored output labels 17,426 imported-term hits: 6,079 defined domains
  and 11,347 undefined domains under the conservative helper. The current
  diagnostic splits those undefined rows as 11,347 blocked by an inner
  shorter-skip ELS and 0 ambiguous from enclosing shorter-skip ELS rows.
- defined-domain-only ordinary `Q(w,w')` diagnostic in
  `scripts/analyze_wrr_ordinary_q.py` and `protocols/wrr_audit_counts.toml`.
  Current ignored output covers 182 imported same-record pairs: 53 have at
  least one defined-domain pair, 17 have all observed domains defined, 36 are
  incomplete because undefined rows were omitted, and 129 have no defined-domain
  pair. The length-5..8 smoke lane has 86 pairs, of which 30 have
  defined-domain ordinary `Q`, 16 have all observed domains defined, 14 are
  incomplete, and 56 have no defined-domain pair. This is not corrected
  distance.
- low-level WRR2/Nations ELS-vs-surface-string distance/proximity helpers in
  `els/wrr.py`. These implement the source-described fixed-row-width distance
  `f^2 + f'^2 + l^2 + 1`, use `f' = 1` for surface-letter strings, and sum
  the inverse distances across declared candidate row widths.
- `P1`, `P2`, Rabbi-title appellation screening for the smaller P3/P4
  sample, permutation-rank, and Bonferroni `rho0` helpers in `els/wrr.py`;
- WRR perturbation triples, perturbed-offset generation, exact perturbed-ELS
  match checks, bounded perturbed-match iteration, and first-ten row-width
  helpers in `els/wrr.py`;
- WRR corrected-distance rank helper in `els/wrr.py` for already-computed
  perturbation proximities. This helper implements the source-described `v/m`
  step with greater-than-or-equal counting. The older
  `corrected_distance_strict_rank` name remains as a backward-compatible alias.
- pair-level corrected-distance arithmetic bridge in `els/wrr.py` for
  already-domain-labeled perturbation occurrence sets. It computes
  `Q(x,y,z)(w,w')` per valid triple, requires a valid ordinary `(0,0,0)` triple,
  enforces the minimum valid-perturbation count, and returns the source-count
  WRR rank. It does not generate the real perturbed ELS/domain rows.
- tie-aware corrected-distance rank helper in `els/wrr.py` for methodology-page
  diagnostics where tied non-ordinary perturbations are half-weighted. A
  uniquely strongest ordinary proximity has corrected distance `0` under the
  tie-aware helper and `1/m` under the source-count helper.
- imported WRR2 term rows from the secondary ANU/McKay source under ignored
  `reports/wrr_1994/`. User decision on 2026-05-21 authorizes this as the
  working machine-readable source for continued WRR2 corrected-distance work,
  while retaining its secondary-source provenance caveat;
- count, same-record pair-audit, pair-control, and skip-cap smoke reports.
- Koren Genesis text-source fingerprinting for raw compressed bytes,
  decompressed source bytes, and the normalized Genesis stream used by the WRR
  smoke reports.
- pair-table reconciliation diagnostic showing 182 imported same-record pairs,
  165 pairs after an appellation length >= 5 screen, and 86 length-filtered
  pairs against the source-cited 163 second-list distances.
- ANU famous-rabbis source-shape diagnostic showing that `WRR1.txt`,
  `WRR2.txt`, `SE2a.txt`, `SE2b.txt`, and `SE3.txt` do not directly expose
  163 raw same-record appellation/date pairs.
- WNP/McKay-Bar-Natan source-critique pages are downloaded and hashed as
  external audit context. They confirm the 5-8 appellation-length restriction
  and flag several Rabbi II-27 Moshe Zacut variants as disputed. The
  reconciliation diagnostic shows that excluding one length-eligible Zacut
  appellation would close the 165-to-163 count gap, while excluding all four
  disputed Zacut rows would overshoot. These pages are not treated as a source
  rule for pre-filtering the candidate set.
- source-policy scenario diagnostics now keep the policy impact visible without
  selecting a policy: baseline 165 >=5 pairs, exclude WNP Zacut 157, and exclude
  all source-review flags 154. The single-term Zacut impact table identifies
  `ZKWTA`, `ZKWTW`, `M$HZKWTA`, and `M$HZKWTW` as individual exclusions that
  would leave 163 >=5 pairs with gap 0, still as diagnostic evidence only.
- legacy perturbation boundary/exact-match diagnostic over ordinary imported
  length 5..8 ELS hits. Current output checks all 959 smoke-cap ordinary hits
  across 64 rows with hits: every ordinary hit keeps all 125 triples in bounds,
  but every row with ordinary hits has fewer than 10 exact perturbed matches;
  exact-match counts range from 1 to 5, with median 1. This is now retained as
  an ordinary-hit diagnostic only; direct corrected-distance search no longer
  requires a full ordinary ELS hit before testing perturbed letters.
- legacy perturbation pair-readiness diagnostic joining ordinary-hit
  exact-match term rows to the lock-prep pair table. Current output has 86
  length-5..8 smoke-lane pairs: 56 lack checked ordinary hits for at least one
  side, 30 have fewer than 10 ordinary-hit exact perturbed matches, and 0 are
  ready under that older ordinary-hit-only screen. This is not a direct-search
  readiness gate.
- real-corpus corrected-distance smoke driver in
  `scripts/analyze_wrr_corrected_distance.py`. It generates exact perturbed
  rows by direct perturbed-letter search from the unperturbed prefix, stores the
  source-described unperturbed `(n,d,k)` offsets for distance/domain
  measurement, labels domains per perturbation triple, and feeds domain-defined
  rows through the pair-level corrected-distance bridge. Current smoke output
  for the 86 length-5..8 candidate-lane pairs has 28 defined corrected
  distances: 56 pairs lack a valid ordinary perturbation and 2 have fewer than
  10 valid perturbations; the maximum valid perturbation count is 125.
- corrected-distance smoke variant comparison in
  `scripts/compare_wrr_corrected_distance_variants.py`. Current 5..8
  candidate-lane comparison gives 28 defined corrected distances for term
  printed, term program, and fixed-250 settings. All three variants have a
  maximum valid perturbation count of 125 under the direct-search driver.
- corrected-distance aggregate diagnostic in
  `scripts/analyze_wrr_corrected_distance_aggregate.py`. It computes P1/P2
  from all defined `c(w,w')` rows and P3/P4 from the smaller sample that omits
  appellations whose imported source token starts with title `RBY`. Current
  length-5..8 smoke output has 28 defined values; the diagnostic aggregate is
  P1 `0.000373062903552`, P2 `5.981029379e-05`, P3
  `0.000349191888979`, and P4 `7.69538206457e-05`. This remains
  diagnostic-only because the pair universe and `D(w)` formula are not locked.
- high-cap local diagnostic protocol in
  `protocols/wrr_corrected_distance_highcap_1000_split_2.toml`. Current
  ignored output at `search-max-skip=1000` has 46 defined corrected distances
  over 86 length-5..8 smoke-lane pairs, 40 ordinary-not-valid pairs, and a
  maximum valid perturbation count of 125. Its diagnostic aggregate is P1
  `0.00220968684352`, P2 `6.37334076429e-06`, P3 `0.0108669973844`, and P4
  `8.66346313541e-05`. The retained all-hit high-cap perturbation and
  pair-readiness diagnostics are ordinary-hit-only legacy checks, not
  direct-search blockers.
- all-lane direct diagnostic protocol in
  `protocols/wrr_corrected_distance_direct_all_lanes.toml`. Current ignored
  output over all 182 imported same-record WRR2 pairs has 50 defined corrected
  distances at cap 250 and 72 defined corrected distances at cap 1000. The
  cap-1000 split defines 46 rows in the length-5..8 lane, 12 additional rows in
  the appellation-min-length lane, and 14 rows currently marked
  `excluded_by_appellation_min_length`. This remains pair-universe diagnostic
  evidence only; see `docs/WRR_DIRECT_ALL_LANES_DIAGNOSTIC.md`.
- defined pair-set audit in `scripts/analyze_wrr_defined_pair_set.py`, joining
  the all-lane corrected-distance outputs back to pair-lane, review-status, and
  WNP-Zacut labels. Current tracked output is
  `docs/WRR_DEFINED_PAIR_SET_AUDIT.md`.
- defined-gap reason audit in `scripts/analyze_wrr_defined_gap_reasons.py`,
  classifying the best current cap-1000 gap as zero-ordinary-hit failures
  rather than under-minimum perturbation failures. Current tracked output is
  `docs/WRR_DEFINED_GAP_REASON_AUDIT.md`.
- cross-pair date-label permutation diagnostic in
  `protocols/wrr_cross_pair_grid.toml`. Current cap-250 output crosses 168
  imported appellations against 31 imported date rows, defines 1,423 corrected
  distances over 5,208 generated rows, and ranks the 50 defined observed
  same-record distances against 1,000 sampled date-label permutations with
  diagnostic rho0 `0.003996003996`. The current repo-defined WNP-excluded
  999,999-permutation diagnostic ranks 48 defined observed c-values over 174
  observed rows at Bonferroni rho0 `0.00086`. Both are still diagnostic-only;
  see `docs/WRR_CROSS_PAIR_GRID.md`.
- exploratory all-lane corrected-distance diagnostics over all 182 imported
  same-record pairs were run before direct perturbed-letter search and should be
  treated as obsolete historical diagnostics until rerun with the current
  driver.

Not yet implemented:

- an optimized full-run real-corpus corrected-distance driver over the final
  locked pair universe and source-selected `D(w)` formula;
- claim-grade P1..P4 and permutation driver over the locked personality/date
  pair table.

## Ambiguities To Pin Before Code

1. Tie handling across related methodology descriptions.

   The source-count WRR formula uses greater-than-or-equal counting. A related
   methodology-page diagnostic uses half-weighted ties. `els/wrr.py` keeps both
   helpers separate. Use `corrected_distance_wrr_rank` for WRR 1994 replication
   work unless a source-specific diagnostic says otherwise.

2. Domain-of-minimality derivation.

   The rank helper only consumes already-computed ordinary and perturbed
   proximity values. `els/wrr.py` can now sum domain-weighted ELS-pair
   contributions when domains are supplied and can derive unambiguous domain
   boundaries across supplied same-word ELS rows and run the diagnostic over
   generated real-corpus hit files. It now identifies enclosing-span ambiguity
   separately; the current WRR2 Genesis smoke cap has 0 enclosing-ambiguous
   rows, while all undefined rows are blocked by inner shorter-skip ELS rows.

3. ELS-vs-ELS versus ELS-vs-surface-text.

   The WRR 1994 paper compares two ELS words. The WRR2/Nations page documents a
   related but not identical ELS-vs-surface-word version. Use the 1994 paper for
   rabbi/date reproduction.

4. Pair table.

   The current imported WRR2 file emits 199 source rows, 182 raw same-record
   appellation/date combinations, 165 pairs after an appellation length >= 5
   screen, and 86 length-filtered rows under the repo audit. The WRR discussion
   sources cite 163 second-list distances, while the 1994 paper says the
   length-5..8 second-list sample has 298 word pairs before the defined-distance
   screen. Current read: `163` is a defined-distance output count, not a raw
   same-record pair table. Before aggregate statistics, derive that count by
   applying the source-backed `c(w,w')` eligibility rules over the candidate set.
   The source-policy scenarios are decision aids only: they show how WNP/context
   exclusions move the raw >=5 count, including four single Zacut rows whose
   individual exclusion leaves 163 >=5 pairs with gap 0, but do not select the
   final pair universe.

## Proposed Implementation Order

1. Select the source policy for candidate pair inclusion.
2. Decide whether `D(w)` uses the printed WRR count formula or the program
   formula documented by MBBK; current audit rows expose both.
3. Extend the smoke corrected-distance driver into an optimized full run over
   the final locked pair universe.
4. Feed defined `c(w,w')` rows into the aggregate `P1`..`P4` diagnostic and
   then into claim-grade permutation tests.

## Current Read

WRR should stay `under_specified`. The project has enough source notes to start
small helper work, but not enough locked method detail to promote the existing
WRR audit outputs into a reproduction or refutation.
