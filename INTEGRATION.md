# CodeLab M1 — Integration Notes

Branch: `feat/ux-v2-codelab` (frontend-only change; no backend touched).

## Files added / changed

| Path | What |
|---|---|
| `part-1-core/frontend/src/pages/CodeLab.tsx` | **default export** — M1 code runner page, route `/codelab` |
| `part-1-core/frontend/src/pages/CodeLab.css` | Scoped Aurora Dark styles (UX-v2 token names declared on `.codelab`) |
| `part-1-core/frontend/src/components/dsa/DailyDSACard.tsx` | **named export `DailyDSACard` + default export** — self-contained dashboard card |
| `part-1-core/frontend/src/components/dsa/DailyDSACard.css` | Scoped card styles |
| `part-1-core/frontend/src/lib/api.ts` | Added `codeApi` (`run`, `languages`), `dsaApi` (`daily`, `submit`) + typed interfaces (`CodeRunResult`, `EngineLanguage`, `DailyDSAQuestion`, `DSASubmitResult`) |
| `part-1-core/frontend/src/main.tsx` | Added `<Route path="codelab" element={<CodeLab />} />` under the Guarded shell |

`src/App.tsx`, `src/components/layout/*`, `src/index.css`, `src/styles/*` were **not** touched.

## Deep-link contract

`/codelab?date=YYYY-MM-DD` → fetches `GET /api/v1/dsa/daily?date=<date>` and shows that day's
DSA question (title, description, examples, hints, topic tags, hidden-test count) beside the
editor; the editor is seeded with the question's `starter_code`; a **Submit solution** button
appears that POSTs `/api/v1/dsa/daily/submit` `{date, language, code}` and shows
`passed/total`, Accepted/Rejected, and `failed_case`. No `date` param → plain code runner
(language select + editor + stdin + Run). Editor code is kept per-language in component state
and persisted to `localStorage` (`sf_codelab_code_v1`).

## DailyDSACard props

```ts
interface DailyDSACardProps {
  date?: string;      // YYYY-MM-DD; default = backend "today"
  className?: string; // extra classes
}
```

- Fetches `GET /api/v1/dsa/daily` (or `?date=`), shows title + difficulty badge
  (easy=cyan, medium=amber, hard=red — green is used **only** for the solved badge) +
  topic tags + `Solve →` linking to `/codelab?date=<question.date>`.
- Solved state: the backend has **no submit-history endpoint**, so the card reads a local
  `localStorage` list (`sf_dsa_solved_v1`) written by CodeLab when a submit is accepted.
  Keep it simple — no mock data.
- Dashboard agent: render `<DailyDSACard />` wherever the `DSA-SLOT` marker is.

## API shapes (verified live against backend at 127.0.0.1:8001)

- `GET /api/v1/code/languages` → `{languages: [{id, name, ...}]}` — **currently 502s**
- `POST /api/v1/code/run` `{language, code, stdin}` → `{run_id, verdict, stdout, stderr, truncated, exit_code, cpu_ms, peak_ram_mb, timed_out, server_ms}` — **currently 502s**
- `GET /api/v1/dsa/daily[?date=]` → `{id, title, difficulty, description, examples[{stdin,stdout,explanation}], starter_code, hidden_test_count, topic_tags, hints, date}` — **works**
- `POST /api/v1/dsa/daily/submit` → `{date, question_id, passed, total, verdict, accepted, failed_case}` — not exercised (engine down)

## Engine status observed (honest)

The **code engine is DOWN** in this environment: both `/code/languages` and `/code/run`
return `502 {"error":"engine_unreachable","message":"code engine unreachable: <urlopen error
[Errno 111] Connection refused>"}`. CodeLab handles this without mocking anything:

- Language select falls back to a static list (python/c/cpp/java) with an amber note that
  the engine is unreachable.
- Run shows an honest error box: "Run failed — nothing was executed / Engine returned HTTP
  502 (not executed). This usually means the code engine service is not running. Your code
  is safe in the editor; try again once the engine is back."
- Screenshots: `ux-v2-codelab-engine-error.png` captures this state.
- `/code/run` was **not** able to actually execute code here. Re-verify on a host where the
  engine runs before claiming end-to-end execution.

## Verification

- `npx tsc -b` clean; `npm run build` clean; `npx oxlint` 0 errors.
- Dev server (port 5177, `/api` → 8001) + Playwright (register → token injection) E2E:
  - `/codelab?date=2026-10-13` → Binary Search (easy) loads with starter code → screenshot
  - Run → honest 502 error state → screenshot
  - `DailyDSACard` standalone on dark bg (temp harness route, removed after) → screenshot
- Screenshots: `~/workspace/your_files/skillforge-v2/output/ux-v2-codelab.png`,
  `ux-v2-codelab-engine-error.png`, `ux-v2-dsa-card.png`.

## Gaps / follow-ups

- No DSA submit-history backend endpoint → solved badge is local-only (per browser).
- `dsa/daily` uses the server's UTC "today" (2026-10-12) while the user is IST (Oct 13) —
  the card passes the explicit `question.date` in the deep link, so this is consistent.
- Editor is a styled textarea with a synced line-number gutter (no heavy editor dep added).
- Playwright note: `page.add_init_script` did not take effect in this env; seeding
  `localStorage` via `evaluate` after an initial same-origin navigation worked.
