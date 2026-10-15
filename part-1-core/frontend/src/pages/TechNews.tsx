import { useEffect, useState } from 'react';
import { api } from '../lib/api';
import { useLang } from '../lib/i18n';
import './TechNews.css';

interface NewsItem {
  title: string;
  url: string;
  source: string;
  score?: number;
  time_ago?: string;
}

interface NewsResponse {
  big_news: NewsItem[];
  latest: NewsItem[];
  updated_min_ago: number | null;
  retention: string;
  stale: boolean;
}

export default function TechNews() {
  const { t } = useLang();
  const [data, setData] = useState<NewsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const load = async (refresh = false) => {
    if (refresh) setRefreshing(true);
    else setLoading(true);
    try {
      const res = await api<NewsResponse>(`/api/v1/news/tech${refresh ? '?refresh=true' : ''}`);
      // API already returns latest-first
      setData(res);
    } catch {
      setData({ big_news: [], latest: [], updated_min_ago: null, retention: '1 year', stale: true });
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const renderCard = (item: NewsItem, big = false) => (
    <a
      key={item.url}
      href={item.url}
      target="_blank"
      rel="noopener noreferrer"
      className={`news-card${big ? ' news-card-big' : ''}`}
    >
      <div className="news-card-title">{item.title}</div>
      <div className="news-card-meta">
        <span className="news-source">{item.source}</span>
        {item.score !== undefined && <span className="news-score">▲ {item.score}</span>}
        {item.time_ago && <span className="news-time">{item.time_ago}</span>}
      </div>
    </a>
  );

  return (
    <div className="tech-news-page">
      <header className="news-header">
        <div>
          <h1>📰 {t('news.title', 'Tech News')}</h1>
          <p className="news-subtitle">{t('news.subtitle', 'Stay updated — right inside SkillForge')}</p>
          {data?.updated_min_ago !== null && data?.updated_min_ago !== undefined && (
            <p className="news-updated">
              🕐 {t('news.updatedAgo', 'Updated')} {data.updated_min_ago}{' '}
              {t('news.minAgo', 'min ago')}
            </p>
          )}
        </div>
        <button
          className="news-refresh"
          onClick={() => load(true)}
          disabled={refreshing}
        >
          {refreshing ? '⏳' : '🔄'} {t('news.refresh', 'Refresh')}
        </button>
      </header>

      {loading ? (
        <div className="news-loading">{t('news.loading', 'Loading news…')}</div>
      ) : (
        <>
          {data && data.big_news.length > 0 && (
            <section className="news-section">
              <h2 className="news-section-title big-news-title">
                🔥 {t('news.bigNews', 'Big News')}
              </h2>
              <div className="news-grid">
                {data.big_news.map((item) => renderCard(item, true))}
              </div>
            </section>
          )}

          <section className="news-section">
            <h2 className="news-section-title">
              ⚡ {t('news.latest', 'Latest')}
            </h2>
            {data && data.latest.length > 0 ? (
              <div className="news-grid">
                {data.latest.map((item) => renderCard(item))}
              </div>
            ) : (
              <div className="news-empty">
                {t('news.empty', 'No news right now. Try refreshing.')}
              </div>
            )}
          </section>

          {data?.stale && (
            <div className="news-stale">
              ⚠️ {t('news.stale', 'Showing cached news — could not reach news sources.')}
            </div>
          )}
        </>
      )}
    </div>
  );
}
