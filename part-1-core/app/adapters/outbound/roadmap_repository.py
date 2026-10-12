"""Outbound adapter: roadmap repository (SQLAlchemy)."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Callable

from sqlalchemy.orm import Session

from app.adapters.outbound.models import RoadmapModel, RoadmapTaskModel
from app.domain.roadmap import Roadmap, RoadmapTask


def _t_to_domain(m: RoadmapTaskModel) -> RoadmapTask:
    return RoadmapTask(
        id=m.task_key, title=m.title, description=m.description,
        why_it_matters=m.why_it_matters,
        target_skills=tuple(json.loads(m.target_skills)),
        prerequisites=tuple(json.loads(m.prerequisites)),
        effort_minutes=m.effort_minutes, priority=m.priority,
        expected_evidence=m.expected_evidence,
        acceptance_criteria=m.acceptance_criteria, status=m.status,
    )


def _r_to_domain(m: RoadmapModel, tasks: list[RoadmapTaskModel]) -> Roadmap:
    return Roadmap(
        id=m.id, user_id=m.user_id, version=m.version,
        title=m.title, source=m.source,
        tasks=[_t_to_domain(t) for t in tasks],
    )


class SqlAlchemyRoadmapRepository:
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._sessions = session_factory

    def save(self, roadmap: Roadmap) -> None:
        with self._sessions() as s:
            m = s.get(RoadmapModel, roadmap.id)
            if m:
                m.title, m.source = roadmap.title, roadmap.source
            else:
                s.add(RoadmapModel(
                    id=roadmap.id, user_id=roadmap.user_id,
                    version=roadmap.version, title=roadmap.title,
                    source=roadmap.source,
                    created_at=datetime.now(timezone.utc),
                ))
            existing = {
                t.task_key: t
                for t in s.query(RoadmapTaskModel).filter_by(roadmap_id=roadmap.id)
            }
            for t in roadmap.tasks:
                if t.id in existing:
                    existing[t.id].status = t.status  # only status mutates after creation
                else:
                    s.add(RoadmapTaskModel(
                        id=uuid.uuid4().hex, task_key=t.id,
                        roadmap_id=roadmap.id, title=t.title,
                        description=t.description, why_it_matters=t.why_it_matters,
                        target_skills=json.dumps(list(t.target_skills)),
                        prerequisites=json.dumps(list(t.prerequisites)),
                        effort_minutes=t.effort_minutes, priority=t.priority,
                        expected_evidence=t.expected_evidence,
                        acceptance_criteria=t.acceptance_criteria,
                        status=t.status,
                        created_at=datetime.now(timezone.utc),
                    ))
            s.commit()

    def get_current(self, user_id: str) -> Roadmap | None:
        with self._sessions() as s:
            m = (
                s.query(RoadmapModel)
                .filter_by(user_id=user_id)
                .order_by(RoadmapModel.version.desc())
                .first()
            )
            if not m:
                return None
            tasks = s.query(RoadmapTaskModel).filter_by(roadmap_id=m.id).all()
            return _r_to_domain(m, tasks)

    def list_versions(self, user_id: str) -> list[Roadmap]:
        with self._sessions() as s:
            models = (
                s.query(RoadmapModel)
                .filter_by(user_id=user_id)
                .order_by(RoadmapModel.version.desc())
                .all()
            )
            out = []
            for m in models:
                tasks = s.query(RoadmapTaskModel).filter_by(roadmap_id=m.id).all()
                out.append(_r_to_domain(m, tasks))
            return out

    def max_version(self, user_id: str) -> int:
        with self._sessions() as s:
            m = (
                s.query(RoadmapModel)
                .filter_by(user_id=user_id)
                .order_by(RoadmapModel.version.desc())
                .first()
            )
            return m.version if m else 0
