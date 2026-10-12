# Skill Gaps page — integration notes (UX v2 rebuild, Milestone 1)

Branch: `feat/ux-v2-skillgaps` (this worktree: `~/workspace/wt-skillgaps`)

## Files changed

| File | Change |
|---|---|
| `part-1-core/frontend/src/pages/SkillGaps.tsx` | **New.** Default-export page at route `/gaps`. Aggregates verified skill gaps across all completed assessments; gap rows with severity badges + 3 actions; per-assessment expandable breakdown; loading / error / empty states. No mock data. |
| `part-1-core/frontend/src/main.tsx` | Added `import SkillGaps` and `<Route path="gaps" element={<SkillGaps />}/>`. |
| `part-1-core/frontend/src/components/Shell.tsx` | Added `{ to: '/gaps', label: 'Skill Gaps' }` to `LINKS` (sits after Assessment, before Roadmap). Note: this shell is the rebuild placeholder — when the shell agent ships the grouped PROVE sidebar, move this link under PROVE → "Skill Gaps". |
| `part-1-core/frontend/vite.config.ts` | `/api` proxy target `http://localhost:8000` → `http://127.0.0.1:8001` (the live backend that serves the new gap endpoints). |

Forbidden files untouched: no `src/App.tsx` exists in this tree (routes live in `main.tsx`); `src/styles/*` not edited (page reuses theme classes `page-title`, `page-sub`, `card`, `grid4`, `stat`, `btn`, `btn-ghost`, `coming` + inline styles on the design tokens).

## Data flow

1. On mount: `GET /api/v1/assessments` → for every assessment with `status === "completed"`, `GET /api/v1/assessments/{id}` (detail adds `per_skill: [{skill, correct, total}]`). Detail failures degrade gracefully to the summary row.
2. Aggregation (client-side, `useMemo`):
   - A skill is a gap iff `correct/total < 0.70` (backend definition).
   - Grouped by skill; if it gaps in multiple assessments, **worst ratio wins** (best correct/total replaced by the lower one); source assessments (topic · level chips) accumulate without duplicates.
   - Severity: ratio < 0.40 → `high` (red), else `medium` (amber).
3. Display order: weakest ratio first. Stats row: total gaps, high-severity count, completed assessments, weakest skill.

## Actions per gap row

- **Practice this skill** → `navigate('/practice')` (page owned by the Practice slice).
- **Add to roadmap** → `GET /api/v1/roadmaps/current`; 200 → `POST /api/v1/roadmaps/regenerate`, 400/404 → `POST /api/v1/roadmaps/generate`; payload `{gaps:[{skill, mastery_pct: round(ratio*100)}]}`. Success shows `✓ Roadmap vN ready — "<skill>" queued` inline (green); failure shows the error inline (red). Only 400/404 fall through to generate — other errors rethrow.
- **Reassess** → `navigate('/assessment')`. ⚠️ Task spec said `/plan`, but no `/plan` route exists in this tree (would be a dead link); routed to the existing `/assessment` placeholder instead. If the coordinator adds a `/plan` route, swap the target.

## States

- **Loading:** "Analyzing your assessment results…" card.
- **Error:** card with the backend message + Retry button (re-runs the load).
- **Empty:** centered card — "No skill gaps found", actionable CTA "Take an assessment to discover yours →" linking to `/assessment` (not `/plan`, same reason as above).
- No mock data anywhere; per-skill rows ≥70% in the breakdown show green `✓ N%` and are excluded from the gaps list.

## Live-backend verification (all done against http://127.0.0.1:8001)

- `POST /assessments/start {topic:"python",level:"beginner",count:4}` → 201; `POST /assessments/{id}/submit {answers:{}}` → 200, `per_skill:[{skill:"python-basics",correct:0,total:4}]`, `gaps:["python-basics"]`.
- `GET /assessments` → 200 list with gaps; `GET /assessments/{id}` → adds `per_skill`. Answer keys never leave the server (verified in responses).
- `POST /roadmaps/generate {gaps:[{skill,mastery_pct}]}` → 201 v1 (3 tasks targeting the gap skill); `GET /roadmaps/current` 400 → 200 after generate; `POST /roadmaps/regenerate {gaps:[...]}` → 201 v2.
- Playwright E2E (headless Chromium, dev server :5179, token injection): page rendered populated + empty states; clicked "Add to roadmap" → inline `✓ Roadmap v3 ready — "python-basics" queued`, backend confirmed v3 with 3 python-basics tasks; expanded breakdown panel renders; "Practice this skill" → `/practice`, "Reassess" → `/assessment`.

## Checks

- `npx tsc --noEmit` — clean.
- `npx vite build` — clean (dist/ built).
- Screenshots: `~/workspace/your_files/skillforge-v2/output/ux-v2-p1-skillgaps.png` (populated, expanded breakdown, roadmap success), `ux-v2-p1-skillgaps-empty.png` (empty state).

## Rollback

- Revert the single commit on `feat/ux-v2-skillgaps` (`git revert HEAD`) or `git reset --hard <base>`; deletes the page, route, nav link, and proxy change. No backend/migration impact (read-only usage of existing endpoints + new ones).

## Open for the coordinator

1. Shell agent's grouped PROVE sidebar: move the `/gaps` link there when it ships.
2. `/practice` and `/assessment` are placeholders owned by other slices — the buttons navigate there by contract only.
3. If a real `/plan` route is introduced, change the empty-state CTA and "Reassess" targets from `/assessment` to `/plan`.
