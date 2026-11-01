import type { RoadmapTask } from '../lib/p1api';
import './RoadmapJourney.css';

/* Roadmap rendered as a navigation journey — Google Maps style.
   A vertical route connects waypoints: visited (green ✓), current
   position (pulsing accent "YOU ARE HERE"), and upcoming stops (numbered).
   Tapping a waypoint opens its details. */

const PRI_CLASS: Record<string, string> = {
  high: 'warn', medium: 'info', low: 'claim',
};

interface Props {
  tasks: RoadmapTask[];
  onSelect: (t: RoadmapTask) => void;
}

export default function RoadmapJourney({ tasks, onSelect }: Props) {
  const completed = tasks.filter((t) => t.status === 'completed').length;
  const totalMin = tasks.reduce((s, t) => s + (t.effort_minutes || 0), 0);
  const pct = tasks.length ? Math.round((100 * completed) / tasks.length) : 0;

  // Current position: first in_progress, else first pending
  const currentIdx = (() => {
    const ip = tasks.findIndex((t) => t.status === 'in_progress');
    if (ip >= 0) return ip;
    return tasks.findIndex((t) => t.status !== 'completed');
  })();

  return (
    <div className="rj">
      <div className="rj-summary">
        <div className="rj-summary-route">
          <span className="rj-pin">📍</span>
          <div>
            <b>Your learning route</b>
            <span>
              {tasks.length} stops · {totalMin} min total · {completed} visited
            </span>
          </div>
        </div>
        <div className="rj-progress">
          <div className="rj-bar"><i style={{ width: `${pct}%` }} /></div>
          <span>{pct}%</span>
        </div>
      </div>

      <div className="rj-route">
        {tasks.map((t, i) => {
          const done = t.status === 'completed';
          const current = i === currentIdx;
          return (
            <div key={t.id} className={`rj-stop${done ? ' done' : ''}${current ? ' current' : ''}`}>
              <div className="rj-rail">
                <button
                  className="rj-marker"
                  onClick={() => onSelect(t)}
                  aria-label={`${done ? 'Visited' : current ? 'Current position' : `Stop ${i + 1}`}: ${t.title}`}
                >
                  {done ? '✓' : current ? '' : i + 1}
                </button>
                {i < tasks.length - 1 && <span className="rj-line" />}
              </div>
              <button className="rj-card" onClick={() => onSelect(t)}>
                {current && !done && <span className="rj-you">YOU ARE HERE</span>}
                <div className="rj-title">{t.title}</div>
                {t.why_it_matters && <div className="rj-why">{t.why_it_matters}</div>}
                <div className="rj-meta">
                  {t.effort_minutes > 0 && <span>⏱ {t.effort_minutes} min</span>}
                  {t.target_skills?.length > 0 && <span>🎯 {t.target_skills.slice(0, 3).join(', ')}</span>}
                </div>
                <div className="rj-tags">
                  <span className={`p1x-pill ${PRI_CLASS[t.priority] ?? 'claim'}`}>
                    {t.priority.toUpperCase()}
                  </span>
                  <span className={`p1x-pill ${done ? 'ok' : current ? 'info' : 'claim'}`}>
                    {done ? 'VISITED' : current ? 'NAVIGATING' : t.status.replace('_', ' ').toUpperCase()}
                  </span>
                </div>
              </button>
            </div>
          );
        })}
      </div>

      {tasks.length > 0 && (
        <div className="rj-destination">
          <span className="rj-pin">🏁</span>
          <span>Destination: job-ready engineer. Completed work is never lost — the route adapts, history stays.</span>
        </div>
      )}
    </div>
  );
}
