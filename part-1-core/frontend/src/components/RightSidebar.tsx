import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../lib/api';
import { useLang } from '../lib/i18n';
import { fetchStreak, type StreakData } from './StreakWidget';
import './RightSidebar.css';

interface CoinData {
  balance: number;
  lifetime_earned: number;
}

async function fetchCoins(): Promise<CoinData | null> {
  try {
    return await api<CoinData>('/api/v1/coins/mine');
  } catch {
    return null;
  }
}

/** Last 7 days, oldest -> newest, as YYYY-MM-DD */
function last7Days(): string[] {
  const days: string[] = [];
  const now = new Date();
  for (let i = 6; i >= 0; i--) {
    const d = new Date(now);
    d.setDate(now.getDate() - i);
    days.push(d.toISOString().slice(0, 10));
  }
  return days;
}

const DAY_LETTERS = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];

export default function RightSidebar() {
  const { t } = useLang();
  const [streak, setStreak] = useState<StreakData | null>(null);
  const [coins, setCoins] = useState<CoinData | null>(null);

  useEffect(() => {
    fetchStreak().then(setStreak);
    fetchCoins().then(setCoins);
  }, []);

  const activeSet = new Set(streak?.recent_days ?? []);
  const week = last7Days();

  return (
    <aside className="sf-right-sidebar" aria-label="Progress sidebar">
      {/* Streak card */}
      <div className="rs-card rs-streak">
        <div className="rs-streak-row">
          <span className="rs-flame" aria-hidden>🔥</span>
          <div>
            <div className="rs-big-number">{streak?.current_streak ?? '–'}</div>
            <div className="rs-label">{t('streak.dayStreak', 'Day streak')}</div>
          </div>
          <div className="rs-sub">
            <div>{t('streak.longest', 'Longest')}: <b>{streak?.longest_streak ?? '–'}</b></div>
          </div>
        </div>
        {/* 7-day mini calendar */}
        <div className="rs-week" role="img" aria-label="Last 7 days activity">
          {week.map((d) => {
            const dt = new Date(d + 'T00:00:00');
            const active = activeSet.has(d);
            const isToday = d === new Date().toISOString().slice(0, 10);
            return (
              <div key={d} className={`rs-day${active ? ' active' : ''}${isToday ? ' today' : ''}`}
                   title={d}>
                <span className="rs-day-letter">{DAY_LETTERS[dt.getDay()]}</span>
                <span className="rs-day-dot" />
              </div>
            );
          })}
        </div>
      </div>

      {/* Coins card */}
      <div className="rs-card rs-coins">
        <div className="rs-streak-row">
          <span className="rs-flame" aria-hidden>🪙</span>
          <div>
            <div className="rs-big-number rs-gold">{coins?.balance ?? '–'}</div>
            <div className="rs-label">{t('coins.balance', 'Coins')}</div>
          </div>
        </div>
        <Link to="/coins" className="rs-shop-link">
          🛒 {t('coins.shop', 'Coin Shop')} →
        </Link>
      </div>

      {/* Today's progress */}
      <div className="rs-card rs-today">
        <div className="rs-label">{t('streak.today', "Today's progress")}</div>
        <div className={`rs-today-status ${streak?.today_done ? 'done' : 'pending'}`}>
          {streak?.today_done
            ? `✅ ${t('streak.doneToday', 'Done today!')}`
            : `⏳ ${t('streak.notYet', 'Not yet — keep going!')}`}
        </div>
      </div>
    </aside>
  );
}
