# KJVA Gutenberg Candidate Source Audit

Status: source-status audit only.

This is not an ELS result, not a corpus import, and not a source lock.
It records Project Gutenberg eBook 30 and eBook 124 RDF metadata only and does not download, retain, normalize, or commit Bible text.

## Summary

- Source pages: 2.
- Metadata fetches ok: 2.
- Public-domain-USA pages: 2.
- KJV-complete metadata candidates: 1.
- Apocrypha/deuterocanon metadata candidates: 1.
- Split KJV+Apocrypha metadata candidates: 1.
- Apocrypha marker pages in RDF: 1.
- Plain-text UTF-8 format pages: 2.
- Source-use ready pages: 0.
- Source-lock ready pages: 0.
- Verse-numbered import ready pages: 0.
- Result-ready pages: 0.
- Claim status: `source_status_only_not_result_bearing`.

## Source Rows

| Source | Status | Rights | Plain text | Apocrypha marker | Source use | Source lock | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gutenberg_ebook_30_kjv_complete | `public_domain_kjv_complete_metadata_component` | Public domain in the USA. | True | False | `needs_source_use_policy_lock` | `not_source_lock_ready` | `not_result_ready` |
| gutenberg_ebook_124_deuterocanonical | `public_domain_apocrypha_metadata_component` | Public domain in the USA. | True | True | `needs_source_use_policy_lock` | `not_source_lock_ready` | `not_result_ready` |

## Anchors

Found anchors: 7/7.

| Source | Anchor | Status | Diagnostic |
| --- | --- | --- | --- |
| gutenberg | `metadata_fetch_status_recorded` | `found` | Project Gutenberg RDF metadata fetched for eBook 30 and eBook 124 |
| gutenberg | `public_domain_usa_recorded` | `found` | RDF rights fields say public domain in the USA |
| gutenberg | `plain_text_format_recorded` | `found` | plain text UTF-8 format URLs are recorded |
| gutenberg | `apocrypha_metadata_recorded` | `found` | eBook 124 RDF metadata identifies the Apocrypha/deuterocanonical component |
| gutenberg | `split_metadata_components_recorded` | `found` | eBook 30 plus eBook 124 form a split metadata candidate |
| gutenberg | `source_lock_not_ready` | `found` | no source-lock-ready corpus import is declared |
| gutenberg | `result_not_ready` | `found` | no result-bearing replication is declared ready |

## Boundary

Project Gutenberg RDF metadata records eBook 30 as `The Bible, King James Version, Complete` and eBook 124 as `Deuterocanonical Books of the Bible Apocrypha`, both with `Public domain in the USA.` rights and plain-text UTF-8 format URLs.
This metadata audit pairs with the separate heading-level coverage probe, but it does not declare source-lock readiness.
A future source-lock pass must still inspect lawful source text in an ignored local cache, then lock verse mapping, book order, Baruch/Epistle handling, checksums, collation, terms, and controls before any result-bearing run.
It does not change any KJVA bridge result status.
