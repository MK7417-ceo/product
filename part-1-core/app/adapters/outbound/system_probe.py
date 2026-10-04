"""Outbound adapter: DatabaseProbe backed by SQLAlchemy."""
from __future__ import annotations

from typing import Callable

from sqlalchemy import text
from sqlalchemy.orm import Session


class SqlAlchemyDatabaseProbe:
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._session_factory = session_factory

    def check(self) -> tuple[bool, str]:
        try:
            with self._session_factory() as session:
                session.execute(text("SELECT 1"))
            return True, "reachable"
        except Exception as exc:  # never raise through the port
            return False, str(exc)[:200]
