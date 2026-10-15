"""Inbound adapter: Placement Simulator service — 6 rounds, cutoffs, cooldown."""
from __future__ import annotations

import random
from datetime import date, datetime, timezone

from app.domain import simulator as sim
from app.domain.user import DomainError


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


# Lazy imports keep module import light for unit tests.
def _aptitude_pool() -> list[dict]:
    from app.adapters.outbound.quant_bank import APTITUDE_QUESTIONS
    return APTITUDE_QUESTIONS


def _english_pool() -> list:
    from app.adapters.outbound.english_bank import ENGLISH_BANK
    return ENGLISH_BANK


def _technical_pool() -> list:
    from app.adapters.outbound.question_bank import _BANK
    return _BANK


def _coding_pool() -> list:
    from app.adapters.outbound.dsa_bank import _DSA_BANK
    return _DSA_BANK


def _interview_pool(category: str) -> list[dict]:
    from app.adapters.outbound.interview_qa import get_interview_qa
    return get_interview_qa(category)


def _seeded_pick(pool: list, count: int, seed: int) -> list:
    rng = random.Random(seed)
    pool = list(pool)
    rng.shuffle(pool)
    return pool[:count]


class SimulatorServiceImpl:
    """Orchestrates simulator attempts across the 6 rounds."""

    def __init__(self, repo, coin_service=None) -> None:
        self._repo = repo
        self._coins = coin_service

    # ---- lifecycle ----

    def start(self, user_id: str, company: str = "general") -> dict:
        """Start or resume a simulator attempt.

        Resumes an in-progress attempt; enforces the 7-day cooldown
        after a completed/eliminated attempt (raises DomainError).
        """
        latest = self._repo.latest_attempt(user_id)
        if latest and latest["status"] == sim.ATTEMPT_IN_PROGRESS:
            return {"attempt": latest, "resumed": True}

        if latest and latest["status"] in (
                sim.ATTEMPT_ELIMINATED, sim.ATTEMPT_PLACED):
            end = latest.get("completed_at") or latest.get("started_at")
            if end:
                try:
                    end_date = datetime.fromisoformat(end).date()
                except ValueError:
                    end_date = date.today()
                if not sim.can_retry(end_date):
                    raise DomainError(
                        "cooldown: retry available on "
                        f"{sim.retry_available_on(end_date).isoformat()}")

        attempt = self._repo.create_attempt(user_id, company or "general")
        return {"attempt": attempt, "resumed": False}

    def my_attempts(self, user_id: str) -> dict:
        attempts = self._repo.list_attempts(user_id)
        # Cooldown info from the latest finished attempt.
        retry_on = None
        latest = attempts[0] if attempts else None
        if latest and latest["status"] in (
                sim.ATTEMPT_ELIMINATED, sim.ATTEMPT_PLACED):
            end = latest.get("completed_at") or latest.get("started_at")
            if end:
                try:
                    end_date = datetime.fromisoformat(end).date()
                except ValueError:
                    end_date = None
                if end_date and not sim.can_retry(end_date):
                    retry_on = sim.retry_available_on(end_date).isoformat()
        return {"attempts": attempts, "retry_available_on": retry_on,
                "can_start": retry_on is None}

    # ---- rounds ----

    def get_round(self, user_id: str, attempt_id: str,
                  round_number: int) -> dict:
        attempt = self._owned_attempt(user_id, attempt_id)
        cfg = sim.round_config(round_number)
        if attempt["status"] != sim.ATTEMPT_IN_PROGRESS:
            raise DomainError("attempt is finished")
        if round_number != attempt["current_round"]:
            raise DomainError(
                f"round {attempt['current_round']} is current; "
                f"requested {round_number}")

        existing = self._repo.get_round(attempt_id, round_number)
        if existing and not existing.get("completed_at"):
            qids = existing["question_ids"]
        else:
            picks = self._pick_questions(cfg, attempt_id, round_number)
            qids = [self._qid(p, cfg["source"]) for p in picks]
            self._repo.create_round(
                attempt_id, round_number, cfg["name"], qids, len(qids))
            # Keep picks for serving below.
            return self._serve(cfg, picks, attempt, existing_round=False)

        picks = self._resolve_questions(cfg, qids)
        return self._serve(cfg, picks, attempt, existing_round=True)

    def submit_round(self, user_id: str, attempt_id: str,
                     round_number: int, answers: dict) -> dict:
        attempt = self._owned_attempt(user_id, attempt_id)
        cfg = sim.round_config(round_number)
        if attempt["status"] != sim.ATTEMPT_IN_PROGRESS:
            raise DomainError("attempt is finished")
        if round_number != attempt["current_round"]:
            raise DomainError("not the current round")

        rnd = self._repo.get_round(attempt_id, round_number)
        if not rnd:
            raise DomainError("round not started")
        if rnd.get("completed_at"):
            raise DomainError("round already submitted")

        picks = self._resolve_questions(cfg, rnd["question_ids"])
        score = self._score(cfg["source"], picks, answers or {})
        total = len(picks)
        passed = sim.round_passed(score, total)

        self._repo.submit_round(rnd["id"], answers or {}, score, passed)

        result: dict = {
            "round_number": round_number,
            "round_name": cfg["name"],
            "score": score,
            "total": total,
            "passed": passed,
            "cutoff": sim.CUTOFF,
        }

        if not passed:
            self._repo.update_attempt(
                attempt_id, status=sim.ATTEMPT_ELIMINATED,
                completed_at=_utcnow(),
                final_score=self._final_score(attempt_id))
            result["status"] = sim.ATTEMPT_ELIMINATED
            result["eliminated_at_round"] = round_number
            result["retry_available_on"] = sim.retry_available_on(
                date.today()).isoformat()
            return result

        nxt = sim.next_round(round_number)
        if nxt is None:
            coins = 0
            if self._coins:
                try:
                    self._coins.earn(user_id, "simulator_placed")
                    coins = sim.PLACED_COINS
                except Exception:
                    coins = 0
            self._repo.update_attempt(
                attempt_id, status=sim.ATTEMPT_PLACED,
                current_round=round_number, completed_at=_utcnow(),
                final_score=self._final_score(attempt_id),
                coins_earned=coins)
            result["status"] = sim.ATTEMPT_PLACED
            result["coins_earned"] = coins
        else:
            self._repo.update_attempt(attempt_id, current_round=nxt)
            result["status"] = sim.ATTEMPT_IN_PROGRESS
            result["next_round"] = nxt
            result["next_round_name"] = sim.ROUNDS[nxt]["name"]
        return result

    # ---- report ----

    def report(self, user_id: str, attempt_id: str) -> dict:
        attempt = self._owned_attempt(user_id, attempt_id)
        rounds = self._repo.list_rounds(attempt_id)
        per_round = []
        pcts = []
        for r in rounds:
            pct = (r["score"] / r["total"]) if r["total"] and r["score"] is not None else 0.0
            pcts.append(pct)
            per_round.append({
                "round_number": r["round_number"],
                "round_name": r["round_name"],
                "score": r["score"],
                "total": r["total"],
                "passed": r["passed"],
                "percent": round(pct * 100),
                "grade": sim.grade_for(pct),
            })
        strengths, weaknesses = [], []
        if per_round:
            best = max(per_round, key=lambda x: x["percent"])
            worst = min(per_round, key=lambda x: x["percent"])
            strengths = [best["round_name"]] if best["percent"] >= 60 else []
            weaknesses = [worst["round_name"]] if worst["percent"] < 80 else []
        avg = round(sum(pcts) / len(pcts) * 100) if pcts else 0
        return {
            "attempt": attempt,
            "rounds": per_round,
            "average_percent": avg,
            "overall_grade": sim.grade_for(avg / 100),
            "strengths": strengths,
            "weaknesses": weaknesses,
            "coins_earned": attempt.get("coins_earned", 0),
        }

    # ---- internals ----

    def _owned_attempt(self, user_id: str, attempt_id: str) -> dict:
        attempt = self._repo.get_attempt(attempt_id)
        if not attempt or attempt["user_id"] != user_id:
            raise DomainError("attempt not found")
        return attempt

    def _pick_questions(self, cfg: dict, attempt_id: str,
                        round_number: int) -> list:
        source = cfg["source"]
        count = cfg["questions"]
        seed = abs(hash((attempt_id, round_number))) % (2 ** 31)
        if source == "aptitude":
            return _seeded_pick(_aptitude_pool(), count, seed)
        if source == "english":
            return _seeded_pick(_english_pool(), count, seed)
        if source == "technical":
            return _seeded_pick(_technical_pool(), count, seed)
        if source == "coding":
            return _seeded_pick(_coding_pool(), count, seed)
        if source == "tech_interview":
            return _seeded_pick(_interview_pool("technical"), count, seed)
        if source == "hr_interview":
            return _seeded_pick(_interview_pool("hr"), count, seed)
        raise DomainError(f"unknown round source: {source}")

    @staticmethod
    def _qid(pick, source: str) -> str:
        if source in ("aptitude", "tech_interview", "hr_interview"):
            return pick["id"]
        return pick.id

    def _resolve_questions(self, cfg: dict, qids: list[str]) -> list:
        source = cfg["source"]
        if source == "aptitude":
            by_id = {q["id"]: q for q in _aptitude_pool()}
        elif source == "english":
            by_id = {q.id: q for q in _english_pool()}
        elif source == "technical":
            by_id = {q.id: q for q in _technical_pool()}
        elif source == "coding":
            by_id = {p.id: p for p in _coding_pool()}
        elif source == "tech_interview":
            by_id = {q["id"]: q for q in _interview_pool("technical")}
        elif source == "hr_interview":
            by_id = {q["id"]: q for q in _interview_pool("hr")}
        else:
            raise DomainError(f"unknown round source: {source}")
        return [by_id[qid] for qid in qids if qid in by_id]

    def _serve(self, cfg: dict, picks: list, attempt: dict,
               existing_round: bool) -> dict:
        source = cfg["source"]
        questions: list[dict] = []
        if source == "aptitude":
            for q in picks:
                questions.append({
                    "id": q["id"], "type": "mcq",
                    "prompt": q["question"], "choices": list(q["options"]),
                })
        elif source in ("english", "technical"):
            from app.adapters.outbound.english_bank import get_passage
            for q in picks:
                item: dict = {
                    "id": q.id, "type": "mcq",
                    "prompt": q.prompt, "choices": list(q.choices),
                    "skill": q.skill,
                }
                if source == "english" and q.skill.startswith("rc-p"):
                    passage = get_passage(q.skill)
                    if passage:
                        item["passage"] = passage
                questions.append(item)
        elif source == "coding":
            for p in picks:
                questions.append({
                    "id": p.id, "type": "coding",
                    "title": p.title, "topic": p.topic,
                    "difficulty": p.difficulty,
                    "description": p.description,
                    "examples": p.examples,
                    "constraints": p.constraints,
                    "theory": p.theory,
                    "hints": p.hints,
                    "starter_code": p.starter_code,
                })
        else:  # interviews
            for q in picks:
                questions.append({
                    "id": q["id"], "type": "interview",
                    "question": q["question"],
                    "category": q["category"],
                })
        return {
            "attempt_id": attempt["id"],
            "round_number": self._round_number(cfg),
            "round_name": cfg["name"],
            "minutes": cfg["minutes"],
            "total": len(questions),
            "questions": questions,
        }

    @staticmethod
    def _round_number(cfg: dict) -> int:
        for n, c in sim.ROUNDS.items():
            if c is cfg:
                return n
        raise DomainError("unknown round config")

    def _score(self, source: str, picks: list, answers: dict) -> int:
        if source in ("aptitude", "english", "technical"):
            correct = 0
            for p in picks:
                qid = p["id"] if isinstance(p, dict) else p.id
                expected = p["answer"] if isinstance(p, dict) else p.answer_index
                try:
                    given = int(answers.get(qid, -1))
                except (TypeError, ValueError):
                    given = -1
                if given == expected:
                    correct += 1
            return correct
        if source == "coding":
            solved = 0
            for p in picks:
                val = answers.get(p.id)
                if isinstance(val, dict):
                    ok = bool(val.get("solved"))
                else:
                    ok = bool(val)
                if ok:
                    solved += 1
            return solved
        # interviews: self-evaluated per question
        return sum(1 for p in picks if bool(answers.get(p["id"])))

    def _final_score(self, attempt_id: str) -> int:
        rounds = self._repo.list_rounds(attempt_id)
        pcts = []
        for r in rounds:
            if r["total"] and r["score"] is not None:
                pcts.append(r["score"] / r["total"])
        return round(sum(pcts) / len(pcts) * 100) if pcts else 0
