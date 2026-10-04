"""Service tests: assessment orchestration with fakes."""
import pytest

from app.adapters.inbound.assessment_service import AssessmentServiceImpl
from app.adapters.outbound.question_bank import StaticQuestionBank
from app.domain.user import DomainError


class FakeAssessments:
    def __init__(self):
        self.by_id = {}

    def save(self, a):
        self.by_id[a.id] = a

    def get(self, aid):
        return self.by_id.get(aid)

    def list_for_user(self, uid):
        return [a for a in self.by_id.values() if a.user_id == uid]


@pytest.fixture()
def svc():
    return AssessmentServiceImpl(FakeAssessments(), StaticQuestionBank())


def test_start_returns_public_questions(svc):
    s, qs = svc.start_assessment("u1", "python", "beginner", count=4)
    assert len(qs) == 4
    assert all("answer_index" not in q for q in qs)
    assert s.status == "open" and s.total == 4


def test_start_unknown_topic(svc):
    with pytest.raises(DomainError, match="unknown topic"):
        svc.start_assessment("u1", "cobol", "beginner")


def test_start_missing_level(svc):
    with pytest.raises(DomainError, match="no advanced questions"):
        svc.start_assessment("u1", "ml-basics", "advanced")


def test_submit_scores_and_gaps(svc):
    bank = StaticQuestionBank()
    s, _ = svc.start_assessment("u1", "python", "beginner", count=4)
    # answer first question right, rest wrong
    first = bank.get(s.question_ids[0])
    answers = {qid: (bank.get(qid).answer_index if qid == first.id else 99)
               for qid in s.question_ids}
    r = svc.submit_assessment("u1", s.id, answers)
    assert r.correct == 1 and r.total == 4
    assert r.gaps  # mostly-wrong skills flagged
    stored = svc.get_assessment("u1", s.id)
    assert stored.status == "completed"


def test_double_submit_rejected(svc):
    s, _ = svc.start_assessment("u1", "python", "beginner", count=2)
    svc.submit_assessment("u1", s.id, {})
    with pytest.raises(DomainError, match="already submitted"):
        svc.submit_assessment("u1", s.id, {})


def test_other_user_rejected(svc):
    s, _ = svc.start_assessment("u1", "python", "beginner", count=2)
    with pytest.raises(DomainError, match="not found"):
        svc.get_assessment("u2", s.id)
