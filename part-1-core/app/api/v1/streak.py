"""Streak API — read-only for the client; writes happen via activity hooks."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from app.api.v1.auth import current_user_id

router = APIRouter(tags=["streak"])


def _svc(request: Request):
    return request.app.state.streak_service


@router.get("/streak/mine")
def my_streak(request: Request, user_id: str = Depends(current_user_id)):
    return _svc(request).get_streak(user_id)
