"""F4 tests: roadmap domain rules, service, and HTTP API."""
import uuid

import pytest
from fastapi.testclient import TestClient

from app.adapters.inbound.roadmap_service import RoadmapServiceImpl
from app.domain.roadmap import (
    Roadmap,
    SkillGap,
    generate_tasks,
    regenerate_tasks,
)
from app.domain.user import DomainError
from app.main import create_app


# ---------- domain: generation ----------

def test_generate_tasks_worst_gap_first():
    tasks = generate_tasks([
        SkillGap("sql", 80),
        SkillGap("python-basics", 20),
    ])
    assert len(tasks) == 6
    # worst gap (python-basics) comes first
    assert tasks[0].target_skills == ("python-basics",)
    assert tasks[0].priority == "high"
    assert tasks[3].target_skills == ("sql",)
    assert tasks[3].priority == "low"


def test_generate_tasks_learn_practice_build_chain():
    tasks = generate_tasks([SkillGap("oops", 50)])
    assert len(tasks) == 3
    assert tasks[0].title.startswith("Learn:")
    assert tasks[1].title.startswith("Practice:")
    assert tasks[2].title.startswith("Build:")
    assert tasks[1].prerequisites == (tasks[0].id,)
    assert tasks[2].prerequisites == (tasks[1].id,)
    assert all(t.status == "pending" for t in tasks)
    assert all(t.why_it_matters for t in tasks)
    assert all(t.expected_evidence and t.acceptance_criteria for t in tasks)


def test_generate_tasks_rejects_bad_input():
    with pytest.raises(DomainError):
        generate_tasks([])
    with pytest.raises(DomainError):
        generate_tasks([SkillGap("x", 150)])
    with pytest.raises(DomainError):
        generate_tasks([SkillGap("  ", 30)])


def test_task_transition_rules():
    t = generate_tasks([SkillGap("sql", 30)])[0]
    t.transition("in_progress")
    assert t.status == "in_progress"
    t.transition("completed")
    assert t.status == "completed"
    with pytest.raises(DomainError):  # completed is terminal
        t.transition("pending")
    t2 = generate_tasks([SkillGap("sql", 30)])[0]
    with pytest.raises(DomainError):  # no skipping
        t2.transition("completed")
    with pytest.raises(DomainError):
        t2.transition("bogus")


def test_regenerate_preserves_completed():
    old_tasks = generate_tasks([SkillGap("python-basics", 20)])
    old_tasks[0].transition("in_progress")
    old_tasks[0].transition("completed")
    old_tasks[1].transition("in_progress")
    old = Roadmap(id="r1", user_id="u1", version=1, title="R",
                  source="manual", tasks=old_tasks)
    new_tasks = regenerate_tasks(old, [SkillGap("python-basics", 55)])
    # completed task survives untouched
    carried = [t for t in new_tasks if t.status == "completed"]
    assert len(carried) == 1
    assert carried[0].id == old_tasks[0].id
    assert carried[0].title == old_tasks[0].title
    # in-progress task was regenerated, not deleted-then-lost: total stays 3
    assert len(new_tasks) == 3  # 1 carried + 2 fresh
    ids = [t.id for t in new_tasks]
    assert len(set(ids)) == len(ids)  # no id collisions


# ---------- service (in-memory repo) ----------

class MemRepo:
    def __init__(self):
        self.saved: list[Roadmap] = []

    def save(self, roadmap):
        self.saved = [r for r in self.saved if r.id != roadmap.id] + [roadmap]

    def get_current(self, user_id):
        cands = [r for r in self.saved if r.user_id == user_id]
        return max(cands, key=lambda r: r.version) if cands else None

    def list_versions(self, user_id):
        return sorted([r for r in self.saved if r.user_id == user_id],
                      key=lambda r: r.version, reverse=True)

    def max_version(self, user_id):
        cur = self.get_current(user_id)
        return cur.version if cur else 0


