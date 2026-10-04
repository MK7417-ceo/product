# SKILLFORGE v2 — Architecture: Clean / Hexagonal (Ports & Adapters)

**Status: DECIDED (2026-10-04, user-approved).** Famous architecture, not
invented here: Alistair Cockburn's Hexagonal Architecture ("Ports & Adapters"),
Robert C. Martin's Clean Architecture. Chosen over microservices-everything
because it gives add/remove/update-anywhere freedom without distributed-system
ops burden at our scale.

## The rule (applies to all 3 parts)

- **Domain core: pure logic.** No FastAPI, no SQLAlchemy, no HTTP clients, no
  framework imports inside the core. It is plain Python (+ pydantic schemas).
- **Inbound ports (interfaces):** what the outside world may ask the core to do.
  Example: `AssessmentService.submit_answers(...)`,
  `RoadmapService.generate(...)`, `BillingService.create_subscription(...)`.
  The API layer calls ports — never domain internals.
- **Outbound ports (interfaces):** what the core needs from the outside world.
  Example: `QuestionRepository`, `AIEvalProvider`, `CodeRunnerClient`,
  `PaymentGateway`, `GitHubPublisher`, `EmailSender`.
- **Adapters implement ports.** FastAPI routers = inbound adapters.
  SQLAlchemy repositories, OpenAI-compatible client, Razorpay/Stripe clients,
  GitHub API client = outbound adapters.

## Why this gives "add / remove / update any feature anywhere"

- **Add** a feature → new inbound port + domain use-case + adapter. Nothing
  else changes.
- **Remove** a feature → delete its module + its router registration. The rest
  never referenced it (they only knew ports).
- **Update / swap** → write a new adapter behind the same port. Swap LLM
  provider, swap Razorpay→Stripe, swap question source — zero caller changes.
- **Test** → the domain core is unit-testable with fake adapters; no DB, no
  network needed for business-logic tests.

## How the 3 parts map onto it

1. **part-1-core** — modular monolith (FastAPI). Each domain (auth, users,
   questions, assessments, scoring, skills, roadmaps, learning) is a module
   with its own ports; modules talk to each other only through inbound ports.
2. **part-2-code-engine** — physically separate service (FastAPI + Docker
   sandbox on an isolated host). Security forces the split: untrusted code
   execution must never share a host with user data. It exposes one versioned
   HTTP API; Core consumes it through the `CodeRunnerClient` outbound port —
   so the runner can be swapped/mocked without touching Core.
3. **part-3-career-launchpad** — modules inside the monolith, each behind
   ports (`PaymentGateway`, `GitHubPublisher`, `ResumeRenderer`, ...).
   Extractable into services later without rewrites, if measured load demands.

## Non-negotiable conventions (all parts)

- `/api/v1` versioned routers; `X-Request-ID` on every request; structured
  JSON logs with the request ID.
- Alembic migrations, always reversible (upgrade + downgrade tested).
- `pytest` per module on the backend; `npx tsc --noEmit` + `npm run build`
  on the frontend. CI runs all of it.
- Deterministic-first: deterministic scoring where possible; LLM only where
  it is unsuitable; every AI output schema-validated, budget-capped, versioned.
- Feature flags for every major capability.
- No raw LLM output → user-facing artifact. No skill levels from self-report
  alone. Regeneration never deletes evidence/history.
- Secrets: never in chat, never in git. Secure Vault / env only.
- Every phase: PLAN approved → build → **agent-lane tests (actually run on
  the agent's end, evidence attached)** → **developer-lane check (user's
  Codespace checklist)** → review → next phase.
