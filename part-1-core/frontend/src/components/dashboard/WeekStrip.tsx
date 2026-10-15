import type { TodayOut } from '../../lib/api-dashboard';
import { ErrBox, Load } from './ui';
import './dashboard.css';

interface Props {
  today: TodayOut | null;
  loading: boolean;
  error: string | null;
  onRetry: () => void;
}

const DAY_LABELS = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];

/** Monday of the week containing `date` (YYYY-MM-DD). Returns Date objects for M..S. */
function weekDays(dateStr: string): Date[] {
  const d = new Date(`${dateStr}T12:00:00Z`);
  const dow = (d.getUTCDay() + 6) % 7; // 0 = Monday
  const monday = new Date(d);
  monday.setUTCDate(d.getUTCDate() - dow);
  return Array.from({ length: 7 }, (_, i) => {
    const day = new Date(monday);
    day.setUTCDate(monday.getUTCDate() + i);
    return day;
  });
}

function sameDay(a: Date, b: Date): boolean {
  return a.getUTCFullYear() === b.getUTCFullYear() &&
    a.getUTCMonth() === b.getUTCMonth() &&
    a.getUTCDate() === b.getUTCDate();
}

export default function WeekStrip({ today, loading, error, onRetry }: Props) {
  if (loading) return <Load label="this week" />;
  if (error) return <ErrBox message={error} onRetry={onRetry} />;
  if (!today) {
    return (
      <section className="sf-card" aria-label="This week">
        <h3>This week</h3>
        <div className="sf-hint">Daily practice, mock, evidence activity.</div>
        <div className="sf-empty">Weekly activity is unavailable right now.</div>
      </section>
    );
  }

  const days = weekDays(today.date);
  const todayDate = new Date(`${today.date}T12:00:00Z`);

  return (
    <section className="sf-card" aria-label="This week">
      <h3>This week</h3>
      <div className="sf-hint">Daily practice, mock, evidence activity.</div>
      <div className="sf-week">
        {days.map((day, i) => (
          <div key={i} className={`sf-day${sameDay(day, todayDate) ? ' sf-today' : ''}`}>
            {DAY_LABELS[i]}
            <i />
          </div>
        ))}
      </div>
      <div className="sf-week-foot">
        Today: <b>{today.questions.length} questions</b> · <b>{today.tasks.length} tasks</b>
        {today.has_roadmap ? '' : ' · no roadmap yet'}
      </div>
    </section>
  );
}
