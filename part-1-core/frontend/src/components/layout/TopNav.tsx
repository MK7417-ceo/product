import { useEffect, useRef, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../lib/auth';
import { PLAN_EVENT, readLocalPlan, resolvePlan, type Plan } from '../../lib/plan';
import SearchBar from '../SearchBar';

/* Breadcrumb label per route. TopNav carries zero page links — the sidebar
   owns navigation; the crumb is wayfinding only. */
export const CRUMBS: Record<string, string> = {
  '/': 'Dashboard',
  '/welcome': 'Welcome',
  '/resume': 'Resume',
  '/subscription': 'Subscription',
  '/plan': 'Assessment',
  '/verification': 'Verification',
  '/roadmap': 'Roadmap',
  '/practice': 'Practice',
  '/codelab': 'Code Lab',
  '/skills': 'Skill Profile',
  '/gaps': 'Skill Gaps',
  '/evidence': 'Evidence',
  '/certificates': 'Certificates',
  '/portfolio': 'Portfolio',
  '/interview': 'Interview Prep',
  '/english': 'English',
  '/settings': 'Settings',
  '/profile': 'Profile',
  '/billing': 'Billing',
  /* P1-6: these pages previously fell through to the 'Dashboard' fallback
     even though their sidebar highlight and page title were correct. */
  '/learn': 'Learn',
  '/daily-plan': 'Daily Plan',
  '/admin/content': 'Content Manager',
  '/simulator': 'Placement Simulator',
  '/news': 'Tech News',
  '/weekly-test': 'Weekly Test',
  '/skill-gaps': 'Skill Gaps',
};

export function HexLogo({ size = 28 }: { size?: number }) {
  return (
    <svg viewBox="0 0 32 32" fill="none" width={size} height={size} aria-hidden>
      <path d="M16 2l12 7v14l-12 7-12-7V9l12-7z" stroke="#E85D26" strokeWidth="2.5" />
      <path d="M11 16l4 4 7-8" stroke="#E85D26" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export default function TopNav() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [plan, setPlan] = useState<Plan | null>(null);
  const [popupOpen, setPopupOpen] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [notifOpen, setNotifOpen] = useState(false);
  const wrapRef = useRef<HTMLDivElement>(null);
  const proWrapRef = useRef<HTMLDivElement>(null);
  const notifWrapRef = useRef<HTMLDivElement>(null);

  // Plan resolution: localStorage demo purchase first, then the real
  // backend tier. Re-run when the plan changes (purchase) or on reload.
  useEffect(() => {
    let alive = true;
    resolvePlan().then((r) => {
      if (alive) setPlan(r.plan);
    });
    const onChange = () => setPlan(readLocalPlan() ?? 'free');
    window.addEventListener(PLAN_EVENT, onChange as EventListener);
    return () => {
      alive = false;
      window.removeEventListener(PLAN_EVENT, onChange as EventListener);
    };
  }, []);

  // Close dropdown / popup on outside click or Escape.
  useEffect(() => {
    const onClick = (e: MouseEvent) => {
      if (wrapRef.current && !wrapRef.current.contains(e.target as Node)) setMenuOpen(false);
      if (proWrapRef.current && !proWrapRef.current.contains(e.target as Node)) setPopupOpen(false);
      if (notifWrapRef.current && !notifWrapRef.current.contains(e.target as Node)) setNotifOpen(false);
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setMenuOpen(false);
        setPopupOpen(false);
        setNotifOpen(false);
      }
    };
    document.addEventListener('mousedown', onClick);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('mousedown', onClick);
      document.removeEventListener('keydown', onKey);
    };
  }, []);

  const onLogout = async () => {
    await logout();
    navigate('/login');
  };

  const initial = (user?.email?.[0] ?? '?').toUpperCase();
  const subscribed = plan === 'pro' || plan === 'expert';
  const crumbLabel =
    CRUMBS[location.pathname] ??
    (location.pathname.startsWith('/learn/') ? 'Learn' : 'Dashboard');

  return (
    <nav className="topnav">
      <div className="topnav-in">
        <Link className="brand" to="/" aria-label="SkillForge home">
          <HexLogo />
          <div>
            SKILLFORGE
            <small>CAREER INTELLIGENCE</small>
          </div>
        </Link>

        <div className="crumb" aria-label="Breadcrumb">
          <Link to="/">Home</Link>
          <span className="sep">/</span>
          <span className="cur">{crumbLabel}</span>
        </div>

        {/* Centered global search — live results across your roadmaps, tasks, evidence… */}
        <div className="topnav-search">
          <SearchBar />
        </div>

        <div className="topnav-right">
          {/* Streak pill intentionally omitted: the practice API exposes no
              streak data (GET /api/v1/practice/today returns date, questions,
              tasks only). We never show a fabricated number. */}

          {!subscribed && (
            <div className="pro-wrap" ref={proWrapRef}>
              <button
                className="pro-btn"
                onClick={() => setPopupOpen((v) => !v)}
                aria-expanded={popupOpen}
                aria-haspopup="dialog"
              >
                ✨ Go Pro
              </button>
              {popupOpen && (
                <div className="pro-popup" role="dialog" aria-label="SkillForge Pro benefits">
                  <div className="tag">LIMITED OFFER</div>
                  <b>Unlock SkillForge Pro</b>
                  <ul>
                    <li>Unlimited roadmaps</li>
                    <li>Certificates + verification</li>
                    <li>Portfolio + interview prep</li>
                  </ul>
                  <button
                    className="btn-primary"
                    style={{ width: '100%', padding: '11px' }}
                    onClick={() => {
                      setPopupOpen(false);
                      navigate('/subscription');
                    }}
                  >
                    Upgrade · ₹299/mo
                  </button>
                  <button className="later" onClick={() => setPopupOpen(false)}>
                    later
                  </button>
                </div>
              )}
            </div>
          )}

          <div className="notif-wrap" ref={notifWrapRef} style={{ position: 'relative' }}>
            <button
              className="iconbtn"
              aria-label="Notifications"
              aria-expanded={notifOpen}
              aria-haspopup="dialog"
              title="Notifications"
              onClick={() => setNotifOpen((v) => !v)}
            >
              🔔
            </button>
            {notifOpen && (
              <div
                className="notif-popup"
                role="dialog"
                aria-label="Notifications"
                style={{
                  position: 'absolute', right: 0, top: 'calc(100% + 10px)', width: 280,
                  background: 'var(--surface)', border: '1px solid var(--border)',
                  borderRadius: 14, padding: 18, boxShadow: '0 18px 44px rgba(0,0,0,0.5)',
                  zIndex: 60,
                }}
              >
                <b style={{ fontSize: 14 }}>Notifications</b>
                <p style={{ fontSize: 13, color: 'var(--muted)', margin: '8px 0 0' }}>
                  Nothing here yet. We&apos;ll notify you about weekly tests, streak reminders, and placement drives.
                </p>
              </div>
            )}
          </div>

          {subscribed && (
            <span className="plan-badge" title={`SkillForge ${plan === 'pro' ? 'Pro' : 'Expert'} plan`}>
              {plan === 'pro' ? 'PRO' : 'EXPERT'}
            </span>
          )}

          <div className="avatar-wrap" ref={wrapRef}>
            <button className="avatar" onClick={() => setMenuOpen((v) => !v)} aria-expanded={menuOpen} aria-label="Account menu">
              {initial}
            </button>
            {menuOpen && (
              <div className="dropdown" role="menu">
                <div className="who">
                  <small>Signed in as</small>
                  <b>{user?.email ?? '—'}</b>
                </div>
                <Link to="/profile" onClick={() => setMenuOpen(false)} role="menuitem">
                  <span className="ic">👤</span>Your profile
                </Link>
                <Link to="/settings" onClick={() => setMenuOpen(false)} role="menuitem">
                  <span className="ic">⚙️</span>Settings
                </Link>
                {!subscribed && (
                  <Link to="/subscription" className="upgrade" onClick={() => setMenuOpen(false)} role="menuitem">
                    <span className="ic">✨</span>Upgrade to Pro
                  </Link>
                )}
                <Link to="/billing" onClick={() => setMenuOpen(false)} role="menuitem">
                  <span className="ic">💳</span>Billing &amp; usage
                </Link>
                <Link to="/settings#integrations" onClick={() => setMenuOpen(false)} role="menuitem">
                  <span className="ic">🔗</span>Integrations
                </Link>
                <hr />
                <button onClick={onLogout} role="menuitem">
                  <span className="ic">🚪</span>Sign out
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
