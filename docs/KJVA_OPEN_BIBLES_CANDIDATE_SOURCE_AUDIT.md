# KJVA Open-Bibles Candidate Source Audit

Status: source-status audit only. This is not an ELS result, not a
corpus import, and not a claim-ready replication.

## Setup

This audit checks GitHub repository metadata for the seven1m/open-bibles
candidate. It records repository JSON, tree path counts, and README
markers only. It does not download, retain, normalize, or commit Bible
text.

Primary candidate:

- https://github.com/seven1m/open-bibles

## Findings

- Metadata rows checked: 1.
- Metadata fetches complete: 1.
- KJV path markers: 1.
- Apocrypha path markers: 0.
- Deuterocanon path markers: 0.
- Verse-numbered import ready pages: 0.
- Result-ready pages: 0.

Current read: this repository is useful as a KJV-only OSIS metadata
candidate, but current tree metadata does not show apocrypha or
deuterocanon coverage. It is not a KJVA/apocrypha source candidate until
a separate source audit finds lawful apocrypha coverage.

## Parsed Shape

| Item | Count |
| --- | ---: |
| source pages | 1 |
| metadata fetches ok | 1 |
| KJV paths | 1 |
| Apocrypha paths | 0 |
| Deuterocanon paths | 0 |
| verse import ready pages | 0 |
| result ready pages | 0 |

## Page Status

| Source | Repo | Tree | README | Branch | KJV Paths | Apocrypha Paths | Deuterocanon Paths | Status |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| seven1m_open_bibles_kjv_osis | fetched | fetched | fetched | master | 1 | 0 | 0 | kjv_only_not_kjva_source_candidate |

## Protocol Anchors

Found anchors: 4 of 4.

| Source | Anchor | Status | Diagnostic |
| --- | --- | --- | --- |
| open_bibles | `metadata_fetch_status_recorded` | found | repository and tree fetch status are recorded |
| open_bibles | `kjv_path_recorded` | found | KJV OSIS path is recorded from tree metadata |
| open_bibles | `apocrypha_absence_recorded` | found | no apocrypha/deuterocanon path marker is present in tree metadata |
| open_bibles | `result_not_ready` | found | no result-bearing replication is declared ready |

## Use Boundary

This audit does not import Bible text, normalize verses, run ELS
searches, evaluate controls, or upgrade the completed KJVA bridge
lane. It only records that current seven1m/open-bibles metadata has
KJV OSIS coverage without visible apocrypha/deuterocanon path coverage.
