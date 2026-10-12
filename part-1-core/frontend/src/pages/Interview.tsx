import { useEffect, useRef, useState } from 'react';
import { prepApi, ApiError, type PrepQuestion } from '../lib/api';

const TOPIC_LABEL: Record<string, string> = {
  python: 'Python', dsa: 'DSA', 'ml-basics': 'ML Basics',
  'system-design': 'System Design', quant: 'Quant', behavioral: 'PI / HR',
};

const TYPING_TEXT =
  'The quick brown fox jumps over the lazy dog. Consistent practice beats cramming before interviews.';

function QuestionCard({ q }: { q: PrepQuestion }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="card" style={{ marginBottom: 10 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', gap: 8, alignItems: 'flex-start' }}>
        <p style={{ fontWeight: 600, margin: 0, flex: 1 }}>{q.question}</p>
        <span className="tag">{q.level}</span>
      </div>
      <button className="btn small" style={{ marginTop: 8 }} onClick={() => setOpen(!open)}>
        {open ? 'Guidance chhupao' : 'Guidance dekho'}
      </button>
      {open && (
        <ul className="sugg">
          {q.guidance.map((g, i) => <li key={i}>{g}</li>)}
        </ul>
      )}
    </div>
  );
}

function TypingTest() {
  const [input, setInput] = useState('');
  const [start, setStart] = useState<number | null>(null);
  const [done, setDone] = useState(false);
  const boxRef = useRef<HTMLTextAreaElement>(null);

  const onChange = (v: string) => {
    if (done) return;
    if (start === null && v.length > 0) setStart(Date.now());
    const val = v.slice(0, TYPING_TEXT.length);
    setInput(val);
    if (val.length === TYPING_TEXT.length) setDone(true);
  };

  const reset = () => {
    setInput('');
    setStart(null);
    setDone(false);
    boxRef.current?.focus();
  };

  let wpm: number | null = null;
  let acc: number | null = null;
  if (done && start) {
    const mins = (Date.now() - start) / 60000;
    const correct = [...input].filter((c, i) => c === TYPING_TEXT[i]).length;
    wpm = Math.round(correct / 5 / mins);
    acc = Math.round((100 * correct) / TYPING_TEXT.length);
  }

  return (
    <div className="card">
      <h3 style={{ marginTop: 0 }}>Typing test</h3>
      <p className="muted" style={{ fontSize: 13, marginTop: 0 }}>Neeche wala text exactly type karo — WPM + accuracy milegi.</p>
      <p className="type-src">{TYPING_TEXT}</p>
      <textarea
        ref={boxRef}
        className="rinput"
        style={{ minHeight: 80, fontFamily: 'monospace' }}
        value={input}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Yahan type karo…"
      />
      <div style={{ display: 'flex', gap: 12, alignItems: 'center', marginTop: 8 }}>
        <button className="btn small" onClick={reset}>Reset</button>
        {done && wpm !== null && (
          <span><strong style={{ color: '#4ade80' }}>{wpm} WPM</strong> <span className="muted">· {acc}% accurate</span></span>
        )}
      </div>
    </div>
  );
}

function PiMock({ questions }: { questions: PrepQuestion[] }) {
  const [idx, setIdx] = useState(0);
  const [secs, setSecs] = useState(120);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    if (!running) return;
    if (secs <= 0) {
      setRunning(false);
      return;
    }
    const t = setTimeout(() => setSecs((s) => s - 1), 1000);
    return () => clearTimeout(t);
  }, [running, secs]);

  const next = () => {
    setIdx((i) => (i + 1) % Math.max(1, questions.length));
    setSecs(120);
    setRunning(false);
  };

  const q = questions[idx];
  const mm = String(Math.floor(secs / 60)).padStart(2, '0');
  const ss = String(secs % 60).padStart(2, '0');

  return (
    <div className="card">
      <h3 style={{ marginTop: 0 }}>PI mock — bolo, timer ke saath</h3>
      {q ? (
        <>
          <p style={{ fontWeight: 600, fontSize: 17 }}>{q.question}</p>
          <div className="timer" style={{ color: secs <= 30 ? '#f87171' : '#7dd3fc' }}>{mm}:{ss}</div>
          <div style={{ display: 'flex', gap: 8, marginTop: 10 }}>
            <button className="btn small primary" onClick={() => setRunning(!running)}>
              {running ? 'Pause' : 'Start 2-min'}
            </button>
            <button className="btn small" onClick={next}>Next question</button>
          </div>
          <p className="muted" style={{ fontSize: 13 }}>Zor se bolo — STAR format yaad rakho. Timer khatam hone tak ruko mat.</p>
        </>
      ) : (
        <p className="muted">PI questions load ho rahe hain…</p>
      )}
    </div>
  );
}

