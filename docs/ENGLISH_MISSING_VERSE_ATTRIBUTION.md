# English Missing-Verse Attribution

Status: current local attribution check for the English KJV-vs-modern-version
comparison.

## Setup

The earlier English version-control triage compared KJV-oriented English search
rows against the available local BibleGateway-overlap English versions. This
page answers a narrower follow-up question: whether the reviewed English rows
are explained by verses that appear as KJV references but are absent from a
modern version's local verse list.

The attribution protocol is:

- `protocols/english_missing_verse_attribution.toml`

The main script is:

- `scripts/analyze_english_missing_verse_attribution.py`

Local outputs are under:

- `reports/english_missing_verse_attribution/`

Those report files are local generated data and stay ignored by git.

## Method

For each available English version, the script compares its verse references
with the KJV baseline.

If a KJV reference is absent from the compared version, the script records that
as a reference gap. It also marks known New Testament disputed KJV references,
such as Matthew 17:21, Mark 9:44, John 5:4, Acts 8:37, and Romans 16:24.

This does not mean every reference gap is a missing-verse claim. Some gaps are
ordinary versification differences, combined verses, Catholic or Protestant
canon differences, or source-file reference choices.

For the current reviewed English hit rows, the script splices the absent KJV
verse references back into the compared version and checks whether the existing
hidden-letter path would keep the same skip. If the path crosses inserted KJV
references and the spacing changes, it is counted as missing-verse-attributed.

The default protocol uses fast mode. It attributes the existing context-review
rows only. It does not rerun a full seed search across every version. The full
seed rescan remains available with `--full-seed-scan`, but it is slower and is
not needed to answer the current reviewed-hit question.

## Results

Current run:

- Available BibleGateway-overlap English versions checked: 34.
- Missing BibleGateway versions skipped: 30.
- Versions with at least one KJV reference absent: 26.
- Reference-gap rows: 27,050.
- Known New Testament disputed KJV-reference rows: 290 across 23 versions.
- Current context-review rows checked: 2.
- Context-review rows attributed to missing verses: 0.

The two reviewed English rows were:

| Version | Hidden term | Span | Attribution |
| --- | --- | --- | --- |
| ERV | `hamathite` | 2 Samuel 17:19 to 2 Samuel 17:15 | not missing-verse related |
| NET | `disciple` | 1 Thessalonians 2:14 to 1 Thessalonians 3:1 | not missing-verse related |

So the answer for the current reviewed English rows is: no. The current
reviewed English hits are not explained by missing-verse gaps. If they differ
between KJV and modern English versions, the likely explanation is changed
translation wording, word order, paraphrase style, spacing, or ordinary ELS
background rather than an absent KJV-only verse.

The reference-gap table still matters. It confirms that many modern English
versions do omit or skip familiar KJV-reference verses in the New Testament.
That is useful source context. It just does not explain the two current
reviewed English rows.

## Files

- `reports/english_missing_verse_attribution/summary.csv`
- `reports/english_missing_verse_attribution/missing_refs.csv`
- `reports/english_missing_verse_attribution/missing_verse_attributed_hits.csv`
- `reports/english_missing_verse_attribution/context_hit_attribution.csv`
- `reports/english_missing_verse_attribution/summary.md`
- `reports/english_missing_verse_attribution/manifest.json`

## Cautions

This is an attribution check, not a new claim search.

Reference gaps are broader than textual omissions. A reference can be absent
because a version combines verses, changes verse numbering, follows a different
canon, or stores the source file differently.

This check does not classify smaller wording changes inside shared verses. The
Comma Johanneum is the clearest example: many versions still have a 1 John 5:7
reference, but the wording differs. That kind of change requires wording-level
comparison, not reference-gap attribution.

Raw English ELS rows remain weak unless they survive controls. English
translation results are secondary to original-language work.
