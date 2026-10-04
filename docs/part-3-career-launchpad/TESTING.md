# TESTING — Part 3: Career Launchpad

**Rule: no phase is "done" until BOTH lanes pass. Billing is NEVER tested with
real money — test mode / sandbox keys only.**

## Agent lane (run on the agent's end, evidence attached to the phase report)

Exact commands (backend repo root):

```bash
# full Part 3 module tests
pytest backend/tests/test_part3_billing.py backend/tests/test_part3_resume.py \
       backend/tests/test_part3_portfolio.py backend/tests/test_part3_hiring.py -v

# entitlement matrix: free/pro/expert × every gated endpoint
pytest backend/tests/test_part3_entitlements.py -v

# webhook signature tests with FakePaymentGateway + tampered payloads
pytest backend/tests/test_part3_webhooks.py -v

# GitHub publish against a disposable TEST repo (never a real user repo)
GITHUB_TEST_REPO=skillforge-publish-test pytest backend/tests/test_part3_publish.py -v

# migrations reversible
alembic upgrade head && alembic downgrade -1 && alembic upgrade head

# frontend
npx tsc --noEmit && npm run build
```

Evidence required: pasted test counts (e.g. "47 passed, 0 failed"), webhook
replay/idempotency proof, one screenshot of a test-mode checkout completing.

## Developer lane (user's Codespace checklist — what "working" looks like)

**P3.1 billing:** open test-mode checkout → pay with Razorpay test card
`4111 1111 1111 1111` → land back → `GET /billing/entitlements` shows Pro →
hit a Pro-gated endpoint (200) → cancel → at period end it's 402 with
upgrade hint. Working = paid features unlock and relock exactly on schedule.

**P3.2 resume:** paste a real JD → download PDF → open it: single column,
no graphics, your real skills only, missing JD keywords flagged. Working =
you'd actually send this to a recruiter.

**P3.3 portfolio:** run the 7-step builder → Publish → repo appears on YOUR
GitHub → Pages URL live → `git pull` works locally. Working = you own the
code and the site is live.

**P3.4 hiring:** run one full mock PI with camera ON → consent modal appears
first → complete → feedback shows 4 dimensions with evidence quotes →
challenge one dimension → it lands in the review queue. Working = feedback
feels specific to YOUR answers, not generic.

**P3.5:** issue a certificate → verify at the public URL → revoke → verify
shows revoked. Link GitHub account → one-click share produces correct text.

## Lane-failure policy

Agent lane red → fix, re-run, never hand to developer. Developer lane
"looks wrong" → it's a bug even if agent lane is green; file in BUGS.md,
fix, both lanes re-run.
