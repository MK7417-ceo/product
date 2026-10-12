import { useEffect, useState } from 'react';
import { roadmapApi, ApiError, type Roadmap, type RoadmapTask, type Evidence } from '../lib/p1api';
import './p1-pages.css';

const PRI_CLASS: Record<string, string> = {
  high: 'amber', medium: 'info', low: 'claim',
};

function TaskDetailPanel({
  task,
  onClose,
  onChanged,
}: {
  task: RoadmapTask;
  onClose: () => void;
  onChanged: () => void;
}) {
  const [ev, setEv] = useState<Evidence[]>([]);
  const [evError, setEvError] = useState('');
  const [evKind, setEvKind] = useState('text');
  const [evContent, setEvContent] = useState('');
  const [busy, setBusy] = useState(false);
  const [submitErr, setSubmitErr] = useState('');

  useEffect(() => {
    roadmapApi
      .listEvidence(task.id)
      .then(setEv)
      .catch((err) => setEvError(err instanceof ApiError ? err.message : 'Could not load evidence'));
  }, [task.id]);

  const startTask = async () => {
    setBusy(true);
    setSubmitErr('');
    try {
      await roadmapApi.updateTask(task.id, 'in_progress');
      onChanged();
    } catch (err) {
      setSubmitErr(err instanceof ApiError ? err.message : 'Update failed');
    } finally {
      setBusy(false);
    }
  };

  const submitEvidence = async () => {
    if (!evContent.trim()) return;
    setBusy(true);
    setSubmitErr('');
    try {
      const e = await roadmapApi.submitEvidence(task.id, evKind, evContent.trim());
      setEv((prev) => [e, ...prev]);
      setEvContent('');
      onChanged(); // task auto-completes on evidence submit
    } catch (err) {
      setSubmitErr(err instanceof ApiError ? err.message : 'Submit failed');
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="p1x-overlay" onClick={onClose}>
      <div className="p1x-panel" onClick={(e) => e.stopPropagation()}>
        <button className="p1x-btn ghost sm close" onClick={onClose}>✕ Close</button>
        <span className={`p1x-pill ${task.status === 'completed' ? 'ok' : task.status === 'in_progress' ? 'info' : 'claim'}`}>
          {task.status.replace('_', ' ').toUpperCase()}
        </span>
        <h2 style={{ marginTop: 10 }}>{task.title}</h2>
        <p className="p1x-muted" style={{ fontSize: 14 }}>{task.description}</p>

        <div className="sec">
          <h4>WHY IT MATTERS</h4>
          <p>{task.why_it_matters}</p>
        </div>
        <div className="sec">
          <h4>DETAILS</h4>
          <div className="p1x-kv"><b>Effort</b><span>⏱ {task.effort_minutes} min</span></div>
          <div className="p1x-kv"><b>Priority</b><span className={`p1x-pill ${PRI_CLASS[task.priority] ?? 'claim'}`}>{task.priority.toUpperCase()}</span></div>
          <div className="p1x-kv"><b>Target skills</b><span>{task.target_skills.join(', ') || '—'}</span></div>
          <div className="p1x-kv"><b>Expected evidence</b><span>📦 {task.expected_evidence}</span></div>
          {task.prerequisites.length > 0 && (
            <div className="p1x-kv"><b>Prerequisites</b><span>{task.prerequisites.join(', ')}</span></div>
          )}
        </div>
        <div className="sec">
          <h4>ACCEPTANCE CRITERIA</h4>
          <p>{task.acceptance_criteria}</p>
        </div>

        {task.status === 'pending' && (
          <button className="p1x-btn" onClick={startTask} disabled={busy} style={{ width: '100%' }}>
            {busy ? 'Starting…' : 'Start task →'}
          </button>
        )}

        <div className="sec">
          <h4>EVIDENCE ({ev.length})</h4>
          {evError && <div className="p1x-err">{evError}</div>}
          {ev.map((e) => (
            <div key={e.id} style={{ border: '1px solid var(--border)', borderRadius: 10, padding: 12, marginBottom: 8 }}>
              <span className="p1x-pill violet">{e.kind.toUpperCase()}</span>
              <span className="p1x-muted" style={{ fontSize: 12, marginLeft: 8 }}>
                {new Date(e.created_at).toLocaleString()}
              </span>
              <p style={{ fontSize: 13.5, margin: '8px 0 0', whiteSpace: 'pre-wrap' }}>
                {e.content.length > 220 ? e.content.slice(0, 220) + '…' : e.content}
              </p>
              {e.feedback && <p className="p1x-muted" style={{ fontSize: 12.5, margin: '6px 0 0' }}>💬 {e.feedback}</p>}
            </div>
          ))}
          {ev.length === 0 && !evError && <p className="p1x-muted" style={{ fontSize: 13.5 }}>No evidence yet.</p>}
        </div>

        {task.status === 'in_progress' && (
          <div className="sec">
            <h4>SUBMIT EVIDENCE — PROOF COMPLETES THE TASK</h4>
            {submitErr && <div className="p1x-err">{submitErr}</div>}
            <div style={{ display: 'flex', gap: 8, marginBottom: 10 }}>
              {['text', 'code', 'url'].map((k) => (
                <button
                  key={k}
                  className={`p1x-btn sm ${evKind === k ? '' : 'ghost'}`}
                  onClick={() => setEvKind(k)}
                >
                  {k}
                </button>
              ))}
            </div>
            <div className="p1x-field">
              <textarea
                value={evContent}
                onChange={(e) => setEvContent(e.target.value)}
                rows={5}
                placeholder={evKind === 'code' ? 'Paste your code…' : evKind === 'url' ? 'https://…' : 'What did you do / learn?'}
                style={evKind === 'code' ? { fontFamily: 'Consolas,monospace' } : undefined}
              />
            </div>
            <button className="p1x-btn" disabled={busy || !evContent.trim()} onClick={submitEvidence} style={{ width: '100%' }}>
              {busy ? 'Submitting…' : 'Submit proof ✓'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default function Roadmap() {
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [gaps, setGaps] = useState([{ skill: 'python-basics', mastery: '35' }]);
  const [detailTask, setDetailTask] = useState<RoadmapTask | null>(null);
  const [regenOpen, setRegenOpen] = useState(false);

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

  const generate = async (regen: boolean) => {
    setError('');
    setBusy(true);
    try {
      const parsed = gaps.map((g) => ({ skill: g.skill.trim(), mastery_pct: Number(g.mastery) }));
      const r = regen ? await roadmapApi.regenerate(parsed) : await roadmapApi.generate(parsed, 'My Roadmap');
      setRoadmap(r);
      setRegenOpen(false);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Generate failed');
    } finally {
      setBusy(false);
    }
  };

  if (loading) return <div className="p1x"><p className="p1x-loading">Loading roadmap…</p></div>;

  if (!roadmap) {
    return (
      <div className="p1x">
        <div className="p1x-head">
          <div>
            <h1 className="p1x-title">Roadmap</h1>
            <p className="p1x-sub">Turn your skill gaps into a learning plan. Worst gaps first.</p>
          </div>
        </div>
        <div className="p1x-card" style={{ maxWidth: 600 }}>
          {error && <div className="p1x-err">{error}</div>}
          {gaps.map((g, i) => (
            <div key={i} style={{ display: 'flex', gap: 10, marginBottom: 10 }}>
              <div className="p1x-field" style={{ flex: 2, margin: 0 }}>
                <input
                  value={g.skill}
                  placeholder="skill (e.g. sql)"
                  onChange={(e) => setGaps((gs) => gs.map((x, j) => (j === i ? { ...x, skill: e.target.value } : x)))}
                />
              </div>
              <div className="p1x-field" style={{ flex: 1, margin: 0 }}>
                <input
                  value={g.mastery}
                  placeholder="mastery %" type="number" min={0} max={100}
                  onChange={(e) => setGaps((gs) => gs.map((x, j) => (j === i ? { ...x, mastery: e.target.value } : x)))}
                />
              </div>
              <button className="p1x-btn ghost sm" onClick={() => setGaps((gs) => gs.filter((_, j) => j !== i))}>✕</button>
            </div>
          ))}
          <button className="p1x-btn ghost sm" style={{ marginBottom: 16 }} onClick={() => setGaps((gs) => [...gs, { skill: '', mastery: '' }])}>
            + add gap
          </button>
          <br />
          <button className="p1x-btn" onClick={() => generate(false)} disabled={busy}>
            {busy ? 'Generating…' : 'Generate my roadmap'}
          </button>
        </div>
      </div>
    );
  }

  const c = roadmap.task_counts;
  const pct = c.total ? Math.round((100 * c.completed) / c.total) : 0;

  return (
    <div className="p1x">
      <div className="p1x-head">
        <div>
          <h1 className="p1x-title">
            {roadmap.title} <span className="p1x-muted" style={{ fontSize: 15, fontWeight: 600 }}>v{roadmap.version}</span>
          </h1>
          <p className="p1x-sub">
            {c.completed}/{c.total} done · {c.in_progress} in progress · completed work is never lost on regenerate
          </p>
        </div>
        <button className="p1x-btn ghost" onClick={() => setRegenOpen(true)} disabled={busy}>⟳ Regenerate</button>
      </div>

      <div className="p1x-card">
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, color: 'var(--muted)', marginBottom: 6 }}>
          <span>OVERALL PROGRESS</span>
          <span style={{ fontWeight: 700 }}>{pct}%</span>
        </div>
        <div className="p1x-bar"><i style={{ width: `${pct}%` }} /></div>
      </div>

      {error && <div className="p1x-err">{error}</div>}

      {regenOpen && (
        <div className="p1x-card" style={{ borderColor: 'rgba(139,92,246,.4)' }}>
          <h3>Regenerate with fresh gaps</h3>
          <p className="hint">Completed tasks and their evidence carry forward untouched.</p>
          {gaps.map((g, i) => (
            <div key={i} style={{ display: 'flex', gap: 10, marginBottom: 10 }}>
              <div className="p1x-field" style={{ flex: 2, margin: 0 }}>
                <input
                  value={g.skill}
                  placeholder="skill"
                  onChange={(e) => setGaps((gs) => gs.map((x, j) => (j === i ? { ...x, skill: e.target.value } : x)))}
                />
              </div>
              <div className="p1x-field" style={{ flex: 1, margin: 0 }}>
                <input
                  value={g.mastery}
                  placeholder="mastery %" type="number" min={0} max={100}
                  onChange={(e) => setGaps((gs) => gs.map((x, j) => (j === i ? { ...x, mastery: e.target.value } : x)))}
                />
              </div>
              <button className="p1x-btn ghost sm" onClick={() => setGaps((gs) => gs.filter((_, j) => j !== i))}>✕</button>
            </div>
          ))}
          <div style={{ display: 'flex', gap: 10 }}>
            <button className="p1x-btn ghost sm" onClick={() => setGaps((gs) => [...gs, { skill: '', mastery: '' }])}>+ add gap</button>
            <span style={{ flex: 1 }} />
            <button className="p1x-btn ghost" onClick={() => setRegenOpen(false)}>Cancel</button>
            <button className="p1x-btn" onClick={() => generate(true)} disabled={busy}>
              {busy ? 'Regenerating…' : 'Regenerate'}
            </button>
          </div>
        </div>
      )}

      {roadmap.tasks.map((t, i) => (
        <button
          key={t.id}
          className={`p1x-task ${t.status === 'completed' ? 'done' : ''}`}
          onClick={() => setDetailTask(t)}
        >
          <div className="n">{t.status === 'completed' ? '✓' : i + 1}</div>
          <div style={{ flex: 1 }}>
            <div className="tt">{t.title}</div>
            <div className="why">{t.why_it_matters}</div>
            <div className="meta">
              <span>⏱ {t.effort_minutes} min</span>
              <span>🎯 {t.target_skills.join(', ')}</span>
              <span>📦 {t.expected_evidence}</span>
            </div>
            <div className="row">
              <span className={`p1x-pill ${PRI_CLASS[t.priority] ?? 'claim'}`}>{t.priority.toUpperCase()}</span>
              <span className={`p1x-pill ${t.status === 'completed' ? 'ok' : t.status === 'in_progress' ? 'info' : 'claim'}`}>
                {t.status.replace('_', ' ').toUpperCase()}
              </span>
              <span className="p1x-muted" style={{ marginLeft: 'auto', fontSize: 12 }}>Details →</span>
            </div>
          </div>
        </button>
      ))}

      {detailTask && (
        <TaskDetailPanel
          task={detailTask}
          onClose={() => setDetailTask(null)}
          onChanged={async () => {
            await load();
            const fresh = await roadmapApi.current().catch(() => null);
            setDetailTask(fresh?.tasks.find((t) => t.id === detailTask.id) ?? null);
          }}
        />
      )}
    </div>
  );
}
