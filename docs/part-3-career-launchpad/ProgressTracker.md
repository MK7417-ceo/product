# ProgressTracker — Part 3: Career Launchpad

**Seeded honestly 2026-10-04: Part 3 is NOT built. All phases PLANNED.**

| Phase | Scope | Status | Agent lane | Developer lane |
|---|---|---|---|---|
| P3.1 | Subscriptions & billing (tiers, checkout, webhooks, entitlements) | PLANNED — **critical path** | — | — |
| P3.2 | Resume builder + JD matcher (ATS) | PLANNED | — | — |
| P3.3 | Portfolio builder + publish to user's GitHub | PLANNED | — | — |
| P3.4a | Typing + quant/aptitude modules | PLANNED | — | — |
| P3.4b | Presentation + extempore | PLANNED | — | — |
| P3.4c | GD + PI mocks (camera), feedback + challenge flow | PLANNED | — | — |
| P3.4d | IELTS-level English track | PLANNED | — | — |
| P3.5 | Certificates, account linking/sharing, trend watcher | PLANNED | — | — |

## Gate rule

A phase moves PLANNED → IN PROGRESS only after its PLAN section is approved.
IN PROGRESS → DONE only when agent lane AND developer lane both pass with
evidence. DONE phases stay green; regressions re-open them.

## Current critical path

P3.1 (billing) gates everything: no paid feature can ship without
entitlements enforced. Recommendation: start P3.1 the moment Part 3 build
begins; P3.2 can overlap once `BillingService` port is stable.
