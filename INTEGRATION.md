<<<<<<< HEAD
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
=======
# Onboarding pages — integration guide (UX v2, Milestone 1)

Owner: ONBOARDING agent. Branch: `feat/ux-v2-onboarding`. All pages are
**default exports**; lazy-import them in the shell router. No page registers
itself in the sidebar — wizard steps/results are internal steppers/panels.

## Files

| File | Route | Purpose |
|---|---|---|
| `part-1-core/frontend/src/pages/onboarding/Welcome.tsx` | `/welcome` | Post-login resume nudge (Flow 1). Shows once. |
| `part-1-core/frontend/src/pages/onboarding/Resume.tsx` | `/resume` | JD matcher + guided resume builder (Flow 2). **Also mount as sidebar LAUNCH → Resume** (same component). |
| `part-1-core/frontend/src/pages/onboarding/Subscription.tsx` | `/subscription` | Free/Pro/Expert plans (Flow 1, step M). |
| `part-1-core/frontend/src/pages/onboarding/MakePlan.tsx` | `/plan` | Subject + level wizard → starts placement (Flow 3). |
| `part-1-core/frontend/src/pages/onboarding/Verification.tsx` | `/verification` | Placement test stepper + per-level results (Flow 3). |
| `part-1-core/frontend/src/pages/onboarding/lib.ts` | — | Shared types + localStorage contracts. |
| `part-1-core/frontend/src/pages/onboarding/onboarding.css` | — | UX v2 tokens + page styles, scoped under `.ob` (never touches shell styles). Imported by each page. |

Suggested router wiring (shell owns `main.tsx`):

```tsx
const Welcome = lazy(() => import('./pages/onboarding/Welcome'));
const Resume = lazy(() => import('./pages/onboarding/Resume'));
const Subscription = lazy(() => import('./pages/onboarding/Subscription'));
const MakePlan = lazy(() => import('./pages/onboarding/MakePlan'));
const Verification = lazy(() => import('./pages/onboarding/Verification'));
// inside the authenticated layout (or Welcome standalone — your call):
<Route path="welcome" element={<Welcome />} />
<Route path="resume" element={<Resume />} />        {/* also the LAUNCH → Resume sidebar entry */}
<Route path="subscription" element={<Subscription />} />
<Route path="plan" element={<MakePlan />} />
<Route path="verification" element={<Verification />} />
```

## Router-state contract: /verification

MakePlan navigates with `navigate('/verification', { state })`. Do not
deep-link to `/verification` — the page redirects to `/plan` when state is
absent (placement sessions are single-use; refresh loses the session by design).

```ts
interface VerificationState {
  placement_id: string;      // from POST /api/v1/placement/start
  topic: string;             // e.g. "python"
  claimed_level: string;     // "intermediate" | "advanced"
  questions: Array<{         // public questions — answer keys NEVER included
    id: string; topic: string; level: string;
    prompt: string; choices: string[];
  }>;
}
```

## localStorage contracts (shell must honor)

| Key | Values | Meaning |
|---|---|---|
| `sf_welcome_seen` | `"1"` | Set when the user clicks "Skip for now" on `/welcome`. The nudge shows exactly once; returning visits redirect to `/`. |
| `sf_plan` | `"pro"` \| `"expert"` \| absent | **DEMO SCAFFOLDING.** Shell's "Go Pro" popup + plan badge read this key: present → hide popup, show PRO/EXPERT badge. Absent → fall back to the backend subscription tier (`GET /api/v1/account/subscription`). |

## Demo-purchase scaffolding (remove when real checkout lands)

`Subscription.tsx` contains a clearly-labeled dashed "DEMO ONLY" panel with
**Simulate Pro purchase / Simulate Expert purchase / Reset to Free**. It only
writes `localStorage['sf_plan']` — no payment is faked, the backend tier is
untouched. The Upgrade buttons call the real `POST /api/v1/account/subscription/checkout`,
which returns **501** today; the UI shows an honest "Checkout coming soon —
we'll notify you" state. Delete the `.ob-demo` block when Razorpay/Stripe KYC
is done.

## Backend endpoints used (all verified live, Oct 13 2026)

- `GET /api/v1/launchpad/resume` → 404 `{error:"no_resume"}` when absent
- `PUT /api/v1/launchpad/resume` → `{title,summary,skills,experience[],projects[],education[],links{}}`
- `POST /api/v1/launchpad/jd-match` `{jd_text}` → `{score, jd_keyword_count, matched:[{keyword,jd_count}], missing:[...], suggestions:[...]}`
- `GET /api/v1/account/subscription` → `{subscription:{tier,name,price_inr,features}, tiers:{free,pro,expert}}` — prices rendered from this, never hardcoded (₹0 / ₹299 / ₹799 verified in `app/domain/billing.py`)
- `POST /api/v1/account/subscription/checkout` `{tier}` → **501** `{error:"payments_not_connected"}`
- `GET /api/v1/placement/topics` → `{topics:["ml-basics","python"]}`
- `POST /api/v1/placement/start` `{topic, claimed_level}` → `{placement_id, verification_skipped, verified_level, questions[], ...}`
- `POST /api/v1/placement/{id}/submit` `{answers:{qid:choiceIdx}}` → `{analysis:{claimed_level, verified_level, correct, total, summary, levels:{lvl:{correct,total,ratio}}}}`
- `GET /api/v1/roadmaps/current` → **400** `{detail:"no roadmap yet — generate one first"}` when none
- `POST /api/v1/roadmaps/generate` `{gaps:[{skill,mastery_pct}], title}` → 201

