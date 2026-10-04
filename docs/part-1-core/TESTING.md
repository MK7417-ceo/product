# Part 1 — SkillForge Core: TESTING

**Rule: no feature is DONE until both lanes pass. Every bugfix ships with a
regression test. Evidence is attached to the PR, not claimed.**

## Lane 1 — Agent (run on agent's end)

Run from the repo task branch, clean tree, before opening the PR.

Backend:
- `cd backend && python -m pytest -q` → all green; report exact count.
- `alembic upgrade head && alembic downgrade -1 && alembic upgrade head`
  on a scratch SQLite DB → reversible-migration proof.
- Boot API (`uvicorn app.main:app --port 8000`), seed → 18 skills +
  36 questions present.
- Exercise the feature's endpoints: register → login → start assessment →
  submit → results; paste status codes + key JSON fields.
- `grep -ri "password\|secret\|token" <diff>` → no secrets in diff.

Frontend:
- `cd frontend && npx tsc --noEmit` → clean.
- `npm run build` → succeeds.
- Playwright (local, real browser): load app, screenshot every touched screen
  at 1440×900 and 390×844 (mobile); attach PNGs. Localhost screenshots via
  local Playwright only.

Evidence required in PR: test counts, migration output, endpoint transcript,
screenshots. "Works on my machine" without this = not done.

## Lane 2 — Developer (user's Codespace checklist)

The user runs this per feature; the feature closes on the user's "OK".

1. Open the PR branch in Codespace; backend up (`uvicorn`), frontend up
   (`npm run dev`).
2. Register a new user → log in → confirm sidebar + dashboard render (Aurora).
3. Start an assessment → answer all → submit → **results page must render**
   (this is the BUG-001 regression: per-skill bars + confidence visible).
4. Check gaps tab: priorities + one-line reasons visible.
5. Generate roadmap → regenerate → confirm old version still listed and
   nothing disappeared.
6. Mobile width: sidebar collapses to usable nav; no overlap.
7. Log out → log in → session persists correctly.

"What working looks like": every step completes with no blank screens, no
console errors, and data matching what was submitted.

## Regression rule

Every entry in BUGS.md gets: a failing test first (or Playwright check), then
the fix, then the test in CI. A bugfix PR without a test is rejected.
