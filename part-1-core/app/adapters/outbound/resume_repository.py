"""Outbound adapter: ResumeRepository backed by SQLAlchemy (upsert)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable

from sqlalchemy.orm import Session

from app.adapters.outbound.models import ResumeModel
from app.domain.launchpad import Resume


class SqlAlchemyResumeRepository:
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._sessions = session_factory

    def upsert(self, user_id: str, resume: Resume, data: str) -> None:
        now = datetime.now(timezone.utc)
        with self._sessions() as s:
            row = s.query(ResumeModel).filter_by(user_id=user_id).one_or_none()
            if row:
                row.title = resume.title
                row.data = data
                row.updated_at = now
            else:
                s.add(ResumeModel(id=resume.id, user_id=user_id,
                                  title=resume.title, data=data,
                                  updated_at=now))
            s.commit()

    def get_by_user(self, user_id: str):
        with self._sessions() as s:
            return s.query(ResumeModel).filter_by(user_id=user_id).one_or_none()
