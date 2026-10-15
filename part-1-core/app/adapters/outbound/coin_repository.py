"""Outbound adapter: coin wallet persistence."""
from __future__ import annotations

import uuid

from app.adapters.outbound.models import CoinTransactionModel, UserCoinModel
from app.domain.coins import CoinBalance


class SqlAlchemyCoinRepository:
    def __init__(self, session_factory) -> None:
        self._sessions = session_factory

    def get(self, user_id: str) -> CoinBalance:
        with self._sessions() as s:
            row = s.get(UserCoinModel, user_id)
            if row is None:
                return CoinBalance(user_id=user_id, balance=0, lifetime_earned=0)
            return CoinBalance(user_id=user_id, balance=row.balance,
                               lifetime_earned=row.lifetime_earned)

    def apply(self, user_id: str, amount: int, reason: str) -> CoinBalance:
        """Apply a signed amount (+earn/-spend) and ledger it. Returns balance."""
        with self._sessions() as s:
            row = s.get(UserCoinModel, user_id)
            if row is None:
                row = UserCoinModel(user_id=user_id, balance=0, lifetime_earned=0)
                s.add(row)
            row.balance += amount
            if amount > 0:
                row.lifetime_earned += amount
            s.add(CoinTransactionModel(
                id=uuid.uuid4().hex[:36].ljust(36, "0")[:36],
                user_id=user_id, amount=amount, reason=reason))
            s.commit()
            return CoinBalance(user_id=user_id, balance=row.balance,
                               lifetime_earned=row.lifetime_earned)

    def history(self, user_id: str, limit: int = 50) -> list[dict]:
        with self._sessions() as s:
            rows = (s.query(CoinTransactionModel)
                    .filter_by(user_id=user_id)
                    .order_by(CoinTransactionModel.created_at.desc())
                    .limit(limit).all())
            return [{"amount": r.amount, "reason": r.reason,
                     "created_at": r.created_at.isoformat() if r.created_at else None}
                    for r in rows]
