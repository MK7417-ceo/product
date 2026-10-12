"""Inbound adapter: implements the PracticeService port."""
from __future__ import annotations

from datetime import datetime, timezone

from app.domain.practice import daily_questions, score_daily, todays_tasks


def _today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


class PracticeServiceImpl:
    def __init__(self, bank, roadmaps) -> None:
        self._bank = bank
        self._roadmaps = roadmaps

    def daily(self, user_id: str, date: str = "") -> dict:
        d = date or _today_str()
        return {"date": d, "questions": daily_questions(user_id, d, self._bank)}

    def submit_daily(self, user_id: str, date: str, answers: dict[str, int]) -> dict:
        d = date or _today_str()
        correct, total = score_daily(user_id, d, answers, self._bank)
        return {"date": d, "correct": correct, "total": total}

    def today(self, user_id: str, date: str = "") -> dict:
        d = date or _today_str()
        questions = daily_questions(user_id, d, self._bank)
        try:
            roadmap = self._roadmaps.get_current(user_id)
        except Exception:
            roadmap = None  # daily practice must never break on roadmap store issues
        tasks = [
            {"id": t.id, "title": t.title, "status": t.status,
             "effort_minutes": t.effort_minutes, "priority": t.priority}
            for t in todays_tasks(roadmap)
        ]
        return {"date": d, "questions": questions, "tasks": tasks,
                "has_roadmap": roadmap is not None}
