import { useEffect, useState } from 'react';
import { accountApi, ApiError, type TierInfo } from '../lib/api';

export default function Settings() {
  const [sub, setSub] = useState<TierInfo | null>(null);
  const [tiers, setTiers] = useState<Record<string, { name: string; price_inr: number; features: string[] }>>({});
  const [links, setLinks] = useState({ github: '', linkedin: '', leetcode: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const [s, l] = await Promise.all([accountApi.subscription(), accountApi.getLinks()]);
        setSub(s.subscription);
        setTiers(s.tiers);
        setLinks(l);
      } catch (err) {
        setError(err instanceof ApiError ? err.message : 'Load failed');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const upgrade = async (tier: string) => {
    setError('');
    setNotice('');
    setBusy(true);
    try {
      const r = await accountApi.checkout(tier);
      setNotice(r.message);
    } catch (err) {
      // 501 comes back as ApiError — surface its honest message
      setNotice(err instanceof ApiError ? err.message : 'Checkout failed');
    } finally {
      setBusy(false);
    }
  };

  const saveLinks = async () => {
    setError('');
    setNotice('');
    setBusy(true);
    try {
      await accountApi.saveLinks(links);
      setNotice('✓ Links saved — portfolio mein dikhenge.');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Save failed');
    } finally {
      setBusy(false);
    }
  };

  if (loading) return <p className="page-sub">Loading settings…</p>;

  return (
    <div>
      <h1 className="page-title">Settings</h1>
      <p className="page-sub">Subscription aur connected accounts.</p>
      {error && <p className="error">{error}</p>}
      {notice && <p className="notice">{notice}</p>}

      <div className="card">
        <h3 style={{ marginTop: 0 }}>Subscription</h3>
        <p className="muted" style={{ marginTop: 0 }}>
          Current plan: <strong style={{ color: '#7dd3fc' }}>{sub?.name}</strong>
        </p>
        <div className="tier-grid">
          {Object.entries(tiers).map(([key, t]) => (
            <div key={key} className={'tier' + (sub?.tier === key ? ' current' : '')}>
              <div className="tier-name">{t.name}</div>
              <div className="tier-price">{t.price_inr === 0 ? 'Free' : `₹${t.price_inr}/mo`}</div>
              <ul>
                {t.features.map((f) => <li key={f}>{f}</li>)}
              </ul>
              {sub?.tier === key ? (
                <span className="muted" style={{ fontSize: 13 }}>✓ Current plan</span>
              ) : (
                <button className="btn small" disabled={busy} onClick={() => upgrade(key)}>
                  Upgrade
                </button>
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <h3 style={{ marginTop: 0 }}>Connected accounts</h3>
        <p className="muted" style={{ fontSize: 13, marginTop: 0 }}>
          Usernames jodo — portfolio aur profile mein dikhenge. OAuth login P3f ke baad aayega.
        </p>
        {(['github', 'linkedin', 'leetcode'] as const).map((k) => (
          <div key={k} style={{ marginBottom: 8 }}>
            <label className="muted" style={{ fontSize: 12, textTransform: 'capitalize' }}>{k} username</label>
            <input
              className="rinput"
              value={links[k]}
              onChange={(e) => setLinks({ ...links, [k]: e.target.value })}
              placeholder={`${k} username`}
            />
          </div>
        ))}
        <button className="btn primary" disabled={busy} onClick={saveLinks} style={{ marginTop: 8 }}>
          {busy ? 'Saving…' : 'Save links'}
        </button>
      </div>

      <style>{`
        .notice { background: rgba(125, 211, 252, 0.08); border: 1px solid rgba(125, 211, 252, 0.3); color: #7dd3fc; padding: 10px 14px; border-radius: 10px; font-size: 14px; }
        .tier-grid { display: grid; gap: 12px; }
        @media (min-width: 700px) { .tier-grid { grid-template-columns: repeat(3, 1fr); } }
        .tier { background: #0d1117; border: 1px solid #232838; border-radius: 12px; padding: 16px; }
        .tier.current { border-color: #7dd3fc; }
        .tier-name { font-weight: 700; font-size: 16px; }
        .tier-price { color: #4ade80; font-weight: 700; margin: 4px 0 8px; }
        .tier ul { margin: 8px 0; padding-left: 18px; font-size: 13px; color: #c6cddb; }
        .tier li { margin: 4px 0; }
        .rinput { width: 100%; box-sizing: border-box; background: #0d1117; color: #e6e9f0; border: 1px solid #232838; border-radius: 8px; padding: 10px 12px; margin-top: 4px; font-size: 14px; }
      `}</style>
    </div>
  );
}
