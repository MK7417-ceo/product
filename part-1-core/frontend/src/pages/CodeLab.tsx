import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import './CodeLab.css';
import { ApiError, codeApi, dsaApi } from '../lib/api';
import type { CodeRunResult, DailyDSAQuestion, DSASubmitResult, EngineLanguage } from '../lib/api';

/* Minimal M1 code runner. Deep link: /codelab?date=YYYY-MM-DD loads that
   day's DSA question into the editor. Engine failures are shown honestly —
   results are never mocked. */

const FALLBACK_LANGUAGES: EngineLanguage[] = [
  { id: 'python', name: 'Python' },
  { id: 'c', name: 'C' },
  { id: 'cpp', name: 'C++' },
  { id: 'java', name: 'Java' },
];

const TEMPLATES: Record<string, string> = {
  python: 'import sys\n\ndef solve() -> None:\n    data = sys.stdin.read().strip()\n    print(data)\n\nif __name__ == "__main__":\n    solve()\n',
  c: '#include <stdio.h>\n\nint main(void) {\n    int c;\n    while ((c = getchar()) != EOF) putchar(c);\n    return 0;\n}\n',
  cpp: '#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    int a, b;\n    if (!(cin >> a >> b)) return 0;\n    cout << a + b << "\\n";\n    return 0;\n}\n',
  java: 'import java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (sc.hasNextInt()) {\n            int a = sc.nextInt();\n            int b = sc.nextInt();\n            System.out.println(a + b);\n        }\n    }\n}\n',
};

const CODE_KEY = 'sf_codelab_code_v1';
const SOLVED_KEY = 'sf_dsa_solved_v1';

function loadCodeCache(): Record<string, string> {
  try {
    return JSON.parse(localStorage.getItem(CODE_KEY) ?? '{}') as Record<string, string>;
  } catch {
    return {};
  }
}

function markSolved(date: string): void {
  try {
    const raw = JSON.parse(localStorage.getItem(SOLVED_KEY) ?? '[]') as string[];
    if (!raw.includes(date)) {
      localStorage.setItem(SOLVED_KEY, JSON.stringify([...raw, date]));
    }
  } catch {
    /* non-fatal */
  }
}

function verdictClass(v: string): string {
  if (v === 'ok') return 'ok';
  if (v === 'compile_error') return 'compile_error';
  if (v === 'runtime_error') return 'runtime_error';
  if (v === 'time_limit') return 'time_limit';
  return 'bad';
}

function engineErrorText(e: unknown): string {
  if (e instanceof ApiError) {
    // ApiError.message is usually the generic "request failed (502)" —
    // report the status plainly instead of repeating it.
    return /^request failed \(\d+\)$/.test(e.message)
      ? `Engine returned HTTP ${e.status} (not executed).`
      : `${e.status}: ${e.message}`;
  }
  return 'Network error — the request never reached the backend.';
}

