"""Inbound adapter: 1v1 battle service — queue, match, challenge, play,
score, reward. No fake opponents: a battle only goes live when a second
REAL user joins; otherwise the player waits in queue."""
from __future__ import annotations

import secrets
import string
import uuid
from datetime import datetime, timedelta, timezone

from app.domain import battles as bt
from app.domain.user import DomainError


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    dt = datetime.fromisoformat(value)
    return dt if dt.tzinfo is not None else dt.replace(tzinfo=timezone.utc)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class BattleServiceImpl:
    def __init__(self, battle_repo, bank, user_repo=None,
                 coin_service=None) -> None:
        self._repo = battle_repo
        self._bank = bank
        self._users = user_repo
        self._coins = coin_service

    # ---- validation helpers ----

    def _bracket(self, topic: str, level: str, window: int) -> str:
        if topic not in self._bank.topics():
            raise DomainError(f"unknown topic: {topic}")
        try:
            bracket = bt.bracket_for(level)
        except ValueError as exc:
            raise DomainError(str(exc))
        if window not in bt.ALLOWED_WINDOWS:
            raise DomainError(
                f"window must be one of {list(bt.ALLOWED_WINDOWS)} seconds")
        return bracket

    def _pool_level(self, bracket: str) -> str:
        # The bank has beginner/intermediate/advanced pools; the advanced
        # bracket (advanced + expert players) plays the advanced pool.
        return bracket

    def _pick(self, topic: str, bracket: str, battle_id: str) -> list:
        pool = self._bank.pool(topic, self._pool_level(bracket))
        try:
            return bt.pick_questions(pool, battle_id)
        except ValueError as exc:
            raise DomainError(str(exc))

    def _clear_stale_open(self, user_id: str) -> None:
        """Expire the user's open battle if it is past its queue window."""
        open_b = self._repo.user_open_battle(user_id)
        if not open_b:
            return
        created = _parse_dt(open_b["created_at"])
        if open_b["status"] == "waiting" and created and (
                _utcnow() - created).total_seconds() > bt.QUEUE_EXPIRY_SECONDS:
            self._repo.expire_waiting(open_b["id"])
        elif open_b["status"] == "challenge" and created and (
                _utcnow() - created).total_seconds() > bt.CHALLENGE_EXPIRY_SECONDS:
            self._repo.expire_waiting(open_b["id"])
        elif open_b["status"] == "live":
            self._maybe_finalize(open_b)

    def _require_no_open(self, user_id: str) -> None:
        self._clear_stale_open(user_id)
        if self._repo.user_open_battle(user_id):
            raise DomainError(
                "you already have an open battle — finish it first")

    # ---- queue + matchmaking ----

    def queue(self, user_id: str, topic: str, level: str,
              window_seconds: int = bt.DEFAULT_WINDOW_SECONDS,
              rematch_of: str | None = None) -> dict:
        bracket = self._bracket(topic, level, window_seconds)
        self._require_no_open(user_id)
        match = self._repo.find_waiting_match(topic, bracket, user_id,
                                              rematch_of=rematch_of)
        if match is not None:
            now = _utcnow()
            live = self._repo.start_live(
                match["id"], user_id, now,
                now + timedelta(seconds=match["window_seconds"]))
            return {"matched": True, "battle": self._public(live, user_id)}
        battle_id = uuid.uuid4().hex
        picks = self._pick(topic, bracket, battle_id)
        row = self._repo.create_waiting(
            user_id, topic, bracket, level, [q.id for q in picks],
            window_seconds, rematch_of=rematch_of, battle_id=battle_id)
        return {"matched": False, "battle": self._public(row, user_id)}

    def rematch(self, user_id: str, battle_id: str) -> dict:
        battle = self._repo.get(battle_id)
        if not battle or user_id not in (battle["player1_id"],
                                         battle["player2_id"]):
            raise DomainError("battle not found")
        if battle["status"] != "finished":
            raise DomainError("only a finished battle can be rematched")
        return self.queue(user_id, battle["topic"], battle["level"],
                          battle["window_seconds"], rematch_of=battle_id)

    # ---- friend challenge ----

    def challenge(self, user_id: str, topic: str, level: str,
                  opponent_email: str,
                  window_seconds: int = bt.DEFAULT_WINDOW_SECONDS) -> dict:
        bracket = self._bracket(topic, level, window_seconds)
        self._require_no_open(user_id)
        if self._users is None:
            raise DomainError("user lookup unavailable")
        opponent = self._users.find_by_email(opponent_email.strip().lower())
        if opponent is None:
            raise DomainError("opponent not found")
        if opponent.id == user_id:
            raise DomainError("you cannot challenge yourself")
        battle_id = uuid.uuid4().hex
        picks = self._pick(topic, bracket, battle_id)
        code = "".join(secrets.choice(string.ascii_uppercase + string.digits)
                       for _ in range(8))
        row = self._repo.create_challenge(
            user_id, topic, bracket, level, [q.id for q in picks],
            window_seconds, opponent_email.strip().lower(), code,
            battle_id=battle_id)
        return {"battle": self._public(row, user_id),
                "invite_code": code}

    def join_challenge(self, user_id: str, invite_code: str,
                       level: str) -> dict:
        battle = self._repo.get_by_invite_code(invite_code.strip().upper())
        if not battle or battle["status"] != "challenge":
            raise DomainError("invite not found or already used")
        created = _parse_dt(battle["created_at"])
        if created and (_utcnow() - created).total_seconds() > bt.CHALLENGE_EXPIRY_SECONDS:
            self._repo.expire_waiting(battle["id"])
            raise DomainError("invite expired")
        if battle["player1_id"] == user_id:
            raise DomainError("you cannot join your own challenge")
        # The invite names one friend — only they may accept it.
        if self._users is not None:
            me = self._users.get(user_id)
            if me is not None and battle["invite_email"] not in (None, "") \
                    and me.email.strip().lower() != battle["invite_email"]:
                raise DomainError("this invite is for another user")
        try:
            bracket = bt.bracket_for(level)
        except ValueError as exc:
            raise DomainError(str(exc))
        if bracket != battle["bracket"]:
            raise DomainError(
                "level bracket mismatch — battles are level-matched")
        self._require_no_open(user_id)
        now = _utcnow()
        live = self._repo.start_live(
            battle["id"], user_id, now,
            now + timedelta(seconds=battle["window_seconds"]))
        return {"battle": self._public(live, user_id)}

    # ---- playing ----

    def get_battle(self, user_id: str, battle_id: str) -> dict:
        battle = self._repo.get(battle_id)
        if not battle or user_id not in (battle["player1_id"],
                                         battle["player2_id"]):
            raise DomainError("battle not found")
        battle = self._maybe_finalize(battle)
        return self._public(battle, user_id, include_review=True)

    def mine(self, user_id: str) -> dict:
        self._clear_stale_open(user_id)
        battles = self._repo.list_for_user(user_id)
        out = []
        for b in battles:
            b = self._maybe_finalize(b)
            out.append(self._public(b, user_id))
        return {
            "battles": out,
            "open": next((b for b in out
                          if b["status"] in ("waiting", "challenge", "live")),
                         None),
        }

    def submit(self, user_id: str, battle_id: str, answers: dict,
               answer_times: dict | None = None) -> dict:
        battle = self._repo.get(battle_id)
        if not battle or user_id not in (battle["player1_id"],
                                         battle["player2_id"]):
            raise DomainError("battle not found")
        if battle["status"] != "live":
            raise DomainError("battle is not live")
        ends = _parse_dt(battle["ends_at"])
        if ends and _utcnow() > ends:
            self._maybe_finalize(battle)
            raise DomainError("time is up — battle finished")
        slot = "player1" if user_id == battle["player1_id"] else "player2"
        clean_answers = {str(k): v for k, v in (answers or {}).items()
                         if str(k) in battle["question_ids"]}
        clean_times = {}
        for k, v in (answer_times or {}).items():
            if str(k) in battle["question_ids"] and isinstance(v, (int, float)):
                clean_times[str(k)] = max(0.0, min(float(v),
                                                   battle["window_seconds"]))
        if battle[f"{slot}_answers"]:
            raise DomainError("you already submitted")
        saved = self._repo.save_answers(battle_id, slot, clean_answers,
                                        clean_times)
        other_slot = "player2" if slot == "player1" else "player1"
        if saved[f"{other_slot}_answers"]:
            finished = self._finalize(saved)
            return {"battle": self._public(finished, user_id,
                                            include_review=True),
                    "waiting_for_opponent": False}
        return {"battle": self._public(saved, user_id),
                "waiting_for_opponent": True}

    # ---- finalize ----

    def _maybe_finalize(self, battle: dict) -> dict:
        if battle["status"] != "live":
            return battle
        ends = _parse_dt(battle["ends_at"])
        if ends and _utcnow() > ends:
            return self._finalize(battle)
        return battle

    def _finalize(self, battle: dict) -> dict:
        correct_map = {}
        for qid in battle["question_ids"]:
            q = self._bank.get(qid)
            if q is not None:
                correct_map[qid] = q.answer_index
        s1 = bt.score_player(battle["player1_answers"],
                             battle["player1_times"], correct_map,
                             battle["window_seconds"])
        s2 = bt.score_player(battle["player2_answers"],
                             battle["player2_times"], correct_map,
                             battle["window_seconds"])
        flag = bt.check_submission(battle["player1_answers"],
                                   battle["player1_times"],
                                   battle["player2_answers"],
                                   battle["player2_times"], correct_map)
        winner_slot = bt.decide_winner(s1, s2)
        winner_id = None
        if winner_slot == 1:
            winner_id = battle["player1_id"]
        elif winner_slot == 2:
            winner_id = battle["player2_id"]
        rewards: dict = {"flagged": flag.flagged,
                         "flag_reason": flag.reason}
        if flag.flagged:
            # Coins withheld pending review — never paid on a flagged run.
            rewards.update({"winner_coins": 0, "loser_coins": 0,
                            "coins_withheld": True})
        else:
            if winner_id is None:
                rewards.update({"winner_coins": 0,
                                "player1_coins": bt.PARTICIPATION_COINS,
                                "player2_coins": bt.PARTICIPATION_COINS})
            else:
                loser_id = (battle["player2_id"] if winner_id == battle["player1_id"]
                            else battle["player1_id"])
                rewards.update({"winner_coins": bt.WINNER_COINS,
                                "winner_id": winner_id,
                                "loser_id": loser_id,
                                "loser_coins": bt.PARTICIPATION_COINS})
            self._pay_rewards(battle, winner_id, rewards)
        return self._repo.finalize(
            battle["id"], s1.points, s1.correct, s2.points, s2.correct,
            winner_id, flag.flagged, flag.reason, rewards)

    def _pay_rewards(self, battle: dict, winner_id: str | None,
                     rewards: dict) -> None:
        if self._coins is None:
            return
        try:
            if winner_id is None:
                for pid in (battle["player1_id"], battle["player2_id"]):
                    if pid:
                        self._coins.earn(pid, "battle_participation")
            else:
                loser_id = (battle["player2_id"] if winner_id == battle["player1_id"]
                            else battle["player1_id"])
                self._coins.earn(winner_id, "battle_win")
                if loser_id:
                    self._coins.earn(loser_id, "battle_participation")
        except Exception:
            # Rewards must never break finalize; the stored rewards record
            # still shows what was due.
            pass

    # ---- presentation (never leak answers to players mid-battle) ----

    def _questions_out(self, battle: dict) -> list[dict]:
        out = []
        for qid in battle["question_ids"]:
            q = self._bank.get(qid)
            if q is None:
                continue
            out.append({"id": q.id, "prompt": q.prompt,
                        "choices": list(q.choices), "skill": q.skill})
        return out

    def _public(self, battle: dict, user_id: str,
                include_review: bool = False) -> dict:
        mine_slot = "player1" if user_id == battle["player1_id"] else "player2"
        out = {
            "battle_id": battle["id"],
            "topic": battle["topic"],
            "bracket": battle["bracket"],
            "status": battle["status"],
            "window_seconds": battle["window_seconds"],
            "player1_id": battle["player1_id"],
            "player2_id": battle["player2_id"],
            "you_are": mine_slot,
            "started_at": battle["started_at"],
            "ends_at": battle["ends_at"],
            "player1_score": battle["player1_score"],
            "player2_score": battle["player2_score"],
            "player1_correct": battle["player1_correct"],
            "player2_correct": battle["player2_correct"],
            "winner_id": battle["winner_id"],
            "you_won": battle["winner_id"] == user_id if battle["winner_id"] else None,
            "flagged": battle["flagged"],
            "flag_reason": battle["flag_reason"],
            "rewards": battle["rewards"],
            "invite_code": battle["invite_code"],
            "rematch_of": battle["rematch_of"],
            "submitted": bool(battle[f"{mine_slot}_answers"]),
        }
        if battle["status"] in ("live", "finished"):
            out["questions"] = self._questions_out(battle)
        if battle["status"] == "finished" and include_review:
            correct_map = {}
            for qid in battle["question_ids"]:
                q = self._bank.get(qid)
                if q is not None:
                    correct_map[qid] = q.answer_index
            out["review"] = [{
                "question_id": qid,
                "given": battle[f"{mine_slot}_answers"].get(qid),
                "correct": correct_map.get(qid),
                "is_correct": battle[f"{mine_slot}_answers"].get(qid) is not None
                and battle[f"{mine_slot}_answers"].get(qid) == correct_map.get(qid),
            } for qid in battle["question_ids"] if qid in correct_map]
        return out

    def fair_play(self) -> dict:
        return {
            "rules": bt.FAIR_PLAY_RULES,
            "winner_coins": bt.WINNER_COINS,
            "participation_coins": bt.PARTICIPATION_COINS,
            "window_seconds_options": list(bt.ALLOWED_WINDOWS),
            "question_count": bt.BATTLE_QUESTION_COUNT,
            "brackets": list(bt.BRACKETS),
        }
