# P1-PAGES Integration Notes — feat/ux-v2-p1pages

Milestone 1 UX rebuild: migrated pages into the Aurora Dark token system.
Branch: `feat/ux-v2-p1pages` (worktree `~/workspace/wt-p1pages`).

## Files added (all new, none modified)

| File | Source branch | Notes |
|---|---|---|
| `part-1-core/frontend/src/pages/Roadmap.tsx` | `origin/feat/f8b-pages` | Generate form; progress header; task cards; task-detail + evidence-submit as slide-over panel; regenerate via inline form (replaces `prompt()`) |
| `part-1-core/frontend/src/pages/Practice.tsx` | `origin/feat/f8c-practice-page` | Aaj ka plan: today's roadmap tasks + 3 daily questions, server-scored |
| `part-1-core/frontend/src/pages/SkillProfile.tsx` | **none existed** — built fresh from real API shapes | Verified/gap/claimed states from live data only (see below) |
| `part-1-core/frontend/src/pages/Evidence.tsx` | **none existed** — built fresh from real API shapes | Aggregates per-task evidence; detail as slide-over panel |
| `part-1-core/frontend/src/pages/Certificates.tsx` | `origin/feat/p3d-certificates-ui` | Earn card, earned list + copy chip, verify as slide-over panel (public endpoint) |
| `part-1-core/frontend/src/pages/Portfolio.tsx` | `origin/feat/p3f-portfolio-ui` | Preview + publish/export as slide-over panel (download + manual Pages steps) |
| `part-1-core/frontend/src/pages/InterviewPrep.tsx` | `origin/feat/p3h-prep-ui` (was `Interview.tsx`) | Question bank / typing test / PI mock as TABS inside the one page |
| `part-1-core/frontend/src/pages/English.tsx` | `origin/feat/p3j-english-ui` | Daily drill panel (5 Qs, server-scored) |
| `part-1-core/frontend/src/pages/Settings.tsx` | `origin/feat/p3l-settings-ui` | Subscription tiers + Integrations section (GitHub/LinkedIn/LeetCode link status, honest coming-soon notes) |
| `part-1-core/frontend/src/pages/p1-pages.css` | new | Token scope + shared P1 component styles |
| `part-1-core/frontend/src/lib/p1api.ts` | typed from `origin/feat/p3l-settings-ui:…/src/lib/api.ts` | Reuses `api()`/`ApiError`/`getAccessToken` from shared `src/lib/api.ts` — shared files NOT edited |

## Tabs-vs-routes decisions (sitemap principle)

- Roadmap task detail + evidence submit → slide-over **panel** inside Roadmap page.
- Evidence submission detail → slide-over **panel** inside Evidence page.
- Certificate verify view → slide-over **panel** inside Certificates page.
- Portfolio export/publish → slide-over **panel** inside Portfolio page.
- Interview modules (question bank / typing test / PI mock) → **tabs** inside InterviewPrep.
- English drill → **panel** inside English (no fake sub-tabs; backend has one daily set).
- NOT built, per scope: Skill Gaps page, Resources entry, notifications page, Presentation/Extempore/GD modules.

## Pages with no source branch (built fresh, real data only)

- **SkillProfile**: `GET /assessments` (latest completed session per topic → measured pct),
  `GET /profiles/me` (self-claimed skills not yet measured → muted "self-claimed" pills,
  never counted as verified), full assessment history. Green (≥70%) ONLY for verified.
- **Evidence**: `GET /roadmaps/current` + per-task `GET /roadmaps/tasks/{id}/evidence`,
  filterable by kind, detail panel shows content + feedback.

## API verification (live backend 127.0.0.1:8001)

All response shapes read from `~/workspace/be-test/part-1-core/app/api/v1/*.py` and
verified live with two seeded users (register → profile → assessments → roadmap →
evidence → cert issue → resume → links). Endpoints exercised during screenshot runs:
`/auth/login`, `/profiles/me`, `/assessments` (+start/submit), `/roadmaps/generate|current`,
`/roadmaps/tasks/{id}` (PATCH), `/roadmaps/tasks/{id}/evidence` (GET+POST),
`/practice/today`, `/practice/daily/submit`, `/english/daily` (+submit),
`/prep/topics`, `/prep/questions`, `/launchpad/certificates` (+issue),
`/launchpad/certificates/verify/{code}` (public), `/launchpad/resume` (PUT),
`/launchpad/portfolio`, `/account/subscription`, `/account/links` (GET+PUT).

## Design tokens

`.p1x` scope in `p1-pages.css` defines the mandated vars:
`--base:#080B14 --surface:#121A2B --border:rgba(255,255,255,.10) --violet:#8B5CF6
--cyan:#36C5F0 --green:#39D98A --amber:#F5B84B --red:#F06C75 --text:#F5F7FB
--muted:#9AA6BB`. Green is used ONLY for verified evidence / perfect drill scores
(drill score numbers are cyan otherwise). No shell/agent files touched:
`src/main.tsx`, `src/components/*`, `src/styles/*`, `vite.config.ts` untouched
(temp screenshot wiring was applied and fully reverted — verified via diff).

## Routes (for the shell agent)

Pages are default exports, ready to wire in `src/main.tsx`:
`/roadmap`→Roadmap, `/practice`→Practice, `/skill-profile`→SkillProfile,
`/evidence`→Evidence, `/certificates`→Certificates, `/portfolio`→Portfolio,
`/interview`→InterviewPrep, `/english`→English, `/settings`→Settings.
Screenshots used exactly these paths on dev port 5178 (reverted after).

## Screenshots

`~/workspace/your_files/skillforge-v2/output/`:
ux-v2-p1-roadmap.png, ux-v2-p1-practice.png, ux-v2-p1-skillprofile.png,
ux-v2-p1-evidence.png, ux-v2-p1-certificates.png, ux-v2-p1-portfolio.png,
ux-v2-p1-interviewprep.png, ux-v2-p1-english.png, ux-v2-p1-settings.png.

## Known gaps / follow-ups

- `prompt()` in the f8b regenerate flow replaced with an inline form (same API).
- Drill score banners: cyan unless perfect (green reserved for verified).
- Certificates "Issue my certificate" stays enabled after issuing (matches source behavior;
  backend permits re-issue — may want a guard later, not my call).
- The 9 pages are not yet routed — shell agent owns `src/main.tsx`.
- node_modules/ installed locally for build/verify (untracked).
