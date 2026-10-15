"""Outbound adapter: password reset token persistence (SQLAlchemy)."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select

from app.adapters.outbound.models import PasswordResetModel


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class SqlAlchemyPasswordResetRepository:
    def __init__(self, session_factory) -> None:
        self._factory = session_factory

    def create(self, user_id: str, token_hash: str, expires_at: datetime) -> dict:
        with self._factory() as s:
            row = PasswordResetModel(
                id=uuid.uuid4().hex,
                user_id=user_id,
                token_hash=token_hash,
                expires_at=expires_at,
            )
            s.add(row)
            s.commit()
            return {"id": row.id, "user_id": user_id, "expires_at": expires_at}

    def find_valid(self, token_hash: str) -> dict | None:
        """Return the reset row for a token hash, or None.

        Callers check expiry + used status via the domain functions."""
        with self._factory() as s:
            row = s.execute(
                select(PasswordResetModel).where(
                    PasswordResetModel.token_hash == token_hash)
            ).scalar_one_or_none()
            if not row:
                return None
            return {
                "id": row.id,
                "user_id": row.user_id,
                "token_hash": row.token_hash,
                "expires_at": row.expires_at,
                "used_at": row.used_at,
                "created_at": row.created_at,
            }

    def mark_used(self, reset_id: str) -> None:
        with self._factory() as s:
            row = s.get(PasswordResetModel, reset_id)
            if row and row.used_at is None:
                row.used_at = _utcnow()
                s.commit()

    def count_recent_for_email(self, user_id: str, since: datetime) -> int:
        """How many reset tokens were created for this user since `since`.
        Used for rate limiting."""
        with self._factory() as s:
            return s.query(PasswordResetModel).filter(
                PasswordResetModel.user_id == user_id,
                PasswordResetModel.created_at >= since,
            ).count()
