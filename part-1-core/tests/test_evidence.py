"""F5 tests: evidence domain rules, service, and HTTP API."""
import uuid

import pytest
from fastapi.testclient import TestClient

from app.adapters.inbound.evidence_service import EvidenceServiceImpl
from app.adapters.inbound.roadmap_service import RoadmapServiceImpl
from app.domain.evidence import validate_evidence
from app.domain.user import DomainError
from app.main import create_app
from tests.test_roadmap import MemRepo


# ---------- domain ----------

def test_validate_evidence_kinds():
    assert "Received" in validate_evidence("code", "def f():\n    return 1\n")
    assert "Link" in validate_evidence("url", "https://github.com/x/y")
    assert "words" in validate_evidence("text", "my notes here")


def test_validate_evidence_rejects_bad_input():
    with pytest.raises(DomainError):
        validate_evidence("video", "x")
    with pytest.raises(DomainError):
        validate_evidence("text", "   ")
    with pytest.raises(DomainError):
        validate_evidence("url", "not-a-url")
    with pytest.raises(DomainError):
        validate_evidence("code", "short")
    with pytest.raises(DomainError):
        validate_evidence("text", "x" * 20001)


# ---------- service ----------

class MemEvidenceRepo:
    def __init__(self):
        self.saved = []

    def save(self, e):
        self.saved.append(e)

    def list_for_task(self, user_id, task_key):
        return [e for e in self.saved if e.user_id == user_id and e.task_key == task_key]


def _svcs():
    repo = MemRepo()
    return (EvidenceServiceImpl(MemEvidenceRepo(), repo),
            RoadmapServiceImpl(repo))


def test_submit_closes_the_loop():
    ev_svc, rm_svc = _svcs()
    r = rm_svc.generate("u1", [{"skill": "sql", "mastery_pct": 30}])
    t = r.tasks[0]
    with pytest.raises(DomainError):  # must be in_progress first
        ev_svc.submit("u1", t.id, "text", "my notes")
    rm_svc.update_task("u1", t.id, "in_progress")
    ev = ev_svc.submit("u1", t.id, "text", "joins combine rows from two tables")
    assert ev.feedback and ev.task_key == t.id
    # task auto-completed by proof submission
    assert rm_svc.get_current("u1").tasks[0].status == "completed"
    with pytest.raises(DomainError):  # already completed
        ev_svc.submit("u1", t.id, "text", "more notes")
    assert len(ev_svc.list_for_task("u1", t.id)) == 1


def test_submit_unknown_task():
    ev_svc, rm_svc = _svcs()
    rm_svc.generate("u1", [{"skill": "sql", "mastery_pct": 30}])
    with pytest.raises(DomainError):
        ev_svc.submit("u1", "nope", "text", "notes")


# ---------- API ----------

def _client():
    return TestClient(create_app())


def _authz(c: TestClient) -> dict:
    email = f"ev-{uuid.uuid4().hex[:8]}@x.com"
    r = c.post("/api/v1/auth/register",
               json={"email": email, "password": "password123"})
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def _roadmap_with_task(c: TestClient, h: dict) -> str:
    r = c.post("/api/v1/roadmaps/generate", headers=h, json={
        "gaps": [{"skill": "sql", "mastery_pct": 30}]})
    assert r.status_code == 201, r.text
    tid = r.json()["tasks"][0]["id"]
    r = c.patch(f"/api/v1/roadmaps/tasks/{tid}",
                headers=h, json={"status": "in_progress"})
    assert r.status_code == 200, r.text
    return tid


def test_api_evidence_flow():
    c = _client()
    h = _authz(c)
    tid = _roadmap_with_task(c, h)
    r = c.post(f"/api/v1/roadmaps/tasks/{tid}/evidence", headers=h, json={
        "kind": "text",
        "content": "JOIN combines rows from two tables on a matching key.",
    })
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["task_key"] == tid and body["feedback"]
    # task completed by the submission
    r = c.get("/api/v1/roadmaps/current", headers=h)
    assert r.json()["task_counts"]["completed"] == 1
    # history is append-only
    r = c.get(f"/api/v1/roadmaps/tasks/{tid}/evidence", headers=h)
    assert r.status_code == 200 and len(r.json()) == 1


def test_api_evidence_requires_auth():
    c = _client()
    assert c.post("/api/v1/roadmaps/tasks/t0001/evidence",
                  json={"kind": "text", "content": "x"}).status_code == 401
    assert c.get("/api/v1/roadmaps/tasks/t0001/evidence").status_code == 401


def test_api_evidence_validates_input():
    c = _client()
    h = _authz(c)
    tid = _roadmap_with_task(c, h)
    r = c.post(f"/api/v1/roadmaps/tasks/{tid}/evidence", headers=h, json={
        "kind": "video", "content": "x"})
    assert r.status_code == 400
    # other user's task is invisible
    h2 = _authz(c)
    r = c.post(f"/api/v1/roadmaps/tasks/{tid}/evidence", headers=h2, json={
        "kind": "text", "content": "trying to cheat"})
    assert r.status_code == 400
