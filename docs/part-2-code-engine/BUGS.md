# Part 2 — Code Execution Engine: BUGS

Bug log. Every entry: date, severity, status, lane that caught it.

## Open

| ID | Date | Severity | Summary | Caught by | Status |
|---|---|---|---|---|---|
| _none_ | — | — | Part not built yet; no bugs filed. | — | — |

## Watch-items (anticipated risks, tracked — not bugs yet)

| ID | Risk | Why it matters | Mitigation in plan |
|---|---|---|---|
| W-1 | Container escape attempt | Untrusted code is adversarial by nature; a single escape is an S0 | `--network none`, non-root, seccomp, separate host, blocking security battery (TESTING.md) |
| W-2 | Resource exhaustion under load | Run queue flood (accidental or malicious) could starve legit runs | Bounded queue (429), per-user quotas, CPU/RAM caps, budget alerts + kill switch |
| W-3 | Plagiarism false positives on idiomatic code | Short/idiomatic solutions (e.g. two-line Python) look alike structurally | Flag-only + human review; starter-code exclusion; threshold tuned on labeled eval set |

## Fixed

| ID | Date | Severity | Summary | Fix | Regression test |
|---|---|---|---|---|---|
| _none yet_ | — | — | — | — | — |

**Rule:** a bug is only "fixed" when its regression test is merged and both
testing lanes re-pass.
