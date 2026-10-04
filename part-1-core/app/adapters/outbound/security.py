"""Outbound adapters: password hashing, JWT issuance, refresh-token storage."""
from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from typing import Callable

import bcrypt
import jwt
from sqlalchemy.orm import Session

from app.adapters.outbound.models import RefreshTokenModel
from app.domain.user import DomainError, User


class BcryptPasswordHasher:
    def hash(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify(self, password: str, password_hash: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode(), password_hash.encode())
        except Exception:
            return False


class JwtTokenIssuer:
    def __init__(self, secret: str, access_minutes: int = 30, refresh_days: int = 7) -> None:
        self._secret = secret
        self._access_delta = timedelta(minutes=access_minutes)
        self._refresh_delta = timedelta(days=refresh_days)

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def issue_access(self, user: User) -> str:
        payload = {"sub": user.id, "role": user.role, "type": "access",
                   "jti": uuid.uuid4().hex,
                   "exp": self._now() + self._access_delta}
        return jwt.encode(payload, self._secret, algorithm="HS256")

    def issue_refresh(self, user: User) -> str:
        payload = {"sub": user.id, "type": "refresh",
                   "jti": uuid.uuid4().hex,
                   "exp": self._now() + self._refresh_delta}
        return jwt.encode(payload, self._secret, algorithm="HS256")

    def decode(self, token: str) -> dict:
        try:
            return jwt.decode(token, self._secret, algorithms=["HS256"])
        except jwt.PyJWTError as exc:
            raise DomainError("invalid or expired token") from exc


class DbTokenStore:
    """Refresh tokens live in the DB as hashes — the raw token never persists."""

    def __init__(self, session_factory: Callable[[], Session], refresh_days: int = 7) -> None:
        self._sessions = session_factory
        self._refresh_delta = timedelta(days=refresh_days)

    @staticmethod
    def _hash(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    def store(self, token: str, user_id: str, expires_at: object = None) -> None:
        exp = expires_at or (datetime.now(timezone.utc) + self._refresh_delta)
        with self._sessions() as s:
            s.add(RefreshTokenModel(token_hash=self._hash(token), user_id=user_id,
                                    expires_at=exp, revoked=False))
            s.commit()

    def revoke(self, token: str) -> None:
        with self._sessions() as s:
            m = s.get(RefreshTokenModel, self._hash(token))
            if m:
                m.revoked = True
                s.commit()

    def is_revoked(self, token: str) -> bool:
        with self._sessions() as s:
            m = s.get(RefreshTokenModel, self._hash(token))
            return m is None or m.revoked

    def owner_of(self, token: str) -> str | None:
        with self._sessions() as s:
            m = s.get(RefreshTokenModel, self._hash(token))
            if not m or m.revoked:
                return None
            return m.user_id

    def revoke_all_for_user(self, user_id: str) -> None:
        with self._sessions() as s:
            s.query(RefreshTokenModel).filter_by(user_id=user_id).update({"revoked": True})
            s.commit()
