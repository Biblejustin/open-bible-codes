# WRR Methodology Gaps

Status: current audit blockers before any WRR reproduction claim.

The repo can now import the external WRR2 plain-text list, count terms in Koren
Genesis, audit same-record appellation/date proximity, and run control screens.
Those pieces are useful source diagnostics. They are still not the WRR 1994
experiment.

## Current Smoke Baseline

Latest audited path:

```bash
python3 -m scripts.run_protocol protocols/wrr_audit_counts.toml --resume
```

Current imported-data shape:

| Item | Count |
| --- | ---: |
| parsed WRR2 personality records | 32 |
| undated records skipped by default | 2 |
| emitted source rows | 199 |
| appellation rows | 168 |
| date rows | 31 |
| same-record pair rows at min length 3 | 182 |
| same-record pair rows after appellation length >= 5 | 165 |
| same-record pair rows at lengths 5..8 | 86 |

Current ANU famous-rabbis source-shape check:

| Source | Raw same-record pairs |
| --- | ---: |
| `WRR1.txt` | 193 |
| `WRR2.txt` | 182 |
| `SE2a.txt` | 117 |
| `SE2b.txt` | 171 |
| `SE3.txt` | 84 |

None of these raw source files directly matches the source-cited 163 second-list
distances.

Current Koren Genesis count smoke:

| Item | Count |
| --- | ---: |
| normalized Genesis letters | 78,064 |
| parsed verses | 2,075 |
| rows counted at min length 3 | 196 |
| zero-hit rows | 112 |
| appellation total hits | 13,043 |
| date total hits | 4,383 |

Current Koren Genesis text lock:

| Item | Value |
| --- | --- |
| raw `genesis.koren.gz` SHA-256 | `35e8e9a0752f6b127e7c081a2ca680a63f9851516d65ca102928102783836ea7` |
| decompressed source SHA-256 | `3b45732824972890c4a702da5cd01b72a91576917bab1850c2b6f13888e2cdff` |
| normalized text SHA-256 | `b26028e02b921fd18a3f5669fa6db38aa500e516926e9f19ad65a6e32ddc3540` |
| normalized letters | 78,064 |
| parsed verses | 2,075 |

Current control read:

| Screen | Result |
| --- | --- |
| top 20 raw pair controls | 0 adjusted-q signal rows |
| length 5..8 top pair controls | 0 adjusted-q signal rows |
| strict same-chapter/same-signed-skip rows at length 5..8 | 0 |

These numbers are audit outputs. They should not be cited as confirmation or
refutation of the WRR paper.

## Reproduction Gate Checklist

| Gate | Required before claim language | Current state |
| --- | --- | --- |
| Source text | Exact Genesis text and normalization locked | Koren Genesis stream is fingerprinted and usable for smoke/audit work. |
| Source pages | Cited paper/list context downloaded and hash-stamped | Paper, ANU files, WRR/Nations pages, MC key, WNP critique pages, MBBK 1999 response, Chance article, Torah-code papers page, and Bombach/Gans/Haralick/Levitt/Rips/Schwartzman/Witztum papers/data are tracked in the source manifest. |
| Pair universe | Declared second-list candidate set yields 163 source-defined distances after the corrected-distance eligibility rule | Lock-prep table exists at `reports/wrr_1994/wrr2_pair_eligibility_table.csv`; imported `WRR2.txt` yields 182 raw same-record pairs, 165 after appellation length >= 5, and 86 under the current 5..8 both-side screen. The `163` count is now treated as a defined-distance output count, not a raw pair table. |
| Exclusions | Every excluded appellation/date row has a citable rule | Not locked; one Zacut-appellation exclusion would close 165 to 163, but that is only a diagnostic hypothesis. |
| Skip caps | Term-specific WRR `D(w)` windows applied for each accepted term | Not locked; helpers now support both the printed WRR formula and the reported WRR-program formula. The skip-cap audit keeps printed selected while reporting program caps side by side. Current pair/control screens still use broad fixed caps for smoke tests. |
| Corrected distance | Per-pair `c(w,w')` implemented and fixture-tested | Helpers now include conservative supplied-row domain labeling, real-corpus WRR2 domain diagnostics with undefined-reason labels, defined-domain-only ordinary `Q(w,w')` diagnostics, exact perturbed-ELS match checks, domain-weighted `Q(w,w')` summation for domain-labeled ELS rows, a tested pair-level corrected-distance arithmetic bridge for already-domain-labeled perturbation sets, and the source-count WRR `v/m` rank step. Undefined `c(w,w')` conditions are source-backed; the real-corpus perturbed-row/domain generator and per-pair output driver are still missing. |
| Aggregate statistic | `P1`, `P2`, `P3`, `P4`, rank handling, and `rho0` run over the locked pair set | Helpers exist, but no reproduction driver can run until the pair set and corrected distances are fixed. |
| Permutation test | Date/rabbi pairings shuffled under the declared WRR rule with recorded seeds/counts | Not built. |
| Report label | Result can be marked reproduction, failed reproduction, or under-specified | Current label must remain `under_specified`. |

