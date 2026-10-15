import { useState } from 'react';
import type { FormEvent } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { api, ApiError } from '../lib/api';
import { HexLogo } from '../components/layout/TopNav';

/**
 * Route: /reset-password?token=… — set a new password from a reset link.
 *
 * UI-first: posts to POST /api/v1/auth/reset-password (backend wiring
 * pending — needs the email-provider decision). A missing/expired token
 * shows a clear message instead of a broken form.
 */
export default function ResetPassword() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const token = params.get('token') ?? '';

  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(false);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    if (password.length < 8) {
      setError('Password must be at least 8 characters.');
      return;
    }
    if (password !== confirm) {
      setError('Passwords do not match.');
      return;
    }
    setBusy(true);
    try {
      await api('/api/v1/auth/reset-password', {
        method: 'POST',
        body: JSON.stringify({ token, new_password: password }),
      });
      setDone(true);
      setTimeout(() => navigate('/login'), 2500);
    } catch (err) {
      setError(
        err instanceof ApiError
          ? err.message
          : 'Could not reset your password. The link may have expired.',
      );
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="auth-wrap">
      <div className="auth-card">
        <div className="auth-logo">
          <HexLogo size={30} />
          <div>
            SKILLFORGE
            <small>CAREER INTELLIGENCE</small>
          </div>
        </div>
        {done ? (
          <>
            <h1>Password updated</h1>
            <p className="sub">
              Your password has been reset. Taking you back to sign in…
            </p>
            <div className="auth-alt">
              <Link to="/login">Sign in now</Link>
            </div>
          </>
        ) : !token ? (
          <>
            <h1>Link expired or invalid</h1>
            <p className="sub">
              This reset link is missing or has expired. Request a fresh one
              and try again.
            </p>
            <Link to="/forgot-password" className="btn-primary" style={{ width: '100%' }}>
              Request a new link
            </Link>
            <div className="auth-alt">
              <Link to="/login">Back to sign in</Link>
            </div>
          </>
        ) : (
          <>
            <h1>Choose a new password</h1>
            <p className="sub">Make it at least 8 characters.</p>
            {error && <div className="auth-err">{error}</div>}
            <form onSubmit={submit}>
              <div className="field">
                <label htmlFor="rp-pass">New password</label>
                <input
                  id="rp-pass"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  autoComplete="new-password"
                  minLength={8}
                />
              </div>
              <div className="field">
                <label htmlFor="rp-confirm">Confirm new password</label>
                <input
                  id="rp-confirm"
                  type="password"
                  value={confirm}
                  onChange={(e) => setConfirm(e.target.value)}
                  required
                  autoComplete="new-password"
                  minLength={8}
                />
              </div>
              <button className="btn-primary" type="submit" disabled={busy}>
                {busy ? 'Updating…' : 'Update password'}
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
}
