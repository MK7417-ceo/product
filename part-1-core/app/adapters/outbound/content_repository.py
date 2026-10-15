"""Outbound adapter: content CMS repository (SQLAlchemy)."""
from __future__ import annotations

import json
from typing import Callable

from sqlalchemy.orm import Session

from app.adapters.outbound.models import BankQuestionModel, TheoryModel, TopicModel
from app.domain.content import BankQuestion, TheoryBlock, Topic


def _t_to_domain(m: TopicModel) -> Topic:
    return Topic(id=m.id, slug=m.slug, name=m.name, description=m.description,
                 icon=m.icon, color=m.color, is_active=m.is_active,
                 created_at=m.created_at)


def _th_to_domain(m: TheoryModel) -> TheoryBlock:
    return TheoryBlock(id=m.id, topic_slug=m.topic_slug, level=m.level,
                       title=m.title, content=m.content,
                       order_index=m.order_index, created_at=m.created_at)


def _q_to_domain(m: BankQuestionModel) -> BankQuestion:
    return BankQuestion(
        id=m.id, topic_slug=m.topic_slug, qtype=m.qtype, level=m.level,
        prompt=m.prompt, skill_tag=m.skill_tag,
        choices=tuple(json.loads(m.choices)) if m.choices else (),
        answer_index=m.answer_index,
        rubric=dict(json.loads(m.rubric)) if m.rubric else {},
        created_at=m.created_at,
    )


class SqlAlchemyContentRepository:
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._sessions = session_factory

    # ---- topics ----
    def list_topics(self, active_only: bool = True) -> list[Topic]:
        with self._sessions() as s:
            q = s.query(TopicModel).order_by(TopicModel.name)
            if active_only:
                q = q.filter(TopicModel.is_active.is_(True))
            return [_t_to_domain(m) for m in q.all()]

    def get_topic(self, slug: str) -> Topic | None:
        with self._sessions() as s:
            m = s.query(TopicModel).filter_by(slug=slug).one_or_none()
            return _t_to_domain(m) if m else None

    def save_topic(self, topic: Topic) -> None:
        with self._sessions() as s:
            m = s.get(TopicModel, topic.id)
            payload = dict(slug=topic.slug, name=topic.name,
                           description=topic.description, icon=topic.icon,
                           color=topic.color, is_active=topic.is_active,
                           created_at=topic.created_at)
            if m:
                for k, v in payload.items():
                    setattr(m, k, v)
            else:
                s.add(TopicModel(id=topic.id, **payload))
            s.commit()

    def delete_topic(self, slug: str) -> bool:
        with self._sessions() as s:
            m = s.query(TopicModel).filter_by(slug=slug).one_or_none()
            if not m:
                return False
            s.delete(m)  # FK ondelete=CASCADE removes theory + questions
            s.commit()
            return True

    def count_questions(self, slug: str) -> dict[str, int]:
        with self._sessions() as s:
            rows = (s.query(BankQuestionModel.qtype, BankQuestionModel.level)
                    .filter_by(topic_slug=slug).all())
            out: dict[str, int] = {}
            for qtype, level in rows:
                out[f"{qtype}:{level}"] = out.get(f"{qtype}:{level}", 0) + 1
            return out

    # ---- theory ----
    def list_theory(self, slug: str, level: str = "") -> list[TheoryBlock]:
        with self._sessions() as s:
            q = (s.query(TheoryModel).filter_by(topic_slug=slug)
                 .order_by(TheoryModel.order_index, TheoryModel.created_at))
            if level:
                q = q.filter(TheoryModel.level == level)
            return [_th_to_domain(m) for m in q.all()]

    def save_theory(self, block: TheoryBlock) -> None:
        with self._sessions() as s:
            m = s.get(TheoryModel, block.id)
            payload = dict(topic_slug=block.topic_slug, level=block.level,
                           title=block.title, content=block.content,
                           order_index=block.order_index,
                           created_at=block.created_at)
            if m:
                for k, v in payload.items():
                    setattr(m, k, v)
            else:
                s.add(TheoryModel(id=block.id, **payload))
            s.commit()

    def delete_theory(self, block_id: str) -> bool:
        with self._sessions() as s:
            m = s.get(TheoryModel, block_id)
            if not m:
                return False
            s.delete(m)
            s.commit()
            return True

    # ---- questions ----
    def list_questions(self, slug: str, qtype: str = "",
                       level: str = "") -> list[BankQuestion]:
        with self._sessions() as s:
            q = (s.query(BankQuestionModel).filter_by(topic_slug=slug)
                 .order_by(BankQuestionModel.created_at))
            if qtype:
                q = q.filter(BankQuestionModel.qtype == qtype)
            if level:
                q = q.filter(BankQuestionModel.level == level)
            return [_q_to_domain(m) for m in q.all()]

    def save_question(self, question: BankQuestion) -> None:
        with self._sessions() as s:
            m = s.get(BankQuestionModel, question.id)
            payload = dict(
                topic_slug=question.topic_slug, qtype=question.qtype,
                level=question.level, skill_tag=question.skill_tag,
                prompt=question.prompt,
                choices=json.dumps(list(question.choices)) if question.choices else None,
                answer_index=question.answer_index,
                rubric=json.dumps(question.rubric) if question.rubric else None,
                created_at=question.created_at,
            )
            if m:
                for k, v in payload.items():
                    setattr(m, k, v)
            else:
                s.add(BankQuestionModel(id=question.id, **payload))
            s.commit()

    def delete_question(self, question_id: str) -> bool:
        with self._sessions() as s:
            m = s.get(BankQuestionModel, question_id)
            if not m:
                return False
            s.delete(m)
            s.commit()
            return True
