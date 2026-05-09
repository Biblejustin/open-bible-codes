# Version Distribution Method

Status: project methodology note.

This project should not assume that a pattern must appear in every textual
source to be worth review. The better first question is:

> Which exact pattern appears in which source text?

Absence in a source is data. It can weaken a claim, define a source-family
boundary, or point to a version-specific review queue. It should not
automatically delete the row from consideration.

## Working Categories

| Category | Meaning | Maximum Read |
| --- | --- | --- |
| all-source pattern | Same exact key appears in every compared source | strongest review queue item, still not a claim |
| multi-source pattern | Same exact key appears in more than one source but not all | source-family or cross-source review queue |
| source-specific pattern | Same exact key appears in one source only | version-specific review queue |
| absent pattern | Registered term/pattern is absent under the current settings | absence recorded; no review row |

## Required Reporting

Use two different report types:

- exact ref-key version presence for aligned textual traditions, such as Hebrew
  MT-family streams or Greek NT editions;
- broad corpus presence for non-aligned corpora, such as LXX vs Greek NT.

Do not treat LXX as a Greek NT version. LXX/NT comparisons answer corpus
presence questions, not exact version-support questions.

For ELS extension reports, include:

- exact pattern key;
- present corpora;
- absent corpora;
- source-family caveat when sources are related;
- whether row-local controls exist for that exact source distribution;
- whether the matched phrase is surface text in the hit span or hidden-path only.

For broad count reports, include:

- observed corpora for the term row;
- present corpora;
- absent corpora;
- hit counts by corpus;
- warning labels for short forms and acronyms.

For exact-hit version-presence reports, include:

- exact ref-key pattern;
- canonical start, center, and end refs;
- present corpora;
- absent corpora;
- source-specific row counts by corpus;
- matching controls when available.

## Promotion Boundary

Version distribution does not promote a row by itself.

Promotion requires:

- preregistered term list or clearly marked post-discovery follow-up;
- exact source-distribution table;
- row-local controls for the exact source scope being discussed;
- context and letter-path audit;
- hidden-path warning when the matched phrase is not surface text in the hit
  span.

## Current Reports

Greek exact-center pattern/version summary:

- `docs/GREEK_PATTERN_VERSION_SUMMARY.md`
- `reports/greek_pattern_versions/summary.csv`

Hebrew exact-hit version-presence summaries:

- `docs/HEBREW_HIT_VERSION_PRESENCE.md`
- `docs/HEBREW_CLAIM_VERSION_PRESENCE.md`
- `docs/HEBREW_CONTROL_VERSION_PRESENCE.md`
- `docs/HEBREW_SCREENING_VERSION_PRESENCE.md`
- `docs/HEBREW_VERSION_PRESENCE_COMPARISON.md`
- `docs/HEBREW_VERSION_SPECIFIC_DISTRIBUTION.md`

Greek NT exact-hit version-presence summaries:

- `docs/GREEK_NT_CLAIM_VERSION_PRESENCE.md`
- `docs/GREEK_CONTROL_VERSION_PRESENCE.md`
- `docs/GREEK_VERSION_PRESENCE_COMPARISON.md`
- `docs/GREEK_SCREENING_VERSION_PRESENCE.md`

Greek LXX/NT corpus-presence summary:

- `docs/GREEK_LXX_NT_CORPUS_PRESENCE.md`

Broad raw-count version presence:

- `docs/BROAD_SEARCH_FINDINGS.md`
- `reports/broad_search/broad_version_presence.csv`

## Interpretation Boundary

A source-specific row can be worth examining inside that source while still
being much weaker than a cross-source row. None of these categories establish
theological meaning, prophecy, proof, or statistical discovery by themselves.
