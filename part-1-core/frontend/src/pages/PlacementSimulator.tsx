import { useCallback, useEffect, useRef, useState } from 'react';
import { ApiError, api } from '../lib/api';
import { useLang } from '../lib/i18n';
import './placement-simulator.css';

/* ---------- types ---------- */

interface AttemptSummary {
  id: string;
  company: string;
  status: string;
  current_round: number;
  created_at: string;
  score_summary?: string;
}

interface McqQ {
  id: string;
  prompt: string;
  choices: string[];
  difficulty?: number;
}

interface CodingProblem {
  id: string;
  title: string;
  description: string;
  starter_code?: string;
  language?: string;
}

interface InterviewQ {
  id: string;
  prompt: string;
  tips?: string;
}

interface RoundData {
  round: number;
  kind: 'mcq' | 'coding' | 'interview';
  questions: (McqQ | CodingProblem | InterviewQ)[];
  duration_minutes: number;
  cutoff?: number;
}

interface RoundResult {
  passed: boolean;
  score: number;
  total: number;
  percentage: number;
  eliminated?: boolean;
  next_round?: number | null;
  coins_earned?: number;
  message?: string;
}

interface ReportRound {
  round: number;
  name: string;
  score: number | null;
  total: number | null;
  percentage: number | null;
  passed: boolean | null;
}

interface FinalReport {
  attempt_id: string;
  company: string;
  status: string;
  rounds: ReportRound[];
  strengths: string[];
  weaknesses: string[];
  coins_earned: number;
  retry_after_days?: number | null;
}

type Phase =
  | 'loading' | 'home' | 'roundIntro' | 'taking'
  | 'roundResult' | 'eliminated' | 'placed' | 'report';

/* ---------- round config ---------- */

const ROUNDS = [
  { n: 1, key: 'aptitude', icon: '🧮', questions: 20, minutes: 30, cutoff: 60, kind: 'mcq' as const },
  { n: 2, key: 'english', icon: '🗣️', questions: 15, minutes: 20, cutoff: 60, kind: 'mcq' as const },
  { n: 3, key: 'technical', icon: '💻', questions: 20, minutes: 30, cutoff: 60, kind: 'mcq' as const },
  { n: 4, key: 'coding', icon: '⌨️', questions: 2, minutes: 60, cutoff: 100, kind: 'coding' as const },
  { n: 5, key: 'techInterview', icon: '🎤', questions: 5, minutes: 30, cutoff: 60, kind: 'interview' as const },
  { n: 6, key: 'hrInterview', icon: '👔', questions: 5, minutes: 30, cutoff: 60, kind: 'interview' as const },
];

const COMPANIES = [
  { slug: 'tcs', name: 'TCS', icon: '🏢', difficulty: 'medium' },
  { slug: 'infosys', name: 'Infosys', icon: '🏛️', difficulty: 'medium' },
  { slug: 'wipro', name: 'Wipro', icon: '🏬', difficulty: 'medium' },
  { slug: 'flipkart', name: 'Flipkart', icon: '🛒', difficulty: 'hard' },
  { slug: 'amazon', name: 'Amazon', icon: '📦', difficulty: 'hard' },
  { slug: 'google', name: 'Google', icon: '🔍', difficulty: 'expert' },
];

/* ---------- i18n ---------- */

