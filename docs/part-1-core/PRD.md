# Part 1 — SkillForge Core: PRD

**Status:** v1.0 — 2026-10-04. Owner: product (agent) + founder (user).
**Scope:** the learn & assess loop. Everything from signup to "what do I learn
next" lives here. Parts 2 (code runner) and 3 (career launchpad) are separate
dossiers.

## Vision

One place where a beginner entering a tech field becomes job-ready: register →
prove your real level with a diagnostic → get assessed on real interview-grade
questions → see verified skill gaps → follow a roadmap → practice daily →
re-assess. No skill level ever comes from self-report alone.

## Personas

1. **Aarav, 21 — final-year CS student (beginner→intermediate).** Wants to know
   if he's actually ready for placements. Pain: tutorials give no proof of
   skill; he needs verified evidence and a plan.
2. **Priya, 27 — QA engineer switching to AI/ML (intermediate).** Self-declared
   "intermediate in Python". Pain: doesn't know what she doesn't know; needs
   the diagnostic to expose real gaps per topic.
3. **Rahul, 24 — self-taught Python dev (advanced).** Wants expert-level,
   time-bound tasks and daily hard questions. Pain: most platforms stop at
   beginner content.

## Goals

- Verified skill profiles (evidence-backed, never self-reported).
- Level-matched assessments mixing curated real interview questions + fresh
  AI-generated questions (hybrid strategy).
- Explainable gaps and dependency-aware roadmaps that preserve history.
- A practice rhythm: daily questions + weekly mocks.

## Non-goals (other parts)

- Code execution (Part 2). Hiring-phase prep, resume/JD, portfolio, billing
  (Part 3). Core exposes ports those parts consume.

## Features

**Must-have (MVP):**
1. Email/password + Google OAuth login; RBAC (user/reviewer/admin).
2. Resume-style registration + onboarding diagnostic → verified level per topic.
3. Hybrid question bank: curated real interview questions (level-tagged) +
   AI-generated questions with validation pipeline.
4. Assessments: MCQ + coding + short reasoning; deterministic scoring;
   budget-capped AI evaluation for subjective answers; human review queue.
5. Skill profiles + ranked gap analysis with plain-language reasons.
6. Roadmap generation + regeneration that never deletes history/evidence.
7. Dashboard (Aurora Dark): readiness ring, skill bars, gaps, roadmap preview.

**Should-have:** domain tracks (beginner→expert→job), daily 2–5 questions,
weekly mocks (1 compulsory + 1 optional), GitHub workflow tutorials.

**Won't-have (v2 Core):** code execution, plagiarism, GD/PI/IELTS, resume,
portfolio, subscriptions — other parts.

## User stories + acceptance criteria

1. *As Aarav, I register and take the diagnostic, so I see my real level per
   topic.* AC: diagnostic ≤ 15 min; results show per-topic level with the
   questions that determined it; a false self-declared "expert" is corrected
   by evidence.
2. *As Priya, I take a Python assessment, so I get a verified profile.* AC:
   MCQ scored deterministically server-side; short answers AI-graded with
   confidence; low-confidence → human review; results page renders showing
   per-skill mastery + confidence (BUG-001 regression).
3. *As Rahul, I get daily hard questions, so I keep improving.* AC: 2–5/day,
   level-matched, never the identical set twice in a row, with explanations.
4. *As any user, I regenerate my roadmap, so completed work is never lost.*
   AC: new roadmap version created; old versions, evidence, completed tasks
   intact.
5. *As a reviewer, I resolve human-review items, so AI mistakes get corrected.*
   AC: reviewer role only; never own items (separation of duties); resolution
   recomputes the session score.

## Success metrics

- Diagnostic completion rate ≥ 60% of registrations.
- Assessment results page crash rate = 0 (regression test locked).
- ≥ 70% of users with ≥ 1 verified skill after 2 assessments.
- Roadmap regeneration preserves 100% of evidence records (audited).

## Risks

- Thin question bank (36 seeded) → content is the long pole; mitigate with
  AI-draft + human-review pipeline and user-supplied links.
- AI question hallucinations → validation pipeline + report button; 100%
  guarantee impossible (communicated to user).
- LLM cost at scale → deterministic-first, caching, per-user caps, kill switch.
