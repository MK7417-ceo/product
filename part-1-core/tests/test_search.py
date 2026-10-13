"""Global search tests: domain ranking + HTTP API (Notes-style unified search)."""
import uuid

import pytest
from fastapi.testclient import TestClient

from app.domain.search import (
    build_snippet,
    mark_matches,
    score_candidate,
    tokenize,
    validate_query,
    validate_types,
)
from app.domain.user import DomainError
from app.main import create_app


# ---------- domain ----------

def test_tokenize():
    assert tokenize("  Python  Basics ") == ["python", "basics"]
    assert tokenize("   ") == []


def test_mark_matches_escapes_html():
    out = mark_matches('<script>alert("x")</script> python', ["python"])
    assert "<script>" not in out
    assert "&lt;script&gt;" in out
    assert "<mark>python</mark>" in out


def test_mark_matches_case_insensitive():
    out = mark_matches("Learn PYTHON basics", ["python"])
    assert "<mark>PYTHON</mark>" in out


def test_score_title_outranks_body():
    terms = ["python"]
    title_hit = score_candidate("python roadmap", "nothing relevant here", terms)
    body_hit = score_candidate("unrelated title", "learn python deeply", terms)
    assert title_hit > body_hit > 0


def test_score_zero_when_no_match():
    assert score_candidate("abc", "def", ["python"]) == 0.0


def test_build_snippet_centres_on_match():
    body = "lorem ipsum dolor sit amet " * 10 + "python " + "consectetur adipiscing elit " * 10
    snip = build_snippet(body, ["python"])
    assert "<mark>python</mark>" in snip
    assert snip.startswith("…") and snip.endswith("…")


def test_build_snippet_no_match_returns_head():
    snip = build_snippet("hello world", ["python"])
    assert "<mark>" not in snip
    assert "hello world" in snip


def test_validate_query_rejects_short_and_blank():
    with pytest.raises(DomainError):
        validate_query("a")
    with pytest.raises(DomainError):
        validate_query("   ")
    assert validate_query(" python ") == ["python"]


def test_validate_types():
    assert validate_types(None) == ("roadmap", "task", "evidence", "assessment", "certificate")
    assert validate_types("task,roadmap") == ("roadmap", "task")
    with pytest.raises(DomainError):
        validate_types("notes")


# ---------- API ----------

def _client():
    return TestClient(create_app())


def _authz(c: TestClient) -> dict:
    email = f"srch-{uuid.uuid4().hex[:8]}@x.com"
    r = c.post("/api/v1/auth/register",
               json={"email": email, "password": "password123"})
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


_GAPS = {"gaps": [{"skill": "python-basics", "mastery_pct": 35}]}


def test_search_finds_roadmap_tasks():
    c = _client()
    h = _authz(c)
    r = c.post("/api/v1/roadmaps/generate", json=_GAPS, headers=h)
    assert r.status_code == 201, r.text

    r = c.get("/api/v1/search", params={"q": "python-basics"}, headers=h)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["count"] >= 1
    types = {hit["type"] for hit in body["results"]}
    assert "task" in types
    # matched term is highlighted in the results
    assert any("<mark>" in hit["snippet"] or "<mark>" in hit["title"]
               for hit in body["results"])


def test_search_type_filter():
    c = _client()
    h = _authz(c)
    c.post("/api/v1/roadmaps/generate", json=_GAPS, headers=h)

    r = c.get("/api/v1/search", params={"q": "python", "types": "roadmap"}, headers=h)
    assert r.status_code == 200, r.text
    assert all(hit["type"] == "roadmap" for hit in r.json()["results"])


def test_search_rejects_unknown_type():
    c = _client()
    h = _authz(c)
    r = c.get("/api/v1/search", params={"q": "python", "types": "notes"}, headers=h)
    assert r.status_code == 400


def test_search_requires_auth():
    c = _client()
    assert c.get("/api/v1/search", params={"q": "python"}).status_code == 401


def test_search_short_query_rejected():
    c = _client()
    h = _authz(c)
    # FastAPI Query(min_length=1) lets "a" through; domain requires >= 2
    assert c.get("/api/v1/search", params={"q": "a"}, headers=h).status_code == 400


def test_search_is_private_per_user():
    c = _client()
    h1 = _authz(c)
    h2 = _authz(c)
    c.post("/api/v1/roadmaps/generate", json=_GAPS, headers=h1)

    r = c.get("/api/v1/search", params={"q": "python-basics"}, headers=h2)
    assert r.status_code == 200
    assert r.json()["count"] == 0, "user2 must not see user1's content"


def test_search_no_match_returns_empty():
    c = _client()
    h = _authz(c)
    r = c.get("/api/v1/search", params={"q": "zzzznothinghere"}, headers=h)
    assert r.status_code == 200
    assert r.json()["results"] == []
