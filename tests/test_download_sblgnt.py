import json

from scripts import download_sblgnt as downloader


class _Response:
    def __init__(self, body: bytes) -> None:
        self.body = body

    def __enter__(self) -> "_Response":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return self.body


def test_download_sblgnt_keeps_txt_files(tmp_path, monkeypatch) -> None:
    api_body = json.dumps(
        [
            {"type": "file", "name": "Matthew.txt", "download_url": "https://example/mat"},
            {"type": "file", "name": "README.md", "download_url": "https://example/readme"},
        ]
    ).encode("utf-8")

    def fake_urlopen(url: str) -> _Response:
        if url == downloader.API_URL:
            return _Response(api_body)
        return _Response(b"text")

    monkeypatch.setattr(downloader, "OUT_DIR", tmp_path)
    monkeypatch.setattr(downloader.urllib.request, "urlopen", fake_urlopen)

    assert downloader.main() == 0
    assert (tmp_path / "Matthew.txt").read_bytes() == b"text"
    assert not (tmp_path / "README.md").exists()

