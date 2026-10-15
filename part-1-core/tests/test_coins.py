"""Coin system tests — domain rules, service earn/spend, API."""
import pytest

from app.domain.coins import (
    BENEFITS,
    benefit_cost,
    can_afford,
    milestone_bonus,
    streak_day_bonus,
)


# ---- domain ----
def test_streak_day_bonus_base():
    assert streak_day_bonus(1) == 2
    assert streak_day_bonus(6) == 2


def test_streak_day_bonus_multiplier():
    assert streak_day_bonus(7) == 5
    assert streak_day_bonus(30) == 5


def test_milestone_bonus():
    assert milestone_bonus(7) == 30
    assert milestone_bonus(30) == 100
    assert milestone_bonus(100) == 300
    assert milestone_bonus(365) == 1000
    assert milestone_bonus(5) == 0


def test_benefit_cost():
    assert benefit_cost("streak_freeze") == 50
    assert benefit_cost("hint_pack") == 5
    with pytest.raises(ValueError):
        benefit_cost("nope")


def test_can_afford():
    assert can_afford(50, "streak_freeze")
    assert not can_afford(49, "streak_freeze")


def test_all_benefits_have_cost_and_name():
    for slug, info in BENEFITS.items():
        assert info["cost"] > 0
        assert info["name"]


# ---- service (in-memory fake repo) ----
class FakeRepo:
    def __init__(self):
        self.bal = 0
        self.earned = 0
        self.ledger = []

    def get(self, user_id):
        from app.domain.coins import CoinBalance
        return CoinBalance(user_id, self.bal, self.earned)

    def apply(self, user_id, amount, reason):
        from app.domain.coins import CoinBalance
        self.bal += amount
        if amount > 0:
            self.earned += amount
        self.ledger.append((amount, reason))
        return CoinBalance(user_id, self.bal, self.earned)

    def history(self, user_id, limit=50):
        return []


@pytest.fixture()
def svc():
    from app.adapters.inbound.coin_service import CoinServiceImpl
    return CoinServiceImpl(FakeRepo())


def test_earn_daily_task(svc):
    r = svc.earn("u1", "daily_task")
    assert r["earned"] == 5
    assert r["balance"] == 5


def test_earn_unknown_event(svc):
    with pytest.raises(ValueError):
        svc.earn("u1", "bogus")


def test_spend_ok(svc):
    svc.earn("u1", "daily_task")  # +5
    r = svc.spend("u1", "hint_pack")  # -5
    assert r["balance"] == 0
    assert r["spent"] == 5


def test_spend_insufficient(svc):
    from app.adapters.inbound.coin_service import InsufficientCoinsError
    with pytest.raises(InsufficientCoinsError):
        svc.spend("u1", "streak_freeze")


def test_spend_unknown_benefit(svc):
    with pytest.raises(ValueError):
        svc.spend("u1", "bogus")


def test_earn_milestone(svc):
    r = svc.earn_milestone("u1", 7)
    assert r["earned"] == 30
    assert svc.earn_milestone("u1", 5) is None
