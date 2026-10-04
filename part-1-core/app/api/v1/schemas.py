"""API-layer schemas. Pydantic lives here (inbound adapter), not in the domain."""
from __future__ import annotations

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: str
    email: str
    role: str
    created_at: str


class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RoleRequest(BaseModel):
    role: str


def to_user_response(user) -> UserResponse:
    return UserResponse(
        id=user.id, email=user.email, role=user.role,
        created_at=user.created_at.isoformat(),
    )
