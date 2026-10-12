import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api, ApiError } from '../../lib/api';
import type { PlacementStart } from './lib';
import './onboarding.css';

/**
 * Route: /plan — "Make a plan" wizard (Flow 3).
 * Step 1: domain + subject select (GET /placement/topics).
 * Step 2: level select (beginner / intermediate / advanced cards).
 * Step 3: review → POST /placement/start.
 *   - verification_skipped (beginner) → ensure a roadmap exists, then /roadmap.
 *   - else → /verification with {placement_id, topic, claimed_level, questions}
 *     in router state.
 */
const LEVELS = [
  {
    id: 'beginner',
    icon: '🌱',
    name: 'Beginner',
    desc: 'Starting from zero — no test. We auto-verify you as a beginner and build your roadmap from the very basics.',
  },
  {
    id: 'intermediate',
    icon: '🚀',
    name: 'Intermediate',
    desc: '8 questions — 4 beginner + 4 intermediate. We verify exactly where you stand before planning.',
  },
  {
    id: 'advanced',
    icon: '⚡',
    name: 'Advanced',
    desc: '12 questions — 4 across each level from beginner to advanced. Prove the depth, skip the basics.',
  },
] as const;

function prettyTopic(topic: string): { name: string; domain: string } {
  const map: Record<string, { name: string; domain: string }> = {
    python: { name: 'Python', domain: 'Programming' },
    'ml-basics': { name: 'ML Basics', domain: 'Machine Learning' },
  };
  return map[topic] ?? { name: topic, domain: 'Track' };
}

export default function MakePlan() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [topics, setTopics] = useState<string[]>([]);
  const [topicsLoading, setTopicsLoading] = useState(true);
  const [topicsError, setTopicsError] = useState('');
  const [topic, setTopic] = useState('');
  const [level, setLevel] = useState<string>('');
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    api<{ topics: string[] }>('/api/v1/placement/topics')
      .then((r) => setTopics(r.topics ?? []))
      .catch((e) => setTopicsError(e instanceof Error ? e.message : 'Could not load subjects'))
      .finally(() => setTopicsLoading(false));
  }, []);

  const ensureRoadmap = async (t: string) => {
    try {
      await api('/api/v1/roadmaps/current');
      return; // a roadmap already exists
    } catch (e) {
      if (!(e instanceof ApiError) || e.status !== 400) throw e;
    }
    // No roadmap yet — generate one from scratch for this topic.
    await api('/api/v1/roadmaps/generate', {
      method: 'POST',
      body: JSON.stringify({
        gaps: [{ skill: t, mastery_pct: 0 }],
        title: `Roadmap: ${prettyTopic(t).name} from scratch`,
      }),
    });
  };

  const start = async () => {
    setStarting(true);
    setError('');
    try {
      const res = await api<PlacementStart>('/api/v1/placement/start', {
        method: 'POST',
        body: JSON.stringify({ topic, claimed_level: level }),
      });
      if (res.verification_skipped) {
        // Beginner fast-path: straight to the roadmap.
        await ensureRoadmap(topic);
        navigate('/roadmap');
      } else {
        navigate('/verification', {
          state: {
            placement_id: res.placement_id,
            topic: res.topic,
            claimed_level: res.claimed_level,
            questions: res.questions,
          },
        });
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Could not start verification');
    } finally {
      setStarting(false);
    }
  };

  const steps = ['Subject', 'Level', 'Start'];

  return (
    <div className="ob">
      <div className="ob-kicker">MAKE A PLAN</div>
      <h1 className="ob-title">Where are you starting from?</h1>
      <p className="ob-sub">
        Pick a subject and your level. We verify your real level with a short test —
        then build your roadmap from there. No self-report ever counts as skill.
      </p>

      <div className="ob-steps">
        {steps.map((s, i) => (
          <div key={s} className={`ob-step ${step === i + 1 ? 'on' : ''} ${step > i + 1 ? 'done' : ''}`}>
            {i + 1}. {s}
          </div>
        ))}
      </div>

      {step === 1 && (
        <div className="ob-card">
          <h3>Choose your subject</h3>
          <p className="ob-hint">The track your roadmap will be built around.</p>
          {topicsLoading && <div className="ob-load" style={{ padding: 20 }}>Loading subjects…</div>}
          {topicsError && <div className="ob-alert err">{topicsError}</div>}
          {!topicsLoading && !topicsError && topics.length === 0 && (
            <p className="ob-empty">No subjects available right now.</p>
          )}
          <div className="ob-pick-grid" style={{ gridTemplateColumns: 'repeat(2, 1fr)' }}>
            {topics.map((t) => {
              const p = prettyTopic(t);
              return (
                <button
                  key={t}
                  className={`ob-pick ${topic === t ? 'sel' : ''}`}
                  onClick={() => setTopic(t)}
                >
                  <span className="ob-lvl-tag">{p.domain}</span>
                  <b style={{ marginTop: 8 }}>{p.name}</b>
                  <p className="mono" style={{ fontSize: 12 }}>{t}</p>
                </button>
              );
            })}
          </div>
          <div className="ob-nav-row">
            <span />
            <button className="ob-btn-sm" disabled={!topic} onClick={() => setStep(2)}>
              Continue →
            </button>
          </div>
        </div>
      )}

      {step === 2 && (
        <div className="ob-card">
          <h3>What level are you at?</h3>
          <p className="ob-hint">Be honest — the verification test decides your real level anyway.</p>
          <div className="ob-pick-grid">
            {LEVELS.map((l) => (
              <button
                key={l.id}
                className={`ob-pick ${level === l.id ? 'sel' : ''}`}
                onClick={() => setLevel(l.id)}
              >
                <span className="ic">{l.icon}</span>
                <b>{l.name}</b>
                <p>{l.desc}</p>
              </button>
            ))}
          </div>
          <div className="ob-nav-row">
            <button className="ob-ghost" onClick={() => setStep(1)}>← Back</button>
            <button className="ob-btn-sm" disabled={!level} onClick={() => setStep(3)}>
              Continue →
            </button>
          </div>
        </div>
      )}

      {step === 3 && (
        <div className="ob-card glow">
          <div className="ob-kicker">READY</div>
          <h3 style={{ fontSize: 20 }}>
            {prettyTopic(topic).name} · <span style={{ textTransform: 'capitalize' }}>{level}</span>
          </h3>
          <p className="ob-hint" style={{ marginTop: 8 }}>
            {level === 'beginner'
              ? 'No test needed — you\u2019ll go straight to a from-scratch roadmap.'
              : 'A short verification test starts now. Answer honestly; your verified level shapes the roadmap.'}
          </p>
          {error && <div className="ob-alert err">{error}</div>}
          <div className="ob-nav-row">
            <button className="ob-ghost" onClick={() => setStep(2)} disabled={starting}>← Back</button>
            <button className="ob-btn" onClick={start} disabled={starting}>
              {starting ? 'Starting…' : level === 'beginner' ? 'Build my roadmap →' : 'Start verification →'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
