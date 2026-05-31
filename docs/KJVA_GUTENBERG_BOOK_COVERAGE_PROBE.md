# KJVA Gutenberg Book Coverage Probe

Status: source-coverage probe only.

This is not an ELS result, not a corpus import, not a verse import, and not a source lock.
It fetches Project Gutenberg eBook 30 plain text for heading-level coverage scanning only.
It does not commit Bible text, normalize Bible text, or create a local corpus.

## Summary

- Source pages: 1.
- Plain-text fetches ok: 1.
- Plain-text bytes scanned: 4644740.
- Expected KJV books checked: 66.
- KJV book headings found: 66.
- Missing KJV book headings: 0.
- Expected apocrypha/deuterocanon books checked: 14.
- Apocrypha/deuterocanon book headings found: 0.
- Missing apocrypha/deuterocanon book headings: 14.
- Book-order lock ready: 0.
- Verse-numbered import ready: 0.
- Source-lock ready: 0.
- Result-ready sources: 0.
- Claim status: `coverage_probe_only_not_result_bearing`.

## Coverage Read

Project Gutenberg eBook 30 heading markers show all 66 KJV book headings and no Apocrypha/deuterocanon book headings.
Missing Apocrypha/deuterocanon heading rows: 1 Esdras, 2 Esdras, Tobit, Judith, Rest of Esther, Wisdom, Ecclesiasticus, Baruch, Song of the Three Children, Susanna, Bel and the Dragon, Prayer of Manasseh, 1 Maccabees, 2 Maccabees.

## Anchors

Found anchors: 5/5.

| Source | Anchor | Status | Diagnostic |
| --- | --- | --- | --- |
| gutenberg | `plain_text_fetch_status_recorded` | `found` | Project Gutenberg plain-text fetch status is recorded |
| gutenberg | `kjv_book_headings_found` | `found` | 66 KJV book headings are found in heading markers |
| gutenberg | `apocrypha_book_headings_absent` | `found` | no Apocrypha/deuterocanon book headings are found in heading markers |
| gutenberg | `source_lock_not_ready` | `found` | no source-lock-ready corpus import is declared |
| gutenberg | `result_not_ready` | `found` | no result-bearing replication is declared ready |

## Boundary

Source URL scanned: `https://www.gutenberg.org/cache/epub/30/pg30.txt`.
This coverage probe checks heading markers only. It does not make a verse map, book-order lock, source checksum lock, collation, term lock, study-lock sidecar, or result-bearing replication.
The current read is that Project Gutenberg eBook 30 is useful as a public-domain KJV-only control candidate, not as an independent KJVA/apocrypha bridge source.
It does not change any KJVA bridge result status.
