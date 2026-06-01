# KJVA Hakkaac Apocrypha Marker Coverage

Status: marker-coverage audit only.

This is not an ELS result, not a corpus import, not a source lock, and not a result-bearing replication.
It scans Hakkaac KJV Apocrypha pages for visible chapter and verse markers only.
It does not commit Bible text, normalize Bible text, create a local corpus, split prose, or authorize a result-bearing run.

## Summary

- Pages scanned: 14.
- Exact book marker matches: 14/14.
- Count-drift books: 0.
- Source markers: 5720.
- Local markers: 5720.
- Chapter rows: 173.
- Chapter drift rows: 0.
- Pages with public-domain note: 14.
- Source-lock ready: 0.
- Result-ready sources: 0.
- Claim status: `marker_coverage_audit_only_not_result_bearing`.

## Book Rows

| Book | Title | Source markers | Local markers | Chapters | Status | Candidate status |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `TOB` | Tobit | 244 | 244 | 14 | `exact_marker_match` | `hakkaac_exact_marker_match_candidate_not_source_lock` |
| `JDT` | Judith | 339 | 339 | 16 | `exact_marker_match` | `hakkaac_exact_marker_match_candidate_not_source_lock` |
| `ESG` | Additions to Esther (Greek) | 105 | 105 | 7 | `exact_marker_match` | `hakkaac_exact_marker_match_candidate_not_source_lock` |
| `WIS` | Wisdom of Solomon | 436 | 436 | 19 | `exact_marker_match` | `hakkaac_exact_marker_match_candidate_not_source_lock` |
| `SIR` | Sirach | 1393 | 1393 | 51 | `exact_marker_match` | `hakkaac_exact_marker_match_candidate_not_source_lock` |
| `BAR` | Baruch | 213 | 213 | 6 | `exact_marker_match` | `hakkaac_exact_marker_match_candidate_not_source_lock` |
| `S3Y` | Prayer of Azarias/Azariah | 68 | 68 | 1 | `exact_marker_match` | `hakkaac_exact_marker_match_candidate_not_source_lock` |
| `SUS` | Susanna | 64 | 64 | 1 | `exact_marker_match` | `hakkaac_exact_marker_match_candidate_not_source_lock` |
| `BEL` | Bel and the Dragon | 42 | 42 | 1 | `exact_marker_match` | `hakkaac_exact_marker_match_candidate_not_source_lock` |
| `1MA` | 1 Maccabees | 924 | 924 | 16 | `exact_marker_match` | `hakkaac_exact_marker_match_candidate_not_source_lock` |
| `2MA` | 2 Maccabees | 555 | 555 | 15 | `exact_marker_match` | `hakkaac_exact_marker_match_candidate_not_source_lock` |
| `1ES` | 1 Esdras | 448 | 448 | 9 | `exact_marker_match` | `hakkaac_exact_marker_match_candidate_not_source_lock` |
| `MAN` | Prayer of Manasses | 15 | 15 | 1 | `exact_marker_match` | `hakkaac_exact_marker_match_candidate_not_source_lock` |
| `2ES` | 2 Esdras | 874 | 874 | 16 | `exact_marker_match` | `hakkaac_exact_marker_match_candidate_not_source_lock` |

## Read

All 14 Hakkaac Apocrypha pages expose the same chapter and visible verse-marker counts as the local KJVA Apocrypha corpus.
This includes `SIR` and `MAN`, the two boundary blockers found in the Project Gutenberg source-lock blocker packet.
The audit strengthens Hakkaac as a possible split-source replication candidate, but only at marker level.

## Boundary

No Bible text is written to tracked outputs.
This page does not change KJVA bridge result status.
Next source-use work still needs policy lock, local ignored text import if allowed, verse mapping, collation against current eBible KJVA, checksums, term lock, and study-lock sidecar.
