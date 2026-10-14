import { useCallback, useEffect, useMemo, useState } from 'react';
import { api, ApiError } from '../../lib/api';
import { useAuth } from '../../lib/auth';
import './ContentManager.css';

/* ------------------------------------------------------------------ */
/* Types (mirror the /api/v1/content/* contract)                       */
/* ------------------------------------------------------------------ */

interface Topic {
  slug: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  active: boolean;
  question_count: number;
  theory_count: number;
}

interface TheoryBlock {
  id: string;
  topic_slug: string;
  title: string;
  level: string;
  body_md: string;
  order: number;
}

type QuestionType = 'mcq' | 'coding' | 'written';

interface Question {
  id: string;
  topic_slug: string;
  type: QuestionType;
  level: string;
  skill: string;
  prompt: string;
  choices?: string[];
  answer_index?: number;
  rubric?: Record<string, unknown>;
}

interface ImportResult {
  title: string;
  description: string;
  headings: string[];
  body_md: string;
  source_url: string;
}

const LEVELS = ['beginner', 'intermediate', 'advanced', 'expert'] as const;
const Q_TYPES: QuestionType[] = ['mcq', 'coding', 'written'];

const contentApi = {
  listTopics: () => api<Topic[]>('/api/v1/content/topics'),
  createTopic: (b: Omit<Topic, 'question_count' | 'theory_count'>) =>
    api<Topic>('/api/v1/content/topics', { method: 'POST', body: JSON.stringify(b) }),
  toggleTopic: (slug: string, active: boolean) =>
    api<Topic>(`/api/v1/content/topics/${slug}`, { method: 'PATCH', body: JSON.stringify({ active }) }),
  listTheory: (slug: string) => api<TheoryBlock[]>(`/api/v1/content/topics/${slug}/theory`),
  saveTheory: (slug: string, b: Partial<TheoryBlock> & { title: string; level: string; body_md: string }) =>
    b.id
      ? api<TheoryBlock>(`/api/v1/content/theory/${b.id}`, { method: 'PATCH', body: JSON.stringify(b) })
      : api<TheoryBlock>(`/api/v1/content/topics/${slug}/theory`, { method: 'POST', body: JSON.stringify(b) }),
  deleteTheory: (id: string) => api<void>(`/api/v1/content/theory/${id}`, { method: 'DELETE' }),
  listQuestions: (slug: string) => api<Question[]>(`/api/v1/content/topics/${slug}/questions`),
  createQuestion: (slug: string, b: Omit<Question, 'id' | 'topic_slug'>) =>
    api<Question>(`/api/v1/content/topics/${slug}/questions`, { method: 'POST', body: JSON.stringify(b) }),
  deleteQuestion: (id: string) => api<void>(`/api/v1/content/questions/${id}`, { method: 'DELETE' }),
  importLink: (url: string) =>
    api<ImportResult>('/api/v1/content/import-link', { method: 'POST', body: JSON.stringify({ url }) }),
};

function slugify(name: string): string {
  return name
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/[\s_]+/g, '-')
    .replace(/-+/g, '-');
}

function errMsg(err: unknown): string {
  return err instanceof ApiError ? err.message : 'Request failed';
}

/* ------------------------------------------------------------------ */
/* Main component                                                      */
/* ------------------------------------------------------------------ */

export default function ContentManager() {
  const { user, loading: authLoading } = useAuth();
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selected, setSelected] = useState<Topic | null>(null);
  const [tab, setTab] = useState<'theory' | 'questions' | 'import'>('theory');

  const load = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      setTopics(await contentApi.listTopics());
    } catch (e) {
      setError(errMsg(e));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (user?.role === 'admin') load();
  }, [user, load]);

  const toggle = async (t: Topic) => {
    try {
      const updated = await contentApi.toggleTopic(t.slug, !t.active);
      setTopics((ts) => ts.map((x) => (x.slug === t.slug ? updated : x)));
      if (selected?.slug === t.slug) setSelected(updated);
    } catch (e) {
      setError(errMsg(e));
    }
  };

  if (authLoading) return <div className="cm-wrap"><p className="cm-muted">Loading…</p></div>;
  if (user?.role !== 'admin') {
    return (
      <div className="cm-wrap">
        <div className="cm-denied">
          <h2>⛔ Access denied</h2>
          <p>This area is for administrators only.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="cm-wrap">
      <header className="cm-head">
        <div>
          <h1>📚 Content Manager</h1>
          <p className="cm-muted">Topics, theory, questions & link importer — admin only.</p>
        </div>
      </header>
      {error && <div className="cm-error" role="alert">{error}</div>}
      {loading ? (
        <p className="cm-muted">Loading topics…</p>
      ) : (
        <div className="cm-grid">
          <section className="cm-panel">
            <TopicList
              topics={topics}
              selected={selected}
              onSelect={(t) => { setSelected(t); setTab('theory'); }}
              onToggle={toggle}
              onCreated={(t) => setTopics((ts) => [...ts, t])}
            />
          </section>
          <section className="cm-panel">
            {selected ? (
              <TopicDetail topic={selected} tab={tab} setTab={setTab} />
            ) : (
              <p className="cm-muted">Select a topic to manage its theory and questions.</p>
            )}
          </section>
        </div>
      )}
    </div>
  );
}


