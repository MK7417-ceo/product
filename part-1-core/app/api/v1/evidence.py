"""Evidence submission and controlled review API."""
from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from app.api.v1.auth import _domain_error, current_user_id, require_admin
from app.domain.user import DomainError

router = APIRouter(prefix="", tags=["evidence"])


class EvidenceSubmitRequest(BaseModel):
    kind: str = Field(description="code | text | url")
    content: str = Field(min_length=1, max_length=20000)


class EvidenceReviewRequest(BaseModel):
    decision: Literal["verified", "rejected", "needs_changes"]
    note: str = Field(default="", max_length=2000)


def _svc(request: Request):
    return request.app.state.evidence_service


def _evidence_out(e) -> dict:
    return {
        "id": e.id, "task_key": e.task_key, "kind": e.kind,
        "content": e.content, "feedback": e.feedback,
        "created_at": e.created_at.isoformat(),
        "status": e.status,
        "reviewed_by": e.reviewed_by,
        "reviewed_at": e.reviewed_at.isoformat() if e.reviewed_at else None,
        "review_note": e.review_note,
    }


@router.post("/roadmaps/tasks/{task_id}/evidence", status_code=201)
def submit_evidence(task_id: str, body: EvidenceSubmitRequest, request: Request,
                    user_id: str = Depends(current_user_id)):
    try:
        return _evidence_out(_svc(request).submit(
            user_id, task_id, body.kind, body.content))
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/roadmaps/tasks/{task_id}/evidence")
def list_evidence(task_id: str, request: Request,
                  user_id: str = Depends(current_user_id)):
    try:
        return [_evidence_out(e) for e in _svc(request).list_for_task(user_id, task_id)]
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/evidence/review-queue")
def review_queue(request: Request, _admin: str = Depends(require_admin)):
    """Global queue is admin-only until organization-scoped reviewer access ships."""
    return [_evidence_out(e) for e in _svc(request).list_pending()]


@router.post("/evidence/{evidence_id}/review")
def review_evidence(evidence_id: str, body: EvidenceReviewRequest, request: Request,
                    reviewer_id: str = Depends(require_admin)):
    try:
        return _evidence_out(_svc(request).review(
            reviewer_id, evidence_id, body.decision, body.note))
    except DomainError as exc:
        raise _domain_error(exc)
