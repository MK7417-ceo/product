import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import type { AssessmentSummary, ProfileOut, RoadmapOut } from '../../lib/api-dashboard';
import { ErrBox, Load } from './ui';
import './dashboard.css';

interface Props {
  profile: ProfileOut | null;
  assessments: AssessmentSummary[];
  roadmap: RoadmapOut | null;
  loading: boolean;
  error: string | null;
  onRetry: () => void;
}

export default function HeroCard({ profile, assessments, roadmap, loading, error, onRetry }: Props) {
  const navigate = useNavigate();
  const [showScoring, setShowScoring] = useState(false);

  if (loading) return <Load label="diagnostic readiness" />;
  if (error) return <ErrBox message={error} onRetry={onRetry} />;

  /* ---- Roadmap exists: hero becomes roadmap progress ---- */
  if (roadmap) {
    const { total, completed } = roadmap.task_counts;
    const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
    const open = total - completed;
    return (
      <section className="sf-hero" aria-label="Roadmap progress">
        <div className="sf-kicker">ROADMAP IN PROGRESS</div>
        <h2>{roadmap.title || 'Your learning roadmap'}</h2>
        <p>
          {total} tasks mapped to your skill gaps — {completed} complete
          {open > 0 ? `, ${open} to go` : '. All done — take today\u2019s practice to stay sharp'}.
        </p>
        <div className="sf-progress">
          <div className="sf-plbl">
            <span>{completed} of {total} tasks complete</span>
            <span>{pct}%</span>
          </div>
          <div className="sf-bar">
            <i style={{ width: `${pct}%` }} />
          </div>
        </div>
        <div className="sf-cta-row">
          <button className="sf-btn-primary" onClick={() => navigate('/roadmap')}>
            {open > 0 ? 'Continue roadmap →' : 'Review roadmap →'}
          </button>
          <button className="sf-btn-ghost" onClick={() => navigate('/practice')}>
            Today&apos;s practice
          </button>
        </div>
      </section>
    );
  }

  /* ---- No roadmap: diagnostic readiness ---- */
  const hasProfile = profile !== null;
  const diagnosticDone = assessments.some((a) => a.status === 'completed');
  const steps = [
    { label: 'Profile created', done: hasProfile },
    { label: 'Diagnostic completed', done: diagnosticDone },
    { label: 'Roadmap generated', done: false },
  ];
  const doneCount = steps.filter((s) => s.done).length;
  const pct = Math.round((doneCount / steps.length) * 100);

  return (
    <section className="sf-hero" aria-label="Diagnostic readiness">
      <div className="sf-kicker">DIAGNOSTIC READINESS</div>
      <h2>Measure your real level in 15 minutes</h2>
      <p>
        No self-report. Server-scored questions across Python and DSA — your
        measured level decides what you learn next.
      </p>
      <div className="sf-steps">
        {steps.map((s) => (
          <span key={s.label} className={`sf-step${s.done ? ' done' : ''}`}>
            <span className="sf-ck">{s.done ? '✓' : '·'}</span>
            {s.label}
          </span>
        ))}
      </div>
      <div className="sf-progress">
        <div className="sf-plbl">
          <span>{doneCount} of {steps.length} steps complete</span>
          <span>{pct}%</span>
        </div>
        <div className="sf-bar">
          <i style={{ width: `${pct}%` }} />
        </div>
      </div>
      <div className="sf-cta-row">
        <button className="sf-btn-primary" onClick={() => navigate('/plan')}>
          Start 15-min diagnostic →
        </button>
        <button className="sf-btn-ghost" onClick={() => setShowScoring(true)}>
          How scoring works
        </button>
      </div>
      {showScoring && (
        <div className="sf-modal-backdrop" onClick={() => setShowScoring(false)}>
          <div
            className="sf-modal"
            role="dialog"
            aria-modal="true"
            aria-label="How scoring works"
            onClick={(e) => e.stopPropagation()}
          >
            <h3>How scoring works</h3>
            <ul className="sf-modal-list">
              <li><strong>No self-report.</strong> Your level is measured by server-scored questions — never by what you claim.</li>
              <li><strong>4 questions per level.</strong> The diagnostic samples 4 random questions from each level, beginner upward.</li>
              <li><strong>70% to pass a level.</strong> Your verified level is the highest level you pass with all lower levels also passing.</li>
              <li><strong>Your roadmap follows your gaps.</strong> The topics you miss become the tasks in your personalized roadmap.</li>
            </ul>
            <button className="sf-btn-primary" onClick={() => setShowScoring(false)}>
              Got it
            </button>
          </div>
        </div>
      )}
    </section>
  );
}
