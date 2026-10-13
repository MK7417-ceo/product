import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api, ApiError } from '../lib/api';

interface TierDetail {
  name: string;
  price_inr: number;
  features: string[];
}

interface SubscriptionData {
  subscription?: { tier?: string; name?: string; price_inr?: number };
  tiers?: Record<string, TierDetail>;
}

const ORDER = ['free', 'pro', 'expert'];

const TIER_BLURB: Record<string, string> = {
  free: 'Start your journey',
  pro: 'For serious builders',
  expert: 'Maximum velocity',
};

export default function Billing() {
  const [data, setData] = useState<SubscriptionData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let alive = true;
    api<SubscriptionData>('/api/v1/account/subscription')
      .then((d) => {
        if (alive) setData(d);
      })
      .catch((e) => {
        if (alive) setError(e instanceof ApiError ? e.message : 'Could not load billing info');
      })
      .finally(() => {
        if (alive) setLoading(false);
      });
    return () => {
      alive = false;
    };
  }, []);

  const current = data?.subscription?.tier ?? 'free';
  const tiers = data?.tiers ?? {};
  const ordered = ORDER.filter((t) => tiers[t]);

  return (
    <>
      <h1 className="page-title">Billing &amp; usage</h1>
      <p className="page-sub">Your current plan and what each tier unlocks.</p>

      {loading && (
        <div style={{ marginTop: 20 }}>
          <div className="skel" style={{ maxWidth: 640 }} />
          <div className="skel" style={{ maxWidth: 520 }} />
          <div className="skel" style={{ maxWidth: 580 }} />
        </div>
      )}

      {error && (
        <div className="notice warn" style={{ marginTop: 20, maxWidth: 640 }}>
          {error}
        </div>
      )}

      {!loading && !error && (
        <>
          <div className="tier-grid" style={{ maxWidth: 960 }}>
            {ordered.map((key) => {
              const t = tiers[key];
              const isCurrent = key === current;
              const isPopular = key === 'pro' && !isCurrent;
              return (
                <div
                  key={key}
                  className={`tier-card${isCurrent ? ' current' : ''}${isPopular ? ' popular' : ''}`}
                >
                  {isCurrent && <span className="tier-now">CURRENT</span>}
                  {isPopular && <span className="tier-flag">MOST POPULAR</span>}
                  <h3>{t.name}</h3>
                  {TIER_BLURB[key] && (
                    <div className="tier-desc">{TIER_BLURB[key]}</div>
                  )}
                  <div className="price">
                    ₹{t.price_inr}
                    <small>/month</small>
                  </div>
                  <ul>
                    {t.features.map((f) => (
                      <li key={f}>{f}</li>
                    ))}
                  </ul>
                </div>
              );
            })}
          </div>

          <div className="notice" style={{ maxWidth: 960 }}>
            Online payments are not connected yet — they need business KYC (Razorpay/Stripe).
            Tier upgrades are currently done manually by the team. No payment is collected here.
          </div>

          <div style={{ marginTop: 20 }}>
            <Link className="btn-primary" to="/subscription">
              {current === 'free' ? 'Upgrade plan' : 'Change plan'}
            </Link>
          </div>
        </>
      )}
    </>
  );
}
