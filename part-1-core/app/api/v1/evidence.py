"""Inbound adapter (HTTP): evidence router — submit + list proof of work."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request, status
from pydantic import BaseModel, Field

from app.api.v1.auth import _domain_error, current_user_id
from app.domain.user import DomainError

router = APIRouter(prefix="", tags=["evidence"])


class EvidenceSubmitRequest(BaseModel):
    kind: str = Field(description="code | text | url")
    content: str = Field(min_length=1, max_length=20000)


def _svc(request: Request):
    return request.app.state.evidence_service


def _evidence_out(e) -> dict:
    return {
        "id": e.id, "task_key": e.task_key, "kind": e.kind,
        "content": e.content, "feedback": e.feedback,
        "created_at": e.created_at.isoformat(),
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
