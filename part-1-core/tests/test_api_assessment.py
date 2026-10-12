"""API tests: assessment flow end to end."""
import uuid

from fastapi.testclient import TestClient

from app.main import create_app


def _authz(client: TestClient) -> dict:
    email = f"as-{uuid.uuid4().hex[:8]}@x.com"
    r = client.post("/api/v1/auth/register",
                    json={"email": email, "password": "password123"})
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_assessment_full_flow():
    c = TestClient(create_app())
    h = _authz(c)

    r = c.post("/api/v1/assessments/start",
               json={"topic": "python", "level": "beginner", "count": 4},
               headers=h)
    assert r.status_code == 201, r.text
    body = r.json()
    assert len(body["questions"]) == 4
    assert all("answer_index" not in q for q in body["questions"])
    aid = body["assessment_id"]

    # submit all wrong -> gaps must be reported
    r = c.post(f"/api/v1/assessments/{aid}/submit",
               json={"answers": {q["id"]: 99 for q in body["questions"]}},
               headers=h)
    assert r.status_code == 200
    out = r.json()
    assert out["correct"] == 0 and out["total"] == 4
    assert out["ratio"] == 0.0
    assert out["gaps"], "expected gap report"
    assert out["per_skill"], "expected per-skill breakdown"

    # history lists it
    r = c.get("/api/v1/assessments", headers=h)
    assert r.status_code == 200
    assert any(a["assessment_id"] == aid for a in r.json()["assessments"])


def test_assessment_requires_auth():
    c = TestClient(create_app())
    assert c.post("/api/v1/assessments/start",
                  json={"topic": "python", "level": "beginner"}).status_code == 401


def test_assessment_bad_topic_400():
    c = TestClient(create_app())
    r = c.post("/api/v1/assessments/start",
               json={"topic": "cobol", "level": "beginner"},
               headers=_authz(c))
    assert r.status_code == 400


def test_bank_grew():
    c = TestClient(create_app())
    r = c.get("/api/v1/placement/topics", headers=_authz(c))
    assert set(r.json()["topics"]) == {"python", "ml-basics"}
