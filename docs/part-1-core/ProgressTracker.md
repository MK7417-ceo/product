# Part 1 — SkillForge Core: ProgressTracker

Updated 2026-10-04. One row per phase/feature. Status: done / in-review /
blocked / planned.

## Foundation (inherited, M0–M9 on master)

| Item | Status | Evidence |
|---|---|---|
| M0 baseline (setup, CI, locked deps) | done | PR #2 merged |
| M1 foundation (request IDs, CORS, /ready) | done | PR #4 merged |
| M2 auth (Bearer, refresh rotation, rate limit) | done | PR #6 merged |
| M3 skill graph (18 skills, 20 edges) + question bank (36 Qs) + seed_versions | done | PR #8 merged |
| M4 deterministic scoring, idempotent submit, session lifecycle | done | PR #10 merged |
| M5 controlled AI eval (mock default, OpenAI-compat adapter, caps, review queue) | done | PR #13 merged |
| M6 profiles + gap analysis endpoints | done | PR #16 merged |
| M7 React frontend (login, dashboard, assessment, roadmap) | done | PR #18 merged |
| M8 verified evidence (server-side rule, no client assertions) | done | PR #20 merged |
| M9 hardening (reviewer/admin roles, export/delete, Dockerfile) | done | PR #22 merged |
| Backend tests | done | 544 green on master |

## v2 Core phases

| Phase | Status | Notes |
|---|---|---|
| A1 Aurora Dark design system | in-review | PR #30 OPEN; tsc clean, build OK, screenshots delivered |
| A2 Google OAuth + resume registration + placement flow | blocked | needs user's PR #30 review + Codespace OK |
| B hybrid question bank (curated + AI-gen + validation) | planned | depends on Part 2 runner for coding-Q verification (mock first) |
| D domain tracks + GitHub tutorials + weekly mocks + daily Qs | planned | 1–2 domains deep first |

## Open PRs (all Core)

- #28 results contract fix (BUG-001) · #29 uvicorn dep (BUG-002) ·
  #30 Aurora redesign (A1 / BUG-003)
