"""Inbound adapter: streak business logic.

`record_activity(user_id)` is the single hook every learning event calls:
task completion, question answered, code submitted, evidence submitted.
It is idempotent per day and safe to call from multiple endpoints.
"""
from __future__ import annotations

from datetime import date, timedelta

from app.domain.streak import apply_activity, milestone_for


class StreakServiceImpl:
    def __init__(self, repo, today_fn=None) -> None:
        self._repo = repo
        # injectable clock for tests: () -> date
        self._today = today_fn or (lambda: date.today())

    def record_activity(self, user_id: str, when: date | None = None) -> dict:
        """Record one learning activity. Returns the streak summary."""
        today = when or self._today()
        current = self._repo.get(user_id)
        updated = apply_activity(current, today)
        if updated is not current:
            self._repo.save(updated)
            self._repo.mark_day_active(user_id, today)
        return self._summary(updated, today)

    def get_streak(self, user_id: str) -> dict:
        today = self._today()
        return self._summary(self._repo.get(user_id), today)

    def _summary(self, streak, today: date) -> dict:
        recent = self._repo.active_days(user_id=streak.user_id,
                                       since=today - timedelta(days=29))
        recent_set = {d.isoformat() for d in recent}
        return {
            "current_streak": streak.current_streak,
            "longest_streak": streak.longest_streak,
            "total_days_active": streak.total_days_active,
            "last_activity_date": (
                streak.last_activity_date.isoformat()
                if streak.last_activity_date else None
            ),
            "today_done": streak.last_activity_date == today,
            "milestone": milestone_for(streak.current_streak),
            # last 30 days, oldest -> newest, for the calendar widget
            "recent_days": sorted(recent_set),
        }
