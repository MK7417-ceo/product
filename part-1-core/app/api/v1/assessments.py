"""Inbound adapter (HTTP): assessment router — sessions, scoring, gap reports."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request, status
from pydantic import BaseModel, Field

from app.api.v1.auth import _domain_error, current_user_id
from app.domain.user import DomainError

router = APIRouter(prefix="", tags=["assessments"])


class AssessmentStartRequest(BaseModel):
    topic: str
    level: str
    count: int = Field(default=6, ge=1, le=20)


class AssessmentSubmitRequest(BaseModel):
    answers: dict[str, int]


def _svc(request: Request):
    return request.app.state.assessment_service


@router.post("/assessments/start", status_code=201)
def start_assessment(body: AssessmentStartRequest, request: Request,
                     user_id: str = Depends(current_user_id)):
    try:
        session, questions = _svc(request).start_assessment(
            user_id, body.topic, body.level, body.count)
        return {"assessment_id": session.id, "topic": session.topic,
                "level": session.level, "total": session.total,
                "questions": questions}
    except DomainError as exc:
        raise _domain_error(exc)


@router.post("/assessments/{assessment_id}/submit")
def submit_assessment(assessment_id: str, body: AssessmentSubmitRequest,
                      request: Request, user_id: str = Depends(current_user_id)):
    try:
        r = _svc(request).submit_assessment(user_id, assessment_id, body.answers)
        return {
            "assessment_id": r.session_id,
            "correct": r.correct, "total": r.total,
            "ratio": round(r.ratio, 3),
            "per_skill": [
                {"skill": s, "correct": c, "total": t}
                for s, c, t in r.per_skill
            ],
            "gaps": list(r.gaps),
        }
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/assessments/{assessment_id}")
def get_assessment(assessment_id: str, request: Request,
                   user_id: str = Depends(current_user_id)):
    try:
        s = _svc(request).get_assessment(user_id, assessment_id)
        return {"assessment_id": s.id, "topic": s.topic, "level": s.level,
                "status": s.status, "correct": s.correct, "total": s.total}
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/assessments")
def list_assessments(request: Request, user_id: str = Depends(current_user_id)):
    sessions = request.app.state.assessment_repo.list_for_user(user_id)
    return {"assessments": [
        {"assessment_id": s.id, "topic": s.topic, "level": s.level,
         "status": s.status, "correct": s.correct, "total": s.total}
        for s in sessions
    ]}
