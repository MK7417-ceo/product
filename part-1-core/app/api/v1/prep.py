"""Inbound adapter (HTTP): hiring-prep router — curated Q&A bank."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request

from app.api.v1.auth import _domain_error, current_user_id
from app.domain.prep import questions as bank_questions
from app.domain.prep import topics as bank_topics
from app.domain.user import DomainError

router = APIRouter(prefix="", tags=["prep"])


def _out(q) -> dict:
    return {"id": q.id, "topic": q.topic, "level": q.level,
            "question": q.question, "guidance": list(q.guidance),
            "tags": list(q.tags)}


@router.get("/prep/topics")
def get_topics(request: Request, user_id: str = Depends(current_user_id)):
    return {"topics": bank_topics()}


@router.get("/prep/questions")
def get_questions(request: Request,
                  topic: str = Query(default=""),
                  level: str = Query(default=""),
                  count: int = Query(default=10, ge=1, le=50),
                  user_id: str = Depends(current_user_id)):
    try:
        return {"questions": [_out(q) for q in bank_questions(topic, level, count)]}
    except DomainError as exc:
        raise _domain_error(exc)
