"""Outbound adapter: assessment session repository (SQLAlchemy)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Callable

from sqlalchemy.orm import Session

from app.adapters.outbound.models import AssessmentModel
from app.domain.assessment import AssessmentSession


def _to_domain(m: AssessmentModel) -> AssessmentSession:
    return AssessmentSession(
        id=m.id, user_id=m.user_id, topic=m.topic, level=m.level,
        question_ids=tuple(json.loads(m.question_ids)),
        answers=dict(json.loads(m.answers)), status=m.status,
        correct=m.correct, total=m.total,
    )


class SqlAlchemyAssessmentRepository:
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._sessions = session_factory

    def save(self, assessment: AssessmentSession) -> None:
        with self._sessions() as s:
            m = s.get(AssessmentModel, assessment.id)
            payload = dict(
                user_id=assessment.user_id, topic=assessment.topic,
                level=assessment.level,
                question_ids=json.dumps(list(assessment.question_ids)),
                answers=json.dumps(assessment.answers), status=assessment.status,
                correct=assessment.correct, total=assessment.total,
                gaps="[]",
                created_at=datetime.now(timezone.utc),
            )
            if m:
                for k, v in payload.items():
                    if k != "created_at":
                        setattr(m, k, v)
            else:
                s.add(AssessmentModel(id=assessment.id, **payload))
            s.commit()

    def get(self, assessment_id: str) -> AssessmentSession | None:
        with self._sessions() as s:
            m = s.get(AssessmentModel, assessment_id)
            return _to_domain(m) if m else None

    def list_for_user(self, user_id: str) -> list[AssessmentSession]:
        with self._sessions() as s:
            rows = (
                s.query(AssessmentModel)
                .filter_by(user_id=user_id)
                .order_by(AssessmentModel.created_at.desc())
                .all()
            )
            return [_to_domain(m) for m in rows]
