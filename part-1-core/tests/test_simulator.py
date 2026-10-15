"""Tests for the Placement Simulator backend."""
from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.adapters.inbound.simulator_service import SimulatorServiceImpl
from app.domain import simulator as sim
from app.domain.user import DomainError


# ---------------------------------------------------------------- domain ----

def test_round_passed_at_cutoff():
    assert sim.round_passed(12, 20) is True  # exactly 60%


def test_round_passed_below_cutoff():
    assert sim.round_passed(11, 20) is False


def test_round_passed_zero_total():
    assert sim.round_passed(0, 0) is False


def test_next_round_advances():
    assert sim.next_round(1) == 2
    assert sim.next_round(5) == 6


def test_next_round_none_at_end():
    assert sim.next_round(6) is None


def test_can_retry_no_prior():
    assert sim.can_retry(None) is True


def test_can_retry_after_7_days():
    assert sim.can_retry(date.today() - timedelta(days=7)) is True
    assert sim.can_retry(date.today() - timedelta(days=30)) is True


def test_can_retry_blocked_within_7_days():
    assert sim.can_retry(date.today() - timedelta(days=6)) is False
    assert sim.can_retry(date.today()) is False


def test_round_config_unknown_raises():
    with pytest.raises(ValueError):
        sim.round_config(99)


def test_grade_boundaries():
    assert sim.grade_for(0.95) == "S"
    assert sim.grade_for(0.85) == "A"
    assert sim.grade_for(0.75) == "B"
    assert sim.grade_for(0.65) == "C"
    assert sim.grade_for(0.5) == "D"
    assert sim.grade_for(0.2) == "F"


# ------------------------------------------------------------ english bank ----

def test_english_bank_size():
    from app.adapters.outbound.english_bank import ENGLISH_BANK
    assert len(ENGLISH_BANK) >= 100


def test_english_bank_valid():
    from app.adapters.outbound.english_bank import ENGLISH_BANK
    ids = [q.id for q in ENGLISH_BANK]
    assert len(set(ids)) == len(ids)
    for q in ENGLISH_BANK:
        assert 0 <= q.answer_index < len(q.choices), q.id
        assert q.topic == "english"
        assert len(q.choices) == 4


def test_english_bank_categories():
    from app.adapters.outbound.english_bank import ENGLISH_BANK, READING_PASSAGES
    skills = {q.skill for q in ENGLISH_BANK}
    for expected in ("tenses", "articles", "prepositions", "subject-verb",
                     "synonyms", "antonyms", "idioms",
                     "sentence-correction", "error-spotting"):
        assert expected in skills
    assert len(READING_PASSAGES) == 5
    rc = [q for q in ENGLISH_BANK if q.skill.startswith("rc-p")]
    assert len(rc) == 20


# ------------------------------------------------------- service (fake repo) ----

class FakeRepo:
    def __init__(self):
        self.attempts: list[dict] = []
        self.rounds: list[dict] = []
        self._n = 0

    def _next_id(self):
        self._n += 1
        return f"id-{self._n}"

    def create_attempt(self, user_id, company):
        a = {"id": self._next_id(), "user_id": user_id, "company": company,
             "status": "in_progress", "current_round": 1, "final_score": None,
             "coins_earned": 0, "started_at": "2026-10-01T00:00:00+00:00",
             "completed_at": None}
        self.attempts.append(a)
        return dict(a)

    def get_attempt(self, attempt_id):
        for a in self.attempts:
            if a["id"] == attempt_id:
                return dict(a)
        return None

    def latest_attempt(self, user_id):
        mine = [a for a in self.attempts if a["user_id"] == user_id]
        return dict(mine[-1]) if mine else None

    def list_attempts(self, user_id, limit=20):
        return [dict(a) for a in self.attempts if a["user_id"] == user_id][:limit]

    def update_attempt(self, attempt_id, **fields):
        for a in self.attempts:
            if a["id"] == attempt_id:
                a.update(fields)
                return dict(a)
        return None

    def create_round(self, attempt_id, round_number, round_name,
                     question_ids, total):
        r = {"id": self._next_id(), "attempt_id": attempt_id,
             "round_number": round_number, "round_name": round_name,
             "score": None, "total": total, "passed": None,
             "question_ids": list(question_ids), "answers": {},
             "started_at": "2026-10-01T00:00:00+00:00", "completed_at": None}
        self.rounds.append(r)
        return dict(r)

    def get_round(self, attempt_id, round_number):
        for r in self.rounds:
            if r["attempt_id"] == attempt_id and r["round_number"] == round_number:
                return dict(r)
        return None

    def list_rounds(self, attempt_id):
        return [dict(r) for r in self.rounds if r["attempt_id"] == attempt_id]

    def submit_round(self, round_id, answers, score, passed):
        for r in self.rounds:
            if r["id"] == round_id:
                r["answers"] = answers
                r["score"] = score
                r["passed"] = passed
                r["completed_at"] = "2026-10-01T01:00:00+00:00"
                return dict(r)
        return None


