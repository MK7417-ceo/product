import { useEffect, useState } from 'react';
import { api } from '../lib/api';
import { useLang } from '../lib/i18n';
import './PlacementPrep.css';

/* ---------- types ---------- */
interface GDTopic {
  id: string;
  topic: string;
  category: string;
  difficulty: number;
  points_for: string[];
  points_against: string[];
  tips: string;
}

interface InterviewQA {
  id: string;
  category: 'hr' | 'technical';
  subcategory: string;
  question: string;
  answer: string;
  tip?: string;
  key_point?: string;
  difficulty: number;
  companies: string[];
}

interface QuantType {
  type_id: string;
  name: string;
  section: string;
  trick_title: string;
  trick: string;
  trick_example: string;
  question_count: number;
}

interface QuantQ {
  id: string;
  prompt: string;
  options: string[];
  answer: number;
  solution: string;
  trick_used: string;
  difficulty: number;
}

type Tab = 'gd' | 'interview' | 'quant' | 'company' | 'random';

export default function PlacementPrep() {
  const { t } = useLang();
  const [tab, setTab] = useState<Tab>('gd');

  return (
    <div className="placement-prep">
      <header className="pp-header">
        <h1>🎯 {t('pp.title', 'Placement Prep')}</h1>
        <p className="pp-subtitle">
          {t('pp.subtitle', 'Everything companies ask — GD, interviews, aptitude, company-wise')}
        </p>
      </header>

      <nav className="pp-tabs" role="tablist">
        {(
          [
            ['gd', '💬', 'pp.tabGD', 'GD Topics'],
            ['interview', '🎤', 'pp.tabInterview', 'Interview Q&A'],
            ['quant', '🔢', 'pp.tabQuant', 'Aptitude'],
            ['company', '🏢', 'pp.tabCompany', 'Company-wise'],
            ['random', '🎲', 'pp.tabRandom', 'Random Practice'],
          ] as [Tab, string, string, string][]
        ).map(([id, icon, key, fallback]) => (
          <button
            key={id}
            role="tab"
            aria-selected={tab === id}
            className={`pp-tab${tab === id ? ' pp-tab-active' : ''}`}
            onClick={() => setTab(id)}
          >
            {icon} {t(key, fallback)}
          </button>
        ))}
      </nav>

      <div className="pp-content">
        {tab === 'gd' && <GDTab />}
        {tab === 'interview' && <InterviewTab />}
        {tab === 'quant' && <QuantTab />}
        {tab === 'company' && <CompanyTab />}
        {tab === 'random' && <RandomTab />}
      </div>
    </div>
  );
}

