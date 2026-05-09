# Greek LXX / NT Corpus Presence

This is a focused read from the broad skip `2..100` count run:

```bash
python3 -m scripts.run_protocol protocols/broad_search.toml --resume
```

Relevant ignored output:

- `reports/broad_search/broad_version_presence.csv`

## Scope

- Term set: `terms/greek_nt_claim_terms.csv`
- Corpora: `LXX`, `TR_NT`, `BYZ_NT`, `TCG_NT`, `SBLGNT`
- Skip range: `2..100`
- Direction: `both`

This is not exact ref-key version comparison. LXX and NT corpora do not share a
single verse coordinate system. This report only asks whether each Greek claim
term has at least one ELS hit in each corpus.

## Summary

| Scope | Terms |
| --- | ---: |
| Present in all observed corpora | 14 |
| Present in multiple observed corpora | 4 |
| Source-specific | 2 |
| Absent in all observed corpora | 12 |

## Present In All Five Greek Corpora

| Term | Normalized | Total hits | Hits by corpus |
| --- | --- | ---: | --- |
| Blood | `αιμα` | 40,429 | BYZ_NT:4,621; LXX:22,054; SBLGNT:4,527; TCG_NT:4,575; TR_NT:4,652 |
| Mary | `μαρια` | 1,403 | BYZ_NT:156; LXX:780; SBLGNT:153; TCG_NT:152; TR_NT:162 |
| Tomb | `ταφοσ` | 394 | BYZ_NT:46; LXX:205; SBLGNT:52; TCG_NT:42; TR_NT:49 |
| Savior | `σωτηρ` | 281 | BYZ_NT:27; LXX:154; SBLGNT:29; TCG_NT:35; TR_NT:36 |
| He Is Risen | `ανεστη` | 192 | BYZ_NT:28; LXX:92; SBLGNT:22; TCG_NT:26; TR_NT:24 |
| Jesus | `ιησουσ` | 140 | BYZ_NT:12; LXX:78; SBLGNT:23; TCG_NT:12; TR_NT:15 |
| Judgment | `κρισισ` | 99 | BYZ_NT:11; LXX:61; SBLGNT:13; TCG_NT:8; TR_NT:6 |
| Judas | `ιουδασ` | 76 | BYZ_NT:11; LXX:44; SBLGNT:8; TCG_NT:7; TR_NT:6 |
| Lord | `κυριοσ` | 63 | BYZ_NT:10; LXX:35; SBLGNT:3; TCG_NT:7; TR_NT:8 |
| Peter | `πετροσ` | 60 | BYZ_NT:10; LXX:24; SBLGNT:11; TCG_NT:8; TR_NT:7 |

## Partial Presence

| Term | Normalized | Present | Absent | Total hits |
| --- | --- | --- | --- | ---: |
| Beast | `θηριον` | BYZ_NT, LXX, TCG_NT, TR_NT | SBLGNT | 14 |
| Dragon | `δρακων` | LXX, TCG_NT, TR_NT | BYZ_NT, SBLGNT | 7 |
| John | `ιωαννησ` | LXX, TCG_NT | BYZ_NT, SBLGNT, TR_NT | 4 |
| Pilate | `πιλατοσ` | LXX, SBLGNT | BYZ_NT, TCG_NT, TR_NT | 2 |
| Christ | `χριστοσ` | LXX only | BYZ_NT, SBLGNT, TCG_NT, TR_NT | 1 |
| He Is Coming | `ερχεται` | LXX only | BYZ_NT, SBLGNT, TCG_NT, TR_NT | 1 |

## Absent In This Broad Scan

Twelve Greek claim rows are absent across LXX and all four NT corpora at this
skip range:

- Lamb of God forms
- Ascension
- Resurrection noun
- Apocalypse noun
- Second Coming phrase
- Jerusalem form in this term list
- Son of God phrase forms
- Jesus Christ
- Jesus Lord
- Seal

## Current Read

LXX often has higher raw counts because it is much larger than the NT corpora.
Raw LXX/NT presence is useful for corpus triage, but it is not version support.
For Greek NT version support, use the exact-hit NT version-presence reports.
