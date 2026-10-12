import { useAuth } from '../lib/auth';

export default function Dashboard() {
  const { user } = useAuth();

  return (
    <div>
      <h1 className="page-title">Namaste{user ? `, ${user.email.split('@')[0]}` : ''} 👋</h1>
      <p className="page-sub">
        Your career intelligence at a glance. More sections light up as you complete assessments and roadmaps.
      </p>

      <div className="grid4">
        <div className="card stat">
          <div className="lb">Account</div>
          <div className="vl" style={{ fontSize: 18, wordBreak: 'break-all' }}>
            {user?.email ?? '—'}
          </div>
          <div className="lb" style={{ marginTop: 8 }}>role: {user?.role ?? '—'}</div>
        </div>
        <div className="card stat">
          <div className="lb">Assessments</div>
          <div className="vl">—</div>
          <div className="lb" style={{ marginTop: 8 }}>take your first test</div>
        </div>
        <div className="card stat">
          <div className="lb">Skill gaps</div>
          <div className="vl">—</div>
          <div className="lb" style={{ marginTop: 8 }}>appear after assessment</div>
        </div>
        <div className="card stat">
          <div className="lb">Roadmap</div>
          <div className="vl">—</div>
          <div className="lb" style={{ marginTop: 8 }}>unlocks after gaps</div>
        </div>
      </div>

      <div className="card">
        <h3 style={{ fontSize: 15, marginBottom: 10 }}>How this works</h3>
        <p className="coming" style={{ marginTop: 0, lineHeight: 1.8 }}>
          1. Take an assessment → 2. We verify your real skill level and find gaps →
          3. You get a personalized roadmap → 4. Complete tasks, submit evidence →
          5. Watch your readiness grow. Skill levels come from verified tests, never
          from self-report alone.
        </p>
      </div>
    </div>
  );
}
