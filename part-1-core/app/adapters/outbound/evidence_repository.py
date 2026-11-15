"""Outbound adapter: append-only evidence with mutable review metadata."""
from __future__ import annotations

from typing import Callable

from sqlalchemy.orm import Session

from app.adapters.outbound.models import EvidenceModel, RoadmapModel, RoadmapTaskModel
from app.domain.evidence import Evidence


def _to_domain(m: EvidenceModel) -> Evidence:
    return Evidence(
        id=m.id, user_id=m.user_id, roadmap_id=m.roadmap_id,
        task_key=m.task_key, kind=m.kind, content=m.content,
        feedback=m.feedback, created_at=m.created_at,
        status=m.status, reviewed_by=m.reviewed_by,
        reviewed_at=m.reviewed_at, review_note=m.review_note,
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
                status=evidence.status, reviewed_by=evidence.reviewed_by,
                reviewed_at=evidence.reviewed_at, review_note=evidence.review_note,
            ))
            s.commit()

    def get_by_id(self, evidence_id: str) -> Evidence | None:
        with self._sessions() as s:
            row = s.get(EvidenceModel, evidence_id)
            return _to_domain(row) if row else None

    def update_review(self, evidence: Evidence, complete_task: bool = False) -> bool:
        """Persist the review and optional task completion in one DB transaction."""
        with self._sessions() as s:
            row = s.get(EvidenceModel, evidence.id)
            if not row or row.status != "pending_review":
                return False
            task = None
            if complete_task:
                # Complete only the task in the exact roadmap version that
                # owns this evidence. Never let stale evidence complete a
                # same-key task in a newer roadmap.
                task = (
                    s.query(RoadmapTaskModel)
                    .filter_by(
                        roadmap_id=evidence.roadmap_id,
                        task_key=evidence.task_key,
                    )
                    .first()
                )
                if not task or task.status not in ("in_progress", "completed"):
                    return False
                if task.status == "in_progress":
                    task.status = "completed"
            row.status = evidence.status
            row.reviewed_by = evidence.reviewed_by
            row.reviewed_at = evidence.reviewed_at
            row.review_note = evidence.review_note
            s.commit()
            return True

    def list_pending(self) -> list[Evidence]:
        with self._sessions() as s:
            rows = (
                s.query(EvidenceModel)
                .filter_by(status="pending_review")
                .order_by(EvidenceModel.created_at.asc())
                .limit(500)
                .all()
            )
            return [_to_domain(row) for row in rows]

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
