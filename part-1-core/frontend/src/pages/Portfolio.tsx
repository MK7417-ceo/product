import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { portfolioApi, ApiError, type Portfolio } from '../lib/api';

export default function PortfolioPage() {
  const [pf, setPf] = useState<Portfolio | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [noResume, setNoResume] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        setPf(await portfolioApi.get());
      } catch (err) {
        if (err instanceof ApiError && err.status === 404) setNoResume(true);
        else setError(err instanceof ApiError ? err.message : 'Load failed');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const download = async () => {
    if (busy) return;
    setError('');
    setBusy(true);
    try {
      const { blob, filename } = await portfolioApi.download();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Download failed');
    } finally {
      setBusy(false);
    }
  };

  if (loading) return <p className="page-sub">Building portfolio preview…</p>;

  return (
    <div>
      <h1 className="page-title">Portfolio</h1>
      <p className="page-sub">Tumhari SkillForge journey — ek page mein. Download karo, GitHub Pages par host karo.</p>
      {error && <p className="error">{error}</p>}

      {noResume ? (
        <div className="card">
          <p className="muted" style={{ marginTop: 0 }}>
            Portfolio ke liye pehle resume chahiye.
          </p>
          <Link className="btn primary" to="/resume">Resume banao</Link>
        </div>
      ) : pf && (
        <>
          <div className="card">
            <h2 style={{ margin: '0 0 4px' }}>{pf.name}</h2>
            <p className="muted" style={{ marginTop: 0 }}>{pf.summary}</p>
            <div className="chips">
              {pf.skills.map((s) => <span key={s} className="chip ok">{s}</span>)}
            </div>
            {(pf.roadmap_total > 0) && (
              <div style={{ marginTop: 12 }}>
                <div className="muted" style={{ fontSize: 13 }}>
                  {pf.roadmap_title} — {pf.roadmap_done}/{pf.roadmap_total} tasks · {pf.evidence_count} evidence
                </div>
                <div className="pbar" style={{ marginTop: 6 }}>
                  <div className="pfill" style={{ width: `${(100 * pf.roadmap_done) / pf.roadmap_total}%` }} />
                </div>
              </div>
            )}
            {pf.certificates.length > 0 && (
              <div style={{ marginTop: 12 }}>
                <strong>🏆 {pf.certificates.length} certificate{pf.certificates.length > 1 ? 's' : ''}</strong>
                {pf.certificates.map((c) => (
                  <div key={c.verification_code} className="muted" style={{ fontSize: 13 }}>
                    {c.title} · <code className="mini-code">{c.verification_code}</code>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="card">
            <h3 style={{ marginTop: 0 }}>Publish karo</h3>
            <p className="muted" style={{ fontSize: 14, marginTop: 0 }}>
              Single-file HTML download karo — koi external asset nahi, seedha GitHub Pages par host hoga.
            </p>
            <button className="btn primary" disabled={busy} onClick={download}>
              {busy ? 'Preparing…' : '⬇ Download portfolio.html'}
            </button>
            <p className="muted" style={{ fontSize: 13, marginBottom: 0 }}>
              GitHub par one-click publish jald aa raha hai — account linking (P3f) ke baad.
              Tab tak: repo banao → yeh file <code className="mini-code">index.html</code> naam se push karo → Settings → Pages ON.
            </p>
          </div>
        </>
      )}

      <style>{`
        .chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }
        .chip.ok { padding: 4px 12px; border-radius: 16px; font-size: 13px; background: rgba(125, 211, 252, 0.1); color: #7dd3fc; border: 1px solid rgba(125, 211, 252, 0.3); }
        .pbar { height: 8px; background: #0d1117; border-radius: 4px; overflow: hidden; }
        .pfill { height: 100%; background: linear-gradient(90deg, #7dd3fc, #4ade80); }
        .mini-code { font-family: monospace; font-size: 12px; color: #7dd3fc; }
      `}</style>
    </div>
  );
}
