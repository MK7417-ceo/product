"""Outbound adapter: evidence repository (SQLAlchemy). Append-only."""
from __future__ import annotations

from typing import Callable

from sqlalchemy.orm import Session

from app.adapters.outbound.models import EvidenceModel
from app.domain.evidence import Evidence


def _to_domain(m: EvidenceModel) -> Evidence:
    return Evidence(
        id=m.id, user_id=m.user_id, roadmap_id=m.roadmap_id,
        task_key=m.task_key, kind=m.kind, content=m.content,
        feedback=m.feedback, created_at=m.created_at,
    )


class SqlAlchemyEvidenceRepository:
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._sessions = session_factory

    def save(self, evidence: Evidence) -> None:
        with self._sessions() as s:
            s.add(EvidenceModel(
                id=evidence.id, user_id=evidence.user_id,
                roadmap_id=evidence.roadmap_id, task_key=evidence.task_key,
                kind=evidence.kind, content=evidence.content,
                feedback=evidence.feedback, created_at=evidence.created_at,
            ))
            s.commit()

    def count_for_user(self, user_id: str) -> int:
        with self._sessions() as s:
            return s.query(EvidenceModel).filter_by(user_id=user_id).count()

    def list_for_task(self, user_id: str, task_key: str) -> list[Evidence]:
        with self._sessions() as s:
            rows = (
                s.query(EvidenceModel)
                .filter_by(user_id=user_id, task_key=task_key)
                .order_by(EvidenceModel.created_at)
                .all()
            )
            return [_to_domain(m) for m in rows]
