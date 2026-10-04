# SPECS — Part 3: Career Launchpad

## 1. Subscription tiers + entitlements matrix

| Feature | Free ₹0 | Pro ₹249/mo (₹1,999/yr) | Expert ₹599/mo (₹4,999/yr) |
|---|---|---|---|
| Typing / quant tests | 5/mo | unlimited | unlimited |
| AI mock interviews (PI/GD/extempore) | 1/mo, no camera | 4/mo, camera | 12/mo, camera + priority eval |
| IELTS track | — | weekly | weekly + detailed rubric |
| JD→ATS resumes | 3/mo | unlimited | unlimited |
| Portfolio publish → GitHub | — | yes | yes |
| Certificates (in-product) | — | yes | yes |
| New-domain early access | — | — | yes |

Quotas enforced per user per month even on paid tiers (fair-use caps);
overage returns 402 with upgrade/renewal hint, never silent failure.

## 2. Checkout flow

1. `POST /billing/checkout {tier, provider, billing_cycle}` → provider
   checkout session URL (test mode until KYC complete).
2. User pays on provider-hosted page (we never see card data).
3. Provider → `POST /billing/webhook/{provider}` with signature header;
   signature verified → `billing_events` recorded (idempotent on
   provider_event_id) → subscription + entitlements updated → receipt email.
4. Unverified signature → 401, logged, never applied.

## 3. JD → ATS resume generation rules

- Input: pasted JD text (≤10k chars) + user's verified profile/skills.
- Keyword extraction: deterministic (TF + skill-graph terms); tailoring of
  bullet wording via AI behind M5 budget cap; every AI claim must cite a
  profile/project fact — no invented experience.
- Output constraints (ATS-safe): single column; fonts Arial/Calibri/Georgia;
  no graphics, tables, text boxes, headers/footers with content; standard
  section heads (Summary, Skills, Experience, Projects, Education).
- Confidential fields never requested; placeholders like `[PHONE — fill in]`.
- Result stored with `jd_hash` for dedup; PDF + DOCX downloads.

## 4. Portfolio builder — 7 steps, ~1 week

1. Template pick (Aurora Dark styled). 2. About + contact. 3. Import verified
   skills (from Part 1 profile — never self-typed levels). 4. Import projects
   (from in-product work). 5. Experience/education. 6. Review + preview.
7. Publish: GitHub OAuth → create repo (`<user>.github.io` or `portfolio`) →
   push static files → enable Pages → return live URL. Existing-portfolio
   link field stays separate and untouched. Builder state saved; resumable.

## 5. Mock interview flow (camera)

1. Pre-flight: explicit consent modal (what's captured, retention = none,
   tab-switch flags recorded) → consent timestamp stored; user may choose
   no-camera practice mode instead.
2. Session: timed prompts per kind (PI/GD/extempore/presentation/IELTS);
   tab-switch/blur events logged as flags.
3. Completion: AI feedback on knowledge / confidence-proxy / expression /
   timing, each with a quoted evidence snippet and a confidence value.
4. Feedback labeled as feedback, not objective truth.

## 6. AI feedback challenge flow

- User clicks "challenge" on any dimension → entry in human-review queue
  (reviewer role, separation of duties — never own items, per Part 1 M9).
- Reviewer upholds/adjusts with a note; user notified; original + revised
  scores both retained (history never rewritten).
- Low-confidence + high-impact auto-queues for review without user action.

## 7. Certificate issuance

- Issued only against real evidence (completed mocks, verified skills);
  `code` UNIQUE, QR → public verify page; `revoked_at` supported.
- Free external certificate opportunities surfaced as links (curated list),
  separate from in-product certificates.
