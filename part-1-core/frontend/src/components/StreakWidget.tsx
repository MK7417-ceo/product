import { useEffect, useState } from 'react';
import { api } from '../lib/api';
import { useLang } from '../lib/i18n';
import './StreakWidget.css';

export interface StreakData {
  current_streak: number;
  longest_streak: number;
  total_days_active: number;
  last_activity_date: string | null;
  today_done: boolean;
  milestone: string | null;
  recent_days: string[];
}

export async function fetchStreak(): Promise<StreakData | null> {
  try {
    return await api<StreakData>('/streak/mine');
  } catch {
    return null;
  }
}

const MILESTONE_EMOJI: Record<string, string> = {
  week: '🎉',
  month: '🏆',
  century: '👑',
  year: '🌟',
};

interface Props {
  compact?: boolean;
  showCalendar?: boolean;
  /** Override for demos/tests — skips the API fetch. */
  data?: StreakData | null;
}

export default function StreakWidget({ compact = false, showCalendar = true, data }: Props) {
  const { t } = useLang();
  const [streak, setStreak] = useState<StreakData | null>(data ?? null);

  useEffect(() => {
    if (data !== undefined) return;
    fetchStreak().then(setStreak);
  }, [data]);

  if (!streak) return null;

  const activeSet = new Set(streak.recent_days);
  const days: { date: string; active: boolean }[] = [];
  const today = new Date();
  for (let i = 29; i >= 0; i--) {
    const d = new Date(today);
    d.setDate(today.getDate() - i);
    const iso = d.toISOString().slice(0, 10);
    days.push({ date: iso, active: activeSet.has(iso) });
  }

  return (
    <div className={`streak-widget${compact ? ' streak-compact' : ''}`}>
      <div className="streak-main">
        <span className={`streak-flame${streak.current_streak > 0 ? ' lit' : ''}`} aria-hidden>
          🔥
        </span>
        <div className="streak-numbers">
          <span className="streak-count">{streak.current_streak}</span>
          <span className="streak-label">{t('streak.days')}</span>
        </div>
        <div className="streak-side">
          <span className="streak-stat">
            {t('streak.longest')}: <b>{streak.longest_streak}</b>
          </span>
          <span className="streak-stat">
            {t('streak.totalDays')}: <b>{streak.total_days_active}</b>
          </span>
        </div>
      </div>

      {streak.milestone && (
        <div className="streak-milestone" role="status">
          {MILESTONE_EMOJI[streak.milestone] ?? '🎉'} {t(`streak.milestone.${streak.milestone}`)}
        </div>
      )}

      <div className={`streak-today${streak.today_done ? ' done' : ' pending'}`}>
        {streak.today_done ? t('streak.todayDone') : t('streak.todayPending')}
      </div>

      {showCalendar && !compact && (
        <div className="streak-calendar">
          <div className="streak-cal-title">{t('streak.calendar')}</div>
          <div className="streak-dots" role="img" aria-label={t('streak.calendar')}>
            {days.map((d) => (
              <span
                key={d.date}
                title={d.date}
                className={`streak-dot${d.active ? ' active' : ''}`}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
