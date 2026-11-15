# SKILLFORGE V2 — Launch Readiness & First-Revenue Plan

**Status:** NOT YET READY FOR A PUBLIC PAID LAUNCH  
**Purpose:** Evidence-based release gates and a practical first-customer plan. This document does not claim untested features work.

## 1. First-release product promise

SKILLFORGE helps Indian students and freshers move from claimed skills to demonstrated skills through:
1. Structured diagnostic assessment.
2. Transparent skill-gap report.
3. Role-focused learning roadmap.
4. Practice and task completion.
5. Evidence submission and review.
6. A shareable skill profile distinguishing self-reported, assessed and independently verified skills.

**Initial audience:** BCA, MCA, BTech and other early-career students/freshers.  
**Initial tracks:** Data Analyst and Python Developer.

Do not market guaranteed placement, guaranteed salary, employer-recognised certification or independently verified skills unless the corresponding process and evidence actually exist.

## 2. Current engineering status (rechecked 15 November 2026)

| Area | Finding | Launch consequence |
|---|---|---|
| Backend/core | Latest full CI: 491 passed; clean Alembic upgrade passed | PASS for current automated suite; keep regression tests in CI |
| Frontend | TypeScript/production build and lint passed in CI | PASS for build/lint; browser E2E and mobile QA remain unverified |
| Code Engine | 18 passed, 14 skipped on GitHub-hosted runner because network namespaces are unavailable | BLOCKED for full sandbox certification; run adversarial integration tests on hardened Linux |
| Sandbox privilege drop | Fail-closed privilege dropping is implemented and covered by the current CI path | Code change PASS; production isolation boundary remains NOT TESTED |
| Evidence | Submission is pending review; only admin can review globally; stale-roadmap evidence is rejected | Core workflow automated tests PASS; tenant-scoped reviewer permissions are not implemented |
| Billing | Checkout remains HTTP 501 / not connected | BLOCKED; do not sell subscriptions or grant paid entitlements |
| Integration docs | A prior audit flagged possible conflict markers; current file still needs a dedicated check | NOT VERIFIED; validate before release |
| Manual QA | Full browser, accessibility, and mobile journey has not been signed off | NOT TESTED; complete staging QA |
| Time handling | User-timezone behavior has not been revalidated in this release | NOT VERIFIED; test configured timezone and India default |

CI evidence: GitHub Actions run 43689849360 on the exact application tree reports 491 core tests passed, clean migration passed, frontend build/lint passed, and Code Engine 18 passed / 14 skipped. The skipped sandbox integration tests are not a security sign-off.

## 3. P0 — Required before public launch

### Security and privacy
- [ ] Code execution uses a proven OS/container isolation boundary, non-root identity, no network, restricted filesystem, and CPU/memory/process/time/output limits.
- [ ] Any failure to establish isolation aborts execution (fail closed).
- [ ] Adversarial tests cover privilege escalation, filesystem/network access, fork bombs, memory exhaustion, timeouts and output flooding.
- [ ] Production secrets are strong, unique and environment-managed.
- [ ] HTTPS, CORS, trusted hosts, rate limits, auth/session expiry and password reset are production-configured.
- [ ] User data access is tenant-scoped and authorization-tested.
- [ ] Privacy policy, terms, refund/cancellation policy and support contact are published.
- [ ] Data deletion/export and retention behavior are documented and tested.
- [ ] Logs never expose passwords, tokens or API keys.

### Skill evidence integrity
- [ ] Evidence lifecycle: SUBMITTED → PENDING_REVIEW → VERIFIED / REJECTED / NEEDS_CHANGES.
- [ ] Task completion and verified-skill status are separate.
- [ ] Self-reported evidence is visibly labelled.
- [ ] Reviewers can inspect evidence, record a reason and leave an audit trail.
- [ ] Users can resubmit after NEEDS_CHANGES.
- [ ] Certificates/profile badges are issued only under explicit documented criteria.

