"""Inbound adapter: implements the AssessmentService port."""
from __future__ import annotations

import uuid
from dataclasses import replace

from app.domain.assessment import (
    AssessmentSession,
    score_assessment,
    validate_assessment,
)
from app.domain.profile import public_question, validate_level
from app.domain.user import DomainError


class AssessmentServiceImpl:
    def __init__(self, assessments, bank) -> None:
        self._assessments = assessments
        self._bank = bank

    def start_assessment(self, user_id: str, topic: str, level: str,
                         count: int = 6) -> tuple[AssessmentSession, list[dict]]:
        validate_level(level)
        if topic not in self._bank.topics():
            raise DomainError(f"unknown topic: {topic}")
        if level not in self._bank.levels(topic):
            raise DomainError(f"no {level} questions for topic {topic}")
        questions = self._bank.questions(topic, level, count)
        validate_assessment(questions)
        session = AssessmentSession(
            id=uuid.uuid4().hex, user_id=user_id, topic=topic, level=level,
            question_ids=tuple(q.id for q in questions),
            total=len(questions),
        )
        self._assessments.save(session)
        return session, [public_question(q) for q in questions]

    def submit_assessment(self, user_id: str, assessment_id: str,
                          answers: dict[str, int]):
        session = self._assessments.get(assessment_id)
        if not session or session.user_id != user_id:
            raise DomainError("assessment session not found")
        if session.status != "open":
            raise DomainError("assessment already submitted")
        questions = [q for qid in session.question_ids
                     if (q := self._bank.get(qid)) is not None]
        result = score_assessment(questions, answers)
        session.answers = dict(answers)
        session.status = "completed"
        session.correct = result.correct
        session.total = result.total
        self._assessments.save(session)
        return replace(result, session_id=session.id)

    def get_assessment(self, user_id: str, assessment_id: str) -> AssessmentSession:
        session = self._assessments.get(assessment_id)
        if not session or session.user_id != user_id:
            raise DomainError("assessment session not found")
        return session
