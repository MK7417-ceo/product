# Part 1 — SkillForge Core: PLAN

**Gates (founder-skills workflow):** no phase starts until its PLAN section is
approved; no phase closes until Agent lane + Developer lane both pass; user
merges every PR.

## Phase A1 — Aurora Dark design system ✅ DONE

Goal: new visual foundation. Features: theme tokens, AppShell sidebar, shared
UI components, redesigned dashboard. Done-criteria: `tsc` clean,
`npm run build` OK, screenshots of running app. Demo: login + dashboard
screenshots delivered. PR #30 OPEN (user review pending).

## Phase A2 — Google OAuth + resume registration + placement flow (BLOCKED)

Goal: real onboarding. Features: Google OAuth login (email/password kept);
resume-style registration form (education, experience, skills, target role /
level / tech focus; no confidential fields); onboarding diagnostic (≤15 min,
theory + subjective + coding-concept questions) → verified per-topic level
report. Done-criteria: Google login round-trip works; diagnostic computes
levels from answers, never from the form alone; old email/password flow
unbroken. Demo: register → diagnostic → "real level" report. Blocked on: user
review of PR #30. Branch: `feat/v2-a2-auth-onboarding`.

## Phase B — Hybrid question bank (PLANNED)

Goal: coding-first, level-matched, non-repeating assessments. Features:
curated-bank ingestion pipeline (user-supplied links → structured,
level-tagged, paraphrased); AI question generator behind a port with schema +
business-rule validation; hybrid set composer (X% AI-fresh + Y% curated, no
identical set twice); report-question button. Done-criteria: 200+ curated
questions across Python + AI/ML basics; generator output passes validation ≥
95%; two consecutive attempts never identical. Demo: two assessments with
visibly different sets. Depends on: Part 2 runner for coding-Q answer
verification (mock adapter until Part 2 lands).

## Phase D — Domain tracks + practice rhythm (PLANNED)

Goal: beginner→expert→job tracks with daily/weekly rhythm. Features: track
definitions (AI/ML, Python, C/C++ first); GitHub workflow tutorials; daily 2–5
level-matched questions with explanations; weekly mock scheduler (1 compulsory
+ 1 optional, camera-ON notice + consent per user decision); streak/progress
UI. Done-criteria: enroll → roadmap → daily questions appear; mock scheduled
+ completable; streak counted. Demo: 7-day practice streak on dashboard.

## Gates between phases

1. PLAN approved (this file updated, user says go).
2. Task branch → tests/build green → PR opened (never merged by agent).
3. Agent lane: commands run on agent's end, evidence attached in PR.
4. Developer lane: user runs Codespace checklist (TESTING.md), reports OK.
5. Merge by user → next phase.

## Dependencies on other parts

- Part 2 (Code Engine): coding-question verification + in-assessment code
  execution. Core defines the `CodeRunnerClient` port now; mock adapter until
  Part 2 lands.
- Part 3 (Launchpad): billing entitlements will gate Pro features later; Core
  keeps an `EntitlementChecker` port stubbed to "allow all" until Part 3.