## Blocking Gaps

### 1. Candidate Pair Set And Defined-Distance Count

The current import creates 182 same-record appellation/date pair rows at
minimum length 3. Filtering only appellations shorter than 5 letters gives 165
rows, while the 5..8 length screen gives 86 rows. That does not yet reconcile
to the source-cited WRR second-list distance count of 163 by raw combinatorics.
The better current reading is that `163` is produced after applying the
corrected-distance eligibility screen, not by selecting a separate raw
same-record pair table.

The WNP/McKay-Bar-Natan source critique confirms the 5-8 appellation-length
restriction and disputes several Rabbi II-27 Moshe Zacut variants
(`ZKWT)`, `ZKWTW`, `M$H ZKWT)`, `M$H ZKWTW`). Since Rabbi II-27 has two date
rows in the imported source, one length-eligible appellation exclusion there
would explain the remaining 165-to-163 gap. Excluding all four WNP-disputed
Zacut rows would remove eight pairs, leaving 157, so the critique page does not
by itself explain the published count. Treat this as a hypothesis, not a
declared rule. Do not make Zacut-specific exclusions unless a citable WRR pair
source requires them before the corrected-distance eligibility screen.

Before any reproduction run, the project needs a locked table showing:

- each personality record;
- every accepted appellation spelling;
- every accepted date spelling;
- which rows are excluded and why;
- final candidate count under the declared WRR rule;
- final defined-distance count after `c(w,w')` eligibility is applied.

Current lock-prep output:

| Item | Count |
| --- | ---: |
| imported same-record pair rows | 182 |
| appellation length >= 5 pair rows | 165 |
| length 5..8 smoke-lane pair rows | 86 |
| WNP Zacut diagnostic pair rows | 8 |
| pair rows with zero Genesis hits at the smoke cap | 129 |
| pair rows where at least one term does not reach the skip-cap target | 155 |
| pair rows with close hits in the nearest-pair smoke audit | 40 |
| pair rows with strict same-chapter/same-skip close hits | 5 |

The generated table is `reports/wrr_1994/wrr2_pair_eligibility_table.csv`;
summary and reader output are `reports/wrr_1994/wrr2_pair_eligibility_summary.csv`
and `reports/wrr_1994/wrr2_pair_eligibility_table.md`. It is explicitly
`lock_prep_only_not_canonical`.

### 2. Primary-Source Cross-Check

The current machine-readable WRR2 source is the ANU/McKay secondary plain-text
file. It is useful because it is stable and parseable, but it must be checked
against a citable transcription of the paper table or another source with clear
provenance.

The PDF table text is not currently reliable enough for direct automated import.

### 3. Corrected Distance `c(w,w')`

