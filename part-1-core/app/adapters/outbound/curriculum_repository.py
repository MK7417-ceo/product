"""Outbound adapter: curriculum repository (SQLAlchemy)."""
from __future__ import annotations

import json
from datetime import date, datetime, timezone
from typing import Callable

from sqlalchemy.orm import Session

from app.adapters.outbound.models import (
    CurriculumDomainModel,
    CurriculumLessonModel,
    CurriculumModuleModel,
    CurriculumQuestionModel,
    DailyTaskModel,
    StudyPlanModel,
)
from app.domain.curriculum import (
    CurriculumDomain,
    CurriculumLesson,
    CurriculumModule,
    CurriculumQuestion,
    DailyTask,
    StudyPlan,
)


def _d_to_domain(m: CurriculumDomainModel) -> CurriculumDomain:
    return CurriculumDomain(id=m.id, slug=m.slug, name=m.name, icon=m.icon,
                            description=m.description, category=m.category,
                            order_index=m.order_index, is_active=m.is_active)


def _m_to_domain(m: CurriculumModuleModel) -> CurriculumModule:
    return CurriculumModule(id=m.id, domain_slug=m.domain_slug, slug=m.slug,
                            name=m.name, description=m.description,
                            order_index=m.order_index,
                            estimated_days=m.estimated_days)


def _l_to_domain(m: CurriculumLessonModel) -> CurriculumLesson:
    return CurriculumLesson(id=m.id, module_id=m.module_id, slug=m.slug,
                            title=m.title, content=m.content,
                            order_index=m.order_index,
                            estimated_minutes=m.estimated_minutes,
                            has_visual=m.has_visual)


def _q_to_domain(m: CurriculumQuestionModel) -> CurriculumQuestion:
    return CurriculumQuestion(
        id=m.id, domain_slug=m.domain_slug, module_slug=m.module_slug or "",
        lesson_id=m.lesson_id, difficulty=m.difficulty, qtype=m.qtype,
        prompt=m.prompt,
        choices=tuple(json.loads(m.choices)) if m.choices else (),
        answer_index=m.answer_index, explanation=m.explanation or "",
        company_tags=tuple(json.loads(m.company_tags)) if m.company_tags else (),
        created_at=m.created_at,
    )


def _p_to_domain(m: StudyPlanModel) -> StudyPlan:
    return StudyPlan(id=m.id, user_id=m.user_id, domain_slug=m.domain_slug,
                     start_level=m.start_level, total_days=m.total_days,
                     current_day=m.current_day, status=m.status,
                     created_at=m.created_at)


def _t_to_domain(m: DailyTaskModel) -> DailyTask:
    due = m.due_date
    due_date = due.date() if isinstance(due, datetime) else due
    return DailyTask(
        id=m.id, plan_id=m.plan_id, day_number=m.day_number,
        lesson_id=m.lesson_id, task_type=m.task_type, title=m.title,
        description=m.description or "",
        question_ids=tuple(json.loads(m.question_ids)) if m.question_ids else (),
        status=m.status, due_date=due_date,
    )


def _due_to_model(due: date | datetime | None) -> datetime | None:
    if due is None:
        return None
    if isinstance(due, datetime):
        return due if due.tzinfo else due.replace(tzinfo=timezone.utc)
    return datetime(due.year, due.month, due.day, tzinfo=timezone.utc)


