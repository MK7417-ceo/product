"""Inbound adapter (HTTP): practice router — daily questions + aaj ka plan."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel

from app.api.v1.auth import _domain_error, current_user_id
from app.domain.user import DomainError

router = APIRouter(prefix="", tags=["practice"])


class DailySubmitRequest(BaseModel):
    answers: dict[str, int]
    date: str = ""


def _svc(request: Request):
    return request.app.state.practice_service


@router.get("/practice/daily")
def get_daily(request: Request, date: str = Query(default=""),
              user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).daily(user_id, date)
    except DomainError as exc:
        raise _domain_error(exc)


@router.post("/practice/daily/submit")
def submit_daily(body: DailySubmitRequest, request: Request,
                 user_id: str = Depends(current_user_id)):
    try:
        result = _svc(request).submit_daily(user_id, body.date, body.answers)
        request.app.state.streak_service.record_activity(user_id)
        # +2 coins per correct answer
        correct = sum(1 for a in (result.get("results") or [])
                      if isinstance(a, dict) and a.get("correct"))
        if correct:
            request.app.state.coin_service.earn(user_id, "question_solved", correct)
            result["coins_earned"] = correct  # +1 per correct answer
        return result
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/practice/today")
def get_today(request: Request, date: str = Query(default=""),
              user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).today(user_id, date)
    except DomainError as exc:
        raise _domain_error(exc)