export default function CodeLab() {
  const [searchParams] = useSearchParams();
  const dateParam = searchParams.get('date') ?? '';

  const [languages, setLanguages] = useState<EngineLanguage[]>(FALLBACK_LANGUAGES);
  const [engineDown, setEngineDown] = useState(false);
  const [lang, setLang] = useState('python');
  const [codeByLang, setCodeByLang] = useState<Record<string, string>>(() => loadCodeCache());
  const [stdin, setStdin] = useState('');
  const [running, setRunning] = useState(false);
  const [runResult, setRunResult] = useState<CodeRunResult | null>(null);
  const [runError, setRunError] = useState<string | null>(null);

  const [question, setQuestion] = useState<DailyDSAQuestion | null>(null);
  const [qLoading, setQLoading] = useState(false);
  const [qError, setQError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [submitResult, setSubmitResult] = useState<DSASubmitResult | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const gutterRef = useRef<HTMLDivElement>(null);
  const areaRef = useRef<HTMLTextAreaElement>(null);

  const code = codeByLang[lang] ?? TEMPLATES[lang] ?? '';

  /* --- languages (engine availability) --- */
  useEffect(() => {
    let alive = true;
    codeApi
      .languages()
      .then((res) => {
        if (!alive) return;
        if (res.languages?.length) {
          setLanguages(res.languages);
          setEngineDown(false);
        }
      })
      .catch((e) => {
        if (!alive) return;
        // Engine unreachable or down: keep fallback list, say so honestly.
        setLanguages(FALLBACK_LANGUAGES);
        setEngineDown(true);
        if (!(e instanceof ApiError)) setEngineDown(true);
      });
    return () => {
      alive = false;
    };
  }, []);

  /* --- deep link: ?date=YYYY-MM-DD loads that day's DSA question --- */
  useEffect(() => {
    setQuestion(null);
    setQError(null);
    setRunResult(null);
    setRunError(null);
    setSubmitResult(null);
    setSubmitError(null);
    if (!dateParam) return;
    let alive = true;
    setQLoading(true);
    dsaApi
      .daily(dateParam)
      .then((q) => {
        if (!alive) return;
        setQuestion(q);
        setQLoading(false);
        // Seed the editor with the question's starter code when available.
        if (q.starter_code) {
          setCodeByLang((prev) => {
            if (prev.python) return prev;
            const next = { ...prev, python: q.starter_code };
            try {
              localStorage.setItem(CODE_KEY, JSON.stringify(next));
            } catch {
              /* non-fatal */
            }
            return next;
          });
          setLang('python');
        }
      })
      .catch((e) => {
        if (!alive) return;
        setQLoading(false);
        setQError(e instanceof ApiError ? e.message : 'Failed to load the question.');
      });
    return () => {
      alive = false;
    };
  }, [dateParam]);

  const setCode = useCallback(
    (value: string) => {
      setCodeByLang((prev) => {
        const next = { ...prev, [lang]: value };
        try {
          localStorage.setItem(CODE_KEY, JSON.stringify(next));
        } catch {
          /* non-fatal */
        }
        return next;
      });
    },
    [lang],
  );

  const onScroll = useCallback(() => {
    const a = areaRef.current;
    const g = gutterRef.current;
    if (a && g) g.scrollTop = a.scrollTop;
  }, []);

  const lineCount = useMemo(() => code.split('\n').length, [code]);

  const run = useCallback(async () => {
    if (running || !code.trim()) return;
    setRunning(true);
    setRunResult(null);
    setRunError(null);
    try {
      const res = await codeApi.run(lang, code, stdin);
      setRunResult(res);
    } catch (e) {
      setRunError(engineErrorText(e));
    } finally {
      setRunning(false);
    }
  }, [running, lang, code, stdin]);

  const submit = useCallback(async () => {
    if (!question || submitting || !code.trim()) return;
    setSubmitting(true);
    setSubmitResult(null);
    setSubmitError(null);
    try {
      const res = await dsaApi.submit(question.date, lang, code);
      setSubmitResult(res);
      if (res.accepted) markSolved(res.date);
    } catch (e) {
      setSubmitError(engineErrorText(e));
    } finally {
      setSubmitting(false);
    }
  }, [question, submitting, lang, code]);

  const onKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      run();
    }
  };

  return (
    <div className="codelab">
      <div className="cl-head">
        <h1>
          Code<span>Lab</span>
        </h1>
        <span className="sub">
          {question ? `Daily DSA · ${question.date}` : 'Write code, run it against the real sandbox.'}
        </span>
        <div className="cl-controls">
          <select
            className="cl-select"
            value={lang}
            onChange={(e) => setLang(e.target.value)}
            aria-label="Programming language"
          >
            {languages.map((l) => (
              <option key={l.id} value={l.id}>
                {l.name ?? l.id}
                {l.available === false ? ' (unavailable)' : ''}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className={`cl-grid${question || qLoading || qError ? '' : ' no-problem'}`}>
        {/* ---- problem panel (deep-linked DSA) ---- */}
        {(question || qLoading || qError) && (
          <div className="cl-card">
            {qLoading && (
              <div className="cl-state">
                <div className="spin" />
                Loading the question…
              </div>
            )}
            {qError && (
              <div className="cl-error-box">
                <div className="err-title">Could not load the DSA question</div>
                <div>{qError}</div>
                <button className="cl-btn retry" onClick={() => window.location.reload()}>
                  Retry
                </button>
              </div>
            )}
            {question && (
              <>
                <h2>{question.title}</h2>
                <div className="date-line">
                  {question.date} · {question.id} · difficulty: {question.difficulty}
                </div>
                <div className="cl-desc">{question.description}</div>
                {question.examples.length > 0 && (
                  <div className="cl-examples">
                    {question.examples.map((ex, i) => (
                      <div className="cl-example" key={i}>
                        <div className="ex-label">Example {i + 1}</div>
                        <div>Input</div>
                        <pre>{ex.stdin || '(empty)'}</pre>
                        <div>Output</div>
                        <pre>{ex.stdout}</pre>
                        {ex.explanation && <div style={{ color: '#9aa6bb' }}>{ex.explanation}</div>}
                      </div>
                    ))}
                  </div>
                )}
                {question.hints.length > 0 && (
                  <details className="cl-hints">
                    <summary>Hints ({question.hints.length})</summary>
                    <ul style={{ marginTop: 8, paddingLeft: 18 }}>
                      {question.hints.map((h, i) => (
                        <li key={i}>{h}</li>
                      ))}
                    </ul>
                  </details>
                )}
                <div className="cl-tags">
                  {question.topic_tags.map((t) => (
                    <span className="cl-tag" key={t}>
                      {t}
                    </span>
                  ))}
                </div>
                <div className="cl-hidden-tests">
                  {question.hidden_test_count} hidden tests run on submit
                </div>
              </>
            )}
          </div>
        )}

        {/* ---- editor panel ---- */}
        <div>
          <div className="cl-editor-card">
            <div className="cl-editor-head">
              <span className="fname">
                main.{lang === 'python' ? 'py' : lang === 'cpp' ? 'cpp' : lang}
              </span>
              <span className="hint">
                <kbd>Ctrl</kbd> + <kbd>Enter</kbd> to run
              </span>
            </div>
            <div className="cl-editor-wrap">
              <div className="cl-gutter" ref={gutterRef} aria-hidden="true">
                {Array.from({ length: lineCount }, (_, i) => (
                  <div key={i}>{i + 1}</div>
                ))}
              </div>
              <textarea
                ref={areaRef}
                className="cl-textarea"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                onScroll={onScroll}
                onKeyDown={onKeyDown}
                spellCheck={false}
                autoCapitalize="off"
                autoCorrect="off"
                placeholder={TEMPLATES[lang] ?? '// write your code here'}
              />
            </div>
            <div className="cl-stdin">
              <label htmlFor="cl-stdin">stdin</label>
              <textarea
                id="cl-stdin"
                value={stdin}
                onChange={(e) => setStdin(e.target.value)}
                placeholder="Input fed to your program…"
                spellCheck={false}
              />
            </div>
            <div className="cl-actions">
              <button className="cl-btn primary" onClick={run} disabled={running || !code.trim()}>
                {running ? 'Running…' : 'Run'}
              </button>
              {question && (
                <button
                  className="cl-btn submit"
                  onClick={submit}
                  disabled={submitting || !code.trim()}
                >
                  {submitting ? 'Submitting…' : `Submit solution`}
                </button>
              )}
              {engineDown && (
                <span className="cl-engine-note">
                  ⚠ Code engine unreachable — language list is a fallback. Runs will report an
                  engine error, not a result.
                </span>
              )}
            </div>
            <div className="cl-output">
              {runError && (
                <div className="cl-error-box" role="alert">
                  <div className="err-title">Run failed — nothing was executed</div>
                  <div>{runError}</div>
                  <div style={{ marginTop: 8, color: '#9aa6bb' }}>
                    This usually means the code engine service is not running. Your code is safe in
                    the editor; try again once the engine is back.
                  </div>
                </div>
              )}
              {runResult && (
                <>
                  <span className={`cl-verdict ${verdictClass(runResult.verdict)}`}>
                    {runResult.verdict.replace(/_/g, ' ')}
                  </span>
                  <span className="cl-meta">
                    {runResult.cpu_ms != null && `cpu ${runResult.cpu_ms}ms`}
                    {runResult.peak_ram_mb != null && ` · ram ${runResult.peak_ram_mb.toFixed(1)}MB`}
                    {runResult.exit_code != null && ` · exit ${runResult.exit_code}`}
                    {runResult.timed_out && ' · timed out'}
                    {runResult.truncated && ' · output truncated'}
                  </span>
                  <div className="cl-io" style={{ marginTop: 12 }}>
                    <div className={`cl-pane stdout${runResult.stdout ? '' : ' empty'}`}>
                      <div className="pane-label">stdout</div>
                      <pre>{runResult.stdout || '(no output)'}</pre>
                    </div>
                    <div className={`cl-pane stderr${runResult.stderr ? '' : ' empty'}`}>
                      <div className="pane-label">stderr</div>
                      <pre>{runResult.stderr || '(no errors)'}</pre>
                    </div>
                  </div>
                </>
              )}
              {submitError && (
                <div className="cl-error-box" role="alert" style={{ marginTop: 12 }}>
                  <div className="err-title">Submit failed — not graded</div>
                  <div>{submitError}</div>
                </div>
              )}
              {submitResult && (
                <div className="cl-submit-result">
                  <div className="cl-score">
                    {submitResult.accepted ? (
                      <span className="accepted">✓ Accepted</span>
                    ) : (
                      <span className="rejected">✗ Not accepted</span>
                    )}
                    <span className="frac">
                      {submitResult.passed}/{submitResult.total} tests passed
                    </span>
                  </div>
                  {submitResult.failed_case && !submitResult.accepted && (
                    <div className="cl-failed">
                      First failing case:
                      <pre className="cl-example">{submitResult.failed_case}</pre>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
