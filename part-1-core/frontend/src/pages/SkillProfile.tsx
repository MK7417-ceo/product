import { useEffect, useState } from 'react';
import { assessmentApi, profileApi, ApiError, type AssessmentSession, type ProfileData } from '../lib/p1api';
import './p1-pages.css';

const VERIFY_BAR = 70;

interface TopicSkill {
  topic: string;
  level: string;
  pct: number;
  correct: number;
  total: number;
  state: 'verified' | 'gap';
}

export default function SkillProfile() {
  const [skills, setSkills] = useState<TopicSkill[]>([]);
  const [claimed, setClaimed] = useState<string[]>([]);
  const [history, setHistory] = useState<AssessmentSession[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const [list, profile] = await Promise.all([
          assessmentApi.list(),
          profileApi.me().catch((e) => {
            if (e instanceof ApiError && e.status === 404) return null;
            throw e;
          }),
        ]);
        const sessions = list.assessments;
        setHistory([...sessions].reverse());

        // latest session per topic decides the measured state
        const latest = new Map<string, AssessmentSession>();
        for (const s of sessions) {
          if (s.status === 'completed' && s.total > 0) latest.set(s.topic, s);
        }
        const rows: TopicSkill[] = [...latest.values()].map((s) => {
          const pct = Math.round((100 * s.correct) / s.total);
          return {
            topic: s.topic,
            level: s.level,
            pct,
            correct: s.correct,
            total: s.total,
            state: pct >= VERIFY_BAR ? 'verified' : 'gap',
          };
        });
        rows.sort((a, b) => b.pct - a.pct);
        setSkills(rows);

        const assessed = new Set(rows.map((r) => r.topic));
        if (profile) {
          const p = profile as ProfileData;
          setClaimed(p.current_skills.filter((s) => !assessed.has(s)));
        }
      } catch (err) {
        setError(err instanceof ApiError ? err.message : 'Load failed');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading)
    return (
      <div className="p1x">
        <p className="p1x-loading">Loading skill profile…</p>
      </div>
    );

  const verified = skills.filter((s) => s.state === 'verified').length;
  const gaps = skills.filter((s) => s.state === 'gap').length;

  return (
    <div className="p1x">
      <div className="p1x-head">
        <div>
          <h1 className="p1x-title">Skill Profile</h1>
          <p className="p1x-sub">
            Measured by server-scored assessments — never by self-report alone.
          </p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <span className="p1x-pill ok">✓ VERIFIED · {verified}</span>
          <span className="p1x-pill gap">GAP · {gaps}</span>
        </div>
      </div>
      {error && <div className="p1x-err">{error}</div>}

      <div className="p1x-card">
        <h2>Measured skills</h2>
        <p className="hint">
          Latest assessment per topic. Green means verified (≥{VERIFY_BAR}%) — green is used only for verified evidence.
        </p>
        {skills.length === 0 && <p className="p1x-empty">No completed assessments yet — take an assessment to get measured.</p>}
        {skills.map((s) => (
          <div className="p1x-skill" key={s.topic}>
            <div className="srow">
              <b>{s.topic}</b>
              <span className={`p1x-pill ${s.state === 'verified' ? 'ok' : 'gap'}`}>
                {s.state === 'verified' ? `✓ VERIFIED · ${s.pct}%` : `GAP · ${s.pct}%`}
              </span>
            </div>
            <div className="p1x-sbar">
              <i
                style={{
                  width: `${Math.max(s.pct, 4)}%`,
                  background: s.state === 'verified' ? 'var(--green)' : 'var(--red)',
                }}
              />
            </div>
            <div className="p1x-muted" style={{ fontSize: 12, marginTop: 4 }}>
              {s.correct}/{s.total} correct · level {s.level}
            </div>
          </div>
        ))}
      </div>

      <div className="p1x-card">
        <h2>Self-claimed — unverified</h2>
        <p className="hint">From your onboarding profile. Shown separately — they never count as verified skill.</p>
        {claimed.length === 0 ? (
          <p className="p1x-empty">Nothing self-claimed beyond measured skills.</p>
        ) : (
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {claimed.map((s) => (
              <span key={s} className="p1x-pill claim">SELF-CLAIMED · {s}</span>
            ))}
          </div>
        )}
      </div>

      <div className="p1x-card">
        <h2>Assessment history</h2>
        <p className="hint">Every scored session, newest first.</p>
        {history.length === 0 && <p className="p1x-empty">No sessions yet.</p>}
        {history.map((s) => (
          <div className="p1x-row" key={s.assessment_id}>
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 600, fontSize: 14 }}>{s.topic} <span className="p1x-muted">· {s.level}</span></div>
              <div className="p1x-muted" style={{ fontSize: 12.5 }}>
                {s.status === 'completed' ? `${s.correct}/${s.total} correct` : s.status}
              </div>
            </div>
            {s.status === 'completed' && s.total > 0 && (
              <span className={`p1x-pill ${Math.round((100 * s.correct) / s.total) >= VERIFY_BAR ? 'ok' : 'gap'}`}>
                {Math.round((100 * s.correct) / s.total)}%
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
