"""Inbound adapter (HTTP): curriculum router.

Public (no auth): domains, modules, lessons, lesson detail.
Auth: study plans (create / mine / advance) and task status updates.
Admin only: create/update/delete domains, modules, lessons, questions.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel

from app.api.v1.auth import _domain_error, current_user_id, require_admin
from app.domain import question_generator as qgen
from app.domain.user import DomainError

router = APIRouter(prefix="", tags=["curriculum"])


class DomainCreateRequest(BaseModel):
    slug: str
    name: str
    description: str = ""
    icon: str = ""
    category: str = "tech-domain"
    order_index: int = 0
    is_active: bool = True


class DomainUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    icon: str | None = None
    category: str | None = None
    order_index: int | None = None
    is_active: bool | None = None


class ModuleCreateRequest(BaseModel):
    slug: str
    name: str
    description: str = ""
    order_index: int = 0
    estimated_days: int = 7


class LessonCreateRequest(BaseModel):
    slug: str
    title: str
    content: str = ""
    order_index: int = 0
    estimated_minutes: int = 30
    has_visual: bool = False


class QuestionCreateRequest(BaseModel):
    domain_slug: str
    qtype: str
    prompt: str
    difficulty: int = 1
    module_slug: str = ""
    lesson_id: str | None = None
    choices: list[str] | None = None
    answer_index: int | None = None
    explanation: str = ""
    company_tags: list[str] | None = None


class PlanCreateRequest(BaseModel):
    domain_slug: str
    start_level: str
    total_days: int


class TaskStatusRequest(BaseModel):
    status: str


class GenerateQuestionsRequest(BaseModel):
    domain_slug: str
    module_slug: str = ""
    count: int = 50
    seed: int = 0
    difficulty_min: int = 1
    difficulty_max: int = 10


def _svc(request: Request):
    return request.app.state.curriculum_service


# ---- public ----
@router.get("/curriculum/domains")
def list_domains(request: Request, category: str = Query(default="")):
    try:
        return {"domains": _svc(request).list_domains(category)}
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/curriculum/companies")
def list_companies(request: Request):
    """All companies with tagged-question counts."""
    try:
        return {"companies": _svc(request).list_companies()}
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/curriculum/companies/{name}/questions")
def questions_by_company(name: str, request: Request,
                         domain: str = Query(default=""),
                         limit: int = Query(default=50, ge=1, le=200)):
    """Questions a company asks — e.g. 'Amazon ne ye questions puche hain'."""
    try:
        return {"company": name.strip().lower(),
                "questions": _svc(request).get_questions_by_company(
                    name, domain, limit)}
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/curriculum/domains/{slug}")
def get_domain(slug: str, request: Request):
    try:
        return _svc(request).get_domain(slug)
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/curriculum/domains/{slug}/modules")
def list_modules(slug: str, request: Request):
    try:
        return {"modules": _svc(request).list_modules(slug)}
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/curriculum/modules/{module_id}/lessons")
def list_lessons(module_id: str, request: Request):
    try:
        return {"lessons": _svc(request).list_lessons(module_id)}
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/curriculum/lessons/{lesson_id}")
def get_lesson_detail(lesson_id: str, request: Request):
    try:
        return _svc(request).get_lesson_detail(lesson_id)
    except DomainError as exc:
        raise _domain_error(exc)


# ---- auth (user plans) ----
@router.post("/curriculum/plans", status_code=201)
def create_plan(body: PlanCreateRequest, request: Request,
                user_id: str = Depends(current_user_id)):
    try:
        plan = _svc(request).create_study_plan(
            user_id, body.domain_slug, body.start_level, body.total_days)
        # Auto-schedule weekly tests for the plan duration.
        try:
            weekly = request.app.state.weekly_test_service
            plan["weekly_tests"] = weekly.schedule_for_plan(
                user_id, body.domain_slug, plan["id"], body.total_days)
        except Exception:
            plan["weekly_tests"] = []
        return plan
    except DomainError as exc:
        raise _domain_error(exc)


@router.get("/curriculum/plans/mine")
def my_plans(request: Request, user_id: str = Depends(current_user_id)):
    return {"plans": _svc(request).my_plans(user_id)}


@router.patch("/curriculum/tasks/{task_id}")
def update_task(task_id: str, body: TaskStatusRequest, request: Request,
                user_id: str = Depends(current_user_id)):
    try:
        result = _svc(request).update_task(user_id, task_id, body.status)
        if body.status == "done":
            streak = request.app.state.streak_service.record_activity(user_id)
            coins = request.app.state.coin_service
            coins.earn(user_id, "daily_task")
            coins.earn_streak_day(user_id, streak["current_streak"])
            milestone = coins.earn_milestone(user_id, streak["current_streak"])
            result["coins_earned"] = True
            if milestone:
                result["milestone_bonus"] = milestone["earned"]
        return result
    except DomainError as exc:
        raise _domain_error(exc)


@router.post("/curriculum/plans/{plan_id}/advance")
def advance_day(plan_id: str, request: Request,
                user_id: str = Depends(current_user_id)):
    try:
        return _svc(request).advance_day(user_id, plan_id)
    except DomainError as exc:
        raise _domain_error(exc)


# ---- admin ----
@router.post("/curriculum/domains", status_code=201)
def create_domain(body: DomainCreateRequest, request: Request,
                  _admin: str = Depends(require_admin)):
    try:
        return _svc(request).create_domain(
            body.slug, body.name, body.description, body.icon,
            body.category, body.order_index, body.is_active)
    except DomainError as exc:
        raise _domain_error(exc)


@router.put("/curriculum/domains/{slug}")
def update_domain(slug: str, body: DomainUpdateRequest, request: Request,
                  _admin: str = Depends(require_admin)):
    try:
        fields = {k: v for k, v in body.model_dump().items() if v is not None}
        return _svc(request).update_domain(slug, **fields)
    except DomainError as exc:
        raise _domain_error(exc)


@router.delete("/curriculum/domains/{slug}", status_code=204)
def delete_domain(slug: str, request: Request,
                  _admin: str = Depends(require_admin)):
    try:
        _svc(request).delete_domain(slug)
    except DomainError as exc:
        raise _domain_error(exc)
    return None


@router.post("/curriculum/domains/{slug}/modules", status_code=201)
def create_module(slug: str, body: ModuleCreateRequest, request: Request,
                  _admin: str = Depends(require_admin)):
    try:
        return _svc(request).create_module(
            slug, body.slug, body.name, body.description,
            body.order_index, body.estimated_days)
    except DomainError as exc:
        raise _domain_error(exc)


@router.delete("/curriculum/modules/{module_id}", status_code=204)
def delete_module(module_id: str, request: Request,
                  _admin: str = Depends(require_admin)):
    try:
        _svc(request).delete_module(module_id)
    except DomainError as exc:
        raise _domain_error(exc)
    return None


@router.post("/curriculum/modules/{module_id}/lessons", status_code=201)
def create_lesson(module_id: str, body: LessonCreateRequest, request: Request,
                  _admin: str = Depends(require_admin)):
    try:
        return _svc(request).create_lesson(
            module_id, body.slug, body.title, body.content,
            body.order_index, body.estimated_minutes, body.has_visual)
    except DomainError as exc:
        raise _domain_error(exc)


@router.delete("/curriculum/lessons/{lesson_id}", status_code=204)
def delete_lesson(lesson_id: str, request: Request,
                  _admin: str = Depends(require_admin)):
    try:
        _svc(request).delete_lesson(lesson_id)
    except DomainError as exc:
        raise _domain_error(exc)
    return None


@router.post("/curriculum/questions", status_code=201)
def add_question(body: QuestionCreateRequest, request: Request,
                 _admin: str = Depends(require_admin)):
    try:
        return _svc(request).add_question(
            body.domain_slug, body.qtype, body.prompt, body.difficulty,
            body.module_slug, body.lesson_id, body.choices,
            body.answer_index, body.explanation, body.company_tags)
    except DomainError as exc:
        raise _domain_error(exc)


@router.delete("/curriculum/questions/{qid}", status_code=204)
def delete_question(qid: str, request: Request,
                    _admin: str = Depends(require_admin)):
    try:
        _svc(request).delete_question(qid)
    except DomainError as exc:
        raise _domain_error(exc)
    return None


@router.post("/curriculum/generate-questions", status_code=201)
def generate_questions_ep(body: GenerateQuestionsRequest, request: Request,
                          _admin: str = Depends(require_admin)):
    """Admin: deterministically generate N questions for a domain/module
    (dsa/os/dbms) and save them to curriculum_questions."""
    try:
        if not 1 <= body.count <= 500:
            raise DomainError("count must be 1-500")
        qs = qgen.generate_questions(
            body.domain_slug, seed=body.seed, count=body.count,
            difficulty_range=(body.difficulty_min, body.difficulty_max),
        )
    except DomainError as exc:
        raise _domain_error(exc)
    svc = _svc(request)
    saved = 0
    for q in qs:
        try:
            svc.add_question(
                body.domain_slug, q["qtype"], q["prompt"], q["difficulty"],
                body.module_slug, None, q["choices"], q["answer_index"],
                q["explanation"], q["company_tags"],
            )
            saved += 1
        except DomainError as exc:
            raise _domain_error(exc)
    return {"generated": saved, "domain_slug": body.domain_slug,
            "module_slug": body.module_slug, "seed": body.seed}


@router.get("/curriculum/generate-capacity")
def generate_capacity(domain_slug: str = Query(default=""),
                      _admin: str = Depends(require_admin)):
    """Admin: how many unique questions the generator can produce per domain."""
    try:
        if domain_slug:
            return {"domain_slug": domain_slug,
                    "capacity": qgen.questions_generatable(domain_slug)}
        return {"capacity": {d: qgen.questions_generatable(d)
                             for d in qgen.SUPPORTED_DOMAINS}}
    except DomainError as exc:
        raise _domain_error(exc)
