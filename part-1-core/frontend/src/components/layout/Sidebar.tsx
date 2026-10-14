import { useEffect, useState } from 'react';
import { NavLink } from 'react-router-dom';
import { api } from '../../lib/api';

interface NavItem {
  to: string;
  label: string;
  icon: string;
  badge?: boolean;
}

const GROUPS: { title: string; items: NavItem[] }[] = [
  { title: 'HOME', items: [{ to: '/', label: 'Dashboard', icon: '🏠' }] },
  {
    title: 'DEVELOP',
    items: [
      { to: '/plan', label: 'Assessment', icon: '🎯' },
      { to: '/roadmap', label: 'Roadmap', icon: '🗺️', badge: true },
      { to: '/practice', label: 'Practice', icon: '📝' },
      { to: '/codelab', label: 'Code Lab', icon: '💻' },
    ],
  },
  {
    title: 'PROVE',
    items: [
      { to: '/skills', label: 'Skill Profile', icon: '📊' },
      { to: '/gaps', label: 'Skill Gaps', icon: '🧩' },
      { to: '/evidence', label: 'Evidence', icon: '🛡️' },
      { to: '/certificates', label: 'Certificates', icon: '🏆' },
    ],
  },
  {
    title: 'LAUNCH',
    items: [
      { to: '/resume', label: 'Resume', icon: '📄' },
      { to: '/portfolio', label: 'Portfolio', icon: '🌐' },
      { to: '/interview', label: 'Interview Prep', icon: '🎤' },
      { to: '/placement-prep', label: 'Placement Prep', icon: '🎯' },
    ],
  },
  {
    title: 'EXPLORE',
    items: [
      { to: '/news', label: 'Tech News', icon: '📰' },
      { to: '/coins', label: 'Coin Shop', icon: '🪙' },
    ],
  },
];

export default function Sidebar() {
  const [openTasks, setOpenTasks] = useState<number | null>(null);

  // Roadmap count badge: open tasks (pending + in_progress) from the
  // current roadmap. Hidden while loading, on error, or when zero.
  useEffect(() => {
    let alive = true;
    api<{ task_counts?: { pending?: number; in_progress?: number } }>('/api/v1/roadmaps/current')
      .then((data) => {
        if (!alive) return;
        const c = data.task_counts;
        setOpenTasks(c ? (c.pending ?? 0) + (c.in_progress ?? 0) : null);
      })
      .catch(() => {
        if (alive) setOpenTasks(null);
      });
    return () => {
      alive = false;
    };
  }, []);

  return (
    <aside className="sidebar">
      {GROUPS.map((g) => (
        <div key={g.title}>
          <div className="sgroup">{g.title}</div>
          {g.items.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) => (isActive ? 'slink active' : 'slink')}
            >
              <span className="ic" aria-hidden>
                {item.icon}
              </span>
              {item.label}
              {item.badge && openTasks != null && openTasks > 0 && (
                <span className="cnt">{openTasks}</span>
              )}
            </NavLink>
          ))}
        </div>
      ))}
    </aside>
  );
}
