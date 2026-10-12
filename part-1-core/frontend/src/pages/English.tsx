import { useEffect, useState } from 'react';
import { englishApi, ApiError, type EnglishQuestion } from '../lib/api';

const KIND_LABEL: Record<string, string> = {
  vocabulary: 'Vocabulary', grammar: 'Grammar', comprehension: 'Reading',
};

export default function English() {
  const [questions, setQuestions] = useState<EnglishQuestion[]>([]);
  const [date, setDate] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [score, setScore] = useState<{ correct: number; total: number } | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const r = await englishApi.daily();
        setQuestions(r.questions);
        setDate(r.date);
      } catch (err) {
        setError(err instanceof ApiError ? err.message : 'Load failed');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const pick = (qid: string, idx: number) => {
    if (score) return;
    setAnswers((a) => ({ ...a, [qid]: idx }));
  };

  const submit = async () => {
    if (score || busy) return;
    setError('');
    setBusy(true);
    try {
      const r = await englishApi.submit(answers);
      setScore({ correct: r.correct, total: r.total });
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Submit failed');
    } finally {
      setBusy(false);
    }
  };

  if (loading) return <p className="page-sub">Loading today's English set…</p>;

  return (
    <div>
      <h1 className="page-title">English</h1>
      <p className="page-sub">{date} — roz 5 questions: vocabulary, grammar, reading. Foreign-company ready.</p>
      {error && <p className="error">{error}</p>}

      <div className="card">
        {questions.map((q, i) => (
          <div key={q.id} className="q-block">
            {q.passage && <p className="passage">{q.passage}</p>}
            <p style={{ fontWeight: 600, marginBottom: 8 }}>
              Q{i + 1}. {q.prompt}
              <span className="tag" style={{ marginLeft: 8 }}>{KIND_LABEL[q.kind] || q.kind} · {q.level}</span>
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
            disabled={busy || Object.keys(answers).length < questions.length}
            onClick={submit}
            style={{ marginTop: 12 }}
          >
            {busy ? 'Checking…' : 'Submit answers'}
          </button>
        ) : (
          <div className="score-banner">
            <span className="score-num">{score.correct}/{score.total}</span>
            <span className="muted">
              {score.correct === score.total
                ? 'Flawless — IELTS band 8 energy!'
                : score.correct >= 3
                  ? 'Good — roz practice se aur badhega.'
                  : 'Kal phir try karo — consistency jeet ti hai.'}
            </span>
          </div>
        )}
      </div>

      <style>{`
        .q-block { padding: 14px 0; border-top: 1px solid #232838; }
        .q-block:first-of-type { border-top: none; }
        .passage { background: #0d1117; border-left: 3px solid #7dd3fc; padding: 10px 12px; font-size: 14px; color: #c6cddb; border-radius: 0 8px 8px 0; }
        .choices { display: grid; gap: 8px; }
        .choice { display: flex; gap: 10px; align-items: center; padding: 10px 12px; border: 1px solid #232838; border-radius: 10px; cursor: pointer; }
        .choice.selected { border-color: #7dd3fc; background: rgba(125, 211, 252, 0.08); }
        .choice.locked { cursor: default; opacity: 0.9; }
        .choice input { accent-color: #7dd3fc; }
        .tag { font-size: 12px; color: #8b93a7; border: 1px solid #232838; border-radius: 12px; padding: 2px 10px; white-space: nowrap; }
        .score-banner { display: flex; align-items: center; gap: 14px; padding: 14px; border: 1px solid #232838; border-radius: 12px; margin-top: 12px; }
        .score-num { font-size: 28px; font-weight: 800; color: #4ade80; }
      `}</style>
    </div>
  );
}
