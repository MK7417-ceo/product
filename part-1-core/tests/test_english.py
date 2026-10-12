"""P3e tests: English track — deterministic daily set + scoring."""
import uuid

import pytest
from fastapi.testclient import TestClient

from app.domain import english as eng
from app.domain.user import DomainError
from app.main import create_app


def test_daily_deterministic_and_mixed_kinds():
    a = eng.daily_set("u1", "2026-10-12")
    b = eng.daily_set("u1", "2026-10-12")
    assert [q["id"] for q in a] == [q["id"] for q in b]
    assert len(a) == 5
    kinds = {q["kind"] for q in a}
    assert kinds == {"vocabulary", "grammar", "comprehension"}
    assert all("answer_index" not in q for q in a)


def test_daily_differs_by_day_and_user():
    a = [q["id"] for q in eng.daily_set("u1", "2026-10-12")]
    assert [q["id"] for q in eng.daily_set("u1", "2026-10-13")] != a
    assert [q["id"] for q in eng.daily_set("u2", "2026-10-12")] != a


def test_score_all_correct_and_rejects_unknown():
    qs = eng.daily_set("u1", "2026-10-12")
    by_id = {q.id: q for q in eng.BANK}
    answers = {q["id"]: by_id[q["id"]].answer_index for q in qs}
    assert eng.score("u1", "2026-10-12", answers) == (5, 5)
    with pytest.raises(DomainError):
        eng.score("u1", "2026-10-12", {"ghost": 0})


def test_bank_valid():
    assert len(eng.BANK) >= 15
    for q in eng.BANK:
        assert q.kind in ("vocabulary", "grammar", "comprehension")
        assert 0 <= q.answer_index < len(q.choices)
        if q.kind == "comprehension":
            assert q.passage


def _client():
    return TestClient(create_app())


def _authz(c: TestClient) -> dict:
    email = f"en-{uuid.uuid4().hex[:8]}@x.com"
    r = c.post("/api/v1/auth/register",
               json={"email": email, "password": "password123"})
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_english_api():
    c = _client()
    h = _authz(c)

    r = c.get("/api/v1/english/daily", headers=h)
    assert r.status_code == 200, r.text
    day = r.json()
    assert len(day["questions"]) == 5

    # all wrong on purpose
    rs = c.post("/api/v1/english/daily/submit", headers=h,
                json={"answers": {q["id"]: 999 % len(q["choices"]) for q in day["questions"]}})
    assert rs.status_code == 200
    assert rs.json()["total"] == 5

    assert c.get("/api/v1/english/daily").status_code == 401
    assert c.post("/api/v1/english/daily/submit",
                  json={"answers": {}}).status_code == 401
