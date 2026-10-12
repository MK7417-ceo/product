import { Link } from 'react-router-dom';
import type { AssessmentSummary, RoadmapOut, RoadmapTask, TodayOut } from '../../lib/api-dashboard';
import { Dot } from './ui';
import './dashboard.css';

interface Props {
  roadmap: RoadmapOut | null;
  assessments: AssessmentSummary[];
  today: TodayOut | null;
  loading: boolean;
}

/** Top actionable task: in_progress first, then pending, highest priority first. */
export function topActionableTask(roadmap: RoadmapOut): RoadmapTask | null {
  const rank: Record<string, number> = { high: 0, medium: 1, low: 2 };
  const open = roadmap.tasks.filter((t) => t.status === 'in_progress' || t.status === 'pending');
  open.sort((a, b) => {
    const aProg = a.status === 'in_progress' ? 0 : 1;
    const bProg = b.status === 'in_progress' ? 0 : 1;
    if (aProg !== bProg) return aProg - bProg;
    return (rank[a.priority] ?? 3) - (rank[b.priority] ?? 3);
  });
  return open[0] ?? null;
}

export default function StatCards({ roadmap, assessments, today, loading }: Props) {
  /* ---- Verified readiness: aggregate server-scored assessments ---- */
  const completed = assessments.filter((a) => a.status === 'completed' && a.total > 0);
  const vCorrect = completed.reduce((s, a) => s + a.correct, 0);
  const vTotal = completed.reduce((s, a) => s + a.total, 0);
  const verifiedPct = vTotal > 0 ? Math.round((vCorrect / vTotal) * 100) : null;

  /* ---- Top skill gap: highest-priority open roadmap task's target skill,
         else the weakest verified assessment topic ---- */
  let gapValue: string;
  let gapSub: string;
  if (roadmap) {
    const top = topActionableTask(roadmap);
    const skill = top?.target_skills?.[0];
    if (skill) {
      gapValue = skill;
      gapSub = `${top!.priority} priority · closes in your roadmap`;
    } else {
      gapValue = 'No open gaps';
      gapSub = 'all roadmap tasks complete';
    }
  } else if (completed.length > 0) {
    const worst = [...completed].sort((a, b) => a.correct / a.total - b.correct / b.total)[0];
    const pct = Math.round((worst.correct / worst.total) * 100);
    gapValue = worst.topic;
    gapSub = `${pct}% verified · weakest area`;
  } else {
    gapValue = 'Find out';
    gapSub = 'Complete the diagnostic to find your gaps →';
  }

  /* ---- Roadmap progress ---- */
  const counts = roadmap?.task_counts ?? null;

  /* ---- Practice: today's served questions (the backend has no streak
         tracking yet, so the card shows today's real activity) ---- */
  const qCount = today ? today.questions.length : null;

  const card = (to: string, label: string, value: React.ReactNode, sub: React.ReactNode) => (
    <Link className="sf-stat" to={to} key={label}>
      <div className="sf-lb">{label}</div>
      <div className="sf-v">{loading ? '…' : value}</div>
      <div className="sf-sub">{sub}</div>
    </Link>
  );

  return (
    <section className="sf-stats" aria-label="Key stats">
      {card(
        '/skills',
        'VERIFIED READINESS',
        verifiedPct === null && !loading ? (
          <span style={{ fontSize: 20 }}>Not yet</span>
        ) : (
          <>
            {verifiedPct ?? '…' }<span className="sf-unit">%</span>
          </>
        ),
        verifiedPct === null && !loading ? (
          <>Take the diagnostic to get a verified score →</>
        ) : (
          <>
            <Dot color={verifiedPct !== null && verifiedPct >= 70 ? '#39d98a' : '#f5b84b'} />
            {completed.length} verified assessment{completed.length === 1 ? '' : 's'}
          </>
        ),
      )}
      {card(
        '/skills',
        'TOP SKILL GAP',
        loading ? '…' : <span style={{ fontSize: gapValue.length > 14 ? 18 : 24 }}>{gapValue}</span>,
        <>
          <Dot color="#f06c75" />
          {gapSub}
        </>,
      )}
      {card(
        '/roadmap',
        'ROADMAP PROGRESS',
        counts ? (
          <>
            {counts.completed}
            <span className="sf-unit">/{counts.total}</span>
          </>
        ) : (
          !loading && <span style={{ fontSize: 20 }}>No plan</span>
        ),
        counts ? (
          <>
            <Dot color="#36c5f0" />
            {counts.in_progress} in progress
          </>
        ) : (
          !loading && <>Generate your roadmap from your gaps →</>
        ),
      )}
      {card(
        '/practice',
        'PRACTICE STREAK',
        qCount === null && !loading ? (
          <span style={{ fontSize: 20 }}>Unavailable</span>
        ) : (
          <>
            {qCount ?? '…'}
            <span className="sf-unit"> today</span>
          </>
        ),
        qCount === null && !loading ? (
          <>Couldn&apos;t reach the backend — retry from Practice</>
        ) : (
          <>
            <Dot color="#f5b84b" />
            daily questions served · open practice
          </>
        ),
      )}
    </section>
  );
}