/* ---------------- Topic list + add form ---------------- */

function TopicList({ topics, selected, onSelect, onToggle, onCreated }: {
  topics: Topic[];
  selected: Topic | null;
  onSelect: (t: Topic) => void;
  onToggle: (t: Topic) => void;
  onCreated: (t: Topic) => void;
}) {
  const [open, setOpen] = useState(false);
  const [name, setName] = useState('');
  const [slug, setSlug] = useState('');
  const [slugTouched, setSlugTouched] = useState(false);
  const [description, setDescription] = useState('');
  const [icon, setIcon] = useState('📘');
  const [color, setColor] = useState('#8b5cf6');
  const [active, setActive] = useState(true);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');

  const onName = (v: string) => {
    setName(v);
    if (!slugTouched) setSlug(slugify(v));
  };

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !slug.trim() || busy) return;
    setBusy(true);
    setErr('');
    try {
      const t = await contentApi.createTopic({
        slug: slug.trim(), name: name.trim(), description: description.trim(),
        icon: icon.trim() || '📘', color, active,
      });
      onCreated(t);
      setOpen(false);
      setName(''); setSlug(''); setSlugTouched(false); setDescription('');
    } catch (e2) {
      setErr(errMsg(e2));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div>
      <div className="cm-row">
        <h2>Topics ({topics.length})</h2>
        <button className="cm-btn" onClick={() => setOpen((o) => !o)}>{open ? 'Cancel' : '+ New Topic'}</button>
      </div>
      {open && (
        <form className="cm-form" onSubmit={submit}>
          {err && <div className="cm-error">{err}</div>}
          <label>Name
            <input value={name} onChange={(e) => onName(e.target.value)} placeholder="Python" required />
          </label>
          <label>Slug (auto)
            <input value={slug} onChange={(e) => { setSlug(slugify(e.target.value)); setSlugTouched(true); }} placeholder="python" required />
          </label>
          <label>Description
            <textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={2} placeholder="Short blurb…" />
          </label>
          <div className="cm-row2">
            <label>Icon <input value={icon} onChange={(e) => setIcon(e.target.value)} maxLength={4} /></label>
            <label>Color <input type="color" value={color} onChange={(e) => setColor(e.target.value)} /></label>
            <label className="cm-check"><input type="checkbox" checked={active} onChange={(e) => setActive(e.target.checked)} /> Active</label>
          </div>
          <button className="cm-btn primary" disabled={busy}>{busy ? 'Saving…' : 'Create Topic'}</button>
        </form>
      )}
      <div className="cm-topics">
        {topics.map((t) => (
          <button
            key={t.slug}
            className={`cm-topic ${selected?.slug === t.slug ? 'sel' : ''} ${t.active ? '' : 'off'}`}
            onClick={() => onSelect(t)}
          >
            <span className="cm-topic-icon" style={{ background: `${t.color}22`, borderColor: t.color }}>{t.icon}</span>
            <span className="cm-topic-main">
              <strong>{t.name}</strong>
              <small className="cm-muted">/{t.slug} · {t.question_count} Q · {t.theory_count} theory</small>
            </span>
            <span
              role="switch"
              aria-checked={t.active}
              tabIndex={0}
              title={t.active ? 'Deactivate' : 'Activate'}
              className={`cm-switch ${t.active ? 'on' : ''}`}
              onClick={(e) => { e.stopPropagation(); onToggle(t); }}
              onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); e.stopPropagation(); onToggle(t); } }}
            />
          </button>
        ))}
        {topics.length === 0 && <p className="cm-muted">No topics yet — create the first one.</p>}
      </div>
    </div>
  );
}

