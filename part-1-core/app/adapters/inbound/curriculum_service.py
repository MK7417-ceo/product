"""Inbound adapter: implements curriculum business logic.

Curriculum = domains -> modules -> lessons -> questions (difficulty 1-10).
Study plans generate day-wise daily tasks with a gradual difficulty ramp.
"""
from __future__ import annotations

import uuid
from datetime import date, timedelta

from app.domain.curriculum import (
    CurriculumDomain,
    CurriculumLesson,
    CurriculumModule,
    CurriculumQuestion,
    DailyTask,
    DomainError,
    StudyPlan,
    difficulty_for_day,
    plan_task_types_for_day,
    validate_category,
    validate_curriculum_question,
    validate_difficulty,
    validate_domain,
    validate_lesson,
    validate_module,
    validate_qtype,
    validate_slug,
    validate_start_level,
    validate_study_plan,
    validate_task_status,
)


class CurriculumServiceImpl:
    def __init__(self, repo) -> None:
        self._repo = repo

    # ---- domains ----
    def list_domains(self, category: str = "") -> list[dict]:
        if category:
            category = validate_category(category)
        return [self._domain_out(d) for d in self._repo.list_domains(True, category)]

    def get_domain(self, slug: str) -> dict:
        slug = validate_slug(slug)
        domain = self._repo.get_domain(slug)
        if not domain:
            raise DomainError("domain not found")
        return self._domain_out(
            domain, module_count=len(self._repo.list_modules(slug)))

    def create_domain(self, slug: str, name: str, description: str = "",
                      icon: str = "", category: str = "tech-domain",
                      order_index: int = 0, is_active: bool = True) -> dict:
        slug = validate_slug(slug)
        category = validate_category(category)
        validate_domain(name, category)
        if self._repo.get_domain(slug):
            raise DomainError("domain slug already exists")
        domain = CurriculumDomain(
            id=uuid.uuid4().hex, slug=slug, name=name.strip(),
            icon=(icon or "").strip(), description=(description or "").strip(),
            category=category, order_index=int(order_index or 0),
            is_active=bool(is_active))
        self._repo.save_domain(domain)
        return self._domain_out(domain, module_count=0)

    def update_domain(self, slug: str, **fields) -> dict:
        slug = validate_slug(slug)
        domain = self._repo.get_domain(slug)
        if not domain:
            raise DomainError("domain not found")
        name = fields.get("name", domain.name)
        category = fields.get("category", domain.category)
        validate_domain(name, category)
        updated = CurriculumDomain(
            id=domain.id, slug=domain.slug, name=name.strip(),
            description=str(fields.get("description", domain.description or "")),
            icon=str(fields.get("icon", domain.icon or "")),
            category=category,
            order_index=int(fields.get("order_index", domain.order_index)),
            is_active=bool(fields.get("is_active", domain.is_active)),
        )
        self._repo.save_domain(updated)
        return self._domain_out(
            updated, module_count=len(self._repo.list_modules(slug)))

    def delete_domain(self, slug: str) -> None:
        slug = validate_slug(slug)
        if not self._repo.delete_domain(slug):
            raise DomainError("domain not found")

    # ---- modules ----
    def list_modules(self, domain_slug: str) -> list[dict]:
        domain_slug = validate_slug(domain_slug)
        if not self._repo.get_domain(domain_slug):
            raise DomainError("domain not found")
        return [self._module_out(m)
                for m in self._repo.list_modules(domain_slug)]

    def create_module(self, domain_slug: str, slug: str, name: str,
                      description: str = "", order_index: int = 0,
                      estimated_days: int = 7) -> dict:
        domain_slug = validate_slug(domain_slug)
        slug = validate_slug(slug)
        validate_module(name, estimated_days)
        if not self._repo.get_domain(domain_slug):
            raise DomainError("domain not found")
        if any(m.slug == slug for m in self._repo.list_modules(domain_slug)):
            raise DomainError("module slug already exists in this domain")
        module = CurriculumModule(
            id=uuid.uuid4().hex, domain_slug=domain_slug, slug=slug,
            name=name.strip(), description=(description or "").strip(),
            order_index=int(order_index or 0),
            estimated_days=int(estimated_days))
        self._repo.save_module(module)
        return self._module_out(module)

    def delete_module(self, module_id: str) -> None:
        if not self._repo.delete_module(module_id):
            raise DomainError("module not found")

    # ---- lessons ----
    def list_lessons(self, module_id: str) -> list[dict]:
        if not self._repo.get_module(module_id):
            raise DomainError("module not found")
        return [self._lesson_out(lesson)
                for lesson in self._repo.list_lessons(module_id)]

    def get_lesson_detail(self, lesson_id: str) -> dict:
        lesson = self._repo.get_lesson(lesson_id)
        if not lesson:
            raise DomainError("lesson not found")
        module = self._repo.get_module(lesson.module_id)
        domain_slug = module.domain_slug if module else ""
        questions = [
            q for q in self._repo.list_questions(domain_slug)
            if q.lesson_id == lesson.id
        ]
        out = self._lesson_out(lesson)
        out["questions"] = [self._question_out(q) for q in questions]
        return out

    def create_lesson(self, module_id: str, slug: str, title: str,
                      content: str = "", order_index: int = 0,
                      estimated_minutes: int = 30,
                      has_visual: bool = False) -> dict:
        slug = validate_slug(slug)
        validate_lesson(title, estimated_minutes)
        if not self._repo.get_module(module_id):
            raise DomainError("module not found")
        if any(lesson.slug == slug
               for lesson in self._repo.list_lessons(module_id)):
            raise DomainError("lesson slug already exists in this module")
        lesson = CurriculumLesson(
            id=uuid.uuid4().hex, module_id=module_id, slug=slug,
            title=title.strip(), content=content or "",
            order_index=int(order_index or 0),
            estimated_minutes=int(estimated_minutes),
            has_visual=bool(has_visual))
        self._repo.save_lesson(lesson)
        return self._lesson_out(lesson)

    def delete_lesson(self, lesson_id: str) -> None:
        if not self._repo.delete_lesson(lesson_id):
            raise DomainError("lesson not found")

    # ---- questions ----
    def add_question(self, domain_slug: str, qtype: str, prompt: str,
                     difficulty: int = 1, module_slug: str = "",
                     lesson_id: str | None = None,
                     choices: list[str] | None = None,
                     answer_index: int | None = None, explanation: str = "",
                     company_tags: list[str] | None = None) -> dict:
        domain_slug = validate_slug(domain_slug)
        qtype = validate_qtype(qtype)
        difficulty = validate_difficulty(difficulty)
        choices_t = tuple(choices or ())
        validate_curriculum_question(qtype, prompt, difficulty, choices_t,
                                     answer_index)
        if not self._repo.get_domain(domain_slug):
            raise DomainError("domain not found")
        if module_slug:
            module_slug = validate_slug(module_slug, "module_slug")
            if not any(m.slug == module_slug
                       for m in self._repo.list_modules(domain_slug)):
                raise DomainError("module not found in this domain")
        if lesson_id and not self._repo.get_lesson(lesson_id):
            raise DomainError("lesson not found")
        question = CurriculumQuestion(
            id=uuid.uuid4().hex, domain_slug=domain_slug,
            module_slug=module_slug, lesson_id=lesson_id,
            difficulty=difficulty, qtype=qtype, prompt=prompt.strip(),
            choices=choices_t, answer_index=answer_index,
            explanation=(explanation or "").strip(),
            company_tags=tuple(t.strip().lower() for t in (company_tags or ())
                               if t.strip()))
        self._repo.save_question(question)
        return self._question_out(question)

    def delete_question(self, qid: str) -> None:
        if not self._repo.delete_question(qid):
            raise DomainError("question not found")

    # ---- study plans ----
    def create_study_plan(self, user_id: str, domain_slug: str,
                          start_level: str, total_days: int) -> dict:
        domain_slug = validate_slug(domain_slug)
        start_level = validate_start_level(start_level)
        validate_study_plan(start_level, total_days)
        total_days = int(total_days)
        if not self._repo.get_domain(domain_slug):
            raise DomainError("domain not found")

        plan = StudyPlan(id=uuid.uuid4().hex, user_id=user_id,
                         domain_slug=domain_slug, start_level=start_level,
                         total_days=total_days, current_day=1, status="active")
        self._repo.create_plan(plan)

        # Gather the domain's lessons in module order for round-robin picking.
        lessons: list[CurriculumLesson] = []
        for module in self._repo.list_modules(domain_slug):
            lessons.extend(self._repo.list_lessons(module.id))

        tasks: list[DailyTask] = []
        for day in range(1, total_days + 1):
            tasks.extend(self._tasks_for_day(
                plan, day, lessons, domain_slug, start_level, total_days))
        return self._plan_out(plan, tasks=tasks)

    def my_plans(self, user_id: str) -> list[dict]:
        out = []
        for plan in self._repo.list_user_plans(user_id):
            out.append(self._plan_out(
                plan, today_tasks=self._today_pending(plan)))
        return out

    def update_task(self, user_id: str, task_id: str, status: str) -> dict:
        task = self._repo.get_task(task_id)
        if not task:
            raise DomainError("task not found")
        plan = self._repo.get_plan(task.plan_id)
        if not plan or plan.user_id != user_id:
            raise DomainError("not your task")
        status = validate_task_status(status)
        self._repo.update_task_status(task_id, status)
        return self._task_out(self._repo.get_task(task_id))

    def advance_day(self, user_id: str, plan_id: str) -> dict:
        plan = self._repo.get_plan(plan_id)
        if not plan:
            raise DomainError("plan not found")
        if plan.user_id != user_id:
            raise DomainError("not your plan")
        if plan.status == "completed":
            raise DomainError("plan already completed")
        if plan.current_day >= plan.total_days:
            self._repo.update_plan_status(plan_id, "completed")
        else:
            self._repo.update_plan_current_day(plan_id, plan.current_day + 1)
        updated = self._repo.get_plan(plan_id)
        return self._plan_out(updated, today_tasks=self._today_pending(updated))

    # ---- plan generation internals ----
    def _tasks_for_day(self, plan: StudyPlan, day: int,
                       lessons: list[CurriculumLesson], domain_slug: str,
                       start_level: str, total_days: int) -> list[DailyTask]:
        types = plan_task_types_for_day(day, total_days)
        target = difficulty_for_day(day, total_days, start_level)
        lesson = lessons[(day - 1) % len(lessons)] if lessons else None
        pool = self._repo.list_questions(domain_slug, max_difficulty=target)
        pick = tuple(q.id for q in pool[:5])  # ordered by difficulty 1->10
        due = date.today() + timedelta(days=day - 1)

        tasks: list[DailyTask] = []
        for ttype in types:
            title, desc, lesson_id, qids = self._task_content(
                ttype, day, target, lesson, pick)
            task = DailyTask(id=uuid.uuid4().hex, plan_id=plan.id,
                             day_number=day, lesson_id=lesson_id,
                             task_type=ttype, title=title, description=desc,
                             question_ids=qids, status="pending",
                             due_date=due)
            self._repo.create_task(task)
            tasks.append(task)
        return tasks

    @staticmethod
    def _task_content(ttype: str, day: int, target: int,
                      lesson: CurriculumLesson | None,
                      pick: tuple[str, ...]) -> tuple[str, str, str | None,
                                                     tuple[str, ...]]:
        lesson_title = lesson.title if lesson else "theory"
        lesson_id = lesson.id if lesson else None
        if ttype == "learn":
            return (f"Learn: {lesson_title}",
                    "Study the lesson theory. Focus on the WHY, not just the what.",
                    lesson_id, ())
        if ttype == "practice":
            return (f"Practice: {lesson_title} (level <= {target})",
                    f"Answer practice questions up to difficulty {target}.",
                    None, pick)
        if ttype == "code":
            return (f"Code: hands-on {lesson_title}",
                    "Solve by writing code. Run it in the code lab.",
                    None, pick)
        if ttype == "revise":
            return (f"Revise: {lesson_title}",
                    "Re-read key points and re-attempt any questions you got wrong.",
                    lesson_id, ())
        # mock
        return (f"Mock test - day {day}",
                "Timed mock: attempt all questions without peeking at answers.",
                None, pick)

    def _today_pending(self, plan: StudyPlan) -> list[DailyTask]:
        return [t for t in self._repo.list_plan_tasks(
            plan.id, day_number=plan.current_day) if t.status == "pending"]

    # ---- serializers ----
    @staticmethod
    def _domain_out(d: CurriculumDomain,
                    module_count: int | None = None) -> dict:
        out = {"id": d.id, "slug": d.slug, "name": d.name, "icon": d.icon,
               "description": d.description, "category": d.category,
               "order_index": d.order_index, "is_active": d.is_active}
        if module_count is not None:
            out["module_count"] = module_count
        return out

    @staticmethod
    def _module_out(m: CurriculumModule) -> dict:
        return {"id": m.id, "domain_slug": m.domain_slug, "slug": m.slug,
                "name": m.name, "description": m.description,
                "order_index": m.order_index,
                "estimated_days": m.estimated_days}

    @staticmethod
    def _lesson_out(lesson: CurriculumLesson) -> dict:
        return {"id": lesson.id, "module_id": lesson.module_id,
                "slug": lesson.slug, "title": lesson.title,
                "content": lesson.content, "order_index": lesson.order_index,
                "estimated_minutes": lesson.estimated_minutes,
                "has_visual": lesson.has_visual}

    @staticmethod
    def _question_out(q: CurriculumQuestion) -> dict:
        return {"id": q.id, "domain_slug": q.domain_slug,
                "module_slug": q.module_slug, "lesson_id": q.lesson_id,
                "difficulty": q.difficulty, "qtype": q.qtype,
                "prompt": q.prompt, "choices": list(q.choices),
                "answer_index": q.answer_index,
                "explanation": q.explanation,
                "company_tags": list(q.company_tags),
                "created_at": q.created_at.isoformat()}

    @classmethod
    def _plan_out(cls, p: StudyPlan, tasks: list[DailyTask] | None = None,
                  today_tasks: list[DailyTask] | None = None) -> dict:
        out = {"id": p.id, "user_id": p.user_id,
               "domain_slug": p.domain_slug, "start_level": p.start_level,
               "total_days": p.total_days, "current_day": p.current_day,
               "status": p.status, "created_at": p.created_at.isoformat()}
        if tasks is not None:
            out["tasks"] = [cls._task_out(t) for t in tasks]
        if today_tasks is not None:
            out["today_tasks"] = [cls._task_out(t) for t in today_tasks]
        return out

    @staticmethod
    def _task_out(t: DailyTask) -> dict:
        return {"id": t.id, "plan_id": t.plan_id,
                "day_number": t.day_number, "lesson_id": t.lesson_id,
                "task_type": t.task_type, "title": t.title,
                "description": t.description,
                "question_ids": list(t.question_ids), "status": t.status,
                "due_date": t.due_date.isoformat() if t.due_date else None}
