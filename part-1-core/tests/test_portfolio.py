"""P3c tests: portfolio data aggregation + HTML generation."""
import uuid

import pytest
from fastapi.testclient import TestClient

from app.domain.portfolio import PortfolioData, render_html
from app.domain.user import DomainError
from app.main import create_app


def test_render_html_escapes_user_content():
    p = PortfolioData(
        name="AI/ML Engineer", summary="Python dev",
        skills=("python", "<script>alert(1)</script>"),
        projects=({"name": "X", "description": "<b>bold</b>", "tech": []},),
    )
    out = render_html(p)
    assert "<script>" not in out
    assert "&lt;script&gt;" in out
    assert "AI/ML Engineer" in out
    assert "python" in out


def test_render_html_requires_name():
    with pytest.raises(DomainError):
        render_html(PortfolioData(name="  ", summary="x"))


def test_render_html_includes_journey_and_certs():
    p = PortfolioData(
        name="Dev", summary="s", skills=("python",),
        certificates=({"title": "Roadmap Completion", "issued_at": "2026-10-12T00:00:00",
                       "detail": "3 tasks", "verification_code": "SF-ABCDEFGH"},),
        roadmap_title="Roadmap v1", roadmap_done=3, roadmap_total=3,
        evidence_count=5)
    out = render_html(p)
    assert "SF-ABCDEFGH" in out
    assert "3/3 tasks" in out
    assert "5 evidence" in out


def _client():
    return TestClient(create_app())


def _authz(c: TestClient) -> dict:
    email = f"pf-{uuid.uuid4().hex[:8]}@x.com"
    r = c.post("/api/v1/auth/register",
               json={"email": email, "password": "password123"})
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_portfolio_endpoints():
    c = _client()
    h = _authz(c)

    # no resume -> 404
    assert c.get("/api/v1/launchpad/portfolio", headers=h).status_code == 404
    assert c.get("/api/v1/launchpad/portfolio/download", headers=h).status_code == 404

    c.put("/api/v1/launchpad/resume", headers=h, json={
        "title": "AI/ML Engineer", "summary": "Python dev, ML enthusiast",
        "skills": ["python", "pytorch"],
        "projects": [{"name": "SkillForge", "description": "career platform",
                      "tech": ["python"]}],
        "links": {"github": "https://github.com/x"}})

    # roadmap for the journey section
    rg = c.post("/api/v1/roadmaps/generate", headers=h,
                json={"gaps": [{"skill": "python-basics", "mastery_pct": 30}]})
    assert rg.status_code == 201

    p = c.get("/api/v1/launchpad/portfolio", headers=h)
    assert p.status_code == 200, p.text
    body = p.json()
    assert body["name"] == "AI/ML Engineer"
    assert body["skills"] == ["python", "pytorch"]
    assert body["roadmap_total"] == 3
    assert body["links"]["github"] == "https://github.com/x"

    d = c.get("/api/v1/launchpad/portfolio/download", headers=h)
    assert d.status_code == 200
    assert d.headers["content-type"].startswith("text/html")
    assert "attachment" in d.headers["content-disposition"]
    assert "AI/ML Engineer" in d.text
    assert "SkillForge" in d.text


def test_portfolio_requires_auth():
    c = _client()
    assert c.get("/api/v1/launchpad/portfolio").status_code == 401
    assert c.get("/api/v1/launchpad/portfolio/download").status_code == 401
