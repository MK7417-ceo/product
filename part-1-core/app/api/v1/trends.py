"""Inbound adapter (HTTP): trend watcher admin API.

Admin only:
  GET  /admin/trends                 — detect new tech trending on GitHub
  POST /admin/trends/{slug}/approve  — approve a candidate -> creates domain + modules

Detection is live (GitHub public search API, no key). Any fetch failure
returns an empty candidate list — never a 500. Approval re-runs detection
and matches by slug; a JSON body may override the suggested details.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from app.api.v1.auth import _domain_error, require_admin
from app.domain.trend_watcher import (
    TechCandidate,
    detect_new_tech,
    suggest_domain,
    suggest_modules,
)
from app.domain.user import DomainError

router = APIRouter(prefix="", tags=["trends"])


class TrendModuleIn(BaseModel):
    slug: str
    name: str
    description: str = ""
    estimated_days: int = 7


class TrendApproveIn(BaseModel):
    name: str | None = None
    description: str | None = None
    icon: str = "🆕"
    category: str = "tech-domain"
    modules: list[TrendModuleIn] | None = None


def _svc(request: Request):
    return request.app.state.curriculum_service


def _known_slugs(request: Request) -> list[str]:
    try:
        return [d["slug"] for d in _svc(request).list_domains()]
    except Exception:
        return []


def _candidate_out(c: TechCandidate) -> dict:
    return {
        "id": c.id, "name": c.name, "category": c.category,
        "reason": c.reason, "stars": c.stars, "repo": c.repo,
        "modules": c.modules,
    }


@router.get("/admin/trends")
def list_trends(request: Request, _admin: str = Depends(require_admin)):
    candidates = detect_new_tech(_known_slugs(request))
    return {"ok": True, "count": len(candidates),
            "candidates": [_candidate_out(c) for c in candidates]}


@router.post("/admin/trends/{slug}/approve", status_code=201)
def approve_trend(slug: str, body: TrendApproveIn | None, request: Request,
                  _admin: str = Depends(require_admin)):
    svc = _svc(request)
    # Re-run detection; match the slug the admin saw.
    matched: TechCandidate | None = None
    for c in detect_new_tech(_known_slugs(request)):
        if c.id == slug:
            matched = c
            break
    if matched is None and body is None:
        return _domain_error("candidate not found — refresh /admin/trends and try again")

    if body and (body.name or body.modules is not None):
        name = (body.name or slug).strip()
        payload = {
            "slug": slug, "name": name,
            "description": body.description or f"{name} — approved from trend watcher",
            "icon": body.icon, "category": body.category,
            "modules": [m.model_dump() for m in (body.modules or [])]
                       or suggest_modules(name),
        }
    elif matched is not None:
        payload = suggest_domain(matched)
    else:
        return _domain_error("candidate not found — refresh /admin/trends and try again")

    try:
        domain = svc.create_domain(
            slug=payload["slug"], name=payload["name"],
            description=payload.get("description", ""),
            icon=payload.get("icon", "🆕"),
            category=payload.get("category", "tech-domain"),
        )
        created_modules = []
        for i, m in enumerate(payload.get("modules", [])):
            try:
                created_modules.append(svc.create_module(
                    domain_slug=payload["slug"], slug=m["slug"], name=m["name"],
                    description=m.get("description", ""), order_index=i,
                    estimated_days=int(m.get("estimated_days", 7))))
            except DomainError:
                continue
        return {"ok": True, "domain": domain, "modules": created_modules}
    except DomainError as exc:
        return _domain_error(str(exc))
