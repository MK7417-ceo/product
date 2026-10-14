import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLang } from '../../lib/i18n';
import { api } from '../../lib/api';
import './onboarding.css';
import './plan-setup.css';

/* Domain catalog — shown to the user with NO coding/non-coding labels.
   The `coding` flag is internal only: it tells the plan generator whether
   to include hands-on code tasks (mirrors backend domain_skills.py). */
interface Domain {
  slug: string;
  name: string;
  icon: string;
  desc: string;
  coding: boolean;
}

const DOMAINS: Domain[] = [
  { slug: 'python', name: 'Python', icon: '🐍', desc: 'Sabse popular language', coding: true },
  { slug: 'javascript', name: 'JavaScript', icon: '🟨', desc: 'Web ki jaan', coding: true },
  { slug: 'java', name: 'Java', icon: '☕', desc: 'Enterprise king', coding: true },
  { slug: 'webdev', name: 'Web Development', icon: '🌐', desc: 'HTML, CSS, websites', coding: true },
  { slug: 'ml-basics', name: 'Machine Learning', icon: '🤖', desc: 'AI ki duniya', coding: true },
  { slug: 'data-science', name: 'Data Science', icon: '📊', desc: 'Data se insights', coding: true },
  { slug: 'data-analyst', name: 'Data Analysis', icon: '📈', desc: 'SQL, dashboards', coding: true },
  { slug: 'networking', name: 'Computer Networking', icon: '🛜', desc: 'Internet kaise kaam karta hai', coding: false },
  { slug: 'r-lang', name: 'R Language', icon: '📉', desc: 'Statistics ke liye', coding: true },
  { slug: 'ruby', name: 'Ruby', icon: '💎', desc: 'Elegant language', coding: true },
  { slug: 'devops', name: 'DevOps', icon: '🛠️', desc: 'Deploy & scale', coding: false },
];

/* Maps our domain slugs to the curriculum DB slugs (sibling seed).
   Most match 1:1; only networking differs. */
export const CURRICULUM_SLUG_MAP: Record<string, string> = {
  networking: 'cn',
};

const LEVELS: { id: Level; icon: string }[] = [
  { id: 'scratch', icon: '🌱' },
  { id: 'beginner', icon: '📖' },
  { id: 'intermediate', icon: '💪' },
];

interface PlanSummary {
  total_days: number;
  total_months: number;
  total_lessons: number;
  est_questions: number;
  target_level: string;
}

interface PlanDay {
  day: number;
  month: number;
  week: number;
  kind: string;
  tasks: unknown[];
}

interface PreviewOut {
  domain_slug: string;
  start_level: string;
  summary: PlanSummary;
  days: PlanDay[];
}

export const PLAN_STORAGE_KEY = 'sf-study-plan';