def _svc():
    return RoadmapServiceImpl(MemRepo())


def test_service_generate_and_current():
    svc = _svc()
    with pytest.raises(DomainError):
        svc.get_current("u1")
    r = svc.generate("u1", [{"skill": "sql", "mastery_pct": 30}])
    assert r.version == 1
    assert len(r.tasks) == 3
    assert svc.get_current("u1").id == r.id


def test_service_regenerate_bumps_version_and_keeps_completed():
    svc = _svc()
    r = svc.generate("u1", [{"skill": "sql", "mastery_pct": 30}])
    t0 = r.tasks[0]
    svc.update_task("u1", t0.id, "in_progress")
    svc.update_task("u1", t0.id, "completed")
    r2 = svc.regenerate("u1", [{"skill": "sql", "mastery_pct": 75}])
    assert r2.version == 2
    done = [t for t in r2.tasks if t.status == "completed"]
    assert len(done) == 1 and done[0].id == t0.id
    assert len(svc.list_versions("u1")) == 2


def test_service_update_task_not_found():
    svc = _svc()
    svc.generate("u1", [{"skill": "sql", "mastery_pct": 30}])
    with pytest.raises(DomainError):
        svc.update_task("u1", "nope", "completed")


# ---------- API ----------

def _client():
    return TestClient(create_app())


def _authz(c: TestClient) -> dict:
    email = f"rm-{uuid.uuid4().hex[:8]}@x.com"
    r = c.post("/api/v1/auth/register",
               json={"email": email, "password": "password123"})
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


_GAPS = {"gaps": [
    {"skill": "python-basics", "mastery_pct": 35},
    {"skill": "sql", "mastery_pct": 60},
]}


def test_api_full_roadmap_flow():
    c = _client()
    h = _authz(c)
    # generate
    r = c.post("/api/v1/roadmaps/generate", json=_GAPS, headers=h)
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["version"] == 1
    assert body["task_counts"]["total"] == 6
    assert body["tasks"][0]["target_skills"] == ["python-basics"]
    # current
    r = c.get("/api/v1/roadmaps/current", headers=h)
    assert r.status_code == 200
    assert r.json()["id"] == body["id"]
    # move a task forward
    tid = body["tasks"][0]["id"]
    r = c.patch(f"/api/v1/roadmaps/tasks/{tid}",
                json={"status": "in_progress"}, headers=h)
    assert r.status_code == 200 and r.json()["status"] == "in_progress"
    r = c.patch(f"/api/v1/roadmaps/tasks/{tid}",
                json={"status": "completed"}, headers=h)
    assert r.status_code == 200
    # illegal jump rejected
    tid2 = body["tasks"][1]["id"]
    r = c.patch(f"/api/v1/roadmaps/tasks/{tid2}",
                json={"status": "completed"}, headers=h)
    assert r.status_code == 400
    # regenerate: completed survives, version bumps
    r = c.post("/api/v1/roadmaps/regenerate", json=_GAPS, headers=h)
    assert r.status_code == 201, r.text
    body2 = r.json()
    assert body2["version"] == 2
    done = [t for t in body2["tasks"] if t["status"] == "completed"]
    assert len(done) == 1 and done[0]["id"] == tid
    # versions list
    r = c.get("/api/v1/roadmaps", headers=h)
    assert r.status_code == 200 and len(r.json()) == 2


def test_api_roadmap_requires_auth():
    c = _client()
    assert c.get("/api/v1/roadmaps/current").status_code == 401
    assert c.post("/api/v1/roadmaps/generate", json=_GAPS).status_code == 401


def test_api_roadmap_bad_input():
    c = _client()
    h = _authz(c)
    r = c.post("/api/v1/roadmaps/generate", json={"gaps": []}, headers=h)
    assert r.status_code in (400, 422)
    r = c.get("/api/v1/roadmaps/current", headers=h)
    # fresh user has no roadmap
    assert r.status_code == 400
