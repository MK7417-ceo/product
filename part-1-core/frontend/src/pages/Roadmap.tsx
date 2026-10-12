import { useEffect, useState } from 'react';
import { roadmapApi, ApiError, type Roadmap, type RoadmapTask } from '../lib/api';

const PRI_COLOR: Record<string, string> = {
  high: '#fbbf24', medium: '#7dd3fc', low: '#8b93a7',
};
const STATUS_COLOR: Record<string, string> = {
  pending: '#8b93a7', in_progress: '#7dd3fc', completed: '#4ade80',
};

export default function RoadmapPage() {
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  // generate form
  const [gaps, setGaps] = useState([{ skill: 'python-basics', mastery: '35' }]);
  // evidence modal
  const [evTask, setEvTask] = useState<RoadmapTask | null>(null);
  const [evKind, setEvKind] = useState('text');
  const [evContent, setEvContent] = useState('');

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      setRoadmap(await roadmapApi.current());
    } catch (err) {
      if (err instanceof ApiError && err.status === 400) setRoadmap(null);
      else setError(err instanceof ApiError ? err.message : 'Load failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const generate = async () => {
    setError('');
    setBusy(true);
    try {
      const parsed = gaps.map((g) => ({ skill: g.skill.trim(), mastery_pct: Number(g.mastery) }));
      const r = await roadmapApi.generate(parsed, 'My Roadmap');
      setRoadmap(r);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Generate failed');
    } finally {
      setBusy(false);
    }
  };

  const startTask = async (t: RoadmapTask) => {
    setError('');
    try {
      await roadmapApi.updateTask(t.id, 'in_progress');
      await load();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Update failed');
    }
  };

  const submitEvidence = async () => {
    if (!evTask) return;
    setError('');
    setBusy(true);
    try {
      await roadmapApi.submitEvidence(evTask.id, evKind, evContent);
      setEvTask(null);
      setEvKind('text');
      setEvContent('');
      await load();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Submit failed');
    } finally {
      setBusy(false);
    }
  };

  const regenerate = async () => {
    if (!roadmap) return;
    const input = prompt('Fresh gaps as skill:mastery, comma-separated (e.g. sql:55,python-basics:60):');
    if (!input) return;
    setBusy(true);
    try {
      const parsed = input.split(',').map((p) => {
        const [skill, m] = p.split(':').map((s) => s.trim());
        return { skill, mastery_pct: Number(m) };
      });
      const r = await roadmapApi.regenerate(parsed);
      setRoadmap(r);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Regenerate failed');
    } finally {
      setBusy(false);
    }
  };

  if (loading) return <p style={{ color: '#8b93a7' }}>Loading…</p>;

  if (!roadmap) {
    return (
      <div>
        <h1 className="page-title">Roadmap</h1>
        <p className="page-sub">Turn your skill gaps into a learning plan. Worst gaps first.</p>
        <div className="card" style={{ maxWidth: 560 }}>
          {error && <div className="auth-err">{error}</div>}
          {gaps.map((g, i) => (
            <div key={i} style={{ display: 'flex', gap: 10, marginBottom: 10 }}>
              <div className="field" style={{ flex: 2, margin: 0 }}>
                <input value={g.skill} placeholder="skill (e.g. sql)"
                  onChange={(e) => setGaps((gs) => gs.map((x, j) => j === i ? { ...x, skill: e.target.value } : x))} />
              </div>
              <div className="field" style={{ flex: 1, margin: 0 }}>
                <input value={g.mastery} placeholder="mastery %" type="number" min={0} max={100}
                  onChange={(e) => setGaps((gs) => gs.map((x, j) => j === i ? { ...x, mastery: e.target.value } : x))} />
              </div>
              <button className="btn-ghost" style={{ padding: '10px 14px' }}
                onClick={() => setGaps((gs) => gs.filter((_, j) => j !== i))}>✕</button>
            </div>
          ))}
          <button className="btn-ghost" style={{ fontSize: 13, marginBottom: 16 }}
            onClick={() => setGaps((gs) => [...gs, { skill: '', mastery: '' }])}>+ add gap</button>
          <br />
          <button className="btn" onClick={generate} disabled={busy}>
            {busy ? 'Generating…' : 'Generate my roadmap'}
          </button>
        </div>
      </div>
    );
  }

  const c = roadmap.task_counts;
  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
        <h1 className="page-title">{roadmap.title} <span style={{ fontSize: 14, color: '#8b93a7' }}>v{roadmap.version}</span></h1>
        <button className="btn-ghost" style={{ fontSize: 13 }} onClick={regenerate} disabled={busy}>
          ⟳ Regenerate
        </button>
      </div>
      <p className="page-sub">{c.completed}/{c.total} done · {c.in_progress} in progress · completed work is never lost on regenerate</p>
      {error && <div className="auth-err">{error}</div>}
      {roadmap.tasks.map((t, i) => (
        <div className="card" key={t.id} style={{ marginBottom: 12, opacity: t.status === 'completed' ? 0.75 : 1 }}>
          <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start' }}>
            <div style={{
              width: 30, height: 30, borderRadius: 9, flexShrink: 0,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 13, fontWeight: 700,
              background: t.status === 'completed' ? 'rgba(74,222,128,.12)' : 'rgba(124,58,237,.12)',
              color: t.status === 'completed' ? '#4ade80' : '#a78bfa',
            }}>{t.status === 'completed' ? '✓' : i + 1}</div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 14, fontWeight: 700 }}>{t.title}</div>
              <div style={{ fontSize: 12.5, color: '#8b93a7', marginTop: 4 }}>{t.why_it_matters}</div>
              <div style={{ fontSize: 11.5, color: '#7dd3fc', marginTop: 6 }}>
                ⏱ {t.effort_minutes} min · 🎯 {t.target_skills.join(', ')} · 📦 {t.expected_evidence}
              </div>
              <div style={{ display: 'flex', gap: 8, marginTop: 10, alignItems: 'center' }}>
                <span style={{ fontSize: 11, fontWeight: 700, color: PRI_COLOR[t.priority] }}>{t.priority.toUpperCase()}</span>
                <span style={{ fontSize: 11, color: STATUS_COLOR[t.status] }}>● {t.status.replace('_', ' ')}</span>
                {t.status === 'pending' && (
                  <button className="btn" style={{ padding: '7px 16px', fontSize: 12, marginLeft: 'auto' }}
                    onClick={() => startTask(t)}>Start task</button>
                )}
                {t.status === 'in_progress' && (
                  <button className="btn" style={{ padding: '7px 16px', fontSize: 12, marginLeft: 'auto' }}
                    onClick={() => setEvTask(t)}>Submit evidence</button>
                )}
              </div>
            </div>
          </div>
        </div>
      ))}

      {evTask && (
        <div style={{
          position: 'fixed', inset: 0, background: 'rgba(0,0,0,.6)', zIndex: 10,
          display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 20,
        }}>
          <div className="card" style={{ maxWidth: 520, width: '100%' }}>
            <h3 style={{ fontSize: 15, marginBottom: 4 }}>Submit evidence</h3>
            <p className="page-sub" style={{ marginBottom: 14 }}>{evTask.title} — proof completes the task</p>
            <div className="field">
              <label>Kind</label>
              <div style={{ display: 'flex', gap: 8 }}>
                {['text', 'code', 'url'].map((k) => (
                  <button key={k} className={evKind === k ? 'btn' : 'btn-ghost'}
                    style={{ padding: '9px 18px', fontSize: 13 }} onClick={() => setEvKind(k)}>{k}</button>
                ))}
              </div>
            </div>
            <div className="field">
              <label>{evKind === 'code' ? 'Your code' : evKind === 'url' ? 'Link (https://…)' : 'Your notes'}</label>
              <textarea value={evContent} onChange={(e) => setEvContent(e.target.value)} rows={5}
                style={{
                  width: '100%', padding: 12, fontSize: 13, borderRadius: 10,
                  background: 'rgba(255,255,255,.05)', border: '1px solid rgba(255,255,255,.08)',
                  color: '#e8edf7', fontFamily: evKind === 'code' ? 'Consolas,monospace' : 'inherit',
                }} />
            </div>
            <div style={{ display: 'flex', gap: 10 }}>
              <button className="btn" onClick={submitEvidence} disabled={busy || !evContent.trim()} style={{ flex: 1 }}>
                {busy ? 'Submitting…' : 'Submit proof'}
              </button>
              <button className="btn-ghost" onClick={() => setEvTask(null)}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
