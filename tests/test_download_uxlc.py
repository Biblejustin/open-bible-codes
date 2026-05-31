from scripts.download_uxlc import is_book_xml


def test_is_book_xml_accepts_book_files_and_rejects_metadata() -> None:
    assert is_book_xml("Tanach/Books/Genesis.xml")
    assert not is_book_xml("Tanach/Books/Genesis.DH.xml")
    assert not is_book_xml("Tanach/Books/TanachHeader.xml")
    assert not is_book_xml("Tanach/Other/Genesis.xml")

