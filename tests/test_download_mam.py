from scripts.download_mam import MAMIndexParser, is_book_href


def test_mam_index_parser_keeps_book_links_only() -> None:
    parser = MAMIndexParser()
    parser.feed('<a href="A01.html">Genesis</a><a href="notes/readme.html">Notes</a>')

    assert parser.book_links == ["A01.html"]
    assert is_book_href("F99.html")
    assert not is_book_href("notes/F99.html")

