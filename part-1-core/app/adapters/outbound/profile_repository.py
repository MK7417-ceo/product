"""Outbound adapters: profile + placement repositories (SQLAlchemy)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Callable

from sqlalchemy.orm import Session

from app.adapters.outbound.models import PlacementModel, ProfileModel
from app.domain.profile import Placement, Profile


def _p_to_domain(m: ProfileModel) -> Profile:
    return Profile(
        id=m.id, user_id=m.user_id, education=m.education,
        experience_years=m.experience_years,
        current_skills=tuple(json.loads(m.current_skills)),
        target_role=m.target_role, target_domain=m.target_domain,
        target_level=m.target_level,
        tech_focus=tuple(json.loads(m.tech_focus)),
        created_at=m.created_at,
    )


def _pl_to_domain(m: PlacementModel) -> Placement:
    return Placement(
        id=m.id, user_id=m.user_id, topic=m.topic, claimed_level=m.claimed_level,
        question_ids=tuple(json.loads(m.question_ids)),
        answers=dict(json.loads(m.answers)), status=m.status,
        correct=m.correct, total=m.total, verified_level=m.verified_level,
    )


class SqlAlchemyProfileRepository:
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._sessions = session_factory

    def save(self, profile: Profile) -> None:
        with self._sessions() as s:
            m = s.get(ProfileModel, profile.id)
            payload = dict(
                user_id=profile.user_id, education=profile.education,
                experience_years=profile.experience_years,
                current_skills=json.dumps(list(profile.current_skills)),
                target_role=profile.target_role, target_domain=profile.target_domain,
                target_level=profile.target_level,
                tech_focus=json.dumps(list(profile.tech_focus)),
                created_at=profile.created_at,
            )
            if m:
                for k, v in payload.items():
                    setattr(m, k, v)
            else:
                s.add(ProfileModel(id=profile.id, **payload))
            s.commit()

    def get_by_user(self, user_id: str) -> Profile | None:
        with self._sessions() as s:
            m = s.query(ProfileModel).filter_by(user_id=user_id).one_or_none()
            return _p_to_domain(m) if m else None


class SqlAlchemyPlacementRepository:
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._sessions = session_factory

    def save(self, placement: Placement) -> None:
        with self._sessions() as s:
            m = s.get(PlacementModel, placement.id)
            payload = dict(
                user_id=placement.user_id, topic=placement.topic,
                claimed_level=placement.claimed_level,
                question_ids=json.dumps(list(placement.question_ids)),
                answers=json.dumps(placement.answers), status=placement.status,
                correct=placement.correct, total=placement.total,
                verified_level=placement.verified_level,
                created_at=datetime.now(timezone.utc),
            )
            if m:
                for k, v in payload.items():
                    if k != "created_at":
                        setattr(m, k, v)
            else:
                s.add(PlacementModel(id=placement.id, **payload))
            s.commit()

    def get(self, placement_id: str) -> Placement | None:
        with self._sessions() as s:
            m = s.get(PlacementModel, placement_id)
            return _pl_to_domain(m) if m else None