const STR = {
  en: {
    title: 'Placement Simulator',
    subtitle: 'Real placement drive experience — 6 rounds, real cutoffs 🏆',
    selectCompany: 'Select a company',
    startDrive: 'Start Drive',
    difficulty: 'Difficulty',
    medium: 'Medium', hard: 'Hard', expert: 'Expert',
    myAttempts: 'My attempts',
    noAttempts: 'No attempts yet. Pick a company and start your first drive!',
    round: 'Round', of: 'of',
    rules: 'Rules',
    cutoff: 'cutoff to pass',
    questions: 'questions',
    minutes: 'min',
    beginRound: 'Begin Round',
    back: 'Back',
    timeLeft: 'Time left',
    submit: 'Submit',
    confirmSubmit: 'Submit your answers? You cannot change them after.',
    unanswered: 'unanswered',
    cancel: 'Cancel',
    autoSubmit: 'Time is up! Submitting automatically.',
    passed: 'PASSED',
    failed: 'FAILED',
    score: 'Score',
    nextRound: 'Next Round →',
    viewReport: 'View Report',
    eliminated: 'Eliminated',
    eliminatedIn: 'Eliminated in Round',
    retryIn: 'Retry available in',
    days: 'days',
    tips: 'Tips to improve',
    backHome: 'Back to Simulator',
    placed: 'PLACED!',
    placedMsg: 'Congratulations! You cleared all 6 rounds! 🎉',
    coinsEarned: 'coins earned',
    certificate: 'Download Certificate',
    report: 'Final Report',
    strengths: 'Strengths',
    weaknesses: 'Work on',
    perRound: 'Per-round performance',
    history: 'Attempt history',
    status: 'Status',
    company: 'Company',
    date: 'Date',
    cooldown: 'You are in cooldown. Please wait before starting a new drive.',
    loadError: 'Could not load. Please try again.',
    startError: 'Could not start the drive. Please try again.',
    submitError: 'Submit failed. Please try again.',
    interviewAnswer: 'Your answer',
    interviewPlaceholder: 'Type your answer here...',
    selfRating: 'Rate your answer',
    next: 'Next →',
    prev: '← Prev',
    finishInterview: 'Finish Interview',
    codeLanguage: 'Language',
    codePlaceholder: '// Write your solution here',
    runNote: 'Submit when ready — your code will be evaluated.',
    submitCode: 'Submit Code',
    eliminationTip1: 'Revise the topics where you scored lowest.',
    eliminationTip2: 'Take a weekly test in that domain before retrying.',
    eliminationTip3: 'Review explanations for every wrong answer.',
  },
  hi: {
    title: 'प्लेसमेंट सिम्युलेटर',
    subtitle: 'असली प्लेसमेंट ड्राइव का अनुभव — 6 राउंड, असली कटऑफ 🏆',
    selectCompany: 'कंपनी चुनें',
    startDrive: 'ड्राइव शुरू करें',
    difficulty: 'कठिनाई',
    medium: 'मध्यम', hard: 'कठिन', expert: 'विशेषज्ञ',
    myAttempts: 'मेरे प्रयास',
    noAttempts: 'अभी कोई प्रयास नहीं। कंपनी चुनें और पहली ड्राइव शुरू करें!',
    round: 'राउंड', of: 'का',
    rules: 'नियम',
    cutoff: 'पास होने के लिए कटऑफ',
    questions: 'प्रश्न',
    minutes: 'मिनट',
    beginRound: 'राउंड शुरू करें',
    back: 'वापस',
    timeLeft: 'बचा समय',
    submit: 'जमा करें',
    confirmSubmit: 'उत्तर जमा करें? बाद में बदल नहीं पाएंगे।',
    unanswered: 'अनुत्तरित',
    cancel: 'रद्द करें',
    autoSubmit: 'समय समाप्त! अपने आप जमा हो रहा है।',
    passed: 'पास',
    failed: 'फेल',
    score: 'स्कोर',
    nextRound: 'अगला राउंड →',
    viewReport: 'रिपोर्ट देखें',
    eliminated: 'बाहर',
    eliminatedIn: 'राउंड में बाहर',
    retryIn: 'पुनः प्रयास',
    days: 'दिन में',
    tips: 'सुधार के सुझाव',
    backHome: 'सिम्युलेटर पर वापस',
    placed: 'प्लेस्ड!',
    placedMsg: 'बधाई हो! आपने सभी 6 राउंड पास कर लिए! 🎉',
    coinsEarned: 'coins मिले',
    certificate: 'सर्टिफिकेट डाउनलोड करें',
    report: 'अंतिम रिपोर्ट',
    strengths: 'मजबूती',
    weaknesses: 'सुधारें',
    perRound: 'हर राउंड का प्रदर्शन',
    history: 'प्रयासों का इतिहास',
    status: 'स्थिति',
    company: 'कंपनी',
    date: 'तारीख',
    cooldown: 'आप कूलडाउन में हैं। नई ड्राइव से पहले प्रतीक्षा करें।',
    loadError: 'लोड नहीं हो सका। पुनः प्रयास करें।',
    startError: 'ड्राइव शुरू नहीं हो सकी। पुनः प्रयास करें।',
    submitError: 'जमा असफल। पुनः प्रयास करें।',
    interviewAnswer: 'आपका उत्तर',
    interviewPlaceholder: 'अपना उत्तर यहां लिखें...',
    selfRating: 'अपने उत्तर को रेट करें',
    next: 'अगला →',
    prev: '← पिछला',
    finishInterview: 'इंटरव्यू समाप्त करें',
    codeLanguage: 'भाषा',
    codePlaceholder: '// अपना समाधान यहां लिखें',
    runNote: 'तैयार होने पर जमा करें — आपका कोड मूल्यांकित होगा।',
    submitCode: 'कोड जमा करें',
    eliminationTip1: 'जिन topics में सबसे कम स्कोर आया, उन्हें दोहराएं।',
    eliminationTip2: 'पुनः प्रयास से पहले उस domain का weekly test दें।',
    eliminationTip3: 'हर गलत उत्तर का explanation पढ़ें।',
  },
  hinglish: {
    title: 'Placement Simulator',
    subtitle: 'Real placement drive experience — 6 rounds, real cutoffs 🏆',
    selectCompany: 'Company select karo',
    startDrive: 'Drive shuru karo',
    difficulty: 'Difficulty',
    medium: 'Medium', hard: 'Hard', expert: 'Expert',
    myAttempts: 'Mere attempts',
    noAttempts: 'Abhi koi attempt nahi. Company chuno aur pehli drive shuru karo!',
    round: 'Round', of: 'ka',
    rules: 'Rules',
    cutoff: 'pass hone ke liye cutoff',
    questions: 'questions',
    minutes: 'min',
    beginRound: 'Round shuru karo',
    back: 'Wapas',
    timeLeft: 'Time left',
    submit: 'Submit karo',
    confirmSubmit: 'Answers submit karun? Baad me change nahi kar paoge.',
    unanswered: 'unanswered',
    cancel: 'Cancel',
    autoSubmit: 'Time khatm! Auto-submit ho raha hai.',
    passed: 'PASS',
    failed: 'FAIL',
    score: 'Score',
    nextRound: 'Agla Round →',
    viewReport: 'Report dekho',
    eliminated: 'Eliminated',
    eliminatedIn: 'Round me bahar',
    retryIn: 'Retry',
    days: 'din me',
    tips: 'Improve karne ke tips',
    backHome: 'Simulator par wapas',
    placed: 'PLACED!',
    placedMsg: 'Badhai ho! Tumne saare 6 rounds clear kar diye! 🎉',
    coinsEarned: 'coins mile',
    certificate: 'Certificate download karo',
    report: 'Final Report',
    strengths: 'Strengths',
    weaknesses: 'Sudharo',
    perRound: 'Har round ka performance',
    history: 'Attempt history',
    status: 'Status',
    company: 'Company',
    date: 'Date',
    cooldown: 'Tum cooldown me ho. Nayi drive se pehle wait karo.',
    loadError: 'Load nahi ho paya. Dobara try karo.',
    startError: 'Drive start nahi ho payi. Dobara try karo.',
    submitError: 'Submit fail ho gaya. Dobara try karo.',
    interviewAnswer: 'Tumhara answer',
    interviewPlaceholder: 'Apna answer yahan likho...',
    selfRating: 'Apne answer ko rate karo',
    next: 'Agla →',
    prev: '← Pichhla',
    finishInterview: 'Interview khatm karo',
    codeLanguage: 'Language',
    codePlaceholder: '// Apna solution yahan likho',
    runNote: 'Ready ho to submit karo — tumhara code evaluate hoga.',
    submitCode: 'Code submit karo',
    eliminationTip1: 'Jin topics me sabse kam score aaya, unhe revise karo.',
    eliminationTip2: 'Retry se pehle us domain ka weekly test do.',
    eliminationTip3: 'Har galat answer ka explanation padho.',
  },
};

