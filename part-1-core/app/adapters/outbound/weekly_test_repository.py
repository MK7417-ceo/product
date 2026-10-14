"""Outbound adapter: weekly test persistence (SQLAlchemy)."""
from __future__ import annotations

import json
import uuid
from datetime import date, datetime, timezone

from sqlalchemy import select

from app.adapters.outbound.models import WeeklyTestModel


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class SqlAlchemyWeeklyTestRepository:
    def __init__(self, session_factory) -> None:
        self._factory = session_factory

    def _row_out(self, row: WeeklyTestModel) -> dict:
        return {
            "id": row.id,
            "user_id": row.user_id,
            "domain_slug": row.domain_slug,
            "plan_id": row.plan_id,
            "week_number": row.week_number,
            "scheduled_date": row.scheduled_date.isoformat() if row.scheduled_date else None,
            "status": row.status,
            "score": row.score,
            "total_questions": row.total_questions,
            "question_ids": json.loads(row.question_ids or "[]"),
            "answers": json.loads(row.answers or "{}"),
            "started_at": row.started_at.isoformat() if row.started_at else None,
            "completed_at": row.completed_at.isoformat() if row.completed_at else None,
        }

    def create(self, user_id: str, domain_slug: str, week_number: int,
               scheduled_date: date, plan_id: str | None = None) -> dict:
        with self._factory() as s:
            row = WeeklyTestModel(
                id=uuid.uuid4().hex,
                user_id=user_id,
                domain_slug=domain_slug,
                plan_id=plan_id,
                week_number=week_number,
                scheduled_date=scheduled_date,
                status="scheduled",
                total_questions=20,
                question_ids="[]",
                answers="{}",
            )
            s.add(row)
            s.commit()
            return self._row_out(row)

    def list_for_user(self, user_id: str, limit: int = 50) -> list[dict]:
        with self._factory() as s:
            rows = s.execute(
                select(WeeklyTestModel)
                .where(WeeklyTestModel.user_id == user_id)
                .order_by(WeeklyTestModel.scheduled_date.desc())
                .limit(limit)
            ).scalars().all()
            return [self._row_out(r) for r in rows]

    def get(self, test_id: str) -> dict | None:
        with self._factory() as s:
            row = s.get(WeeklyTestModel, test_id)
            return self._row_out(row) if row else None

    def used_question_ids(self, user_id: str, domain_slug: str) -> set[str]:
        """All question ids already used in this user's tests for the domain."""
        with self._factory() as s:
            rows = s.execute(
                select(WeeklyTestModel.question_ids)
                .where(WeeklyTestModel.user_id == user_id)
                .where(WeeklyTestModel.domain_slug == domain_slug)
            ).all()
            used: set[str] = set()
            for (qids,) in rows:
                used.update(json.loads(qids or "[]"))
            return used

    def start(self, test_id: str, question_ids: list[str]) -> dict | None:
        with self._factory() as s:
            row = s.get(WeeklyTestModel, test_id)
            if row is None:
                return None
            row.status = "active"
            row.question_ids = json.dumps(question_ids)
            row.started_at = _utcnow()
            s.commit()
            return self._row_out(row)

    def submit(self, test_id: str, answers: dict, score: int) -> dict | None:
        with self._factory() as s:
            row = s.get(WeeklyTestModel, test_id)
            if row is None:
                return None
            row.status = "completed"
            row.answers = json.dumps(answers)
            row.score = score
            row.completed_at = _utcnow()
            s.commit()
            return self._row_out(row)

    def mark_missed(self, test_id: str) -> None:
        with self._factory() as s:
            row = s.get(WeeklyTestModel, test_id)
            if row is not None and row.status in ("scheduled", "active"):
                row.status = "missed"
                s.commit()

    def latest_for_plan(self, plan_id: str) -> dict | None:
        with self._factory() as s:
            row = s.execute(
                select(WeeklyTestModel)
                .where(WeeklyTestModel.plan_id == plan_id)
                .order_by(WeeklyTestModel.week_number.desc())
                .limit(1)
            ).scalars().first()
            return self._row_out(row) if row else None
