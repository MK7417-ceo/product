"""AI/RAG DB-first tests.

These prove the user-mandated rule, not just the happy path:
  - a DB hit NEVER calls the LLM (zero API cost),
  - an unvalidated (pending) LLM answer is NEVER served as a DB answer,
  - a miss without an API key degrades gracefully instead of inventing
    an answer or crashing.
"""
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.adapters.inbound.ai_answer_service import (
    AiAnswerServiceImpl,
    NullProvider,
)
from app.adapters.outbound.ai_answer_repository import (
    SqlAlchemyAiAnswerRepository,
)
from app.adapters.outbound.models import (
    AiAnswerModel,
    TheoryModel,
    TopicModel,
)
from app.core.database import Base
from app.domain.ai_answer import cosine, embed
from app.domain.user import DomainError
from app.main import create_app


class FakeProvider:
    """Records every call so tests can prove zero-call DB hits."""
    name = "fake"

    def __init__(self, text="fake llm answer"):
        self.calls: list[str] = []
        self.text = text

    def generate(self, question: str, context: str) -> str:
        self.calls.append(question)
        return self.text


def _service(provider):
    eng = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(eng)
    factory = sessionmaker(bind=eng)
    repo = SqlAlchemyAiAnswerRepository(factory)
    return repo, AiAnswerServiceImpl(repo, provider), factory


def _seed_approved(factory, question: str, answer: str) -> str:
    from app.domain.ai_answer import normalize_question
    with factory() as s:
        m = AiAnswerModel(
            id=uuid.uuid4().hex, question=question,
            normalized_question=normalize_question(question), answer=answer,
            source="manual", status="approved", topic_slug="",
            created_by="admin", approved_by="admin",
            embedding_json=__import__("json").dumps(embed(question)))
        s.add(m)
        s.commit()
        return m.id


def _seed_theory(factory, slug: str, title: str, content: str) -> None:
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    with factory() as s:
        s.add(TopicModel(id=uuid.uuid4().hex, slug=slug, name=slug,
                         created_at=now))
        s.add(TheoryModel(id=uuid.uuid4().hex, topic_slug=slug, level="beginner",
                          title=title, content=content, order_index=0,
                          created_at=now))
        s.commit()


def test_embedding_deterministic_and_self_similar():
    vec1 = embed("python me loop kya hota hai")
    vec2 = embed("python me loop kya hota hai")
    assert vec1 == vec2
    assert abs(cosine(vec1, vec2) - 1.0) < 1e-9
    other = embed("quantum entanglement physics")
    assert cosine(vec1, other) < 0.3


def test_plural_stemming_matches_singular():
    assert abs(cosine(embed("loops"), embed("loop")) - 1.0) < 1e-9


def test_rag_chunk_scores_buried_paragraph_in_long_block():
    repo, svc, factory = _service(FakeProvider())
    long_filler = " ".join(f"filler paragraph {i} about unrelated things"
                            for i in range(40))
    _seed_theory(
        factory, "python", "Python loops",
        f"{long_filler}\n\nLoop ek kaam baar baar karne ke liye hota hai. "
        "For loop list ke har item par chalta hai.")
    result = svc.ask("user-1", "python me loop kya hota hai")
    assert result.source == "rag"
    assert result.llm_called is False
    assert "loop" in result.answer.lower()


def test_exact_db_hit_never_calls_llm():
    repo, svc, factory = _service(FakeProvider())
    _seed_approved(factory, "Python me loop kya hai",
                   "Loop ek kaam baar baar karne ke liye hota hai.")
    result = svc.ask("user-1", "Python me loop kya hai")
    assert result.source == "db"
    assert result.confidence == 1.0
    assert result.validated is True
    assert result.llm_called is False
    assert svc._provider.calls == []


def test_similar_db_hit_never_calls_llm():
    repo, svc, factory = _service(FakeProvider())
    _seed_approved(factory, "Python me for loop kaise kaam karta hai",
                   "For loop list ke har item par ek baar chalta hai.")
    result = svc.ask("user-1", "for loop Python me kaise kaam karta hai")
    assert result.source == "db"
    assert result.llm_called is False
    assert svc._provider.calls == []


