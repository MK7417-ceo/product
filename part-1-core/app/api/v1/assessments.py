"""Inbound adapter (HTTP): assessment router — sessions, scoring, gap reports."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request, status
from pydantic import BaseModel, Field

from app.api.v1.auth import _domain_error, current_user_id
from app.domain.assessment import score_assessment
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
        # REG-1: the detail response must carry the same per_skill/gaps
        # breakdown as the list response. It used to omit both, so the
        # SkillGaps page (which prefers detail over list) computed [] gaps
        # for a user with a genuine gap and showed "No skill gaps found".
        per_skill, gaps = _breakdown(request, s)
        return {"assessment_id": s.id, "topic": s.topic, "level": s.level,
                "status": s.status, "correct": s.correct, "total": s.total,
                "per_skill": per_skill, "gaps": gaps}
    except DomainError as exc:
        raise _domain_error(exc)


def _breakdown(request: Request, s):
    """Recompute per_skill + gaps for a session, exactly as submit does.

    Shared by the list and detail endpoints so they can never disagree.
    Open sessions have no answers yet, so they report an empty breakdown.
    """
    per_skill: list[dict] = []
    gaps: list[str] = []
    bank = getattr(request.app.state, "question_bank", None)
    if s.status == "completed" and bank is not None:
        questions = [q for qid in s.question_ids
                     if (q := bank.get(qid)) is not None]
        if questions:
            r = score_assessment(questions, s.answers or {})
            per_skill = [{"skill": sk, "correct": c, "total": t}
                         for sk, c, t in r.per_skill]
            gaps = list(r.gaps)
    return per_skill, gaps


@router.get("/assessments")
def list_assessments(request: Request, user_id: str = Depends(current_user_id)):
    sessions = request.app.state.assessment_repo.list_for_user(user_id)
    # P0-1: the list response must carry the same per_skill breakdown the
    # submit response has (the frontend iterates it).
    out = []
    for s in sessions:
        per_skill, gaps = _breakdown(request, s)
        out.append({"assessment_id": s.id, "topic": s.topic, "level": s.level,
                    "status": s.status, "correct": s.correct, "total": s.total,
                    "per_skill": per_skill, "gaps": gaps})
    return {"assessments": out}
