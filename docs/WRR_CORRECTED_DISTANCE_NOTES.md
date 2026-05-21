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
  `reports/wrr_1994/`;
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
- perturbation boundary/exact-match diagnostic over imported length 5..8 ELS
  hits. Current output checks all 959 smoke-cap hits across 64 rows with hits:
  every ordinary hit keeps all 125 triples in bounds, but every row with hits
  has fewer than 10 exact perturbed matches; exact-match counts range from 1 to
  5, with median 1.
- perturbation pair-readiness diagnostic joining checked exact-match term rows
  to the lock-prep pair table. Current output has 86 length-5..8 smoke-lane
  pairs: 56 lack checked hits for at least one side, 30 have fewer than 10
  exact perturbed matches, and 0 are ready for pair-level perturbed `Q`.
- real-corpus corrected-distance smoke driver in
  `scripts/analyze_wrr_corrected_distance.py`. It generates exact perturbed
  rows from ordinary ELS hits, labels domains per perturbation triple, and
  feeds domain-defined rows through the pair-level corrected-distance bridge.
  Current smoke output for the 86 length-5..8 candidate-lane pairs has 0
  defined corrected distances: 56 pairs lack a valid ordinary perturbation and
  30 have fewer than 10 valid perturbations; the maximum valid perturbation
  count is 3.
- corrected-distance smoke variant comparison in
  `scripts/compare_wrr_corrected_distance_variants.py`. Current 5..8
  candidate-lane comparison gives 0 defined corrected distances for term
  printed, term program, and fixed-250 settings. Term printed and term program
  both have maximum valid perturbation count 3; fixed-250 raises that maximum
  to 4 but still does not define any corrected distances.
- corrected-distance aggregate diagnostic in
  `scripts/analyze_wrr_corrected_distance_aggregate.py`. It computes P1/P2
  from all defined `c(w,w')` rows and P3/P4 from the smaller sample that omits
  appellations whose imported source token starts with title `RBY`. Current
  length-5..8 smoke output has 0 defined values, so aggregate P1..P4 are
  intentionally blank.
- high-cap local diagnostic protocol in
  `protocols/wrr_corrected_distance_highcap_1000_split_2.toml`. Current
  ignored output at `search-max-skip=1000` still has 0 defined corrected
  distances over 86 length-5..8 smoke-lane pairs. The merged corrected-distance
  summary has maximum valid perturbation count 4. The all-hit high-cap
  perturbation diagnostic has 80/120 rows with hits, 3,694 checked hits, and
  80 rows whose minimum exact perturbation count remains below 10. The joined
  pair-readiness diagnostic has 0 ready pairs, 40 pairs missing checked hits on
  one side, and 46 pairs below the exact-perturbation threshold.

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

## Proposed Implementation Order

1. Decide whether `D(w)` uses the printed WRR count formula or the program
   formula documented by MBBK; current audit rows expose both.
2. Extend the smoke corrected-distance driver into an optimized full run over
   the final locked pair universe.
3. Feed defined `c(w,w')` rows into the aggregate `P1`..`P4` diagnostic and
   then into claim-grade permutation tests.

## Current Read

WRR should stay `under_specified`. The project has enough source notes to start
small helper work, but not enough locked method detail to promote the existing
WRR audit outputs into a reproduction or refutation.
