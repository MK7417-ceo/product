import { useCallback, useEffect, useMemo, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { api, ApiError } from '../lib/api';

/* ---------- Types ---------- */

interface AssessmentSummary {
  assessment_id: string;
  topic: string;
  level: string;
  status: string;
  correct: number;
  total: number;
  gaps: string[];
}

interface PerSkill {
  skill: string;
  correct: number;
  total: number;
}

interface AssessmentDetail extends AssessmentSummary {
  per_skill: PerSkill[];
}

interface GapSource {
  assessment_id: string;
  topic: string;
  level: string;
}

interface SkillGap {
  skill: string;
  correct: number;
  total: number;
  ratio: number; // 0..1, worst observed
  sources: GapSource[];
}

interface Roadmap {
  id: string;
  version: number;
}

type LoadState = 'loading' | 'ready' | 'error';

/* ---------- Helpers ---------- */

function severityOf(ratio: number): 'high' | 'medium' {
  return ratio < 0.4 ? 'high' : 'medium';
}

const SEV_STYLE: Record<'high' | 'medium', { bg: string; fg: string; bd: string; label: string }> = {
  high: {
    bg: 'rgba(240,108,117,.14)',
    fg: 'var(--red)',
    bd: 'rgba(240,108,117,.35)',
    label: 'HIGH · <40%',
  },
  medium: {
    bg: 'rgba(245,184,75,.14)',
    fg: 'var(--amber)',
    bd: 'rgba(245,184,75,.35)',
    label: 'MEDIUM · 40–70%',
  },
};

/* ---------- Component ---------- */

export default function SkillGaps() {
  const navigate = useNavigate();
  const [state, setState] = useState<LoadState>('loading');
  const [error, setError] = useState('');
  const [assessments, setAssessments] = useState<AssessmentDetail[]>([]);
  const [openPanel, setOpenPanel] = useState<string | null>(null);
  const [roadmapBusy, setRoadmapBusy] = useState<string | null>(null); // skill being added
  const [roadmapMsg, setRoadmapMsg] = useState<{ skill: string; text: string } | null>(null);

  const load = useCallback(async () => {
    setState('loading');
    setError('');
    try {
      const list = await api<{ assessments: AssessmentSummary[] }>('/api/v1/assessments');
      const completed = list.assessments.filter((a) => a.status === 'completed');
      const details: AssessmentDetail[] = await Promise.all(
        completed.map((a) =>
          api<AssessmentDetail>(`/api/v1/assessments/${a.assessment_id}`).catch(
            () => ({ ...a, per_skill: [] as PerSkill[] }),
          ),
        ),
      );
      setAssessments(details);
      setState('ready');
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load assessments.');
      setState('error');
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const gaps: SkillGap[] = useMemo(() => {
    const bySkill = new Map<string, SkillGap>();
    for (const a of assessments) {
      for (const ps of a.per_skill) {
        const ratio = ps.total > 0 ? ps.correct / ps.total : 0;
        if (ratio >= 0.7) continue; // not a gap by backend definition
        const existing = bySkill.get(ps.skill);
        const source: GapSource = { assessment_id: a.assessment_id, topic: a.topic, level: a.level };
        if (!existing) {
          bySkill.set(ps.skill, {
            skill: ps.skill,
            correct: ps.correct,
            total: ps.total,
            ratio,
            sources: [source],
          });
        } else {
          if (!existing.sources.some((s) => s.assessment_id === a.assessment_id)) {
            existing.sources.push(source);
          }
          if (ratio < existing.ratio) {
            // worst ratio wins across assessments
            existing.correct = ps.correct;
            existing.total = ps.total;
            existing.ratio = ratio;
          }
        }
      }
    }
    return [...bySkill.values()].sort((x, y) => x.ratio - y.ratio);
  }, [assessments]);

  const addToRoadmap = useCallback(async (gap: SkillGap) => {
    setRoadmapBusy(gap.skill);
    setRoadmapMsg(null);
    try {
      const mastery_pct = Math.round(gap.ratio * 100);
      const payload = { gaps: [{ skill: gap.skill.slice(0, 80), mastery_pct }] };
      let current: Roadmap | null = null;
      try {
        current = await api<Roadmap>('/api/v1/roadmaps/current');
      } catch (e) {
        if (!(e instanceof ApiError) || (e.status !== 400 && e.status !== 404)) throw e;
        // no roadmap yet → generate below
      }
      const rm = current
        ? await api<Roadmap>('/api/v1/roadmaps/regenerate', {
            method: 'POST',
            body: JSON.stringify(payload),
          })
        : await api<Roadmap>('/api/v1/roadmaps/generate', {
            method: 'POST',
            body: JSON.stringify(payload),
          });
      setRoadmapMsg({ skill: gap.skill, text: `✓ Roadmap v${rm.version} ready — "${gap.skill}" queued` });
    } catch (e) {
      setRoadmapMsg({
        skill: gap.skill,
        text: `✗ Couldn't update roadmap: ${e instanceof Error ? e.message : 'unknown error'}`,
      });
    } finally {
      setRoadmapBusy(null);
    }
  }, []);

  /* ---------- States ---------- */

  if (state === 'loading') {
    return (
      <div>
        <h1 className="page-title">Skill Gaps</h1>
        <p className="page-sub">Verified weaknesses from your completed assessments.</p>
        <div className="card">
          <p className="coming" style={{ marginTop: 0 }}>
            Analyzing your assessment results…
          </p>
        </div>
      </div>
    );
  }

  if (state === 'error') {
    return (
      <div>
        <h1 className="page-title">Skill Gaps</h1>
        <p className="page-sub">Verified weaknesses from your completed assessments.</p>
        <div className="card">
          <p style={{ color: 'var(--red)', fontSize: 14, margin: 0 }}>
            Couldn't load your assessments: {error}
          </p>
          <button className="btn" style={{ marginTop: 14 }} onClick={() => void load()}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (gaps.length === 0) {
    return (
      <div>
        <h1 className="page-title">Skill Gaps</h1>
        <p className="page-sub">Verified weaknesses from your completed assessments.</p>
        <div className="card" style={{ textAlign: 'center', padding: '48px 24px' }}>
          <div style={{ fontSize: 44, marginBottom: 12 }}>🛰️</div>
          <h3 style={{ fontSize: 17, margin: '0 0 8px' }}>No skill gaps found</h3>
          <p style={{ color: 'var(--muted)', fontSize: 14, margin: '0 0 20px' }}>
            Take an assessment to discover yours — gaps come from server-scored tests,
            never from self-report.
          </p>
          <Link to="/plan" className="btn" style={{ textDecoration: 'none', display: 'inline-block' }}>
            Take an assessment to discover yours →
          </Link>
        </div>
      </div>
    );
  }

  const highCount = gaps.filter((g) => severityOf(g.ratio) === 'high').length;

  return (
    <div>
      <h1 className="page-title">Skill Gaps</h1>
      <p className="page-sub">
        Every gap below was measured by a server-scored assessment. Worst ratio wins when a
        skill gaps in multiple tests.
      </p>

      <div className="grid4">
        <div className="card stat">
          <div className="lb">Total gaps</div>
          <div className="vl" style={{ color: 'var(--red)' }}>{gaps.length}</div>
          <div className="lb" style={{ marginTop: 8 }}>below 70% mastery</div>
        </div>
        <div className="card stat">
          <div className="lb">High severity</div>
          <div className="vl" style={{ color: highCount ? 'var(--red)' : 'var(--green)' }}>
            {highCount}
          </div>
          <div className="lb" style={{ marginTop: 8 }}>under 40% mastery</div>
        </div>
        <div className="card stat">
          <div className="lb">Assessments</div>
          <div className="vl">{assessments.length}</div>
          <div className="lb" style={{ marginTop: 8 }}>completed</div>
        </div>
        <div className="card stat">
          <div className="lb">Weakest skill</div>
          <div className="vl" style={{ fontSize: 18, wordBreak: 'break-all' }}>
            {gaps[0].skill}
          </div>
          <div className="lb" style={{ marginTop: 8 }}>
            {Math.round(gaps[0].ratio * 100)}% mastery
          </div>
        </div>
      </div>

      {/* ---------- Gap rows ---------- */}
      <div style={{ display: 'grid', gap: 14 }}>
        {gaps.map((g) => {
          const sev = SEV_STYLE[severityOf(g.ratio)];
          const pct = Math.round(g.ratio * 100);
          return (
            <div className="card" key={g.skill}>
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 12,
                  flexWrap: 'wrap',
                  marginBottom: 10,
                }}
              >
                <b style={{ fontSize: 16 }}>{g.skill}</b>
                <span
                  style={{
                    fontSize: 11,
                    fontWeight: 700,
                    padding: '3px 10px',
                    borderRadius: 99,
                    letterSpacing: '.04em',
                    background: sev.bg,
                    color: sev.fg,
                    border: `1px solid ${sev.bd}`,
                  }}
                >
                  {sev.label}
                </span>
                <span className="mono" style={{ marginLeft: 'auto', fontSize: 13, color: 'var(--muted)' }}>
                  {g.correct}/{g.total} · {pct}%
                </span>
              </div>

              <div
                style={{
                  height: 8,
                  background: 'rgba(255,255,255,.06)',
                  borderRadius: 99,
                  overflow: 'hidden',
                  marginBottom: 10,
                }}
              >
                <div
                  style={{
                    width: `${Math.max(pct, 3)}%`,
                    height: '100%',
                    borderRadius: 99,
                    background: severityOf(g.ratio) === 'high' ? 'var(--red)' : 'var(--amber)',
                  }}
                />
              </div>

              <div style={{ fontSize: 12.5, color: 'var(--muted)', marginBottom: 14 }}>
                Seen in:{' '}
                {g.sources.map((s) => (
                  <span
                    key={s.assessment_id}
                    style={{
                      display: 'inline-block',
                      background: 'rgba(255,255,255,.05)',
                      border: '1px solid var(--border)',
                      borderRadius: 8,
                      padding: '2px 8px',
                      marginRight: 6,
                    }}
                  >
                    {s.topic} · {s.level}
                  </span>
                ))}
              </div>

              <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                <button className="btn-ghost" onClick={() => navigate('/practice')}>
                  Practice this skill
                </button>
                <button
                  className="btn-ghost"
                  disabled={roadmapBusy === g.skill}
                  onClick={() => void addToRoadmap(g)}
                >
                  {roadmapBusy === g.skill ? 'Updating roadmap…' : 'Add to roadmap'}
                </button>
                <button className="btn-ghost" onClick={() => navigate('/plan')}>
                  Reassess
                </button>
              </div>

              {roadmapMsg?.skill === g.skill && (
                <p
                  style={{
                    margin: '10px 0 0',
                    fontSize: 13,
                    color: roadmapMsg.text.startsWith('✓') ? 'var(--green)' : 'var(--red)',
                  }}
                >
                  {roadmapMsg.text}
                </p>
              )}
            </div>
          );
        })}
      </div>

      {/* ---------- Per-assessment breakdown ---------- */}
      <h2
        style={{
          fontSize: 13,
          fontWeight: 700,
          letterSpacing: '.1em',
          color: 'var(--muted)',
          margin: '34px 0 14px',
        }}
      >
        PER-ASSESSMENT BREAKDOWN
      </h2>
      <div style={{ display: 'grid', gap: 10 }}>
        {assessments.map((a) => {
          const open = openPanel === a.assessment_id;
          const ratio = a.total > 0 ? a.correct / a.total : 0;
          return (
            <div className="card" key={a.assessment_id} style={{ padding: '16px 20px' }}>
              <button
                onClick={() => setOpenPanel(open ? null : a.assessment_id)}
                style={{
                  all: 'unset',
                  display: 'flex',
                  width: '100%',
                  alignItems: 'center',
                  gap: 12,
                  cursor: 'pointer',
                }}
              >
                <span style={{ fontSize: 14 }}>{open ? '▾' : '▸'}</span>
                <b style={{ fontSize: 15 }}>
                  {a.topic} · {a.level}
                </b>
                <span style={{ fontSize: 12.5, color: 'var(--muted)' }}>
                  {a.correct}/{a.total} ({Math.round(ratio * 100)}%)
                </span>
                {a.gaps.length > 0 && (
                  <span
                    style={{
                      fontSize: 11,
                      fontWeight: 700,
                      padding: '2px 9px',
                      borderRadius: 99,
                      background: 'rgba(240,108,117,.14)',
                      color: 'var(--red)',
                      border: '1px solid rgba(240,108,117,.35)',
                    }}
                  >
                    {a.gaps.length} gap{a.gaps.length === 1 ? '' : 's'}
                  </span>
                )}
                <span
                  className="mono"
                  style={{
                    marginLeft: 'auto',
                    fontSize: 11,
                    color: 'var(--muted)',
                    wordBreak: 'break-all',
                  }}
                >
                  {a.assessment_id.slice(0, 8)}
                </span>
              </button>

              {open && (
                <div style={{ marginTop: 14, display: 'grid', gap: 12 }}>
                  {a.per_skill.length === 0 && (
                    <p className="coming" style={{ margin: 0 }}>
                      Per-skill detail unavailable for this assessment.
                    </p>
                  )}
                  {a.per_skill.map((ps) => {
                    const r = ps.total > 0 ? ps.correct / ps.total : 0;
                    const p = Math.round(r * 100);
                    const isGap = r < 0.7;
                    return (
                      <div key={ps.skill}>
                        <div
                          style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            fontSize: 14,
                            marginBottom: 6,
                          }}
                        >
                          <b style={{ fontWeight: 600 }}>{ps.skill}</b>
                          <span
                            style={{
                              fontSize: 11,
                              fontWeight: 700,
                              padding: '3px 10px',
                              borderRadius: 99,
                              background: isGap
                                ? 'rgba(240,108,117,.14)'
                                : 'rgba(57,217,138,.14)',
                              color: isGap ? 'var(--red)' : 'var(--green)',
                            }}
                          >
                            {isGap ? `GAP · ${p}%` : `✓ ${p}%`}
                          </span>
                        </div>
                        <div
                          style={{
                            height: 8,
                            background: 'rgba(255,255,255,.06)',
                            borderRadius: 99,
                            overflow: 'hidden',
                          }}
                        >
                          <div
                            style={{
                              width: `${Math.max(p, 3)}%`,
                              height: '100%',
                              borderRadius: 99,
                              background: isGap ? 'var(--red)' : 'var(--green)',
                            }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
      </div>

      <p
        style={{
          marginTop: 36,
          fontSize: 13,
          color: 'var(--muted)',
          textAlign: 'center',
          letterSpacing: '.02em',
        }}
      >
        Know your level. Close your gaps. Show your proof.
      </p>
    </div>
  );
}
