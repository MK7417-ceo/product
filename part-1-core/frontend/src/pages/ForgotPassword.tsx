import { useState } from 'react';
import type { FormEvent } from 'react';
import { Link } from 'react-router-dom';
import { api, ApiError } from '../lib/api';
import { HexLogo } from '../components/layout/TopNav';

/**
 * Route: /forgot-password — request a password reset link.
 *
 * UI-first: posts to POST /api/v1/auth/forgot-password (backend wiring
 * pending — needs the email-provider decision). Until then the submit
 * surfaces the backend's answer honestly instead of pretending.
 */
export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [sent, setSent] = useState(false);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setBusy(true);
    try {
      await api('/api/v1/auth/forgot-password', {
        method: 'POST',
        body: JSON.stringify({ email }),
      });
      setSent(true);
    } catch (err) {
      setError(
        err instanceof ApiError
          ? err.message
          : 'Could not send the reset link. Please try again.',
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
        {sent ? (
          <>
            <h1>Check your inbox</h1>
            <p className="sub">
              If an account exists for <b>{email}</b>, a password reset link
              is on its way. It expires in 30 minutes.
            </p>
            <div className="auth-alt">
              <Link to="/login">Back to sign in</Link>
            </div>
          </>
        ) : (
          <>
            <h1>Reset your password</h1>
            <p className="sub">
              Enter the email you signed up with and we'll send you a reset link.
            </p>
            {error && <div className="auth-err">{error}</div>}
            <form onSubmit={submit}>
              <div className="field">
                <label htmlFor="fp-email">Email</label>
                <input
                  id="fp-email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  autoComplete="email"
                  placeholder="you@example.com"
                />
              </div>
              <button className="btn-primary" type="submit" disabled={busy}>
                {busy ? 'Sending…' : 'Send reset link'}
              </button>
            </form>
            <div className="auth-alt">
              Remembered it? <Link to="/login">Back to sign in</Link>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
