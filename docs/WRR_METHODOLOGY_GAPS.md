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
| Pair universe | Declared second-list candidate set yields 163 source-defined distances after the corrected-distance eligibility rule | Lock-prep table exists at `reports/wrr_1994/wrr2_pair_eligibility_table.csv`; imported `WRR2.txt` yields 182 raw same-record pairs, 165 after appellation length >= 5, and 86 under the current 5..8 both-side screen. The `163` count is now treated as a defined-distance output count, not a raw pair table. Source-policy scenarios are diagnostic only: baseline 165 >=5 pairs, exclude WNP Zacut 157, exclude all source-review flags 154. Single-term Zacut diagnostics identify `ZKWTA`, `ZKWTW`, `M$HZKWTA`, and `M$HZKWTW` as individual exclusions that leave 163 >=5 pairs with gap 0. Visual triage notes separate OCR misses from title-prefix and Chelm source-rule questions, but do not exclude pairs automatically. |
| Exclusions | Every excluded appellation/date row has a citable rule | Not locked; one of four Zacut-appellation exclusions would close 165 to 163, but that is only a diagnostic hypothesis. The source-policy scenario packet does not select any exclusion rule. |
| Skip caps | Term-specific WRR `D(w)` windows applied for each accepted term | Locally locked for the repo-defined run: printed WRR formula main, reported-program formula required sensitivity. D(w) sensitivity currently shows cap-1000 all-lane printed/program defined 72/72 with 0 changed pair rows. Exact published reproduction still needs a method-equivalence statement because MBBK reports a program-formula mismatch. |
| Corrected distance | Per-pair `c(w,w')` implemented and fixture-tested | Full selected-universe cap-1000 corrected-distance output exists for all 182 imported same-record pairs under keep_all_working_source and printed `D(w)`: 72 defined, 110 ordinary-not-valid, 0 under-minimum. Undefined `c(w,w')` conditions are source-backed; exact published reproduction still needs the source-defined 163-distance gap explained. |
| Aggregate statistic | `P1`, `P2`, `P3`, `P4`, rank handling, and `rho0` run over the locked pair set | P1..P4 aggregation exists for defined corrected-distance rows; P3/P4 use the smaller non-Rabbi-title sample. Current direct-search smoke output has 28 defined values at cap 250 and 46 defined values at cap 1000. Cross-pair date-label permutation diagnostics include legacy cap-250 runs plus the locked local cap-1000 keep-all 999,999-permutation run. Exact published reproduction still needs independent source transcription and method-equivalence closure. |
| Permutation test | Date/rabbi pairings shuffled under the declared WRR rule with recorded seeds/counts | Legacy diagnostic date-label shuffles exist, and the selected local lock now has a keep-all cap-1000 999,999-permutation run. Exact published reproduction remains caveated by the source-defined 163-distance gap with current manual source records locked unchanged. |
| Report label | Result can be marked reproduction, failed reproduction, or under-specified | Current exact-publication label remains `under_specified`; `docs/WRR_CLAIM_READINESS.md` marks the selected repo-defined local lock ready for locked-method language. |

## Blocking Gaps

### 1. Candidate Pair Set And Defined-Distance Count

The current import creates 182 same-record appellation/date pair rows at
minimum length 3. Filtering only appellations shorter than 5 letters gives 165
rows, while the 5..8 length screen gives 86 rows. That does not yet reconcile
to the source-cited WRR second-list distance count of 163 by raw combinatorics.
The better current reading is that `163` is produced after applying the
corrected-distance eligibility screen, not by selecting a separate raw
same-record pair table.

The direct all-lane corrected-distance diagnostic now tests all 182 imported
same-record pairs. It defines 50 values at cap 250 and 72 values at cap 1000,
so it still does not explain the source-cited 163 count. At cap 1000, 14
defined values come from rows currently marked
`excluded_by_appellation_min_length`, which is useful diagnostic pressure but
not a source rule.

`docs/WRR_DEFINED_PAIR_SET_AUDIT.md` now joins those direct all-lane runs back
to pair-lane, review-status, and WNP-Zacut labels. The best current direct run
still defines only 72 of the source-cited 163 distances, leaving a 91-distance
gap. The remaining missing mass is ordinary-not-valid, not an
under-minimum-valid edge case.

`docs/WRR_DEFINED_GAP_REASON_AUDIT.md` further classifies that gap. In the
best current cap-1000 run, ordinary-not-valid rows are all zero-ordinary-hit
failures in the current imported term forms: 83 rows lack appellation ordinary
hits, 12 lack date ordinary hits, and 15 lack both. That points the next
source-reconciliation work toward term normalization, source row boundaries,
and the final pair-universe rule before permutation language.

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
file. User decision on 2026-05-21: use this file as the working source for
continued corrected-distance work because it is stable and parseable. It remains
secondary rather than primary-paper ground truth; a citable table cross-check
would improve provenance, but it is no longer the current implementation
blocker.

The PDF table text is not currently reliable enough for direct automated import.

### 3. Corrected Distance `c(w,w')`

