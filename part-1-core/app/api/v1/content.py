"""Inbound adapter (HTTP): content CMS router.

Public (no auth): list topics, topic detail, theory blocks.
Admin only: create/update/delete topics, theory, questions, link import.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel

from app.adapters.inbound.link_importer import import_from_url
from app.api.v1.auth import _domain_error, require_admin
from app.domain.user import DomainError

router = APIRouter(prefix="", tags=["content"])


class TopicCreateRequest(BaseModel):
    slug: str
    name: str
    description: str = ""
    icon: str = ""
    color: str = "#8b5cf6"


class TopicUpdateRequest(BaseModel):
    name: str = ""
    description: str = ""
    icon: str = ""
    color: str = ""
    is_active: bool | None = None


class TheoryCreateRequest(BaseModel):
    level: str
    title: str
    content: str
    order_index: int = 0


class QuestionCreateRequest(BaseModel):
    qtype: str
    level: str
    prompt: str
    skill_tag: str = ""
    choices: list[str] | None = None
    answer_index: int | None = None
    rubric: dict | None = None


class ImportUrlRequest(BaseModel):
    url: str


def _svc(request: Request):
    return request.app.state.content_service


# ---- public ----
@router.get("/content/topics")
def list_topics(request: Request,
                active_only: bool = Query(default=True)):
    return {"topics": _svc(request).list_topics(active_only)}


@router.get("/content/topics/{slug}")
def get_topic(slug: str, request: Request):
    try:
        return _svc(request).get_topic(slug)
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/content/topics/{slug}/theory")
def list_theory(slug: str, request: Request,
                level: str = Query(default="")):
    try:
        return {"theory": _svc(request).list_theory(slug, level)}
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/content/topics/{slug}/questions")
def list_questions(slug: str, request: Request,
                   qtype: str = Query(default=""),
                   level: str = Query(default="")):
    try:
        return {"questions": _svc(request).list_questions(slug, qtype, level)}
    except DomainError as exc:
        raise _domain_error(exc)


# ---- admin ----
@router.post("/content/topics", status_code=201)
def create_topic(body: TopicCreateRequest, request: Request,
                 _admin: str = Depends(require_admin)):
    try:
        return _svc(request).create_topic(
            body.slug, body.name, body.description, body.icon, body.color)
    except DomainError as exc:
        raise _domain_error(exc)


@router.put("/content/topics/{slug}")
def update_topic(slug: str, body: TopicUpdateRequest, request: Request,
                 _admin: str = Depends(require_admin)):
    try:
        fields = body.model_dump()
        if fields.get("is_active") is None:
            fields.pop("is_active")
        return _svc(request).update_topic(slug, **fields)
    except DomainError as exc:
        raise _domain_error(exc)


@router.delete("/content/topics/{slug}", status_code=204)
def delete_topic(slug: str, request: Request,
                 _admin: str = Depends(require_admin)):
    try:
        _svc(request).delete_topic(slug)
    except DomainError as exc:
        raise _domain_error(exc)
    return None


@router.post("/content/topics/{slug}/theory", status_code=201)
def add_theory(slug: str, body: TheoryCreateRequest, request: Request,
               _admin: str = Depends(require_admin)):
    try:
        return _svc(request).add_theory(
            slug, body.level, body.title, body.content, body.order_index)
    except DomainError as exc:
        raise _domain_error(exc)


@router.delete("/content/theory/{block_id}", status_code=204)
def delete_theory(block_id: str, request: Request,
                  _admin: str = Depends(require_admin)):
    try:
        _svc(request).delete_theory(block_id)
    except DomainError as exc:
        raise _domain_error(exc)
    return None


@router.post("/content/topics/{slug}/questions", status_code=201)
def add_question(slug: str, body: QuestionCreateRequest, request: Request,
                 _admin: str = Depends(require_admin)):
    try:
        return _svc(request).add_question(
            slug, body.qtype, body.level, body.prompt, body.skill_tag,
            body.choices, body.answer_index, body.rubric)
    except DomainError as exc:
        raise _domain_error(exc)


@router.delete("/content/questions/{question_id}", status_code=204)
def delete_question(question_id: str, request: Request,
                    _admin: str = Depends(require_admin)):
    try:
        _svc(request).delete_question(question_id)
    except DomainError as exc:
        raise _domain_error(exc)
    return None


@router.post("/content/import-url")
def import_url(body: ImportUrlRequest, request: Request,
               _admin: str = Depends(require_admin)):
    # Preview only — admin reviews/edits before saving as theory.
    return import_from_url(body.url)
