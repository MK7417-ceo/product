# Part 1 — SkillForge Core: SPECS

## 1. Onboarding diagnostic

Inputs: user picks tech focus (language or domain) + self-declared level per
topic. Behavior: serves 8–12 questions mixing theory, subjective, and
coding-concept across the focus's topics; adaptive — wrong answers step
difficulty down. Outputs: per-topic verified level (beginner / intermediate /
advanced) + the questions that determined it. Edge: user abandons mid-way →
session resumable 24h; all-correct → capped at "advanced" (expert needs a full
assessment).

## 2. Assessment session

Inputs: domain + level + idempotency_key. Behavior: composes hybrid set
(curated + AI-fresh, level-matched); serves without answer keys; accepts
answers only (never scores); deterministic grading for MCQ/numeric/known-code;
short reasoning → AI eval with confidence. Outputs: per-skill mastery % +
confidence %, session status completed. Edge: duplicate submit (same
idempotency key) → returns original result; submit after completion → 409.

## 3. Deterministic scoring (M4, kept)

Inputs: user_answer + question answer_key. Behavior: exact / numeric-tolerance /
test-based comparison, server-side. Outputs: score 0..1 per response,
graded_by="deterministic". Edge: malformed answer → score 0, logged, never
crashes.

## 4. AI evaluation (M5, kept + real LLM later)

Inputs: short-reasoning answer + rubric. Behavior: provider call with token /
timeout / cost caps; schema + business-rule validation (evidence quotes must
be verbatim substrings); confidence < 0.75 → human review queue. Outputs:
score, confidence, model + prompt versions. Edge: provider timeout → queued
for retry, session stays "grading"; cost cap hit → kill switch, deterministic
fallback where possible.

## 5. Gap analysis

Inputs: verified profile + target role/level. Behavior: ranks gaps by
(importance × gap size × prerequisite weight); each gap gets a one-line
reason. Outputs: ordered list {skill, current, target, priority, reason}.
Edge: no evidence for a skill → listed as "unassessed", never assumed zero.

## 6. Roadmap generation / regeneration

Inputs: gaps + skill graph (prerequisites respected). Behavior: tasks carry
title, why-it-matters, target skills, prerequisites, effort, priority,
expected evidence, acceptance criteria; regeneration creates a NEW version.
Outputs: versioned roadmap. Edge: regenerate with completed tasks → completed
tasks + evidence + history preserved; only future tasks reordered.

## 7. Domain tracks

Inputs: track enrollment (AI/ML, Python, C/C++ first). Behavior: track =
ordered skill-graph slice + assessments + projects + GitHub tutorials.
Outputs: track progress %, next action. Edge: track content missing for a
domain → "coming soon", never empty screens.

## 8. Daily questions

Inputs: user level + domain. Behavior: 2–5/day, level-matched, important
patterns weighted; never the identical set twice in a row. Outputs: questions
+ explanations after attempt. Edge: user skips days → no punishment, streak
pauses.

## 9. Weekly mocks

Inputs: domain. Behavior: 1 compulsory + 1 optional mock/week,
interview-style, time-bound; camera-ON notice + consent (user decision).
Outputs: mock score + breakdown. Edge: missed compulsory mock → reminder,
not lockout.