def test_rag_answers_from_own_theory_without_llm():
    repo, svc, factory = _service(FakeProvider())
    _seed_theory(
        factory, "python", "Python loop",
        "Python me loop ek kaam baar baar karne ke liye use hota hai. "
        "For loop list ke har item par chalta hai.")
    result = svc.ask("user-1", "python me loop kya hota hai")
    assert result.source == "rag"
    assert result.validated is True
    assert result.llm_called is False
    assert result.citations and result.citations[0].topic_slug == "python"
    assert "loop" in result.answer.lower()
    assert svc._provider.calls == []


def test_unvalidated_llm_answer_never_served_until_approved():
    repo, svc, factory = _service(FakeProvider("recursion ka fake jawab"))
    first = svc.ask("user-1", "recursion kya hota hai")
    assert first.source == "llm"
    assert first.validated is False
    assert first.llm_called is True
    assert first.answer_id is not None
    assert len(svc.list_pending()) == 1

    # Same question, no LLM available: must NOT serve the pending answer.
    no_key = AiAnswerServiceImpl(repo, NullProvider())
    second = no_key.ask("user-1", "recursion kya hota hai")
    assert second.source == "fallback"
    assert "recursion ka fake jawab" not in second.answer

    # After admin approval the same question IS a DB hit — still no LLM.
    svc.approve(first.answer_id, "admin-1")
    third = no_key.ask("user-1", "recursion kya hota hai")
    assert third.source == "db"
    assert third.answer == "recursion ka fake jawab"
    assert third.validated is True


def test_reject_never_served_and_cannot_be_approved():
    repo, svc, factory = _service(FakeProvider("galat jawab"))
    first = svc.ask("user-1", "xyz abc concept kya hai")
    assert first.source == "llm"
    svc.reject(first.answer_id, "admin-1")
    with pytest.raises(DomainError):
        svc.approve(first.answer_id, "admin-1")
    no_key = AiAnswerServiceImpl(repo, NullProvider())
    assert no_key.ask("user-1", "xyz abc concept kya hai").source == "fallback"


def test_miss_without_key_degrades_gracefully():
    repo, svc, factory = _service(NullProvider())
    result = svc.ask("user-1", "quantum entanglement kya hota hai")
    assert result.source == "fallback"
    assert result.llm_called is False
    assert result.llm_configured is False
    # Honest about the miss — no invented answer.
    assert "nahi mila" in result.answer


def test_empty_question_rejected():
    repo, svc, factory = _service(NullProvider())
    with pytest.raises(DomainError):
        svc.ask("user-1", "   ")


# ---- API wiring ----
# NOTE: sibling agents run the full suite concurrently against the shared
# /tmp test DB (conftest deletes + recreates it), which makes that DB
# unreliable mid-run ("readonly database"). These API tests therefore build
# an app instance wired to an isolated in-memory DB (StaticPool so the
# TestClient request thread shares the same connection).

def _isolated_client() -> TestClient:
    from sqlalchemy.pool import StaticPool

    import app.core.database as dbmod
    import app.main as mainmod

    eng = create_engine("sqlite:///:memory:",
                        connect_args={"check_same_thread": False},
                        poolclass=StaticPool)
    Base.metadata.create_all(eng)
    factory = sessionmaker(bind=eng)
    orig_db, orig_main = dbmod.SessionLocal, mainmod.SessionLocal
    dbmod.SessionLocal = factory
    mainmod.SessionLocal = factory
    try:
        app = create_app()
    finally:
        dbmod.SessionLocal = orig_db
        mainmod.SessionLocal = orig_main
    return TestClient(app)


def _authz(client: TestClient) -> dict:
    email = f"ai-{uuid.uuid4().hex[:8]}@x.com"
    r = client.post("/api/v1/auth/register",
                    json={"email": email, "password": "password123"})
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_ai_doubt_requires_auth():
    c = _isolated_client()
    r = c.post("/api/v1/ai/doubt", json={"question": "loop kya hai"})
    assert r.status_code == 401


def test_ai_doubt_fallback_without_key_and_status():
    c = _isolated_client()
    h = _authz(c)
    r = c.post("/api/v1/ai/doubt",
               json={"question": "quantum entanglement kya hota hai"},
               headers=h)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["source"] == "fallback"
    assert body["llm_called"] is False
    assert body["llm_configured"] is False

    r = c.get("/api/v1/ai/status", headers=h)
    assert r.status_code == 200
    assert r.json()["db_first"] is True
    assert r.json()["llm_configured"] is False


def test_ai_pending_requires_admin():
    c = _isolated_client()
    h = _authz(c)
    assert c.get("/api/v1/ai/pending", headers=h).status_code == 403
