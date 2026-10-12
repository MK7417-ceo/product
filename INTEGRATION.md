# INTEGRATION — feat/ux-v2-rebuild (merged)

## Shell
# INTEGRATION.md — SHELL agent (Milestone 1: app shell)

Branch: `feat/ux-v2-shell`. Work confined to `~/workspace/wt-shell`
(worktree of `~/workspace/product`). Nothing pushed, nothing merged.

## What was built

Aurora Dark app shell matching `~/workspace/ux-preview/index.html`:
sticky TopNav, grouped desktop sidebar, mobile bottom nav, full route
table, auth pages in the new system, real Profile + Billing pages, and
tiny placeholder pages for every route other agents own.

## Files created

- `part-1-core/frontend/src/styles/theme.css` — design-token stylesheet
  (`--base/--surface/--border/--violet/--cyan/--green/--amber/--red/--text/--muted`)
  + all shell/auth/page styles. Palette: violet = actions, cyan = learning,
  green = verified evidence only.
- `part-1-core/frontend/src/components/layout/TopNav.tsx` — logo (hexagon SVG),
  breadcrumb (Home / Page via `CRUMBS` route map), CENTERED ⌘K search (focusable,
  readOnly, non-functional for M1), "✨ Go Pro" + persistent premium popup
  (Upgrade → `/subscription`, "later" dismisses), notification bell (visual only,
  title="coming soon"), gradient avatar + dropdown (Signed in as, Your profile,
  Settings, ✨ Upgrade to Pro, Billing & usage, Integrations → `/settings#integrations`,
  Sign out via AuthContext). No streak pill: `GET /api/v1/practice/today` returns
  `{date, questions, tasks, has_roadmap}` — no streak field, so none is shown.
- `part-1-core/frontend/src/components/layout/Sidebar.tsx` — grouped nav
  (HOME / DEVELOP / PROVE / LAUNCH) with icons + active state; Roadmap count
  badge = pending+in_progress tasks from `GET /api/v1/roadmaps/current`
  (hidden while loading / on error / when 0).
- `part-1-core/frontend/src/components/layout/BottomNav.tsx` — mobile tabs
  (≤900px): Home→/, Develop→/plan, Prove→/skills, Launch→/resume.
- `part-1-core/frontend/src/components/layout/AppShell.tsx` — `RequireAuth`
  (reuses AuthContext) + TopNav/Sidebar/`<Outlet/>`/BottomNav.
- `part-1-core/frontend/src/lib/plan.ts` — M1 plan contract: subscribed if
  `localStorage['sf_plan']` ∈ {pro, expert} (set by the demo subscription flow)
  OR the real backend tier is pro/expert; dispatches `sf:plan-change` on change.
  After "purchase": Go Pro button + popup + "Upgrade to Pro" menu item disappear,
  PRO/EXPERT badge shows next to the avatar.
- `part-1-core/frontend/src/App.tsx` — router with lazy page imports;
  `/assessment` → redirects to `/plan`. `src/main.tsx` now just renders `<App/>`.
- `part-1-core/frontend/src/pages/Profile.tsx` — real: `authApi.me()` (via
  AuthContext) + `GET /api/v1/account/subscription` for tier; loading/error/empty
  states; link to `/settings`.
- `part-1-core/frontend/src/pages/Billing.tsx` — real: current tier + full tier
  matrix from `GET /api/v1/account/subscription`; "CURRENT" badge; honest note
  that checkout is 501 until payments KYC (never faked); link to `/subscription`.
- `src/pages/Login.tsx`, `src/pages/Register.tsx` — restyled, auth logic untouched.
- 16 placeholder pages at the exact paths below (tiny, buildable; to be
  overwritten by their owners at merge).
- Deleted (unused, superseded): `src/components/Shell.tsx`, `src/pages/Placeholder.tsx`.

## Files modified

- `vite.config.ts` — dev proxy target `localhost:8000` → `127.0.0.1:8001`
  (the live shared test backend).

## Route table

| Route | Page | Owner |
|---|---|---|
| `/` | Dashboard | placeholder (other agent) |
| `/login`, `/register` | Login / Register (public) | SHELL |
| `/welcome` | onboarding/Welcome | placeholder |
| `/resume` | onboarding/Resume | placeholder |
| `/subscription` | onboarding/Subscription | placeholder |
| `/plan` | onboarding/MakePlan | placeholder |
| `/verification` | onboarding/Verification | placeholder |
| `/assessment` | → redirect `/plan` | SHELL |
| `/roadmap` | Roadmap | placeholder |
| `/practice` | Practice | placeholder |
| `/codelab` | CodeLab | placeholder |
| `/skills` | SkillProfile | placeholder |
| `/gaps` | SkillGaps | placeholder (P1-pages agent owns) |
| `/evidence` | Evidence | placeholder |
| `/certificates` | Certificates | placeholder |
| `/portfolio` | Portfolio | placeholder |
| `/interview` | InterviewPrep | placeholder |
| `/english` | English | placeholder |
| `/settings` | Settings | placeholder |
| `/profile` | Profile (real) | SHELL |
| `/billing` | Billing (real) | SHELL |
| `*` | → redirect `/` | SHELL |

NOT created (per spec): `/notifications`, `/skill-gaps` (superseded by the
approved `/gaps` P1 page), `/resources`.

## Breadcrumb mapping (`CRUMBS` in TopNav.tsx)

/→Dashboard, /welcome→Welcome, /resume→Resume, /subscription→Subscription,
/plan→Assessment, /verification→Verification, /roadmap→Roadmap, /practice→Practice,
/codelab→Code Lab, /skills→Skill Profile, /gaps→Skill Gaps, /evidence→Evidence, /certificates→Certificates,
/portfolio→Portfolio, /interview→Interview Prep, /english→English, /settings→Settings,
/profile→Profile, /billing→Billing.

## Contracts other agents must know

1. **Demo purchase**: the Subscription page must call `setLocalPlan('pro'|'expert')`
   from `src/lib/plan.ts` on demo purchase (writes `localStorage['sf_plan']` and
   fires `sf:plan-change`). Real checkout stays 501 — do not fake payment.
2. **Roadmap badge** refreshes only on page load (no live updates) — acceptable for M1.
3. **TopNav has zero page links**; all navigation lives in the Sidebar/BottomNav.
4. Search box is visual + focusable only (readOnly). Bell is visual only.
5. Placeholder pages are intentional; do not "fix" them here — their owners deliver.

## Verification (all against live backend 127.0.0.1:8001, dev server :5174)

- `npx tsc --noEmit` — clean.
- `npx vite build` — succeeds.
- Playwright (register→API tokens→inject `sf_access_token`/`sf_refresh_token`):
  desktop shell, avatar dropdown, premium popup, mobile bottom nav, login page —
  screenshots in `~/workspace/your_files/skillforge-v2/output/`:
  `ux-v2-shell-desktop.png`, `ux-v2-avatar-dropdown.png`, `ux-v2-premium-popup.png`,
  `ux-v2-mobile-nav.png`, `ux-v2-login.png`
  (+ `ux-v2-plan-expert.png` bonus: EXPERT badge state).
- Verified live: /profile and /billing render real backend data (Free tier);
  /assessment → /plan redirect; roadmap badge hidden with no roadmap;
  EXPERT state (sf_plan=expert): badge shows, Go Pro + popup + "Upgrade to Pro" hidden.
- NOT verified: a user with an actual open roadmap (badge with count) — the
  shared test DB had no roadmap for the test users; badge logic follows the
  `task_counts` shape exactly. Also not verified: backend-tier-driven PRO state
  (no test user has a paid tier).


## Dashboard
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
