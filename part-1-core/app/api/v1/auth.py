"""Inbound adapter (HTTP): auth router. Calls the AuthService port only.

DomainError -> HTTP mapping lives here, at the edge.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.api.v1.schemas import (
    AuthResponse,
    ForgotPasswordRequest,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    ResetPasswordRequest,
    RoleRequest,
    UserResponse,
    to_user_response,
)
from app.domain.user import DomainError
from app.ports.inbound import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
_bearer = HTTPBearer(auto_error=False)


def _service(request: Request) -> AuthService:
    return request.app.state.auth_service


def _pwd_reset_service(request: Request):
    return request.app.state.password_reset_service


def _issuer(request: Request):
    return request.app.state.token_issuer


def _auth_result(result) -> AuthResponse:
    return AuthResponse(
        user=to_user_response(result.user),
        access_token=result.access_token,
        refresh_token=result.refresh_token,
    )


def _domain_error(exc: DomainError) -> HTTPException:
    msg = str(exc)
    if msg in ("invalid credentials", "invalid or expired token",
               "refresh token revoked", "not a refresh token"):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=msg)
    if msg == "email already registered":
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
    if msg == "user not found":
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)


def current_user_id(
    request: Request,
    creds: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> str:
    if not creds:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing token")
    try:
        claims = _issuer(request).decode(creds.credentials)
    except DomainError as exc:
        raise _domain_error(exc)
    if claims.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not an access token")
    return claims["sub"]


def require_admin(request: Request, user_id: str = Depends(current_user_id)) -> str:
    try:
        user = _service(request).get_user(user_id)
    except DomainError as exc:
        raise _domain_error(exc)
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="admin required")
    return user_id


@router.post("/register", response_model=AuthResponse, status_code=201)
def register(body: RegisterRequest, request: Request):
    try:
        return _auth_result(_service(request).register(body.email, body.password))
    except DomainError as exc:
        raise _domain_error(exc)


@router.post("/login", response_model=AuthResponse)
def login(body: LoginRequest, request: Request):
    try:
        return _auth_result(_service(request).login(body.email, body.password))
    except DomainError as exc:
        raise _domain_error(exc)


@router.post("/refresh", response_model=AuthResponse)
def refresh(body: RefreshRequest, request: Request):
    try:
        return _auth_result(_service(request).refresh(body.refresh_token))
    except DomainError as exc:
        raise _domain_error(exc)


@router.post("/logout", status_code=204)
def logout(body: RefreshRequest, request: Request):
    _service(request).logout(body.refresh_token)
    return None


@router.get("/me", response_model=UserResponse)
def me(request: Request, user_id: str = Depends(current_user_id)):
    try:
        return to_user_response(_service(request).get_user(user_id))
    except DomainError as exc:
        raise _domain_error(exc)


@router.post("/users/{target_id}/role", response_model=UserResponse)
def set_role(target_id: str, body: RoleRequest, request: Request,
             _admin: str = Depends(require_admin)):
    try:
        return to_user_response(_service(request).set_role(target_id, body.role))
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/export")
def export(request: Request, user_id: str = Depends(current_user_id)):
    try:
        return _service(request).export_data(user_id)
    except DomainError as exc:
        raise _domain_error(exc)


@router.delete("/me", status_code=204)
def delete_me(request: Request, user_id: str = Depends(current_user_id)):
    try:
        _service(request).delete_account(user_id)
    except DomainError as exc:
        raise _domain_error(exc)
    return None


@router.post("/forgot-password")
def forgot_password(body: ForgotPasswordRequest, request: Request):
    """Request a password reset link.

    ALWAYS returns 200 — never reveals whether the email has an account.
    Rate limited: max 3 requests per email per hour (429 when exceeded).
    """
    try:
        return _pwd_reset_service(request).forgot_password(body.email)
    except DomainError as exc:
        msg = str(exc)
        if msg.startswith("too many reset requests"):
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                                detail=msg)
        raise _domain_error(exc)


@router.post("/reset-password")
def reset_password(body: ResetPasswordRequest, request: Request):
    """Set a new password from a reset link token."""
    try:
        return _pwd_reset_service(request).reset_password(
            body.token, body.new_password)
    except DomainError as exc:
        raise _domain_error(exc)
