# KJVA Hakkaac Apocrypha Boundary Candidate

Status: candidate audit only.

This is not an ELS result, not a corpus import, not a source lock, and not a result-bearing replication.
It scans Hakkaac KJV Apocrypha pages for visible verse markers only.
It does not commit Bible text, normalize Bible text, create a local corpus, split unmarked prose, or authorize a result-bearing run.

## Summary

- Pages scanned: 2.
- Pages with public-domain note: 2.
- Sirach 44 marker count: 23.
- Sirach 44 has marker 23: 1.
- Prayer of Manasseh marker count: 15.
- Prayer of Manasseh has markers 1..15: 1.
- Candidate resolves Sirach blocker: 1.
- Candidate resolves Prayer blocker: 1.
- Source-lock ready: 0.
- Result-ready sources: 0.
- Claim status: `candidate_audit_only_not_result_bearing`.

## Marker Rows

| Page | Book | Chapter | Markers | Target | Status | Candidate status |
| --- | --- | --- | --- | --- | --- | --- |
| `hakkaac_sirach_44` | SIR | 44 | `1..23` | `23` | `all_target_markers_present` | `sirach_marker_gap_candidate_not_source_lock` |
| `hakkaac_manasseh_1` | MAN | 1 | `1..15` | `1..15` | `all_target_markers_present` | `prayer_boundary_candidate_not_source_lock` |

## Read

This candidate helps the Prayer of Manasseh boundary question because the page exposes markers 1..15.
This candidate helps the Sirach marker-gap question because the Sirach 44 page exposes marker 23.
Any use still needs a source-use decision, checksum lock, collation against current KJVA, source-order rule, and study-lock sidecar before results.

## Boundary

No Bible text is written to tracked outputs.
This page does not change KJVA bridge result status.
