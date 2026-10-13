"""Outbound adapter: global search repository (SQLAlchemy).

One query per content type, always scoped to the requesting user —
like Apple Notes never surfacing another person's locked notes,
a user only ever searches their own content.
"""
from __future__ import annotations

from typing import Callable

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.adapters.outbound.models import (
    AssessmentModel,
    CertificateModel,
    EvidenceModel,
    RoadmapModel,
    RoadmapTaskModel,
)


def _escape_like(term: str) -> str:
    return term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def _like(col, term: str):
    return col.ilike(f"%{_escape_like(term)}%", escape="\\")


class SqlAlchemySearchRepository:
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._sessions = session_factory

    def _clauses(self, cols, terms):
        return [or_(*(_like(c, t) for c in cols)) for t in terms]

    def search(self, user_id: str, terms: list[str],
               types: tuple[str, ...]) -> list[dict]:
        """Raw candidates: [{type, id, title, body, created_at}]."""
        out: list[dict] = []
        with self._sessions() as s:
            if "roadmap" in types:
                cols = [RoadmapModel.title]
                q = (
                    s.query(RoadmapModel)
                    .filter(RoadmapModel.user_id == user_id)
                    .filter(or_(*self._clauses(cols, terms)))
                )
                for m in q.all():
                    out.append({
                        "type": "roadmap", "id": m.id,
                        "title": m.title, "body": f"{m.title} · v{m.version} · {m.source}",
                        "created_at": m.created_at,
                    })
            if "task" in types:
                cols = [
                    RoadmapTaskModel.title, RoadmapTaskModel.description,
                    RoadmapTaskModel.why_it_matters, RoadmapTaskModel.target_skills,
                    RoadmapTaskModel.expected_evidence,
                    RoadmapTaskModel.acceptance_criteria,
                ]
                q = (
                    s.query(RoadmapTaskModel)
                    .join(RoadmapModel,
                          RoadmapTaskModel.roadmap_id == RoadmapModel.id)
                    .filter(RoadmapModel.user_id == user_id)
                    .filter(or_(*self._clauses(cols, terms)))
                )
                for m in q.all():
                    out.append({
                        "type": "task", "id": m.task_key,
                        "title": m.title,
                        "body": " ".join([
                            m.description, m.why_it_matters,
                            m.target_skills, m.expected_evidence,
                            m.acceptance_criteria, m.status, m.priority,
                        ]),
                        "created_at": m.created_at,
                    })
            if "evidence" in types:
                cols = [EvidenceModel.content, EvidenceModel.feedback,
                        EvidenceModel.kind]
                q = (
                    s.query(EvidenceModel)
                    .filter(EvidenceModel.user_id == user_id)
                    .filter(or_(*self._clauses(cols, terms)))
                )
                for m in q.all():
                    out.append({
                        "type": "evidence", "id": m.id,
                        "title": f"{m.kind} evidence · {m.task_key}",
                        "body": f"{m.content} {m.feedback}",
                        "created_at": m.created_at,
                    })
            if "assessment" in types:
                cols = [AssessmentModel.topic, AssessmentModel.level,
                        AssessmentModel.gaps]
                q = (
                    s.query(AssessmentModel)
                    .filter(AssessmentModel.user_id == user_id)
                    .filter(or_(*self._clauses(cols, terms)))
                )
                for m in q.all():
                    out.append({
                        "type": "assessment", "id": m.id,
                        "title": f"{m.topic} · {m.level}",
                        "body": f"{m.topic} {m.level} {m.status} gaps: {m.gaps}",
                        "created_at": m.created_at,
                    })
            if "certificate" in types:
                cols = [CertificateModel.title, CertificateModel.detail,
                        CertificateModel.kind]
                q = (
                    s.query(CertificateModel)
                    .filter(CertificateModel.user_id == user_id)
                    .filter(or_(*self._clauses(cols, terms)))
                )
                for m in q.all():
                    out.append({
                        "type": "certificate", "id": m.id,
                        "title": m.title,
                        "body": f"{m.kind} {m.detail} {m.ref_id}",
                        "created_at": m.created_at,
                    })
        return out
