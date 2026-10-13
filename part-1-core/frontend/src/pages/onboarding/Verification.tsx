import { useState } from 'react';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';
import { api } from '../../lib/api';
import type {
  CodingQuestion,
  PlacementSubmitResult,
  Question,
  VerificationState,
} from './lib';
import './onboarding.css';

/**
 * Route: /verification — placement verification test (Flow 3, F6c v3).
 *
 * 20 questions: 15 MCQ (5 × beginner/intermediate/advanced, seeded random)
 * + 5 coding problems (2 easy + 2 medium + 1 hard, engine-graded against
 * hidden tests). Coding is optional per question — blank code submits as
 * not_attempted; the verified level comes from the MCQ per-level rule.
 *
 * Receives its session via router state from MakePlan:
 *   { placement_id, topic, claimed_level, questions, coding_questions }
 * If the state is missing (refresh / deep link), redirects to /plan —
 * placement sessions are single-use and re-created from there.
 *
 * GREEN DISCIPLINE: the green "verified" badge appears ONLY when a level
 * beyond beginner was genuinely verified by the test.
 */
const LEVEL_ORDER = ['beginner', 'intermediate', 'advanced', 'expert'];
const PASS = 0.7;
const CODE_LANGUAGES = ['python', 'c', 'cpp', 'java'] as const;

function prettyTopic(t: string): string {
  return t === 'ml-basics' ? 'ML Basics' : t === 'python' ? 'Python' : t;
}

type Item =
  | { kind: 'mcq'; q: Question }
  | { kind: 'code'; q: CodingQuestion };

const VERDICT_LABEL: Record<string, string> = {
  accepted: '✓ accepted',
  wrong_answer: '✗ wrong answer',
  runtime_error: '⚠ runtime error',
  engine_error: '⚠ engine unreachable',
  not_attempted: '– not attempted',
};

