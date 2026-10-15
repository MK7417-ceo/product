import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../lib/auth';
import { api, ApiError } from '../lib/api';

interface SubscriptionInfo {
  subscription?: { tier?: string; name?: string; price_inr?: number };
}

export default function Profile() {
  const { user } = useAuth();
  const [tier, setTier] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let alive = true;
    api<SubscriptionInfo>('/api/v1/account/subscription')
      .then((d) => {
        if (alive) setTier(d.subscription?.tier ?? null);
      })
      .catch((e) => {
        if (alive) setError(e instanceof ApiError ? e.message : 'Could not load plan info');
      })
      .finally(() => {
        if (alive) setLoading(false);
      });
    return () => {
      alive = false;
    };
  }, []);

  const joined = user?.created_at ? new Date(user.created_at).toLocaleDateString() : '—';

  return (
    <>
      <h1 className="page-title">Profile</h1>
      <p className="page-sub">Your account details.</p>

      <div className="card" style={{ marginTop: 20, maxWidth: 640 }}>
        <dl className="kv">
          <dt>Email</dt>
          <dd>{user?.email ?? '—'}</dd>
          <dt>Role</dt>
          <dd>{user?.role ?? '—'}</dd>
          <dt>Member since</dt>
          <dd>{joined}</dd>
          <dt>Plan</dt>
          <dd>
            {loading ? (
              <span className="empty">Loading…</span>
            ) : tier ? (
              <span style={{ textTransform: 'capitalize', fontWeight: 700 }}>{tier}</span>
            ) : (
              <span className="empty">Unknown</span>
            )}
          </dd>
        </dl>
        {error && (
          <div className="notice warn" style={{ marginTop: 16 }}>
            {error}
          </div>
        )}
        <div style={{ marginTop: 20, display: 'flex', gap: 12 }}>
          <Link className="btn-ghost" to="/settings">
            Open settings
          </Link>
        </div>
      </div>
    </>
  );
}