Gap mapping (Verification → "Generate my roadmap"): levels with ratio < 0.7 →
one gap `{skill: topic, mastery_pct: worst_ratio*100}`; if everything passed,
one gap for the *next* level `{skill: "<topic> (<next> track)", mastery_pct: 0}`.

## Design

- Tokens (exact var names, defined in `onboarding.css` under `.ob`): `--base #080B14`, `--surface #121A2B`, `--border rgba(255,255,255,.10)`, `--violet #8B5CF6`, `--cyan #36C5F0`, `--green #39D98A`, `--amber #F5B84B`, `--red #F06C75`, `--text #F5F7FB`, `--muted #9AA6BB`.
- **Green discipline:** green is used ONLY for the verified-level badge when a level beyond beginner was genuinely verified. ATS ring is violet→cyan; level bars are cyan/amber/red by ratio.
- All pages have loading / error / empty states. No mock data anywhere (demo purchase panel excepted, labeled).

## Verified

- `tsc -b` clean, `vite build` clean.
- Live-backend E2E via Playwright (real registered user, real tokens): register →
  /plan → topic+level → /verification (8 Qs, stepper, submit) → per-level results
  → /resume (seeded resume, JD paste → ATS 47 ring + matched/missing + suggestions)
  → /subscription (real tiers/prices, 501 checkout, demo-purchase sets `sf_plan=pro`
  and the Pro card flips to CURRENT) → /welcome nudge for a resume-less user.
- Screenshots: `~/workspace/your_files/skillforge-v2/output/ux-v2-{make-plan,verification,verification-result,resume-ats,subscription}.png`.

## Gaps / notes for the shell agent

- `src/App.tsx` does not exist in this worktree (routing lives in `main.tsx`); nothing outside `src/pages/onboarding/` + this file was touched. `vite.config.ts` proxy still targets `localhost:8000` (the standard backend port); the live test backend ran on `:8001` via a local TCP forward.
- `Welcome` works best as a full-page (no sidebar) route — your call in the router.
- If the shell shows a plan badge, read `localStorage['sf_plan']` first, backend tier second (demo override wins).
>>>>>>> feat/ux-v2-onboarding

## Onboarding
# Onboarding pages — integration guide (UX v2, Milestone 1)

Owner: ONBOARDING agent. Branch: `feat/ux-v2-onboarding`. All pages are
**default exports**; lazy-import them in the shell router. No page registers
itself in the sidebar — wizard steps/results are internal steppers/panels.

## Files

| File | Route | Purpose |
|---|---|---|
| `part-1-core/frontend/src/pages/onboarding/Welcome.tsx` | `/welcome` | Post-login resume nudge (Flow 1). Shows once. |
| `part-1-core/frontend/src/pages/onboarding/Resume.tsx` | `/resume` | JD matcher + guided resume builder (Flow 2). **Also mount as sidebar LAUNCH → Resume** (same component). |
| `part-1-core/frontend/src/pages/onboarding/Subscription.tsx` | `/subscription` | Free/Pro/Expert plans (Flow 1, step M). |
| `part-1-core/frontend/src/pages/onboarding/MakePlan.tsx` | `/plan` | Subject + level wizard → starts placement (Flow 3). |
| `part-1-core/frontend/src/pages/onboarding/Verification.tsx` | `/verification` | Placement test stepper + per-level results (Flow 3). |
| `part-1-core/frontend/src/pages/onboarding/lib.ts` | — | Shared types + localStorage contracts. |
| `part-1-core/frontend/src/pages/onboarding/onboarding.css` | — | UX v2 tokens + page styles, scoped under `.ob` (never touches shell styles). Imported by each page. |

Suggested router wiring (shell owns `main.tsx`):

```tsx
const Welcome = lazy(() => import('./pages/onboarding/Welcome'));
const Resume = lazy(() => import('./pages/onboarding/Resume'));
const Subscription = lazy(() => import('./pages/onboarding/Subscription'));
const MakePlan = lazy(() => import('./pages/onboarding/MakePlan'));
const Verification = lazy(() => import('./pages/onboarding/Verification'));
// inside the authenticated layout (or Welcome standalone — your call):
<Route path="welcome" element={<Welcome />} />
<Route path="resume" element={<Resume />} />        {/* also the LAUNCH → Resume sidebar entry */}
<Route path="subscription" element={<Subscription />} />
<Route path="plan" element={<MakePlan />} />
<Route path="verification" element={<Verification />} />
```

## Router-state contract: /verification

MakePlan navigates with `navigate('/verification', { state })`. Do not
deep-link to `/verification` — the page redirects to `/plan` when state is
absent (placement sessions are single-use; refresh loses the session by design).

