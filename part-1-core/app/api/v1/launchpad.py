"""Inbound adapter (HTTP): launchpad router — resume + JD matcher (P3a)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.api.v1.auth import _domain_error, current_user_id
from app.domain.user import DomainError

router = APIRouter(prefix="", tags=["launchpad"])


class ResumeRequest(BaseModel):
    title: str = ""
    summary: str = ""
    skills: list[str] = []
    experience: list[dict] = []
    projects: list[dict] = []
    education: list[dict] = []
    links: dict = {}


class JDMatchRequest(BaseModel):
    jd_text: str


def _svc(request: Request):
    return request.app.state.launchpad_service


def _resume_out(resume) -> dict:
    return {
        "id": resume.id, "title": resume.title, "summary": resume.summary,
        "skills": list(resume.skills),
        "experience": [{"title": e.title, "company": e.company, "start": e.start,
                        "end": e.end, "bullets": list(e.bullets)}
                       for e in resume.experience],
        "projects": [{"name": p.name, "description": p.description,
                      "tech": list(p.tech), "link": p.link}
                     for p in resume.projects],
        "education": [{"degree": e.degree, "school": e.school, "year": e.year}
                      for e in resume.education],
        "links": resume.links,
    }


@router.put("/launchpad/resume")
def save_resume(body: ResumeRequest, request: Request,
                user_id: str = Depends(current_user_id)):
    try:
        return _resume_out(_svc(request).save_resume(user_id, body.model_dump()))
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/launchpad/resume")
def get_resume(request: Request, user_id: str = Depends(current_user_id)):
    try:
        return _resume_out(_svc(request).get_resume(user_id))
    except DomainError as exc:
        if "no resume yet" in str(exc):
            return JSONResponse(status_code=404,
                                content={"error": "no_resume", "message": str(exc)})
        raise _domain_error(exc)


@router.post("/launchpad/jd-match")
def jd_match(body: JDMatchRequest, request: Request,
             user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).match_jd(user_id, body.jd_text)
    except DomainError as exc:
        if "no resume yet" in str(exc):
            return JSONResponse(status_code=404,
                                content={"error": "no_resume", "message": str(exc)})
        raise _domain_error(exc)
