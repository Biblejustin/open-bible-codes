import tempfile
import unittest
from pathlib import Path

from scripts.import_tpt_pdf import (
    BookInfo,
    LineItem,
    PageLine,
    build_page_lines,
    main,
    parse_book_lines,
)


class TptPdfImportTests(unittest.TestCase):
    def test_build_page_lines_drops_blue_footnote_markers_and_small_notes(self) -> None:
        lines = build_page_lines(
            """<?xml version="1.0" encoding="UTF-8"?>
<pdf2xml>
<page number="1" position="absolute" top="0" left="0" height="496" width="378">
  <fontspec id="0" size="25" family="Times" color="#dd362c"/>
  <fontspec id="1" size="13" family="Times" color="#000000"/>
  <fontspec id="2" size="10" family="Times" color="#0000ee"/>
  <fontspec id="3" size="11" family="Times" color="#000000"/>
  <fontspec id="4" size="10" family="Times" color="#000000"/>
  <text top="10" left="10" width="10" height="23" font="0">1</text>
  <text top="18" left="20" width="50" height="11" font="1"> Body</text>
  <text top="15" left="70" width="5" height="9" font="2">a</text>
  <text top="40" left="10" width="80" height="10" font="3">1:1 footnote</text>
  <text top="60" left="10" width="5" height="9" font="4">2</text>
  <text top="63" left="20" width="50" height="11" font="1"> next</text>
</page>
</pdf2xml>
"""
        )

        rendered = [" ".join(item.text for item in line.items) for line in lines]

        self.assertEqual(rendered, ["1 Body", "2 next"])
        self.assertEqual(lines[0].items[0].kind, "chapter")
        self.assertEqual(lines[1].items[0].kind, "verse")

    def test_parse_book_lines_skips_psalm_titles_and_preserves_ranges(self) -> None:
        rows = parse_book_lines(
            BookInfo("PSA", ("PSALMS",)),
            [
                line(("PSALMS", "text")),
                line(("1", "chapter"), ("T HE T REE", "text")),
                line(("1", "verse"), ("Blessed text", "text")),
                line(("4-5", "verse"), ("Combined range", "text")),
            ],
        )

        self.assertEqual([row.ref for row in rows], ["PSA 1:1", "PSA 1:4-5"])
        self.assertEqual(rows[0].text, "Blessed text")

    def test_parse_single_chapter_book_creates_verse_one_without_marker(self) -> None:
        rows = parse_book_lines(
            BookInfo("2JN", ("2 JOHN",), single_chapter=True),
            [
                line(("2 JOHN", "text")),
                line(("Loving Truth", "text")),
                line(("From the elder to the chosen woman:", "text")),
                line(("2", "verse"), ("because of truth", "text")),
            ],
        )

        self.assertEqual([row.ref for row in rows], ["2JN 1:1", "2JN 1:2"])
        self.assertEqual(rows[0].text, "From the elder to the chosen woman:")

    def test_main_writes_csv_from_synthetic_pdf_xml(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "tpt.pdf"
            out = Path(tmp) / "tpt.csv"
            manifest = Path(tmp) / "manifest.json"
            pdf.write_bytes(b"%PDF synthetic")

            original = __import__("scripts.import_tpt_pdf", fromlist=["pdftohtml_xml"])
            saved = original.pdftohtml_xml
            original.pdftohtml_xml = lambda _path: synthetic_full_xml()
            try:
                exit_code = main(["--pdf", str(pdf), "--out", str(out), "--manifest", str(manifest)])
            finally:
                original.pdftohtml_xml = saved

            self.assertEqual(exit_code, 0)
            text = out.read_text(encoding="utf-8")
            self.assertIn("MAT 1:1", text)
            self.assertTrue(manifest.exists())


def line(*items: tuple[str, str]) -> PageLine:
    return PageLine(1, tuple(LineItem(text, kind) for text, kind in items))


def synthetic_full_xml() -> str:
    pages = []
    page = 1
    for title in [
        "PSALMS",
        "PROVERBS",
        "SONG OF SONGS",
        "MATTHEW",
        "MARK",
        "LUKE",
        "JOHN",
        "ACTS",
        "ROMANS",
        "1 CORINTHIANS",
        "2 CORINTHIANS",
        "GALATIANS",
        "EPHESIANS",
        "PHILIPPIANS",
        "COLOSSIANS",
        "1 THESSALONIANS",
        "2 THESSALONIANS",
        "1 TIMOTHY",
        "2 TIMOTHY",
        "TITUS",
        "PHILEMON",
        "HEBREWS",
        "JAMES (JACOB)",
        "1 PETER",
        "2 PETER",
        "1 JOHN",
        "2 JOHN",
        "3 JOHN",
        "JUDE (JUDAH)",
        "REVELATION",
    ]:
        pages.append(render_intro_page(page, title))
        page += 1
        pages.append(render_body_page(page, title))
        page += 1
    pages.append(render_plain_page(page, "YOUR PERSONAL"))
    return "<?xml version='1.0' encoding='UTF-8'?><pdf2xml>" + "".join(pages) + "</pdf2xml>"


def render_intro_page(page: int, title: str) -> str:
    return f"""
<page number="{page}" position="absolute" top="0" left="0" height="496" width="378">
  <fontspec id="t" size="25" family="Times" color="#000000"/>
  <text top="10" left="10" width="50" height="23" font="t">{title}</text>
  <text top="40" left="10" width="50" height="23" font="t">Introduction</text>
  <text top="70" left="10" width="50" height="23" font="t">AT A GLANCE</text>
</page>
"""


def render_body_page(page: int, title: str) -> str:
    return f"""
<page number="{page}" position="absolute" top="0" left="0" height="496" width="378">
  <fontspec id="title" size="25" family="Times" color="#000000"/>
  <fontspec id="chap" size="25" family="Times" color="#dd362c"/>
  <fontspec id="body" size="13" family="Times" color="#000000"/>
  <fontspec id="verse" size="10" family="Times" color="#000000"/>
  <text top="10" left="10" width="50" height="23" font="title">{title}</text>
  <text top="40" left="10" width="10" height="23" font="chap">1</text>
  <text top="48" left="25" width="80" height="11" font="body"> body one</text>
  <text top="70" left="10" width="5" height="9" font="verse">2</text>
  <text top="73" left="25" width="80" height="11" font="body"> body two</text>
</page>
"""


def render_plain_page(page: int, text: str) -> str:
    return f"""
<page number="{page}" position="absolute" top="0" left="0" height="496" width="378">
  <fontspec id="title" size="25" family="Times" color="#000000"/>
  <text top="10" left="10" width="50" height="23" font="title">{text}</text>
</page>
"""


if __name__ == "__main__":
    unittest.main()