/* ---------------- Topic detail: Theory / Questions / Import tabs ---------------- */

function TopicDetail({ topic, tab, setTab }: {
  topic: Topic;
  tab: 'theory' | 'questions' | 'import';
  setTab: (t: 'theory' | 'questions' | 'import') => void;
}) {
  return (
    <div>
      <div className="cm-row">
        <h2>{topic.icon} {topic.name}</h2>
        <span className="cm-muted">/{topic.slug}</span>
      </div>
      <div className="cm-tabs" role="tablist">
        {(['theory', 'questions', 'import'] as const).map((k) => (
          <button key={k} role="tab" aria-selected={tab === k}
            className={`cm-tab ${tab === k ? 'sel' : ''}`} onClick={() => setTab(k)}>
            {k === 'theory' ? '📖 Theory' : k === 'questions' ? '❓ Questions' : '🔗 Import from Link'}
          </button>
        ))}
      </div>
      {tab === 'theory' && <TheoryTab topic={topic} />}
      {tab === 'questions' && <QuestionsTab topic={topic} />}
      {tab === 'import' && <ImportTab topic={topic} />}
    </div>
  );
}

/* ---------------- Theory ---------------- */

function TheoryTab({ topic }: { topic: Topic }) {
  const [items, setItems] = useState<TheoryBlock[]>([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState('');
  const [editing, setEditing] = useState<Partial<TheoryBlock> | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setErr('');
    try {
      const list = await contentApi.listTheory(topic.slug);
      setItems([...list].sort((a, b) => a.order - b.order || a.title.localeCompare(b.title)));
    } catch (e) { setErr(errMsg(e)); } finally { setLoading(false); }
  }, [topic.slug]);

  useEffect(() => { load(); }, [load]);

  const remove = async (id: string) => {
    if (!window.confirm('Delete this theory block?')) return;
    try {
      await contentApi.deleteTheory(id);
      setItems((xs) => xs.filter((x) => x.id !== id));
    } catch (e) { setErr(errMsg(e)); }
  };

  const grouped = useMemo(() => {
    const g = new Map<string, TheoryBlock[]>();
    for (const it of items) {
      const k = it.level;
      if (!g.has(k)) g.set(k, []);
      g.get(k)!.push(it);
    }
    return [...g.entries()].sort((a, b) => LEVELS.indexOf(a[0] as never) - LEVELS.indexOf(b[0] as never));
  }, [items]);

  return (
    <div>
      <div className="cm-row">
        <h3>Theory blocks ({items.length})</h3>
        <button className="cm-btn" onClick={() => setEditing({ title: '', level: 'beginner', body_md: '', order: items.length })}>+ Add</button>
      </div>
      {err && <div className="cm-error">{err}</div>}
      {editing && (
        <TheoryForm
          initial={editing}
          onCancel={() => setEditing(null)}
          onSaved={(saved) => {
            setItems((xs) => {
              const rest = xs.filter((x) => x.id !== saved.id);
              return [...rest, saved].sort((a, b) => a.order - b.order);
            });
            setEditing(null);
          }}
          topicSlug={topic.slug}
        />
      )}
      {loading ? <p className="cm-muted">Loading…</p> : grouped.map(([level, blocks]) => (
        <div key={level} className="cm-group">
          <h4 className="cm-level">{level}</h4>
          {blocks.map((b) => (
            <div key={b.id} className="cm-card">
              <div className="cm-row">
                <strong>#{b.order} — {b.title}</strong>
                <span>
                  <button className="cm-mini" onClick={() => setEditing(b)}>Edit</button>{' '}
                  <button className="cm-mini danger" onClick={() => remove(b.id)}>Delete</button>
                </span>
              </div>
              <p className="cm-muted cm-preview">{b.body_md.slice(0, 160)}{b.body_md.length > 160 ? '…' : ''}</p>
            </div>
          ))}
        </div>
      ))}
      {!loading && items.length === 0 && <p className="cm-muted">No theory yet.</p>}
    </div>
  );
}

