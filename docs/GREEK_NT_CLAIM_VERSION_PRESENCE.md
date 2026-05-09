# Greek NT Claim Version Presence

This is the tracked summary for the Greek NT claim-term exact-hit
version-presence run:

```bash
python3 -m scripts.run_protocol protocols/greek_nt_claim_version_presence.toml --resume
```

## Scope

- Term source: `terms/greek_nt_claim_terms.csv`
- Corpora: `TR_NT`, `BYZ_NT`, `TCG_NT`, `SBLGNT`
- Skip range: `2..100`
- Direction: `both`
- Minimum normalized term length: `4`
- Max hits: `100` per term per corpus

The report groups hits by exact ref-key pattern:

`term_id + normalized_term + signed_skip + direction + canonical start/center/end refs`

NT book labels are canonicalized so eBible USFM refs such as `MAT 1:1` align
with SBLGNT refs such as `Matt 1:1`.

## Output

Ignored local outputs:

- `reports/greek_nt_claim_version_presence/hit_patterns.csv`
- `reports/greek_nt_claim_version_presence/term_summary.csv`
- `reports/greek_nt_claim_version_presence/greek_nt_claim_version_presence.md`
- `reports/greek_nt_claim_version_presence/manifest.json`

Latest run:

- Runtime: `12.495s`
- Declared terms: `32`
- Summary rows: `32`
- Hit records: `1,467`
- Exact pattern rows: `787`

Pattern scope counts:

| Scope | Pattern rows |
| --- | ---: |
| `present_all_observed_sources` | 109 |
| `present_multiple_sources` | 250 |
| `source_specific` | 428 |

Source-specific rows:

| Source | Rows |
| --- | ---: |
| `SBLGNT` | 212 |
| `BYZ_NT` | 97 |
| `TR_NT` | 73 |
| `TCG_NT` | 46 |

## Current Read

Greek NT exact-hit rows are more version-sensitive than Hebrew MT-family rows.
The top recurring pattern is not all-source stability, but either:

- `SBLGNT`-only rows; or
- `BYZ_NT,TCG_NT,TR_NT` rows absent from SBLGNT.

Top all-source claim rows:

- `αιμα` / blood: 73 all-source exact patterns.
- `μαρια` / Mary: 19 all-source exact patterns.
- `ταφοσ` / tomb: 6 all-source exact patterns.
- `σωτηρ` / savior: 5 all-source exact patterns.
- `ανεστη` / he is risen: 2 all-source exact patterns.

Zero-hit rows: `14` of `32`, mostly longer phrases and nominal forms:

- Lamb of God phrase forms
- Ascension
- Resurrection noun
- Christ
- Second Coming
- Son of God phrase forms
- Jesus Christ
- Jesus Lord

## Caution

This is a capped hit-presence matrix, not a significance test. It is useful for
sorting Greek NT rows into all-source, multi-source, and source-specific review
queues. It does not make a theological or textual claim by itself.
