import { useEffect, useState } from 'react';
import { certificatesApi, roadmapApi, ApiError, type Certificate, type CertificateVerifyResult, type Roadmap } from '../lib/p1api';
import './p1-pages.css';

export default function Certificates() {
  const [certs, setCerts] = useState<Certificate[]>([]);
  const [roadmap, setRoadmap] = useState<Roadmap | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [copied, setCopied] = useState('');
  const [code, setCode] = useState('');
  const [vres, setVres] = useState<CertificateVerifyResult | null>(null);
  const [verifyOpen, setVerifyOpen] = useState(false);

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
  const eligible = roadmap !== null && total > 0 && done === total;

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

  if (loading)
    return (
      <div className="p1x">
        <p className="p1x-loading">Loading certificates…</p>
      </div>
    );

  const pct = total ? Math.round((100 * done) / total) : 0;

  return (
    <div className="p1x">
      <div className="p1x-head">
        <div>
          <h1 className="p1x-title">Certificates</h1>
          <p className="p1x-sub">Mehnat ka saboot — sirf earn karne par milta hai, khud se nahi.</p>
        </div>
        <button className="p1x-btn ghost" onClick={() => setVerifyOpen(true)}>🔍 Verify a code</button>
      </div>
      {error && <div className="p1x-err">{error}</div>}

      <div className="p1x-card">
        <h2>Earn a certificate</h2>
        {roadmap ? (
          <div>
            <p className="p1x-muted" style={{ margin: '4px 0 10px', fontSize: 14 }}>
              {roadmap.title} — {done}/{total} tasks complete
            </p>
            <div className="p1x-bar" style={{ marginBottom: 14 }}>
              <i style={{ width: `${pct}%` }} />
            </div>
            <button className="p1x-btn" disabled={busy || !eligible} onClick={issue}>
              {busy ? 'Issuing…' : eligible ? 'Issue my certificate' : `Complete all ${total} tasks to unlock`}
            </button>
            {!eligible && total > 0 && (
              <p className="p1x-muted" style={{ fontSize: 13, marginTop: 10 }}>
                Certificates are issued only when every roadmap task is complete — each task needs submitted evidence.
              </p>
            )}
          </div>
        ) : (
          <p className="p1x-empty">Roadmap banao aur saare tasks complete karo — certificate yahan milega.</p>
        )}
      </div>

      <div className="p1x-card">
        <h2>Earned ({certs.length})</h2>
        {certs.length === 0 && <p className="p1x-empty">Abhi koi certificate nahi — upar se earn karo.</p>}
        {certs.map((c) => (
          <div className="p1x-row" key={c.id}>
            <div style={{ fontSize: 26 }}>🏆</div>
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 700, fontSize: 15 }}>{c.title}</div>
              <div className="p1x-muted" style={{ fontSize: 13 }}>
                {new Date(c.issued_at).toLocaleDateString()} · {c.detail}
              </div>
              <button className="p1x-codechip" onClick={() => copy(c.verification_code)} title="Copy code">
                {c.verification_code} {copied === c.verification_code ? '✓ copied' : '⧉ copy'}
              </button>
            </div>
          </div>
        ))}
      </div>

      {verifyOpen && (
        <div className="p1x-overlay" onClick={() => setVerifyOpen(false)}>
          <div className="p1x-panel" onClick={(e) => e.stopPropagation()}>
            <button className="p1x-btn ghost sm close" onClick={() => setVerifyOpen(false)}>✕ Close</button>
            <h2>Verify a certificate</h2>
            <p className="p1x-muted" style={{ fontSize: 13.5 }}>
              Employer koi bhi code yahan check kar sakta hai — login nahi chahiye.
            </p>
            <div style={{ display: 'flex', gap: 8, marginTop: 12 }}>
              <input
                className="p1x-input mono"
                style={{ textTransform: 'uppercase' }}
                placeholder="SF-XXXXXXXX"
                value={code}
                onChange={(e) => setCode(e.target.value)}
              />
              <button className="p1x-btn" disabled={busy || !code.trim()} onClick={verify}>Verify</button>
            </div>
            {vres && (
              <div
                className="p1x-card"
                style={{ marginTop: 14, borderColor: vres.valid ? 'rgba(57,217,138,.45)' : 'rgba(240,108,117,.45)' }}
              >
                {vres.valid ? (
                  <>
                    <span className="p1x-pill ok">✓ VALID</span>
                    <p style={{ fontWeight: 700, margin: '8px 0 4px' }}>{vres.title}</p>
                    <p className="p1x-muted" style={{ fontSize: 13, margin: 0 }}>
                      Issued to {vres.issued_to ?? '—'} on{' '}
                      {vres.issued_at && new Date(vres.issued_at).toLocaleDateString()}
                      {vres.detail ? ` · ${vres.detail}` : ''}
                    </p>
                  </>
                ) : (
                  <>
                    <span className="p1x-pill gap">✕ NOT FOUND</span>
                    <p className="p1x-muted" style={{ fontSize: 13.5, margin: '8px 0 0' }}>
                      Yeh code kisi certificate se match nahi karta.
                    </p>
                  </>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
