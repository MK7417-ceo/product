"""Tests: streak system — domain logic, service, API."""
import uuid
from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.adapters.inbound.streak_service import StreakServiceImpl
from app.adapters.outbound.models import Base, UserModel
from app.adapters.outbound.streak_repository import SqlAlchemyStreakRepository
from app.core.database import SessionLocal
from app.domain.streak import UserStreak, apply_activity, milestone_for
from app.main import create_app


def _factory():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def _blank(uid="u1"):
    return UserStreak(uid, 0, 0, None, 0)


# ---------- domain ----------

def test_first_activity_starts_streak():
    s = apply_activity(_blank(), date(2026, 10, 15))
    assert (s.current_streak, s.longest_streak, s.total_days_active) == (1, 1, 1)
    assert s.last_activity_date == date(2026, 10, 15)


def test_consecutive_day_increments():
    s = apply_activity(_blank(), date(2026, 10, 15))
    s = apply_activity(s, date(2026, 10, 16))
    assert s.current_streak == 2
    assert s.longest_streak == 2
    assert s.total_days_active == 2


def test_gap_resets_current_but_keeps_longest():
    s = apply_activity(_blank(), date(2026, 10, 15))
    s = apply_activity(s, date(2026, 10, 16))   # streak 2
    s = apply_activity(s, date(2026, 10, 20))   # 4-day gap
    assert s.current_streak == 1
    assert s.longest_streak == 2
    assert s.total_days_active == 3


def test_same_day_is_idempotent():
    s = apply_activity(_blank(), date(2026, 10, 15))
    s2 = apply_activity(s, date(2026, 10, 15))
    assert s2 is s  # no change at all


def test_milestones():
    assert milestone_for(7) == "week"
    assert milestone_for(30) == "month"
    assert milestone_for(100) == "century"
    assert milestone_for(8) is None


# ---------- service ----------

def test_service_records_and_summarizes():
    svc = StreakServiceImpl(SqlAlchemyStreakRepository(_factory()),
                            today_fn=lambda: date(2026, 10, 15))
    out = svc.record_activity("u9")
    assert out["current_streak"] == 1
    assert out["today_done"] is True
    assert out["recent_days"] == ["2026-10-15"]

    # second call same day: no double count
    out = svc.record_activity("u9")
    assert out["current_streak"] == 1
    assert out["total_days_active"] == 1


def test_service_gap_and_longest():
    days = iter([date(2026, 10, 15), date(2026, 10, 16), date(2026, 10, 20)])
    svc = StreakServiceImpl(SqlAlchemyStreakRepository(_factory()),
                            today_fn=lambda: next(days))
    svc.record_activity("u9")
    svc.record_activity("u9")
    out = svc.record_activity("u9")
    assert out["current_streak"] == 1
    assert out["longest_streak"] == 2
    assert len(out["recent_days"]) == 3


# ---------- API ----------

def _client():
    return TestClient(create_app())


def _token(client):
    email = f"streak-{uuid.uuid4().hex[:8]}@x.com"
    r = client.post("/api/v1/auth/register",
                    json={"email": email, "password": "password123"})
    assert r.status_code == 201, r.text
    r = client.post("/api/v1/auth/login",
                    json={"email": email, "password": "password123"})
    return r.json()["access_token"]


def test_api_streak_mine():
    c = _client()
    h = {"Authorization": f"Bearer {_token(c)}"}

    r = c.get("/api/v1/streak/mine", headers=h)
    assert r.status_code == 200
    body = r.json()
    assert body["current_streak"] == 0
    assert body["today_done"] is False

    # unauthenticated -> 401
    r = c.get("/api/v1/streak/mine")
    assert r.status_code == 401


def test_api_task_completion_records_streak():
    """Completing a curriculum task bumps the streak via the API hook."""
    from app.adapters.outbound.models import CurriculumDomainModel
    from app.core.database import SessionLocal as _SL, engine as _eng
    from app.adapters.outbound.models import Base as _Base
    _Base.metadata.create_all(_eng)
    with _SL() as s:
        exists = s.query(CurriculumDomainModel).filter_by(slug="dsa").first()
        if not exists:
            s.add(CurriculumDomainModel(
                id="seed-dsa-test", slug="dsa", name="DSA", icon="🧠",
                description="t", category="cs-core", order_index=1,
                is_active=True))
            s.commit()

    c = _client()
    tok = _token(c)
    h = {"Authorization": f"Bearer {tok}"}

    # create a study plan (generates daily tasks)
    r = c.post("/api/v1/curriculum/plans",
               json={"domain_slug": "dsa", "start_level": "scratch",
                     "total_days": 7},
               headers=h)
    assert r.status_code in (200, 201), r.text
    plan_id = r.json()["id"] if "id" in r.json() else r.json()["plan"]["id"]

    r = c.get("/api/v1/curriculum/plans/mine", headers=h)
    plans = r.json()["plans"]
    my = next(p for p in plans if p["id"] == plan_id)
    tasks = my.get("today_tasks") or my.get("tasks") or []
    assert tasks, "plan should have tasks"

    task_id = tasks[0]["id"]
    r = c.patch(f"/api/v1/curriculum/tasks/{task_id}",
                json={"status": "done"}, headers=h)
    assert r.status_code == 200, r.text

    r = c.get("/api/v1/streak/mine", headers=h)
    body = r.json()
    assert body["current_streak"] == 1
    assert body["today_done"] is True
    assert body["total_days_active"] == 1
