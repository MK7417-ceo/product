"""Service tests: onboarding orchestration with fake outbound ports."""
import pytest

from app.adapters.inbound.onboarding_service import OnboardingServiceImpl
from app.adapters.outbound.question_bank import StaticQuestionBank
from app.domain.user import DomainError


class FakeProfiles:
    def __init__(self):
        self.by_user = {}

    def save(self, p):
        self.by_user[p.user_id] = p

    def get_by_user(self, uid):
        return self.by_user.get(uid)


class FakePlacements:
    def __init__(self):
        self.by_id = {}

    def save(self, p):
        self.by_id[p.id] = p

    def get(self, pid):
        return self.by_id.get(pid)


@pytest.fixture()
def svc():
    return OnboardingServiceImpl(FakeProfiles(), FakePlacements(), StaticQuestionBank())


def _profile_fields(**over):
    base = dict(education="B.Tech", experience_years=2, current_skills=["python"],
                target_role="AI Engineer", target_domain="AI/ML",
                target_level="intermediate", tech_focus=["python"])
    base.update(over)
    return base


def test_save_and_get_profile(svc):
    p = svc.save_profile("u1", **_profile_fields())
    assert p.target_level == "intermediate"
    assert svc.get_profile("u1").id == p.id


def test_save_profile_twice_replaces(svc):
    p1 = svc.save_profile("u1", **_profile_fields())
    p2 = svc.save_profile("u1", **_profile_fields(target_level="advanced"))
    assert p1.id == p2.id
    assert svc.get_profile("u1").target_level == "advanced"


def test_get_missing_profile(svc):
    with pytest.raises(DomainError, match="profile not found"):
        svc.get_profile("ghost")


def test_start_placement_returns_public_questions(svc):
    session, questions = svc.start_placement("u1", "python", "beginner")
    assert len(questions) == 4
    assert all("answer_index" not in q for q in questions)
    assert session.status == "open"


def test_start_placement_unknown_topic(svc):
    with pytest.raises(DomainError, match="unknown topic"):
        svc.start_placement("u1", "cobol", "beginner")


def test_submit_all_correct_verifies_claim(svc):
    bank = StaticQuestionBank()
    session, _ = svc.start_placement("u1", "python", "intermediate")
    answers = {q.id: q.answer_index for q in
               [bank.get(qid) for qid in session.question_ids]}
    done = svc.submit_placement("u1", session.id, answers)
    assert done.status == "completed"
    assert done.verified_level == "intermediate"
    assert done.correct == 4


def test_submit_all_wrong_steps_down(svc):
    bank = StaticQuestionBank()
    session, _ = svc.start_placement("u1", "python", "advanced")
    answers = {qid: 99 for qid in session.question_ids}  # nothing matches
    done = svc.submit_placement("u1", session.id, answers)
    assert done.verified_level == "beginner"


def test_double_submit_rejected(svc):
    session, _ = svc.start_placement("u1", "python", "beginner")
    svc.submit_placement("u1", session.id, {})
    with pytest.raises(DomainError, match="already completed"):
        svc.submit_placement("u1", session.id, {})


def test_other_users_session_rejected(svc):
    session, _ = svc.start_placement("u1", "python", "beginner")
    with pytest.raises(DomainError, match="not found"):
        svc.submit_placement("u2", session.id, {})
