import { useNavigate } from 'react-router-dom';
import type { TodayOut } from '../../lib/api-dashboard';
import { ErrBox, Load } from './ui';
import './dashboard.css';

interface Props {
  today: TodayOut | null;
  loading: boolean;
  error: string | null;
  onRetry: () => void;
}

function statusPill(status: string): string {
  if (status === 'in_progress') return 'sf-pill sf-inprogress';
  if (status === 'completed') return 'sf-pill sf-completed';
  return 'sf-pill sf-pending';
}

export default function TodayRail({ today, loading, error, onRetry }: Props) {
  const navigate = useNavigate();

  let body: React.ReactNode;
  if (loading) {
    body = <Load label="today's tasks" />;
  } else if (error) {
    body = <ErrBox message={error} onRetry={onRetry} />;
  } else if (!today || today.tasks.length === 0) {
    body = (
      <div className="sf-empty">
        <div>
          {today && !today.has_roadmap
            ? 'No roadmap yet — your daily tasks appear once you generate one.'
            : 'Nothing scheduled for today.'}
        </div>
        <div className="sf-cta">
          <button className="sf-btn-sm" onClick={() => navigate(today?.has_roadmap ? '/practice' : '/roadmap')}>
            {today?.has_roadmap ? 'Open practice →' : 'Create your plan →'}
          </button>
        </div>
      </div>
    );
  } else {
    body = (
      <>
        <div className="sf-today-list">
          {today.tasks.map((t) => (
            <div className="sf-today-item" key={t.id}>
              <div className="sf-tb">
                <b>{t.title}</b>
                <div className="sf-tm">
                  <span>⏱ {t.effort_minutes} min</span>
                  <span className={statusPill(t.status)}>{t.status.replace('_', ' ').toUpperCase()}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
        <div className="sf-cta-row" style={{ marginTop: 14 }}>
          <button className="sf-btn-sm" onClick={() => navigate('/practice')}>
            Open practice →
          </button>
        </div>
      </>
    );
  }

  return (
    <aside className="sf-rail" aria-label="Right rail">
      <section className="sf-card">
        <h3>Today&apos;s tasks</h3>
        <div className="sf-hint">
          {today ? `Top priorities for ${today.date}.` : 'Your daily focus list.'}
        </div>
        {body}
      </section>

      <section className="sf-card" aria-label="Daily DSA">
        <h3>Daily DSA</h3>
        <div className="sf-hint">One focused data-structure or algorithms problem a day.</div>
        {/* DSA-SLOT: coordinator wires <DailyDSACard/> from src/components/dsa/DailyDSACard.tsx here */}
      </section>
    </aside>
  );
}
