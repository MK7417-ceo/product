"""Inbound adapter (HTTP): english router — daily English set + scoring."""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from app.api.v1.auth import _domain_error, current_user_id
from app.domain import english as eng
from app.domain.user import DomainError

router = APIRouter(prefix="", tags=["english"])


class EnglishSubmitRequest(BaseModel):
    answers: dict[str, int]
    date: str = ""


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


@router.get("/english/daily")
def get_daily(request: Request, user_id: str = Depends(current_user_id)):
    try:
        d = _today()
        return {"date": d, "questions": eng.daily_set(user_id, d)}
    except DomainError as exc:
        raise _domain_error(exc)


@router.post("/english/daily/submit")
def submit_daily(body: EnglishSubmitRequest, request: Request,
                 user_id: str = Depends(current_user_id)):
    try:
        d = body.date or _today()
        correct, total = eng.score(user_id, d, body.answers)
        return {"date": d, "correct": correct, "total": total}
    except DomainError as exc:
        raise _domain_error(exc)
