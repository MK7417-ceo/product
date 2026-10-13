"""Inbound adapter: implements the OnboardingService port."""
from __future__ import annotations

import uuid

from app.domain.dsa import grade_dsa
from app.domain.profile import (
    Placement,
    Profile,
    analysis_to_dict,
    analyze_placement,
    analyze_placement_coding,
    analyze_placement_written,
    public_question,
    public_written_question,
    sample_placement_coding,
    sample_placement_questions,
    sample_placement_written,
    validate_level,
    validate_profile,
)
from app.domain.dsa import public_dsa
from app.ports.outbound import CodeEngineError


class OnboardingServiceImpl:
    def __init__(self, profiles, placements, bank, dsa_bank=None,
                 code_runner=None) -> None:
        self._profiles = profiles
        self._placements = placements
        self._bank = bank
        self._dsa_bank = dsa_bank if dsa_bank is not None else []
        self._runner = code_runner

    def save_profile(self, user_id: str, **fields) -> Profile:
        validate_profile(
            fields.get("education", ""), fields.get("experience_years", 0),
            fields.get("current_skills", []), fields.get("target_role", ""),
            fields.get("target_domain", ""), fields.get("target_level", ""),
            fields.get("tech_focus", []),
        )
        existing = self._profiles.get_by_user(user_id)
        profile = Profile(
            id=existing.id if existing else uuid.uuid4().hex,
            user_id=user_id,
            education=fields["education"].strip(),
            experience_years=float(fields["experience_years"]),
            current_skills=tuple(s.strip() for s in fields["current_skills"]),
            target_role=fields["target_role"].strip(),
            target_domain=fields["target_domain"].strip(),
            target_level=fields["target_level"],
            tech_focus=tuple(s.strip() for s in fields["tech_focus"]),
        )
        self._profiles.save(profile)
        return profile

    def get_profile(self, user_id: str) -> Profile:
        from app.domain.user import DomainError
        profile = self._profiles.get_by_user(user_id)
        if not profile:
            raise DomainError("profile not found")
        return profile

    def start_placement(self, user_id: str, topic: str, claimed_level: str):
        from app.domain.user import DomainError
        validate_level(claimed_level)
        if topic not in self._bank.topics():
            raise DomainError(f"unknown topic: {topic}")
        placement_id = uuid.uuid4().hex
        if claimed_level == "beginner":
            # Beginners start from scratch: no verification questions needed.
            # The session is completed immediately as verified beginner.
            session = Placement(
                id=placement_id, user_id=user_id, topic=topic,
                claimed_level=claimed_level, question_ids=(),
                status="completed", correct=0, total=0,
                verified_level="beginner",
            )
            self._placements.save(session)
            return session, [], [], []
        questions = sample_placement_questions(
            self._bank, topic, claimed_level, placement_id
        )
        coding = sample_placement_coding(self._dsa_bank, placement_id)
        written = sample_placement_written(self._bank, topic, placement_id)
        session = Placement(
            id=placement_id, user_id=user_id, topic=topic,
            claimed_level=claimed_level,
            question_ids=tuple(q.id for q in questions),
        )
        self._placements.save(session)
        return (session, [public_question(q) for q in questions],
                [public_dsa(q) for q in coding],
                [public_written_question(q) for q in written])

    def _grade_one(self, request_id: str):
        """Build the injected grader for placement coding submissions.

        CodeEngineError (infrastructure failure) propagates out of run_one
        and maps to engine_error — never misreported as the user's
        runtime_error. MCQ grading is unaffected.
        """
        def grade_fn(problem, language: str, code: str):
            if self._runner is None:
                return "engine_error", 0, len(problem.hidden_tests)

            def run_one(lang: str, src: str, stdin: str):
                # CodeEngineError propagates -> caught below as engine_error.
                body = self._runner.run(lang, src, stdin, {}, request_id)
                ok = (body.get("verdict") == "ok"
                      and (body.get("exit_code") in (0, None)))
                err = "" if ok else (body.get("stderr") or body.get("verdict")
                                     or "run failed")
                return ok, body.get("stdout", ""), err

            try:
                verdict = grade_dsa(run_one, problem, language, code)
            except CodeEngineError:
                return "engine_error", 0, len(problem.hidden_tests)
            return verdict.verdict, verdict.passed, verdict.total
        return grade_fn

    def submit_placement(
        self, user_id: str, placement_id: str, answers: dict[str, int],
        code: dict | None = None, written: dict[str, str] | None = None,
    ) -> tuple[Placement, dict]:
        from app.domain.user import DomainError
        session = self._placements.get(placement_id)
        if not session or session.user_id != user_id:
            raise DomainError("placement session not found")
        if session.status != "open":
            raise DomainError("placement session already completed")
        questions = [q for qid in session.question_ids
                     if (q := self._bank.get(qid)) is not None]
        # Coding problems are re-derived from the session seed — the same
        # deterministic draw as start_placement, no migration needed.
        coding_problems = sample_placement_coding(self._dsa_bank, placement_id)
        coding = analyze_placement_coding(
            coding_problems, code or {},
            self._grade_one(f"placement-{placement_id[:8]}"))
        # Written questions likewise re-derived from the session seed.
        written_questions = sample_placement_written(
            self._bank, session.topic, placement_id)
        written_results = analyze_placement_written(
            written_questions, written or {})
        analysis = analyze_placement(
            session.claimed_level, questions, answers,
            coding=coding, written=written_results)
        session.answers = dict(answers)
        session.status = "completed"
        session.correct = analysis.correct
        session.total = analysis.total
        session.verified_level = analysis.verified_level
        self._placements.save(session)
        return session, analysis_to_dict(analysis)
