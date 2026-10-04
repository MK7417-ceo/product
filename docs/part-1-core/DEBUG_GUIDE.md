# Part 1 — SkillForge Core: DEBUG_GUIDE

## The playbook (every bug, every time)

1. **Reproduce** — write the exact steps; note who/when/data. If you can't
   reproduce, you can't verify the fix. Capture `X-Request-ID` from the
   failing response header.
2. **Isolate the layer** — UI, API, domain, or DB?
   - UI: devtools console/network. Blank screen? → read the React error.
   - API: replay the request with curl + the request ID; read structured logs
     (`grep <request-id> logs/app.json`).
   - Domain: 10-line script calling the inbound port directly with a fake
     adapter. Fails here → business-logic bug.
   - DB: is the row there? Is the migration at the right head
     (`alembic current`)?
3. **Logs** — every line carries `request_id`, `user_id`, `duration_ms`. No
   request ID → the middleware is broken; fix that first.
4. **Minimal repro** — shrink to the smallest failing case; add it as a test.
5. **Fix + regression test** — fix at the right layer (don't patch UI for a
   domain bug). Ship the test with the fix (TESTING.md regression rule).

## Common failure catalog (Core)

| Symptom | Likely layer | First check |
|---|---|---|
| 401 on everything after ~30 min | auth | access token expired; is refresh rotation running? (30-min tokens) |
| Results page blank after submit | API/UI contract | response shape vs `AttemptResult` type — `mastery_percentage` present? (BUG-001) |
| `alembic upgrade` fails on fresh DB | migrations | heads diverged? `alembic heads`; never edit a merged migration |
| Seed says "already seeded" but tables empty | seed ledger | `seed_versions` row vs actual rows; re-run seed on scratch DB |
| AI eval stuck in "grading" | scoring/adapters | provider timeout? cost cap hit? check `ai_evaluation_runs` latency/cost |
| Gaps show "unassessed" for everything | evidence | responses graded but no `evidence_records`? check verification rule (≥70% + server-evaluated) |
| Roadmap regen lost tasks | roadmap | versioning broken — regen must INSERT new version, never UPDATE |

## Severity

- **S1** — auth broken, data loss, blank core screens. Stop everything, fix now.
- **S2** — feature wrong/degraded (bad scores, wrong gaps). Fix this phase.
- **S3** — cosmetic, copy, minor UX. Backlog.
