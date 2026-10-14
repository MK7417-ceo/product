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
    assert svc.get_profile("u1").user_id == p.user_id


def test_save_profile_twice_replaces(svc):
    p1 = svc.save_profile("u1", **_profile_fields())
    p2 = svc.save_profile("u1", **_profile_fields(target_level="advanced"))
    assert p1.user_id == p2.user_id
    assert svc.get_profile("u1").target_level == "advanced"


def test_get_missing_profile(svc):
    with pytest.raises(DomainError, match="profile not found"):
        svc.get_profile("ghost")


def test_start_placement_beginner_skips_questions(svc):
    # beginners start from scratch: session completes immediately, no questions
    session, questions = svc.start_placement("u1", "python", "beginner")
    assert questions == []
    assert session.status == "completed"
    assert session.verified_level == "beginner"


def test_start_placement_returns_public_questions(svc):
    session, questions = svc.start_placement("u1", "python", "intermediate")
    assert len(questions) == 8  # intermediate claim -> 2 levels x 4
    assert all("answer_index" not in q for q in questions)
    assert session.status == "open"


def test_start_placement_spread_matches_claim(svc):
    _, questions = svc.start_placement("u1", "python", "advanced")
    assert len(questions) == 12  # 3 levels x 4
    levels = [q["level"] for q in questions]
    assert levels == ["beginner"] * 4 + ["intermediate"] * 4 + ["advanced"] * 4


def test_start_placement_expert_claim_now_works(svc):
    _, questions = svc.start_placement("u1", "python", "expert")
    assert len(questions) == 16  # 4 levels x 4
    assert "expert" in {q["level"] for q in questions}


def test_start_placement_unknown_topic(svc):
    with pytest.raises(DomainError, match="unknown topic"):
        svc.start_placement("u1", "cobol", "beginner")


def test_submit_all_correct_verifies_claim(svc):
    bank = StaticQuestionBank()
    session, _ = svc.start_placement("u1", "python", "intermediate")
    answers = {q.id: q.answer_index for q in
               [bank.get(qid) for qid in session.question_ids]}
    done, analysis = svc.submit_placement("u1", session.id, answers)
    assert done.status == "completed"
    assert done.verified_level == "intermediate"
    assert done.correct == 8
    assert analysis["verified_level"] == "intermediate"
    assert set(analysis["levels"]) == {"beginner", "intermediate"}


def test_submit_all_wrong_steps_down(svc):
    session, _ = svc.start_placement("u1", "python", "advanced")
    answers = {qid: 99 for qid in session.question_ids}  # nothing matches
    done, analysis = svc.submit_placement("u1", session.id, answers)
    assert done.verified_level == "beginner"
    assert "verified level: beginner" in analysis["summary"]


def test_submit_partial_finds_true_level(svc):
    bank = StaticQuestionBank()
    session, _ = svc.start_placement("u1", "python", "advanced")
    answers = {}
    for qid in session.question_ids:
        q = bank.get(qid)
        # ace beginner+intermediate, bomb advanced
        answers[qid] = q.answer_index if q.level != "advanced" else 99
    done, analysis = svc.submit_placement("u1", session.id, answers)
    assert done.verified_level == "intermediate"
    assert analysis["levels"]["advanced"]["correct"] == 0


def test_double_submit_rejected(svc):
    session, _ = svc.start_placement("u1", "python", "intermediate")
    svc.submit_placement("u1", session.id, {})
    with pytest.raises(DomainError, match="already completed"):
        svc.submit_placement("u1", session.id, {})


def test_other_users_session_rejected(svc):
    session, _ = svc.start_placement("u1", "python", "intermediate")
    with pytest.raises(DomainError, match="not found"):
        svc.submit_placement("u2", session.id, {})
