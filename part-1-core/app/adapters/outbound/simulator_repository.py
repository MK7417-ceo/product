"""Outbound adapter: Placement Simulator persistence."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from app.adapters.outbound.models import (
    SimulatorAttemptModel,
    SimulatorRoundModel,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _attempt_out(a: SimulatorAttemptModel) -> dict:
    return {
        "id": a.id,
        "user_id": a.user_id,
        "company": a.company,
        "status": a.status,
        "current_round": a.current_round,
        "final_score": a.final_score,
        "coins_earned": a.coins_earned,
        "started_at": a.started_at.isoformat() if a.started_at else None,
        "completed_at": a.completed_at.isoformat() if a.completed_at else None,
    }


def _round_out(r: SimulatorRoundModel) -> dict:
    return {
        "id": r.id,
        "attempt_id": r.attempt_id,
        "round_number": r.round_number,
        "round_name": r.round_name,
        "score": r.score,
        "total": r.total,
        "passed": r.passed,
        "question_ids": json.loads(r.question_ids or "[]"),
        "answers": json.loads(r.answers or "{}"),
        "started_at": r.started_at.isoformat() if r.started_at else None,
        "completed_at": r.completed_at.isoformat() if r.completed_at else None,
    }


class SqlAlchemySimulatorRepository:
    """CRUD for simulator attempts and rounds."""

    def __init__(self, session_factory) -> None:
        self._sf = session_factory

    # ---- attempts ----

    def create_attempt(self, user_id: str, company: str) -> dict:
        with self._sf() as s:
            a = SimulatorAttemptModel(
                id=uuid.uuid4().hex, user_id=user_id, company=company,
                status="in_progress", current_round=1)
            s.add(a)
            s.commit()
            return _attempt_out(a)

    def get_attempt(self, attempt_id: str) -> dict | None:
        with self._sf() as s:
            a = s.get(SimulatorAttemptModel, attempt_id)
            return _attempt_out(a) if a else None

    def latest_attempt(self, user_id: str) -> dict | None:
        with self._sf() as s:
            a = (s.query(SimulatorAttemptModel)
                 .filter_by(user_id=user_id)
                 .order_by(SimulatorAttemptModel.started_at.desc())
                 .first())
            return _attempt_out(a) if a else None

    def list_attempts(self, user_id: str, limit: int = 20) -> list[dict]:
        with self._sf() as s:
            rows = (s.query(SimulatorAttemptModel)
                    .filter_by(user_id=user_id)
                    .order_by(SimulatorAttemptModel.started_at.desc())
                    .limit(limit).all())
            return [_attempt_out(r) for r in rows]

    def update_attempt(self, attempt_id: str, **fields) -> dict | None:
        with self._sf() as s:
            a = s.get(SimulatorAttemptModel, attempt_id)
            if not a:
                return None
            for k, v in fields.items():
                setattr(a, k, v)
            s.commit()
            return _attempt_out(a)

    # ---- rounds ----

    def create_round(self, attempt_id: str, round_number: int,
                     round_name: str, question_ids: list[str],
                     total: int) -> dict:
        with self._sf() as s:
            r = SimulatorRoundModel(
                id=uuid.uuid4().hex, attempt_id=attempt_id,
                round_number=round_number, round_name=round_name,
                question_ids=json.dumps(question_ids), total=total)
            s.add(r)
            s.commit()
            return _round_out(r)

    def get_round(self, attempt_id: str, round_number: int) -> dict | None:
        with self._sf() as s:
            r = (s.query(SimulatorRoundModel)
                 .filter_by(attempt_id=attempt_id, round_number=round_number)
                 .order_by(SimulatorRoundModel.started_at.desc())
                 .first())
            return _round_out(r) if r else None

    def list_rounds(self, attempt_id: str) -> list[dict]:
        with self._sf() as s:
            rows = (s.query(SimulatorRoundModel)
                    .filter_by(attempt_id=attempt_id)
                    .order_by(SimulatorRoundModel.round_number).all())
            return [_round_out(r) for r in rows]

    def submit_round(self, round_id: str, answers: dict,
                     score: int, passed: bool) -> dict | None:
        with self._sf() as s:
            r = s.get(SimulatorRoundModel, round_id)
            if not r:
                return None
            r.answers = json.dumps(answers)
            r.score = score
            r.passed = passed
            r.completed_at = _utcnow()
            s.commit()
            return _round_out(r)
