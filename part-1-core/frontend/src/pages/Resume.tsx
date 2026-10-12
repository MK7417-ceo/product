import { useEffect, useState } from 'react';
import { launchpadApi, ApiError, type ResumeData, type JDMatchResult } from '../lib/api';

const EMPTY: Omit<ResumeData, 'id'> = {
  title: '', summary: '', skills: [], experience: [], projects: [], education: [], links: {},
};

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="rsec">
      <h3>{title}</h3>
      {children}
    </div>
  );
}

export default function Resume() {
  const [tab, setTab] = useState<'build' | 'jd'>('build');
  const [form, setForm] = useState(EMPTY);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [saved, setSaved] = useState(false);
  const [busy, setBusy] = useState(false);
  // jd tab
  const [jd, setJd] = useState('');
  const [match, setMatch] = useState<JDMatchResult | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const r = await launchpadApi.getResume();
        const { id: _id, ...rest } = r;
        setForm(rest);
      } catch (err) {
        if (!(err instanceof ApiError && err.status === 404)) {
          setError(err instanceof ApiError ? err.message : 'Load failed');
        }
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const set = (k: keyof typeof EMPTY, v: unknown) => {
    setForm((f) => ({ ...f, [k]: v }));
    setSaved(false);
  };

  const addRow = (k: 'experience' | 'projects' | 'education') => {
    const blanks = {
      experience: { title: '', company: '', start: '', end: '', bullets: [] },
      projects: { name: '', description: '', tech: [], link: '' },
      education: { degree: '', school: '', year: '' },
    };
    set(k, [...(form[k] as unknown[]), blanks[k]]);
  };

  const delRow = (k: 'experience' | 'projects' | 'education', i: number) => {
    set(k, (form[k] as unknown[]).filter((_, j) => j !== i));
  };

  const editRow = (k: 'experience' | 'projects' | 'education', i: number, patch: object) => {
    set(k, (form[k] as unknown[]).map((row, j) => (j === i ? { ...(row as object), ...patch } : row)));
  };

  const save = async () => {
    setError('');
    setBusy(true);
    try {
      await launchpadApi.saveResume(form);
      setSaved(true);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Save failed');
    } finally {
      setBusy(false);
    }
  };

  const runMatch = async () => {
    if (!jd.trim() || busy) return;
    setError('');
    setBusy(true);
    setMatch(null);
    try {
      setMatch(await launchpadApi.matchJd(jd));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Match failed');
    } finally {
      setBusy(false);
    }
  };

  if (loading) return <p className="page-sub">Loading resume…</p>;

  const inp = 'rinput';
  return (
    <div>
      <h1 className="page-title">Resume</h1>
      <p className="page-sub">ATS-friendly resume banao, phir job description se match karo.</p>
      {error && <p className="error">{error}</p>}

      <div className="lang-tabs">
        <button className={'lang-tab' + (tab === 'build' ? ' active' : '')} onClick={() => setTab('build')}>Builder</button>
        <button className={'lang-tab' + (tab === 'jd' ? ' active' : '')} onClick={() => setTab('jd')}>JD Match</button>
      </div>

      {tab === 'build' && (
        <div className="card">
          <Section title="Basics">
            <input className={inp} placeholder="Resume title (e.g. AI/ML Engineer)" value={form.title} onChange={(e) => set('title', e.target.value)} />
            <textarea className={inp} placeholder="Summary — 2 lines mein tum kaun ho" value={form.summary} onChange={(e) => set('summary', e.target.value)} />
            <input className={inp} placeholder="Skills (comma separated): python, pytorch, sql" value={form.skills.join(', ')} onChange={(e) => set('skills', e.target.value.split(',').map((s) => s.trim()).filter(Boolean))} />
          </Section>

          <Section title="Experience">
            {form.experience.map((e, i) => (
              <div key={i} className="rrow">
                <input className={inp} placeholder="Title" value={e.title} onChange={(ev) => editRow('experience', i, { title: ev.target.value })} />
                <input className={inp} placeholder="Company" value={e.company} onChange={(ev) => editRow('experience', i, { company: ev.target.value })} />
                <textarea className={inp} placeholder="Bullets (ek line = ek bullet)" value={e.bullets.join('\n')} onChange={(ev) => editRow('experience', i, { bullets: ev.target.value.split('\n').map((s) => s.trim()).filter(Boolean) })} />
                <button className="btn small danger" onClick={() => delRow('experience', i)}>Remove</button>
              </div>
            ))}
            <button className="btn small" onClick={() => addRow('experience')}>+ Add experience</button>
          </Section>

          <Section title="Projects">
            {form.projects.map((p, i) => (
              <div key={i} className="rrow">
                <input className={inp} placeholder="Project name" value={p.name} onChange={(e) => editRow('projects', i, { name: e.target.value })} />
                <input className={inp} placeholder="Description" value={p.description} onChange={(e) => editRow('projects', i, { description: e.target.value })} />
                <input className={inp} placeholder="Tech (comma separated)" value={p.tech.join(', ')} onChange={(e) => editRow('projects', i, { tech: e.target.value.split(',').map((s) => s.trim()).filter(Boolean) })} />
                <button className="btn small danger" onClick={() => delRow('projects', i)}>Remove</button>
              </div>
            ))}
            <button className="btn small" onClick={() => addRow('projects')}>+ Add project</button>
          </Section>

          <Section title="Education">
            {form.education.map((e, i) => (
              <div key={i} className="rrow">
                <input className={inp} placeholder="Degree" value={e.degree} onChange={(ev) => editRow('education', i, { degree: ev.target.value })} />
                <input className={inp} placeholder="School" value={e.school} onChange={(ev) => editRow('education', i, { school: ev.target.value })} />
                <input className={inp} placeholder="Year" value={e.year} onChange={(ev) => editRow('education', i, { year: ev.target.value })} />
                <button className="btn small danger" onClick={() => delRow('education', i)}>Remove</button>
              </div>
            ))}
            <button className="btn small" onClick={() => addRow('education')}>+ Add education</button>
          </Section>

          <div style={{ display: 'flex', gap: 12, alignItems: 'center', marginTop: 16 }}>
            <button className="btn primary" disabled={busy} onClick={save}>{busy ? 'Saving…' : 'Save resume'}</button>
            {saved && <span style={{ color: '#4ade80' }}>✓ saved</span>}
          </div>
        </div>
      )}

      {tab === 'jd' && (
        <div>
          <div className="card">
            <h3 style={{ marginTop: 0 }}>Job description paste karo</h3>
            <textarea className={inp} style={{ minHeight: 140 }} placeholder="JD yahan paste karo…" value={jd} onChange={(e) => setJd(e.target.value)} />
            <button className="btn primary" disabled={busy || !jd.trim()} onClick={runMatch} style={{ marginTop: 10 }}>
              {busy ? 'Matching…' : 'Match karo'}
            </button>
          </div>
          {match && (
            <div className="card">
              <div className="score-banner">
                <span className="score-num">{match.score}%</span>
                <span className="muted">ATS match — {match.matched.length}/{match.jd_keyword_count} JD keywords mile</span>
              </div>
              <h4>Missing keywords</h4>
              <div className="chips">
                {match.missing.map((m) => (
                  <span key={m.keyword} className="chip miss">{m.keyword} ×{m.jd_count}</span>
                ))}
                {match.missing.length === 0 && <span className="muted">kuch missing nahi — solid!</span>}
              </div>
              <h4>Suggestions</h4>
              <ul className="sugg">
                {match.suggestions.map((s, i) => <li key={i}>{s}</li>)}
              </ul>
            </div>
          )}
        </div>
      )}

      <style>{`
        .rinput { width: 100%; box-sizing: border-box; background: #0d1117; color: #e6e9f0; border: 1px solid #232838; border-radius: 8px; padding: 10px 12px; margin: 6px 0; font-size: 14px; font-family: inherit; }
        textarea.rinput { min-height: 64px; resize: vertical; }
        .rsec { border-top: 1px solid #232838; padding: 12px 0; }
        .rsec:first-of-type { border-top: none; }
        .rsec h3 { margin: 0 0 6px; font-size: 15px; }
        .rrow { background: #0d1117; border: 1px solid #232838; border-radius: 10px; padding: 10px; margin: 8px 0; }
        .btn.danger { color: #f87171; }
        .score-banner { display: flex; align-items: center; gap: 14px; padding: 14px; border: 1px solid #232838; border-radius: 12px; margin: 12px 0; }
        .score-num { font-size: 28px; font-weight: 800; color: #7dd3fc; }
        .chips { display: flex; flex-wrap: wrap; gap: 8px; }
        .chip { padding: 4px 12px; border-radius: 16px; font-size: 13px; background: rgba(248, 113, 113, 0.12); color: #fca5a5; border: 1px solid rgba(248, 113, 113, 0.3); }
        .sugg { margin: 8px 0; padding-left: 20px; color: #c6cddb; font-size: 14px; }
        .sugg li { margin: 6px 0; }
        .lang-tabs { display: flex; gap: 8px; margin: 14px 0; }
        .lang-tab { padding: 8px 16px; border-radius: 10px; border: 1px solid #232838; background: #141821; color: #c6cddb; cursor: pointer; }
        .lang-tab.active { border-color: #7dd3fc; color: #7dd3fc; }
      `}</style>
    </div>
  );
}
