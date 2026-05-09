# Greek Surface Prospective Report

Status: negative_primary_filter_result; no claim.

This is the first locked Greek surface prospective run after removing
the prior selected surface rows from the expanded Greek term list.

## Lock

| Field | Value |
| --- | --- |
| Lock commit | `79f5c93` |
| Lock dirty-state | `False` |
| Preflight status | `passed` |
| Preflight artifact | `reports/study_locks/greek_surface_prospective.preflight.json` |
| Protocol status | `written after report step` |
| Term rows | 288 |
| Skip range | `2..50` |
| Direction | `both` |
| Minimum normalized length | `5` |

## Result

| Stage | Count |
| --- | ---: |
| Exact-center surface hit rows | 303 |
| Unique exact-center surface patterns | 151 |
| All-source patterns | 24 |
| Multi-source patterns | 53 |
| Source-only patterns | 74 |
| Selected rows under registered all-source length-5 rule | 0 |
| Control rows evaluated | 0 |

## Triage Buckets

| Bucket | Terms |
| --- | ---: |
| all-source but below length threshold | 7 |
| multi-source broader surface queue | 10 |
| no exact-center surface pattern | 265 |
| source-specific broader surface queue | 6 |

## Top Queue Before Primary Filter

| Term | Concept | Exact-center hits | All-source | Multi-source | Source-only |
| --- | --- | ---: | ---: | ---: | ---: |
| `αμην` | Amen | 101 | 11 | 14 | 19 |
| `σιων` | Zion | 37 | 4 | 5 | 8 |
| `αραμ` | Aram | 14 | 3 | 0 | 2 |
| `δασα` | Lasha | 36 | 2 | 7 | 12 |
| `ασηρ` | Asher | 14 | 2 | 2 | 1 |
| `χουσ` | Cush | 28 | 1 | 6 | 10 |
| `σαβα` | Seba | 9 | 1 | 2 | 0 |
| `ιουδα` | Judah | 14 | 0 | 4 | 3 |
| `λεων` | Lion | 9 | 0 | 3 | 2 |
| `αδαμ` | Adam | 7 | 0 | 2 | 2 |

## Registered Outcome

No row met the registered all-source exact-center surface plus length-5 rule. Therefore no control p/q values were computed and the study produced no prospective controlled review candidate.

The primary filter was deliberately stricter than the exploratory queue:
all-source exact-center surface rows had to have normalized length at
least 5. The run found all-source rows only in the dense length-4 bucket
after prior selected rows were removed.

## Interpretation Boundary

This is a valid negative result for the registered primary gate. It does
not make a theological, prophetic, historical, or statistical claim. It
does preserve lower-strength queue data for later separately locked
studies, especially if a future study explicitly registers length-4 rows.
