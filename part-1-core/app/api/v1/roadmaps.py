"""Inbound adapter (HTTP): roadmaps router — generate, view, update, regenerate."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

from app.api.v1.auth import _domain_error, current_user_id
from app.domain.user import DomainError

router = APIRouter(prefix="", tags=["roadmaps"])


class SkillGapIn(BaseModel):
    skill: str = Field(min_length=1, max_length=80)
    mastery_pct: float = Field(ge=0, le=100)


class GenerateRequest(BaseModel):
    gaps: list[SkillGapIn] = Field(min_length=1, max_length=30)
    title: str = Field(default="", max_length=200)


class RegenerateRequest(BaseModel):
    gaps: list[SkillGapIn] = Field(min_length=1, max_length=30)


class TaskStatusRequest(BaseModel):
    status: str


def _svc(request: Request):
    return request.app.state.roadmap_service


def _task_out(t) -> dict:
    return {
        "id": t.id, "title": t.title, "description": t.description,
        "why_it_matters": t.why_it_matters,
        "target_skills": list(t.target_skills),
        "prerequisites": list(t.prerequisites),
        "effort_minutes": t.effort_minutes, "priority": t.priority,
        "expected_evidence": t.expected_evidence,
        "acceptance_criteria": t.acceptance_criteria,
        "status": t.status,
    }


def _roadmap_out(r) -> dict:
    tasks = [_task_out(t) for t in r.tasks]
    return {
        "id": r.id, "version": r.version, "title": r.title, "source": r.source,
        "tasks": tasks,
        "task_counts": {
            "total": len(tasks),
            "pending": sum(1 for t in tasks if t["status"] == "pending"),
            "in_progress": sum(1 for t in tasks if t["status"] == "in_progress"),
            "completed": sum(1 for t in tasks if t["status"] == "completed"),
        },
    }


@router.post("/roadmaps/generate", status_code=201)
def generate(body: GenerateRequest, request: Request,
             user_id: str = Depends(current_user_id)):
    try:
        return _roadmap_out(_svc(request).generate(
            user_id, [g.model_dump() for g in body.gaps], title=body.title))
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/roadmaps/current")
def current(request: Request, user_id: str = Depends(current_user_id)):
    try:
        return _roadmap_out(_svc(request).get_current(user_id))
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/roadmaps")
def versions(request: Request, user_id: str = Depends(current_user_id)):
    roadmaps = _svc(request).list_versions(user_id)
    return [
        {"id": r.id, "version": r.version, "title": r.title,
         "source": r.source, "task_total": len(r.tasks),
         "completed": sum(1 for t in r.tasks if t.status == "completed")}
        for r in roadmaps
    ]


@router.patch("/roadmaps/tasks/{task_id}")
def update_task(task_id: str, body: TaskStatusRequest, request: Request,
                user_id: str = Depends(current_user_id)):
    try:
        return _task_out(_svc(request).update_task(user_id, task_id, body.status))
    except DomainError as exc:
        raise _domain_error(exc)


@router.post("/roadmaps/regenerate", status_code=201)
def regenerate(body: RegenerateRequest, request: Request,
               user_id: str = Depends(current_user_id)):
    try:
        return _roadmap_out(_svc(request).regenerate(
            user_id, [g.model_dump() for g in body.gaps]))
    except DomainError as exc:
        raise _domain_error(exc)