export default function Verification() {
  const location = useLocation();
  const navigate = useNavigate();
  const state = location.state as VerificationState | null;

  const [idx, setIdx] = useState(0);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [codeSubs, setCodeSubs] = useState<
    Record<string, { language: string; code: string }>
  >({});
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState('');
  const [result, setResult] = useState<PlacementSubmitResult | null>(null);
  const [generating, setGenerating] = useState(false);
  const [genError, setGenError] = useState('');

  const mcqs: Question[] = state?.questions ?? [];
  const coding: CodingQuestion[] = state?.coding_questions ?? [];
  if (!state || mcqs.length === 0) {
    return <Navigate to="/plan" replace />;
  }
  const { topic, claimed_level } = state;

  const items: Item[] = [
    ...mcqs.map((q) => ({ kind: 'mcq' as const, q })),
    ...coding.map((q) => ({ kind: 'code' as const, q })),
  ];
  const item = items[idx];
  const mcqAnswered = Object.keys(answers).length;
  const codeAttempted = Object.values(codeSubs).filter((s) =>
    s.code.trim(),
  ).length;
  const allMcqAnswered = mcqAnswered === mcqs.length;

  const choose = (choiceIdx: number) => {
    if (item.kind !== 'mcq') return;
    setAnswers((a) => ({ ...a, [item.q.id]: choiceIdx }));
  };

  const setCode = (pid: string, patch: { language?: string; code?: string }) =>
    setCodeSubs((s) => {
      const cur = s[pid] ?? { language: 'python', code: '' };
      const next = { ...cur, ...patch };
      // Seed the editor with the python starter on first touch.
      if (patch.language === 'python' && !cur.code) {
        const cq = coding.find((c) => c.id === pid);
        if (cq?.starter_code) next.code = cq.starter_code;
      }
      if (patch.language && patch.language !== 'python') {
        // keep whatever the user typed; no starter for other languages
      }
      return { ...s, [pid]: next };
    });

  const submit = async () => {
    setSubmitting(true);
    setSubmitError('');
    try {
      const code: Record<string, { language: string; code: string }> = {};
      for (const [pid, sub] of Object.entries(codeSubs)) {
        if (sub.code.trim()) code[pid] = sub;
      }
      const res = await api<PlacementSubmitResult>(
        `/api/v1/placement/${state.placement_id}/submit`,
        { method: 'POST', body: JSON.stringify({ answers, code }) },
      );
      setResult(res);
    } catch (e) {
      setSubmitError(e instanceof Error ? e.message : 'Submit failed');
    } finally {
      setSubmitting(false);
    }
  };

  const generateRoadmap = async () => {
    if (!result) return;
    setGenerating(true);
    setGenError('');
    try {
      const levels = result.analysis.levels;
      const failed = LEVEL_ORDER.filter(
        (l) => levels[l] && levels[l].total > 0 && levels[l].ratio < PASS,
      );
      // Coding failures become roadmap gaps too — but only genuine
      // failures (wrong_answer / runtime_error), never infrastructure
      // issues (engine_error) or skips (not_attempted).
      const failedCoding = (result.analysis.coding ?? []).filter(
        (c) => c.verdict === 'wrong_answer' || c.verdict === 'runtime_error',
      );
      let gaps: { skill: string; mastery_pct: number }[];
      let title: string;
      if (failed.length > 0 || failedCoding.length > 0) {
        const worst = failed.length
          ? Math.min(...failed.map((l) => levels[l].ratio))
          : 0.5;
        gaps = [{ skill: topic, mastery_pct: Math.round(worst * 100) }];
        if (failedCoding.length > 0) {
          gaps.push({ skill: `${topic} coding practice`, mastery_pct: 40 });
        }
        title = `Roadmap: ${prettyTopic(topic)} from ${result.verified_level}`;
      } else {
        // Passed everything at the claimed level — roadmap targets the next level.
        const next = LEVEL_ORDER[LEVEL_ORDER.indexOf(result.verified_level) + 1];
        gaps = next
          ? [{ skill: `${topic} (${next} track)`, mastery_pct: 0 }]
          : [{ skill: topic, mastery_pct: 70 }];
        title = next
          ? `Roadmap: ${prettyTopic(topic)} → ${next}`
          : `Roadmap: ${prettyTopic(topic)} mastery`;
      }
      await api('/api/v1/roadmaps/generate', {
        method: 'POST',
        body: JSON.stringify({ gaps, title }),
      });
      navigate('/roadmap');
    } catch (e) {
      setGenError(e instanceof Error ? e.message : 'Could not generate roadmap');
    } finally {
      setGenerating(false);
    }
  };

  /* ---------------- results panel ---------------- */
  if (result) {
    const a = result.analysis;
    const ordered = LEVEL_ORDER.filter((l) => a.levels[l]);
    const genuinelyVerified = a.verified_level !== 'beginner';
    return (
      <div className="ob">
        <div className="ob-kicker">VERIFICATION COMPLETE</div>
        <h1 className="ob-title">Your verified level</h1>
        <p className="ob-sub">{a.summary}</p>

        <div className="ob-card glow" style={{ textAlign: 'center', padding: '30px 22px' }}>
          {genuinelyVerified ? (
            <span className="ob-badge verified" style={{ fontSize: 15, padding: '10px 22px' }}>
              ✓ VERIFIED · {a.verified_level.toUpperCase()}
            </span>
          ) : (
            <span className="ob-badge neutral" style={{ fontSize: 15, padding: '10px 22px' }}>
              VERIFIED · BEGINNER — starting from basics
            </span>
          )}
          <p className="ob-hint" style={{ margin: '14px 0 0' }}>
            Claimed <b style={{ textTransform: 'capitalize' }}>{a.claimed_level}</b> ·{' '}
            {a.correct}/{a.total} MCQ correct
            {a.coding_total > 0 && (
              <> · {a.coding_accepted}/{a.coding_total} code accepted</>
            )}
          </p>
        </div>

        <div className="ob-section-t">PER-LEVEL BREAKDOWN</div>
        <div className="ob-card">
          {ordered.map((l) => {
            const r = a.levels[l];
            const pct = Math.round(r.ratio * 100);
            const barColor = r.ratio >= PASS ? '#36C5F0' : r.ratio >= 0.4 ? '#F5B84B' : '#F06C75';
            return (
              <div className="ob-lvl" key={l}>
                <div className="row">
                  <b>{l}</b>
                  <span className="mono" style={{ color: 'var(--muted)', fontSize: 13 }}>
                    {r.correct}/{r.total} · {pct}%
                    {r.ratio >= PASS ? ' · passed' : ' · gap'}
                  </span>
                </div>
                <div className="ob-bar">
                  <i style={{ width: `${pct}%`, background: barColor }} />
                </div>
              </div>
            );
          })}
          <p className="ob-empty" style={{ marginTop: 6 }}>
            Verified = highest level at ≥70% with every lower level passed.
          </p>
        </div>

        {a.coding && a.coding.length > 0 && (
          <>
            <div className="ob-section-t">CODING</div>
            <div className="ob-card">
              {a.coding.map((c) => (
                <div className="ob-lvl" key={c.problem_id}>
                  <div className="row">
                    <b>{c.title}</b>
                    <span className="mono" style={{ color: 'var(--muted)', fontSize: 13 }}>
                      {c.difficulty} · {VERDICT_LABEL[c.verdict] ?? c.verdict}
                      {c.verdict !== 'not_attempted' &&
                        c.verdict !== 'engine_error' &&
                        ` · ${c.passed}/${c.total} tests`}
                    </span>
                  </div>
                </div>
              ))}
              <p className="ob-empty" style={{ marginTop: 6 }}>
                Code is graded against hidden tests on the server. Skipped
                problems count as not attempted, not as failures.
              </p>
            </div>
          </>
        )}

        {genError && <div className="ob-alert err">{genError}</div>}
        <div className="ob-cta-row">
          <button className="ob-btn" onClick={generateRoadmap} disabled={generating}>
            {generating ? 'Generating…' : 'Generate my roadmap →'}
          </button>
        </div>
      </div>
    );
  }

  /* ---------------- question stepper ---------------- */
  const pct = Math.round(((idx + 1) / items.length) * 100);
  const letters = ['A', 'B', 'C', 'D', 'E', 'F'];
  const isLast = idx === items.length - 1;

  return (
    <div className="ob">
      <div className="ob-kicker">PLACEMENT VERIFICATION</div>
      <h1 className="ob-title">
        {prettyTopic(topic)}{' '}
        <span style={{ color: 'var(--muted)', fontWeight: 500, fontSize: 18 }}>
          · claimed <span style={{ textTransform: 'capitalize' }}>{claimed_level}</span>
        </span>
      </h1>
      <p className="ob-sub">
        {mcqs.length} questions check your knowledge, {coding.length} check your
        code. Answer keys and hidden tests never leave the server.
      </p>

      <div className="ob-card">
        <div className="ob-meta">
          <span className="mono">
            Question {idx + 1} of {items.length}
          </span>
          {item.kind === 'mcq' ? (
            <span className="ob-lvl-tag">{item.q.level}</span>
          ) : (
            <span className="ob-lvl-tag code">CODING · {item.q.difficulty}</span>
          )}
          <span className="mono" style={{ marginLeft: 'auto' }}>
            {mcqAnswered}/{mcqs.length} MCQ · {codeAttempted}/{coding.length} code
          </span>
        </div>
        <div className="ob-bar cyan" style={{ marginBottom: 20 }}>
          <i style={{ width: `${pct}%` }} />
        </div>

        {item.kind === 'mcq' ? (
          <>
            <p className="ob-qprompt">{item.q.prompt}</p>
            {item.q.choices.map((c, i) => (
              <button
                key={i}
                className={`ob-choice ${answers[item.q.id] === i ? 'sel' : ''}`}
                onClick={() => choose(i)}
              >
                <span className="k">{letters[i] ?? i + 1}</span>
                <span>{c}</span>
              </button>
            ))}
          </>
        ) : (
          <CodingPanel
            q={item.q}
            sub={codeSubs[item.q.id]}
            onChange={(patch) => setCode(item.q.id, patch)}
          />
        )}

        {submitError && <div className="ob-alert err">{submitError}</div>}

        <div className="ob-nav-row">
          <button
            className="ob-ghost"
            onClick={() => setIdx((v) => Math.max(0, v - 1))}
            disabled={idx === 0}
          >
            ← Previous
          </button>
          {!isLast ? (
            <button className="ob-btn-sm" onClick={() => setIdx((v) => v + 1)}>
              Next →
            </button>
          ) : (
            <button
              className="ob-btn-sm"
              onClick={submit}
              disabled={!allMcqAnswered || submitting}
              title={
                allMcqAnswered
                  ? 'Submit verification'
                  : 'Answer all MCQ questions first (coding is optional)'
              }
            >
              {submitting
                ? 'Submitting…'
                : allMcqAnswered
                  ? 'Submit verification'
                  : `${mcqAnswered}/${mcqs.length} MCQ answered`}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

function CodingPanel({
  q,
  sub,
  onChange,
}: {
  q: CodingQuestion;
  sub: { language: string; code: string } | undefined;
  onChange: (patch: { language?: string; code?: string }) => void;
}) {
  const language = sub?.language ?? 'python';
  const code = sub?.code ?? '';
  return (
    <div>
      <p className="ob-qprompt">{q.title}</p>
      <p className="ob-sub" style={{ whiteSpace: 'pre-wrap' }}>
        {q.description}
      </p>
      {q.examples.slice(0, 2).map((e, i) => (
        <div className="ob-example" key={i}>
          <div className="mono" style={{ fontSize: 12 }}>
            <div>
              <b>Input:</b> <code>{e.stdin || '(empty)'}</code>
            </div>
            <div>
              <b>Output:</b> <code>{e.stdout}</code>
            </div>
            {e.explanation && (
              <div style={{ color: 'var(--muted)' }}>{e.explanation}</div>
            )}
          </div>
        </div>
      ))}
      <div className="ob-code-row">
        <select
          className="ob-lang"
          value={language}
          onChange={(e) => onChange({ language: e.target.value })}
          aria-label="Language"
        >
          {CODE_LANGUAGES.map((l) => (
            <option key={l} value={l}>
              {l}
            </option>
          ))}
        </select>
        {q.starter_code && (
          <button
            type="button"
            className="ob-ghost-sm"
            onClick={() => onChange({ language: 'python', code: q.starter_code })}
          >
            Load python template
          </button>
        )}
        <span className="ob-hint mono" style={{ fontSize: 12 }}>
          {q.hidden_test_count} hidden tests · optional — blank counts as skipped
        </span>
      </div>
      <textarea
        className="ob-code-editor"
        value={code}
        onChange={(e) => onChange({ code: e.target.value })}
        placeholder={
          language === 'python' && q.starter_code
            ? undefined
            : `Write your ${language} solution here… (stdin → stdout)`
        }
        spellCheck={false}
        rows={10}
      />
    </div>
  );
}
