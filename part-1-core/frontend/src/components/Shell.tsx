import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../lib/auth';

const LINKS = [
  { to: '/', label: 'Dashboard' },
  { to: '/assessment', label: 'Assessment' },
  { to: '/gaps', label: 'Skill Gaps' },
  { to: '/roadmap', label: 'Roadmap' },
  { to: '/practice', label: 'Practice' },
  { to: '/code', label: 'Code Runner' },
  { to: '/portfolio', label: 'Portfolio' },
];

export default function Shell() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const onLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="logo">
          SKILL<span>FORGE</span>
        </div>
        <div className="brand-sub">Career Intelligence</div>
        <nav className="nav">
          {LINKS.map((l) => (
            <NavLink key={l.to} to={l.to} end={l.to === '/'} className={({ isActive }) => (isActive ? 'active' : '')}>
              <span className="dot" />
              {l.label}
            </NavLink>
          ))}
        </nav>
        <div className="side-user">
          <div className="nm">{user?.email ?? '—'}</div>
          <div className="lv">🎯 {user?.role ?? 'member'}</div>
          <button onClick={onLogout}>Sign out</button>
        </div>
      </aside>
      <main className="main">
        <Outlet />
      </main>
    </div>
  );
}
