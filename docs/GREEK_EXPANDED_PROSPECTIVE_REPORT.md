# Greek Expanded Prospective Report

Status: prospective screen complete; no claim.

This report records the first run after
`docs/GREEK_EXPANDED_PROSPECTIVE_PREREGISTRATION.md` and
`terms/greek_expanded_prospective_terms.csv` were committed.

## Run

| Field | Value |
| --- | --- |
| Local report build commit | recorded in local manifest only |
| Command | `python3 -m scripts.run_protocol protocols/greek_expanded_prospective_exact_center.toml --resume` |
| Protocol | `protocols/greek_expanded_prospective_exact_center.toml` |
| Started UTC | `2026-05-05T23:59:36.462848+00:00` |
| Ended UTC | `2026-05-06T00:00:01.087331+00:00` |
| Runtime | 24.624s |
| Status | success |

For resumed protocol runs, this subreport can remain cached. The build
commit is recorded in the local manifest; top-level
assembly reports record their own current commit.

## Locked Scope

| Field | Value |
| --- | --- |
| Term file | `terms/greek_expanded_prospective_terms.csv` |
| Term rows | 291 |
| Prior exact-center cohort terms | excluded by normalized Greek form |
| Corpora | TR_NT, BYZ_NT, TCG_NT, SBLGNT |
| Skip range | `2..50` |
| Direction | both |
| Minimum term length | 4 |
| Extension phrase length | up to 4 words |
| Top rows per corpus | 3000 |

## Surface-Context Counts

| Corpus | Raw hits | Context hits | Exact-center hits | Exact-span hits |
| --- | ---: | ---: | ---: | ---: |
| BYZ_NT | 15,744 | 1,148 | 85 | 144 |
| SBLGNT | 15,638 | 1,160 | 69 | 121 |
| TCG_NT | 15,704 | 1,134 | 88 | 148 |
| TR_NT | 15,745 | 1,071 | 85 | 141 |

Top exact-center surface terms:

| Corpus | Term | Concept | Exact-center hits |
| --- | --- | --- | ---: |
| BYZ_NT | `αμην` (amen; English: Amen) | Amen | 26 |
| BYZ_NT | `δασα` (dasa; English: Lasha) | Lasha | 10 |
| BYZ_NT | `σιων` (sion; English: Zion) | Zion | 9 |
| BYZ_NT | `χουσ` (chous; English: Cush) | Cush | 6 |
| BYZ_NT | `ασηρ` (aser; English: Asher) | Asher | 4 |
| SBLGNT | `αμην` (amen; English: Amen) | Amen | 21 |
| SBLGNT | `σιων` (sion; English: Zion) | Zion | 10 |
| SBLGNT | `δασα` (dasa; English: Lasha) | Lasha | 8 |
| SBLGNT | `αραμ` (aram; English: Aram) | Aram | 4 |
| SBLGNT | `χουσ` (chous; English: Cush) | Cush | 4 |
| TCG_NT | `αμην` (amen; English: Amen) | Amen | 26 |
| TCG_NT | `δασα` (dasa; English: Lasha) | Lasha | 10 |
| TCG_NT | `σιων` (sion; English: Zion) | Zion | 10 |
| TCG_NT | `χουσ` (chous; English: Cush) | Cush | 9 |
| TCG_NT | `αραμ` (aram; English: Aram) | Aram | 4 |
| TR_NT | `αμην` (amen; English: Amen) | Amen | 28 |
| TR_NT | `χουσ` (chous; English: Cush) | Cush | 9 |
| TR_NT | `δασα` (dasa; English: Lasha) | Lasha | 8 |
| TR_NT | `σιων` (sion; English: Zion) | Zion | 8 |
| TR_NT | `ιουδα` (iouda; English: Judah) | Judah | 6 |

## Phrase-Extension Pattern Matrix

| Scope | Patterns |
| --- | ---: |
| none | 0 |

Total exact-center phrase-extension patterns: 0.

## Read

The prospective expanded screen produced exact-center surface hits, but no
same-skip phrase-extension rows survived the locked exact-center pattern
presence filter. Under the preregistered routing rules, no row enters the
control queue from this run.

This is a useful negative result. It means the stricter phrase-extension
gate is selective when applied to 291 new Greek terms, and the previous
`δοξα` (doxa; English: glory) row was not trivially reproduced by a larger nearby term list.

## Next Step

The next defensible move is to choose one of two locked paths:

- run controls only if a future rerun changes the pattern matrix;
- define a separate prospective study for exact-center surface hits without
  requiring same-skip phrase extension.

Do not promote raw exact-center surface hits from this run as claims.