class SqlAlchemyCurriculumRepository:
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._sessions = session_factory

    # ---- domains ----
    def list_domains(self, active_only: bool = True,
                     category: str = "") -> list[CurriculumDomain]:
        with self._sessions() as s:
            q = (s.query(CurriculumDomainModel)
                 .order_by(CurriculumDomainModel.order_index,
                           CurriculumDomainModel.slug))
            if active_only:
                q = q.filter(CurriculumDomainModel.is_active.is_(True))
            if category:
                q = q.filter(CurriculumDomainModel.category == category)
            return [_d_to_domain(m) for m in q.all()]

    def get_domain(self, slug: str) -> CurriculumDomain | None:
        with self._sessions() as s:
            m = (s.query(CurriculumDomainModel)
                 .filter_by(slug=slug).one_or_none())
            return _d_to_domain(m) if m else None

    def save_domain(self, domain: CurriculumDomain) -> None:
        with self._sessions() as s:
            m = s.get(CurriculumDomainModel, domain.id)
            payload = dict(slug=domain.slug, name=domain.name, icon=domain.icon,
                           description=domain.description, category=domain.category,
                           order_index=domain.order_index,
                           is_active=domain.is_active)
            if m:
                for k, v in payload.items():
                    setattr(m, k, v)
            else:
                s.add(CurriculumDomainModel(id=domain.id, **payload))
            s.commit()

    def delete_domain(self, slug: str) -> bool:
        with self._sessions() as s:
            m = (s.query(CurriculumDomainModel)
                 .filter_by(slug=slug).one_or_none())
            if not m:
                return False
            s.delete(m)  # FK ondelete=CASCADE removes modules + lessons
            s.commit()
            return True

    # ---- modules ----
    def list_modules(self, domain_slug: str) -> list[CurriculumModule]:
        with self._sessions() as s:
            q = (s.query(CurriculumModuleModel)
                 .filter_by(domain_slug=domain_slug)
                 .order_by(CurriculumModuleModel.order_index,
                           CurriculumModuleModel.slug))
            return [_m_to_domain(m) for m in q.all()]

    def get_module(self, module_id: str) -> CurriculumModule | None:
        with self._sessions() as s:
            m = s.get(CurriculumModuleModel, module_id)
            return _m_to_domain(m) if m else None

    def save_module(self, module: CurriculumModule) -> None:
        with self._sessions() as s:
            m = s.get(CurriculumModuleModel, module.id)
            payload = dict(domain_slug=module.domain_slug, slug=module.slug,
                           name=module.name, description=module.description,
                           order_index=module.order_index,
                           estimated_days=module.estimated_days)
            if m:
                for k, v in payload.items():
                    setattr(m, k, v)
            else:
                s.add(CurriculumModuleModel(id=module.id, **payload))
            s.commit()

    def delete_module(self, module_id: str) -> bool:
        with self._sessions() as s:
            m = s.get(CurriculumModuleModel, module_id)
            if not m:
                return False
            s.delete(m)  # FK ondelete=CASCADE removes lessons
            s.commit()
            return True

    # ---- lessons ----
    def list_lessons(self, module_id: str) -> list[CurriculumLesson]:
        with self._sessions() as s:
            q = (s.query(CurriculumLessonModel)
                 .filter_by(module_id=module_id)
                 .order_by(CurriculumLessonModel.order_index,
                           CurriculumLessonModel.slug))
            return [_l_to_domain(m) for m in q.all()]

    def get_lesson(self, lesson_id: str) -> CurriculumLesson | None:
        with self._sessions() as s:
            m = s.get(CurriculumLessonModel, lesson_id)
            return _l_to_domain(m) if m else None

    def save_lesson(self, lesson: CurriculumLesson) -> None:
        with self._sessions() as s:
            m = s.get(CurriculumLessonModel, lesson.id)
            payload = dict(module_id=lesson.module_id, slug=lesson.slug,
                           title=lesson.title, content=lesson.content,
                           order_index=lesson.order_index,
                           estimated_minutes=lesson.estimated_minutes,
                           has_visual=lesson.has_visual)
            if m:
                for k, v in payload.items():
                    setattr(m, k, v)
            else:
                s.add(CurriculumLessonModel(id=lesson.id, **payload))
            s.commit()

    def delete_lesson(self, lesson_id: str) -> bool:
        with self._sessions() as s:
            m = s.get(CurriculumLessonModel, lesson_id)
            if not m:
                return False
            s.delete(m)
            s.commit()
            return True

    # ---- questions (difficulty 1->10 gradual ramp) ----
    def list_questions(self, domain_slug: str, module_slug: str = "",
                       max_difficulty: int | None = None
                       ) -> list[CurriculumQuestion]:
        with self._sessions() as s:
            q = (s.query(CurriculumQuestionModel)
                 .filter_by(domain_slug=domain_slug)
                 .order_by(CurriculumQuestionModel.difficulty,
                           CurriculumQuestionModel.created_at))
            if module_slug:
                q = q.filter(CurriculumQuestionModel.module_slug == module_slug)
            if max_difficulty is not None:
                q = q.filter(
                    CurriculumQuestionModel.difficulty <= max_difficulty)
            return [_q_to_domain(m) for m in q.all()]

    def get_question(self, qid: str) -> CurriculumQuestion | None:
        with self._sessions() as s:
            m = s.get(CurriculumQuestionModel, qid)
            return _q_to_domain(m) if m else None

    def get_questions_by_ids(self, ids: list[str]) -> list[CurriculumQuestion]:
        """Fetch questions by id list (for weekly tests)."""
        if not ids:
            return []
        with self._sessions() as s:
            rows = (s.query(CurriculumQuestionModel)
                    .filter(CurriculumQuestionModel.id.in_(ids)).all())
            return [_q_to_domain(m) for m in rows]

    def get_questions_by_company(self, company: str,
                                 domain_slug: str = "",
                                 limit: int = 50) -> list[CurriculumQuestion]:
        """Questions tagged with a company (case-insensitive).

        company_tags is stored as JSON text, so we filter in Python
        after a domain-scoped query — simple, portable across DBs.
        """
        want = company.strip().lower()
        with self._sessions() as s:
            q = (s.query(CurriculumQuestionModel)
                 .order_by(CurriculumQuestionModel.difficulty,
                           CurriculumQuestionModel.created_at))
            if domain_slug:
                q = q.filter(
                    CurriculumQuestionModel.domain_slug == domain_slug)
            out: list[CurriculumQuestion] = []
            for m in q.all():
                try:
                    tags = [str(t).lower() for t in json.loads(m.company_tags or "[]")]
                except Exception:
                    tags = []
                if want in tags:
                    out.append(_q_to_domain(m))
                    if len(out) >= limit:
                        break
            return out

    def list_companies(self) -> list[dict]:
        """All company tags in use with question counts."""
        counts: dict[str, int] = {}
        with self._sessions() as s:
            rows = s.query(CurriculumQuestionModel.company_tags).all()
            for (raw,) in rows:
                try:
                    tags = json.loads(raw or "[]")
                except Exception:
                    continue
                for t in tags:
                    key = str(t).strip().lower()
                    if key:
                        counts[key] = counts.get(key, 0) + 1
        return [{"name": k, "questions": v}
                for k, v in sorted(counts.items(), key=lambda kv: -kv[1])]

    def save_question(self, question: CurriculumQuestion) -> None:
        with self._sessions() as s:
            m = s.get(CurriculumQuestionModel, question.id)
            payload = dict(
                domain_slug=question.domain_slug,
                module_slug=question.module_slug or "",
                lesson_id=question.lesson_id,
                difficulty=question.difficulty, qtype=question.qtype,
                prompt=question.prompt,
                choices=(json.dumps(list(question.choices))
                         if question.choices else None),
                answer_index=question.answer_index,
                explanation=question.explanation or "",
                company_tags=json.dumps(list(question.company_tags)),
                created_at=question.created_at,
            )
            if m:
                for k, v in payload.items():
                    setattr(m, k, v)
            else:
                s.add(CurriculumQuestionModel(id=question.id, **payload))
            s.commit()

    def delete_question(self, qid: str) -> bool:
        with self._sessions() as s:
            m = s.get(CurriculumQuestionModel, qid)
            if not m:
                return False
            s.delete(m)
            s.commit()
            return True

    # ---- study plans ----
    def create_plan(self, plan: StudyPlan) -> None:
        with self._sessions() as s:
            s.add(StudyPlanModel(
                id=plan.id, user_id=plan.user_id, domain_slug=plan.domain_slug,
                start_level=plan.start_level, total_days=plan.total_days,
                current_day=plan.current_day, status=plan.status,
                created_at=plan.created_at))
            s.commit()

    def get_plan(self, plan_id: str) -> StudyPlan | None:
        with self._sessions() as s:
            m = s.get(StudyPlanModel, plan_id)
            return _p_to_domain(m) if m else None

    def list_user_plans(self, user_id: str) -> list[StudyPlan]:
        with self._sessions() as s:
            q = (s.query(StudyPlanModel).filter_by(user_id=user_id)
                 .order_by(StudyPlanModel.created_at.desc()))
            return [_p_to_domain(m) for m in q.all()]

    def update_plan_current_day(self, plan_id: str, day: int) -> None:
        with self._sessions() as s:
            m = s.get(StudyPlanModel, plan_id)
            if m:
                m.current_day = int(day)
                s.commit()

    def update_plan_status(self, plan_id: str, status: str) -> None:
        with self._sessions() as s:
            m = s.get(StudyPlanModel, plan_id)
            if m:
                m.status = status
                s.commit()

    # ---- daily tasks ----
    def create_task(self, task: DailyTask) -> None:
        with self._sessions() as s:
            s.add(DailyTaskModel(
                id=task.id, plan_id=task.plan_id, day_number=task.day_number,
                lesson_id=task.lesson_id, task_type=task.task_type,
                title=task.title, description=task.description,
                question_ids=json.dumps(list(task.question_ids)),
                status=task.status, due_date=_due_to_model(task.due_date)))
            s.commit()

    def list_plan_tasks(self, plan_id: str,
                        day_number: int | None = None) -> list[DailyTask]:
        with self._sessions() as s:
            q = (s.query(DailyTaskModel).filter_by(plan_id=plan_id)
                 .order_by(DailyTaskModel.day_number,
                           DailyTaskModel.task_type, DailyTaskModel.title))
            if day_number is not None:
                q = q.filter(DailyTaskModel.day_number == day_number)
            return [_t_to_domain(m) for m in q.all()]

    def get_task(self, task_id: str) -> DailyTask | None:
        with self._sessions() as s:
            m = s.get(DailyTaskModel, task_id)
            return _t_to_domain(m) if m else None

    def update_task_status(self, task_id: str, status: str) -> bool:
        with self._sessions() as s:
            m = s.get(DailyTaskModel, task_id)
            if not m:
                return False
            m.status = status
            s.commit()
            return True
