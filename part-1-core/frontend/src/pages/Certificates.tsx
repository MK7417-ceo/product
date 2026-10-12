import { useEffect, useState } from 'react';
import { certificatesApi, roadmapApi, ApiError, type Certificate, type Roadmap } from '../lib/api';

export default function Certificates() {
  const [certs, setCerts] = useState<Certificate[]>([]);
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [copied, setCopied] = useState('');
  // verify box
  const [code, setCode] = useState('');
  const [vres, setVres] = useState<{ valid: boolean; title?: string; issued_to?: string; issued_at?: string } | null>(null);

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const [c, r] = await Promise.all([
        certificatesApi.list(),
        roadmapApi.current().catch((e) => {
          if (e instanceof ApiError && e.status === 400) return null;
          throw e;
        }),
      ]);
      setCerts(c);
      setRoadmap(r);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Load failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const done = roadmap ? roadmap.tasks.filter((t) => t.status === 'completed').length : 0;
  const total = roadmap ? roadmap.tasks.length : 0;
  const eligible = roadmap && total > 0 && done === total;

  const issue = async () => {
    if (!roadmap || busy) return;
    setError('');
    setBusy(true);
    try {
      await certificatesApi.issue('roadmap', roadmap.id);
      await load();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Issue failed');
    } finally {
      setBusy(false);
    }
  };

  const copy = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(text);
      setTimeout(() => setCopied(''), 1500);
    } catch {
      /* clipboard unavailable */
    }
  };

  const verify = async () => {
    if (!code.trim() || busy) return;
    setError('');
    setBusy(true);
    setVres(null);
    try {
      setVres(await certificatesApi.verify(code.trim().toUpperCase()));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Verify failed');
    } finally {
      setBusy(false);
    }
  };

  if (loading) return <p className="page-sub">Loading certificates…</p>;

  return (
    <div>
      <h1 className="page-title">Certificates</h1>
      <p className="page-sub">Mehnat ka saboot — sirf earn karne par milta hai, khud se nahi.</p>
      {error && <p className="error">{error}</p>}

      {/* earn */}
      <div className="card">
        <h3 style={{ marginTop: 0 }}>Earn a certificate</h3>
        {roadmap ? (
          <div>
            <p className="muted" style={{ margin: '4px 0 10px' }}>
              {roadmap.title} — {done}/{total} tasks complete
            </p>
            <div className="pbar">
              <div className="pfill" style={{ width: total ? `${(100 * done) / total}%` : '0%' }} />
            </div>
            <button className="btn primary" disabled={busy || !eligible} onClick={issue} style={{ marginTop: 12 }}>
              {busy ? 'Issuing…' : eligible ? 'Issue my certificate' : `Complete all ${total} tasks to unlock`}
            </button>
          </div>
        ) : (
          <p className="muted" style={{ margin: 0 }}>Roadmap banao aur saare tasks complete karo — certificate yahan milega.</p>
        )}
      </div>

      {/* earned */}
      <div className="card">
        <h3 style={{ marginTop: 0 }}>Earned ({certs.length})</h3>
        {certs.length === 0 && <p className="muted" style={{ margin: 0 }}>Abhi koi certificate nahi — upar se earn karo.</p>}
        {certs.map((c) => (
          <div key={c.id} className="cert-row">
            <div className="cert-badge">🏆</div>
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 700 }}>{c.title}</div>
              <div className="muted" style={{ fontSize: 13 }}>
                {new Date(c.issued_at).toLocaleDateString()} · {c.detail}
              </div>
              <button className="code-chip" onClick={() => copy(c.verification_code)} title="Copy code">
                {c.verification_code} {copied === c.verification_code ? '✓' : '⧉'}
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* public verify */}
      <div className="card">
        <h3 style={{ marginTop: 0 }}>Verify a certificate</h3>
        <p className="muted" style={{ marginTop: 0, fontSize: 13 }}>Employer koi bhi code yahan check kar sakta hai — login nahi chahiye.</p>
        <div style={{ display: 'flex', gap: 8 }}>
          <input
            className="rinput"
            style={{ margin: 0, fontFamily: 'monospace', textTransform: 'uppercase' }}
            placeholder="SF-XXXXXXXX"
            value={code}
            onChange={(e) => setCode(e.target.value)}
          />
          <button className="btn" disabled={busy || !code.trim()} onClick={verify}>Verify</button>
        </div>
        {vres && (
          <div className={'vres' + (vres.valid ? ' ok' : ' bad')}>
            {vres.valid ? (
              <><strong>✓ Valid</strong> — {vres.title}<br />
                <span className="muted" style={{ fontSize: 13 }}>Issued to {vres.issued_to} on {vres.issued_at && new Date(vres.issued_at).toLocaleDateString()}</span></>
            ) : (
              <><strong>✕ Not found</strong> — yeh code kisi certificate se match nahi karta.</>
            )}
          </div>
        )}
      </div>

      <style>{`
        .pbar { height: 8px; background: #0d1117; border-radius: 4px; overflow: hidden; }
        .pfill { height: 100%; background: linear-gradient(90deg, #7dd3fc, #4ade80); transition: width 0.4s; }
        .cert-row { display: flex; gap: 12px; align-items: flex-start; padding: 12px 0; border-top: 1px solid #232838; }
        .cert-row:first-of-type { border-top: none; }
        .cert-badge { font-size: 26px; }
        .code-chip { margin-top: 6px; font-family: monospace; background: #0d1117; border: 1px dashed #7dd3fc; color: #7dd3fc; border-radius: 8px; padding: 4px 10px; cursor: pointer; font-size: 13px; }
        .rinput { width: 100%; box-sizing: border-box; background: #0d1117; color: #e6e9f0; border: 1px solid #232838; border-radius: 8px; padding: 10px 12px; font-size: 14px; }
        .vres { margin-top: 12px; padding: 12px; border-radius: 10px; border: 1px solid #232838; font-size: 14px; }
        .vres.ok { border-color: rgba(74, 222, 128, 0.4); }
        .vres.bad { border-color: rgba(248, 113, 113, 0.4); }
      `}</style>
    </div>
  );
}
