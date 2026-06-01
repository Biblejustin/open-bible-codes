# KJVA Hakkaac Apocrypha Collation Audit

Status: ignored local collation audit only.

Source-use decision: Hakkaac was approved for ignored local import and collation only.
This is not an ELS result, not a corpus import, not a source lock, and not a result-bearing replication.
Raw Hakkaac verse text is written only under ignored `data/private/` output.
Tracked outputs record hashes, counts, lengths, refs, and status only; they do not write Bible text.

## Summary

- Pages fetched: 14.
- Local verses: 5720.
- Hakkaac verses: 5720.
- Comparable refs: 5720.
- Exact normalized verse matches: 5719.
- Length-match hash-drift verses: 0.
- Length-drift verses: 1.
- Missing Hakkaac refs: 0.
- Missing local refs: 0.
- Exact book stream matches: 13/14.
- Book stream drift books: 1.
- Local normalized letters: 593090.
- Hakkaac normalized letters: 593091.
- Normalized length delta: 1.
- Apocrypha stream hash match: 0.
- Source-lock ready: 0.
- Result-ready sources: 0.
- Claim status: `ignored_local_collation_audit_only_not_result_bearing`.

## Book Rows

| Book | Title | Exact verses | Drift verses | Missing refs | Letters delta | Stream status |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `TOB` | Tobit | 244 | 0 | 0 | 0 | `exact_normalized_stream_match` |
| `JDT` | Judith | 339 | 0 | 0 | 0 | `exact_normalized_stream_match` |
| `ESG` | Additions to Esther (Greek) | 105 | 0 | 0 | 0 | `exact_normalized_stream_match` |
| `WIS` | Wisdom of Solomon | 436 | 0 | 0 | 0 | `exact_normalized_stream_match` |
| `SIR` | Sirach | 1392 | 1 | 0 | 1 | `stream_drift` |
| `BAR` | Baruch | 213 | 0 | 0 | 0 | `exact_normalized_stream_match` |
| `S3Y` | Prayer of Azarias/Azariah | 68 | 0 | 0 | 0 | `exact_normalized_stream_match` |
| `SUS` | Susanna | 64 | 0 | 0 | 0 | `exact_normalized_stream_match` |
| `BEL` | Bel and the Dragon | 42 | 0 | 0 | 0 | `exact_normalized_stream_match` |
| `1MA` | 1 Maccabees | 924 | 0 | 0 | 0 | `exact_normalized_stream_match` |
| `2MA` | 2 Maccabees | 555 | 0 | 0 | 0 | `exact_normalized_stream_match` |
| `1ES` | 1 Esdras | 448 | 0 | 0 | 0 | `exact_normalized_stream_match` |
| `MAN` | Prayer of Manasses | 15 | 0 | 0 | 0 | `exact_normalized_stream_match` |
| `2ES` | 2 Esdras | 874 | 0 | 0 | 0 | `exact_normalized_stream_match` |

## Drift Rows

| Ref | Status | Local letters | Hakkaac letters | First diff offset |
| --- | --- | ---: | ---: | ---: |
| `SIR 19:1` | `length_drift` | 107 | 108 | 17 |

## Blocker Rows

- Exact blocker rows: 16/16.
- `SIR 44:23` status: `exact_normalized_match`.
- `MAN 1:1..15` status: `exact_normalized_match`.

## Read

This audit answers whether Hakkaac's normalized KJV Apocrypha letter stream matches the current local KJVA Apocrypha source closely enough to remain useful as source evidence.
The blocker rows cover `SIR 44:23` and `MAN 1:1..15`, the two places that blocked Project Gutenberg source-lock work.

## Boundary

No Bible text is written to tracked outputs.
This page does not change KJVA bridge result status.
A future result-bearing run still needs source policy lock, checksum lock, source-order decision, term lock, controls, and a study-lock sidecar.
