import { useEffect, useState } from 'react';
import { roadmapApi, ApiError, type Evidence, type RoadmapTask } from '../lib/p1api';
import './p1-pages.css';

interface EvidenceWithTask extends Evidence {
  taskTitle: string;
  taskStatus: string;
}

function EvidenceDetailPanel({ item, onClose }: { item: EvidenceWithTask; onClose: () => void }) {
  return (
    <div className="p1x-overlay" onClick={onClose}>
      <div className="p1x-panel" onClick={(e) => e.stopPropagation()}>
        <button className="p1x-btn ghost sm close" onClick={onClose}>✕ Close</button>
        <span className="p1x-pill violet">{item.kind.toUpperCase()}</span>
        <h2 style={{ marginTop: 10 }}>Evidence detail</h2>
        <p className="p1x-muted" style={{ fontSize: 14 }}>
          Task: <b style={{ color: 'var(--text)' }}>{item.taskTitle}</b> · {item.taskStatus.replace('_', ' ')}
        </p>
        <div className="sec">
          <h4>SUBMITTED</h4>
          <p className="p1x-muted" style={{ fontSize: 13 }}>{new Date(item.created_at).toLocaleString()}</p>
        </div>
        <div className="sec">
          <h4>CONTENT</h4>
          <p style={{ whiteSpace: 'pre-wrap', fontFamily: item.kind === 'code' ? 'Consolas,monospace' : 'inherit', fontSize: 13.5 }}>
            {item.content}
          </p>
        </div>
        {item.feedback && (
          <div className="sec">
            <h4>FEEDBACK</h4>
            <p>💬 {item.feedback}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default function EvidencePage() {
  const [items, setItems] = useState<EvidenceWithTask[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selected, setSelected] = useState<EvidenceWithTask | null>(null);
  const [filter, setFilter] = useState<'all' | 'text' | 'code' | 'url'>('all');

  useEffect(() => {
    (async () => {
      try {
        const rm = await roadmapApi.current().catch((e) => {
          if (e instanceof ApiError && e.status === 400) return null;
          throw e;
        });
        if (!rm) {
          setItems([]);
          return;
        }
        const results = await Promise.all(
          rm.tasks.map(async (t: RoadmapTask) => {
            const ev = await roadmapApi.listEvidence(t.id).catch(() => []);
            return ev.map((e) => ({ ...e, taskTitle: t.title, taskStatus: t.status }));
          }),
        );
        const all = results.flat().sort((a, b) => b.created_at.localeCompare(a.created_at));
        setItems(all);
      } catch (err) {
        setError(err instanceof ApiError ? err.message : 'Load failed');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading)
    return (
      <div className="p1x">
        <p className="p1x-loading">Loading evidence…</p>
      </div>
    );

  const shown = filter === 'all' ? items : items.filter((i) => i.kind === filter);

  return (
    <div className="p1x">
      <div className="p1x-head">
        <div>
          <h1 className="p1x-title">Evidence</h1>
          <p className="p1x-sub">Proof of work across all roadmap tasks — this is what certificates are built on.</p>
        </div>
        <div className="p1x-tabs" style={{ margin: 0 }}>
          {(['all', 'text', 'code', 'url'] as const).map((k) => (
            <button key={k} className={`p1x-tab ${filter === k ? 'active' : ''}`} onClick={() => setFilter(k)}>
              {k === 'all' ? `All (${items.length})` : k}
            </button>
          ))}
        </div>
      </div>
      {error && <div className="p1x-err">{error}</div>}

      <div className="p1x-card">
        {shown.length === 0 && (
          <p className="p1x-empty">
            {items.length === 0
              ? 'No evidence yet — start a roadmap task and submit proof of work from the Roadmap page.'
              : `No ${filter} evidence yet.`}
          </p>
        )}
        {shown.map((e) => (
          <button key={e.id} className="p1x-task" onClick={() => setSelected(e)} style={{ cursor: 'pointer' }}>
            <div className="n">🛡</div>
            <div style={{ flex: 1 }}>
              <div className="tt">{e.taskTitle}</div>
              <div className="why">
                {e.content.length > 140 ? e.content.slice(0, 140) + '…' : e.content}
              </div>
              <div className="row">
                <span className="p1x-pill violet">{e.kind.toUpperCase()}</span>
                <span className="p1x-muted" style={{ fontSize: 12 }}>
                  {new Date(e.created_at).toLocaleString()}
                </span>
                {e.feedback && <span className="p1x-pill info">HAS FEEDBACK</span>}
                <span className="p1x-muted" style={{ marginLeft: 'auto', fontSize: 12 }}>Details →</span>
              </div>
            </div>
          </button>
        ))}
      </div>

      {selected && <EvidenceDetailPanel item={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