function TheoryForm({ initial, topicSlug, onCancel, onSaved }: {
  initial: Partial<TheoryBlock>;
  topicSlug: string;
  onCancel: () => void;
  onSaved: (t: TheoryBlock) => void;
}) {
  const [title, setTitle] = useState(initial.title ?? '');
  const [level, setLevel] = useState(initial.level ?? 'beginner');
  const [body, setBody] = useState(initial.body_md ?? '');
  const [order, setOrder] = useState(initial.order ?? 0);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !body.trim() || busy) return;
    setBusy(true); setErr('');
    try {
      const saved = await contentApi.saveTheory(topicSlug, {
        ...initial, title: title.trim(), level, body_md: body, order: Number(order) || 0,
      });
      onSaved(saved);
    } catch (e2) { setErr(errMsg(e2)); } finally { setBusy(false); }
  };

  return (
    <form className="cm-form cm-card" onSubmit={submit}>
      <h4>{initial.id ? 'Edit theory' : 'New theory block'}</h4>
      {err && <div className="cm-error">{err}</div>}
      <label>Title <input value={title} onChange={(e) => setTitle(e.target.value)} required /></label>
      <div className="cm-row2">
        <label>Level
          <select value={level} onChange={(e) => setLevel(e.target.value)}>
            {LEVELS.map((l) => <option key={l} value={l}>{l}</option>)}
          </select>
        </label>
        <label>Order <input type="number" value={order} onChange={(e) => setOrder(Number(e.target.value))} min={0} /></label>
      </div>
      <label>Body (markdown)
        <textarea value={body} onChange={(e) => setBody(e.target.value)} rows={8}
          placeholder="# Heading&#10;&#10;Explain the concept…" required />
      </label>
      <div className="cm-row">
        <button type="button" className="cm-btn" onClick={onCancel}>Cancel</button>
        <button className="cm-btn primary" disabled={busy}>{busy ? 'Saving…' : 'Save'}</button>
      </div>
    </form>
  );
}

/* ---------------- Questions ---------------- */

