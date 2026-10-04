# Part 1 — SkillForge Core: Change_log

Newest first. Every entry: date, what changed, PR/commit, impact.

- **2026-10-04** — Hexagonal architecture ADOPTED for all 3 parts (user
  decision). Core modules to be refactored behind ports/adapters; no behavior
  change. Recorded in `../ARCHITECTURE.md`.
- **2026-10-04** — Program split into 3 parts; this dossier created
  (`skillforge-v2/part-1-core/`). Founder-skills gates adopted: PLAN approved
  → build → agent lane + developer lane → review.
- **2026-10-04** — Phase A1 complete: Aurora Dark theme, sidebar AppShell,
  shared UI components, redesigned dashboard. PR #30 opened; `tsc` clean,
  `npm run build` OK; running-app screenshots captured.
- **2026-10-04** — PR #29 opened: adds missing `uvicorn` to
  backend/requirements.txt (fresh installs couldn't boot).
- **2026-10-04** — PR #28 opened: assessment results contract fix — submit now
  emits `mastery_percentage`/`confidence_percentage` (legacy `percentage`
  kept); fixes blank results page (BUG-001).
- **2026-10-04** — v2 decisions locked: Aurora Dark UI; hybrid question
  strategy (AI-fresh + curated real interview Qs); MVP-first launch;
  Free ₹0 / Pro ₹249 / Expert ₹599 subscriptions (Part 3).
- **2026-10-03** — PR #26 merged (evidence-integrity fixes: wrong-FK fallback,
  verified evidence on human review). 544 backend tests green.
- **2026-10-03** — PR #24 merged (refresh-token auto-renewal, login user_id
  shape fix). 543 tests green.
- **2026-10-03** — M9 merged (PR #22): RBAC reviewer/admin, export/delete,
  Dockerfile. M0–M9 complete.
- **2026-10-03** — M8 (PR #20), M7 (PR #18), M6 (PR #16), M5 (PR #13),
  M4 (PR #10), M3 (PR #8), M2 (PR #6), M1 (PR #4), M0 (PR #2) merged.
