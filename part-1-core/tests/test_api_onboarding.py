"""API tests: profile + placement verification end to end."""
import uuid

from fastapi.testclient import TestClient

from app.main import create_app


def make_client() -> TestClient:
    return TestClient(create_app())


def _token(client: TestClient) -> str:
    email = f"ob-{uuid.uuid4().hex[:8]}@x.com"
    r = client.post("/api/v1/auth/register",
                    json={"email": email, "password": "password123"})
    assert r.status_code == 201, r.text
    return r.json()["access_token"]


def _authz(client: TestClient) -> dict:
    return {"Authorization": f"Bearer {_token(client)}"}


_PROFILE = {
    "education": "B.Tech CSE", "experience_years": 1.5,
    "current_skills": ["python", "sql"],
    "target_role": "AI Engineer", "target_domain": "AI/ML",
    "target_level": "intermediate", "tech_focus": ["python", "ml"],
}


def test_profile_create_and_read():
    c = make_client()
    h = _authz(c)
    r = c.post("/api/v1/profiles", json=_PROFILE, headers=h)
    assert r.status_code == 201, r.text
    assert r.json()["target_role"] == "AI Engineer"
    r = c.get("/api/v1/profiles/me", headers=h)
    assert r.status_code == 200
    assert r.json()["education"] == "B.Tech CSE"


def test_profile_requires_auth():
    assert make_client().get("/api/v1/profiles/me").status_code == 401


def test_placement_topics():
    c = make_client()
    r = c.get("/api/v1/placement/topics", headers=_authz(c))
    assert "python" in r.json()["topics"]


def test_placement_full_verify_flow():
    c = make_client()
    h = _authz(c)
    r = c.post("/api/v1/placement/start",
               json={"topic": "python", "claimed_level": "beginner"}, headers=h)
    assert r.status_code == 201, r.text
    body = r.json()
    assert len(body["questions"]) == 4
    assert all("answer_index" not in q for q in body["questions"])

    # answer everything wrong -> verified level must step down to beginner (floor)
    r = c.post(f"/api/v1/placement/{body['placement_id']}/submit",
               json={"answers": {q["id"]: 99 for q in body["questions"]}}, headers=h)
    assert r.status_code == 200
    out = r.json()
    assert out["status"] == "completed"
    assert out["verified_level"] == "beginner"
    assert out["correct"] == 0


def test_placement_unknown_topic_400():
    c = make_client()
    r = c.post("/api/v1/placement/start",
               json={"topic": "cobol", "claimed_level": "beginner"},
               headers=_authz(c))
    assert r.status_code == 400


def test_google_login_unconfigured_501():
    r = make_client().get("/api/v1/auth/google/login")
    assert r.status_code == 501
    assert "GOOGLE_CLIENT_ID" in r.json()["detail"]