The repo has cylindrical distance and WRR arithmetic helpers, conservative
domain labeling for supplied same-word ELS rows, a real-corpus WRR2 Genesis
domain-labeling diagnostic with undefined-reason labels, exact perturbed-ELS
match checks, domain-weighted `Q(w,w')` summation for already-domain-labeled
ELS rows, a tested pair-level arithmetic bridge from domain-labeled
perturbation sets to `c(w,w')`, a smoke real-corpus corrected-distance driver,
plus the source-count WRR rank step for already-computed ordinary and perturbed
proximity values. MBBK Appendix A and the Gans communities paper support the
undefined `c(w,w')` rule: the ordinary `(0,0,0)` value must be defined and at
least 10 perturbation proximities must be defined; the `v/m` count uses
perturbation proximity values greater than or equal to ordinary.
Current domain diagnostics label 17,426 imported-term hits: 6,079 defined
domains, 11,347 blocked by an inner shorter-skip ELS, and 0 ambiguous from
enclosing shorter-skip rows under the smoke cap. The ordinary-Q diagnostic over
182 imported same-record pairs finds 53 pairs with at least one defined-domain
pair, 17 pairs with all observed domains defined, 36 incomplete defined-only
pairs, and 129 pairs with no defined-domain pair. In the length-5..8 smoke lane
specifically, 30 of 86 pairs have defined-domain ordinary `Q`, 16 are complete,
14 are incomplete, and 56 have no defined-domain pair.

The retained perturbation diagnostic distinguishes boundary validity from exact
perturbed matches over ordinary ELS hits. In the current output, all 959
smoke-cap ordinary hits across 64 rows with hits keep all 125 perturbation
triples in bounds, but every row with ordinary hits has fewer than 10 exact
perturbed matches. Exact-match counts range from 1 to 5, with median 1. This is
now a legacy ordinary-hit diagnostic only; the corrected-distance driver no
longer requires a full ordinary ELS hit before testing perturbed letters.

The legacy pair-readiness join gives the same warning for the ordinary-hit-only
screen: of 86 length-5..8 smoke-lane pairs, 56 lack checked ordinary hits for
at least one side, 30 have fewer than 10 ordinary-hit exact perturbed matches,
and 0 are ready under that older screen. It is not a readiness gate for direct
perturbed-letter search.

The corrected-distance smoke driver now generates exact perturbed rows by
direct perturbed-letter search from the unperturbed prefix, labels domains per
perturbation triple, and applies the pair-level bridge to the same 86
length-5..8 smoke-lane pairs. Current cap-250 output has 28 defined corrected
distances: 56 pairs lack a valid ordinary perturbation, 2 are below the
10-valid-perturbation floor, and the maximum valid perturbation count is 125.
That is still not a WRR reproduction because the final pair universe and
`D(w)` formula remain unlocked. A variant comparison now checks term-printed,
term-program, and fixed-250 skip settings side by side: all three produce 28
defined corrected distances at cap 250.

The separate direct all-lane diagnostic over all 182 imported same-record pairs
has 50 defined values at cap 250 and 72 defined values at cap 1000. It is
tracked in `docs/WRR_DIRECT_ALL_LANES_DIAGNOSTIC.md` and
`protocols/wrr_corrected_distance_direct_all_lanes.toml`. A cap-1000
reported-program formula rerun produced 0 changed pair rows versus the printed
formula in this diagnostic.
The defined pair-set audit in `scripts/analyze_wrr_defined_pair_set.py` joins
those outputs to pair-lane and review-status labels; current tracked output is
`docs/WRR_DEFINED_PAIR_SET_AUDIT.md`.
The defined-gap reason audit in
`scripts/analyze_wrr_defined_gap_reasons.py` classifies why the best current
run remains short of 163; current tracked output is
`docs/WRR_DEFINED_GAP_REASON_AUDIT.md`.
Implementation notes are now tracked in
`docs/WRR_CORRECTED_DISTANCE_NOTES.md`.

Needed next for exact published reproduction:

- recover citable source-policy or pair-rule evidence for WNP/context-reviewed rows;
- explain the 163 source-cited defined-distance count from an independently
  locked source/method chain;
- state exact method equivalence or mismatch for printed `D(w)` versus the WRR
  program formula documented by MBBK;
- keep the current local cap-1000 corrected-distance/permutation run labeled
  as locked local evidence, not exact published reproduction.

### 4. Term-Specific Skip Caps

Older pair/control screens used fixed broad search caps. WRR uses term-specific
skip windows tied to expected ELS counts.

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

Fixed `max_skip=250` remains smoke/audit evidence only. The selected local
locked-method run uses term-specific `D(w)` under the printed WRR formula as
the main rule and carries the reported-program formula as sensitivity output.

### 5. Aggregate Statistic And Permutations

The repo has tested helpers for `P1`, `P2`, permutation rank, and Bonferroni
`rho0`, plus a P1..P4 aggregate diagnostic over already-defined
corrected-distance rows. Current cap-250 smoke output has 28 defined c-values
and diagnostic P1 `0.000373062903552`, P2 `5.981029379e-05`, P3
`0.000349191888979`, and P4 `7.69538206457e-05`. Current cap-1000 split output
has 46 defined c-values and diagnostic P1 `0.00220968684352`, P2
`6.37334076429e-06`, P3 `0.0108669973844`, and P4 `8.66346313541e-05`.
Current cross-pair cap-250 permutation output uses 1,000 date-label shuffles
over 30 concepts; the observed same-record rows have 50 defined c-values and
diagnostic rho0 `0.003996003996`. The locked local cap-1000 keep-all
999,999-permutation run uses the selected full source universe over 182
observed rows with 72 defined c-values and Bonferroni rho0 `0.000404`. That
locks the repo-defined local evidence path. The repo still needs exact
published-reproduction closure that:

- verifies independent source transcriptions;
- verifies the selected `D(w)` and permutation procedure against the published WRR
  procedure or states the mismatch;
- records whether the run reproduces, fails to reproduce, or remains
  under-specified against the published claim.

## Review Rule

Treat the selected keep-all cap-1000 output as locked local evidence only. Move
to exact published WRR reproduction language only after the source policy, pair
set, method-equivalence statement, 163 defined-distance explanation, and
permutation procedure are independently locked.
