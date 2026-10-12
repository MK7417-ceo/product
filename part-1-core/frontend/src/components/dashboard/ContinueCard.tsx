import { useNavigate } from 'react-router-dom';
import type { RoadmapOut } from '../../lib/api-dashboard';
import { ErrBox, Load } from './ui';
import { topActionableTask } from './StatCards';
import './dashboard.css';

interface Props {
  roadmap: RoadmapOut | null;
  loading: boolean;
  error: string | null;
  onRetry: () => void;
}

export default function ContinueCard({ roadmap, loading, error, onRetry }: Props) {
  const navigate = useNavigate();

  if (loading) return <Load label="continue where you left off" />;
  if (error) return <ErrBox message={error} onRetry={onRetry} />;

  const task = roadmap ? topActionableTask(roadmap) : null;
  if (!task) {
    return (
      <section className="sf-card" aria-label="Continue where you left off">
        <h3>Continue where you left off</h3>
        <div className="sf-hint">One task. Clear done-state. No decisions needed.</div>
        <div className="sf-empty">
          <div>No roadmap yet — your next task will appear here.</div>
          <div className="sf-cta">
            <button className="sf-btn-primary" onClick={() => navigate('/roadmap')}>
              Create your plan →
            </button>
          </div>
        </div>
      </section>
    );
  }

  const prioClass =
    task.priority === 'high' ? 'sf-prio-high' : task.priority === 'medium' ? 'sf-prio-medium' : 'sf-prio-low';

  return (
    <section className="sf-card" aria-label="Continue where you left off">
      <h3>Continue where you left off</h3>
      <div className="sf-hint">One task. Clear done-state. No decisions needed.</div>
      <div className="sf-task">
        <div className="sf-n">{roadmap!.tasks.findIndex((t) => t.id === task.id) + 1}</div>
        <div className="sf-tbody">
          <b>{task.title}</b>
          <p>{task.why_it_matters || task.description}</p>
          <div className="sf-meta">
            <span>⏱ {task.effort_minutes} min</span>
            {task.expected_evidence && <span>🎯 {task.expected_evidence}</span>}
            <span className={prioClass}>{task.priority.toUpperCase()}</span>
          </div>
        </div>
        <button className="sf-btn-sm" onClick={() => navigate('/roadmap')}>
          {task.status === 'in_progress' ? 'Resume →' : 'Start →'}
        </button>
      </div>
    </section>
  );
}
