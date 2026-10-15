import { useCallback, useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../lib/api';
import { useLang } from '../lib/i18n';
import './weekly-test.css';

interface TestSummary {
  id: string;
  domain_slug: string;
  week_number: number;
  scheduled_date: string | null;
  status: string;
  score: number | null;
  total_questions: number;
}

interface Question {
  id: string;
  prompt: string;
  choices: string[];
  difficulty: number;
  explanation?: string;
}

interface TestSession {
  test: TestSummary;
  questions: Question[];
  duration_minutes: number;
}

interface TestResult {
  score: number;
  total: number;
  percentage: number;
  grade: string;
  grade_message: string;
  coins_earned: number;
  review: {
    question_id: string;
    prompt: string;
    choices: string[];
    given: number | null;
    correct: number | null;
    is_correct: boolean;
    explanation: string;
  }[];
}

type Phase = 'loading' | 'overview' | 'taking' | 'result';

const STR = {
  en: {
    title: 'Weekly Tests',
    subtitle: 'Test yourself every week — track your growth 📈',
    upcoming: 'Upcoming',
    past: 'Past tests',
    noTests: 'No weekly tests yet. Create a study plan to get weekly tests scheduled automatically!',
    startTest: 'Start Test',
    week: 'Week',
    questions: 'questions',
    minutes: 'min',
    timeLeft: 'Time left',
    questionOf: 'of',
    submit: 'Submit Test',
    confirmSubmit: 'Submit your answers? You cannot change them after.',
    cancel: 'Cancel',
    score: 'Score',
    grade: 'Grade',
    coinsEarned: 'coins earned',
    reviewAnswers: 'Review answers',
    correct: 'Correct',
    wrong: 'Wrong',
    yourAnswer: 'Your answer',
    correctAnswer: 'Correct answer',
    notAnswered: 'Not answered',
    backToTests: 'Back to tests',
    trend: 'Score trend',
    statusScheduled: 'Scheduled',
    statusActive: 'In progress',
    statusCompleted: 'Completed',
    statusMissed: 'Missed',
    nextIn: 'Next test in',
    days: 'days',
    today: 'today!',
    autoSubmit: 'Time is up! Submitting automatically.',
  },
  hi: {
    title: 'साप्ताहिक टेस्ट',
    subtitle: 'हर हफ्ते खुद को परखें — अपनी growth देखें 📈',
    upcoming: 'आगामी',
    past: 'पिछले टेस्ट',
    noTests: 'अभी कोई weekly test नहीं है। Study plan बनाएं — weekly tests अपने आप schedule हो जाएंगे!',
    startTest: 'टेस्ट शुरू करें',
    week: 'सप्ताह',
    questions: 'प्रश्न',
    minutes: 'मिनट',
    timeLeft: 'बचा समय',
    questionOf: 'का',
    submit: 'टेस्ट जमा करें',
    confirmSubmit: 'उत्तर जमा करें? बाद में बदल नहीं पाएंगे।',
    cancel: 'रद्द करें',
    score: 'स्कोर',
    grade: 'ग्रेड',
    coinsEarned: 'coins मिले',
    reviewAnswers: 'उत्तर देखें',
    correct: 'सही',
    wrong: 'गलत',
    yourAnswer: 'आपका उत्तर',
    correctAnswer: 'सही उत्तर',
    notAnswered: 'उत्तर नहीं दिया',
    backToTests: 'टेस्ट पर वापस',
    trend: 'स्कोर ट्रेंड',
    statusScheduled: 'निर्धारित',
    statusActive: 'चल रहा है',
    statusCompleted: 'पूर्ण',
    statusMissed: 'छूट गया',
    nextIn: 'अगला टेस्ट',
    days: 'दिन में',
    today: 'आज!',
    autoSubmit: 'समय समाप्त! अपने आप जमा हो रहा है।',
  },
  hinglish: {
    title: 'Weekly Tests',
    subtitle: 'Har hafte khud ko parkho — apni growth dekho 📈',
    upcoming: 'Upcoming',
    past: 'Past tests',
    noTests: 'Abhi koi weekly test nahi hai. Study plan banao — weekly tests apne aap schedule ho jayenge!',
    startTest: 'Test shuru karo',
    week: 'Week',
    questions: 'questions',
    minutes: 'min',
    timeLeft: 'Time left',
    questionOf: 'of',
    submit: 'Submit karo',
    confirmSubmit: 'Answers submit karun? Baad me change nahi kar paoge.',
    cancel: 'Cancel',
    score: 'Score',
    grade: 'Grade',
    coinsEarned: 'coins mile',
    reviewAnswers: 'Answers dekho',
    correct: 'Sahi',
    wrong: 'Galat',
    yourAnswer: 'Tumhara answer',
    correctAnswer: 'Sahi answer',
    notAnswered: 'Answer nahi diya',
    backToTests: 'Tests par wapas',
    trend: 'Score trend',
    statusScheduled: 'Scheduled',
    statusActive: 'Chal raha hai',
    statusCompleted: 'Complete',
    statusMissed: 'Miss ho gaya',
    nextIn: 'Agla test',
    days: 'din me',
    today: 'aaj!',
    autoSubmit: 'Time khatm! Auto-submit ho raha hai.',
  },
};

const GRADE_COLORS: Record<string, string> = {
  S: '#ffd700', A: '#4ade80', B: '#60a5fa',
  C: '#facc15', D: '#fb923c', F: '#f87171',
};

export default function WeeklyTest() {
  const { lang } = useLang();
  const t = STR[lang] ?? STR.en;
  const navigate = useNavigate();
  const [phase, setPhase] = useState<Phase>('loading');
  const [upcoming, setUpcoming] = useState<TestSummary[]>([]);
  const [past, setPast] = useState<TestSummary[]>([]);
  const [daysUntil, setDaysUntil] = useState<number | null>(null);
  const [session, setSession] = useState<TestSession | null>(null);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [qIndex, setQIndex] = useState(0);
  const [secondsLeft, setSecondsLeft] = useState(0);
  const [result, setResult] = useState<TestResult | null>(null);
  const [showConfirm, setShowConfirm] = useState(false);
  const timerRef = useRef<number | null>(null);

  const load = useCallback(async () => {
    setPhase('loading');
    try {
      const data = await api<{
        upcoming: TestSummary[]; past: TestSummary[];
        days_until_next: number | null;
      }>('/api/v1/weekly-tests/mine');
      setUpcoming(data.upcoming ?? []);
      setPast(data.past ?? []);
      setDaysUntil(data.days_until_next);
      setPhase('overview');
    } catch {
      setPhase('overview');
    }
  }, []);

  useEffect(() => { load(); }, [load]);
  useEffect(() => () => { if (timerRef.current) window.clearInterval(timerRef.current); }, []);

  const startTest = async (test: TestSummary) => {
    try {
      const s = await api<TestSession>(`/api/v1/weekly-tests/start/${test.id}`, { method: 'POST' });
      setSession(s);
      setAnswers({});
      setQIndex(0);
      setSecondsLeft((s.duration_minutes || 30) * 60);
      setResult(null);
      setPhase('taking');
      if (timerRef.current) window.clearInterval(timerRef.current);
      timerRef.current = window.setInterval(() => {
        setSecondsLeft(prev => {
          if (prev <= 1) {
            if (timerRef.current) window.clearInterval(timerRef.current);
            doSubmit(s.test.id, true);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    } catch {
      // start failed — stay on overview
    }
  };

  const doSubmit = async (testId: string, auto = false) => {
    if (timerRef.current) window.clearInterval(timerRef.current);
    try {
      const r = await api<TestResult>(`/api/v1/weekly-tests/${testId}/submit`, {
        method: 'POST',
        body: JSON.stringify({ answers }),
      });
      setResult(r);
      setPhase('result');
      if (auto) alert(t.autoSubmit);
    } catch {
      setPhase('overview');
    }
  };

  const fmtTime = (s: number) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return `${m}:${sec.toString().padStart(2, '0')}`;
  };

  const statusLabel = (s: string) =>
    s === 'completed' ? t.statusCompleted
    : s === 'active' ? t.statusActive
    : s === 'missed' ? t.statusMissed : t.statusScheduled;

  /* ---------- render ---------- */

  if (phase === 'loading') {
    return <div className="wt-page"><div className="wt-loading">…</div></div>;
  }

  if (phase === 'taking' && session) {
    const q = session.questions[qIndex];
    const total = session.questions.length;
    const answered = Object.keys(answers).length;
    return (
      <div className="wt-page">
        <div className="wt-timerbar">
          <span className={secondsLeft < 300 ? 'wt-timer danger' : 'wt-timer'}>
            ⏱ {t.timeLeft}: {fmtTime(secondsLeft)}
          </span>
          <div className="wt-progress">
            <div className="wt-progress-fill" style={{ width: `${(answered / total) * 100}%` }} />
          </div>
          <span className="wt-answered">{answered}/{total}</span>
        </div>
        {q && (
          <div className="wt-card">
            <div className="wt-qhead">
              <span>Q{qIndex + 1} {t.questionOf} {total}</span>
              <span className="wt-diff">★{q.difficulty}</span>
            </div>
            <p className="wt-prompt">{q.prompt}</p>
            <div className="wt-choices">
              {q.choices.map((c, i) => (
                <button
                  key={i}
                  className={`wt-choice ${answers[q.id] === i ? 'selected' : ''}`}
                  onClick={() => setAnswers(a => ({ ...a, [q.id]: i }))}
                >
                  <span className="wt-choice-letter">{'ABCD'[i]}</span> {c}
                </button>
              ))}
            </div>
            <div className="wt-nav">
              <button disabled={qIndex === 0} onClick={() => setQIndex(qIndex - 1)}>←</button>
              <div className="wt-dots">
                {session.questions.map((qq, i) => (
                  <button
                    key={qq.id}
                    className={`wt-dot ${i === qIndex ? 'current' : ''} ${answers[qq.id] !== undefined ? 'done' : ''}`}
                    onClick={() => setQIndex(i)}
                  />
                ))}
              </div>
              {qIndex < total - 1
                ? <button onClick={() => setQIndex(qIndex + 1)}>→</button>
                : <button className="wt-submit" onClick={() => setShowConfirm(true)}>{t.submit}</button>}
            </div>
          </div>
        )}
        {showConfirm && (
          <div className="wt-modal-backdrop">
            <div className="wt-modal">
              <p>{t.confirmSubmit}</p>
              <p className="wt-modal-sub">{answered}/{total} answered</p>
              <div className="wt-modal-actions">
                <button onClick={() => setShowConfirm(false)}>{t.cancel}</button>
                <button className="wt-submit" onClick={() => { setShowConfirm(false); doSubmit(session.test.id); }}>
                  {t.submit}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  if (phase === 'result' && result) {
    return (
      <div className="wt-page">
        <div className="wt-card wt-result">
          <div className="wt-grade" style={{ borderColor: GRADE_COLORS[result.grade] }}>
            <span className="wt-grade-letter" style={{ color: GRADE_COLORS[result.grade] }}>
              {result.grade}
            </span>
            <span className="wt-grade-msg">{result.grade_message}</span>
          </div>
          <div className="wt-score-row">
            <div><strong>{result.score}/{result.total}</strong><span>{t.score}</span></div>
            <div><strong>{result.percentage}%</strong><span>%</span></div>
            <div><strong>🪙 {result.coinsEarned}</strong><span>{t.coinsEarned}</span></div>
          </div>
          <h3>{t.reviewAnswers}</h3>
          <div className="wt-review">
            {result.review.map(r => (
              <div key={r.question_id} className={`wt-review-item ${r.is_correct ? 'ok' : 'bad'}`}>
                <p className="wt-review-prompt">{r.prompt}</p>
                <p className={r.is_correct ? 'wt-ok' : 'wt-bad'}>
                  {r.is_correct ? `✅ ${t.correct}` : `❌ ${t.wrong}`}
                </p>
                {!r.is_correct && (
                  <p className="wt-review-detail">
                    {t.yourAnswer}: {r.given !== null && r.given !== undefined ? r.choices[r.given] : t.notAnswered}<br />
                    {t.correctAnswer}: {r.correct !== null && r.correct !== undefined ? r.choices[r.correct] : '—'}
                  </p>
                )}
                {r.explanation && <p className="wt-review-exp">💡 {r.explanation}</p>}
              </div>
            ))}
          </div>
          <button className="wt-submit" onClick={() => { setResult(null); load(); }}>
            {t.backToTests}
          </button>
        </div>
      </div>
    );
  }

  /* overview */
  const completed = past.filter(p => p.status === 'completed');
  return (
    <div className="wt-page">
      <h1>📝 {t.title}</h1>
      <p className="wt-sub">{t.subtitle}</p>

      {daysUntil !== null && upcoming.length > 0 && (
        <div className="wt-next">
          ⏳ {t.nextIn}: {daysUntil === 0 ? t.today : `${daysUntil} ${t.days}`}
        </div>
      )}

      <h2>{t.upcoming}</h2>
      {upcoming.length === 0 && past.length === 0 ? (
        <div className="wt-card wt-empty">{t.noTests}</div>
      ) : (
        <div className="wt-grid">
          {upcoming.map(u => (
            <div key={u.id} className="wt-card">
              <div className="wt-card-head">
                <strong>{t.week} {u.week_number} — {u.domain_slug}</strong>
                <span className={`wt-status ${u.status}`}>{statusLabel(u.status)}</span>
              </div>
              <p className="wt-meta">{u.total_questions} {t.questions} · 30 {t.minutes}</p>
              <button className="wt-submit" onClick={() => startTest(u)}>{t.startTest}</button>
            </div>
          ))}
        </div>
      )}

      {completed.length > 1 && (
        <>
          <h2>📈 {t.trend}</h2>
          <div className="wt-trend">
            {completed.slice().reverse().map(p => (
              <div key={p.id} className="wt-trend-bar" title={`Week ${p.week_number}: ${p.score}/${p.total_questions}`}>
                <div
                  className="wt-trend-fill"
                  style={{ height: `${((p.score ?? 0) / (p.total_questions || 20)) * 100}%` }}
                />
                <span>W{p.week_number}</span>
              </div>
            ))}
          </div>
        </>
      )}

      <h2>{t.past}</h2>
      <div className="wt-grid">
        {past.map(p => (
          <div key={p.id} className="wt-card">
            <div className="wt-card-head">
              <strong>{t.week} {p.week_number} — {p.domain_slug}</strong>
              <span className={`wt-status ${p.status}`}>{statusLabel(p.status)}</span>
            </div>
            {p.status === 'completed' && p.score !== null && (
              <p className="wt-meta">{t.score}: <strong>{p.score}/{p.total_questions}</strong></p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
