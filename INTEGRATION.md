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
| `/evidence` | Evidence | placeholder |
| `/certificates` | Certificates | placeholder |
| `/portfolio` | Portfolio | placeholder |
| `/interview` | InterviewPrep | placeholder |
| `/english` | English | placeholder |
| `/settings` | Settings | placeholder |
| `/profile` | Profile (real) | SHELL |
| `/billing` | Billing (real) | SHELL |
| `*` | → redirect `/` | SHELL |

NOT created (per spec): `/notifications`, `/skill-gaps`, `/resources`.

## Breadcrumb mapping (`CRUMBS` in TopNav.tsx)

/→Dashboard, /welcome→Welcome, /resume→Resume, /subscription→Subscription,
/plan→Assessment, /verification→Verification, /roadmap→Roadmap, /practice→Practice,
/codelab→Code Lab, /skills→Skill Profile, /evidence→Evidence, /certificates→Certificates,
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

