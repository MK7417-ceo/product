"""P3a tests: resume builder + JD matcher."""
import uuid

import pytest
from fastapi.testclient import TestClient

from app.domain.launchpad import Resume, keywords, match_jd
from app.domain.user import DomainError
from app.main import create_app


# ---------- domain ----------

def _resume(**kw):
    base = {"id": "r1", "user_id": "u1", "title": "AI/ML Engineer",
            "summary": "Python developer, machine learning enthusiast",
            "skills": ("python", "pytorch", "sql"),
            "experience": (), "projects": (), "education": (), "links": {}}
    base.update(kw)
    return Resume(**base)


def test_keywords_drops_stopwords():
    kw = keywords("We are looking for a Python developer with 3 years experience")
    assert "python" in kw and "developer" in kw
    assert "we" not in kw and "are" not in kw and "for" not in kw


def test_match_jd_scores_and_explains():
    jd = "Hiring a Python developer. Must know python, pytorch, and docker. Python experience required."
    m = match_jd(_resume(), jd)
    assert 0 < m.score <= 100
    matched = {h.keyword for h in m.matched}
    assert {"python", "pytorch"} <= matched
    assert "docker" in {h.keyword for h in m.missing}
    assert any("docker" in s for s in m.suggestions)


def test_match_jd_rejects_empty():
    with pytest.raises(DomainError):
        match_jd(_resume(), "   ")


def test_resume_validation():
    with pytest.raises(DomainError):
        _resume(title="  ").validate()


# ---------- API ----------

def _client():
    return TestClient(create_app())


def _authz(c: TestClient) -> dict:
    email = f"lz-{uuid.uuid4().hex[:8]}@x.com"
    r = c.post("/api/v1/auth/register",
               json={"email": email, "password": "password123"})
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


_RESUME = {
    "title": "AI/ML Engineer",
    "summary": "Python developer building ML systems",
    "skills": ["python", "pytorch", "fastapi", "sql"],
    "experience": [{"title": "ML Intern", "company": "Acme",
                    "bullets": ["Built a pytorch classifier"]}],
    "projects": [{"name": "SkillForge", "description": "career platform",
                  "tech": ["python", "react"]}],
    "education": [{"degree": "B.Tech", "school": "XYZ", "year": "2026"}],
    "links": {"github": "https://github.com/x"},
}


def test_resume_crud_and_jd_match():
    c = _client()
    h = _authz(c)

    assert c.get("/api/v1/launchpad/resume", headers=h).status_code == 404

    r = c.put("/api/v1/launchpad/resume", json=_RESUME, headers=h)
    assert r.status_code == 200, r.text
    assert r.json()["skills"] == ["python", "pytorch", "fastapi", "sql"]

    g = c.get("/api/v1/launchpad/resume", headers=h)
    assert g.status_code == 200
    assert g.json()["title"] == "AI/ML Engineer"

    jd = ("We need a Python developer with pytorch and fastapi. "
          "Must know docker and kubernetes. Python required.")
    m = c.post("/api/v1/launchpad/jd-match", json={"jd_text": jd}, headers=h)
    assert m.status_code == 200, m.text
    body = m.json()
    assert 0 < body["score"] < 100
    assert "docker" in {x["keyword"] for x in body["missing"]}
    assert any("docker" in s for s in body["suggestions"])

    # upsert replaces
    r2 = c.put("/api/v1/launchpad/resume",
               json={**_RESUME, "title": "Senior AI Engineer"}, headers=h)
    assert r2.json()["title"] == "Senior AI Engineer"
    g2 = c.get("/api/v1/launchpad/resume", headers=h)
    assert g2.json()["title"] == "Senior AI Engineer"


def test_resume_requires_title_and_auth():
    c = _client()
    h = _authz(c)
    r = c.put("/api/v1/launchpad/resume", json={"title": "  "}, headers=h)
    assert r.status_code == 400
    assert c.get("/api/v1/launchpad/resume").status_code == 401
    assert c.post("/api/v1/launchpad/jd-match",
                  json={"jd_text": "python"}).status_code == 401