class FakeCoins:
    def __init__(self):
        self.earned: list[tuple[str, str]] = []

    def earn(self, user_id, event, qty=1):
        self.earned.append((user_id, event))
        return {"earned": 100, "event": event}


@pytest.fixture()
def svc():
    return SimulatorServiceImpl(FakeRepo(), FakeCoins())


def _correct_answers(svc, user_id, attempt_id, rnd):
    """Build a fully-correct answer map for a served round."""
    from app.adapters.outbound.quant_bank import APTITUDE_QUESTIONS
    from app.adapters.outbound.english_bank import ENGLISH_BANK
    from app.adapters.outbound.question_bank import _BANK
    source = sim.ROUNDS[rnd["round_number"]]["source"]
    answers = {}
    for q in rnd["questions"]:
        qid = q["id"]
        if source == "aptitude":
            expected = next(
                x["answer"] for x in APTITUDE_QUESTIONS if x["id"] == qid)
            answers[qid] = expected
        elif source in ("english", "technical"):
            expected = next(
                x.answer_index for x in (ENGLISH_BANK if source == "english" else _BANK)
                if x.id == qid)
            answers[qid] = expected
        elif source == "coding":
            answers[qid] = {"solved": True}
        else:
            answers[qid] = True
    return answers


def test_start_creates_attempt(svc):
    out = svc.start("u1", "tcs")
    assert out["resumed"] is False
    assert out["attempt"]["status"] == "in_progress"
    assert out["attempt"]["current_round"] == 1


def test_start_resumes_in_progress(svc):
    first = svc.start("u1")["attempt"]
    second = svc.start("u1")
    assert second["resumed"] is True
    assert second["attempt"]["id"] == first["id"]


def test_start_cooldown_blocks(svc):
    repo = svc._repo
    repo.attempts.append({
        "id": "old-1", "user_id": "u9", "company": "tcs",
        "status": "eliminated", "current_round": 2, "final_score": 40,
        "coins_earned": 0,
        "started_at": (date.today() - timedelta(days=2)).isoformat() + "T00:00:00",
        "completed_at": (date.today() - timedelta(days=2)).isoformat() + "T00:00:00",
    })
    with pytest.raises(DomainError, match="cooldown"):
        svc.start("u9")


def test_start_cooldown_expired_allows(svc):
    repo = svc._repo
    repo.attempts.append({
        "id": "old-2", "user_id": "u8", "company": "tcs",
        "status": "eliminated", "current_round": 2, "final_score": 40,
        "coins_earned": 0,
        "started_at": (date.today() - timedelta(days=8)).isoformat() + "T00:00:00",
        "completed_at": (date.today() - timedelta(days=8)).isoformat() + "T00:00:00",
    })
    out = svc.start("u8")
    assert out["resumed"] is False


def test_get_round_questions_no_answers_leaked(svc):
    attempt = svc.start("u1")["attempt"]
    rnd = svc.get_round("u1", attempt["id"], 1)
    assert rnd["round_name"] == "Aptitude"
    assert len(rnd["questions"]) == 20
    for q in rnd["questions"]:
        assert "answer" not in q and "answer_index" not in q


