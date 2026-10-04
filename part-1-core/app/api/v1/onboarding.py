"""Inbound adapter (HTTP): onboarding router — profiles + placement verification."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

from app.api.v1.auth import _domain_error, current_user_id
from app.domain.user import DomainError

router = APIRouter(prefix="", tags=["onboarding"])


class ProfileRequest(BaseModel):
    education: str
    experience_years: float = Field(ge=0, le=60)
    current_skills: list[str] = Field(min_length=1)
    target_role: str
    target_domain: str
    target_level: str
    tech_focus: list[str] = Field(min_length=1)


class PlacementStartRequest(BaseModel):
    topic: str
    claimed_level: str


class PlacementSubmitRequest(BaseModel):
    answers: dict[str, int]


def _svc(request: Request):
    return request.app.state.onboarding_service


def _profile_out(p) -> dict:
    return {
        "id": p.id, "user_id": p.user_id, "education": p.education,
        "experience_years": p.experience_years,
        "current_skills": list(p.current_skills),
        "target_role": p.target_role, "target_domain": p.target_domain,
        "target_level": p.target_level, "tech_focus": list(p.tech_focus),
        "created_at": p.created_at.isoformat(),
    }


@router.post("/profiles", status_code=201)
def save_profile(body: ProfileRequest, request: Request,
                 user_id: str = Depends(current_user_id)):
    try:
        return _profile_out(_svc(request).save_profile(user_id, **body.model_dump()))
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/profiles/me")
def get_my_profile(request: Request, user_id: str = Depends(current_user_id)):
    try:
        return _profile_out(_svc(request).get_profile(user_id))
    except DomainError as exc:
        raise _domain_error(exc)


@router.post("/placement/start", status_code=201)
def start_placement(body: PlacementStartRequest, request: Request,
                    user_id: str = Depends(current_user_id)):
    try:
        session, questions = _svc(request).start_placement(
            user_id, body.topic, body.claimed_level)
        return {"placement_id": session.id, "topic": session.topic,
                "claimed_level": session.claimed_level, "questions": questions}
    except DomainError as exc:
        raise _domain_error(exc)


@router.post("/placement/{placement_id}/submit")
def submit_placement(placement_id: str, body: PlacementSubmitRequest,
                     request: Request, user_id: str = Depends(current_user_id)):
    try:
        s = _svc(request).submit_placement(user_id, placement_id, body.answers)
        return {
            "placement_id": s.id, "status": s.status,
            "correct": s.correct, "total": s.total,
            "claimed_level": s.claimed_level,
            "verified_level": s.verified_level,
        }
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/placement/topics")
def placement_topics(request: Request, user_id: str = Depends(current_user_id)):
    return {"topics": request.app.state.question_bank.topics()}
