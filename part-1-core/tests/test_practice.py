"""F6 tests: daily questions + aaj ka plan (domain, service, HTTP API)."""
import uuid

from fastapi.testclient import TestClient

from app.adapters.inbound.practice_service import PracticeServiceImpl
from app.adapters.outbound.question_bank import StaticQuestionBank
from app.domain.practice import (
    daily_question_ids,
    daily_questions,
    score_daily,
    todays_tasks,
)
from app.domain.roadmap import SkillGap, generate_tasks
from app.domain.user import DomainError
from app.main import create_app

import pytest


# ---------- domain: determinism ----------

def _bank():
    return StaticQuestionBank()


def test_daily_same_user_same_day_same_set():
    b = _bank()
    a = daily_question_ids("u1", "2026-10-12", b)
    c = daily_question_ids("u1", "2026-10-12", b)
    assert a.question_ids == c.question_ids
    assert len(a.question_ids) == 3


def test_daily_different_day_different_set():
    b = _bank()
    a = daily_question_ids("u1", "2026-10-12", b)
    c = daily_question_ids("u1", "2026-10-13", b)
    assert a.question_ids != c.question_ids


def test_daily_different_user_different_set():
    b = _bank()
    a = daily_question_ids("u1", "2026-10-12", b)
    c = daily_question_ids("u2", "2026-10-12", b)
    assert a.question_ids != c.question_ids


def test_daily_public_questions_have_no_keys():
    qs = daily_questions("u1", "2026-10-12", _bank())
    assert len(qs) == 3
    assert all("answer_index" not in q for q in qs)
    assert all(q["choices"] for q in qs)


def test_daily_rejects_bad_input():
    with pytest.raises(DomainError):
        daily_question_ids("", "2026-10-12", _bank())
    with pytest.raises(DomainError):
        daily_question_ids("u1", "nope", _bank())


def test_score_daily_all_correct():
    b = _bank()
    picked = daily_question_ids("u1", "2026-10-12", b)
    answers = {qid: b.get(qid).answer_index for qid in picked.question_ids}
    correct, total = score_daily("u1", "2026-10-12", answers, b)
    assert (correct, total) == (3, 3)


def test_score_daily_partial_and_unknown_rejected():
    b = _bank()
    picked = daily_question_ids("u1", "2026-10-12", b)
    answers = {picked.question_ids[0]: b.get(picked.question_ids[0]).answer_index,
               picked.question_ids[1]: 999}
    correct, total = score_daily("u1", "2026-10-12", answers, b)
    assert (correct, total) == (1, 3)
    with pytest.raises(DomainError):
        score_daily("u1", "2026-10-12", {"ghost": 0}, b)


def test_todays_tasks_picks_top_two_actionable():
    from app.domain.roadmap import Roadmap
    tasks = generate_tasks([SkillGap("python-basics", 20), SkillGap("sql", 60)])
    rm = Roadmap(id="r1", user_id="u", version=1, title="t", source="manual",
                 tasks=list(tasks))
    top = todays_tasks(rm)
    assert len(top) == 2
    assert all(t.status in ("pending", "in_progress") for t in top)
    assert top[0].priority == "high"
    assert todays_tasks(None) == []


# ---------- service + API ----------

def _client():
    return TestClient(create_app())


def _authz(c: TestClient) -> dict:
    email = f"pr-{uuid.uuid4().hex[:8]}@x.com"
    r = c.post("/api/v1/auth/register",
               json={"email": email, "password": "password123"})
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_api_daily_roundtrip_and_today():
    c = _client()
    h = _authz(c)

    r = c.get("/api/v1/practice/daily", headers=h)
    assert r.status_code == 200, r.text
    day = r.json()
    assert len(day["questions"]) == 3
    assert "answer_index" not in str(day)

    # repeat call, same day: same questions
    r2 = c.get("/api/v1/practice/daily", headers=h)
    assert [q["id"] for q in r2.json()["questions"]] == [q["id"] for q in day["questions"]]

    # submit: 0/3 (deliberately wrong answers)
    answers = {q["id"]: 999 for q in day["questions"]}
    rs = c.post("/api/v1/practice/daily/submit",
                json={"answers": answers}, headers=h)
    assert rs.status_code == 200, rs.text
    assert rs.json()["correct"] == 0
    assert rs.json()["total"] == 3

    # today without a roadmap: questions present, tasks empty
    rt = c.get("/api/v1/practice/today", headers=h)
    assert rt.status_code == 200, rt.text
    today = rt.json()
    assert len(today["questions"]) == 3
    assert today["tasks"] == []
    assert today["has_roadmap"] is False


def test_api_today_includes_roadmap_tasks():
    c = _client()
    h = _authz(c)
    gaps = {"gaps": [{"skill": "python-basics", "mastery_pct": 30}]}
    rg = c.post("/api/v1/roadmaps/generate", json=gaps, headers=h)
    assert rg.status_code == 201, rg.text

    rt = c.get("/api/v1/practice/today", headers=h)
    assert rt.status_code == 200, rt.text
    today = rt.json()
    assert today["has_roadmap"] is True
    assert len(today["tasks"]) == 2
    assert today["tasks"][0]["priority"] == "high"


def test_api_requires_auth():
    c = _client()
    assert c.get("/api/v1/practice/daily").status_code == 401
    assert c.post("/api/v1/practice/daily/submit",
                  json={"answers": {}}).status_code == 401
    assert c.get("/api/v1/practice/today").status_code == 401


def test_service_impl_deterministic():
    b = _bank()
    svc = PracticeServiceImpl(b, None)
    first = svc.daily("u9")["questions"]
    second = svc.daily("u9")["questions"]
    assert [q["id"] for q in first] == [q["id"] for q in second]
