import { useState } from 'react';
import { assessmentApi, ApiError, type AssessmentResult, type AssessmentStart } from '../lib/api';

const TOPICS = ['python', 'ml-basics'];
const LEVELS = ['beginner', 'intermediate', 'advanced'];

type Phase = 'setup' | 'taking' | 'done';

export default function Assessment() {
  const [phase, setPhase] = useState<Phase>('setup');
  const [topic, setTopic] = useState('python');
  const [level, setLevel] = useState('beginner');
  const [session, setSession] = useState<AssessmentStart | null>(null);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const start = async () => {
    setError('');
    setBusy(true);
    try {
      const s = await assessmentApi.start(topic, level, 6);
      setSession(s);
      setAnswers({});
      setResult(null);
      setPhase('taking');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not start assessment');
    } finally {
      setBusy(false);
    }
  };

  const submit = async () => {
    if (!session) return;
    if (Object.keys(answers).length < session.questions.length) {
      setError(`Answer all ${session.questions.length} questions first.`);
      return;
    }
    setError('');
    setBusy(true);
    try {
      const r = await assessmentApi.submit(session.assessment_id, answers);
      setResult(r);
      setPhase('done');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Submit failed');
    } finally {
      setBusy(false);
    }
  };

  if (phase === 'setup') {
    return (
      <div>
        <h1 className="page-title">Assessment</h1>
        <p className="page-sub">Level-matched tests. Answer keys never leave the server — your score is earned.</p>
        <div className="card" style={{ maxWidth: 520 }}>
          {error && <div className="auth-err">{error}</div>}
          <div className="field">
            <label>Topic</label>
            <div style={{ display: 'flex', gap: 8 }}>
              {TOPICS.map((t) => (
                <button key={t} className={topic === t ? 'btn' : 'btn-ghost'}
                  style={{ padding: '10px 18px', fontSize: 13 }}
                  onClick={() => setTopic(t)}>{t}</button>
              ))}
            </div>
          </div>
          <div className="field">
            <label>Level</label>
            <div style={{ display: 'flex', gap: 8 }}>
              {LEVELS.map((l) => (
                <button key={l} className={level === l ? 'btn' : 'btn-ghost'}
                  style={{ padding: '10px 18px', fontSize: 13 }}
                  onClick={() => setLevel(l)}>{l}</button>
              ))}
            </div>
          </div>
          <button className="btn" onClick={start} disabled={busy} style={{ width: '100%' }}>
            {busy ? 'Preparing…' : 'Start 6-question test'}
          </button>
        </div>
      </div>
    );
  }

  if (phase === 'taking' && session) {
    const done = Object.keys(answers).length;
    return (
      <div>
        <h1 className="page-title">{session.topic} · {session.level}</h1>
        <p className="page-sub">{done}/{session.questions.length} answered</p>
        {error && <div className="auth-err">{error}</div>}
        {session.questions.map((q, i) => (
          <div className="card" key={q.id} style={{ marginBottom: 14 }}>
            <div style={{ fontSize: 12, color: '#8b93a7', marginBottom: 8 }}>Q{i + 1}</div>
            <div style={{ fontSize: 15, fontWeight: 600, marginBottom: 12 }}>{q.prompt}</div>
            {q.choices.map((c, ci) => (
              <label key={ci} style={{
                display: 'flex', gap: 10, alignItems: 'center', padding: '10px 12px',
                borderRadius: 10, cursor: 'pointer', fontSize: 14,
                background: answers[q.id] === ci ? 'rgba(124,58,237,.16)' : 'rgba(255,255,255,.03)',
                border: answers[q.id] === ci ? '1px solid rgba(124,58,237,.4)' : '1px solid transparent',
                marginBottom: 6,
              }}>
                <input type="radio" name={q.id} checked={answers[q.id] === ci}
                  onChange={() => setAnswers((a) => ({ ...a, [q.id]: ci }))} />
                {c}
              </label>
            ))}
          </div>
        ))}
        <button className="btn" onClick={submit} disabled={busy} style={{ width: '100%', marginTop: 6 }}>
          {busy ? 'Scoring…' : 'Submit answers'}
        </button>
      </div>
    );
  }

  if (phase === 'done' && result) {
    const pct = Math.round(result.ratio * 100);
    return (
      <div>
        <h1 className="page-title">Results</h1>
        <p className="page-sub">Scored on the server — deterministic, no self-report.</p>
        <div className="grid4" style={{ gridTemplateColumns: 'repeat(3,1fr)' }}>
          <div className="card stat">
            <div className="lb">Score</div>
            <div className="vl">{result.correct}<span style={{ fontSize: 14, color: '#8b93a7' }}>/{result.total}</span></div>
          </div>
          <div className="card stat">
            <div className="lb">Mastery</div>
            <div className="vl" style={{ color: pct >= 70 ? '#4ade80' : pct >= 40 ? '#fbbf24' : '#f87171' }}>{pct}%</div>
          </div>
          <div className="card stat">
            <div className="lb">Skill gaps</div>
            <div className="vl">{result.gaps.length}</div>
          </div>
        </div>
        <div className="card" style={{ marginBottom: 16 }}>
          <h3 style={{ fontSize: 14, marginBottom: 14 }}>Per-skill breakdown</h3>
          {result.per_skill.map((s) => {
            const p = Math.round((s.correct / s.total) * 100);
            return (
              <div key={s.skill} style={{ marginBottom: 12 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 13, marginBottom: 6 }}>
                  <b>{s.skill}</b><span style={{ color: '#8b93a7' }}>{s.correct}/{s.total} · {p}%</span>
                </div>
                <div className="bar" style={{ height: 7, background: 'rgba(255,255,255,.07)', borderRadius: 4, overflow: 'hidden' }}>
                  <div style={{ width: `${p}%`, height: '100%', background: p >= 70 ? 'linear-gradient(90deg,#22d3ee,#7c3aed)' : '#fbbf24' }} />
                </div>
              </div>
            );
          })}
        </div>
        {result.gaps.length > 0 && (
          <div className="card">
            <h3 style={{ fontSize: 14, marginBottom: 10 }}>Gaps found — these become your roadmap</h3>
            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
              {result.gaps.map((g) => (
                <span key={g} style={{
                  fontSize: 12, fontWeight: 700, color: '#fbbf24',
                  background: 'rgba(251,191,36,.12)', border: '1px solid rgba(251,191,36,.3)',
                  padding: '5px 14px', borderRadius: 14,
                }}>{g}</span>
              ))}
            </div>
          </div>
        )}
        <button className="btn-ghost" onClick={() => setPhase('setup')} style={{ marginTop: 18 }}>
          Take another test
        </button>
      </div>
    );
  }

  return null;
}
