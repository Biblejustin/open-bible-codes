# KJVA Gutenberg Candidate Checksum Sidecar

Status: checksum sidecar only.

This is not an ELS result, not a corpus import, not a source-use approval, not a source lock, and not a result-bearing replication.
It records Project Gutenberg eBook 30 and eBook 124 RDF and plain-text checksums as candidate identifiers.
It does not commit Bible text, choose source wording, split unmarked prose, replace current eBible KJVA, or authorize a KJVA bridge run.

## Summary

- Source rows: 2.
- Metadata fetches OK: 2.
- Public-domain-USA rows: 2.
- Plain-text checksum rows: 2.
- Checksum records ready: 2.
- KJV plain-text SHA-256: `349cb0de0e1e0c14bbb960d201b44a1753b64d5cd23316a17fdb9e9ac01747ac`.
- Apocrypha plain-text SHA-256: `ed2f875e0f0972ed4748988f5b44480eccdb22ca3b4a3ce85edc75f17d259f4b`.
- Source-use ready pages: 0.
- Verse-import ready pages: 0.
- Source-lock ready: 0.
- Result-ready: 0.
- Claim status: `checksum_sidecar_only_not_result_bearing`.

## Checksum Rows

| Source | Component | eBook | RDF SHA-256 | Plain-text SHA-256 | Rights | Status |
| --- | --- | ---: | --- | --- | --- | --- |
| `gutenberg_ebook_30_kjv_complete` | `kjv_66_book_component` | 30 | `7c23fdfdb685b0fda299646a9c44fc1e6b84cc8b09a65a76b0a5094793ab5aba` | `349cb0de0e1e0c14bbb960d201b44a1753b64d5cd23316a17fdb9e9ac01747ac` | Public domain in the USA. | `checksum_record_ready_not_source_locked` |
| `gutenberg_ebook_124_deuterocanonical` | `apocrypha_deuterocanon_component` | 124 | `757e47397efe131c78d529a54679d2e73878d0e5603df86c88f11b7bf7d47e01` | `ed2f875e0f0972ed4748988f5b44480eccdb22ca3b4a3ce85edc75f17d259f4b` | Public domain in the USA. | `checksum_record_ready_not_source_locked` |

## Boundary

This sidecar closes only the candidate checksum-record step for Project Gutenberg eBook 30 and eBook 124.
It does not close source-use, verse mapping, collation, `SIR 44:23`, Prayer of Manasseh, `SIR 19:1`, term/control, or study-lock blockers.
No Bible text is written to tracked outputs.
It does not change any KJVA bridge result status.
