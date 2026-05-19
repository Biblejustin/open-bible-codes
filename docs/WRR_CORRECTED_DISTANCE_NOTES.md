# WRR Corrected Distance Notes

Status: source-backed implementation notes, not a completed reproduction.

Primary source:

- WRR 1994 paper PDF:
  `https://academicweb.nd.edu/~rwilliam/ndonly/readings/Methods/06-ContentAnalysis/Equidistant%20Letter%20Sequences%20in%20the%20Book%20of%20Genesis%201994.pdf`

Related methodology source:

- WRR2/Nations methodology page:
  `https://www.math.toronto.edu/drorbn/Codes/Nations/WRR2/index.html`

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
  10. The existing `els/wrr.py` helpers already implement the expected-count
  arithmetic and skip-cap selection.
- Corrected distance `c(w,w')` is based on ranking the ordinary proximity
  against 125 perturbation proximities from triples `(x,y,z)` with each element
  in `{-2,-1,0,1,2}`.
- Perturbed ELS offsets keep the early letters on the ordinary progression and
  perturb the last three gaps:
  `n, n+d, ..., n+(k-4)d, n+(k-3)d+x, n+(k-2)d+x+y, n+(k-1)d+x+y+z`.
- The 1994 Appendix A.2 formula defines `v(w,w')` as the number of valid
  triples whose perturbed proximity is greater than the ordinary proximity, and
  `c(w,w') = v(w,w') / m(w,w')`, where `m(w,w')` is the number of valid triples.
- The corrected distance is undefined if the ordinary `(0,0,0)` case is not in
  the valid perturbation set or if `m(w,w') < 10`.

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
- low-level WRR2/Nations ELS-vs-surface-string distance/proximity helpers in
  `els/wrr.py`. These implement the source-described fixed-row-width distance
  `f^2 + f'^2 + l^2 + 1`, use `f' = 1` for surface-letter strings, and sum
  the inverse distances across declared candidate row widths.
- `P1`, `P2`, permutation-rank, and Bonferroni `rho0` helpers in `els/wrr.py`;
- WRR perturbation triples, perturbed-offset generation, and first-ten
  row-width helpers in `els/wrr.py`;
- strict WRR 1994 corrected-distance rank helper in `els/wrr.py` for
  already-computed perturbation proximities. This helper implements the
  Appendix A.2 `v/m` step with strict greater-than counting.
- tie-aware corrected-distance rank helper in `els/wrr.py` for methodology-page
  diagnostics where tied non-ordinary perturbations are half-weighted. A
  uniquely strongest ordinary proximity has corrected distance `0` under both
  helpers.
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
  disputed Zacut rows would overshoot. These pages are not treated as the
  canonical WRR pair table.
- perturbation boundary diagnostic over sampled imported length 5..8 ELS hits.

Not yet implemented:

- source-checked handling for undefined domain rows before they are used in a
  reproduction driver;
- corrected-distance `c(w,w')` calculation over real word pairs from those
  `Q` and perturbed-`Q` values;
- permutation driver over the locked personality/date pair table.

## Ambiguities To Pin Before Code

1. Tie handling across related methodology descriptions.

   The 1994 paper's Appendix A.2 text defines `v(w,w')` with strict
   greater-than counting, while a related methodology-page diagnostic uses
   half-weighted ties. `els/wrr.py` keeps both helpers separate. Use the strict
   helper for WRR 1994 replication work unless a source-specific diagnostic
   says otherwise.

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
   screen. Before computing `c(w,w')`, lock a reconciliation table explaining
   how the 298 candidate pairs reduce to the 163 defined distances cited in
   later discussion.

## Proposed Implementation Order

1. Reconcile the canonical WRR pair table against a primary or citable
   transcription.
2. Establish an explicit source-backed policy for undefined domain rows.
3. Feed ordinary and perturbed `Q` values through the strict WRR 1994
   rank helper to produce `c(w,w')`.

## Current Read

WRR should stay `under_specified`. The project has enough source notes to start
small helper work, but not enough locked method detail to promote the existing
WRR audit outputs into a reproduction or refutation.
