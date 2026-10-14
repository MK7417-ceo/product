"""Streak domain — pure logic for daily learning streaks.

A streak counts consecutive calendar days (UTC) with at least one learning
activity (task completed, question answered, code submitted).

Rules:
- first activity ever            -> current=1, longest=1, total=1
- activity on same day as last   -> no change (idempotent)
- activity the day after last    -> current+1, total+1, longest=max
- activity after a gap (>=2 days)-> current=1, total+1, longest unchanged
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class UserStreak:
    """Pure value object — adapter models never leak into the domain."""

    user_id: str
    current_streak: int
    longest_streak: int
    last_activity_date: date | None
    total_days_active: int

    def as_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "current_streak": self.current_streak,
            "longest_streak": self.longest_streak,
            "last_activity_date": (
                self.last_activity_date.isoformat() if self.last_activity_date else None
            ),
            "total_days_active": self.total_days_active,
        }


def apply_activity(streak: UserStreak, today: date) -> UserStreak:
    """Return the updated streak after an activity on `today`. Pure."""
    if today < date(1970, 1, 1):
        raise ValueError("invalid activity date")
    last = streak.last_activity_date
    if last is None:
        return UserStreak(
            user_id=streak.user_id,
            current_streak=1,
            longest_streak=1,
            last_activity_date=today,
            total_days_active=1,
        )
    if today == last:
        return streak  # already counted today — idempotent
    if today < last:
        raise ValueError("activity date is before last activity date")
    gap = (today - last).days
    if gap == 1:
        current = streak.current_streak + 1
    else:
        current = 1  # streak broken
    return UserStreak(
        user_id=streak.user_id,
        current_streak=current,
        longest_streak=max(streak.longest_streak, current),
        last_activity_date=today,
        total_days_active=streak.total_days_active + 1,
    )


# Milestones celebrated in the UI (days -> key).
MILESTONES: dict[int, str] = {
    7: "week",
    30: "month",
    100: "century",
    365: "year",
}


def milestone_for(streak_days: int) -> str | None:
    """Return the milestone key if `streak_days` hits one, else None."""
    return MILESTONES.get(streak_days)
