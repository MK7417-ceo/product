import { useEffect, useState } from 'react';
import { englishApi, ApiError, type EnglishQuestion } from '../lib/p1api';
import './p1-pages.css';

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
    englishApi
      .daily()
      .then((r) => {
        setQuestions(r.questions);
        setDate(r.date);
      })
      .catch((err) => setError(err instanceof ApiError ? err.message : 'Load failed'))
      .finally(() => setLoading(false));
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

  if (loading)
    return (
      <div className="p1x">
        <p className="p1x-loading">Loading today's English set…</p>
      </div>
    );

  const answered = Object.keys(answers).length;
  const pct = questions.length ? Math.round((100 * answered) / questions.length) : 0;

  return (
    <div className="p1x">
      <div className="p1x-head">
        <div>
          <h1 className="p1x-title">English</h1>
          <p className="p1x-sub">{date} — roz 5 questions: vocabulary, grammar, reading. Foreign-company ready.</p>
        </div>
      </div>
      {error && <div className="p1x-err">{error}</div>}

      <div className="p1x-card">
        <h2>Daily drill</h2>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, color: 'var(--muted)', margin: '4px 0 6px' }}>
          <span>ANSWERED</span>
          <span style={{ fontWeight: 700 }}>{answered}/{questions.length}</span>
        </div>
        <div className="p1x-bar" style={{ marginBottom: 8 }}>
          <i style={{ width: `${pct}%` }} />
        </div>

        {questions.map((q, i) => (
          <div key={q.id} className="p1x-qblock">
            {q.passage && <p className="p1x-passage">{q.passage}</p>}
            <p className="qp">
              Q{i + 1}. {q.prompt}
              <span className="p1x-pill claim" style={{ marginLeft: 8 }}>
                {(KIND_LABEL[q.kind] || q.kind).toUpperCase()} · {q.level.toUpperCase()}
              </span>
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
        {questions.length === 0 && <p className="p1x-empty">Aaj ka set load nahi ho paaya.</p>}

        {!score ? (
          <button
            className="p1x-btn"
            disabled={busy || answered < questions.length || questions.length === 0}
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
                ? 'Flawless — IELTS band 8 energy!'
                : score.correct >= 3
                  ? 'Good — roz practice se aur badhega.'
                  : 'Kal phir try karo — consistency jeet ti hai.'}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
