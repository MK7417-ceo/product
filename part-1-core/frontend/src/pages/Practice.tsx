import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { practiceApi, ApiError, type TodayPlan, type DailyQuestion } from '../lib/p1api';
import './p1-pages.css';

const PRI_CLASS: Record<string, string> = {
  high: 'amber', medium: 'info', low: 'claim',
};

export default function Practice() {
  const [plan, setPlan] = useState<TodayPlan | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [score, setScore] = useState<{ correct: number; total: number } | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    practiceApi
      .today()
      .then(setPlan)
      .catch((err) => setError(err instanceof ApiError ? err.message : 'Load failed'))
      .finally(() => setLoading(false));
  }, []);

  const pick = (qid: string, idx: number) => {
    if (score) return;
    setAnswers((a) => ({ ...a, [qid]: idx }));
  };

  const submit = async () => {
    if (!plan || score || busy) return;
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

  if (loading)
    return (
      <div className="p1x">
        <p className="p1x-loading">Loading aaj ka plan…</p>
      </div>
    );

  return (
    <div className="p1x">
      <div className="p1x-head">
        <div>
          <h1 className="p1x-title">Aaj ka plan</h1>
          <p className="p1x-sub">
            {plan?.date ?? ''} — roz ke 3 questions + roadmap ke aaj ke tasks. Chhote steps, roz.
          </p>
        </div>
      </div>
      {error && <div className="p1x-err">{error}</div>}

      <div className="p1x-card">
        <h2>Aaj ke tasks</h2>
        <p className="hint">Roadmap se — sabse important do tasks.</p>
        {plan && plan.tasks.length > 0 ? (
          plan.tasks.map((t) => (
            <div className="p1x-row" key={t.id}>
              <span className={`p1x-pill ${PRI_CLASS[t.priority] ?? 'claim'}`} style={{ marginTop: 2 }}>
                {t.priority.toUpperCase()}
              </span>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 600, fontSize: 14.5 }}>{t.title}</div>
                <div className="p1x-muted" style={{ fontSize: 12.5 }}>
                  ⏱ {t.effort_minutes} min · {t.status.replace('_', ' ')}
                </div>
              </div>
              <Link to="/roadmap" className="p1x-btn sm ghost" style={{ textDecoration: 'none' }}>
                Roadmap →
              </Link>
            </div>
          ))
        ) : (
          <p className="p1x-empty">
            Roadmap abhi nahi bani — <Link to="/roadmap">roadmap banao</Link> to aaj ke tasks yahan dikhenge.
          </p>
        )}
      </div>

      <div className="p1x-card">
        <h2>Roz ke 3 questions</h2>
        <p className="hint">Server-scored, streak-friendly.</p>
        {plan &&
          plan.questions.map((q: DailyQuestion, i: number) => (
            <div key={q.id} className="p1x-qblock">
              <p className="qp">
                Q{i + 1}. {q.prompt}
                <span className="p1x-pill claim" style={{ marginLeft: 8 }}>{q.level.toUpperCase()}</span>
              </p>
              <div className="p1x-choices">
                {q.choices.map((c, idx) => (
                  <label
                    key={idx}
                    className={
                      'p1x-choice' + (answers[q.id] === idx ? ' selected' : '') + (score ? ' locked' : '')
                    }
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
        {plan && plan.questions.length === 0 && <p className="p1x-empty">Aaj ke questions load nahi ho paaye.</p>}
        {!score ? (
          <button
            className="p1x-btn"
            disabled={busy || !plan || Object.keys(answers).length < (plan ? plan.questions.length : 3)}
            onClick={submit}
            style={{ marginTop: 12 }}
          >
            {busy ? 'Checking…' : 'Submit answers'}
          </button>
        ) : (
          <div className={score.correct === score.total && score.total > 0 ? 'p1x-score perfect' : 'p1x-score'}>
            <span className="num">{score.correct}/{score.total}</span>
            <span className="p1x-muted">
              {score.correct === score.total
                ? 'Perfect — kal phir milte hain!'
                : 'Kal phir try karo, streak banao.'}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