/* ---------- GD TAB ---------- */
function GDTab() {
  const { t } = useLang();
  const [topics, setTopics] = useState<GDTopic[]>([]);
  const [category, setCategory] = useState('');
  const [open, setOpen] = useState<string | null>(null);

  useEffect(() => {
    api<{ topics: GDTopic[] }>(
      `/api/v1/placement/gd-topics${category ? `?category=${category}` : ''}`
    )
      .then((r) => setTopics(r.topics))
      .catch(() => setTopics([]));
  }, [category]);

  return (
    <div>
      <div className="pp-filters">
        {['', 'tech', 'social', 'abstract'].map((c) => (
          <button
            key={c}
            className={`pp-chip${category === c ? ' pp-chip-active' : ''}`}
            onClick={() => setCategory(c)}
          >
            {c === '' ? t('pp.all', 'All') : c}
          </button>
        ))}
      </div>
      <div className="pp-list">
        {topics.map((topic) => (
          <div key={topic.id} className="pp-card">
            <button
              className="pp-card-head"
              onClick={() => setOpen(open === topic.id ? null : topic.id)}
              aria-expanded={open === topic.id}
            >
              <span className="pp-card-title">{topic.topic}</span>
              <span className="pp-badges">
                <span className="pp-badge">{topic.category}</span>
                <span className="pp-badge">★{topic.difficulty}</span>
                <span className="pp-expand">{open === topic.id ? '▾' : '▸'}</span>
              </span>
            </button>
            {open === topic.id && (
              <div className="pp-card-body">
                <div className="pp-cols">
                  <div>
                    <h4>✅ {t('pp.forPoints', 'Points FOR')}</h4>
                    <ul>
                      {topic.points_for.map((p, i) => (
                        <li key={i}>{p}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4>❌ {t('pp.againstPoints', 'Points AGAINST')}</h4>
                    <ul>
                      {topic.points_against.map((p, i) => (
                        <li key={i}>{p}</li>
                      ))}
                    </ul>
                  </div>
                </div>
                <div className="pp-tip">💡 {topic.tips}</div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

/* ---------- INTERVIEW TAB ---------- */
function InterviewTab() {
  const { t } = useLang();
  const [items, setItems] = useState<InterviewQA[]>([]);
  const [category, setCategory] = useState('');
  const [search, setSearch] = useState('');
  const [open, setOpen] = useState<string | null>(null);

  useEffect(() => {
    api<{ items: InterviewQA[] }>(
      `/api/v1/placement/interview-qa${category ? `?category=${category}` : ''}`
    )
      .then((r) => setItems(r.items))
      .catch(() => setItems([]));
  }, [category]);

  const filtered = search
    ? items.filter((q) =>
        (q.question + q.answer).toLowerCase().includes(search.toLowerCase())
      )
    : items;

  return (
    <div>
      <div className="pp-filters">
        <input
          className="pp-search"
          placeholder={t('pp.search', 'Search questions…')}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        {['', 'hr', 'technical'].map((c) => (
          <button
            key={c}
            className={`pp-chip${category === c ? ' pp-chip-active' : ''}`}
            onClick={() => setCategory(c)}
          >
            {c === '' ? t('pp.all', 'All') : c === 'hr' ? 'HR' : t('pp.technical', 'Technical')}
          </button>
        ))}
      </div>
      <div className="pp-count">
        {filtered.length} {t('pp.questions', 'questions')}
      </div>
      <div className="pp-list">
        {filtered.map((q) => (
          <div key={q.id} className="pp-card">
            <button
              className="pp-card-head"
              onClick={() => setOpen(open === q.id ? null : q.id)}
              aria-expanded={open === q.id}
            >
              <span className="pp-card-title">{q.question}</span>
              <span className="pp-badges">
                <span className={`pp-badge pp-badge-${q.category}`}>{q.category}</span>
                <span className="pp-expand">{open === q.id ? '▾' : '▸'}</span>
              </span>
            </button>
            {open === q.id && (
              <div className="pp-card-body">
                <p className="pp-answer">{q.answer}</p>
                {(q.tip || q.key_point) && (
                  <div className="pp-tip">💡 {q.tip || q.key_point}</div>
                )}
                {q.companies.length > 0 && (
                  <div className="pp-companies">
                    🏢 {q.companies.join(', ')}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

/* ---------- QUANT TAB ---------- */
function QuantTab() {
  const { t } = useLang();
  const [types, setTypes] = useState<QuantType[]>([]);
  const [typeId, setTypeId] = useState('');
  const [questions, setQuestions] = useState<QuantQ[]>([]);
  const [trick, setTrick] = useState<QuantType | null>(null);
  const [revealed, setRevealed] = useState<Record<string, boolean>>({});
  const [picked, setPicked] = useState<Record<string, number>>({});

  useEffect(() => {
    api<{ types: QuantType[] }>('/api/v1/placement/quant/types')
      .then((r) => setTypes(r.types))
      .catch(() => setTypes([]));
  }, []);

  useEffect(() => {
    if (!typeId) {
      setQuestions([]);
      setTrick(null);
      return;
    }
    api<{ questions: QuantQ[]; trick: QuantType | null }>(
      `/api/v1/placement/quant?type_id=${typeId}`
    )
      .then((r) => {
        setQuestions(r.questions);
        setTrick(r.trick);
        setRevealed({});
        setPicked({});
      })
      .catch(() => setQuestions([]));
  }, [typeId]);

  const sections = [...new Set(types.map((x) => x.section))];

  return (
    <div>
      {sections.map((sec) => (
        <div key={sec} className="pp-section">
          <h3 className="pp-section-title">{sec}</h3>
          <div className="pp-chips">
            {types
              .filter((x) => x.section === sec)
              .map((x) => (
                <button
                  key={x.type_id}
                  className={`pp-chip${typeId === x.type_id ? ' pp-chip-active' : ''}`}
                  onClick={() => setTypeId(x.type_id)}
                >
                  {x.name}
                </button>
              ))}
          </div>
        </div>
      ))}

      {trick && (
        <div className="pp-trick">
          <h4>⚡ {trick.trick_title}</h4>
          <p>{trick.trick}</p>
          <p className="pp-trick-ex">
            <em>{trick.trick_example}</em>
          </p>
        </div>
      )}

      <div className="pp-list">
        {questions.map((q, qi) => (
          <div key={q.id} className="pp-card">
            <div className="pp-q-prompt">
              <strong>Q{qi + 1}.</strong> {q.prompt}
            </div>
            <div className="pp-options">
              {q.options.map((opt, oi) => {
                const isAnswer = revealed[q.id] && oi === q.answer;
                const isWrong =
                  revealed[q.id] && picked[q.id] === oi && oi !== q.answer;
                return (
                  <button
                    key={oi}
                    className={`pp-option${isAnswer ? ' pp-opt-correct' : ''}${
                      isWrong ? ' pp-opt-wrong' : ''
                    }`}
                    disabled={revealed[q.id]}
                    onClick={() => {
                      setPicked({ ...picked, [q.id]: oi });
                      setRevealed({ ...revealed, [q.id]: true });
                    }}
                  >
                    {String.fromCharCode(65 + oi)}. {opt}
                  </button>
                );
              })}
            </div>
            {revealed[q.id] && (
              <div className="pp-solution">
                <div>
                  {picked[q.id] === q.answer ? '✅ ' : '❌ '}
                  {t('pp.solution', 'Solution')}: {q.solution}
                </div>
                <div className="pp-tip">
                  ⚡ {t('pp.trickUsed', 'Trick')}: {q.trick_used}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

/* ---------- COMPANY TAB ---------- */
const POPULAR_COMPANIES = [
  'tcs', 'infosys', 'wipro', 'amazon', 'google', 'microsoft',
  'flipkart', 'accenture', 'cognizant', 'hcl', 'swiggy', 'zoho',
];

function CompanyTab() {
  const { t } = useLang();
  const [company, setCompany] = useState('tcs');
  const [items, setItems] = useState<InterviewQA[]>([]);
  const [open, setOpen] = useState<string | null>(null);

  useEffect(() => {
    api<{ items: InterviewQA[] }>(
      `/api/v1/placement/interview-qa?company=${company}`
    )
      .then((r) => setItems(r.items))
      .catch(() => setItems([]));
  }, [company]);

  return (
    <div>
      <p className="pp-hint">
        🏢 {t('pp.companyHint', 'Pick a company — see what they actually ask')}
      </p>
      <div className="pp-chips">
        {POPULAR_COMPANIES.map((c) => (
          <button
            key={c}
            className={`pp-chip${company === c ? ' pp-chip-active' : ''}`}
            onClick={() => setCompany(c)}
          >
            {c.toUpperCase()}
          </button>
        ))}
      </div>
      <div className="pp-count">
        {items.length} {t('pp.questions', 'questions')} @ {company.toUpperCase()}
      </div>
      <div className="pp-list">
        {items.map((q) => (
          <div key={q.id} className="pp-card">
            <button
              className="pp-card-head"
              onClick={() => setOpen(open === q.id ? null : q.id)}
              aria-expanded={open === q.id}
            >
              <span className="pp-card-title">{q.question}</span>
              <span className="pp-badges">
                <span className={`pp-badge pp-badge-${q.category}`}>{q.category}</span>
                <span className="pp-expand">{open === q.id ? '▾' : '▸'}</span>
              </span>
            </button>
            {open === q.id && (
              <div className="pp-card-body">
                <p className="pp-answer">{q.answer}</p>
                {(q.tip || q.key_point) && (
                  <div className="pp-tip">💡 {q.tip || q.key_point}</div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

/* ---------- RANDOM PRACTICE TAB ---------- */
function RandomTab() {
  const { t } = useLang();
  const [items, setItems] = useState<InterviewQA[]>([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState<Record<string, boolean>>({});
  const [count, setCount] = useState(5);

  const draw = async () => {
    setLoading(true);
    try {
      const r = await api<{ items: InterviewQA[] }>(
        `/api/v1/placement/interview-qa/random?count=${count}`
      );
      setItems(r.items);
      setOpen({});
    } catch {
      setItems([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="pp-random-controls">
        <label>
          {t('pp.howMany', 'How many?')}{' '}
          <select value={count} onChange={(e) => setCount(Number(e.target.value))}>
            {[4, 5, 6].map((n) => (
              <option key={n} value={n}>
                {n}
              </option>
            ))}
          </select>
        </label>
        <button className="pp-draw-btn" onClick={draw} disabled={loading}>
          🎲 {loading ? '…' : t('pp.draw', 'Draw random questions')}
        </button>
      </div>
      <p className="pp-hint">
        {t(
          'pp.randomHint',
          'Answer out loud first, then tap to reveal the model answer.'
        )}
      </p>
      <div className="pp-list">
        {items.map((q, i) => (
          <div key={q.id + i} className="pp-card">
            <button
              className="pp-card-head"
              onClick={() => setOpen({ ...open, [q.id + i]: !open[q.id + i] })}
            >
              <span className="pp-card-title">
                <strong>Q{i + 1}.</strong> {q.question}
              </span>
              <span className="pp-badges">
                <span className={`pp-badge pp-badge-${q.category}`}>{q.category}</span>
                <span className="pp-expand">{open[q.id + i] ? '▾' : '▸'}</span>
              </span>
            </button>
            {open[q.id + i] && (
              <div className="pp-card-body">
                <p className="pp-answer">{q.answer}</p>
                {(q.tip || q.key_point) && (
                  <div className="pp-tip">💡 {q.tip || q.key_point}</div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
