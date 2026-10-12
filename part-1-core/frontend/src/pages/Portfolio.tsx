import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { portfolioApi, ApiError, type Portfolio } from '../lib/p1api';
import './p1-pages.css';

export default function Portfolio() {
  const [pf, setPf] = useState<Portfolio | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [noResume, setNoResume] = useState(false);
  const [publishOpen, setPublishOpen] = useState(false);

  useEffect(() => {
    portfolioApi
      .get()
      .then(setPf)
      .catch((err) => {
        if (err instanceof ApiError && err.status === 404) setNoResume(true);
        else setError(err instanceof ApiError ? err.message : 'Load failed');
      })
      .finally(() => setLoading(false));
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
      setPublishOpen(false);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Download failed');
    } finally {
      setBusy(false);
    }
  };

  if (loading)
    return (
      <div className="p1x">
        <p className="p1x-loading">Building portfolio preview…</p>
      </div>
    );

  return (
    <div className="p1x">
      <div className="p1x-head">
        <div>
          <h1 className="p1x-title">Portfolio</h1>
          <p className="p1x-sub">Tumhari SkillForge journey — ek page mein. Download karo, GitHub Pages par host karo.</p>
        </div>
        {pf && (
          <button className="p1x-btn" onClick={() => setPublishOpen(true)}>🌐 Publish / Export</button>
        )}
      </div>
      {error && <div className="p1x-err">{error}</div>}

      {noResume ? (
        <div className="p1x-card">
          <p className="p1x-muted" style={{ marginTop: 0 }}>Portfolio ke liye pehle resume chahiye.</p>
          <Link className="p1x-btn" style={{ textDecoration: 'none', display: 'inline-block' }} to="/resume">
            Resume banao
          </Link>
        </div>
      ) : (
        pf && (
          <>
            <div className="p1x-card">
              <h2 style={{ fontSize: 22 }}>{pf.name}</h2>
              <p className="p1x-muted" style={{ marginTop: 4 }}>{pf.summary}</p>
              <div className="p1x-chips">
                {pf.skills.map((s) => (
                  <span key={s} className="p1x-chip">{s}</span>
                ))}
              </div>
              {pf.roadmap_total > 0 && (
                <div style={{ marginTop: 14 }}>
                  <div className="p1x-muted" style={{ fontSize: 13 }}>
                    {pf.roadmap_title} — {pf.roadmap_done}/{pf.roadmap_total} tasks · {pf.evidence_count} evidence
                  </div>
                  <div className="p1x-bar" style={{ marginTop: 6 }}>
                    <i style={{ width: `${(100 * pf.roadmap_done) / pf.roadmap_total}%` }} />
                  </div>
                </div>
              )}
              {pf.certificates.length > 0 && (
                <div style={{ marginTop: 14 }}>
                  <strong>🏆 {pf.certificates.length} certificate{pf.certificates.length > 1 ? 's' : ''}</strong>
                  {pf.certificates.map((c) => (
                    <div key={c.verification_code} className="p1x-muted" style={{ fontSize: 13 }}>
                      {c.title} · <code className="p1x-codechip" style={{ cursor: 'default' }}>{c.verification_code}</code>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {pf.projects.length > 0 && (
              <div className="p1x-card">
                <h2>Projects</h2>
                {pf.projects.map((p) => (
                  <div className="p1x-row" key={p.name}>
                    <div>
                      <div style={{ fontWeight: 600 }}>{p.name}</div>
                      <div className="p1x-muted" style={{ fontSize: 13 }}>{p.description}</div>
                      <div className="p1x-chips" style={{ marginTop: 6 }}>
                        {p.tech.map((t) => (
                          <span key={t} className="p1x-chip">{t}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {publishOpen && (
              <div className="p1x-overlay" onClick={() => setPublishOpen(false)}>
                <div className="p1x-panel" onClick={(e) => e.stopPropagation()}>
                  <button className="p1x-btn ghost sm close" onClick={() => setPublishOpen(false)}>✕ Close</button>
                  <h2>Publish karo</h2>
                  <p className="p1x-muted" style={{ fontSize: 14 }}>
                    Single-file HTML download karo — koi external asset nahi, seedha GitHub Pages par host hoga.
                  </p>
                  <button className="p1x-btn" disabled={busy} onClick={download} style={{ width: '100%', marginTop: 8 }}>
                    {busy ? 'Preparing…' : '⬇ Download portfolio.html'}
                  </button>
                  <div className="sec" style={{ marginTop: 18 }}>
                    <h4>MANUAL PAGES STEPS</h4>
                    <ul>
                      <li>GitHub par naya repo banao</li>
                      <li>Download ki hui file ko <b>index.html</b> naam se push karo</li>
                      <li>Repo Settings → Pages → ON karo</li>
                    </ul>
                  </div>
                  <p className="p1x-muted" style={{ fontSize: 13 }}>
                    GitHub par one-click publish jald aa raha hai — account linking ke baad. OAuth verification abhi available nahi hai.
                  </p>
                </div>
              </div>
            )}
          </>
        )
      )}
    </div>
  );
}
