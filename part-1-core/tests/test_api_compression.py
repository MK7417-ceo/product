"""API tests — gzip compression middleware (speed items).

Large JSON responses are gzip-compressed when the client accepts gzip;
small responses below the minimum size are sent uncompressed.
"""
from fastapi.testclient import TestClient

from app.main import create_app


def make_client() -> TestClient:
    return TestClient(create_app())


def test_large_response_is_gzip_compressed():
    client = make_client()
    plain = client.get("/openapi.json")
    gzipped = client.get("/openapi.json", headers={"Accept-Encoding": "gzip"})
    assert plain.status_code == 200
    assert gzipped.status_code == 200
    assert gzipped.headers.get("content-encoding") == "gzip"
    assert gzipped.headers.get("vary") == "Accept-Encoding"
    # Same decoded body, much smaller on the wire.
    assert gzipped.content == plain.content
    assert int(gzipped.headers["content-length"]) < len(plain.content) // 2


def test_small_response_is_not_compressed():
    client = make_client()
    resp = client.get("/api/v1/health", headers={"Accept-Encoding": "gzip"})
    assert resp.status_code == 200
    assert "content-encoding" not in resp.headers


def test_no_accept_encoding_means_no_compression():
    client = make_client()
    resp = client.get("/openapi.json", headers={"Accept-Encoding": "identity"})
    assert resp.status_code == 200
    assert "content-encoding" not in resp.headers