def _play_round(svc, user_id, attempt_id, n):
    """Play one round with all-correct answers; return submit result."""
    rnd = svc.get_round(user_id, attempt_id, n)
    answers = _correct_answers(svc, user_id, attempt_id, rnd)
    return svc.submit_round(user_id, attempt_id, n, answers), rnd


def test_get_round_english_has_passages(svc):
    attempt = svc.start("u1")["attempt"]
    _play_round(svc, "u1", attempt["id"], 1)
    rnd = svc.get_round("u1", attempt["id"], 2)
    assert rnd["round_name"] == "English"
    assert len(rnd["questions"]) == 15
    for q in rnd["questions"]:
        if q["skill"].startswith("rc-p"):
            assert "passage" in q


def test_get_round_coding_problems(svc):
    attempt = svc.start("u1")["attempt"]
    for n in (1, 2, 3):
        _play_round(svc, "u1", attempt["id"], n)
    rnd = svc.get_round("u1", attempt["id"], 4)
    assert rnd["round_name"] == "Coding"
    assert len(rnd["questions"]) == 2
    assert all(q["type"] == "coding" for q in rnd["questions"])
    assert "starter_code" in rnd["questions"][0]


def test_submit_pass_advances(svc):
    attempt = svc.start("u1")["attempt"]
    rnd = svc.get_round("u1", attempt["id"], 1)
    answers = _correct_answers(svc, "u1", attempt["id"], rnd)
    out = svc.submit_round("u1", attempt["id"], 1, answers)
    assert out["passed"] is True
    assert out["score"] == 20
    assert out["next_round"] == 2
    latest = svc._repo.get_attempt(attempt["id"])
    assert latest["current_round"] == 2


def test_submit_fail_eliminates(svc):
    attempt = svc.start("u1")["attempt"]
    svc.get_round("u1", attempt["id"], 1)
    out = svc.submit_round("u1", attempt["id"], 1, {})  # all wrong
    assert out["passed"] is False
    assert out["status"] == "eliminated"
    assert "retry_available_on" in out
    latest = svc._repo.get_attempt(attempt["id"])
    assert latest["status"] == "eliminated"


def test_full_run_to_placed_awards_coins(svc):
    attempt = svc.start("u1", "amazon")["attempt"]
    aid = attempt["id"]
    out = None
    for n in range(1, 7):
        out, _ = _play_round(svc, "u1", aid, n)
        assert out["passed"] is True, f"round {n} failed: {out}"
    assert out["status"] == "placed"
    assert out["coins_earned"] == 100
    assert ("u1", "simulator_placed") in svc._coins.earned


def test_report_contents(svc):
    attempt = svc.start("u1")["attempt"]
    aid = attempt["id"]
    rnd = svc.get_round("u1", aid, 1)
    svc.submit_round("u1", aid, 1, _correct_answers(svc, "u1", aid, rnd))
    rep = svc.report("u1", aid)
    assert rep["attempt"]["id"] == aid
    assert len(rep["rounds"]) == 1
    assert rep["rounds"][0]["percent"] == 100
    assert rep["overall_grade"] == "S"
    assert "Aptitude" in rep["strengths"]


def test_submit_wrong_round_rejected(svc):
    attempt = svc.start("u1")["attempt"]
    with pytest.raises(DomainError, match="not the current round"):
        svc.submit_round("u1", attempt["id"], 2, {})


def test_get_round_other_user_rejected(svc):
    attempt = svc.start("u1")["attempt"]
    with pytest.raises(DomainError, match="attempt not found"):
        svc.get_round("u2", attempt["id"], 1)


def test_my_attempts_history(svc):
    svc.start("u1", "tcs")
    out = svc.my_attempts("u1")
    assert len(out["attempts"]) == 1
    assert out["can_start"] is True  # in_progress doesn't block listing
