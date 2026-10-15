import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../lib/auth';
import { api } from '../../lib/api';
import { markWelcomeSeen, welcomeSeen } from './lib';
import './onboarding.css';

/**
 * Route: /welcome — post-login resume nudge (Flow 1).
 * "Add your resume to unlock JD matching" → /resume.
 * "Skip for now" → /subscription. Skip is tracked in localStorage so the
 * nudge shows exactly once; returning visitors are sent to the dashboard.
 */
export default function Welcome() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    if (welcomeSeen()) {
      navigate('/', { replace: true });
      return;
    }
    // Resume already on file? Skip the nudge, continue the journey.
    api('/api/v1/launchpad/resume')
      .then(() => navigate('/subscription', { replace: true }))
      .catch(() => setChecking(false)); // 404 → no resume yet → show nudge
  }, [navigate]);

  const skip = () => {
    markWelcomeSeen();
    navigate('/subscription');
  };

  if (checking) {
    return (
      <div className="ob">
        <div className="ob-load">Getting your workspace ready…</div>
      </div>
    );
  }

  const name = user?.email?.split('@')[0] ?? 'there';

  return (
    <div className="ob">
      <div className="ob-kicker">WELCOME TO SKILLFORGE</div>
      <h1 className="ob-title">Hey {name} — let's set up your launchpad</h1>
      <p className="ob-sub">
        SkillForge matches your resume against real job descriptions and scores
        it like an ATS would — so you know exactly what's missing before you apply.
      </p>

      <div className="ob-card glow">
        <div className="ob-kicker">STEP 1 OF ONBOARDING</div>
        <h3 style={{ fontSize: 20 }}>Add your resume to unlock JD matching</h3>
        <p className="ob-hint" style={{ marginTop: 8, maxWidth: 560 }}>
          Paste any job description and get an instant ATS score (0–100): matched
          keywords, missing keywords, and concrete suggestions to close the gap.
        </p>
        <ul className="ob-sug">
          <li>ATS score against any pasted job description</li>
          <li>Missing-keyword prompts that guide your edits</li>
          <li>Guided builder — we ask for each missing detail inline</li>
        </ul>
        <div className="ob-cta-row">
          <button className="ob-btn" onClick={() => navigate('/resume')}>
            Add my resume →
          </button>
          <button className="ob-ghost" onClick={skip}>
            Skip for now
          </button>
        </div>
      </div>

      <p className="ob-empty">
        You can add your resume any time from the <b>Resume</b> section under Launch.
      </p>
    </div>
  );
}
