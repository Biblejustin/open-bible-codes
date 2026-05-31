# KJVA Wikisource Book Coverage Probe

Status: source-coverage probe only. This is not an ELS result, not a
corpus import, not a verse import, and not a source lock.

## Setup

This probe checks book-link coverage on the Wikisource Ballantyne KJV +
Apocrypha candidate page. It records link text, link target status, and
volume numbers only. It does not import, retain, normalize, or commit
Bible text.

Source page: https://en.wikisource.org/wiki/The_Holy_Bible,_containing_the_Old_%26_New_Testament_%26_the_Apocrypha

## Findings

- Expected KJV books checked: 66.
- Existing KJV book links: 36.
- Redlinked KJV book links: 30.
- Missing KJV book links: 0.
- Expected apocrypha/deuterocanon books checked: 14.
- Existing apocrypha/deuterocanon book links: 0.
- Redlinked apocrypha/deuterocanon book links: 0.
- Missing apocrypha/deuterocanon book links: 14.
- Book-order lock ready: 0.
- Verse-numbered import ready: 0.
- Result-ready sources: 0.

Current read: the main Wikisource page has KJV book-link metadata, but
the parsed book-link table does not expose apocrypha/deuterocanon book
links. This keeps the source at coverage-probe status only.

## Book Link Summary

| Section | Existing | Redlinked | Missing | Expected |
| --- | ---: | ---: | ---: | ---: |
| KJV | 36 | 30 | 0 | 66 |
| Apocrypha/deuterocanon | 0 | 0 | 14 | 14 |

## Protocol Anchors

Found anchors: 5 of 5.

| Source | Anchor | Status | Diagnostic |
| --- | --- | --- | --- |
| wikisource | `main_page_fetch_status_recorded` | found | main page fetch state is recorded |
| wikisource | `kjv_book_links_recorded` | found | expected KJV book-link rows are recorded |
| wikisource | `apocrypha_book_links_recorded` | found | expected apocrypha/deuterocanon book-link rows are recorded |
| wikisource | `book_order_not_ready` | found | no book-order lock is declared ready |
| wikisource | `result_not_ready` | found | no result-bearing replication is declared ready |

## Book Rows

| Section | Book | Status | Link Text | Volume |
| --- | --- | --- | --- | ---: |
| kjv | Genesis | existing | Genesis | 1 |
| kjv | Exodus | existing | Exodus | 1 |
| kjv | Leviticus | existing | Leviticus | 1 |
| kjv | Numbers | existing | Numbers | 1 |
| kjv | Deuteronomy | existing | Deuteronomy | 1 |
| kjv | Joshua | existing | Joshua | 1 |
| kjv | Judges | existing | Judges | 1 |
| kjv | Ruth | existing | Ruth | 1 |
| kjv | 1 Samuel | existing | I. Samuel | 1 |
| kjv | 2 Samuel | existing | II. Samuel | 1 |
| kjv | 1 Kings | existing | I. Kings | 1 |
| kjv | 2 Kings | existing | II. Kings | 1 |
| kjv | 1 Chronicles | existing | I. Chronicles | 1 |
| kjv | 2 Chronicles | existing | II. Chronicles | 1 |
| kjv | Ezra | existing | Ezra | 1 |
| kjv | Nehemiah | existing | Nehemiah | 1 |
| kjv | Esther | existing | Esther | 1 |
| kjv | Job | existing | Job | 2 |
| kjv | Psalms | existing | Psalms | 2 |
| kjv | Proverbs | redlink | Proverbs | 2 |
| kjv | Ecclesiastes | redlink | Ecclesiastes | 2 |
| kjv | Song of Solomon | redlink | Song of Solomon | 2 |
| kjv | Isaiah | redlink | Isaiah | 2 |
| kjv | Jeremiah | redlink | Jeremiah | 2 |
| kjv | Lamentations | redlink | Lamentations | 2 |
| kjv | Ezekiel | redlink | Ezekiel | 2 |
| kjv | Daniel | redlink | Daniel | 2 |
| kjv | Hosea | existing | Hosea | 2 |
| kjv | Joel | existing | Joel | 2 |
| kjv | Amos | existing | Amos | 2 |
| kjv | Obadiah | existing | Obadiah | 2 |
| kjv | Jonah | existing | Jonah | 2 |
| kjv | Micah | existing | Micah | 2 |
| kjv | Nahum | existing | Nahum | 2 |
| kjv | Habakkuk | existing | Habakkuk | 2 |
| kjv | Zephaniah | existing | Zephaniah | 2 |
| kjv | Haggai | existing | Haggai | 2 |
| kjv | Zechariah | existing | Zechariah | 2 |
| kjv | Malachi | existing | Malachi | 2 |
| kjv | Matthew | existing | Matthew | 3 |
| kjv | Mark | existing | Mark | 3 |
| kjv | Luke | existing | Luke | 3 |
| kjv | John | existing | John | 3 |
| kjv | Acts | existing | Acts | 3 |
| kjv | Romans | redlink | Romans | 3 |
| kjv | 1 Corinthians | redlink | 1 Corinthians | 3 |
| kjv | 2 Corinthians | redlink | 2 Corinthians | 3 |
| kjv | Galatians | redlink | Galatians | 3 |
| kjv | Ephesians | redlink | Ephesians | 3 |
| kjv | Philippians | redlink | Philippians | 3 |
| kjv | Colossians | redlink | Colossians | 3 |
| kjv | 1 Thessalonians | redlink | 1 Thessalonians | 3 |
| kjv | 2 Thessalonians | redlink | 2 Thessalonians | 3 |
| kjv | 1 Timothy | redlink | 1 Timothy | 3 |
| kjv | 2 Timothy | redlink | 2 Timothy | 3 |
| kjv | Titus | redlink | Titus | 3 |
| kjv | Philemon | redlink | Philemon | 3 |
| kjv | Hebrews | redlink | Hebrews | 3 |
| kjv | James | redlink | James | 3 |
| kjv | 1 Peter | redlink | 1 Peter | 3 |
| kjv | 2 Peter | redlink | 2 Peter | 3 |
| kjv | 1 John | redlink | 1 John | 3 |
| kjv | 2 John | redlink | 2 John | 3 |
| kjv | 3 John | redlink | 3 John | 3 |
| kjv | Jude | redlink | Jude | 3 |
| kjv | Revelation | redlink | Revelation | 3 |
| apocrypha | 1 Esdras | missing |  |  |
| apocrypha | 2 Esdras | missing |  |  |
| apocrypha | Tobit | missing |  |  |
| apocrypha | Judith | missing |  |  |
| apocrypha | Rest of Esther | missing |  |  |
| apocrypha | Wisdom | missing |  |  |
| apocrypha | Ecclesiasticus | missing |  |  |
| apocrypha | Baruch | missing |  |  |
| apocrypha | Song of the Three Children | missing |  |  |
| apocrypha | Susanna | missing |  |  |
| apocrypha | Bel and the Dragon | missing |  |  |
| apocrypha | Prayer of Manasseh | missing |  |  |
| apocrypha | 1 Maccabees | missing |  |  |
| apocrypha | 2 Maccabees | missing |  |  |

## Use Boundary

This probe does not decide that Wikisource can supply a KJVA corpus.
It does not fetch child book text, map verses, choose book order, run
ELS searches, evaluate controls, and does not change any KJVA result
status.