### Core product journey
- [ ] Visitor understands the product and can start onboarding.
- [ ] Registration, login, logout, password reset and session refresh work.
- [ ] User completes diagnostic assessment and receives a reproducible result.
- [ ] Skill gaps map to defined requirements for the selected role.
- [ ] Roadmap tasks have clear outcomes, effort estimates and acceptance criteria.
- [ ] Practice submissions persist and update progress correctly.
- [ ] Evidence submission, review and verified profile states work end-to-end.
- [ ] Every core screen has loading, empty, error and retry states.
- [ ] Mobile viewport has no blocking overflow or unusable controls.

## 4. P1 — Required before accepting payments

- [ ] Payment provider account and required business/KYC steps are completed by the operator.
- [ ] Server creates payment orders; the client cannot assign itself a paid plan.
- [ ] Signed provider webhooks verify payment and are idempotent.
- [ ] Refund, cancellation, failed-payment and renewal states are handled.
- [ ] Backend enforces entitlements on every paid API/action.
- [ ] Price, billing interval, taxes if applicable, refund policy and renewal terms appear before checkout.
- [ ] Test-mode payments pass before live keys are enabled.
- [ ] Support contact and customer support process are operational.

Never store card details. Never trust a redirect/success screen as proof of payment. Never put provider secrets in frontend code or Git.

## 5. Suggested first-revenue model (validate, do not assume)

| Plan | Proposed price | Scope |
|---|---:|---|
| Free Beta | ₹0 | One diagnostic, basic skill-gap snapshot, starter roadmap |
| Pro Monthly | ₹299/month | Full role roadmap, practice sets, progress history and portfolio/profile tools |
| Pro Annual | ₹1,999/year | Same Pro features at an annual discount |

These are pricing hypotheses, not validated market prices. Only list features that are implemented and tested. Do not sell human verification, certificates, mentor review, interview guarantees or placement promises until delivery is real.

### First 30 days
1. Recruit 20–30 students/freshers for a free guided beta.
2. Observe 10 users completing onboarding → assessment → roadmap.
3. Ask what outcome they would pay for, what they currently use and what they distrust.
4. Measure signup-to-assessment completion, assessment-to-roadmap conversion, weekly return rate, evidence submissions, support requests and willingness to pay.
5. Offer a clearly described limited paid pilot only after the workflow, support and refund terms are ready.
6. Avoid paid ads until organic onboarding and retention show evidence of value.

### Customer acquisition
- College placement cells, coding clubs, student communities and faculty referrals.
- Short demos showing real diagnostics and roadmaps—not fabricated placement outcomes.
- Free workshops: “Know your Data Analyst/Python Developer skill gaps.”
- Referral invitations after a user completes a meaningful product outcome.
- Obtain consent before using testimonials, student work or personal data in marketing.

## 6. Release engineering
- [x] CI runs backend tests, frontend typecheck/build/lint, Code Engine tests and a clean Alembic upgrade check.
- [ ] Add security/dependency scanning and browser E2E; these are not covered by the current CI run.
- [ ] Staging mirrors production configuration.
- [ ] Database migrations, backups and rollback are tested.
- [ ] Error monitoring, uptime monitoring and structured logs are enabled.
- [ ] Health/readiness endpoints check dependencies appropriately.
- [ ] Domain, HTTPS, email delivery, CORS and environment variables are configured.
- [ ] Release tag and changelog identify the deployed commit.
- [ ] Post-deployment smoke test is completed.

## 7. Release decision

Do not call the product ready for paid launch until all P0 and P1 checks pass with evidence.

An invite-only beta may begin earlier only if authentication, privacy, data isolation and core assessment/roadmap flows are safe and working. Keep public code execution disabled until sandbox isolation is proven. Keep paid checkout disabled until server-verified payments and refund/support processes are complete.

## 8. Evidence required for sign-off
- CI run on exact release commit.
- Frontend build and lint output.
- Code Engine security review and adversarial test results.
- Browser E2E report for desktop and mobile.
- Staging smoke-test checklist.
- Privacy/terms/refund policy URLs.
- Payment test-mode and webhook verification results.
- Backup/restore and rollback evidence.
- 10-user usability notes and beta metrics.

**Release owner sign-off:** Product pending · Engineering/security pending · Operations/payment pending · Customer support pending
