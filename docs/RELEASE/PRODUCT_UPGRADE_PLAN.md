# SKILLFORGE — Product Upgrade & Launch Execution Plan

This document separates verified findings from items that still require runtime testing. A file or route existing is not proof that a feature works end-to-end.

## Product bar
SKILLFORGE must help a learner demonstrate skills, close measurable gaps, build evidence, and match career opportunities. Do not advertise unimplemented capabilities, fake verification, fake outcomes, or payment success.

## Verified findings from source inspection

### P0 — data, security, launch blockers
- The core backend uses SQLAlchemy and defaults to `sqlite:///./skillforge.db`; this is a relative path resolved from the process working directory. Docker Compose defines PostgreSQL with a persistent `pgdata` volume. Local persistence location and migrations still need a runtime restart test.
- Alembic migration files exist, but the versions directory contains multiple historical migrations and merge revisions. A clean-database upgrade and an existing-database upgrade both need to be tested.
- Evidence submission currently transitions the roadmap task to completed immediately. Existing tests assert this behavior. Submission must not equal independent verification; introduce explicit review states and keep verified skills separate.
- Code Engine has resource limits and a network namespace requirement. If isolation primitives cannot be established, execution must fail closed. It still needs execution in a hardened Linux/container environment before any public multi-tenant launch.
- Billing checkout currently reports that online payments are not connected (HTTP 501). Do not sell subscriptions until provider checkout, signed webhooks, idempotency, refunds/cancellations, entitlements, tax/invoice handling and regional payment methods are verified.
- Existing CI has backend tests but does not fully gate frontend build/type checks and Code Engine tests.
- Practice date calculation uses UTC; user-facing daily streaks should use the profile timezone, defaulting to Asia/Kolkata for India-based users.

### P1 — intelligence and learning quality
- Assessment scoring and gap detection are deterministic/rule-based. Keep scoring deterministic, but expand the curated question bank, skill coverage, difficulty calibration and anti-cheating safeguards.
- Doubt solver is DB-first with curated-content RAG and optional Gemini fallback. Current local embeddings are hashed token vectors, not a pretrained semantic model.
- Evaluate multilingual E5-small (MIT) or multilingual MiniLM (Apache-2.0) for semantic retrieval. Benchmark Hindi, Hinglish and English relevance, CPU latency, memory and model loading before adoption.
- Do not train or claim predictive ML until sufficient consented, representative outcome data exists. Begin with transparent rules and evaluate recommendation quality.
- Roadmap generation currently depends on supplied skill/mastery inputs and deterministic templates. Connect it to assessment results, evidence review, role skill frameworks and learner constraints.

### P2 — experience, growth and revenue
- Audit every route and user journey for loading, empty, error, success, validation and mobile states.
- Improve first-session activation: short onboarding, free diagnostic, immediate actionable report and clear next step.
- Add shareable verified profiles, portfolio projects, public skill pages, SEO career/role pages and referral loops.
- Add accessible, consistent responsive design; optimize bundle size, caching, pagination and N+1 database queries.
- Separate Free/Pro/Team entitlements on the server. Add international pricing/currencies and payment methods only after legal/provider availability is checked for target countries.

## Execution gates (in order)
1. Database: prove clean migration, CRUD, persistence after restart, user isolation, transaction rollback, backups/restore, query plans and concurrent reads/writes.
2. Security: authentication/session review, authorization matrix, rate limiting, secret handling, evidence ownership, sandbox isolation and dependency audit.
3. Core workflow: onboarding → assessment → gaps → roadmap → practice → evidence submission/review → verified profile.
4. AI/ML: benchmark semantic retrieval and recommendation quality; model must be optional, cached, observable and never block core product use.
5. Frontend quality: typecheck, lint, production build, responsive accessibility and end-to-end critical-path tests.
6. Performance: establish p50/p95 API latency, frontend Core Web Vitals, query count, bundle size and load-test targets before optimization claims.
7. Monetization: payment provider selection, global coverage by country, signed webhooks, subscription lifecycle, server-side entitlements and billing support.
8. Launch: staging acceptance, monitoring/alerts, backups, restore drill, privacy/terms/refund policies, support channel and rollback plan.

## Acceptance principles
- Every feature must be tested as a user journey, not just by checking that its page or endpoint exists.
- No fake AI, fake verification, fake testimonials, fake payment success or invented performance claims.
- Preserve backward compatibility with migrations and test data.
- Changes are isolated on `feat/expert-product-upgrade`; do not merge to main without owner approval.
- Report each item as PASS, FAIL, BLOCKED or NOT TESTED, with evidence.