The repo has cylindrical distance and WRR arithmetic helpers, conservative
domain labeling for supplied same-word ELS rows, a real-corpus WRR2 Genesis
domain-labeling diagnostic with undefined-reason labels, exact perturbed-ELS
match checks, domain-weighted `Q(w,w')` summation for already-domain-labeled
ELS rows, a tested pair-level arithmetic bridge from domain-labeled
perturbation sets to `c(w,w')`, plus the source-count WRR rank step for
already-computed ordinary and perturbed proximity values. MBBK Appendix A and
the Gans communities paper support the undefined `c(w,w')` rule: the ordinary
`(0,0,0)` value must be defined and at least 10 perturbation proximities must be
defined; the `v/m` count uses perturbation proximity values greater than or
equal to ordinary.
Current domain diagnostics label 17,426 imported-term hits: 6,079 defined
domains, 11,347 blocked by an inner shorter-skip ELS, and 0 ambiguous from
enclosing shorter-skip rows under the smoke cap. The ordinary-Q diagnostic over
182 imported same-record pairs finds 53 pairs with at least one defined-domain
pair, 17 pairs with all observed domains defined, 36 incomplete defined-only
pairs, and 129 pairs with no defined-domain pair. In the length-5..8 smoke lane
specifically, 30 of 86 pairs have defined-domain ordinary `Q`, 16 are complete,
14 are incomplete, and 56 have no defined-domain pair. The repo still does not
implement the paper's corrected distance value for every term pair because the
real-corpus perturbed-row/domain generator and per-pair output driver are
missing.

The perturbation diagnostic now distinguishes boundary validity from exact
perturbed matches. In the current output, all 959 smoke-cap hits across 64 rows
with hits keep all 125 perturbation triples in bounds, but every row with hits
has fewer than 10 exact perturbed matches. Exact-match counts range from 1 to
5, with median 1. This is still only a term-hit diagnostic, not a pair-level
corrected-distance calculation.

The pair-readiness join gives the same warning at the pair-table level: of 86
length-5..8 smoke-lane pairs, 56 lack checked hits for at least one side, 30
have fewer than 10 exact perturbed matches, and 0 are ready for
pair-level perturbed `Q`. The other 96 imported same-record pairs are outside
the current length-5..8 perturbation diagnostic scope.
Implementation notes are now tracked in
`docs/WRR_CORRECTED_DISTANCE_NOTES.md`.

Needed next:

- lock whether `D(w)` uses the printed WRR count formula or the WRR program
  formula documented by MBBK;
- generate and domain-label real perturbed ELS rows per term/triple;
- feed real perturbed `Q(x,y,z)(w,w')` rows through the tested pair-level bridge;
- output per-pair `c(w,w')` rows before aggregate statistics are attempted.

### 4. Term-Specific Skip Caps

The audit currently uses fixed broad search caps for pair/control screens. WRR
uses term-specific skip windows tied to expected ELS counts.

Current length 5..8 skip-cap smoke:

| Item | Count |
| --- | ---: |
| length-filtered rows | 120 |
| unique normalized terms | 109 |
| rows with estimated `D(w) <= 250` | 16 |
| rows where reported-program `D(w)` is smaller than printed `D(w)` | 13 |
| rows where reported-program `D(w)` equals printed `D(w)` | 107 |
| rows not reaching expected 10 by word-max skip | 55 |
| rows with zero observed hits at max skip 250 | 56 |

This means fixed `max_skip=250` is not a reproduction setting, and the printed
formula versus reported-program formula choice remains a method lock item.

### 5. Aggregate Statistic And Permutations

The repo has tested helpers for `P1`, `P2`, permutation rank, and Bonferroni
`rho0`. It still needs a driver that:

- computes corrected distances for the locked pair set;
- computes `P1`, `P2`, `P3`, and `P4`;
- shuffles date/rabbi pairings under the declared WRR rule;
- records random seeds, permutation count, ties, and manifests;
- reports whether the run reproduces, fails to reproduce, or remains
  under-specified.

## Review Rule

Treat current WRR outputs as source-audit and smoke-test evidence only. Move to
claim language only after the pair set, corrected distance, skip caps, and
permutation procedure are all locked before looking at final results.
