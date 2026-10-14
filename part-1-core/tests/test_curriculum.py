"""Tests: curriculum — domain validators, service, API, study plans."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.adapters.inbound.curriculum_service import CurriculumServiceImpl
from app.adapters.outbound.curriculum_repository import SqlAlchemyCurriculumRepository
from app.adapters.outbound.models import Base, UserModel
from app.core.database import SessionLocal
from app.domain.curriculum import (
    DomainError,
    difficulty_band,
    difficulty_for_day,
    plan_task_types_for_day,
    validate_difficulty,
    validate_slug,
)
from app.main import create_app


@pytest.fixture()
def svc():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    return CurriculumServiceImpl(SqlAlchemyCurriculumRepository(factory))


# ---- domain validators ----

def test_difficulty_must_be_1_to_10():
    assert validate_difficulty(1) == 1
    assert validate_difficulty(10) == 10
    with pytest.raises(DomainError):
        validate_difficulty(0)
    with pytest.raises(DomainError):
        validate_difficulty(11)


def test_difficulty_bands():
    assert difficulty_band(1) == "basic"
    assert difficulty_band(3) == "basic"
    assert difficulty_band(4) == "intermediate"
    assert difficulty_band(7) == "advanced"
    assert difficulty_band(10) == "expert"


def test_difficulty_ramp_is_gradual():
    # "dheere dheere level badhega" — never jumps straight to hard
    assert difficulty_for_day(1, 30, "scratch") == 1
    assert difficulty_for_day(1, 30, "beginner") == 3
    assert difficulty_for_day(1, 30, "intermediate") == 5
    assert difficulty_for_day(30, 30, "scratch") == 10
    mid = difficulty_for_day(15, 30, "scratch")
    assert 1 < mid < 10  # gradual, not a jump


def test_task_type_rhythm():
    assert plan_task_types_for_day(1, 30) == ["learn", "practice"]
    assert "code" in plan_task_types_for_day(3, 30)
    assert "revise" in plan_task_types_for_day(7, 30)
    assert "mock" in plan_task_types_for_day(14, 30)
    assert "mock" in plan_task_types_for_day(30, 30)  # last day always mock


def test_bad_slug_rejected():
    with pytest.raises(DomainError):
        validate_slug("Bad Slug!!")


# ---- service: domains/modules/lessons/questions ----

def test_domain_crud(svc):
    d = svc.create_domain("test-dsa", "Test DSA", category="cs-core", icon="🧠")
    assert d["slug"] == "test-dsa"
    assert d["category"] == "cs-core"
    with pytest.raises(DomainError, match="already exists"):
        svc.create_domain("test-dsa", "Duplicate")
    domains = svc.list_domains()
    assert any(x["slug"] == "test-dsa" for x in domains)
    with pytest.raises(DomainError, match="invalid category"):
        svc.create_domain("bad-cat", "Bad", category="nope")


def test_module_lesson_chain(svc):
    svc.create_domain("test-os", "Test OS", category="cs-core")
    m = svc.create_module("test-os", "scheduling", "CPU Scheduling", estimated_days=5)
    assert m["domain_slug"] == "test-os"
    mods = svc.list_modules("test-os")
    assert len(mods) == 1
    les = svc.create_lesson(m["id"], "fcfs", "FCFS Scheduling",
                            content="## FCFS\nFirst come first served.", has_visual=True)
    assert les["has_visual"] is True
    lessons = svc.list_lessons(m["id"])
    assert [l["slug"] for l in lessons] == ["fcfs"]


def test_questions_ordered_by_difficulty(svc):
    svc.create_domain("test-db", "Test DB", category="cs-core")
    m = svc.create_module("test-db", "mod1", "Module 1")
    les = svc.create_lesson(m["id"], "les1", "Lesson 1")
    for diff in (8, 2, 5, 1):
        svc.add_question("test-db", "mcq", f"Q diff {diff}", difficulty=diff,
                         lesson_id=les["id"],
                         choices=["a", "b"], answer_index=0,
                         explanation=f"because {diff}")
    detail = svc.get_lesson_detail(les["id"])
    assert [q["difficulty"] for q in detail["questions"]] == [1, 2, 5, 8]  # 1→10 ramp order


def test_question_mcq_validation(svc):
    svc.create_domain("test-cn", "Test CN", category="cs-core")
    with pytest.raises(DomainError, match="at least 2 choices"):
        svc.add_question("test-cn", "mcq", "Bad MCQ", difficulty=3)  # no choices
    with pytest.raises(DomainError, match="1-10"):
        svc.add_question("test-cn", "mcq", "Bad diff", difficulty=99,
                         choices=["a", "b"], answer_index=0)


# ---- service: study plans ----

def _seed_plan_domain(svc):
    svc.create_domain("test-py", "Test Python", category="language")
    m = svc.create_module("test-py", "basics", "Basics", estimated_days=7)
    svc.create_lesson(m["id"], "variables", "Variables", content="# Vars")
    svc.create_lesson(m["id"], "loops", "Loops", content="# Loops")
    for diff in (1, 2, 3, 5, 8):
        svc.add_question("test-py", "mcq", f"Q{diff}", difficulty=diff,
                         choices=["a", "b"], answer_index=0,
                         explanation="why")


def test_create_study_plan_generates_tasks(svc):
    _seed_plan_domain(svc)
    plan = svc.create_study_plan("user-1", "test-py", "scratch", total_days=7)
    assert plan["domain_slug"] == "test-py"
    assert plan["total_days"] == 7
    assert plan["current_day"] == 1
    assert len(plan["tasks"]) >= 14  # ≥2 tasks/day × 7 days


def test_plan_task_ownership_guard(svc):
    _seed_plan_domain(svc)
    plan = svc.create_study_plan("user-1", "test-py", "scratch", total_days=7)
    task_id = plan["tasks"][0]["id"]
    with pytest.raises(DomainError, match="not your task"):
        svc.update_task("user-2", task_id, "done")
    done = svc.update_task("user-1", task_id, "done")
    assert done["status"] == "done"


def test_advance_day_completes_plan(svc):
    _seed_plan_domain(svc)
    plan = svc.create_study_plan("user-1", "test-py", "scratch", total_days=7)
    for _ in range(6):
        plan = svc.advance_day("user-1", plan["id"])
    assert plan["current_day"] == 7
    plan = svc.advance_day("user-1", plan["id"])
    assert plan["status"] == "completed"
    with pytest.raises(DomainError, match="already completed"):
        svc.advance_day("user-1", plan["id"])


def test_my_plans_returns_today_tasks(svc):
    _seed_plan_domain(svc)
    svc.create_study_plan("user-1", "test-py", "scratch", total_days=7)
    plans = svc.my_plans("user-1")
    assert len(plans) == 1
    assert len(plans[0]["today_tasks"]) >= 2
    assert all(t["day_number"] == 1 for t in plans[0]["today_tasks"])


# ---- API ----

@pytest.fixture()
def client():
    app = create_app()
    return TestClient(app)


def _make_user_and_token(client, email, role="user"):
    client.post("/api/v1/auth/register",
                json={"email": email, "password": "password123"})
    # promote via DB for admin test
    if role == "admin":
        with SessionLocal() as s:
            u = s.query(UserModel).filter_by(email=email).one()
            u.role = "admin"
            s.commit()
    r = client.post("/api/v1/auth/login",
                    json={"email": email, "password": "password123"})
    return r.json()["access_token"]


def test_api_public_domains(client):
    admin_tok = _make_user_and_token(client, "cur-pub@example.com", role="admin")
    client.post("/api/v1/curriculum/domains",
                json={"slug": "pub-dom", "name": "Public Dom", "category": "cs-core"},
                headers={"Authorization": f"Bearer {admin_tok}"})
    r = client.get("/api/v1/curriculum/domains")
    assert r.status_code == 200
    domains = r.json()["domains"]
    assert any(d["slug"] == "pub-dom" for d in domains)


def test_api_admin_write_requires_admin(client):
    user_tok = _make_user_and_token(client, "cur-u@example.com")
    r = client.post("/api/v1/curriculum/domains",
                    json={"slug": "x", "name": "X", "category": "cs-core"},
                    headers={"Authorization": f"Bearer {user_tok}"})
    assert r.status_code == 403
    admin_tok = _make_user_and_token(client, "cur-a@example.com", role="admin")
    r = client.post("/api/v1/curriculum/domains",
                    json={"slug": "test-api-dom", "name": "API Dom",
                          "category": "cs-core"},
                    headers={"Authorization": f"Bearer {admin_tok}"})
    assert r.status_code == 201
    assert r.json()["slug"] == "test-api-dom"


def test_api_plan_requires_auth(client):
    r = client.post("/api/v1/curriculum/plans",
                    json={"domain_slug": "dsa", "start_level": "scratch",
                          "total_days": 30})
    assert r.status_code in (401, 403)
