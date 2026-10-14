"""Inbound adapter: implements the OnboardingService port."""
from __future__ import annotations

import uuid

from app.domain.profile import (
    Placement,
    Profile,
    analysis_to_dict,
    analyze_placement,
    public_question,
    sample_placement_questions,
    validate_level,
    validate_profile,
)


class OnboardingServiceImpl:
    def __init__(self, profiles, placements, bank) -> None:
        self._profiles = profiles
        self._placements = placements
        self._bank = bank

    def save_profile(self, user_id: str, **fields) -> Profile:
        validate_profile(
            fields.get("education", ""), fields.get("experience_years", 0),
            fields.get("current_skills", []), fields.get("target_role", ""),
            fields.get("target_domain", ""), fields.get("target_level", ""),
            fields.get("tech_focus", []),
        )
        existing = self._profiles.get_by_user(user_id)
        profile = Profile(
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

    def start_placement(self, user_id: str, topic: str, claimed_level: str) -> tuple[Placement, list[dict]]:
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
            return session, []
        questions = sample_placement_questions(
            self._bank, topic, claimed_level, placement_id
        )
        session = Placement(
            id=placement_id, user_id=user_id, topic=topic,
            claimed_level=claimed_level,
            question_ids=tuple(q.id for q in questions),
        )
        self._placements.save(session)
        return session, [public_question(q) for q in questions]

    def submit_placement(
        self, user_id: str, placement_id: str, answers: dict[str, int]
    ) -> tuple[Placement, dict]:
        from app.domain.user import DomainError
        session = self._placements.get(placement_id)
        if not session or session.user_id != user_id:
            raise DomainError("placement session not found")
        if session.status != "open":
            raise DomainError("placement session already completed")
        questions = [q for qid in session.question_ids
                     if (q := self._bank.get(qid)) is not None]
        analysis = analyze_placement(session.claimed_level, questions, answers)
        session.answers = dict(answers)
        session.status = "completed"
        session.correct = analysis.correct
        session.total = analysis.total
        session.verified_level = analysis.verified_level
        self._placements.save(session)
        return session, analysis_to_dict(analysis)
