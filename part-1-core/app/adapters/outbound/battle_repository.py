"""Outbound adapter: 1v1 battle persistence (SQLAlchemy)."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from sqlalchemy import select

from app.adapters.outbound.models import BattleModel


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class SqlAlchemyBattleRepository:
    def __init__(self, session_factory) -> None:
        self._factory = session_factory

    def _row_out(self, row: BattleModel) -> dict:
        return {
            "id": row.id,
            "topic": row.topic,
            "bracket": row.bracket,
            "level": row.level,
            "question_ids": json.loads(row.question_ids or "[]"),
            "player1_id": row.player1_id,
            "player2_id": row.player2_id,
            "invite_email": row.invite_email,
            "invite_code": row.invite_code,
            "rematch_of": row.rematch_of,
            "status": row.status,
            "window_seconds": row.window_seconds,
            "player1_answers": json.loads(row.player1_answers or "{}"),
            "player2_answers": json.loads(row.player2_answers or "{}"),
            "player1_times": json.loads(row.player1_times or "{}"),
            "player2_times": json.loads(row.player2_times or "{}"),
            "player1_score": row.player1_score,
            "player2_score": row.player2_score,
            "player1_correct": row.player1_correct,
            "player2_correct": row.player2_correct,
            "winner_id": row.winner_id,
            "flagged": row.flagged,
            "flag_reason": row.flag_reason,
            "rewards": json.loads(row.rewards or "{}"),
            "started_at": row.started_at.isoformat() if row.started_at else None,
            "ends_at": row.ends_at.isoformat() if row.ends_at else None,
            "created_at": row.created_at.isoformat() if row.created_at else None,
        }

    def create_waiting(self, player1_id: str, topic: str, bracket: str,
                       level: str, question_ids: list[str],
                       window_seconds: int,
                       rematch_of: str | None = None,
                       battle_id: str | None = None) -> dict:
        with self._factory() as s:
            row = BattleModel(
                id=battle_id or uuid.uuid4().hex, topic=topic, bracket=bracket,
                level=level, question_ids=json.dumps(question_ids),
                player1_id=player1_id, status="waiting",
                window_seconds=window_seconds, rematch_of=rematch_of)
            s.add(row)
            s.commit()
            return self._row_out(row)

    def create_challenge(self, player1_id: str, topic: str, bracket: str,
                         level: str, question_ids: list[str],
                         window_seconds: int, invite_email: str,
                         invite_code: str,
                         battle_id: str | None = None) -> dict:
        with self._factory() as s:
            row = BattleModel(
                id=battle_id or uuid.uuid4().hex, topic=topic, bracket=bracket,
                level=level, question_ids=json.dumps(question_ids),
                player1_id=player1_id, status="challenge",
                window_seconds=window_seconds, invite_email=invite_email,
                invite_code=invite_code)
            s.add(row)
            s.commit()
            return self._row_out(row)

    def get(self, battle_id: str) -> dict | None:
        with self._factory() as s:
            row = s.get(BattleModel, battle_id)
            return self._row_out(row) if row else None

    def get_by_invite_code(self, code: str) -> dict | None:
        with self._factory() as s:
            row = s.execute(
                select(BattleModel).where(BattleModel.invite_code == code)
            ).scalars().first()
            return self._row_out(row) if row else None

    def find_waiting_match(self, topic: str, bracket: str, user_id: str,
                           rematch_of: str | None = None) -> dict | None:
        """A waiting battle the user may join: same topic+bracket, not
        their own. A rematch request prefers the opponent's rematch entry
        for the same original battle."""
        with self._factory() as s:
            q = (select(BattleModel)
                 .where(BattleModel.status == "waiting",
                        BattleModel.topic == topic,
                        BattleModel.bracket == bracket,
                        BattleModel.player1_id != user_id)
                 .order_by(BattleModel.created_at))
            if rematch_of:
                q = q.where(BattleModel.rematch_of == rematch_of)
            row = s.execute(q).scalars().first()
            return self._row_out(row) if row else None

    def user_open_battle(self, user_id: str) -> dict | None:
        """The user's currently unresolved battle (waiting/challenge/live),
        if any — one open battle per user at a time."""
        with self._factory() as s:
            row = s.execute(
                select(BattleModel)
                .where(((BattleModel.player1_id == user_id)
                        | (BattleModel.player2_id == user_id)),
                       BattleModel.status.in_(("waiting", "challenge", "live")))
                .order_by(BattleModel.created_at.desc())
            ).scalars().first()
            return self._row_out(row) if row else None

    def list_for_user(self, user_id: str, limit: int = 50) -> list[dict]:
        with self._factory() as s:
            rows = s.execute(
                select(BattleModel)
                .where((BattleModel.player1_id == user_id)
                       | (BattleModel.player2_id == user_id))
                .order_by(BattleModel.created_at.desc())
                .limit(limit)
            ).scalars().all()
            return [self._row_out(r) for r in rows]

    def start_live(self, battle_id: str, player2_id: str,
                   started_at: datetime, ends_at: datetime) -> dict:
        with self._factory() as s:
            row = s.get(BattleModel, battle_id)
            row.player2_id = player2_id
            row.status = "live"
            row.started_at = started_at
            row.ends_at = ends_at
            s.commit()
            return self._row_out(row)

    def save_answers(self, battle_id: str, slot: str, answers: dict,
                     times: dict) -> dict:
        with self._factory() as s:
            row = s.get(BattleModel, battle_id)
            if slot == "player1":
                row.player1_answers = json.dumps(answers)
                row.player1_times = json.dumps(times)
            else:
                row.player2_answers = json.dumps(answers)
                row.player2_times = json.dumps(times)
            s.commit()
            return self._row_out(row)

    def finalize(self, battle_id: str, score1: int, correct1: int,
                 score2: int, correct2: int, winner_id: str | None,
                 flagged: bool, flag_reason: str, rewards: dict) -> dict:
        with self._factory() as s:
            row = s.get(BattleModel, battle_id)
            row.status = "finished"
            row.player1_score = score1
            row.player1_correct = correct1
            row.player2_score = score2
            row.player2_correct = correct2
            row.winner_id = winner_id
            row.flagged = flagged
            row.flag_reason = flag_reason
            row.rewards = json.dumps(rewards)
            s.commit()
            return self._row_out(row)

    def expire_waiting(self, battle_id: str) -> dict | None:
        """Drop a stale waiting/challenge entry (lazy expiry)."""
        with self._factory() as s:
            row = s.get(BattleModel, battle_id)
            if row is None or row.status not in ("waiting", "challenge"):
                return self._row_out(row) if row else None
            s.delete(row)
            s.commit()
            return None
