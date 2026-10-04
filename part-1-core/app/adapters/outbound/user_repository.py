"""Outbound adapter: UserRepository backed by SQLAlchemy."""
from __future__ import annotations

from typing import Callable

from sqlalchemy.orm import Session

from app.adapters.outbound.models import RefreshTokenModel, UserModel
from app.domain.user import User


def _to_domain(m: UserModel) -> User:
    return User(id=m.id, email=m.email, password_hash=m.password_hash, role=m.role, created_at=m.created_at)


class SqlAlchemyUserRepository:
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._sessions = session_factory

    def save(self, user: User) -> None:
        with self._sessions() as s:
            s.add(UserModel(id=user.id, email=user.email, password_hash=user.password_hash,
                            role=user.role, created_at=user.created_at))
            s.commit()

    def find_by_email(self, email: str) -> User | None:
        with self._sessions() as s:
            m = s.query(UserModel).filter_by(email=email).one_or_none()
            return _to_domain(m) if m else None

    def get(self, user_id: str) -> User | None:
        with self._sessions() as s:
            m = s.get(UserModel, user_id)
            return _to_domain(m) if m else None

    def update_role(self, user_id: str, role: str) -> User | None:
        with self._sessions() as s:
            m = s.get(UserModel, user_id)
            if not m:
                return None
            m.role = role
            s.commit()
            return _to_domain(m)

    def delete(self, user_id: str) -> None:
        with self._sessions() as s:
            s.query(RefreshTokenModel).filter_by(user_id=user_id).delete()
            s.query(UserModel).filter_by(id=user_id).delete()
            s.commit()
