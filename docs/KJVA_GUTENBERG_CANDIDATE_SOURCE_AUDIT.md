# KJVA Gutenberg Candidate Source Audit

Status: source-status audit only.

This is not an ELS result, not a corpus import, and not a source lock.
It records Project Gutenberg RDF metadata only and does not download, retain, normalize, or commit Bible text.

## Summary

- Source pages: 1.
- Metadata fetches ok: 1.
- Public-domain-USA pages: 1.
- KJV-complete metadata candidates: 1.
- Apocrypha marker pages in RDF: 0.
- Plain-text UTF-8 format pages: 1.
- Source-use ready pages: 0.
- Source-lock ready pages: 0.
- Verse-numbered import ready pages: 0.
- Result-ready pages: 0.
- Claim status: `source_status_only_not_result_bearing`.

## Source Rows

| Source | Status | Rights | Plain text | Apocrypha marker | Source use | Source lock | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gutenberg_ebook_30_kjv_complete | `public_domain_kjv_complete_metadata_needs_apocrypha_coverage_probe` | Public domain in the USA. | True | False | `needs_source_use_policy_lock` | `not_source_lock_ready` | `not_result_ready` |

## Anchors

Found anchors: 6/6.

| Source | Anchor | Status | Diagnostic |
| --- | --- | --- | --- |
| gutenberg | `metadata_fetch_status_recorded` | `found` | Project Gutenberg RDF metadata fetched |
| gutenberg | `public_domain_usa_recorded` | `found` | RDF rights field says public domain in the USA |
| gutenberg | `plain_text_format_recorded` | `found` | plain text UTF-8 format URL is recorded |
| gutenberg | `apocrypha_coverage_not_confirmed` | `found` | RDF metadata does not itself confirm Apocrypha coverage |
| gutenberg | `source_lock_not_ready` | `found` | no source-lock-ready corpus import is declared |
| gutenberg | `result_not_ready` | `found` | no result-bearing replication is declared ready |

## Boundary

Project Gutenberg RDF metadata records eBook 30 as `The Bible, King James Version, Complete` with `Public domain in the USA.` rights and a plain-text UTF-8 format URL.
The RDF metadata does not itself confirm Apocrypha/deuterocanon coverage, so this audit does not declare source-lock readiness.
A future coverage probe may inspect the lawful source text in an ignored local cache, then separately lock verse mapping, book order, checksums, collation, terms, and controls before any result-bearing run.
It does not change any KJVA bridge result status.
