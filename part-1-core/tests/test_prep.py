"""P3d tests: hiring-prep question bank + API."""
import uuid

import pytest
from fastapi.testclient import TestClient

from app.domain.prep import BANK, LEVELS, TOPICS, PrepQuestion, questions, topics
from app.domain.user import DomainError
from app.main import create_app


def test_bank_valid_and_tagged():
    assert len(BANK) >= 30
    for q in BANK:
        assert q.topic in TOPICS and q.level in LEVELS
        assert q.question.strip() and len(q.guidance) >= 2
    ids = [q.id for q in BANK]
    assert len(ids) == len(set(ids)), "duplicate question ids"


def test_topics_counts_match_bank():
    ts = {t["topic"]: t["count"] for t in topics()}
    assert sum(ts.values()) == len(BANK)
    assert ts["behavioral"] >= 5 and ts["quant"] >= 5


def test_questions_filtering():
    py = questions(topic="python")
    assert py and all(q.topic == "python" for q in py)
    adv = questions(level="advanced")
    assert adv and all(q.level == "advanced" for q in adv)
    both = questions(topic="dsa", level="beginner", count=2)
    assert len(both) == 2
    with pytest.raises(DomainError):
        questions(topic="nope")


def _client():
    return TestClient(create_app())


def _authz(c: TestClient) -> dict:
    email = f"pp-{uuid.uuid4().hex[:8]}@x.com"
    r = c.post("/api/v1/auth/register",
               json={"email": email, "password": "password123"})
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_prep_api():
    c = _client()
    h = _authz(c)

    t = c.get("/api/v1/prep/topics", headers=h)
    assert t.status_code == 200
    assert len(t.json()["topics"]) == len(TOPICS)

    q = c.get("/api/v1/prep/questions?topic=quant&count=3", headers=h)
    assert q.status_code == 200, q.text
    qs = q.json()["questions"]
    assert len(qs) == 3
    assert all(x["topic"] == "quant" for x in qs)
    assert all(x["guidance"] for x in qs)

    bad = c.get("/api/v1/prep/questions?topic=nope", headers=h)
    assert bad.status_code == 400

    assert c.get("/api/v1/prep/topics").status_code == 401
    assert c.get("/api/v1/prep/questions").status_code == 401
