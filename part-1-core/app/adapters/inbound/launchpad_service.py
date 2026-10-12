"""Inbound adapter: implements the LaunchpadService port (P3a: resume + JD)."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from app.domain.certificate import (
    KINDS,
    Certificate,
    check_roadmap_eligible,
    new_verification_code,
)
from app.domain.portfolio import PortfolioData, render_html
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
    def __init__(self, resumes, roadmaps=None, certificates=None,
                 users=None, evidence=None) -> None:
        self._resumes = resumes
        self._roadmaps = roadmaps
        self._certificates = certificates
        self._users = users
        self._evidence = evidence

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

    # ---------- certificates ----------

    def _need(self, name: str):
        repo = {"roadmaps": self._roadmaps, "certificates": self._certificates,
                "users": self._users}[name]
        if repo is None:
            raise DomainError("certificates not configured")
        return repo

    def list_certificates(self, user_id: str) -> list[Certificate]:
        return self._need("certificates").list_for_user(user_id)

    def issue_certificate(self, user_id: str, kind: str, ref_id: str) -> Certificate:
        if kind not in KINDS:
            raise DomainError(f"unknown certificate kind: {kind}")
        if not ref_id or not ref_id.strip():
            raise DomainError("ref_id required")
        certs = self._need("certificates")
        if certs.exists(user_id, kind, ref_id):
            raise DomainError("certificate already issued for this item")

        if kind == "roadmap":
            roadmap = self._need("roadmaps").get_current(user_id)
            if not roadmap or roadmap.id != ref_id:
                raise DomainError("ref_id must be your current roadmap")
            eligible, reason = check_roadmap_eligible(roadmap)
            if not eligible:
                raise DomainError(f"not eligible: {reason}")
            title = KINDS[kind][0].format(ref_title=roadmap.title)
            detail = (f"{len(list(roadmap.tasks))} tasks completed; "
                      f"roadmap v{roadmap.version}")
        else:  # pragma: no cover — future kinds
            raise DomainError(f"kind not implemented: {kind}")

        cert = Certificate(id=uuid.uuid4().hex, user_id=user_id, kind=kind,
                           title=title, ref_id=ref_id,
                           verification_code=new_verification_code(),
                           issued_at=self.now().isoformat(), detail=detail)
        cert.validate()
        certs.save(cert)
        return cert

    # ---------- portfolio ----------

    def get_portfolio(self, user_id: str) -> PortfolioData:
        resume = self.get_resume(user_id)  # raises if none — portfolio needs a resume
        roadmap = None
        if self._roadmaps is not None:
            try:
                roadmap = self._roadmaps.get_current(user_id)
            except Exception:
                roadmap = None
        certs: list[dict] = []
        if self._certificates is not None:
            certs = [{"title": c.title, "issued_at": c.issued_at,
                      "detail": c.detail, "verification_code": c.verification_code}
                     for c in self._certificates.list_for_user(user_id)]
        evidence_count = 0
        if self._evidence is not None:
            try:
                evidence_count = self._evidence.count_for_user(user_id)
            except Exception:
                evidence_count = 0
        tasks = list(roadmap.tasks) if roadmap else []
        done = sum(1 for t in tasks if t.status == "completed")
        data = PortfolioData(
            name=resume.title, summary=resume.summary, skills=resume.skills,
            experience=tuple({"title": e.title, "company": e.company,
                              "bullets": list(e.bullets)} for e in resume.experience),
            projects=tuple({"name": p.name, "description": p.description,
                            "tech": list(p.tech)} for p in resume.projects),
            education=tuple({"degree": e.degree, "school": e.school,
                             "year": e.year} for e in resume.education),
            links=resume.links, certificates=tuple(certs),
            roadmap_title=roadmap.title if roadmap else "",
            roadmap_done=done, roadmap_total=len(tasks),
            evidence_count=evidence_count)
        data.validate()
        return data

    def render_portfolio(self, user_id: str) -> tuple[str, str]:
        """(filename, html)."""
        data = self.get_portfolio(user_id)
        safe = "".join(c if c.isalnum() else "-" for c in data.name.lower())[:40]
        return f"portfolio-{safe or 'me'}.html", render_html(data)

    def verify_certificate(self, code: str) -> dict:
        cert = self._need("certificates").find_by_code(code.strip().upper())
        if not cert:
            return {"valid": False}
        issued_to = None
        if self._users is not None:
            user = self._users.get(cert.user_id)
            issued_to = user.email if user else None
        return {"valid": True, "title": cert.title, "kind": cert.kind,
                "issued_to": issued_to, "issued_at": cert.issued_at,
                "detail": cert.detail}
