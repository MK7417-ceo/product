"""Inbound adapter (HTTP): study plans router.

POST /study-plans/preview — pure plan generation, no persistence, no auth
    needed for preview (plan is created for the logged-in user on create).
POST /study-plans — persist the plan; 501 until the study_plans table
    (sibling task) is ready.

Auth: preview is public (marketing/onboarding); create requires login.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.api.v1.auth import _domain_error, current_user_id
from app.domain.study_planner import generate_plan, plan_summary
from app.domain.user import DomainError

router = APIRouter(prefix="", tags=["study-plans"])


class StudyPlanRequest(BaseModel):
    domain_slug: str
    start_level: str
    lessons: list = []
    coding: bool = True


def _storage_ready() -> bool:
    """True once the sibling task's study_plans table/model exists."""
    try:
        from app.adapters.outbound import models  # noqa: F401

        return hasattr(models, "StudyPlanModel")
    except ImportError:
        return False


@router.post("/study-plans/preview")
def preview_plan(body: StudyPlanRequest):
    try:
        days = generate_plan(
            body.domain_slug, body.start_level, body.lessons, coding=body.coding
        )
        summary = plan_summary(
            body.domain_slug, body.start_level, body.lessons, coding=body.coding
        )
    except DomainError as exc:
        raise _domain_error(exc)
    return {
        "domain_slug": body.domain_slug,
        "start_level": body.start_level,
        "summary": summary,
        "days": days,
    }


@router.post("/study-plans", status_code=status.HTTP_201_CREATED)
def create_plan(body: StudyPlanRequest, request: Request, user_id: str = Depends(current_user_id)):
    if not _storage_ready():
        return JSONResponse(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            content={
                "detail": "Study-plan storage is not ready yet. "
                "Use /study-plans/preview for generation."
            },
        )
    # Storage-ready path: the sibling task's service persists here.
    # (Deliberately unimplemented in this slice — no fake persistence.)
    return JSONResponse(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        content={"detail": "Study-plan persistence wiring is pending."},
    )
