"""Inbound adapter: coin business logic.

`earn(user_id, event)` is called by learning hooks (task done, question
solved, streak milestones). `spend(user_id, benefit)` powers the coin shop.
"""
from __future__ import annotations

from app.domain.coins import (
    BENEFITS,
    EARN_RULES,
    CoinBalance,
    benefit_cost,
    milestone_bonus,
    streak_day_bonus,
)


class InsufficientCoinsError(Exception):
    pass


class CoinServiceImpl:
    def __init__(self, repo) -> None:
        self._repo = repo

    # ---- reads ----
    def get_balance(self, user_id: str) -> dict:
        return self._repo.get(user_id).as_dict()

    def history(self, user_id: str, limit: int = 50) -> dict:
        return {"transactions": self._repo.history(user_id, limit)}

    def benefits(self) -> dict:
        return {"benefits": [
            {"slug": slug, **info} for slug, info in BENEFITS.items()
        ]}

    # ---- earning ----
    def earn(self, user_id: str, event: str, qty: int = 1) -> dict:
        """Earn coins for a learning event. Returns updated balance."""
        if event not in EARN_RULES:
            raise ValueError(f"unknown earn event: {event}")
        amount = EARN_RULES[event] * qty
        bal = self._repo.apply(user_id, amount, f"earn:{event}")
        return {**bal.as_dict(), "earned": amount, "event": event}

    def earn_streak_day(self, user_id: str, streak_days: int) -> dict:
        amount = streak_day_bonus(streak_days)
        bal = self._repo.apply(user_id, amount, f"earn:streak_day:{streak_days}")
        return {**bal.as_dict(), "earned": amount}

    def earn_milestone(self, user_id: str, streak_days: int) -> dict | None:
        bonus = milestone_bonus(streak_days)
        if not bonus:
            return None
        bal = self._repo.apply(user_id, bonus, f"earn:milestone:{streak_days}")
        return {**bal.as_dict(), "earned": bonus}

    # ---- spending ----
    def spend(self, user_id: str, benefit: str) -> dict:
        cost = benefit_cost(benefit)  # raises ValueError if unknown
        bal = self._repo.get(user_id)
        if bal.balance < cost:
            raise InsufficientCoinsError(
                f"need {cost} coins, have {bal.balance}")
        updated = self._repo.apply(user_id, -cost, f"spend:{benefit}")
        return {**updated.as_dict(), "spent": cost, "benefit": benefit}
