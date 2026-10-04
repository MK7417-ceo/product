# Part 1 — SkillForge Core: TRD

**Status:** v1.0 — 2026-10-04. Stack: FastAPI · PostgreSQL · React+Vite+TS ·
Alembic · pytest · Docker. Architecture: Clean/Hexagonal (see
`../ARCHITECTURE.md`).

## Hexagonal mapping

Domain core = plain Python + pydantic. No FastAPI/SQLAlchemy/HTTP imports.

| Domain concept | Inbound port (what world asks) | Outbound port (what core needs) | Adapter |
|---|---|---|---|
| auth | `AuthService.register/login/refresh/logout` | `UserRepository`, `PasswordHasher`, `TokenIssuer`, `OAuthClient` | FastAPI routers (in); SQLAlchemy repos, JWT, Google OAuth client (out) |
| users | `ProfileService.get/update` | `UserRepository` | routers; SQLAlchemy |
| questions | `QuestionBankService.list/search` | `QuestionRepository` | routers; SQLAlchemy |
| assessments | `AssessmentService.start/submit/finalize` | `QuestionRepository`, `SessionRepository`, `IdempotencyStore` | routers; SQLAlchemy |
| scoring | `ScoringService.grade` | `AIEvalProvider`, `EvalRunStore`, `ReviewQueue` | deterministic grader (in-core); OpenAI-compat/mock AI client (out) |
| skills | `SkillGraphService.get_graph`, `ProfileService.recompute` | `SkillGraphRepository`, `EvidenceRepository` | routers; SQLAlchemy |
| gaps | `GapAnalysisService.rank_gaps` | `ProfileRepository` | in-core ranking; router |
| roadmaps | `RoadmapService.generate/regenerate` | `RoadmapRepository` | routers; SQLAlchemy (versioned rows) |
| learning | `PracticeService.daily_questions/schedule_mock` | `QuestionRepository`, `EmailSender` | routers; SQLAlchemy; email adapter |

Rules: routers call inbound ports only. Modules talk to each other via inbound
ports, never by importing another module's internals. Outbound ports are
interfaces; adapters are swappable (mock AI provider today, real LLM tomorrow).

## API endpoints (v1)

| Method | Path | Purpose |
|---|---|---|
| POST | /auth/register, /auth/login | email/password auth |
| POST | /auth/oauth/google | Google OAuth (Phase A2) |
| POST | /auth/refresh, /auth/logout | token rotation |
| POST | /api/v1/assessments/start | begin session (idempotency key) |
| GET | /api/v1/assessments/questions | level-matched questions (no answer keys) |
| POST | /api/v1/assessments/submit | submit answers (never scores) |
| GET | /api/v1/assessments/{id}/results | per-skill mastery + confidence |
| GET | /api/v1/profiles/{user_id} | verified skill profile |
| GET | /api/v1/profiles/{user_id}/gaps | ranked gaps + reasons |
| POST | /api/v1/roadmaps/generate | new roadmap version |
| GET | /api/v1/roadmaps/{user_id} | roadmap history |
| GET/POST | /api/v1/evaluations/... | AI eval runs + review queue (reviewer role) |
| GET | /api/v1/learning/daily | 2–5 daily questions |
| POST | /api/v1/learning/mocks/schedule | weekly mock (1 compulsory + 1 optional) |
| GET | /api/v1/admin/users/{id}/export | data export (M9) |

## Data model (key tables)

- `users` (id, email, password_hash, role, oauth_google_sub, created_at)
- `skill_graph_versions`, `skills` (id, name, domain, level),
  `skill_edges` (prerequisite), `question_bank_versions`,
  `questions` (id, skill_id, type, difficulty, prompt, answer_key JSON, rubric,
  source, version)
- `assessment_sessions` (id, user_id, idempotency_key, status,
  skill_graph_version, question_bank_version),
  `assessment_responses` (session_id, question_id, user_answer, score,
  graded_by)
- `evidence_records` (id, user_id, skill_id, score_pct, method, verified_by,
  verified_at, status) — server-verified only
- `ai_evaluation_runs` (prompt_version, model, confidence, cost, latency),
  `human_review_queue` (status, reviewer_id ≠ owner)
- `roadmaps` (id, user_id, version, generated_at),
  `roadmap_tasks` (roadmap_id, skill_id, status, evidence links)
- `seed_versions` (idempotent seeding ledger)

## NFRs

- API p95 < 300 ms (excluding AI eval); AI eval calls timeout-capped + cached.
- Every request carries `X-Request-ID`; structured JSON logs.
- Migrations always reversible; upgrade + downgrade tested on SQLite + Postgres.
- Auth: 30-min access tokens, refresh rotation, rate limiting, RBAC on all
  assessment/roadmap/eval endpoints.
- No PII beyond registration fields; export/delete (M9) retained.
- Feature flags for: google_oauth, ai_question_gen, daily_questions, mocks.
