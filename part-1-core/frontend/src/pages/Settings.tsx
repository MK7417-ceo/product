import { useEffect, useState } from 'react';
import { accountApi, ApiError, type TierInfo, type AccountLinks } from '../lib/p1api';
import './p1-pages.css';

const EMPTY_LINKS: AccountLinks = { github: '', linkedin: '', leetcode: '' };

export default function Settings() {
  const [sub, setSub] = useState<TierInfo | null>(null);
  const [tiers, setTiers] = useState<Record<string, { name: string; price_inr: number; features: string[] }>>({});
  const [links, setLinks] = useState<AccountLinks>(EMPTY_LINKS);
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
      const saved = await accountApi.saveLinks(links);
      setLinks(saved);
      setNotice('✓ Links saved — portfolio mein dikhenge.');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Save failed');
    } finally {
      setBusy(false);
    }
  };

  if (loading)
    return (
      <div className="p1x">
        <p className="p1x-loading">Loading settings…</p>
      </div>
    );

  return (
    <div className="p1x">
      <div className="p1x-head">
        <div>
          <h1 className="p1x-title">Settings</h1>
          <p className="p1x-sub">Subscription aur connected accounts.</p>
        </div>
      </div>
      {error && <div className="p1x-err">{error}</div>}
      {notice && <div className="p1x-notice">{notice}</div>}

      <div className="p1x-card">
        <h2>Subscription</h2>
        <p className="hint">
          Current plan: <strong style={{ color: 'var(--cyan)' }}>{sub?.name ?? '—'}</strong>
        </p>
        <div className="p1x-grid3">
          {Object.entries(tiers).map(([key, t]) => (
            <div key={key} className={`p1x-tier ${sub?.tier === key ? 'current' : ''}`}>
              <div className="tname">{t.name}</div>
              <div className="tprice">{t.price_inr === 0 ? 'Free' : `₹${t.price_inr}/mo`}</div>
              <ul>
                {t.features.map((f) => (
                  <li key={f}>{f}</li>
                ))}
              </ul>
              {sub?.tier === key ? (
                <span className="p1x-muted" style={{ fontSize: 13 }}>✓ Current plan</span>
              ) : (
                <button className="p1x-btn sm" disabled={busy} onClick={() => upgrade(key)}>
                  Upgrade
                </button>
              )}
            </div>
          ))}
        </div>
        <p className="p1x-muted" style={{ fontSize: 13, marginTop: 12, marginBottom: 0 }}>
          Online payments abhi connected nahi hain — Razorpay/Stripe ke liye business KYC chahiye. Tab tak upgrades team manually karti hai.
        </p>
      </div>

      <div className="p1x-card">
        <h2>Integrations</h2>
        <p className="hint">
          GitHub / LinkedIn / LeetCode usernames jodo — portfolio aur profile mein dikhenge. Ye usernames hain, verified OAuth connections nahi.
        </p>
        {(['github', 'linkedin', 'leetcode'] as const).map((k) => (
          <div className="p1x-field" key={k}>
            <label style={{ textTransform: 'capitalize' }}>
              {k} username{' '}
              <span className={`p1x-pill ${links[k] ? 'info' : 'claim'}`} style={{ marginLeft: 6 }}>
                {links[k] ? 'LINKED' : 'NOT LINKED'}
              </span>
            </label>
            <input
              value={links[k]}
              onChange={(e) => setLinks({ ...links, [k]: e.target.value })}
              placeholder={`${k} username`}
            />
          </div>
        ))}
        <button className="p1x-btn" disabled={busy} onClick={saveLinks} style={{ marginTop: 4 }}>
          {busy ? 'Saving…' : 'Save links'}
        </button>
        <div className="sec" style={{ marginTop: 18 }}>
          <h4 style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.1em', color: 'var(--muted)', margin: '0 0 6px' }}>
            COMING SOON — HONEST STATUS
          </h4>
          <ul style={{ margin: 0, paddingLeft: 18, color: 'var(--muted)', fontSize: 13.5 }}>
            <li>Google OAuth login — backend endpoints coded hain, credentials configure hone tak 501.</li>
            <li>GitHub/LinkedIn OAuth verification — abhi sirf username save hota hai, ownership verify nahi hota.</li>
            <li>GitHub one-click portfolio publish — abhi manual Pages steps (Portfolio page mein).</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
