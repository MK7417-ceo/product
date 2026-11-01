"""Inbound adapter (HTTP): DB-first doubt solver + admin review queue.

Endpoints:
  POST /ai/doubt              — ask a question (auth required)
  GET  /ai/status             — provider/llm-configured status (auth, no secrets)
  GET  /ai/pending            — pending LLM answers awaiting review (admin)
  POST /ai/pending/{id}/approve — approve -> becomes a served DB answer (admin)
  POST /ai/pending/{id}/reject  — reject -> never served (admin)
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from app.api.v1.auth import _domain_error, current_user_id, require_admin
from app.domain.user import DomainError

router = APIRouter(prefix="", tags=["ai"])


def _svc(request: Request):
    return request.app.state.ai_answer_service


class DoubtRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    topic_slug: str = Field(default="", max_length=80)


def _answer_dict(a) -> dict:
    return {
        "id": a.id, "question": a.question, "answer": a.answer,
        "source": a.source, "status": a.status,
        "topic_slug": a.topic_slug, "created_by": a.created_by,
        "approved_by": a.approved_by,
    }


def _ask_dict(r) -> dict:
    return {
        "answer": r.answer, "source": r.source,
        "confidence": r.confidence, "validated": r.validated,
        "llm_called": r.llm_called, "llm_configured": r.llm_configured,
        "answer_id": r.answer_id,
        "citations": [{"topic_slug": c.topic_slug, "title": c.title}
                      for c in r.citations],
    }


@router.post("/ai/doubt")
def ask_doubt(body: DoubtRequest, request: Request,
              user_id: str = Depends(current_user_id)):
    try:
        result = _svc(request).ask(user_id, body.question, body.topic_slug)
    except DomainError as exc:
        raise _domain_error(exc)
    return _ask_dict(result)


@router.get("/ai/status")
def ai_status(request: Request, user_id: str = Depends(current_user_id)):
    svc = _svc(request)
    return {
        "provider": svc.provider_name,
        "llm_configured": svc.llm_configured,
        "db_first": True,
        "note": ("LLM answers are stored as pending and served as DB "
                 "answers only after admin approval."),
    }


@router.get("/ai/pending")
def list_pending(request: Request, _admin: str = Depends(require_admin)):
    return {"pending": [_answer_dict(a) for a in _svc(request).list_pending()]}


@router.post("/ai/pending/{answer_id}/approve")
def approve_pending(answer_id: str, request: Request,
                    admin_id: str = Depends(require_admin)):
    try:
        ans = _svc(request).approve(answer_id, admin_id)
    except DomainError as exc:
        raise _domain_error(exc)
    return _answer_dict(ans)


@router.post("/ai/pending/{answer_id}/reject")
def reject_pending(answer_id: str, request: Request,
                   admin_id: str = Depends(require_admin)):
    try:
        ans = _svc(request).reject(answer_id, admin_id)
    except DomainError as exc:
        raise _domain_error(exc)
    return _answer_dict(ans)
