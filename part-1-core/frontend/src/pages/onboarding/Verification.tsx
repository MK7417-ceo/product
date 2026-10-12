import { useState } from 'react';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';
import { api } from '../../lib/api';
import type { PlacementSubmitResult, VerificationState } from './lib';
import './onboarding.css';

/**
 * Route: /verification — placement verification test (Flow 3, step T–V).
 *
 * Receives its session via router state from MakePlan:
 *   { placement_id, topic, claimed_level, questions }
 * If the state is missing (refresh / deep link), redirects to /plan —
 * placement sessions are single-use and re-created from there.
 *
 * GREEN DISCIPLINE: the green "verified" badge appears ONLY when a level
 * beyond beginner was genuinely verified by the test.
 */
const LEVEL_ORDER = ['beginner', 'intermediate', 'advanced', 'expert'];
const PASS = 0.7;

function prettyTopic(t: string): string {
  return t === 'ml-basics' ? 'ML Basics' : t === 'python' ? 'Python' : t;
}

export default function Verification() {
  const location = useLocation();
  const navigate = useNavigate();
  const state = location.state as VerificationState | null;

  const [idx, setIdx] = useState(0);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState('');
  const [result, setResult] = useState<PlacementSubmitResult | null>(null);
  const [generating, setGenerating] = useState(false);
  const [genError, setGenError] = useState('');

  if (!state || !state.questions || state.questions.length === 0) {
    return <Navigate to="/plan" replace />;
  }

  const { placement_id, topic, claimed_level, questions } = state;
  const q = questions[idx];
  const answered = Object.keys(answers).length;
  const allAnswered = answered === questions.length;

  const choose = (choiceIdx: number) =>
    setAnswers((a) => ({ ...a, [q.id]: choiceIdx }));

  const submit = async () => {
    setSubmitting(true);
    setSubmitError('');
    try {
      const res = await api<PlacementSubmitResult>(
        `/api/v1/placement/${placement_id}/submit`,
        { method: 'POST', body: JSON.stringify({ answers }) },
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
      let gaps: { skill: string; mastery_pct: number }[];
      let title: string;
      if (failed.length > 0) {
        const worst = Math.min(...failed.map((l) => levels[l].ratio));
        gaps = [{ skill: topic, mastery_pct: Math.round(worst * 100) }];
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
            {a.correct}/{a.total} correct overall
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
  const pct = Math.round(((idx + 1) / questions.length) * 100);
  const letters = ['A', 'B', 'C', 'D', 'E', 'F'];

  return (
    <div className="ob">
      <div className="ob-kicker">PLACEMENT VERIFICATION</div>
      <h1 className="ob-title">
        {prettyTopic(topic)} <span style={{ color: 'var(--muted)', fontWeight: 500, fontSize: 18 }}>
          · claimed <span style={{ textTransform: 'capitalize' }}>{claimed_level}</span>
        </span>
      </h1>
      <p className="ob-sub">
        Answer each question honestly — your verified level decides where your
        roadmap starts. Answer keys never leave the server.
      </p>

      <div className="ob-card">
        <div className="ob-meta">
          <span className="mono">Question {idx + 1} of {questions.length}</span>
          <span className="ob-lvl-tag">{q.level}</span>
          <span className="mono" style={{ marginLeft: 'auto' }}>{answered}/{questions.length} answered</span>
        </div>
        <div className="ob-bar cyan" style={{ marginBottom: 20 }}>
          <i style={{ width: `${pct}%` }} />
        </div>

        <p className="ob-qprompt">{q.prompt}</p>

        {q.choices.map((c, i) => (
          <button
            key={i}
            className={`ob-choice ${answers[q.id] === i ? 'sel' : ''}`}
            onClick={() => choose(i)}
          >
            <span className="k">{letters[i] ?? i + 1}</span>
            <span>{c}</span>
          </button>
        ))}

        {submitError && <div className="ob-alert err">{submitError}</div>}

        <div className="ob-nav-row">
          <button className="ob-ghost" onClick={() => setIdx((v) => Math.max(0, v - 1))} disabled={idx === 0}>
            ← Previous
          </button>
          {idx < questions.length - 1 ? (
            <button className="ob-btn-sm" onClick={() => setIdx((v) => v + 1)}>
              Next →
            </button>
          ) : (
            <button className="ob-btn-sm" onClick={submit} disabled={!allAnswered || submitting}>
              {submitting ? 'Submitting…' : allAnswered ? 'Submit answers' : `${answered}/${questions.length} answered`}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
