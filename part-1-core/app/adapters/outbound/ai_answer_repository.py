"""Outbound adapter: SQLAlchemy storage for AI/RAG answers + theory lookup.

The validated-write gate lives here AND in the service: this repository
only ever returns APPROVED rows from the DB-hit queries (find_exact,
list_approved). Pending LLM answers are retrievable by id / list_pending
for the admin review queue, and are never mixed into the lookup path.
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Callable

from sqlalchemy.orm import Session

from app.adapters.outbound.models import AiAnswerModel, TheoryModel
from app.domain.ai_answer import Answer


def _to_domain(m: AiAnswerModel) -> Answer:
    emb: list[float] = []
    if m.embedding_json:
        try:
            emb = [float(v) for v in json.loads(m.embedding_json)]
        except (ValueError, TypeError):
            emb = []
    return Answer(
        id=m.id, question=m.question,
        normalized_question=m.normalized_question, answer=m.answer,
        source=m.source, status=m.status, topic_slug=m.topic_slug,
        created_by=m.created_by, approved_by=m.approved_by,
        embedding=emb, created_at=m.created_at)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class SqlAlchemyAiAnswerRepository:
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._sessions = session_factory

    # ---- DB-hit path: APPROVED rows only ----
    def find_exact(self, normalized_question: str) -> Answer | None:
        with self._sessions() as s:
            m = s.query(AiAnswerModel).filter_by(
                normalized_question=normalized_question,
                status="approved").one_or_none()
            return _to_domain(m) if m else None

    def list_approved(self) -> list[Answer]:
        with self._sessions() as s:
            return [_to_domain(m) for m in
                    s.query(AiAnswerModel).filter_by(status="approved").all()]

    # ---- write path: LLM answers land as PENDING, never approved ----
    def save_pending(self, question: str, normalized_question: str,
                     answer: str, topic_slug: str, created_by: str,
                     embedding: list[float]) -> Answer:
        with self._sessions() as s:
            m = AiAnswerModel(
                id=uuid.uuid4().hex, question=question,
                normalized_question=normalized_question, answer=answer,
                source="llm", status="pending", topic_slug=topic_slug or "",
                created_by=created_by, approved_by="",
                embedding_json=json.dumps(embedding),
                created_at=_utcnow(), updated_at=_utcnow())
            s.add(m)
            s.commit()
            return _to_domain(m)

    def get(self, answer_id: str) -> Answer | None:
        with self._sessions() as s:
            m = s.get(AiAnswerModel, answer_id)
            return _to_domain(m) if m else None

    def list_pending(self) -> list[Answer]:
        with self._sessions() as s:
            return [_to_domain(m) for m in
                    s.query(AiAnswerModel).filter_by(status="pending")
                    .order_by(AiAnswerModel.created_at).all()]

    def approve(self, answer_id: str, admin_id: str) -> Answer | None:
        """Only a PENDING answer can become approved. Returns None when the
        row is missing or not pending (rejecting silent state changes)."""
        with self._sessions() as s:
            m = s.get(AiAnswerModel, answer_id)
            if not m or m.status != "pending":
                return None
            m.status = "approved"
            m.approved_by = admin_id
            m.updated_at = _utcnow()
            s.commit()
            return _to_domain(m)

    def reject(self, answer_id: str, admin_id: str) -> Answer | None:
        with self._sessions() as s:
            m = s.get(AiAnswerModel, answer_id)
            if not m or m.status != "pending":
                return None
            m.status = "rejected"
            m.approved_by = admin_id
            m.updated_at = _utcnow()
            s.commit()
            return _to_domain(m)

    # ---- RAG source: the app's own curated theory ----
    def list_theory(self) -> list[dict]:
        with self._sessions() as s:
            return [{"topic_slug": m.topic_slug, "title": m.title,
                     "content": m.content}
                    for m in s.query(TheoryModel)
                    .order_by(TheoryModel.topic_slug,
                              TheoryModel.order_index).all()]
