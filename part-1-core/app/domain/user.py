"""Domain: user identity. PURE — no framework, no DB, no crypto imports.

Crypto/hashing/token details live in outbound adapters; the domain only
declares what it needs and enforces business rules.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone

VALID_ROLES = ("user", "reviewer", "admin")
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class DomainError(Exception):
    """Business-rule violation. Adapters translate these to HTTP codes."""


@dataclass(frozen=True)
class User:
    id: str
    email: str
    password_hash: str
    role: str = "user"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class AuthResult:
    user: User
    access_token: str
    refresh_token: str


def validate_email(email: str) -> str:
    cleaned = email.strip().lower()
    if not _EMAIL_RE.match(cleaned):
        raise DomainError("invalid email address")
    return cleaned


def validate_password(password: str) -> None:
    if len(password) < 8:
        raise DomainError("password must be at least 8 characters")


def validate_role(role: str) -> str:
    if role not in VALID_ROLES:
        raise DomainError(f"unknown role: {role}")
    return role


def new_user(user_id: str, email: str, password_hash: str) -> User:
    """Factory: every new user starts as role 'user'. No other default exists."""
    return User(id=user_id, email=validate_email(email), password_hash=password_hash, role="user")
