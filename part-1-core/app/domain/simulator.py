"""Placement Simulator domain — pure functions, no I/O.

6 rounds, 60% cutoff each, 7-day retry cooldown after elimination/completion.
"""
from __future__ import annotations

from datetime import date, timedelta

CUTOFF = 0.60
RETRY_DAYS = 7
PLACED_COINS = 100
TOTAL_ROUNDS = 6

# round_number -> config
ROUNDS: dict[int, dict] = {
    1: {"name": "Aptitude", "questions": 20, "minutes": 30, "source": "aptitude"},
    2: {"name": "English", "questions": 15, "minutes": 20, "source": "english"},
    3: {"name": "Technical MCQ", "questions": 20, "minutes": 30, "source": "technical"},
    4: {"name": "Coding", "questions": 2, "minutes": 60, "source": "coding"},
    5: {"name": "Technical Interview", "questions": 5, "minutes": 30, "source": "tech_interview"},
    6: {"name": "HR Interview", "questions": 5, "minutes": 30, "source": "hr_interview"},
}

ATTEMPT_IN_PROGRESS = "in_progress"
ATTEMPT_ELIMINATED = "eliminated"
ATTEMPT_PLACED = "placed"


def round_passed(score: int, total: int) -> bool:
    """True when score meets the 60% cutoff."""
    if total <= 0:
        return False
    return (score / total) >= CUTOFF


def next_round(current: int) -> int | None:
    """Next round number, or None when the simulator is complete."""
    nxt = current + 1
    return nxt if nxt <= TOTAL_ROUNDS else None


def round_config(round_number: int) -> dict:
    """Config for a round; raises ValueError for unknown rounds."""
    cfg = ROUNDS.get(round_number)
    if cfg is None:
        raise ValueError(f"unknown round: {round_number}")
    return cfg


def can_retry(last_end: date | None, today: date | None = None) -> bool:
    """True when the 7-day cooldown has passed (or there is no prior attempt)."""
    if last_end is None:
        return True
    today = today or date.today()
    return (today - last_end).days >= RETRY_DAYS


def retry_available_on(last_end: date) -> date:
    """Date on which a new attempt becomes allowed."""
    return last_end + timedelta(days=RETRY_DAYS)


def grade_for(pct: float) -> str:
    """S/A/B/C/D/F grade for a percentage (0-1)."""
    if pct >= 0.9:
        return "S"
    if pct >= 0.8:
        return "A"
    if pct >= 0.7:
        return "B"
    if pct >= 0.6:
        return "C"
    if pct >= 0.4:
        return "D"
    return "F"