function QuestionsTab({ topic }: { topic: Topic }) {
  const [items, setItems] = useState<Question[]>([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState('');
  const [open, setOpen] = useState(false);
  const [typeFilter, setTypeFilter] = useState<'all' | QuestionType>('all');
  const [levelFilter, setLevelFilter] = useState('all');

  const load = useCallback(async () => {
    setLoading(true); setErr('');
    try { setItems(await contentApi.listQuestions(topic.slug)); }
    catch (e) { setErr(errMsg(e)); } finally { setLoading(false); }
  }, [topic.slug]);

  useEffect(() => { load(); }, [load]);

  const remove = async (id: string) => {
    if (!window.confirm('Delete this question?')) return;
    try {
      await contentApi.deleteQuestion(id);
      setItems((xs) => xs.filter((x) => x.id !== id));
    } catch (e) { setErr(errMsg(e)); }
  };

  const filtered = items.filter(
    (q) => (typeFilter === 'all' || q.type === typeFilter) && (levelFilter === 'all' || q.level === levelFilter),
  );

  return (
    <div>
      <div className="cm-row">
        <h3>Questions ({items.length})</h3>
        <button className="cm-btn" onClick={() => setOpen((o) => !o)}>{open ? 'Cancel' : '+ Add'}</button>
      </div>
      <div className="cm-row cm-filters">
        <label>Type
          <select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value as never)}>
            <option value="all">all</option>{Q_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
          </select>
        </label>
        <label>Level
          <select value={levelFilter} onChange={(e) => setLevelFilter(e.target.value)}>
            <option value="all">all</option>{LEVELS.map((l) => <option key={l} value={l}>{l}</option>)}
          </select>
        </label>
      </div>
      {err && <div className="cm-error">{err}</div>}
      {open && <QuestionForm topicSlug={topic.slug} onCancel={() => setOpen(false)} onSaved={(q) => { setItems((xs) => [...xs, q]); setOpen(false); }} />}
      {loading ? <p className="cm-muted">Loading…</p> : filtered.map((q) => (
        <div key={q.id} className="cm-card">
          <div className="cm-row">
            <span>
              <span className={`cm-pill ${q.type}`}>{q.type}</span>{' '}
              <span className="cm-pill lvl">{q.level}</span>{' '}
              <small className="cm-muted">#{q.skill}</small>
            </span>
            <button className="cm-mini danger" onClick={() => remove(q.id)}>Delete</button>
          </div>
          <p className="cm-qprompt">{q.prompt}</p>
          {q.type === 'mcq' && q.choices && (
            <ol className="cm-choices">
              {q.choices.map((c, i) => (
                <li key={i} className={i === q.answer_index ? 'cm-correct' : ''}>{c}{i === q.answer_index ? ' ✓' : ''}</li>
              ))}
            </ol>
          )}
          {q.type === 'written' && q.rubric && (
            <details><summary>Rubric JSON</summary><pre className="cm-pre">{JSON.stringify(q.rubric, null, 2)}</pre></details>
          )}
        </div>
      ))}
      {!loading && filtered.length === 0 && <p className="cm-muted">No questions match.</p>}
    </div>
  );
}

function QuestionForm({ topicSlug, onCancel, onSaved }: {
  topicSlug: string;
  onCancel: () => void;
  onSaved: (q: Question) => void;
}) {
  const [type, setType] = useState<QuestionType>('mcq');
  const [level, setLevel] = useState('beginner');
  const [skill, setSkill] = useState('');
  const [prompt, setPrompt] = useState('');
  const [choices, setChoices] = useState(['', '', '', '']);
  const [answerIndex, setAnswerIndex] = useState(0);
  const [rubric, setRubric] = useState('{\n  "key_concepts": []\n}');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');

  const setChoice = (i: number, v: string) =>
    setChoices((cs) => cs.map((c, j) => (j === i ? v : c)));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!skill.trim() || !prompt.trim() || busy) return;
    setBusy(true); setErr('');
    try {
      const base = { type, level, skill: skill.trim(), prompt: prompt.trim() };
      let body: Omit<Question, 'id' | 'topic_slug'>;
      if (type === 'mcq') {
        const cs = choices.map((c) => c.trim());
        if (cs.some((c) => !c)) throw new Error('All 4 choices are required for MCQ');
        body = { ...base, choices: cs, answer_index: answerIndex };
      } else if (type === 'written') {
        let parsed: Record<string, unknown>;
        try { parsed = JSON.parse(rubric); }
        catch { throw new Error('Rubric must be valid JSON'); }
        body = { ...base, rubric: parsed };
      } else {
        body = base;
      }
      onSaved(await contentApi.createQuestion(topicSlug, body));
    } catch (e2) {
      setErr(e2 instanceof Error ? e2.message : errMsg(e2));
    } finally { setBusy(false); }
  };

  return (
    <form className="cm-form cm-card" onSubmit={submit}>
      <h4>New question</h4>
      {err && <div className="cm-error">{err}</div>}
      <div className="cm-row2">
        <label>Type
          <select value={type} onChange={(e) => setType(e.target.value as QuestionType)}>
            {Q_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
          </select>
        </label>
        <label>Level
          <select value={level} onChange={(e) => setLevel(e.target.value)}>
            {LEVELS.map((l) => <option key={l} value={l}>{l}</option>)}
          </select>
        </label>
      </div>
      <label>Skill tag <input value={skill} onChange={(e) => setSkill(e.target.value)} placeholder="python-basics" required /></label>
      <label>Prompt
        <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} rows={3} required />
      </label>
      {type === 'mcq' && (
        <fieldset className="cm-fieldset">
          <legend>Choices (mark the correct one)</legend>
          {choices.map((c, i) => (
            <div key={i} className="cm-row">
              <input type="radio" name="ans" checked={answerIndex === i} onChange={() => setAnswerIndex(i)} aria-label={`Choice ${i + 1} is correct`} />
              <input value={c} onChange={(e) => setChoice(i, e.target.value)} placeholder={`Choice ${i + 1}`} />
            </div>
          ))}
        </fieldset>
      )}
      {type === 'written' && (
        <label>Rubric (JSON — key concepts for grading)
          <textarea value={rubric} onChange={(e) => setRubric(e.target.value)} rows={5} spellCheck={false} />
        </label>
      )}
      {type === 'coding' && (
        <p className="cm-muted">Coding questions are graded by hidden tests on the backend. Add tests via the runner admin later.</p>
      )}
      <div className="cm-row">
        <button type="button" className="cm-btn" onClick={onCancel}>Cancel</button>
        <button className="cm-btn primary" disabled={busy}>{busy ? 'Saving…' : 'Save Question'}</button>
      </div>
    </form>
  );
}

/* ---------------- Import from Link ---------------- */

type ImportState = 'idle' | 'loading' | 'preview' | 'error' | 'saved';

