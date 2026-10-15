"""Inbound adapter: implements content CMS business logic."""
from __future__ import annotations

import uuid

from app.domain.content import (
    BankQuestion,
    DomainError,
    TheoryBlock,
    Topic,
    validate_bank_question,
    validate_level,
    validate_qtype,
    validate_slug,
    validate_theory,
    validate_topic,
)


class ContentServiceImpl:
    def __init__(self, repo) -> None:
        self._repo = repo

    # ---- topics ----
    def list_topics(self, active_only: bool = True) -> list[dict]:
        return [self._topic_out(t) for t in self._repo.list_topics(active_only)]

    def get_topic(self, slug: str) -> dict:
        slug = validate_slug(slug)
        topic = self._repo.get_topic(slug)
        if not topic:
            raise DomainError("topic not found")
        return self._topic_out(topic, counts=self._repo.count_questions(slug))

    def create_topic(self, slug: str, name: str, description: str = "",
                     icon: str = "", color: str = "#8b5cf6") -> dict:
        slug = validate_slug(slug)
        validate_topic(name, description, icon, color)
        if self._repo.get_topic(slug):
            raise DomainError("topic slug already exists")
        topic = Topic(id=uuid.uuid4().hex, slug=slug, name=name.strip(),
                      description=(description or "").strip(),
                      icon=(icon or "").strip(), color=color or "#8b5cf6")
        self._repo.save_topic(topic)
        return self._topic_out(topic)

    def update_topic(self, slug: str, **fields) -> dict:
        slug = validate_slug(slug)
        topic = self._repo.get_topic(slug)
        if not topic:
            raise DomainError("topic not found")
        name = fields.get("name", topic.name)
        validate_topic(name)
        updated = Topic(
            id=topic.id, slug=topic.slug, name=name.strip(),
            description=str(fields.get("description", topic.description or "")),
            icon=str(fields.get("icon", topic.icon or "")),
            color=str(fields.get("color", topic.color or "#8b5cf6")),
            is_active=bool(fields.get("is_active", topic.is_active)),
            created_at=topic.created_at,
        )
        self._repo.save_topic(updated)
        return self._topic_out(updated)

    def delete_topic(self, slug: str) -> None:
        slug = validate_slug(slug)
        if not self._repo.delete_topic(slug):
            raise DomainError("topic not found")

    # ---- theory ----
    def list_theory(self, slug: str, level: str = "") -> list[dict]:
        slug = validate_slug(slug)
        if not self._repo.get_topic(slug):
            raise DomainError("topic not found")
        if level:
            validate_level(level)
        return [self._theory_out(b) for b in self._repo.list_theory(slug, level)]

    def add_theory(self, slug: str, level: str, title: str, content: str,
                   order_index: int = 0) -> dict:
        slug = validate_slug(slug)
        level = validate_level(level)
        validate_theory(title, content)
        if not self._repo.get_topic(slug):
            raise DomainError("topic not found")
        block = TheoryBlock(id=uuid.uuid4().hex, topic_slug=slug, level=level,
                            title=title.strip(), content=content,
                            order_index=int(order_index))
        self._repo.save_theory(block)
        return self._theory_out(block)

    def delete_theory(self, block_id: str) -> None:
        if not self._repo.delete_theory(block_id):
            raise DomainError("theory block not found")

    # ---- questions ----
    def list_questions(self, slug: str, qtype: str = "",
                       level: str = "") -> list[dict]:
        slug = validate_slug(slug)
        if not self._repo.get_topic(slug):
            raise DomainError("topic not found")
        if qtype:
            validate_qtype(qtype)
        if level:
            validate_level(level)
        return [self._question_out(q)
                for q in self._repo.list_questions(slug, qtype, level)]

    def add_question(self, slug: str, qtype: str, level: str, prompt: str,
                     skill_tag: str = "", choices: list[str] | None = None,
                     answer_index: int | None = None,
                     rubric: dict | None = None) -> dict:
        slug = validate_slug(slug)
        qtype = validate_qtype(qtype)
        level = validate_level(level)
        choices_t = tuple(choices or ())
        validate_bank_question(qtype, prompt, choices_t, answer_index)
        if not self._repo.get_topic(slug):
            raise DomainError("topic not found")
        question = BankQuestion(
            id=uuid.uuid4().hex, topic_slug=slug, qtype=qtype, level=level,
            prompt=prompt.strip(), skill_tag=(skill_tag or "").strip(),
            choices=choices_t, answer_index=answer_index,
            rubric=dict(rubric or {}),
        )
        self._repo.save_question(question)
        return self._question_out(question)

    def delete_question(self, question_id: str) -> None:
        if not self._repo.delete_question(question_id):
            raise DomainError("question not found")

    # ---- serializers ----
    @staticmethod
    def _topic_out(t: Topic, counts: dict | None = None) -> dict:
        out = {"id": t.id, "slug": t.slug, "name": t.name,
               "description": t.description, "icon": t.icon, "color": t.color,
               "is_active": t.is_active,
               "created_at": t.created_at.isoformat()}
        if counts is not None:
            out["question_counts"] = counts
        return out

    @staticmethod
    def _theory_out(b: TheoryBlock) -> dict:
        return {"id": b.id, "topic_slug": b.topic_slug, "level": b.level,
                "title": b.title, "content": b.content,
                "order_index": b.order_index,
                "created_at": b.created_at.isoformat()}

    @staticmethod
    def _question_out(q: BankQuestion) -> dict:
        return {"id": q.id, "topic_slug": q.topic_slug, "qtype": q.qtype,
                "level": q.level, "prompt": q.prompt, "skill_tag": q.skill_tag,
                "choices": list(q.choices), "answer_index": q.answer_index,
                "rubric": q.rubric, "created_at": q.created_at.isoformat()}
