import { useEffect, useRef, useState } from 'react';
import { prepApi, ApiError, type PrepQuestion } from '../lib/p1api';
import './p1-pages.css';

const TOPIC_LABEL: Record<string, string> = {
  python: 'Python', dsa: 'DSA', 'ml-basics': 'ML Basics',
  'system-design': 'System Design', quant: 'Quant', behavioral: 'PI / HR',
};

const TYPING_TEXT =
  'The quick brown fox jumps over the lazy dog. Consistent practice beats cramming before interviews.';

function QuestionCard({ q }: { q: PrepQuestion }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="p1x-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', gap: 8, alignItems: 'flex-start' }}>
        <p style={{ fontWeight: 600, margin: 0, flex: 1, fontSize: 15 }}>{q.question}</p>
        <span className="p1x-pill claim">{q.level.toUpperCase()}</span>
      </div>
      <button className="p1x-btn ghost sm" style={{ marginTop: 10 }} onClick={() => setOpen(!open)}>
        {open ? 'Guidance chhupao' : 'Guidance dekho'}
      </button>
      {open && (
        <ul style={{ margin: '10px 0 0', paddingLeft: 20, color: 'var(--muted)', fontSize: 14 }}>
          {q.guidance.map((g, i) => (
            <li key={i} style={{ margin: '6px 0' }}>{g}</li>
          ))}
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
    wpm = mins > 0 ? Math.round(correct / 5 / mins) : 0;
    acc = Math.round((100 * correct) / TYPING_TEXT.length);
  }

  return (
    <div className="p1x-card">
      <h2>Typing test</h2>
      <p className="hint">Neeche wala text exactly type karo — WPM + accuracy milegi.</p>
      <p className="p1x-type-src">{TYPING_TEXT}</p>
      <div className="p1x-field" style={{ marginTop: 10 }}>
        <textarea
          ref={boxRef}
          style={{ minHeight: 90, fontFamily: 'Consolas,monospace' }}
          value={input}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Yahan type karo…"
        />
      </div>
      <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
        <button className="p1x-btn ghost sm" onClick={reset}>Reset</button>
        {done && wpm !== null && (
          <span>
            <strong style={{ color: 'var(--green)' }}>{wpm} WPM</strong>{' '}
            <span className="p1x-muted">· {acc}% accurate</span>
          </span>
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
    <div className="p1x-card">
      <h2>PI mock — bolo, timer ke saath</h2>
      {q ? (
        <>
          <p style={{ fontWeight: 600, fontSize: 17 }}>{q.question}</p>
          <div className="p1x-timer" style={{ color: secs <= 30 ? 'var(--red)' : 'var(--cyan)' }}>
            {mm}:{ss}
          </div>
          <div style={{ display: 'flex', gap: 8, marginTop: 10 }}>
            <button className="p1x-btn sm" onClick={() => setRunning(!running)}>
              {running ? 'Pause' : 'Start 2-min'}
            </button>
            <button className="p1x-btn ghost sm" onClick={next}>Next question</button>
          </div>
          <p className="p1x-muted" style={{ fontSize: 13, marginTop: 10 }}>
            Zor se bolo — STAR format yaad rakho. Timer khatam hone tak ruko mat.
          </p>
        </>
      ) : (
        <p className="p1x-empty">PI questions load ho rahe hain…</p>
      )}
    </div>
  );
}

export default function InterviewPrep() {
  const [tab, setTab] = useState<'qs' | 'typing' | 'pi'>('qs');
  const [topics, setTopics] = useState<{ topic: string; count: number }[]>([]);
  const [topic, setTopic] = useState('python');
  const [qs, setQs] = useState<PrepQuestion[]>([]);
  const [piQs, setPiQs] = useState<PrepQuestion[]>([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const t = await prepApi.topics();
        setTopics(t.topics);
        if (t.topics.length > 0 && !t.topics.some((x) => x.topic === topic)) {
          setTopic(t.topics[0].topic);
        }
        const pi = await prepApi.questions('behavioral', 10);
        setPiQs(pi.questions);
      } catch (err) {
        setError(err instanceof ApiError ? err.message : 'Load failed');
      } finally {
        setLoading(false);
      }
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
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

  if (loading)
    return (
      <div className="p1x">
        <p className="p1x-loading">Loading interview prep…</p>
      </div>
    );

  return (
    <div className="p1x">
      <div className="p1x-head">
        <div>
          <h1 className="p1x-title">Interview Prep</h1>
          <p className="p1x-sub">Tech + quant + PI — guidance ke saath practice karo.</p>
        </div>
      </div>
      {error && <div className="p1x-err">{error}</div>}

      <div className="p1x-tabs">
        {(['qs', 'typing', 'pi'] as const).map((t) => (
          <button key={t} className={`p1x-tab ${tab === t ? 'active' : ''}`} onClick={() => setTab(t)}>
            {t === 'qs' ? '❓ Questions' : t === 'typing' ? '⌨ Typing test' : '🎤 PI mock'}
          </button>
        ))}
      </div>

      {tab === 'qs' && (
        <>
          <div className="p1x-tabs" style={{ marginTop: 0 }}>
            {topics.map((t) => (
              <button
                key={t.topic}
                className={`p1x-tab ${topic === t.topic ? 'active' : ''}`}
                onClick={() => setTopic(t.topic)}
              >
                {TOPIC_LABEL[t.topic] || t.topic} ({t.count})
              </button>
            ))}
          </div>
          {qs.length === 0 && <p className="p1x-empty">Is topic ke liye questions nahi mile.</p>}
          {qs.map((q) => (
            <QuestionCard key={q.id} q={q} />
          ))}
        </>
      )}
      {tab === 'typing' && <TypingTest />}
      {tab === 'pi' && <PiMock questions={piQs} />}
    </div>
  );
}
