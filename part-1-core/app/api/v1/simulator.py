"""Placement Simulator API — 6 rounds, cutoffs, cooldown, reports."""
from __future__ import annotations

import html

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from app.api.v1.auth import _domain_error, current_user_id
from app.domain.user import DomainError

router = APIRouter(tags=["simulator"])


def _svc(request: Request):
    return request.app.state.simulator_service


class StartRequest(BaseModel):
    company: str = "general"


class SubmitRequest(BaseModel):
    answers: dict = {}


@router.post("/simulator/start")
def start_simulator(body: StartRequest, request: Request,
                    user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).start(user_id, body.company)
    except DomainError as exc:
        msg = str(exc)
        if msg.startswith("cooldown:"):
            return JSONResponse(status_code=429, content={"error": msg})
        raise _domain_error(exc)


@router.get("/simulator/mine")
def my_simulators(request: Request,
                  user_id: str = Depends(current_user_id)):
    return _svc(request).my_attempts(user_id)


@router.get("/simulator/attempt/{attempt_id}/round/{round_number}")
def get_round(attempt_id: str, round_number: int, request: Request,
              user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).get_round(user_id, attempt_id, round_number)
    except DomainError as exc:
        raise _domain_error(exc)


@router.post("/simulator/attempt/{attempt_id}/round/{round_number}/submit")
def submit_round(attempt_id: str, round_number: int, body: SubmitRequest,
                 request: Request,
                 user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).submit_round(
            user_id, attempt_id, round_number, body.answers)
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/simulator/attempt/{attempt_id}/report")
def attempt_report(attempt_id: str, request: Request,
                   user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).report(user_id, attempt_id)
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/simulator/attempt/{attempt_id}/certificate",
            response_class=HTMLResponse)
def attempt_certificate(attempt_id: str, request: Request,
                        user_id: str = Depends(current_user_id)):
    """Printable HTML certificate for a passed simulator attempt."""
    try:
        rep = _svc(request).report(user_id, attempt_id)
    except DomainError as exc:
        raise _domain_error(exc)
    if not rep.get("placed"):
        raise _domain_error(DomainError("certificate available only for placed attempts"))
    name = html.escape(str(rep.get("user_name") or rep.get("email") or "Candidate"))
    company = html.escape(str(rep.get("company") or "General"))
    score = html.escape(str(rep.get("score", "")))
    date = html.escape(str(rep.get("completed_at", "")))
    page = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>Placement Certificate — SkillForge</title>
<style>
body{{font-family:Georgia,serif;background:#0f172a;color:#e8ecf4;display:flex;
align-items:center;justify-content:center;min-height:100vh;margin:0}}
.cert{{border:3px solid #E85D26;border-radius:16px;padding:48px 64px;text-align:center;
max-width:560px;background:#1e1b4b}}
.cert h1{{color:#F5EFE6;margin:0 0 8px;font-size:32px}}
.cert .name{{font-size:28px;margin:24px 0 8px;color:#fff}}
.cert .meta{{color:#9aa6bb;margin:6px 0}}
@media print{{body{{background:#fff;color:#000}}.cert{{background:#fff;border-color:#333}}}}
</style></head><body>
<div class="cert">
<h1>🏆 Placement Ready</h1>
<p class="meta">SkillForge Placement Simulator</p>
<p class="meta">This certifies that</p>
<div class="name">{name}</div>
<p class="meta">cleared all 6 rounds ({company}) with score {score}</p>
<p class="meta">{date}</p>
</div></body></html>"""
    return HTMLResponse(content=page)
