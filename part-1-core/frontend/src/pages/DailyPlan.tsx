import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLang } from '../lib/i18n';
import { api } from '../lib/api';
import { PLAN_STORAGE_KEY } from './onboarding/LearningSetup';
import './daily-plan.css';

interface Task {
  type: string;
  title?: string;
  count?: number;
  minutes?: number;
  timed?: boolean;
  lesson_id?: string;
}

interface PlanDay {
  day: number;
  month: number;
  week: number;
  kind: string;
  tasks: Task[];
}

interface StoredPlan {
  domain_slug: string;
  domain_name: string;
  domain_icon: string;
  start_level: string;
  started_at: string;
  days: PlanDay[];
  summary: { total_days: number };
  server_managed?: boolean;
  total_days?: number;
}

/* Server-managed plan (sibling curriculum API) */
interface ServerTask {
  id: string;
  task_type: string;
  title: string;
  description?: string;
  status: 'pending' | 'done' | 'skipped';
}

interface ServerPlan {
  id: string;
  domain_slug: string;
  current_day: number;
  total_days: number;
  status: string;
  today_tasks: ServerTask[];
}

interface Progress {
  [dateKey: string]: { day: number; done: number[] };
}

const PROGRESS_KEY = 'sf-daily-progress';

function dateKey(d: Date): string {
  return d.toISOString().slice(0, 10);
}

function loadPlan(): StoredPlan | null {
  try {
    const raw = localStorage.getItem(PLAN_STORAGE_KEY);
    return raw ? (JSON.parse(raw) as StoredPlan) : null;
  } catch {
    return null;
  }
}

function loadProgress(): Progress {
  try {
    return JSON.parse(localStorage.getItem(PROGRESS_KEY) || '{}') as Progress;
  } catch {
    return {};
  }
}

const TASK_ICONS: Record<string, string> = {
  learn: '📚',
  practice: '✏️',
  code: '💻',
  revise: '🔁',
  mock: '🧪',
};

