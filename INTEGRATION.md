# Dashboard agent (Milestone 1) — integration notes

Branch: `feat/ux-v2-dashboard` · commit adds the SkillForge v2 dashboard.
All sections derive from the **live** backend (`http://127.0.0.1:8001`) — no mock data.

## Files created

| File | Purpose |
|---|---|
| `part-1-core/frontend/src/pages/Dashboard.tsx` | **Default export `Dashboard`** — the dashboard page. The shell's router should lazy-import this as the index route. Orchestrates 5 parallel fetches (roadmap, practice/today, assessments, profile, placement topics), computes greeting + next-best-action, and composes the sections below. |
| `part-1-core/frontend/src/lib/api-dashboard.ts` | Typed API helpers using the **shared** `api()` fetch client from `src/lib/api.ts` (token + 401-refresh logic reused, untouched). Missing resources (`GET /roadmaps/current` 400 "no roadmap yet", `GET /profiles/me` 400 "profile not found") resolve to `null` so the UI renders actionable empty states. |
| `part-1-core/frontend/src/components/dashboard/dashboard.css` | Component-scoped styles. Uses the shell's token names: `--base` (with `#080B14` fallback), `--surface`, `--border`, `--violet`, `--cyan`, `--green`, `--amber`, `--red`, `--text`, `--muted`. Violet = primary actions, cyan = learning/progress, green = verified-only indicators. |
| `part-1-core/frontend/src/components/dashboard/ui.tsx` | `Load` (skeleton), `ErrBox` (error + retry), `Dot`. |
| `part-1-core/frontend/src/components/dashboard/HeroCard.tsx` | Diagnostic-readiness hero (violet→cyan gradient top border). No roadmap → 3-step checklist (profile / diagnostic / roadmap) + progress + "Start 15-min diagnostic →" to `/assessment`. Roadmap present → hero switches to roadmap progress with "Continue roadmap →" to `/roadmap`. |
| `part-1-core/frontend/src/components/dashboard/StatCards.tsx` | Four clickable stat cards: **Verified readiness → /skills** (aggregated % over completed assessments; "Not yet" empty state), **Top skill gap → /skills** (top open roadmap task's first target skill, else weakest verified topic), **Roadmap progress → /roadmap** (`task_counts`), **Practice streak → /practice**. Also exports `topActionableTask()` used by Dashboard + ContinueCard. |
| `part-1-core/frontend/src/components/dashboard/ContinueCard.tsx` | "Continue where you left off": top actionable task (in_progress first, then pending, high→low priority) with why-it-matters, effort, expected evidence, priority; "Resume →"/"Start →" to `/roadmap`. Empty: "No roadmap yet — Create your plan →". |
| `part-1-core/frontend/src/components/dashboard/WeekStrip.tsx` | Weekly strip, current day highlighted (cyan). Below: real today stats from `/practice/today` ("Today: 3 questions · 2 tasks"). No activity history exists in the backend, so past/future days are neutral — nothing is invented. |
| `part-1-core/frontend/src/components/dashboard/TodayRail.tsx` | Right rail: "Today's tasks" from `GET /practice/today` (title, effort, status pill, → `/practice`), then a "Daily DSA" card containing **only** the marker below. |

## Files modified (non-dashboard)

- `part-1-core/frontend/vite.config.ts` — dev proxy target changed `localhost:8000` → `127.0.0.1:8001` so the frontend talks to the **live test backend** for this milestone. Revert or parametrize if the shell expects 8000 elsewhere.

## Data dependencies (all verified against `part-1-core/app/api/v1/*.py`)

- `GET /api/v1/roadmaps/current` → hero (roadmap mode), roadmap stat, continue card, gap card
- `GET /api/v1/practice/today` → today's tasks rail, practice stat, week strip
- `GET /api/v1/assessments` → verified-readiness stat, gap fallback, hero diagnostic step
- `GET /api/v1/profiles/me` → hero diagnostic step, next-best-action
- `GET /api/v1/placement/topics` → next-best-action line names the real first topic ("complete ml-basics diagnostic…")

## Known gaps / adaptations (honest, no invented data)

1. **No streak endpoint exists** in the backend (grep found zero "streak" references). The "PRACTICE STREAK" card shows today's *served* question count (`3 today · daily questions served · open practice`) until a streak endpoint is added.
2. **No `/skills` route** exists in the current router — stat cards 1–2 link to `/skills` as specified; today that 404s to `/` (the `*` redirect). The shell agent must register the skills page route (another agent's scope).
3. **No `/plan` route** exists — the hero CTA goes to `/assessment` (diagnostic entry) instead, per the task's "/plan or /roadmap" allowance.
4. The backend serves dates in **UTC** (`/practice/today` → `2026-10-12` while IST is the 13th). The week strip highlights the backend's "today", which can lag IST by a day.
5. **DSA slot** — `TodayRail.tsx` renders exactly:
   `{/* DSA-SLOT: coordinator wires <DailyDSACard/> from src/components/dsa/DailyDSACard.tsx here */}`
   and nothing else in that position. The DSA agent owns the component.

## Quality

- `tsc --noEmit` — clean. `vite build` — succeeds.
- Screenshots (Playwright, real backend, tokens via `sf_access_token`/`sf_refresh_token` localStorage keys, design tokens injected for mockup fidelity):
  - `~/workspace/your_files/skillforge-v2/output/ux-v2-dashboard-desktop.png` (1440×900, populated: profile + placement + assessment + roadmap)
  - `~/workspace/your_files/skillforge-v2/output/ux-v2-dashboard-empty.png` (fresh user — all empty states actionable)
  - `~/workspace/your_files/skillforge-v2/output/ux-v2-dashboard-mobile.png` (390×844, populated)
- Console: zero errors on the populated load; on the fresh-user load the expected 400s (`no roadmap yet`, `profile not found`) are caught and rendered as empty states, not errors.

## Rollback

Single commit on `feat/ux-v2-dashboard`. Revert with `git revert <sha>`; the only non-dashboard change is the `vite.config.ts` proxy line.
