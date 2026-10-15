"""Tests: content CMS — topics, theory, questions (service + API + importer)."""
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.adapters.inbound.content_service import ContentServiceImpl
from app.adapters.inbound.link_importer import import_from_url
from app.adapters.outbound.content_repository import SqlAlchemyContentRepository
from app.adapters.outbound.models import Base, UserModel
from app.core.database import SessionLocal
from app.domain.content import DomainError
from app.main import create_app


@pytest.fixture()
def svc():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    return ContentServiceImpl(SqlAlchemyContentRepository(factory))


def test_create_and_list_topics(svc):
    svc.create_topic("javascript", "JavaScript", "JS from zero to hero", "js", "#f7df1e")
    topics = svc.list_topics()
    assert len(topics) == 1
    assert topics[0]["slug"] == "javascript"
    assert topics[0]["name"] == "JavaScript"
    assert topics[0]["is_active"] is True


def test_duplicate_slug_rejected(svc):
    svc.create_topic("golang", "Go")
    with pytest.raises(DomainError, match="already exists"):
        svc.create_topic("golang", "Go Again")


def test_bad_slug_rejected(svc):
    with pytest.raises(DomainError, match="invalid topic slug"):
        svc.create_topic("Bad Slug!!", "Bad")


def test_theory_crud_ordered(svc):
    svc.create_topic("rust", "Rust")
    svc.add_theory("rust", "beginner", "Ownership", "# Ownership\n...", order_index=1)
    svc.add_theory("rust", "beginner", "Install", "# Install\n...", order_index=0)
    blocks = svc.list_theory("rust")
    assert [b["title"] for b in blocks] == ["Install", "Ownership"]
    assert svc.list_theory("rust", level="beginner") != []
    with pytest.raises(DomainError, match="invalid level"):
        svc.list_theory("rust", level="expert")


def test_mcq_question_validation(svc):
    svc.create_topic("sql", "SQL")
    # missing answer_index -> rejected
    with pytest.raises(DomainError, match="answer_index"):
        svc.add_question("sql", "mcq", "beginner", "Pick one",
                         choices=["a", "b"], answer_index=None)
    # coding must not carry answer_index
    with pytest.raises(DomainError, match="must not have answer_index"):
        svc.add_question("sql", "coding", "beginner", "Write a query",
                         answer_index=0)
    q = svc.add_question("sql", "mcq", "beginner", "Pick one",
                         skill_tag="select", choices=["a", "b"], answer_index=1)
    assert q["answer_index"] == 1
    assert q["choices"] == ["a", "b"]
    qs = svc.list_questions("sql", qtype="mcq", level="beginner")
    assert len(qs) == 1


def test_delete_topic_cascades(svc):
    svc.create_topic("kotlin", "Kotlin")
    svc.add_theory("kotlin", "beginner", "Intro", "content")
    svc.add_question("kotlin", "written", "beginner", "Explain coroutines")
    assert len(svc.list_theory("kotlin")) == 1
    svc.delete_topic("kotlin")
    assert svc.list_topics() == []
    with pytest.raises(DomainError, match="topic not found"):
        svc.get_topic("kotlin")


def test_topic_detail_has_counts(svc):
    svc.create_topic("swift", "Swift")
    svc.add_question("swift", "mcq", "beginner", "Q1",
                     choices=["a", "b"], answer_index=0)
    svc.add_question("swift", "coding", "intermediate", "Q2")
    detail = svc.get_topic("swift")
    assert detail["question_counts"] == {"mcq:beginner": 1, "coding:intermediate": 1}


# ---- link importer: failure paths (no real network needed) ----
def test_importer_rejects_private_host():
    r = import_from_url("http://localhost:8000/admin")
    assert r["ok"] is False
    assert "private" in r["error"].lower()


def test_importer_rejects_bad_scheme():
    r = import_from_url("ftp://example.com/x")
    assert r["ok"] is False
    assert "http" in r["error"].lower()


def test_importer_rejects_garbage():
    r = import_from_url("not a url")
    assert r["ok"] is False


def test_importer_graceful_on_unreachable():
    # TEST-NET-1 documentation IP: unreachable; must return ok=False, never raise
    r = import_from_url("http://192.0.2.1/nope")
    assert r["ok"] is False
    assert r["error"]


# ---- API ----
def _client() -> TestClient:
    return TestClient(create_app())


def _register(client: TestClient, role: str = "user") -> str:
    email = f"cms-{uuid.uuid4().hex[:8]}@x.com"
    r = client.post("/api/v1/auth/register",
                    json={"email": email, "password": "password123"})
    assert r.status_code == 201, r.text
    if role == "admin":
        with SessionLocal() as s:
            m = s.query(UserModel).filter_by(email=email).one()
            m.role = "admin"
            s.commit()
    r = client.post("/api/v1/auth/login",
                    json={"email": email, "password": "password123"})
    return r.json()["access_token"]


def test_api_public_topics_and_admin_write():
    c = _client()
    # public list works without auth
    r = c.get("/api/v1/content/topics")
    assert r.status_code == 200
    assert "topics" in r.json()

    user_tok = _register(c, "user")
    admin_tok = _register(c, "admin")
    user_h = {"Authorization": f"Bearer {user_tok}"}
    admin_h = {"Authorization": f"Bearer {admin_tok}"}

    # non-admin POST -> 403
    r = c.post("/api/v1/content/topics",
               json={"slug": "deno-x", "name": "Deno"},
               headers=user_h)
    assert r.status_code == 403

    # admin creates
    r = c.post("/api/v1/content/topics",
               json={"slug": "deno", "name": "Deno", "description": "JS runtime"},
               headers=admin_h)
    assert r.status_code == 201, r.text
    assert r.json()["slug"] == "deno"

    # admin adds theory + question
    r = c.post("/api/v1/content/topics/deno/theory",
               json={"level": "beginner", "title": "Hello", "content": "# Hi"},
               headers=admin_h)
    assert r.status_code == 201, r.text
    r = c.post("/api/v1/content/topics/deno/questions",
               json={"qtype": "mcq", "level": "beginner", "prompt": "Q?",
                     "choices": ["a", "b"], "answer_index": 0},
               headers=admin_h)
    assert r.status_code == 201, r.text

    # public reads see it
    r = c.get("/api/v1/content/topics/deno")
    assert r.status_code == 200
    assert r.json()["question_counts"] == {"mcq:beginner": 1}
    r = c.get("/api/v1/content/topics/deno/theory")
    assert r.status_code == 200
    assert len(r.json()["theory"]) == 1

    # admin delete cascades
    r = c.delete("/api/v1/content/topics/deno", headers=admin_h)
    assert r.status_code == 204
    r = c.get("/api/v1/content/topics/deno")
    assert r.status_code == 400  # codebase convention: domain errors -> 400


def test_api_import_url_admin_only():
    c = _client()
    user_tok = _register(c, "user")
    r = c.post("/api/v1/content/import-url", json={"url": "http://localhost/"},
               headers={"Authorization": f"Bearer {user_tok}"})
    assert r.status_code == 403
    admin_tok = _register(c, "admin")
    r = c.post("/api/v1/content/import-url", json={"url": "http://localhost/"},
               headers={"Authorization": f"Bearer {admin_tok}"})
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is False  # private host blocked, honest error
