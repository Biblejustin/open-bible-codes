# Greek Surface New Terms Prospective Report

Status: prospective_controlled_review_material; no claim.

This is the first locked Greek surface new-terms prospective run over the clean user-requested term lock after prior selected rows were removed.

## Lock

| Field | Value |
| --- | --- |
| Lock commit | `e9db94c` |
| Lock dirty-state | `False` |
| Preflight status | `passed` |
| Preflight artifact | `reports/study_locks/greek_surface_new_terms.preflight.json` |
| Protocol status | `written after report step` |
| Term rows | 236 |
| Skip range | `2..50` |
| Direction | `both` |
| Minimum normalized length | `5` |

## Result

| Stage | Count |
| --- | ---: |
| Exact-center surface hit rows | 78 |
| Unique exact-center surface patterns | 38 |
| All-source patterns | 9 |
| Multi-source patterns | 8 |
| Source-only patterns | 21 |
| Selected rows under registered all-source length-5 rule | 9 |
| Control rows evaluated | 5 |

## Triage Buckets

| Bucket | Terms |
| --- | ---: |
| multi-source broader surface queue | 4 |
| no exact-center surface pattern | 221 |
| selected | 5 |
| source-specific broader surface queue | 6 |

## Top Queue Before Primary Filter

| Term | Concept | Exact-center hits | All-source | Multi-source | Source-only |
| --- | --- | ---: | ---: | ---: | ---: |
| `ονομα` (onoma; English: Name) | ὄνομα | 38 | 5 | 3 | 12 |
| `οικοσ` (oikos; English: House) | οἶκος | 7 | 1 | 1 | 0 |
| `σοφια` (sophia; English: wisdom) | σοφία | 4 | 1 | 0 | 0 |
| `θυσια` (thusia; English: Sacrifice) | θυσία | 4 | 1 | 0 | 0 |
| `σκηνη` (skene; English: Tabernacle) | σκηνή | 4 | 1 | 0 | 0 |
| `αρτοσ` (artos; English: Bread) | ἄρτος | 4 | 0 | 1 | 1 |
| `σιμων` (simon; English: Simon the Zealot) | Simon the Zealot | 4 | 0 | 1 | 1 |
| `τοξον` (toxon) | τόξον | 3 | 0 | 1 | 0 |
| `ιεσσαι` (iessai; English: Jesse) | Jesse | 3 | 0 | 1 | 0 |
| `στομα` (stoma) | στόμα | 2 | 0 | 0 | 2 |

## Registered Outcome

Rows with all_source_q_value <= 0.05: 5.

The primary filter was deliberately stricter than the exploratory queue: all-source exact-center surface rows had to have normalized length at least 5. This run produced 9 selected review rows for matched-control interpretation.

## Interpretation Boundary

This is controlled review material, not a theological, prophetic, historical, or statistical claim. 5 control-summary rows met the registered q<=0.05 threshold and need manual review.
