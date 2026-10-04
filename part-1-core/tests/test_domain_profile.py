"""Domain tests: profile rules + placement scoring/verification."""
import pytest

from app.domain.profile import (
    Question,
    public_question,
    score_placement,
    validate_level,
    validate_profile,
    verify_level,
)
from app.domain.user import DomainError


def _fields(**over):
    base = dict(
        education="B.Tech CSE", experience_years=1.5,
        current_skills=["python"], target_role="AI Engineer",
        target_domain="AI/ML", target_level="intermediate",
        tech_focus=["python", "ml"],
    )
    base.update(over)
    return base


def test_validate_profile_ok():
    validate_profile(**_fields())  # must not raise


def test_validate_profile_rejects():
    with pytest.raises(DomainError):
        validate_profile(**_fields(education="  "))
    with pytest.raises(DomainError):
        validate_profile(**_fields(target_level="god"))
    with pytest.raises(DomainError):
        validate_profile(**_fields(current_skills=[]))
    with pytest.raises(DomainError):
        validate_profile(**_fields(experience_years=-1))


def test_validate_level():
    assert validate_level("expert") == "expert"
    with pytest.raises(DomainError):
        validate_level("nope")


def _qs():
    return [
        Question(id="q1", topic="python", level="beginner", prompt="p1",
                 choices=("a", "b"), answer_index=0),
        Question(id="q2", topic="python", level="beginner", prompt="p2",
                 choices=("a", "b"), answer_index=1),
    ]


def test_score_placement():
    correct, total = score_placement(_qs(), {"q1": 0, "q2": 0})
    assert (correct, total) == (1, 2)


def test_public_question_hides_answer():
    pub = public_question(_qs()[0])
    assert "answer_index" not in pub
    assert pub["choices"] == ["a", "b"]


def test_verify_level_steps_down():
    assert verify_level("advanced", 1.0) == "advanced"
    assert verify_level("advanced", 0.7) == "advanced"
    assert verify_level("advanced", 0.5) == "intermediate"
    assert verify_level("advanced", 0.0) == "beginner"
    assert verify_level("beginner", 0.0) == "beginner"  # floor
