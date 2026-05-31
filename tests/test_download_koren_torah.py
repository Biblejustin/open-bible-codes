from scripts import download_koren_torah as downloader


class _Response:
    def __init__(self, body: bytes) -> None:
        self.body = body

    def __enter__(self) -> "_Response":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return self.body


def test_download_koren_torah_writes_declared_files(tmp_path, monkeypatch) -> None:
    seen: list[str] = []

    def fake_urlopen(url: str) -> _Response:
        seen.append(url)
        return _Response(f"body:{url}".encode("utf-8"))

    monkeypatch.setattr(downloader, "OUT_DIR", tmp_path)
    monkeypatch.setattr(downloader.urllib.request, "urlopen", fake_urlopen)

    assert downloader.main() == 0

    assert len(seen) == len(downloader.FILES)
    assert all((tmp_path / name).exists() for name in downloader.FILES)

