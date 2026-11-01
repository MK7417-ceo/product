"""API tests — public SEO endpoints (no auth, real sitemap content)."""
from fastapi.testclient import TestClient

from app.main import create_app


class FakeContent:
    def list_topics(self, active_only=True):
        return [
            {"slug": "python", "name": "Python", "theory_count": 4},
            {"slug": "empty-topic", "name": "Empty", "theory_count": 0},
        ]


def make_client() -> TestClient:
    app = create_app()
    app.state.content_service = FakeContent()
    return TestClient(app)


def test_sitemap_lists_only_topics_with_content():
    resp = make_client().get("/sitemap.xml")
    assert resp.status_code == 200
    assert "application/xml" in resp.headers["content-type"]
    body = resp.text
    assert "/topics/python" in body
    assert "empty-topic" not in body  # never promise content that isn't there
    assert "/topics" in body
    assert "/directory" in body


def test_sitemap_uses_request_base_url_without_invented_domain():
    resp = make_client().get("/sitemap.xml")
    assert "http://testserver/topics/python" in resp.text
    assert "skillforge.ai" not in resp.text


def test_robots_txt_points_at_sitemap_and_blocks_api():
    resp = make_client().get("/robots.txt")
    assert resp.status_code == 200
    assert "text/plain" in resp.headers["content-type"]
    assert "Sitemap: http://testserver/sitemap.xml" in resp.text
    assert "Disallow: /api/" in resp.text
    assert "Allow: /topics" in resp.text


def test_sitemap_lists_both_language_versions_of_each_topic():
    body = make_client().get("/sitemap.xml").text
    assert "/topics/python" in body
    assert "/en/topics/python" in body
    assert "/en/topics" in body
    # Still never promises content that isn't there, in either language.
    assert "empty-topic" not in body


def test_sitemap_hreflang_pairs_topic_urls():
    body = make_client().get("/sitemap.xml").text
    assert 'hreflang="hi"' in body
    assert 'hreflang="en"' in body
    assert 'href="http://testserver/topics/python"' in body
    assert 'href="http://testserver/en/topics/python"' in body


def test_robots_txt_allows_english_topics():
    resp = make_client().get("/robots.txt")
    assert "Allow: /en/topics" in resp.text
