"""P3b tests: certificates — earned, not self-issued; public verify."""
import uuid

import pytest
from fastapi.testclient import TestClient

from app.domain.certificate import (
    check_roadmap_eligible,
    new_verification_code,
)
from app.main import create_app


def test_verification_code_format():
    c1, c2 = new_verification_code(), new_verification_code()
    assert c1.startswith("SF-") and len(c1) == 11
    assert c1 != c2


def test_check_roadmap_eligible():
    class T:
        def __init__(self, s): self.status = s
    class R:
        def __init__(self, ts): self.tasks = ts
    ok, _ = check_roadmap_eligible(R([T("completed"), T("completed")]))
    assert ok is True
    ok, reason = check_roadmap_eligible(R([T("completed"), T("pending")]))
    assert ok is False and "1/2" in reason
    ok, _ = check_roadmap_eligible(None)
    assert ok is False
    ok, _ = check_roadmap_eligible(R([]))
    assert ok is False


def _client():
    return TestClient(create_app())


def _authz(c: TestClient) -> dict:
    email = f"ct-{uuid.uuid4().hex[:8]}@x.com"
    r = c.post("/api/v1/auth/register",
               json={"email": email, "password": "password123"})
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def _complete_all_tasks(c: TestClient, h: dict, roadmap_id: str, tasks: list):
    for t in tasks:
        if t["status"] == "pending":
            r = c.patch(f"/api/v1/roadmaps/tasks/{t['id']}",
                        json={"status": "in_progress"}, headers=h)
            assert r.status_code == 200, r.text
        r = c.patch(f"/api/v1/roadmaps/tasks/{t['id']}",
                    json={"status": "completed"}, headers=h)
        assert r.status_code == 200, r.text


def test_certificate_full_flow():
    c = _client()
    h = _authz(c)

    # no certificates yet
    assert c.get("/api/v1/launchpad/certificates", headers=h).json() == []

    # roadmap with one gap -> 3 tasks
    rg = c.post("/api/v1/roadmaps/generate", headers=h,
                json={"gaps": [{"skill": "python-basics", "mastery_pct": 30}]})
    assert rg.status_code == 201, rg.text
    roadmap = rg.json()

    # not eligible before completing tasks
    bad = c.post("/api/v1/launchpad/certificates/issue", headers=h,
                 json={"kind": "roadmap", "ref_id": roadmap["id"]})
    assert bad.status_code == 400
    assert "not eligible" in bad.json()["detail"]

    _complete_all_tasks(c, h, roadmap["id"], roadmap["tasks"])

    # now eligible
    ok = c.post("/api/v1/launchpad/certificates/issue", headers=h,
                json={"kind": "roadmap", "ref_id": roadmap["id"]})
    assert ok.status_code == 200, ok.text
    cert = ok.json()
    assert cert["verification_code"].startswith("SF-")
    assert "Roadmap Completion" in cert["title"]

    # duplicate issue rejected
    dup = c.post("/api/v1/launchpad/certificates/issue", headers=h,
                 json={"kind": "roadmap", "ref_id": roadmap["id"]})
    assert dup.status_code == 400

    # list shows it
    lst = c.get("/api/v1/launchpad/certificates", headers=h).json()
    assert len(lst) == 1 and lst[0]["id"] == cert["id"]

    # PUBLIC verify works without auth
    v = c.get(f"/api/v1/launchpad/certificates/verify/{cert['verification_code']}")
    assert v.status_code == 200
    assert v.json()["valid"] is True
    assert v.json()["issued_to"] is not None

    v2 = c.get("/api/v1/launchpad/certificates/verify/SF-FAKECODE")
    assert v2.json()["valid"] is False


def test_issue_rejects_unknown_kind_and_auth():
    c = _client()
    h = _authz(c)
    r = c.post("/api/v1/launchpad/certificates/issue", headers=h,
               json={"kind": "nope", "ref_id": "x"})
    assert r.status_code == 400
    assert c.get("/api/v1/launchpad/certificates").status_code == 401
    assert c.post("/api/v1/launchpad/certificates/issue",
                  json={"kind": "roadmap", "ref_id": "x"}).status_code == 401