export default function DailyPlan() {
  const { t } = useLang();
  const navigate = useNavigate();
  const [plan, setPlan] = useState<StoredPlan | null>(null);
  const [progress, setProgress] = useState<Progress>({});
  const [celebrated, setCelebrated] = useState(false);
  const [serverPlan, setServerPlan] = useState<ServerPlan | null>(null);
  const [serverLoading, setServerLoading] = useState(false);

  useEffect(() => {
    const p = loadPlan();
    setPlan(p);
    setProgress(loadProgress());
    if (p?.server_managed) {
      setServerLoading(true);
      api<{ plans: ServerPlan[] }>('/api/v1/curriculum/plans/mine')
        .then((out) => {
          const match =
            out.plans.find(
              (sp) => sp.domain_slug === p.domain_slug && sp.status === 'active',
            ) ?? out.plans[0] ??
            null;
          setServerPlan(match);
        })
        .catch(() => setServerPlan(null))
        .finally(() => setServerLoading(false));
    }
  }, []);

  const todayIdx = useMemo(() => {
    if (!plan) return 1;
    const start = new Date(plan.started_at).getTime();
    const days = Math.floor((Date.now() - start) / 86400000) + 1;
    return Math.min(Math.max(1, days), plan.days.length);
  }, [plan]);

  const today = plan?.days[todayIdx - 1] ?? null;
  const key = dateKey(new Date());
  const done: number[] = progress[key]?.done ?? [];

  const streak = useMemo(() => {
    if (!plan) return 0;
    let s = 0;
    const d = new Date();
    // If today isn't finished yet, streak counts from yesterday.
    const todayDone = (progress[dateKey(d)]?.done.length ?? 0) >= (today?.tasks.length ?? 1);
    if (!todayDone) d.setDate(d.getDate() - 1);
    for (;;) {
      const k = dateKey(d);
      const entry = progress[k];
      const dayNum = entry?.day;
      const dayTasks = dayNum ? plan.days[dayNum - 1]?.tasks.length ?? 0 : 0;
      if (entry && dayTasks > 0 && entry.done.length >= dayTasks) {
        s += 1;
        d.setDate(d.getDate() - 1);
      } else break;
      if (s > 365) break;
    }
    return s;
  }, [progress, plan, today]);

  const toggle = (i: number) => {
    if (serverPlan) {
      const st = serverPlan.today_tasks[i];
      if (!st) return;
      const nextStatus = st.status === 'done' ? 'pending' : 'done';
      const prev = serverPlan;
      setServerPlan({
        ...serverPlan,
        today_tasks: serverPlan.today_tasks.map((x, xi) =>
          xi === i ? { ...x, status: nextStatus } : x,
        ),
      });
      api(`/api/v1/curriculum/tasks/${st.id}`, {
        method: 'PATCH',
        body: JSON.stringify({ status: nextStatus }),
      }).catch(() => setServerPlan(prev)); // revert on failure
      return;
    }
    const next = done.includes(i) ? done.filter((x) => x !== i) : [...done, i];
    const p = { ...progress, [key]: { day: todayIdx, done: next } };
    setProgress(p);
    try {
      localStorage.setItem(PROGRESS_KEY, JSON.stringify(p));
    } catch {
      /* ignore */
    }
    if (today && next.length === today.tasks.length) setCelebrated(true);
  };

  const taskLabel = (task: Task): string => {
    const base = t(`daily.task.${task.type}` as 'daily.task.learn');
    if (task.title) return `${base}: ${task.title}`;
    const parts: string[] = [base];
    if (task.count) parts.push(`${task.count} ${task.count === 1 ? t('daily.question.one') : t('daily.questions')}`);
    if (task.minutes) parts.push(`· ${task.minutes} ${t('daily.minutes')}`);
    if (task.timed) parts.push('⏱️');
    return parts.join(' ');
  };

  if (!plan) {
    return (
      <div className="daily empty">
        <h1>{t('daily.title')}</h1>
        <p className="muted">Koi active plan nahi hai. Pehle apna learning plan banao!</p>
        <button className="btn-primary" onClick={() => navigate('/learning-setup')}>
          {t('plan.title')} →
        </button>
      </div>
    );
  }

  // ---- server-managed rendering ----
  if (plan.server_managed) {
    if (serverLoading) {
      return (
        <div className="daily empty">
          <h1>
            {plan.domain_icon} {plan.domain_name}
          </h1>
          <p className="muted">{t('plan.loading')}</p>
        </div>
      );
    }
    if (!serverPlan) {
      return (
        <div className="daily empty">
          <h1>
            {plan.domain_icon} {plan.domain_name}
          </h1>
          <p className="muted">Plan load nahi ho paya. Dobara try karo.</p>
          <button className="btn-ghost" onClick={() => navigate('/learning-setup')}>
            ← {t('plan.back')}
          </button>
        </div>
      );
    }
    const stasks = serverPlan.today_tasks;
    const sdone = stasks.filter((x) => x.status === 'done').length;
    const spct = stasks.length ? Math.round((sdone / stasks.length) * 100) : 0;
    const sallDone = stasks.length > 0 && sdone === stasks.length;
    return (
      <div className="daily">
        <header className="daily-head">
          <div>
            <h1>
              {plan.domain_icon} {plan.domain_name}
            </h1>
            <p className="muted">
              {t('daily.dayOf')} {serverPlan.current_day} / {serverPlan.total_days} ·{' '}
              {t('daily.title')}
            </p>
          </div>
          <div className="streak" title={t('daily.streak')}>
            🔥 {streak}
          </div>
        </header>
        <div className="progress-wrap">
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${spct}%` }} />
          </div>
          <span className="progress-pct">{spct}%</span>
        </div>
        {sallDone ? (
          <div className="celebrate">
            <div className="celebrate-emoji">🎉</div>
            <h2>{t('daily.complete')}</h2>
            <p className="muted">{t('daily.complete.sub')}</p>
          </div>
        ) : (
          <ul className="task-list">
            {stasks.map((st, i) => (
              <li key={st.id} className={st.status === 'done' ? 'task done' : 'task'}>
                <label>
                  <input
                    type="checkbox"
                    checked={st.status === 'done'}
                    onChange={() => toggle(i)}
                    aria-label={st.title}
                  />
                  <span className="task-icon">{TASK_ICONS[st.task_type] ?? '📌'}</span>
                  <span className="task-text">
                    {t(`daily.task.${st.task_type}` as 'daily.task.learn')}: {st.title}
                  </span>
                </label>
              </li>
            ))}
          </ul>
        )}
        <div className="daily-foot">
          <button className="btn-ghost" onClick={() => navigate('/')}>
            ← Dashboard
          </button>
        </div>
      </div>
    );
  }

  if (!today) {
    return (
      <div className="daily empty">
        <h1>{t('daily.title')}</h1>
        <p className="muted">Koi active plan nahi hai. Pehle apna learning plan banao!</p>
        <button className="btn-primary" onClick={() => navigate('/learning-setup')}>
          {t('plan.title')} →
        </button>
      </div>
    );
  }

  const pct = today.tasks.length ? Math.round((done.length / today.tasks.length) * 100) : 0;
  const allDone = done.length === today.tasks.length && today.tasks.length > 0;

  return (
    <div className="daily">
      <header className="daily-head">
        <div>
          <h1>
            {plan.domain_icon} {plan.domain_name}
          </h1>
          <p className="muted">
            {t('daily.dayOf')} {todayIdx} / {plan.days.length} · {t('daily.title')}
            {today.kind !== 'learn' && (
              <span className={`kind-badge ${today.kind}`}>
                {today.kind === 'revision' ? `🔁 ${t('daily.task.revise')}` : `🧪 ${t('daily.task.mock')}`}
              </span>
            )}
          </p>
        </div>
        <div className="streak" title={t('daily.streak')}>
          🔥 {streak}
        </div>
      </header>

      <div className="progress-wrap">
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${pct}%` }} />
        </div>
        <span className="progress-pct">{pct}%</span>
      </div>

      {allDone || celebrated ? (
        <div className="celebrate">
          <div className="celebrate-emoji">🎉</div>
          <h2>{t('daily.complete')}</h2>
          <p className="muted">{t('daily.complete.sub')}</p>
        </div>
      ) : (
        <ul className="task-list">
          {today.tasks.map((task, i) => (
            <li key={i} className={done.includes(i) ? 'task done' : 'task'}>
              <label>
                <input
                  type="checkbox"
                  checked={done.includes(i)}
                  onChange={() => toggle(i)}
                  aria-label={taskLabel(task)}
                />
                <span className="task-icon">{TASK_ICONS[task.type] ?? '📌'}</span>
                <span className="task-text">{taskLabel(task)}</span>
              </label>
            </li>
          ))}
        </ul>
      )}

      {!allDone && done.length > 0 && <p className="muted keep-going">{t('daily.keepGoing')}</p>}

      <div className="daily-foot">
        <button className="btn-ghost" onClick={() => navigate('/')}>
          ← Dashboard
        </button>
      </div>
    </div>
  );
}
