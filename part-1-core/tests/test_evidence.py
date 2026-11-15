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
    def __init__(self, roadmaps=None):
        self.saved = []
        self.roadmaps = roadmaps

    def save(self, e):
        self.saved.append(e)

    def get_by_id(self, evidence_id):
        return next((e for e in self.saved if e.id == evidence_id), None)

    def update_review(self, evidence, complete_task=False):
        if complete_task and self.roadmaps:
            self.roadmaps.complete_verified_task(evidence.user_id, evidence.task_key)
        return True

    def list_pending(self):
        return [e for e in self.saved if e.status == "pending_review"]

    def list_for_task(self, user_id, task_key):
        return [e for e in self.saved if e.user_id == user_id and e.task_key == task_key]


def _svcs():
    repo = MemRepo()
    roadmap_service = RoadmapServiceImpl(repo)
    ev_repo = MemEvidenceRepo(roadmap_service)
    return (EvidenceServiceImpl(ev_repo, roadmap_service), roadmap_service, ev_repo)


def test_submit_waits_for_review_then_verification_completes_task():
    ev_svc, rm_svc, ev_repo = _svcs()
    r = rm_svc.generate("u1", [{"skill": "sql", "mastery_pct": 30}])
    task = r.tasks[0]
    with pytest.raises(DomainError):
        ev_svc.submit("u1", task.id, "text", "my notes")
    rm_svc.update_task("u1", task.id, "in_progress")
    ev = ev_svc.submit("u1", task.id, "text", "joins combine rows from two tables")
    assert ev.feedback and ev.task_key == task.id
    assert ev.status == "pending_review"
    assert rm_svc.get_current("u1").tasks[0].status == "in_progress"
    assert len(ev_svc.list_pending()) == 1

    reviewed = ev_svc.review("reviewer-1", ev.id, "verified", "Meets the acceptance criteria.")
    assert reviewed.status == "verified"
    assert reviewed.reviewed_by == "reviewer-1"
    assert reviewed.reviewed_at is not None
    assert rm_svc.get_current("u1").tasks[0].status == "completed"
    with pytest.raises(DomainError):
        ev_svc.review("reviewer-1", ev.id, "verified", "Duplicate review")
    assert len(ev_svc.list_for_task("u1", task.id)) == 1


def test_stale_evidence_cannot_verify_a_new_roadmap_task():
    ev_svc, rm_svc, _ = _svcs()
    old_roadmap = rm_svc.generate("u1", [{"skill": "sql", "mastery_pct": 30}])
    old_task = old_roadmap.tasks[0]
    rm_svc.update_task("u1", old_task.id, "in_progress")
    evidence = ev_svc.submit(
        "u1", old_task.id, "text", "joins combine rows from two tables"
    )

    new_roadmap = rm_svc.regenerate("u1", [{"skill": "sql", "mastery_pct": 70}])
    assert new_roadmap.id != old_roadmap.id

    with pytest.raises(DomainError, match="older roadmap"):
        ev_svc.review("reviewer-1", evidence.id, "verified", "Looks good")


def test_rejected_evidence_keeps_task_open_and_requires_feedback():
    ev_svc, rm_svc, _ = _svcs()
    task = rm_svc.generate("u1", [{"skill": "sql", "mastery_pct": 30}]).tasks[0]
    rm_svc.update_task("u1", task.id, "in_progress")
    ev = ev_svc.submit("u1", task.id, "text", "joins combine rows from two tables")
    with pytest.raises(DomainError):
        ev_svc.review("reviewer-1", ev.id, "rejected", "")
    reviewed = ev_svc.review("reviewer-1", ev.id, "needs_changes", "Add a real query example.")
    assert reviewed.status == "needs_changes"
    assert rm_svc.get_current("u1").tasks[0].status == "in_progress"


def test_submit_unknown_task():
    ev_svc, rm_svc, _ = _svcs()
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
    assert body["status"] == "pending_review"
    # Submitting proof does not falsely mark the task complete.
    r = c.get("/api/v1/roadmaps/current", headers=h)
    assert r.json()["task_counts"]["completed"] == 0
    assert r.json()["task_counts"]["in_progress"] == 1
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

def test_review_queue_requires_admin_until_tenant_scoping_exists():
    c = _client()
    h = _authz(c)
    assert c.get("/api/v1/evidence/review-queue", headers=h).status_code == 403


def test_reviewer_can_verify_evidence_and_close_task():
    c = _client()
    learner = _authz(c)
    reviewer_email = f"reviewer-{uuid.uuid4().hex[:8]}@x.com"
    reviewer_reg = c.post("/api/v1/auth/register", json={
        "email": reviewer_email, "password": "password123"})
    assert reviewer_reg.status_code == 201
    reviewer_id = reviewer_reg.json()["user"]["id"]
    c.app.state.auth_service.set_role(reviewer_id, "admin")
    reviewer_login = c.post("/api/v1/auth/login", json={
        "email": reviewer_email, "password": "password123"})
    rh = {"Authorization": f"Bearer {reviewer_login.json()['access_token']}"}

    task_id = _roadmap_with_task(c, learner)
    submitted = c.post(f"/api/v1/roadmaps/tasks/{task_id}/evidence",
        headers=learner, json={"kind": "text", "content": "JOIN combines rows using a matching key."})
    assert submitted.status_code == 201, submitted.text
    evidence_id = submitted.json()["id"]

    queue = c.get("/api/v1/evidence/review-queue", headers=rh)
    assert queue.status_code == 200
    assert any(item["id"] == evidence_id for item in queue.json())

    reviewed = c.post(f"/api/v1/evidence/{evidence_id}/review", headers=rh,
        json={"decision": "verified", "note": "Clear explanation and valid example."})
    assert reviewed.status_code == 200, reviewed.text
    assert reviewed.json()["status"] == "verified"
    current = c.get("/api/v1/roadmaps/current", headers=learner)
    assert current.json()["task_counts"]["completed"] == 1

def test_reviewer_cannot_review_own_evidence():
    ev_svc, rm_svc, _ = _svcs()
    task = rm_svc.generate("learner-1", [{"skill": "sql", "mastery_pct": 30}]).tasks[0]
    rm_svc.update_task("learner-1", task.id, "in_progress")
    ev = ev_svc.submit("learner-1", task.id, "text", "joins combine rows from two tables")
    with pytest.raises(DomainError):
        ev_svc.review("learner-1", ev.id, "verified", "Self review")
