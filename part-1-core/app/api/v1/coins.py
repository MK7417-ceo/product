"""Coin API — wallet balance, history, shop benefits, spending."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from app.adapters.inbound.coin_service import InsufficientCoinsError
from app.api.v1.auth import current_user_id

router = APIRouter(tags=["coins"])


def _svc(request: Request):
    return request.app.state.coin_service


class SpendRequest(BaseModel):
    benefit: str


@router.get("/coins/mine")
def my_coins(request: Request, user_id: str = Depends(current_user_id)):
    return _svc(request).get_balance(user_id)


@router.get("/coins/history")
def coin_history(request: Request, user_id: str = Depends(current_user_id)):
    return _svc(request).history(user_id)


@router.get("/coins/benefits")
def coin_benefits(request: Request):
    return _svc(request).benefits()


@router.post("/coins/spend")
def spend_coins(body: SpendRequest, request: Request,
                user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).spend(user_id, body.benefit)
    except ValueError as exc:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(exc))
    except InsufficientCoinsError as exc:
        from fastapi import HTTPException
        raise HTTPException(status_code=402, detail=str(exc))
