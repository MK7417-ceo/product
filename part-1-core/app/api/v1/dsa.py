"""Inbound adapter (HTTP): Daily-DSA router — question of the day + grading."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.api.v1.auth import _domain_error, current_user_id
from app.domain.user import DomainError
from app.ports.outbound import CodeEngineError

router = APIRouter(prefix="", tags=["dsa"])


class DSASubmitRequest(BaseModel):
    date: str = ""
    language: str = "python"
    code: str


def _svc(request: Request):
    return request.app.state.dsa_service


@router.get("/dsa/daily")
def dsa_daily(request: Request, date: str = Query(default=""),
              user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).daily(date)
    except DomainError as exc:
        raise _domain_error(exc)


@router.post("/dsa/daily/submit")
def dsa_submit(body: DSASubmitRequest, request: Request,
               user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).submit(body.date, body.language, body.code)
    except DomainError as exc:
        raise _domain_error(exc)
    except CodeEngineError as exc:
        return JSONResponse(status_code=exc.status,
                            content={"error": exc.code, "message": str(exc)})
