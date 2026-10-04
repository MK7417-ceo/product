# Part 2 — Code Execution Engine: SPECS

Per-feature specs: inputs → behavior → outputs → edge cases. These are the
test oracle; TESTING.md executes them.

## S1 — Code execution (`POST /v1/run`)

- **Inputs:** `{language: "python"|"c"|"cpp"|"java", code: string (≤100KB),
  stdin: string (≤1MB), limits?: {wall_time_s, memory_mb}}`, `X-Request-ID`.
- **Behavior:** validate → compile if needed (C/C++/Java; ≤15s of the budget) →
  run in a fresh container with the limits table (TRD) → capture
  stdout/stderr/exit → classify verdict → remove container → store metadata.
- **Outputs:** `{run_id, verdict, stdout (≤64KB, truncated flag), stderr
  (≤16KB), exit_code, cpu_ms, peak_ram_mb, timed_out: bool}`.
- **Edge cases:**
  - Infinite loop → killed at wall-time → `TLE`.
  - `malloc` bomb / huge list → OOM-killed → `MLE`.
  - Socket connect attempt → fails (no network) → program sees connection
    error; verdict from exit code (`RUNTIME_ERROR` if nonzero).
  - Fork bomb → pids-limit contains it → `TLE` or `RUNTIME_ERROR`; host flat.
  - 10MB stdout → truncated at 1MB, `truncated: true`.
  - Empty code / unsupported language → `400` with machine-readable error code.
  - Compile error (C++) → `COMPILE_ERROR`, stderr carries the compiler message.

## S2 — Language matrix (v1)

| Language | Toolchain | Compile step | Notes |
|---|---|---|---|
| Python | CPython 3.12 | none | `-u` unbuffered; recursion limit default |
| C | GCC 13, `-std=c11 -O2` | yes | warnings shown, not fatal |
| C++ | G++ 13, `-std=c++17 -O2` | yes | same |
| Java | OpenJDK 17 | `javac`, then `java` | class name must be `Main` (documented) |

Adding a language = new image + matrix row + adapter config; no port changes.

## S3 — Async jobs (`POST /v1/jobs`, `GET /v1/jobs/{job_id}`)

- For runs needing >10s wall time (up to 30s max). Job states:
  `QUEUED → RUNNING → DONE | FAILED`. Queue depth 100; beyond → `429`.
- Poll returns the same `RunResult` shape when DONE.

## S4 — Grading (`POST /v1/grade`)

- **Inputs:** `{language, code, cases: [{stdin, expected_stdout, time_limit_s?}]}`.
- **Behavior:** one container per case (isolation between cases); stdout
  compared after trailing-whitespace normalization.
- **Outputs:** per-case `{verdict, cpu_ms, peak_ram_mb}` + overall
  (`ACCEPTED` only if all cases pass).

## S5 — Plagiarism pipeline (`POST /v1/plagiarism/check`)

Stages (all deterministic, no LLM):
1. **Normalize:** strip comments + whitespace; canonicalize identifiers
   (`var1`, `var2`… in order of appearance); normalize string literals to
   `STR`; **exclude starter/boilerplate code** supplied by the question.
2. **Fingerprint:** token 5-grams hashed (all languages) + AST-shape hash
   (Python via `ast`); store both fingerprints in the report.
3. **Score:** Jaccard over n-gram sets, blended 70/30 with AST-shape match
   (Python) or 100% n-gram (others).
4. **Decide:** score ≥ 0.85 → `flagged: true` + reasons (e.g.
   "identifier-renamed clone, 0.93"); 0.6–0.85 → `needs_review`;
   < 0.6 → clear. **Flagged items go to a human review queue; nothing is
   auto-punished, ever.**

## S6 — Editor UX (Core frontend)

- Layout (Aurora Dark): left editor, right output panel; collapsible stdin box;
  language picker; Run (sync) button with spinner; verdict badge colored per
  verdict (green AC, amber TLE/MLE, red RE/CE).
- Behaviors: code persists to localStorage per language; Ctrl/Cmd+Enter runs;
  errors shown with the relevant stderr lines first; empty-output state says
  what to try next.
- Mobile (360px): stacked layout (editor above, output below), no horizontal
  scroll, tap targets ≥ 44px, readable without zoom.
