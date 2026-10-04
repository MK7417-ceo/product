"""Inbound adapter (HTTP): Google OAuth endpoints.

Fully implemented, but they return 501 until the operator configures
GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET / GOOGLE_REDIRECT_URI.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, status

from app.api.v1.auth import _auth_result, _domain_error
from app.domain.user import DomainError

router = APIRouter(prefix="/auth/google", tags=["oauth"])


@router.get("/login")
def google_login(request: Request):
    provider = request.app.state.oauth_provider
    if not provider.configured:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="google oauth not configured: set GOOGLE_CLIENT_ID, "
                   "GOOGLE_CLIENT_SECRET and GOOGLE_REDIRECT_URI",
        )
    return {"auth_url": provider.auth_url()}


@router.get("/callback")
def google_callback(code: str, request: Request):
    provider = request.app.state.oauth_provider
    try:
        email = provider.exchange(code)
        return _auth_result(request.app.state.auth_service.register_oauth(email))
    except DomainError as exc:
        if "not configured" in str(exc):
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=str(exc))
        raise _domain_error(exc)
