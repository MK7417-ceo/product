"""Outbound adapter: streak persistence (SQLAlchemy)."""
from __future__ import annotations

from datetime import date

from sqlalchemy import select

from app.adapters.outbound.models import StreakActivityModel, UserStreakModel
from app.domain.streak import UserStreak


class SqlAlchemyStreakRepository:
    def __init__(self, session_factory) -> None:
        self._factory = session_factory

    def get(self, user_id: str) -> UserStreak:
        with self._factory() as s:
            row = s.get(UserStreakModel, user_id)
            if row is None:
                return UserStreak(
                    user_id=user_id,
                    current_streak=0,
                    longest_streak=0,
                    last_activity_date=None,
                    total_days_active=0,
                )
            return UserStreak(
                user_id=row.user_id,
                current_streak=row.current_streak,
                longest_streak=row.longest_streak,
                last_activity_date=row.last_activity_date,
                total_days_active=row.total_days_active,
            )

    def save(self, streak: UserStreak) -> None:
        with self._factory() as s:
            row = s.get(UserStreakModel, streak.user_id)
            if row is None:
                row = UserStreakModel(user_id=streak.user_id)
                s.add(row)
            row.current_streak = streak.current_streak
            row.longest_streak = streak.longest_streak
            row.last_activity_date = streak.last_activity_date
            row.total_days_active = streak.total_days_active
            s.commit()

    def mark_day_active(self, user_id: str, day: date) -> bool:
        """Insert (user_id, day) if absent. Returns True if it was new."""
        with self._factory() as s:
            existing = s.get(StreakActivityModel, (user_id, day))
            if existing is not None:
                return False
            s.add(StreakActivityModel(user_id=user_id, activity_date=day))
            s.commit()
            return True

    def active_days(self, user_id: str, since: date) -> list[date]:
        """Active days on/after `since`, ascending."""
        with self._factory() as s:
            rows = s.execute(
                select(StreakActivityModel.activity_date)
                .where(StreakActivityModel.user_id == user_id)
                .where(StreakActivityModel.activity_date >= since)
                .order_by(StreakActivityModel.activity_date)
            ).scalars().all()
            return list(rows)
