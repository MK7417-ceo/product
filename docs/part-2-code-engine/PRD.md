# Part 2 — Code Execution Engine: PRD

**Status:** APPROVED as plan (2026-10-04). **Build state: NOT BUILT.** This PRD is
the contract the implementation will be judged against.

## Vision

Give every SKILLFORGE learner a safe, instant, GFG/W3Schools-like "write code →
run → see output" experience inside the product — on any device including phones —
without the product ever trusting user-submitted code. Untrusted code runs only
in isolated Docker containers on a dedicated runner host, never near user data.

## Personas

1. **Aarav, the learner (17–24, phone-first, Tier-2/3 India).** Prepares for
   placements. Writes Python/C++ in the in-browser editor during practice and
   assessments, expects output in seconds, and needs the editor to be usable on
   a 6-inch screen. Cares about: speed, clear error messages, no setup.
2. **Meera, the platform admin.** Responsible for infra cost and safety. Cares
   about: zero container escapes, bounded cost per run, abuse detection, and a
   plagiarism signal she can trust enough to send to human review — never an
   auto-ban.

## Goals

- G1: Execute untrusted code for Python, C, C++, Java with hard resource limits
  and p95 end-to-end latency under 8s for typical runs.
- G2: Zero sandbox-escape / host-impact security incidents.
- G3: Mobile-friendly editor UX (the user is phone-first).
- G4: Plagiarism signal that flags suspicious similarity for human review with a
  documented low false-positive rate — never auto-punishment.

## Non-goals

- NOT building a compiler or interpreter from scratch (explicit user decision;
  industry uses standard toolchains in sandboxes).
- NOT a full IDE (no debugger, no multi-file projects in v1).
- NOT auto-grading beyond running code against provided test cases in v1
  (verdicts: Accepted / Wrong Answer / TLE / MLE / Runtime Error / Compile Error).
- NOT real-time collaborative editing.

## Features — Must / Should / Won't

**Must (P2.1–P2.3):**
- M1: `POST /v1/run` — submit code + language + stdin, get stdout/stderr/exit/verdict.
- M2: Docker-based isolation: no network, CPU/RAM/wall-time/output caps per run.
- M3: Separate runner host from Core (security non-negotiable).
- M4: Language matrix v1: Python 3.12, GCC C11, G++ C++17, OpenJDK 17.
- M5: In-browser editor UX (Aurora Dark): run button, stdin box, output panel,
  compile/runtime errors shown plainly, mobile-usable.
- M6: Plagiarism pipeline: normalize (strip comments/whitespace, canonicalize
  identifiers, exclude starter code) → structural fingerprint → similarity score
  → flag for human review. Never auto-punish.

**Should (P2.4):**
- S1: Async job mode for long runs (`POST /v1/jobs`, poll `GET /v1/jobs/{id}`).
- S2: Per-user run quotas + rate limits (abuse/cost control).
- S3: Editor niceties: dark/light already Aurora; add line numbers, tab size,
  font-size control, sample test-case runner.

**Won't (v1):**
- W1: New languages beyond the v1 matrix (JS/Go/Rust later, behind the same port).
- W2: Persistent user file systems or package installs inside the sandbox.
- W3: GPU execution.

## Key user stories

- US1: As Aarav, I paste my Python solution, press Run, and see output or a
  clear error within seconds — on my phone.
- US2: As the assessment engine (Core), I submit candidate code + hidden test
  cases through `CodeRunnerClient` and get a deterministic verdict per case.
- US3: As Meera, I see a plagiarism flag with the similarity evidence and the
  two code fingerprints, and I decide — the system never bans on its own.

## Acceptance criteria

- AC1: Fork bomb, outbound-network attempt, and disk-fill programs are all
  contained; host metrics stay flat (proven by the malicious-code battery).
- AC2: A program sleeping 60s is killed at the wall-time limit and reported TLE.
- AC3: Two submissions differing only in comments/whitespace/variable names
  score ≥ 0.95 similarity; two genuinely different solutions score < 0.5.
- AC4: Editor is fully operable at 360px width (run, edit, view output).

## Success metrics

- p95 run latency (submit → result): < 8s for Python/C++ typical tasks.
- Isolation incidents: **0** (blocking metric; any escape stops the release).
- Plagiarism precision on the labeled eval set: ≥ 0.9 at the flag threshold.
- Cost per 1k runs tracked and under the budget line set in TRD.

## Risks

- R1 **Abuse (crypto mining, spam):** mitigated by quotas, rate limits, CPU caps,
  and anomaly alerts; residual risk accepted, monitored.
- R2 **Cost blow-up:** per-run cost is small but unbounded users × runs is not;
  mitigated by quotas + kill switch + budget alerts.
- R3 **False plagiarism flags:** mitigated by flag-only design + human review +
  starter-code exclusion; metric-tracked.
