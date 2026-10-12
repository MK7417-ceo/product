"""Inbound adapter: implements the LaunchpadService port (P3a: resume + JD)."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from app.domain.launchpad import (
    Education,
    Experience,
    Project,
    Resume,
    match_jd,
)
from app.domain.user import DomainError


def _resume_from_row(row) -> Resume:
    d = json.loads(row.data)
    return Resume(
        id=row.id, user_id=row.user_id, title=row.title,
        summary=d.get("summary", ""), skills=tuple(d.get("skills", [])),
        experience=tuple(Experience(**e) for e in d.get("experience", [])),
        projects=tuple(Project(**p) for p in d.get("projects", [])),
        education=tuple(Education(**e) for e in d.get("education", [])),
        links=d.get("links", {}))


def _resume_to_data(resume: Resume) -> str:
    return json.dumps({
        "summary": resume.summary, "skills": list(resume.skills),
        "experience": [e.__dict__ | {"bullets": list(e.bullets)}
                       for e in resume.experience],
        "projects": [p.__dict__ | {"tech": list(p.tech)} for p in resume.projects],
        "education": [e.__dict__ for e in resume.education],
        "links": resume.links,
    })


class LaunchpadServiceImpl:
    def __init__(self, resumes) -> None:
        self._resumes = resumes

    def save_resume(self, user_id: str, payload: dict) -> Resume:
        try:
            resume = Resume(
                id=payload.get("id") or uuid.uuid4().hex,
                user_id=user_id,
                title=payload.get("title", ""),
                summary=payload.get("summary", ""),
                skills=tuple(payload.get("skills", [])),
                experience=tuple(Experience(
                    title=e.get("title", ""), company=e.get("company", ""),
                    start=e.get("start", ""), end=e.get("end", ""),
                    bullets=tuple(e.get("bullets", [])))
                    for e in payload.get("experience", [])),
                projects=tuple(Project(
                    name=p.get("name", ""), description=p.get("description", ""),
                    tech=tuple(p.get("tech", [])), link=p.get("link", ""))
                    for p in payload.get("projects", [])),
                education=tuple(Education(
                    degree=e.get("degree", ""), school=e.get("school", ""),
                    year=e.get("year", ""))
                    for e in payload.get("education", [])),
                links=payload.get("links", {}),
            )
        except (TypeError, AttributeError) as exc:
            raise DomainError(f"invalid resume payload: {exc}")
        resume.validate()
        self._resumes.upsert(user_id, resume, _resume_to_data(resume))
        return resume

    def get_resume(self, user_id: str) -> Resume:
        row = self._resumes.get_by_user(user_id)
        if not row:
            raise DomainError("no resume yet — save one first")
        return _resume_from_row(row)

    def match_jd(self, user_id: str, jd_text: str) -> dict:
        resume = self.get_resume(user_id)
        m = match_jd(resume, jd_text)
        return {
            "score": m.score,
            "jd_keyword_count": m.jd_keyword_count,
            "matched": [{"keyword": h.keyword, "jd_count": h.jd_count}
                        for h in m.matched],
            "missing": [{"keyword": h.keyword, "jd_count": h.jd_count}
                        for h in m.missing[:15]],
            "suggestions": list(m.suggestions),
        }

    @staticmethod
    def now():
        return datetime.now(timezone.utc)
