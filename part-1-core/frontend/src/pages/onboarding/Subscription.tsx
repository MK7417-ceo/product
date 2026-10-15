import { useEffect, useState } from 'react';
import { api, ApiError } from '../../lib/api';
import {
  clearDemoPlan, fmtINR, getDemoPlan, setDemoPlan,
  type DemoPlan, type SubscriptionInfo, type TierInfo,
} from './lib';
import './onboarding.css';

/**
 * Route: /subscription — Free / Pro / Expert (Flow 1, step M).
 * Prices + feature lists come from the backend billing matrix — never
 * hardcoded. Checkout returns 501 until Razorpay/Stripe KYC is done, so we
 * show an HONEST "coming soon" state and never fake a payment.
 */
interface SubResponse {
  subscription: SubscriptionInfo;
  tiers: Record<string, TierInfo>;
}

const ORDER = ['free', 'pro', 'expert'] as const;

export default function Subscription() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [tiers, setTiers] = useState<Record<string, TierInfo> | null>(null);
  const [backendTier, setBackendTier] = useState('free');
  const [demoPlan, setDemoPlanState] = useState<DemoPlan | null>(getDemoPlan());
  const [checkoutMsg, setCheckoutMsg] = useState('');
  const [busyTier, setBusyTier] = useState<string | null>(null);

  useEffect(() => {
    api<SubResponse>('/api/v1/account/subscription')
      .then((r) => {
        setTiers(r.tiers);
        setBackendTier(r.subscription.tier);
      })
      .catch((e) => setError(e instanceof Error ? e.message : 'Could not load plans'))
      .finally(() => setLoading(false));
  }, []);

  const currentTier = demoPlan ?? backendTier;

  const upgrade = async (tier: string) => {
    setBusyTier(tier);
    setCheckoutMsg('');
    try {
      await api('/api/v1/account/subscription/checkout', {
        method: 'POST',
        body: JSON.stringify({ tier }),
      });
      // The backend never succeeds today — but if it ever does, say so plainly.
      setCheckoutMsg('Checkout completed — your plan is now active.');
    } catch (e) {
      if (e instanceof ApiError && e.status === 501) {
        setCheckoutMsg(
          'Checkout coming soon — online payments aren\u2019t connected yet. ' +
          'They need business KYC (Razorpay/Stripe) first, so tier upgrades are ' +
          'currently done manually by the team. We\u2019ll notify you the moment ' +
          'it\u2019s live — we will never charge you without a real checkout.',
        );
      } else {
        setCheckoutMsg(e instanceof Error ? `Checkout failed: ${e.message}` : 'Checkout failed');
      }
    } finally {
      setBusyTier(null);
    }
  };

  const simulate = (p: DemoPlan | null) => {
    if (p) setDemoPlan(p); else clearDemoPlan();
    setDemoPlanState(getDemoPlan());
  };

  if (loading) {
    return <div className="ob"><div className="ob-load">Loading plans…</div></div>;
  }
  if (error || !tiers) {
    return (
      <div className="ob">
        <h1 className="ob-title">Subscription</h1>
        <div className="ob-alert err">{error || 'Plans unavailable'}</div>
      </div>
    );
  }

  return (
    <div className="ob">
      <div className="ob-kicker">SUBSCRIPTION</div>
      <h1 className="ob-title">Pick the plan that fits your grind</h1>
      <p className="ob-sub">
        Start free. Upgrade when you want unlimited roadmaps, certificates and
        interview prep. Current plan:{' '}
        <b style={{ textTransform: 'uppercase' }}>{tiers[currentTier]?.name ?? currentTier}</b>
        {demoPlan && <span style={{ color: 'var(--amber)' }}> (demo override)</span>}
      </p>

      <div className="ob-plans">
        {ORDER.map((key) => {
          const t = tiers[key];
          if (!t) return null;
          const isCurrent = key === currentTier;
          const price = key === 'free' ? 'Free' : fmtINR(t.price_inr);
          return (
            <div key={key} className={`ob-plan ${key === 'pro' ? 'hl' : ''} ${isCurrent ? 'current' : ''}`}>
              {isCurrent && <span className="cur-tag">CURRENT</span>}
              <div className="pname">{t.name}</div>
              <div className="price">
                {price}
                {key !== 'free' && <small> /month</small>}
              </div>
              <ul>
                {t.features.map((f) => <li key={f}>{f}</li>)}
              </ul>
              {isCurrent ? (
                <button className="ob-ghost" disabled style={{ width: '100%' }}>
                  Your plan
                </button>
              ) : key === 'free' ? (
                <button className="ob-ghost" style={{ width: '100%' }} onClick={() => simulate(null)}>
                  Downgrade to Free
                </button>
              ) : (
                <button
                  className="ob-btn-sm"
                  style={{ width: '100%', padding: '12px' }}
                  onClick={() => upgrade(key)}
                  disabled={busyTier !== null}
                >
                  {busyTier === key ? 'Contacting checkout…' : `Upgrade · ${fmtINR(t.price_inr)}/mo`}
                </button>
              )}
            </div>
          );
        })}
      </div>

      {checkoutMsg && (
        <div className="ob-alert info" style={{ marginTop: 18 }}>{checkoutMsg}</div>
      )}

      {/* DEMO SCAFFOLDING — delete this block when real checkout lands. */}
      <div className="ob-demo">
        <div className="tag">DEMO ONLY — REMOVE WHEN REAL CHECKOUT LANDS</div>
        <p>
          The Milestone-1 demo has no payment gateway, so this control <b>simulates</b> a
          purchase. It sets <code>localStorage['sf_plan']</code>, which the shell reads:
          the “Go Pro” popup disappears and a <b>PRO</b>/<b>EXPERT</b> badge appears on
          the account. Nothing is charged; the backend tier is untouched.
        </p>
        <div className="ob-cta-row" style={{ marginTop: 0 }}>
          <button className="ob-btn-sm" onClick={() => simulate('pro')}>Simulate Pro purchase</button>
          <button className="ob-btn-sm" onClick={() => simulate('expert')}>Simulate Expert purchase</button>
          <button className="ob-ghost" onClick={() => simulate(null)}>Reset to Free</button>
        </div>
      </div>
    </div>
  );
}
