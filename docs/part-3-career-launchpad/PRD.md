# PRD — Part 3: Career Launchpad

**Status:** DRAFT (requirements locked 2026-10-04). **Part of:** SKILLFORGE v2 program.

## Vision

Part 1 teaches the skills; Part 2 proves them in code. **Part 3 gets the user
hired.** It turns verified skill evidence into hiring outcomes: interview-ready
through realistic mocks, a JD-tailored ATS resume, a live portfolio on the
user's own GitHub, and recognized certificates — behind a subscription model
that funds the platform.

## Personas

1. **Rahul, 21 — Final-year student, job seeker (India).** Knows Python/ML
   basics, has never faced a real interview. Needs: typing/quant practice,
   mock interviews with honest feedback, a resume that passes ATS filters,
   and a portfolio that looks expert-level. Price-sensitive → Free → Pro path.
2. **Priya, 24 — Abroad aspirant.** Targeting foreign companies. Needs:
   IELTS-level English track, presentation/extempore practice, PI feedback on
   expression and timing. Will pay Expert tier if the English track is real.
3. **Arjun — Mentor / admin.** Reviews challenged AI feedback, curates new
   domains flagged by the trend watcher, issues certificates. Needs: review
   queues, challenge resolution workflow, curation tooling.

## Goals

- G1: A user can complete a full mock interview (camera-ON, proctored) and
  receive dimension-scored feedback they can act on.
- G2: A user can generate a job-specific, ATS-friendly resume from any pasted JD.
- G3: A user can build and publish an expert-level portfolio to their own
  GitHub in ~1 week of guided steps.
- G4: Subscriptions (Free/Pro/Expert) gate features correctly; billing works
  in test mode end-to-end before any real money moves.
- G5: Certificates issued are verifiable and tied to real evidence.

## Non-goals

- No job marketplace, no employer dashboards, no job matching (out of scope).
- No automatic posting to LinkedIn/LeetCode (their APIs don't allow it —
  honest limitation, communicated to the user).
- No long-term storage of interview video (privacy rule).

## Features — Must / Should / Won't

**Must:** subscription tiers + entitlements + checkout (Razorpay test mode);
entitlement checks on every gated endpoint; JD→ATS resume generator;
portfolio builder (7-step) + publish to user's GitHub via OAuth + Pages;
mock interview flow with camera consent + tab-switch flags; AI feedback on
knowledge/confidence-proxy/expression/timing with challenge → human review;
typing + quant test modules; certificate issuance + verification page.

**Should:** presentation + extempore modules; GD module; IELTS-level English
track; account linking (Google/GitHub OAuth) + one-click share/export;
LeetCode deep-link nudge; trend watcher (flagging + admin curation flow).

**Won't:** auto-posting to LinkedIn/LeetCode; video retention beyond the
session; in-house payment processing (provider-hosted checkout only).

## Key user stories

- US1: As Rahul, I paste a JD and download a tailored ATS resume in under
  2 minutes, so I can apply today.
- US2: As Rahul, I run a mock PI with camera ON, get feedback on my weak
  answers, and can challenge a score I disagree with.
- US3: As Priya, I follow the IELTS track weekly and see my expression/
  timing scores improve over a month.
- US4: As Rahul, I finish the 7-step portfolio builder and my portfolio is
  live at `rahul.github.io` — code I own.
- US5: As a free user hitting a paywall, I see exactly what Pro unlocks and
  can upgrade via Razorpay test checkout.

## Acceptance criteria (sample)

- AC1: JD→resume output is single-column, standard fonts, no graphics/tables;
  ≥80% of JD keywords present or explicitly flagged as missing.
- AC2: Mock interview cannot start without explicit camera consent; consent
  timestamp + scope stored; no video file retained after session ends.
- AC3: Portfolio publish creates a repo on the USER's GitHub (not ours),
  enables Pages, and returns the live URL; existing-portfolio link stays
  separate and untouched.
- AC4: Expired subscription → gated endpoints return 402 with upgrade hint;
  no silent feature loss mid-session.
- AC5: Every billing webhook is signature-verified; unverified webhooks are
  rejected and logged, never applied.

## Success metrics

- Mock completion rate ≥ 60% of started mocks.
- Resume downloads per active user per month.
- Portfolio publishes (repo created + Pages live).
- Free → Pro conversion ≥ 3% within 90 days of launch.
- Challenge rate on AI feedback < 15% (proxy for feedback quality).

## Risks

- **Payment KYC delays:** Razorpay/Stripe production payouts need business KYC —
  start paperwork early; test mode unblocks all development.
- **Camera-privacy concerns:** mitigate with explicit consent, visible
  recording indicator, zero retention, and a no-camera practice mode.
- **LinkedIn/LeetCode API limits:** no auto-post promises; linking + share/
  export + deep-link nudges only.
- **AI feedback disputes:** challenge → human review queue; feedback labeled
  as feedback, never objective truth.
