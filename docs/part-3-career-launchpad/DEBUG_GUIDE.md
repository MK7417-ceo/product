# DEBUG_GUIDE — Part 3: Career Launchpad

## The playbook (every bug, every time)

1. **Reproduce** — exact steps, exact inputs, exact user/tier. No "it sometimes".
2. **Isolate the layer** — UI? API? domain core? provider webhook? Run the
   domain core directly with a fake adapter: if it passes there, the bug is
   in the adapter or the wire, not the logic.
3. **Request ID + logs** — every request carries `X-Request-ID`; grep
   structured logs for it. Billing: also grep `provider_event_id`.
4. **Provider dashboard cross-check** — Razorpay/Stripe dashboard shows the
   ground truth for payments; GitHub repo settings show the truth for Pages.
5. **Minimal repro** — smallest script/command that triggers it; attach to
   the BUGS.md entry.
6. **Fix + regression test** — every fix ships with a test that fails
   without the fix. No test, no close.

## Common failure catalog (Part 3 specific)

| Symptom | Likely cause | Check |
|---|---|---|
| Webhook 401s | signature secret mismatch / wrong env | compare `RAZORPAY_WEBHOOK_SECRET` with dashboard; test-mode vs live keys |
| Paid but still locked (402) | entitlement not recomputed after webhook | `billing_events.applied_at` null? replay guard swallowed it? |
| Double-charged / double-applied | webhook retried, idempotency missed | `provider_event_id` UNIQUE constraint hit? |
| GitHub publish fails | OAuth scope missing `repo`/`pages` | re-auth with correct scopes; token expiry |
| Pages URL 404 after publish | Pages build still running / wrong branch | repo Settings → Pages; wait ~2 min; check branch |
| Camera permission denied | browser/OS block, not our bug | show in-product help text; offer no-camera practice mode |
| Feedback feels generic | AI prompt fell back / low evidence | check eval run: confidence, evidence quotes present? |
| Resume has invented experience | tailoring prompt not constrained | verify "cite profile fact" rule in prompt version |

## Severity levels

- **S1:** money wrong (double charge, paid-but-locked) — stop everything, fix now.
- **S2:** feature broken for a tier (publish fails, mock won't start).
- **S3:** degraded (slow webhook apply, generic feedback).
- **S4:** cosmetic.

## Notes

- Never debug billing with live keys. Ever.
- Camera/media issues: reproduce in the same browser the user used —
  permissions are per-browser, per-origin.
- When in doubt, blame the adapter first: ports make the domain core the
  least likely suspect by design.
