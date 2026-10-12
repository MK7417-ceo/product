import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { practiceApi, ApiError, type DailyQuestion, type TodayPlan } from '../lib/api';

const PRI_COLOR: Record<string, string> = {
  high: '#fbbf24', medium: '#7dd3fc', low: '#8b93a7',
};

export default function Practice() {
  const [plan, setPlan] = useState<TodayPlan | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [score, setScore] = useState<{ correct: number; total: number } | null>(null);
  const [busy, setBusy] = useState(false);

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      setPlan(await practiceApi.today());
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Load failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const pick = (qid: string, idx: number) => {
    if (score) return;
    setAnswers((a) => ({ ...a, [qid]: idx }));
  };

  const submit = async () => {
    if (!plan || score) return;
    setError('');
    setBusy(true);
    try {
      const r = await practiceApi.submitDaily(answers);
      setScore({ correct: r.correct, total: r.total });
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Submit failed');
    } finally {
      setBusy(false);
    }
  };

  if (loading) return <p className="page-sub">Loading aaj ka plan…</p>;

  return (
    <div>
      <h1 className="page-title">Aaj ka plan</h1>
      <p className="page-sub">
        {plan ? plan.date : ''} — roz ke 3 questions + roadmap ke aaj ke tasks. Chhote steps, roz.
      </p>
      {error && <p className="error">{error}</p>}

      {/* today's roadmap tasks */}
      <div className="card">
        <h2 style={{ marginTop: 0 }}>Aaj ke tasks</h2>
        {plan && plan.tasks.length > 0 ? (
          plan.tasks.map((t) => (
            <div key={t.id} className="task-row">
              <span className="pri-dot" style={{ background: PRI_COLOR[t.priority] || '#8b93a7' }} />
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 600 }}>{t.title}</div>
                <div className="muted">{t.effort_minutes} min · {t.status.replace('_', ' ')}</div>
              </div>
              <Link className="btn small" to="/roadmap">Roadmap</Link>
            </div>
          ))
        ) : (
          <p className="muted" style={{ margin: 0 }}>
            Roadmap abhi nahi bani — <Link to="/roadmap">roadmap banao</Link> to aaj ke tasks yahan dikhenge.
          </p>
        )}
      </div>

      {/* daily questions */}
      <div className="card">
        <h2 style={{ marginTop: 0 }}>Roz ke 3 questions</h2>
        {plan && plan.questions.map((q: DailyQuestion, i: number) => (
          <div key={q.id} className="q-block">
            <p style={{ fontWeight: 600, marginBottom: 8 }}>
              Q{i + 1}. {q.prompt}
              <span className="tag" style={{ marginLeft: 8 }}>{q.level}</span>
            </p>
            <div className="choices">
              {q.choices.map((c, idx) => (
                <label
                  key={idx}
                  className={'choice' + (answers[q.id] === idx ? ' selected' : '') + (score ? ' locked' : '')}
                >
                  <input
                    type="radio"
                    name={q.id}
                    checked={answers[q.id] === idx}
                    onChange={() => pick(q.id, idx)}
                    disabled={!!score}
                  />
                  <span>{c}</span>
                </label>
              ))}
            </div>
          </div>
        ))}
        {!score ? (
          <button
            className="btn primary"
            disabled={busy || !plan || Object.keys(answers).length < (plan ? plan.questions.length : 3)}
            onClick={submit}
          >
            {busy ? 'Checking…' : 'Submit answers'}
          </button>
        ) : (
          <div className="score-banner">
            <span className="score-num">{score.correct}/{score.total}</span>
            <span className="muted">
              {score.correct === score.total
                ? 'Perfect — kal phir milte hain!'
                : 'Kal phir try karo, streak banao.'}
            </span>
          </div>
        )}
      </div>

      <style>{`
        .task-row { display: flex; align-items: center; gap: 12px; padding: 10px 0; border-top: 1px solid #232838; }
        .task-row:first-of-type { border-top: none; }
        .pri-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
        .btn.small { padding: 6px 12px; font-size: 13px; }
        .q-block { padding: 14px 0; border-top: 1px solid #232838; }
        .q-block:first-of-type { border-top: none; }
        .choices { display: grid; gap: 8px; }
        .choice { display: flex; gap: 10px; align-items: center; padding: 10px 12px; border: 1px solid #232838; border-radius: 10px; cursor: pointer; }
        .choice.selected { border-color: #7dd3fc; background: rgba(125, 211, 252, 0.08); }
        .choice.locked { cursor: default; opacity: 0.9; }
        .choice input { accent-color: #7dd3fc; }
        .score-banner { display: flex; align-items: center; gap: 14px; padding: 14px; border: 1px solid #232838; border-radius: 12px; margin-top: 12px; }
        .score-num { font-size: 28px; font-weight: 800; color: #4ade80; }
      `}</style>
    </div>
  );
}