export default function LearningSetup() {
  const { t } = useLang();
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const [domain, setDomain] = useState<Domain | null>(null);
  const [level, setLevel] = useState<Level | null>(null);
  const [preview, setPreview] = useState<PreviewOut | null>(null);
  const [loading, setLoading] = useState(false);
  const [starting, setStarting] = useState(false);

  const pickDomain = (d: Domain) => {
    setDomain(d);
    setStep(1);
  };

  const pickLevel = async (l: Level) => {
    if (!domain) return;
    setLevel(l);
    setLoading(true);
    try {
      const out = await api<PreviewOut>('/api/v1/study-plans/preview', {
        method: 'POST',
        body: JSON.stringify({
          domain_slug: domain.slug,
          start_level: l,
          lessons: [],
          coding: domain.coding,
        }),
      });
      setPreview(out);
      setStep(2);
    } catch {
      setPreview(null);
      setStep(2);
    } finally {
      setLoading(false);
    }
  };

  const startPlan = async () => {
    if (!domain || !level) return;
    setStarting(true);
    const totalDays = preview?.summary.total_days ?? { scratch: 120, beginner: 90, intermediate: 60 }[level];
    let persisted = false;
    try {
      // Real persistence: sibling curriculum API (study_plans + daily_tasks tables).
      await api('/api/v1/curriculum/plans', {
        method: 'POST',
        body: JSON.stringify({
          domain_slug: CURRICULUM_SLUG_MAP[domain.slug] ?? domain.slug,
          start_level: level,
          total_days: totalDays,
        }),
      });
      persisted = true;
    } catch {
      // Domain not seeded there yet, or API unavailable — local fallback below.
    }
    if (!persisted) {
      // Local fallback: keep the generated preview plan on this device.
      let plan: PreviewOut | null = preview;
      if (!plan) {
        try {
          plan = await api<PreviewOut>('/api/v1/study-plans/preview', {
            method: 'POST',
            body: JSON.stringify({
              domain_slug: domain.slug,
              start_level: level,
              lessons: [],
              coding: domain.coding,
            }),
          });
        } catch {
          plan = null;
        }
      }
      if (plan) {
        try {
          localStorage.setItem(
            PLAN_STORAGE_KEY,
            JSON.stringify({
              domain_slug: plan.domain_slug,
              start_level: plan.start_level,
              domain_name: domain.name,
              domain_icon: domain.icon,
              started_at: new Date().toISOString(),
              days: plan.days,
              summary: plan.summary,
            }),
          );
        } catch {
          /* storage unavailable — still navigate */
        }
      }
    } else {
      // Server-persisted: remember which domain/level for the DailyPlan page.
      try {
        localStorage.setItem(
          PLAN_STORAGE_KEY,
          JSON.stringify({
            domain_slug: domain.slug,
            start_level: level,
            domain_name: domain.name,
            domain_icon: domain.icon,
            started_at: new Date().toISOString(),
            server_managed: true,
            total_days: totalDays,
          }),
        );
      } catch {
        /* ignore */
      }
    }
    setStarting(false);
    navigate('/daily-plan');
  };

  return (
    <div className="ob plan-setup">
      <h1>{t('plan.title')}</h1>

      {step === 0 && (
        <section>
          <h2>{t('plan.step.domain')}</h2>
          <p className="muted">{t('plan.step.domain.sub')}</p>
          <div className="domain-grid">
            {DOMAINS.map((d) => (
              <button key={d.slug} className="domain-card" onClick={() => pickDomain(d)}>
                <span className="domain-icon">{d.icon}</span>
                <span className="domain-name">{d.name}</span>
                <span className="domain-desc">{d.desc}</span>
              </button>
            ))}
          </div>
        </section>
      )}

      {step === 1 && (
        <section>
          <h2>{t('plan.step.level')}</h2>
          <p className="muted">{t('plan.step.level.sub')}</p>
          {loading && <p className="muted">{t('plan.loading')}</p>}
          <div className="level-grid">
            {LEVELS.map((l) => (
              <button
                key={l.id}
                className="level-card"
                disabled={loading}
                onClick={() => pickLevel(l.id)}
              >
                <span className="level-icon">{l.icon}</span>
                <span className="level-name">{t(`plan.level.${l.id}` as 'plan.level.scratch')}</span>
                <span className="level-desc">{t(`plan.level.${l.id}.desc` as 'plan.level.scratch.desc')}</span>
              </button>
            ))}
          </div>
          <button className="btn-ghost" onClick={() => setStep(0)}>
            ← {t('plan.back')}
          </button>
        </section>
      )}

      {step === 2 && (
        <section>
          <h2>
            {t('plan.preview.title')}: {domain?.icon} {domain?.name}
          </h2>
          {preview ? (
            <div className="preview-stats">
              <div className="stat">
                <span className="stat-num">📅 {preview.summary.total_days}</span>
                <span className="stat-label">{t('plan.preview.days')}</span>
              </div>
              <div className="stat">
                <span className="stat-num">❓ {preview.summary.est_questions}+</span>
                <span className="stat-label">{t('plan.preview.questions')}</span>
              </div>
              <div className="stat">
                <span className="stat-num">🎯 {preview.summary.target_level}</span>
                <span className="stat-label">{t('plan.preview.target')}</span>
              </div>
              <div className="stat-note">📝 {t('plan.preview.revision')}</div>
              <div className="stat-note">🧪 {t('plan.preview.mock')}</div>
            </div>
          ) : (
            <p className="muted">{t('plan.loading')}</p>
          )}
          <div className="cta-row">
            <button className="btn-ghost" onClick={() => setStep(1)}>
              ← {t('plan.back')}
            </button>
            <button className="btn-primary" disabled={starting} onClick={startPlan}>
              {starting ? t('plan.loading') : t('plan.cta')}
            </button>
          </div>
        </section>
      )}
    </div>
  );
}
