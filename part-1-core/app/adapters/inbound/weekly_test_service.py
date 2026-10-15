"""Inbound adapter: weekly test service — schedule, start, submit, grade."""
from __future__ import annotations

from datetime import date, timedelta

from app.domain.user import DomainError
from app.domain import weekly_test as wt


class WeeklyTestServiceImpl:
    """Orchestrates weekly tests using the curriculum question pool."""

    def __init__(self, weekly_repo, curriculum_repo, coin_service=None) -> None:
        self._wrepo = weekly_repo
        self._crepo = curriculum_repo
        self._coins = coin_service

    # ---- scheduling ----

    def schedule_for_plan(self, user_id: str, domain_slug: str,
                          plan_id: str, total_days: int,
                          start_date: date | None = None) -> list[dict]:
        """Create one weekly test row per week of the plan. Called on plan creation."""
        start = start_date or date.today()
        weeks = max(1, (total_days + 6) // 7)
        out = []
        for week in range(1, weeks + 1):
            scheduled = start + timedelta(days=(week - 1) * 7)
            out.append(self._wrepo.create(
                user_id=user_id, domain_slug=domain_slug,
                week_number=week, scheduled_date=scheduled, plan_id=plan_id))
        return out

    def my_tests(self, user_id: str) -> dict:
        tests = self._wrepo.list_for_user(user_id)
        today = date.today()
        upcoming = [t for t in tests if t["status"] in ("scheduled", "active")]
        past = [t for t in tests if t["status"] in ("completed", "missed")]
        next_test = None
        for t in sorted(upcoming, key=lambda x: x["scheduled_date"] or ""):
            next_test = t
            break
        days_until = None
        if next_test and next_test.get("scheduled_date"):
            try:
                sd = date.fromisoformat(next_test["scheduled_date"])
                days_until = max(0, (sd - today).days)
            except ValueError:
                pass
        return {
            "upcoming": upcoming,
            "past": past,
            "next_test": next_test,
            "days_until_next": days_until,
        }

    # ---- taking a test ----

    def start_test(self, user_id: str, test_id: str) -> dict:
        test = self._wrepo.get(test_id)
        if not test or test["user_id"] != user_id:
            raise DomainError("test not found")
        if test["status"] == "completed":
            raise DomainError("test already completed")

        # Build the question pool for the domain.
        pool_rows = self._crepo.list_questions(test["domain_slug"])
        pool = [{"id": q.id, "difficulty": q.difficulty} for q in pool_rows]
        if not pool:
            raise DomainError("no questions available for this domain yet")

        used = self._wrepo.used_question_ids(user_id, test["domain_slug"])
        picks = wt.generate_weekly_test(
            test["domain_slug"], test["week_number"], pool,
            used_ids=used, seed=hash((user_id, test_id)) % (2 ** 31))

        started = self._wrepo.start(test_id, [p.question_id for p in picks])
        questions = self._questions_by_id([p.question_id for p in picks])
        return {
            "test": started,
            "questions": questions,
            "duration_minutes": wt.TEST_DURATION_MINUTES,
        }

    def _questions_by_id(self, ids: list[str]) -> list[dict]:
        from app.adapters.inbound.curriculum_service import CurriculumServiceImpl
        rows = self._crepo.get_questions_by_ids(ids)
        result = [CurriculumServiceImpl._question_out(q) for q in rows]
        # Preserve test order.
        order = {qid: i for i, qid in enumerate(ids)}
        result.sort(key=lambda q: order.get(q["id"], 999))
        return result

    def submit_test(self, user_id: str, test_id: str, answers: dict) -> dict:
        test = self._wrepo.get(test_id)
        if not test or test["user_id"] != user_id:
            raise DomainError("test not found")
        if test["status"] == "completed":
            raise DomainError("test already submitted")

        questions = self._questions_by_id(test["question_ids"])
        answer_map = {q["id"]: q.get("answer_index") for q in questions}
        score = 0
        review = []
        for q in questions:
            qid = q["id"]
            correct = answer_map.get(qid)
            given = answers.get(qid)
            is_correct = given is not None and given == correct
            if is_correct:
                score += 1
            review.append({
                "question_id": qid,
                "prompt": q["prompt"],
                "choices": q["choices"],
                "given": given,
                "correct": correct,
                "is_correct": is_correct,
                "explanation": q.get("explanation", ""),
            })

        total = test["total_questions"] or len(questions) or 1
        pct = round(score / total * 100, 1)
        grade = wt.calculate_grade(pct)
        saved = self._wrepo.submit(test_id, answers, score)

        coins_earned = 0
        if self._coins is not None:
            try:
                res = self._coins.earn(user_id, "mock_completed")
                coins_earned = res.get("earned", 0) if isinstance(res, dict) else 0
            except Exception:
                coins_earned = 0

        return {
            "test": saved,
            "score": score,
            "total": total,
            "percentage": pct,
            "grade": grade["grade"],
            "grade_message": grade["message"],
            "coins_earned": coins_earned,
            "review": review,
        }
