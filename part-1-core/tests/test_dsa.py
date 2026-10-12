"""Tests: Daily DSA — deterministic pick, hidden-test secrecy, grading."""
import uuid
from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from app.adapters.inbound.dsa_service import DSAServiceImpl
from app.adapters.outbound.dsa_bank import BANK
from app.domain.dsa import (
    DSAQuestion,
    Example,
    HiddenTest,
    grade_dsa,
    parse_day,
    pick_for_date,
    public_dsa,
)
from app.domain.user import DomainError
from app.main import create_app


def test_bank_valid_and_unique():
    ids = [q.id for q in BANK]
    assert len(ids) == len(set(ids)) == 14
    assert {q.difficulty for q in BANK} == {"easy", "medium", "hard"}
    for q in BANK:
        assert len(q.hidden_tests) >= 3
        assert q.examples


def test_pick_deterministic_and_rotates():
    d = date(2026, 10, 13)
    assert pick_for_date(BANK, d) is pick_for_date(BANK, d)
    assert pick_for_date(BANK, d).id != pick_for_date(BANK, date(2026, 10, 14)).id
    seen = {
        pick_for_date(BANK, date(2026, 1, 1) + timedelta(days=i)).id
        for i in range(14)
    }
    assert len(seen) == 14  # full rotation over 14 days


def test_public_hides_hidden_tests():
    pub = public_dsa(BANK[0])
    assert "hidden_tests" not in pub
    assert "HiddenTest" not in str(pub)
    assert pub["hidden_test_count"] == len(BANK[0].hidden_tests)
    assert pub["starter_code"]


def test_parse_day():
    assert parse_day("") == date.today()
    assert parse_day("2026-01-05") == date(2026, 1, 5)
    with pytest.raises(DomainError):
        parse_day("not-a-date")


def _tiny_q():
    return DSAQuestion(
        id="t1", title="T", difficulty="easy", description="d",
        examples=(Example("1", "2"),),
        starter_code="x",
        hidden_tests=(HiddenTest("1", "2"), HiddenTest("3", "4")),
    )


def test_grade_all_pass():
    v = grade_dsa(
        lambda lang, code, s: (True, {"1": "2", "3": "4"}[s], ""),
        _tiny_q(), "python", "code")
    assert v.accepted and (v.passed, v.total) == (2, 2)


def test_grade_wrong_answer_reports_case():
    v = grade_dsa(lambda lang, code, s: (True, "WRONG", ""),
                  _tiny_q(), "python", "code")
    assert v.verdict == "wrong_answer"
    assert v.failed_case["expected"] == "2"
    assert v.failed_case["got"] == "WRONG"


def test_grade_runtime_error():
    v = grade_dsa(lambda lang, code, s: (False, "", "boom"),
                  _tiny_q(), "python", "code")
    assert v.verdict == "runtime_error"
    assert v.failed_case["error"] == "boom"


class FakeRunner:
    def __init__(self, outputs):
        self.outputs = outputs

    def run(self, language, code, stdin, limits, request_id):
        return {"verdict": "ok", "stdout": self.outputs.get(stdin, ""),
                "stderr": "", "exit_code": 0}


def test_service_daily_and_submit():
    q = BANK[0]
    svc = DSAServiceImpl(
        bank=[q],
        code_runner=FakeRunner({t.stdin: t.expected for t in q.hidden_tests}),
    )
    d = svc.daily("2026-10-13")
    assert d["id"] == q.id and d["date"] == "2026-10-13"
    assert "hidden_tests" not in d
    out = svc.submit("2026-10-13", "python", "code")
    assert out["accepted"] and out["passed"] == out["total"] == len(q.hidden_tests)


def test_service_submit_rejects_bad_input():
    svc = DSAServiceImpl(bank=BANK[:1], code_runner=FakeRunner({}))
    with pytest.raises(DomainError):
        svc.submit("", "brainfuck", "code")
    with pytest.raises(DomainError):
        svc.submit("", "python", "   ")


def _authed_client(runner):
    c = TestClient(create_app())
    c.app.state.dsa_service = DSAServiceImpl(code_runner=runner)
    email = f"dsa-{uuid.uuid4().hex[:8]}@x.com"
    r = c.post("/api/v1/auth/register",
               json={"email": email, "password": "password123"})
    assert r.status_code == 201, r.text
    token = r.json()["access_token"]
    return c, {"Authorization": f"Bearer {token}"}


def test_api_daily_needs_auth():
    assert TestClient(create_app()).get("/api/v1/dsa/daily").status_code == 401


def test_api_daily_ok_and_safe():
    c, h = _authed_client(FakeRunner({}))
    r = c.get("/api/v1/dsa/daily", headers=h)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["hidden_test_count"] >= 3
    assert "hidden_tests" not in body
    assert body["date"]


def test_api_submit_accepted_and_wrong():
    q = BANK[3]  # climbing stairs
    good = FakeRunner({t.stdin: t.expected for t in q.hidden_tests})
    c, h = _authed_client(good)
    # force the picked question to be q by pinning the bank
    c.app.state.dsa_service = DSAServiceImpl(bank=[q], code_runner=good)
    day = "2026-10-13"
    r = c.post("/api/v1/dsa/daily/submit",
               json={"date": day, "language": "python", "code": "print(1)"},
               headers=h)
    assert r.status_code == 200, r.text
    assert r.json()["accepted"] is True

    bad = FakeRunner({})
    c.app.state.dsa_service = DSAServiceImpl(bank=[q], code_runner=bad)
    r = c.post("/api/v1/dsa/daily/submit",
               json={"date": day, "language": "python", "code": "print(1)"},
               headers=h)
    assert r.json()["accepted"] is False
    assert r.json()["verdict"] == "wrong_answer"