```ts
interface VerificationState {
  placement_id: string;      // from POST /api/v1/placement/start
  topic: string;             // e.g. "python"
  claimed_level: string;     // "intermediate" | "advanced"
  questions: Array<{         // public questions — answer keys NEVER included
    id: string; topic: string; level: string;
    prompt: string; choices: string[];
  }>;
}
```

## localStorage contracts (shell must honor)

| Key | Values | Meaning |
|---|---|---|
| `sf_welcome_seen` | `"1"` | Set when the user clicks "Skip for now" on `/welcome`. The nudge shows exactly once; returning visits redirect to `/`. |
| `sf_plan` | `"pro"` \| `"expert"` \| absent | **DEMO SCAFFOLDING.** Shell's "Go Pro" popup + plan badge read this key: present → hide popup, show PRO/EXPERT badge. Absent → fall back to the backend subscription tier (`GET /api/v1/account/subscription`). |

## Demo-purchase scaffolding (remove when real checkout lands)

`Subscription.tsx` contains a clearly-labeled dashed "DEMO ONLY" panel with
**Simulate Pro purchase / Simulate Expert purchase / Reset to Free**. It only
writes `localStorage['sf_plan']` — no payment is faked, the backend tier is
untouched. The Upgrade buttons call the real `POST /api/v1/account/subscription/checkout`,
which returns **501** today; the UI shows an honest "Checkout coming soon —
we'll notify you" state. Delete the `.ob-demo` block when Razorpay/Stripe KYC
is done.

## Backend endpoints used (all verified live, Oct 13 2026)

- `GET /api/v1/launchpad/resume` → 404 `{error:"no_resume"}` when absent
- `PUT /api/v1/launchpad/resume` → `{title,summary,skills,experience[],projects[],education[],links{}}`
- `POST /api/v1/launchpad/jd-match` `{jd_text}` → `{score, jd_keyword_count, matched:[{keyword,jd_count}], missing:[...], suggestions:[...]}`
- `GET /api/v1/account/subscription` → `{subscription:{tier,name,price_inr,features}, tiers:{free,pro,expert}}` — prices rendered from this, never hardcoded (₹0 / ₹299 / ₹799 verified in `app/domain/billing.py`)
- `POST /api/v1/account/subscription/checkout` `{tier}` → **501** `{error:"payments_not_connected"}`
- `GET /api/v1/placement/topics` → `{topics:["ml-basics","python"]}`
- `POST /api/v1/placement/start` `{topic, claimed_level}` → `{placement_id, verification_skipped, verified_level, questions[], ...}`
- `POST /api/v1/placement/{id}/submit` `{answers:{qid:choiceIdx}}` → `{analysis:{claimed_level, verified_level, correct, total, summary, levels:{lvl:{correct,total,ratio}}}}`
- `GET /api/v1/roadmaps/current` → **400** `{detail:"no roadmap yet — generate one first"}` when none
- `POST /api/v1/roadmaps/generate` `{gaps:[{skill,mastery_pct}], title}` → 201

Gap mapping (Verification → "Generate my roadmap"): levels with ratio < 0.7 →
one gap `{skill: topic, mastery_pct: worst_ratio*100}`; if everything passed,
one gap for the *next* level `{skill: "<topic> (<next> track)", mastery_pct: 0}`.

## Design

- Tokens (exact var names, defined in `onboarding.css` under `.ob`): `--base #080B14`, `--surface #121A2B`, `--border rgba(255,255,255,.10)`, `--violet #8B5CF6`, `--cyan #36C5F0`, `--green #39D98A`, `--amber #F5B84B`, `--red #F06C75`, `--text #F5F7FB`, `--muted #9AA6BB`.
- **Green discipline:** green is used ONLY for the verified-level badge when a level beyond beginner was genuinely verified. ATS ring is violet→cyan; level bars are cyan/amber/red by ratio.
- All pages have loading / error / empty states. No mock data anywhere (demo purchase panel excepted, labeled).

## Verified

- `tsc -b` clean, `vite build` clean.
- Live-backend E2E via Playwright (real registered user, real tokens): register →
  /plan → topic+level → /verification (8 Qs, stepper, submit) → per-level results
  → /resume (seeded resume, JD paste → ATS 47 ring + matched/missing + suggestions)
  → /subscription (real tiers/prices, 501 checkout, demo-purchase sets `sf_plan=pro`
  and the Pro card flips to CURRENT) → /welcome nudge for a resume-less user.
- Screenshots: `~/workspace/your_files/skillforge-v2/output/ux-v2-{make-plan,verification,verification-result,resume-ats,subscription}.png`.

## Gaps / notes for the shell agent

- `src/App.tsx` does not exist in this worktree (routing lives in `main.tsx`); nothing outside `src/pages/onboarding/` + this file was touched. `vite.config.ts` proxy still targets `localhost:8000` (the standard backend port); the live test backend ran on `:8001` via a local TCP forward.
- `Welcome` works best as a full-page (no sidebar) route — your call in the router.
- If the shell shows a plan badge, read `localStorage['sf_plan']` first, backend tier second (demo override wins).
