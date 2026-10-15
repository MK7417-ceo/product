"""Placement Simulator API — 6 rounds, cutoffs, cooldown, reports."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
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
