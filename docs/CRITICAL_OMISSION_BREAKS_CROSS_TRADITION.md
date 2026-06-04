# Critical Omission Breaks Cross Tradition

## Setup

Run:

```bash
python3 -m scripts.analyze_critical_omission_breaks_cross_tradition
```

Outputs:

- `reports/critical_omission_breaks_cross_tradition.csv`
- `reports/critical_omission_breaks_cross_tradition.manifest.json`

## Method

The script reads `reports/critical_omission_breaks_examples.csv`, then checks
each TR broken hit against:

- eBible Greek Majority Text NT (`configs/example_ebible_grcmt.toml`)
- eBible Text-Critical Greek NT (`configs/example_ebible_grctcgnt.toml`)

It maps start/end refs and verse-local offsets into the comparison corpus and
checks whether the same normalized term appears at the same skip.

## Results

Current output rows: 558, one per TR broken example row.

Classes:

- `preserved_by_byz_and_tcg`: 163.
- `preserved_by_byz`: 0.
- `preserved_by_tcg`: 157.
- `tr_specific_under_equivalent_offsets`: 238.

Comparison status counts:

- BYZ_NT preserved equivalent offsets: 163.
- BYZ_NT ref missing: 192.
- BYZ_NT coordinate mismatch: 150.
- BYZ_NT not preserved equivalent offsets: 53.
- TCG_NT preserved equivalent offsets: 320.
- TCG_NT ref missing: 192.
- TCG_NT coordinate mismatch: 36.
- TCG_NT not preserved equivalent offsets: 10.

## Stage 1 Proximity (added)

The strict equivalent-offset test maps each TR hit's letter offsets verse-locally
into the comparison corpus and requires an exact match. It miscounts when
upstream word-length deltas (movable nu, article presence, verb-ending variants)
shift every offset even though the same ELS is physically present at the same
skip. For BYZ_NT that conservative mapping put 150 hits in `coordinate_mismatch`
that may in fact be preserved.

The script now also emits a proximity classification that tolerates those
deltas: `byz_proximity_status`, `tcg_proximity_status`,
`cross_tradition_class_proximity`, and `window_verses`. A hit is
`preserved_within_verse_span` when the same query occurs at the same skip within
`--window-verses` (default 2) of the hit's verse span in the comparison corpus.
The mechanic is `els.critical.verse_span_preserved`, unit-tested on toy corpora;
the proximity test is a strict superset of the equivalent-offset test (any
`preserved_equivalent_offsets` hit is also `preserved_within_verse_span`).

The strict columns and counts above are unchanged. Reproduce with:

```bash
python3 -m scripts.analyze_critical_omission_breaks_cross_tradition --window-verses 2
```

Proximity status counts (window 2):

- BYZ_NT preserved within verse span: 260.
- BYZ_NT omitted in comparison tradition: 192.
- BYZ_NT not preserved within window: 106.
- TCG_NT preserved within verse span: 341.
- TCG_NT omitted in comparison tradition: 192.
- TCG_NT not preserved within window: 25.

Proximity cross-tradition classes:

- `preserved_by_byz_and_tcg`: 260.
- `omitted_in_byz_and_tcg`: 192.
- `preserved_by_tcg`: 81.
- `tr_specific_within_window`: 25.

Read: tolerating word-length deltas recovers 97 BYZ and 21 TCG hits the strict
test mislabelled. BYZ_NT preservation rises from 163 to 260. Of the 558 broken
hits, 260 (47%) sit at the same skip in both the Byzantine and critical
traditions, 81 (15%) in the critical text only, and just 25 (4%) are genuinely
TR-specific yet unexplained.

## Shared-Omission Floor (Stage 2 result)

The 192 hits that do not resolve in BYZ_NT or TCG_NT are **not** a versification
artifact. They trace to seven verses the Byzantine Majority text and the
critical text both omit, with the verse number simply skipped (Acts 8 runs
...36, 38, ...), not renumbered:

- Romans 16:25, 16:26, 16:27 (the doxology, absent from BYZ Romans 16 which ends
  at v24).
- Acts 8:37, Acts 15:34, Acts 24:7.
- Luke 17:36.

A versification remap would be wrong here: there is no renumbered verse to map
to, so mapping a hit's letters onto a neighbour would fabricate preservation.
The honest classification is `omitted_in_comparison_tradition` (the
`byz_omitted_refs` / `tcg_omitted_refs` columns name the verse), aggregated as
`omitted_in_byz_and_tcg`. `els.critical.ref_absence_kind` distinguishes an
omitted verse (book+chapter present, verse number absent) from a chapter that is
genuinely absent; it is unit-tested on toy corpora.

The finding: these 192 hits depend on verses nearly unique to the TR/Erasmian
tradition -- verses that entered TR through a few late manuscripts and
back-translation from the Latin, and that TR's own Byzantine family does not
carry. For this pool the framing is not "codes lost in the modern critical
text" but "codes that depend on verses absent from essentially every other
edition." Only 25 of 558 remain a genuine TR-specific residual.

## Window Sensitivity

The proximity test has one free parameter, `--window-verses`. The headline
recovery is robust to it; the shared-omission floor does not depend on it:

| window | BYZ preserved | omitted_in_byz_and_tcg | TCG only | residual |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 237 | 192 | 86 | 43 |
| 1 | 259 | 192 | 82 | 25 |
| 2 | 260 | 192 | 81 | 25 |
| 3 | 264 | 192 | 77 | 25 |
| 5 | 274 | 192 | 68 | 24 |

BYZ preservation is 259-264 across windows 1-3 (and already 237 at window 0,
versus the strict 163), so the recovery is not a window artifact. The 192
omitted floor is identical at every window, as it must be. `window=2` is not
cherry-picked.

## The 25-Hit Residual

The 25 `tr_specific_within_window` hits are TR codes broken by an SBL omission
where BYZ_NT and TCG_NT *retain* the verse but the exact ELS does not reproduce
at that skip. They are all short terms (normalized length 3-6) at moderate-to-
wide skips (|skip| 20-49, median 38) -- e.g. `ναος`, `αιμα`, `νωε`, `ιραν` --
spanning verses such as Luke 23:17 and Matthew 23:14 whose surrounding wording
differs between editions. This is squarely the high-coincidence regime the
project flags elsewhere: short terms at wide skips.

A base-rate estimate (via `els.statistics.estimated_search_space` times each
term's letter-frequency product in BYZ_NT) makes the point concrete: every
residual term is expected to occur in BYZ_NT *by chance* across skips 2-50 from
dozens to tens of thousands of times -- `ευα` (Eve) ~43,000, `νωε` (Noah)
~17,500, `ναος` (temple) ~4,600, and even the 6-letter `σενααρ` ~18. A string
that the text produces thousands of times by chance is not meaningfully
"absent" from a tradition because one windowed instance fails to reproduce.

So the cross-tradition screen surfaces no credible TR-specific code: the 25 are
chance-dominated short strings. A length- and skip-matched shuffled-term control
would formalize this, but the base rates already show the expected outcome.
Treat the 25 as a review queue, not a result.

## Cautions

- Raw break counts are not significance tests.
- Equivalent-offset mapping is conservative and can miss preservation after local wording-length changes.
- This is a robustness screen, not a textual-critical stemma.
