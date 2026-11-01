import { useState } from 'react';
import type { FormEvent } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../lib/auth';
import { api, ApiError } from '../lib/api';
import { HexLogo } from '../components/layout/TopNav';
import PasswordField from '../components/PasswordField';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [googleBusy, setGoogleBusy] = useState(false);
  const [googleNote, setGoogleNote] = useState('');

  const googleLogin = async () => {
    setGoogleNote('');
    setGoogleBusy(true);
    try {
      // Existing backend endpoint: GET /api/v1/auth/google/login returns
      // { auth_url } when configured, 501 when OAuth credentials are absent.
      const res = await api<{ auth_url?: string }>('/api/v1/auth/google/login');
      if (res.auth_url) {
        window.location.href = res.auth_url;
        return;
      }
      setGoogleNote('Google sign-in is not available right now — please sign in with email below.');
    } catch (err) {
      if (err instanceof ApiError && err.status === 501) {
        // Graceful "not configured" state: no dead button, no silent failure.
        // OAuth credentials remain a pending user action; nothing is invented.
        setGoogleNote(
          'Google sign-in is not set up yet (Google OAuth credentials are still pending). Please sign in with email for now.',
        );
      } else {
        setGoogleNote('Could not start Google sign-in — please try again or sign in with email.');
      }
    } finally {
      setGoogleBusy(false);
    }
  };

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setBusy(true);
    try {
      await login(email, password);
      navigate('/');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Login failed');
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
        <h1>Welcome back</h1>
        <p className="sub">Sign in to continue building your career intelligence.</p>
        {error && <div className="auth-err">{error}</div>}
        <form onSubmit={submit}>
          <div className="field">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
            />
          </div>
          <PasswordField
            id="password"
            label="Password"
            value={password}
            onChange={setPassword}
            autoComplete="current-password"
          />
          <div className="auth-forgot">
            <Link to="/forgot-password">Forgot password?</Link>
          </div>
          <button className="btn-primary" type="submit" disabled={busy}>
            {busy ? 'Signing in…' : 'Sign in'}
          </button>
        </form>
        <button className="auth-google" type="button" onClick={googleLogin} disabled={googleBusy}>
          {googleBusy ? 'Connecting to Google…' : 'Continue with Google'}
        </button>
        {googleNote && <div className="auth-note" role="status">{googleNote}</div>}
        <div className="auth-alt">
          New here? <Link to="/register">Create an account</Link>
        </div>
      </div>
    </div>
  );
}
