# KJVA CrossWire Candidate Source Audit

Status: source-status audit only.

This is not an ELS result, not a corpus import, and not a source lock.
It records GitLab metadata only and does not download, retain, normalize, or commit Bible text.

## Summary

- Source pages: 1.
- Metadata fetches ok: 1.
- Possible independent KJVA metadata candidates: 1.
- KJVA OSIS paths: 1.
- KJVDC XML paths: 1.
- Source-use ready pages: 0.
- Source-lock ready pages: 0.
- Verse-numbered import ready pages: 0.
- Result-ready pages: 0.
- Claim status: `source_status_only_not_result_bearing`.

## Source Rows

| Source | Status | Branch | Tree paths | KJVA OSIS | KJVDC XML | Source use | Source lock | Result |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| crosswire_gitlab_kjva_osis | `possible_independent_kjva_candidate_needs_text_audit` | `master` | 9 | True | True | `needs_rights_review` | `not_source_lock_ready` | `not_result_ready` |

## Anchors

Found anchors: 6/6.

| Source | Anchor | Status | Diagnostic |
| --- | --- | --- | --- |
| crosswire | `metadata_fetch_status_recorded` | `found` | GitLab project and tree fetch status are recorded |
| crosswire | `kjva_osis_path_recorded` | `found` | kjva.osis.xml path is present in tree metadata |
| crosswire | `kjvdc_xml_path_recorded` | `found` | kjvdc.xml path is present in tree metadata |
| crosswire | `source_use_not_ready` | `found` | conf metadata requires rights review before local text import |
| crosswire | `source_lock_not_ready` | `found` | no source-lock-ready corpus import is declared |
| crosswire | `result_not_ready` | `found` | no result-bearing replication is declared ready |

## Boundary

CrossWire metadata is a stronger future source candidate than the KJV-only Open-Bibles repository because it exposes both `kjva.osis.xml` and `kjvdc.xml` path names.
The configuration metadata records `DistributionLicense=GPL` for KJVA and `DistributionLicense=General public license for distribution for any purpose` for the DC-only file, while also noting Crown rights language; source-use review is still required before any local text import.
It is still not source-lock ready: the project has not imported the text, mapped verses, checked book order, compared against current KJVA output, or frozen checksums in a study lock.
It does not change any KJVA bridge result status.
