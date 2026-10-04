"""Inbound adapter: implements the OnboardingService port."""
from __future__ import annotations

import uuid

from app.domain.profile import (
    Placement,
    Profile,
    public_question,
    score_placement,
    validate_level,
    validate_profile,
    verify_level,
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

    def start_placement(self, user_id: str, topic: str, claimed_level: str) -> tuple[Placement, list[dict]]:
        from app.domain.user import DomainError
        validate_level(claimed_level)
        if topic not in self._bank.topics():
            raise DomainError(f"unknown topic: {topic}")
        questions = self._bank.questions(topic, claimed_level, 4)
        if len(questions) < 4:
            raise DomainError(f"not enough questions for {topic}/{claimed_level}")
        session = Placement(
            id=uuid.uuid4().hex, user_id=user_id, topic=topic,
            claimed_level=claimed_level,
            question_ids=tuple(q.id for q in questions),
        )
        self._placements.save(session)
        return session, [public_question(q) for q in questions]

    def submit_placement(self, user_id: str, placement_id: str, answers: dict[str, int]) -> Placement:
        from app.domain.user import DomainError
        session = self._placements.get(placement_id)
        if not session or session.user_id != user_id:
            raise DomainError("placement session not found")
        if session.status != "open":
            raise DomainError("placement session already completed")
        questions = [q for qid in session.question_ids
                     if (q := self._bank.get(qid)) is not None]
        correct, total = score_placement(questions, answers)
        session.answers = dict(answers)
        session.status = "completed"
        session.correct = correct
        session.total = total
        session.verified_level = verify_level(session.claimed_level, correct / total if total else 0)
        self._placements.save(session)
        return session