function ImportTab({ topic }: { topic: Topic }) {
  const [url, setUrl] = useState('');
  const [state, setState] = useState<ImportState>('idle');
  const [result, setResult] = useState<ImportResult | null>(null);
  const [err, setErr] = useState('');
  // editable preview fields
  const [title, setTitle] = useState('');
  const [level, setLevel] = useState('beginner');
  const [body, setBody] = useState('');
  const [order, setOrder] = useState(0);
  const [busy, setBusy] = useState(false);

  const run = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim() || state === 'loading') return;
    setState('loading'); setErr(''); setResult(null);
    try {
      const r = await contentApi.importLink(url.trim());
      setResult(r);
      setTitle(r.title);
      setLevel('beginner');
      setBody(r.body_md || `# ${r.title}\n\n${r.description}\n\n${r.headings.map((h) => `## ${h}`).join('\n\n')}`);
      setState('preview');
    } catch (e2) {
      setErr(errMsg(e2));
      setState('error');
    }
  };

  const save = async () => {
    if (!title.trim() || !body.trim() || busy) return;
    setBusy(true); setErr('');
    try {
      await contentApi.saveTheory(topic.slug, { title: title.trim(), level, body_md: body, order: Number(order) || 0 });
      setState('saved');
    } catch (e2) { setErr(errMsg(e2)); } finally { setBusy(false); }
  };

  return (
    <div>
      <h3>🔗 Import from Link</h3>
      <p className="cm-muted">Paste a tutorial/docs URL. We fetch the page and extract its structure — you review and save it as a theory block.</p>
      <form className="cm-form" onSubmit={run}>
        <label>Page URL
          <input value={url} onChange={(e) => setUrl(e.target.value)} placeholder="https://…" inputMode="url" required />
        </label>
        <button className="cm-btn primary" disabled={state === 'loading'}>
          {state === 'loading' ? 'Fetching…' : 'Fetch & Preview'}
        </button>
      </form>

      {state === 'loading' && <p className="cm-muted">⏳ Fetching page…</p>}

      {state === 'error' && (
        <div className="cm-card">
          <div className="cm-error">⚠️ Could not fetch that URL — the site may block scrapers or the link is invalid. <strong>Paste the content manually</strong> below instead.</div>
          {err && <p className="cm-muted">{err}</p>}
          <button className="cm-btn" onClick={() => { setResult({ title: '', description: '', headings: [], body_md: '', source_url: url }); setTitle(''); setBody(''); setState('preview'); }}>
            Paste manually
          </button>
        </div>
      )}

      {state === 'preview' && result && (
        <div className="cm-card">
          <h4>Preview — edit before saving</h4>
          <p className="cm-muted">Source: <a href={result.source_url} target="_blank" rel="noopener noreferrer">{result.source_url}</a></p>
          {result.headings.length > 0 && (
            <div className="cm-headings">
              <strong>Detected headings:</strong>
              <ul>{result.headings.slice(0, 12).map((h, i) => <li key={i}>{h}</li>)}</ul>
            </div>
          )}
          <div className="cm-form">
            {err && <div className="cm-error">{err}</div>}
            <label>Title <input value={title} onChange={(e) => setTitle(e.target.value)} required /></label>
            <div className="cm-row2">
              <label>Level
                <select value={level} onChange={(e) => setLevel(e.target.value)}>
                  {LEVELS.map((l) => <option key={l} value={l}>{l}</option>)}
                </select>
              </label>
              <label>Order <input type="number" value={order} onChange={(e) => setOrder(Number(e.target.value))} min={0} /></label>
            </div>
            <label>Body (markdown — editable)
              <textarea value={body} onChange={(e) => setBody(e.target.value)} rows={10} required />
            </label>
            <div className="cm-row">
              <button type="button" className="cm-btn" onClick={() => setState('idle')}>Discard</button>
              <button className="cm-btn primary" disabled={busy} onClick={save}>{busy ? 'Saving…' : '💾 Save as Theory'}</button>
            </div>
          </div>
        </div>
      )}

      {state === 'saved' && (
        <div className="cm-card cm-saved">
          ✅ Saved as a theory block for <strong>{topic.name}</strong>. Find it under the Theory tab.
          <div className="cm-row"><button className="cm-btn" onClick={() => { setState('idle'); setUrl(''); }}>Import another</button></div>
        </div>
      )}
    </div>
  );
}