export default function Interview() {
  const [tab, setTab] = useState<'qs' | 'typing' | 'pi'>('qs');
  const [topics, setTopics] = useState<{ topic: string; count: number }[]>([]);
  const [topic, setTopic] = useState('python');
  const [qs, setQs] = useState<PrepQuestion[]>([]);
  const [piQs, setPiQs] = useState<PrepQuestion[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const t = await prepApi.topics();
        setTopics(t.topics);
        const pi = await prepApi.questions('behavioral', 10);
        setPiQs(pi.questions);
      } catch (err) {
        setError(err instanceof ApiError ? err.message : 'Load failed');
      }
    })();
  }, []);

  useEffect(() => {
    (async () => {
      try {
        const r = await prepApi.questions(topic, 10);
        setQs(r.questions);
      } catch (err) {
        setError(err instanceof ApiError ? err.message : 'Load failed');
      }
    })();
  }, [topic]);

  return (
    <div>
      <h1 className="page-title">Interview Prep</h1>
      <p className="page-sub">Tech + quant + PI — guidance ke saath practice karo.</p>
      {error && <p className="error">{error}</p>}

      <div className="lang-tabs">
        {(['qs', 'typing', 'pi'] as const).map((t) => (
          <button key={t} className={'lang-tab' + (tab === t ? ' active' : '')} onClick={() => setTab(t)}>
            {t === 'qs' ? 'Questions' : t === 'typing' ? 'Typing test' : 'PI mock'}
          </button>
        ))}
      </div>

      {tab === 'qs' && (
        <>
          <div className="lang-tabs" style={{ marginTop: 0 }}>
            {topics.map((t) => (
              <button
                key={t.topic}
                className={'lang-tab' + (topic === t.topic ? ' active' : '')}
                onClick={() => setTopic(t.topic)}
              >
                {TOPIC_LABEL[t.topic] || t.topic} ({t.count})
              </button>
            ))}
          </div>
          {qs.map((q) => <QuestionCard key={q.id} q={q} />)}
        </>
      )}
      {tab === 'typing' && <TypingTest />}
      {tab === 'pi' && <PiMock questions={piQs} />}

      <style>{`
        .lang-tabs { display: flex; gap: 8px; margin: 14px 0; flex-wrap: wrap; }
        .lang-tab { padding: 8px 16px; border-radius: 10px; border: 1px solid #232838; background: #141821; color: #c6cddb; cursor: pointer; }
        .lang-tab.active { border-color: #7dd3fc; color: #7dd3fc; }
        .tag { font-size: 12px; color: #8b93a7; border: 1px solid #232838; border-radius: 12px; padding: 2px 10px; white-space: nowrap; }
        .sugg { margin: 8px 0 0; padding-left: 20px; color: #c6cddb; font-size: 14px; }
        .sugg li { margin: 6px 0; }
        .rinput { width: 100%; box-sizing: border-box; background: #0d1117; color: #e6e9f0; border: 1px solid #232838; border-radius: 8px; padding: 10px 12px; font-size: 14px; }
        .type-src { background: #0d1117; border: 1px solid #232838; border-radius: 8px; padding: 12px; font-family: monospace; font-size: 14px; color: #8b93a7; }
        .timer { font-size: 40px; font-weight: 800; font-family: monospace; }
      `}</style>
    </div>
  );
}
