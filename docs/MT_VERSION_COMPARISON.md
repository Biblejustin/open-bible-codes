# MT Version Comparison

This is the current normalized Hebrew MT-family comparison after adding UXLC,
MAM, eBible Hebrew WLC, and UHB. It is meant to answer a practical ELS question:
when a term or pattern appears in one Hebrew source but not another, how much
textual drift is present under the same ELS normalization rules?

Command:

```bash
python3 -m scripts.run_protocol protocols/mt_version_comparison.toml --resume
```

Outputs:

- `reports/mt_version_comparison/summary.csv`
- `reports/mt_version_comparison/verse_differences.csv`
- `reports/mt_version_comparison/mt_version_comparison.md`

## Corpus Sizes

| Corpus | Verses | Normalized letters |
| --- | ---: | ---: |
| MT_WLC | 23,213 | 1,197,042 |
| UXLC | 23,213 | 1,197,043 |
| MAM | 23,202 | 1,201,975 |
| EBIBLE_WLC | 23,213 | 1,197,042 |
| UHB | 23,145 | 1,195,624 |

## Pair Summary

| Pair | Shared refs | Equal refs | Different refs | Left-only refs | Right-only refs |
| --- | ---: | ---: | ---: | ---: | ---: |
| MT_WLC vs UXLC | 23,213 | 23,208 | 5 | 0 | 0 |
| MT_WLC vs MAM | 23,200 | 21,319 | 1,881 | 13 | 2 |
| MT_WLC vs EBIBLE_WLC | 23,213 | 23,212 | 1 | 0 | 0 |
| MT_WLC vs UHB | 23,011 | 20,672 | 2,339 | 202 | 134 |
| UXLC vs MAM | 23,200 | 21,316 | 1,884 | 13 | 2 |
| UXLC vs EBIBLE_WLC | 23,213 | 23,207 | 6 | 0 | 0 |
| UXLC vs UHB | 23,011 | 20,668 | 2,343 | 202 | 134 |
| MAM vs EBIBLE_WLC | 23,200 | 21,319 | 1,881 | 2 | 13 |
| MAM vs UHB | 23,001 | 19,367 | 3,634 | 201 | 144 |
| EBIBLE_WLC vs UHB | 23,011 | 20,671 | 2,340 | 202 | 134 |

## MT_WLC vs UXLC

The two Leningrad-family streams are very close after the project’s ELS
normalization. The current normalized-verse difference list has only five refs:

- `2Sam 13:37`
- `2Sam 14:7`
- `Ezek 16:36`
- `Amos 7:2`
- `2Chr 27:4`

This is the useful baseline. If an ELS hit differs between MT_WLC and UXLC, it
is probably tied to one of a small number of normalized textual changes or to
one-letter stream-position shifts downstream from those changes.

## eBible WLC Packaging Check

eBible Hebrew WLC is not treated as a materially independent MT edition. It is
a public-domain USFM package useful for checking whether another WLC packaging
creates different normalized streams.

The eBible package includes standalone Hebrew paragraph markers (`פ` (pe; English: open paragraph marker) / `ס` (samekh; English: closed paragraph marker)) in
the verse text. The importer strips those before ELS normalization. After that:

- eBible WLC has the same normalized length as MT_WLC: 1,197,042 letters.
- eBible WLC differs from MT_WLC in one normalized verse.
- eBible WLC differs from UXLC in six normalized verses.

Current read: keep EBIBLE_WLC in version-distribution reports as a packaging
check, but do not count it as an independent textual witness like MAM.

## UHB Compared With Leningrad Streams

UHB is useful, but it is not just another WLC packaging. It is a CC BY-SA
USFM 3.0 stream based on OSHB/WLC with ULT-style versification, selected
ketiv/qere decisions, and some alternate readings.

After stripping USFM markup and Hebrew paragraph markers:

- UHB has 23,145 parsed verses and 1,195,624 normalized letters.
- Against MT_WLC, it shares 23,011 refs.
- 20,672 shared refs are normalized-identical against MT_WLC.
- 2,339 shared refs differ against MT_WLC.
- MT_WLC has 202 left-only refs and UHB has 134 right-only refs under canonical
  ref alignment.

Current read: include UHB in version-distribution reports, but label it as a
derived MT-family stream. For ELS, a UHB-only hit may reflect versification,
ketiv/qere selection, or alternate readings rather than a simple manuscript
difference.

## MAM Compared With Leningrad Streams

MAM is more different, as expected. It is a Masorah-reader edition rather than
another direct Leningrad transcription. Current comparison shows:

- About 21.3k shared refs are normalized-identical against the Leningrad streams.
- About 1.9k shared refs have normalized consonantal differences.
- MAM has 23,202 parsed verses, 11 fewer than MT_WLC/UXLC/EBIBLE_WLC and 57
  more than UHB.
- Against MAM, the Leningrad streams have 13 left-only refs and MAM has 2
  right-only refs under canonical ref alignment.

Notable unmatched refs against MAM under canonical ref alignment:

- Leningrad-only in this alignment: `Exod 20:23-26`, `Num 25:19`,
  `Deut 5:30-33`, `Josh 21:44-45`, `1Sam 24:23`, `Jer 31:40`
- MAM-only in this alignment: `1Sam 23:29`, `Jer 30:25`

Some of these are likely verse-boundary and numbering differences, not simple
wording differences. Spot checks confirm that some text is present in MAM under
nearby shifted refs. The generated `verse_differences.csv` keeps full
normalized verse text and first-difference windows for review.

## Use For ELS Work

For Hebrew ELS findings, report version distribution explicitly:

- present in all five observed Hebrew MT-family streams;
- present in both Leningrad-family streams but absent in MAM;
- present in MAM but absent in one or both Leningrad streams;
- present in UHB but absent in one or more other Hebrew streams;
- absent from all observed Hebrew MT-family streams.

The comparison does not establish or refute a pattern. It tells us where textual
variation can plausibly create, move, or break a hit.

## Cautions

- This is a normalized consonantal comparison, not a full diplomatic collation.
- Vowels, cantillation, punctuation, and final-form distinctions are removed
  under normal ELS settings.
- Some left-only/right-only refs reflect versification differences. The text
  can still be present under nearby shifted refs in another corpus.
- Different rows are review queues, not claims.
