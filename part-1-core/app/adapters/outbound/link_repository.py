"""Outbound adapter: AccountLinkRepository backed by SQLAlchemy."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable

from sqlalchemy.orm import Session

from app.adapters.outbound.models import AccountLinkModel
from app.domain.billing import AccountLinks


class SqlAlchemyAccountLinkRepository:
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._sessions = session_factory

    def upsert(self, links: AccountLinks) -> None:
        now = datetime.now(timezone.utc)
        with self._sessions() as s:
            row = s.query(AccountLinkModel).filter_by(user_id=links.user_id).one_or_none()
            if row:
                row.github, row.linkedin, row.leetcode = (
                    links.github, links.linkedin, links.leetcode)
                row.updated_at = now
            else:
                s.add(AccountLinkModel(user_id=links.user_id, github=links.github,
                                       linkedin=links.linkedin, leetcode=links.leetcode,
                                       updated_at=now))
            s.commit()

    def get_by_user(self, user_id: str) -> AccountLinks | None:
        with self._sessions() as s:
            row = s.query(AccountLinkModel).filter_by(user_id=user_id).one_or_none()
            return (AccountLinks(user_id=row.user_id, github=row.github,
                                 linkedin=row.linkedin, leetcode=row.leetcode)
                    if row else None)
