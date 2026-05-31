import json

from scripts import download_oshb_wlc as downloader


class _Response:
    def __init__(self, body: bytes) -> None:
        self.body = body

    def __enter__(self) -> "_Response":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return self.body


def test_download_oshb_wlc_keeps_xml_files(tmp_path, monkeypatch) -> None:
    api_body = json.dumps(
        [
            {"type": "file", "name": "Genesis.xml", "download_url": "https://example/gen"},
            {"type": "file", "name": "README.md", "download_url": "https://example/readme"},
        ]
    ).encode("utf-8")

    def fake_urlopen(url: str) -> _Response:
        if url == downloader.API_URL:
            return _Response(api_body)
        return _Response(b"xml")

    monkeypatch.setattr(downloader, "OUT_DIR", tmp_path)
    monkeypatch.setattr(downloader.urllib.request, "urlopen", fake_urlopen)

    assert downloader.main() == 0
    assert (tmp_path / "Genesis.xml").read_bytes() == b"xml"
    assert not (tmp_path / "README.md").exists()

