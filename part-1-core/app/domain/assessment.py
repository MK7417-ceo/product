"""Domain: assessment sessions + deterministic scoring + gap report. PURE.

An assessment is a level-matched set of questions on a topic. The client
submits answers only — scores are always computed server-side. A gap is a
skill tag where the user scored below the mastery threshold.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.profile import Question
from app.domain.user import DomainError

MASTERY_THRESHOLD = 0.7


@dataclass
class AssessmentSession:
    id: str
    user_id: str
    topic: str
    level: str
    question_ids: tuple[str, ...]
    answers: dict[str, int] = field(default_factory=dict)
    status: str = "open"  # open | completed
    correct: int = 0
    total: int = 0


@dataclass(frozen=True)
class AssessmentResult:
    session_id: str
    correct: int
    total: int
    ratio: float
    per_skill: tuple[tuple[str, int, int], ...]  # (skill, correct, total)
    gaps: tuple[str, ...]  # skill tags below mastery


def score_assessment(questions: list[Question], answers: dict[str, int]) -> AssessmentResult:
    correct = sum(1 for q in questions if answers.get(q.id) == q.answer_index)
    total = len(questions)
    by_skill: dict[str, list[int]] = {}
    for q in questions:
        hit = 1 if answers.get(q.id) == q.answer_index else 0
        by_skill.setdefault(q.skill or q.topic, [0, 0])
        by_skill[q.skill or q.topic][0] += hit
        by_skill[q.skill or q.topic][1] += 1
    per_skill = tuple(
        (skill, c, t) for skill, (c, t) in sorted(by_skill.items())
    )
    gaps = tuple(
        skill for skill, c, t in per_skill if t and (c / t) < MASTERY_THRESHOLD
    )
    return AssessmentResult(
        session_id="",
        correct=correct,
        total=total,
        ratio=(correct / total) if total else 0.0,
        per_skill=per_skill,
        gaps=gaps,
    )


def validate_assessment(questions: list[Question]) -> None:
    if not questions:
        raise DomainError("no questions available for this topic/level")