const ROUND_NAMES: Record<string, Record<'en' | 'hi' | 'hinglish', string>> = {
  aptitude: { en: 'Aptitude', hi: 'एप्टिट्यूड', hinglish: 'Aptitude' },
  english: { en: 'English', hi: 'अंग्रेजी', hinglish: 'English' },
  technical: { en: 'Technical MCQ', hi: 'तकनीकी MCQ', hinglish: 'Technical MCQ' },
  coding: { en: 'Coding', hi: 'कोडिंग', hinglish: 'Coding' },
  techInterview: { en: 'Technical Interview', hi: 'तकनीकी इंटरव्यू', hinglish: 'Technical Interview' },
  hrInterview: { en: 'HR Interview', hi: 'HR इंटरव्यू', hinglish: 'HR Interview' },
};

export default function PlacementSimulator() {
  const { lang } = useLang();
  const t = STR[lang] ?? STR.en;
  const [phase, setPhase] = useState<Phase>('loading');
  const [attempts, setAttempts] = useState<AttemptSummary[]>([]);
  const [company, setCompany] = useState<string | null>(null);
  const [attemptId, setAttemptId] = useState<string | null>(null);
  const [roundN, setRoundN] = useState(1);
  const [roundData, setRoundData] = useState<RoundData | null>(null);
  const [answers, setAnswers] = useState<Record<string, number | string>>({});
  const [ratings, setRatings] = useState<Record<string, number>>({});
  const [codeLang, setCodeLang] = useState('python');
  const [qIndex, setQIndex] = useState(0);
  const [secondsLeft, setSecondsLeft] = useState(0);
  const [roundResult, setRoundResult] = useState<RoundResult | null>(null);
  const [report, setReport] = useState<FinalReport | null>(null);
  const [showConfirm, setShowConfirm] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [cooldown, setCooldown] = useState(false);
  const timerRef = useRef<number | null>(null);

  const roundCfg = ROUNDS[roundN - 1];
  const roundName = (key: string) => ROUND_NAMES[key]?.[lang] ?? ROUND_NAMES[key]?.en ?? key;

  const stopTimer = () => {
    if (timerRef.current) { window.clearInterval(timerRef.current); timerRef.current = null; }
  };
  useEffect(() => stopTimer, []);

  const apiErr = (e: unknown, fallback: string) => {
    if (e instanceof ApiError && e.status === 429) { setCooldown(true); setError(t.cooldown); }
    else setError(fallback);
  };

  /* ---------- home ---------- */

  const load = useCallback(async () => {
    setPhase('loading'); setError(null); setCooldown(false);
    try {
      const data = await api<{ attempts: AttemptSummary[] }>('/api/v1/simulator/mine');
      setAttempts(data.attempts ?? []);
    } catch (e) { apiErr(e, t.loadError); } finally { setPhase('home'); }
  }, [t]);

  useEffect(() => { load(); }, [load]);

  /* ---------- start ---------- */

  const startDrive = async () => {
    if (!company) return;
    setError(null); setCooldown(false);
    try {
      const data = await api<{ id: string; current_round?: number }>(
        '/api/v1/simulator/start', { method: 'POST', body: JSON.stringify({ company }) });
      setAttemptId(data.id);
      setRoundN(data.current_round ?? 1);
      setPhase('roundIntro');
    } catch (e) { apiErr(e, t.startError); }
  };

  /* ---------- round fetch ---------- */

  const beginRound = async () => {
    if (!attemptId) return;
    setError(null);
    try {
      const data = await api<RoundData>(`/api/v1/simulator/attempt/${attemptId}/round/${roundN}`);
      setRoundData(data);
      setAnswers({}); setRatings({}); setQIndex(0);
      setSecondsLeft((data.duration_minutes || roundCfg.minutes) * 60);
      setPhase('taking');
      stopTimer();
      timerRef.current = window.setInterval(() => {
        setSecondsLeft(prev => {
          if (prev <= 1) { stopTimer(); doSubmitRef.current(true); return 0; }
          return prev - 1;
        });
      }, 1000);
    } catch (e) { apiErr(e, t.loadError); }
  };

  /* ---------- submit ---------- */

  const doSubmit = async (auto = false) => {
    if (!attemptId || !roundData) return;
    stopTimer(); setShowConfirm(false);
    try {
      const payload: Record<string, unknown> = { kind: roundData.kind };
      if (roundData.kind === 'mcq') payload.answers = answers;
      else if (roundData.kind === 'coding') payload.solutions = { ...answers, language: codeLang };
      else payload.responses = roundData.questions.map(q => ({
        question_id: (q as InterviewQ).id,
        answer: answers[(q as InterviewQ).id] ?? '',
        self_rating: ratings[(q as InterviewQ).id] ?? 0,
      }));
      const r = await api<RoundResult>(
        `/api/v1/simulator/attempt/${attemptId}/round/${roundN}/submit`,
        { method: 'POST', body: JSON.stringify(payload) });
      setRoundResult(r);
      if (auto) alert(t.autoSubmit);
      if (r.eliminated || !r.passed) setPhase('eliminated');
      else if (roundN === 6) setPhase('placed');
      else setPhase('roundResult');
    } catch (e) { apiErr(e, t.submitError); }
  };
  const doSubmitRef = useRef(doSubmit);
  doSubmitRef.current = doSubmit;

  const nextRound = () => {
    setRoundN(roundN + 1);
    setRoundData(null);
    setPhase('roundIntro');
  };

  /* ---------- report ---------- */

  const loadReport = async (id: string) => {
    setError(null);
    try {
      const r = await api<FinalReport>(`/api/v1/simulator/attempt/${id}/report`);
      setReport(r);
      setPhase('report');
    } catch (e) { apiErr(e, t.loadError); }
  };

  const fmtTime = (s: number) => `${Math.floor(s / 60)}:${(s % 60).toString().padStart(2, '0')}`;

  /* ================= render ================= */

  if (phase === 'loading') {
    return <div className="ps-page"><div className="ps-loading">…</div></div>;
  }

  /* ----- home: company select + history ----- */
  if (phase === 'home') {
    return (
      <div className="ps-page">
        <h1>🏆 {t.title}</h1>
        <p className="ps-sub">{t.subtitle}</p>
        {error && <div className="ps-error">{error}</div>}
        <h2>{t.selectCompany}</h2>
        <div className="ps-companies">
          {COMPANIES.map(c => (
            <button
              key={c.slug}
              className={`ps-company ${company === c.slug ? 'selected' : ''}`}
              onClick={() => setCompany(c.slug)}
            >
              <span className="ps-company-icon">{c.icon}</span>
              <span className="ps-company-name">{c.name}</span>
              <span className={`ps-diff ps-diff-${c.difficulty}`}>{t[c.difficulty as 'medium']}</span>
            </button>
          ))}
        </div>
        <button className="ps-cta" disabled={!company || cooldown} onClick={startDrive}>
          {t.startDrive}
        </button>

        <h2>{t.myAttempts}</h2>
        {attempts.length === 0 ? (
          <p className="ps-empty">{t.noAttempts}</p>
        ) : (
          <div className="ps-history">
            {attempts.map(a => (
              <div key={a.id} className="ps-attempt" onClick={() => loadReport(a.id)}>
                <span className="ps-attempt-co">{a.company}</span>
                <span className={`ps-status ps-status-${a.status}`}>{a.status}</span>
                <span className="ps-attempt-date">
                  {a.created_at ? new Date(a.created_at).toLocaleDateString() : ''}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  }

  /* ----- round intro ----- */
  if (phase === 'roundIntro') {
    const cfg = ROUNDS[roundN - 1];
    return (
      <div className="ps-page ps-center">
        <div className="ps-intro">
          <div className="ps-intro-round">{t.round} {roundN} {t.of} 6</div>
          <div className="ps-intro-icon">{cfg.icon}</div>
          <h2>{roundName(cfg.key)}</h2>
          <div className="ps-rules">
            <div className="ps-rule"><span>❓</span> {cfg.questions} {t.questions}</div>
            <div className="ps-rule"><span>⏱</span> {cfg.minutes} {t.minutes}</div>
            <div className="ps-rule"><span>🎯</span> {cfg.cutoff}% {t.cutoff}</div>
          </div>
          <button className="ps-cta" onClick={beginRound}>{t.beginRound}</button>
          <button className="ps-ghost" onClick={() => setPhase('home')}>{t.back}</button>
        </div>
      </div>
    );
  }

  /* ----- taking: mcq / coding / interview ----- */
  if (phase === 'taking' && roundData) {
    const qs = roundData.questions;
    const answered = Object.keys(answers).filter(k => k !== 'language').length;
    const q = qs[qIndex];

    return (
      <div className="ps-page">
        <div className="ps-timerbar">
          <span className="ps-round-label">{roundCfg.icon} {t.round} {roundN}/6</span>
          <span className={secondsLeft < 300 ? 'ps-timer danger' : 'ps-timer'}>
            ⏱ {t.timeLeft}: {fmtTime(secondsLeft)}
          </span>
          <div className="ps-progress">
            <div className="ps-progress-fill" style={{ width: `${(answered / qs.length) * 100}%` }} />
          </div>
          <span className="ps-answered">{answered}/{qs.length}</span>
        </div>
        {error && <div className="ps-error">{error}</div>}

        {roundData.kind === 'mcq' && q && 'choices' in q && (
          <McqCard
            q={q as McqQ} index={qIndex} total={qs.length} t={t}
            selected={answers[q.id] as number | undefined}
            onSelect={(i) => setAnswers(a => ({ ...a, [q.id]: i }))}
          />
        )}

        {roundData.kind === 'coding' && q && 'description' in q && (
          <div className="ps-card">
            <div className="ps-qhead"><span>{(q as CodingProblem).title}</span></div>
            <p className="ps-prompt">{(q as CodingProblem).description}</p>
            <div className="ps-lang-row">
              <label>{t.codeLanguage}:</label>
              <select value={codeLang} onChange={e => setCodeLang(e.target.value)} className="ps-select">
                <option value="python">Python</option>
                <option value="c">C</option>
                <option value="cpp">C++</option>
                <option value="java">Java</option>
                <option value="javascript">JavaScript</option>
              </select>
            </div>
            <textarea
              className="ps-code"
              placeholder={t.codePlaceholder}
              value={(answers[q.id] as string) ?? (q as CodingProblem).starter_code ?? ''}
              onChange={e => setAnswers(a => ({ ...a, [q.id]: e.target.value }))}
              spellCheck={false}
            />
            <p className="ps-note">{t.runNote}</p>
          </div>
        )}

        {roundData.kind === 'interview' && q && 'prompt' in q && !('choices' in q) && !('description' in q) && (
          <div className="ps-card">
            <div className="ps-qhead"><span>Q{qIndex + 1} {t.of} {qs.length}</span></div>
            <p className="ps-prompt">{(q as InterviewQ).prompt}</p>
            {(q as InterviewQ).tips && <p className="ps-tip">💡 {(q as InterviewQ).tips}</p>}
            <label className="ps-label">{t.interviewAnswer}</label>
            <textarea
              className="ps-textarea"
              placeholder={t.interviewPlaceholder}
              value={(answers[q.id] as string) ?? ''}
              onChange={e => setAnswers(a => ({ ...a, [q.id]: e.target.value }))}
            />
            <label className="ps-label">{t.selfRating}</label>
            <div className="ps-rating">
              {[1, 2, 3, 4, 5].map(r => (
                <button
                  key={r}
                  className={`ps-star ${(ratings[q.id] ?? 0) >= r ? 'on' : ''}`}
                  onClick={() => setRatings(x => ({ ...x, [q.id]: r }))}
                >★</button>
              ))}
            </div>
          </div>
        )}

        <div className="ps-nav">
          <button disabled={qIndex === 0} onClick={() => setQIndex(qIndex - 1)}>{t.prev}</button>
          <div className="ps-dots">
            {qs.map((qq, i) => {
              const id = (qq as McqQ).id;
              return (
                <button key={id}
                  className={`ps-dot ${i === qIndex ? 'current' : ''} ${answers[id] !== undefined && answers[id] !== '' ? 'done' : ''}`}
                  onClick={() => setQIndex(i)} />
              );
            })}
          </div>
          {qIndex < qs.length - 1
            ? <button onClick={() => setQIndex(qIndex + 1)}>{t.next}</button>
            : roundData.kind === 'interview'
              ? <button className="ps-submit" onClick={() => doSubmit()}>{t.finishInterview}</button>
              : roundData.kind === 'coding'
                ? <button className="ps-submit" onClick={() => doSubmit()}>{t.submitCode}</button>
                : <button className="ps-submit" onClick={() => setShowConfirm(true)}>{t.submit}</button>}
        </div>

        {showConfirm && (
          <div className="ps-modal-backdrop">
            <div className="ps-modal">
              <p>{t.confirmSubmit}</p>
              <p className="ps-modal-sub">{answered}/{qs.length} · {qs.length - answered} {t.unanswered}</p>
              <div className="ps-modal-actions">
                <button onClick={() => setShowConfirm(false)}>{t.cancel}</button>
                <button className="ps-submit" onClick={() => doSubmit()}>{t.submit}</button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  /* ----- round result ----- */
  if (phase === 'roundResult' && roundResult) {
    return (
      <div className="ps-page ps-center">
        <div className={`ps-result-card ${roundResult.passed ? 'pass' : 'fail'}`}>
          <div className="ps-result-badge">{roundResult.passed ? t.passed : t.failed}</div>
          <div className="ps-result-score">{t.score}: {roundResult.score}/{roundResult.total}</div>
          <div className="ps-result-pct">{Math.round(roundResult.percentage)}%</div>
          <div className="ps-result-bar">
            <div className="ps-result-fill" style={{ width: `${roundResult.percentage}%` }} />
          </div>
          {roundResult.coins_earned ? (
            <div className="ps-coins">🪙 +{roundResult.coins_earned} {t.coinsEarned}</div>
          ) : null}
          <button className="ps-cta" onClick={nextRound}>{t.nextRound}</button>
        </div>
      </div>
    );
  }

  /* ----- eliminated ----- */
  if (phase === 'eliminated') {
    const rr = roundResult;
    return (
      <div className="ps-page ps-center">
        <div className="ps-elim">
          <div className="ps-elim-icon">❌</div>
          <h2>{t.eliminated}</h2>
          <p>{t.eliminatedIn} {roundN}</p>
          {rr && <p className="ps-elim-score">{t.score}: {rr.score}/{rr.total} ({Math.round(rr.percentage)}%)</p>}
          <div className="ps-tips">
            <h3>{t.tips}</h3>
            <ul>
              <li>{t.eliminationTip1}</li>
              <li>{t.eliminationTip2}</li>
              <li>{t.eliminationTip3}</li>
            </ul>
          </div>
          {attemptId && (
            <button className="ps-ghost" onClick={() => loadReport(attemptId)}>{t.viewReport}</button>
          )}
          <button className="ps-cta" onClick={() => setPhase('home')}>{t.backHome}</button>
        </div>
      </div>
    );
  }

  /* ----- placed ----- */
  if (phase === 'placed') {
    return (
      <div className="ps-page ps-center">
        <div className="ps-placed">
          <div className="ps-confetti">{'🎉🎊✨🏆✨🎊🎉'}</div>
          <h1>{t.placed}</h1>
          <p>{t.placedMsg}</p>
          {roundResult?.coins_earned ? (
            <div className="ps-coins big">🪙 +{roundResult.coins_earned} {t.coinsEarned}</div>
          ) : null}
          <div className="ps-placed-actions">
            {attemptId && (
              <>
                <button className="ps-cta" onClick={() => loadReport(attemptId)}>{t.viewReport}</button>
                <a
                  className="ps-ghost ps-link"
                  href={`/api/v1/simulator/attempt/${attemptId}/certificate`}
                  target="_blank" rel="noreferrer"
                >{t.certificate}</a>
              </>
            )}
            <button className="ps-ghost" onClick={() => setPhase('home')}>{t.backHome}</button>
          </div>
        </div>
      </div>
    );
  }

  /* ----- report ----- */
  if (phase === 'report' && report) {
    return (
      <div className="ps-page">
        <h1>📊 {t.report}</h1>
        <p className="ps-sub">{report.company} · <span className={`ps-status ps-status-${report.status}`}>{report.status}</span></p>
        <h2>{t.perRound}</h2>
        <div className="ps-report-rounds">
          {report.rounds.map(r => (
            <div key={r.round} className="ps-rr">
              <span className="ps-rr-name">{r.round}. {roundName(ROUNDS[r.round - 1]?.key ?? '')}</span>
              <div className="ps-rr-bar">
                <div
                  className={`ps-rr-fill ${r.passed ? 'pass' : r.passed === false ? 'fail' : ''}`}
                  style={{ width: `${r.percentage ?? 0}%` }}
                />
              </div>
              <span className="ps-rr-score">
                {r.percentage != null ? `${Math.round(r.percentage)}%` : '—'}
              </span>
            </div>
          ))}
        </div>
        <div className="ps-sw">
          <div className="ps-sw-col">
            <h3>💪 {t.strengths}</h3>
            <ul>{report.strengths.map((s, i) => <li key={i}>{s}</li>)}</ul>
          </div>
          <div className="ps-sw-col">
            <h3>🎯 {t.weaknesses}</h3>
            <ul>{report.weaknesses.map((s, i) => <li key={i}>{s}</li>)}</ul>
          </div>
        </div>
        <button className="ps-cta" onClick={() => setPhase('home')}>{t.backHome}</button>
      </div>
    );
  }

  return <div className="ps-page"><div className="ps-loading">…</div></div>;
}

/* ---------- MCQ card ---------- */

function McqCard({ q, index, total, t, selected, onSelect }: {
  q: McqQ; index: number; total: number;
  t: Record<string, string>;
  selected: number | undefined;
  onSelect: (i: number) => void;
}) {
  return (
    <div className="ps-card">
      <div className="ps-qhead">
        <span>Q{index + 1} {t.of} {total}</span>
      </div>
      <p className="ps-prompt">{q.prompt}</p>
      <div className="ps-choices">
        {q.choices.map((c, i) => (
          <button
            key={i}
            className={`ps-choice ${selected === i ? 'selected' : ''}`}
            onClick={() => onSelect(i)}
          >
            <span className="ps-choice-letter">{'ABCD'[i]}</span> {c}
          </button>
        ))}
      </div>
    </div>
  );
}
