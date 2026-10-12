import { NavLink } from 'react-router-dom';

/* Mobile bottom tabs (visible ≤900px; sidebar is hidden there). */
const TABS = [
  { to: '/', label: 'Home', icon: '🏠' },
  { to: '/plan', label: 'Develop', icon: '🎯' },
  { to: '/skills', label: 'Prove', icon: '🛡️' },
  { to: '/resume', label: 'Launch', icon: '🚀' },
];

export default function BottomNav() {
  return (
    <nav className="mnav" aria-label="Mobile navigation">
      {TABS.map((t) => (
        <NavLink
          key={t.to}
          to={t.to}
          end={t.to === '/'}
          className={({ isActive }) => (isActive ? 'active' : '')}
        >
          <span aria-hidden>{t.icon}</span>
          {t.label}
        </NavLink>
      ))}
    </nav>
  );
}
