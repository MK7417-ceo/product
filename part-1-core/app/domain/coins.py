"""Coin reward system — pure domain logic.

Coins reward learning activity. Earning rules (amounts in coins):
- daily task complete: +5
- streak day bonus: +2 (streak >= 7 -> +5)
- question solved: +1
- coding problem solved: +10
- mock test completed: +20
- streak milestone 7/30/100/365: +30/+100/+300/+1000

Spendable benefits:
- streak_freeze: 100 (protect streak for 1 missed day)
- hint_pack: 10 (hint on a hard question)
- premium_mock: 200 (unlock a premium mock test)
- cert_fast_track: 500 (priority certificate processing)
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


# ---- earning rules: event -> coins ----
EARN_RULES: dict[str, int] = {
    "daily_task": 5,
    "question_solved": 1,
    "coding_solved": 10,
    "mock_completed": 20,
    "simulator_placed": 100,
}

# streak day bonus: base x multiplier
STREAK_DAY_BASE = 2
STREAK_MULTIPLIER_DAYS = 7  # streak >= 7 -> +5 instead of +2
STREAK_DAY_BONUS_LONG = 5

# milestone day -> bonus coins
MILESTONE_BONUS: dict[int, int] = {
    7: 30,
    30: 100,
    100: 300,
    365: 1000,
}

# ---- spendable benefits: benefit -> cost ----
BENEFITS: dict[str, dict] = {
    "streak_freeze": {
        "cost": 50,
        "name": "Streak Freeze",
        "icon": "🧊",
        "description": "Miss one day without losing your streak.",
    },
    "hint_pack": {
        "cost": 5,
        "name": "Hint",
        "icon": "💡",
        "description": "Get a hint on a hard question.",
    },
    "premium_mock": {
        "cost": 80,
        "name": "Premium Mock Test",
        "icon": "📝",
        "description": "Unlock a company-level premium mock test.",
    },
    "cert_fast_track": {
        "cost": 200,
        "name": "Certificate Fast-track",
        "icon": "🏆",
        "description": "Priority processing for your certificate.",
    },
}


@dataclass(frozen=True)
class CoinBalance:
    user_id: str
    balance: int
    lifetime_earned: int

    def as_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "balance": self.balance,
            "lifetime_earned": self.lifetime_earned,
        }


def streak_day_bonus(streak_days: int) -> int:
    """Coins for keeping the streak alive today."""
    if streak_days >= STREAK_MULTIPLIER_DAYS:
        return STREAK_DAY_BONUS_LONG
    return STREAK_DAY_BASE


def milestone_bonus(streak_days: int) -> int:
    """Bonus coins when hitting a streak milestone, else 0."""
    return MILESTONE_BONUS.get(streak_days, 0)


def benefit_cost(benefit: str) -> int:
    """Cost of a benefit; raises ValueError for unknown benefits."""
    info = BENEFITS.get(benefit)
    if info is None:
        raise ValueError(f"unknown benefit: {benefit}")
    return info["cost"]


def can_afford(balance: int, benefit: str) -> bool:
    return balance >= benefit_cost(benefit)
