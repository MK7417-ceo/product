import { useCallback, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../lib/api';
import TheoryCard from '../components/visual/TheoryCard';
import './Learn.css';

interface Topic {
  slug: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  active: boolean;
  theory_count?: number;
}

interface TheoryBlock {
  id: string;
  topic_slug: string;
  title: string;
  level: string;
  content: string;
  order_index: number;
}

const LEVEL_LABEL: Record<string, string> = {
  beginner: '🌱 Beginner',
  intermediate: '🌿 Intermediate',
  advanced: '🌳 Advanced',
  expert: '🔥 Expert',
};

function TopicList() {
  const navigate = useNavigate();
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const r = await api<{ topics: Topic[] }>('/api/v1/content/topics');
        // Hide topics with no theory content — don't promise what isn't there.
        setTopics(r.topics.filter((t) => (t.theory_count ?? 0) > 0));
      } catch (e) {
        setError(e instanceof Error ? e.message : 'Failed to load topics');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return <div className="learn-wrap"><p className="learn-muted">Loading topics…</p></div>;
  if (error) return <div className="learn-wrap"><p className="learn-error">{error}</p></div>;

  return (
    <div className="learn-wrap">
      <header className="learn-head">
        <h1>📖 Learn</h1>
        <p className="learn-muted">Pick a topic, read the theory, then practice it.</p>
      </header>
      {topics.length === 0 ? (
        <p className="learn-muted">No topics yet — check back soon.</p>
      ) : (
        <div className="learn-grid">
          {topics.map((t) => (
            <button
              key={t.slug}
              className="learn-topic-card"
              style={{ ['--topic-color' as string]: t.color || '#E85D26' }}
              onClick={() => navigate(`/learn/${t.slug}`)}
            >
              <span className="learn-topic-icon">{t.icon || '📘'}</span>
              <span className="learn-topic-name">{t.name}</span>
              {t.description && <span className="learn-topic-desc">{t.description}</span>}
              <span className="learn-topic-cta">Read →</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

function TopicDetail() {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const [topic, setTopic] = useState<Topic | null>(null);
  const [blocks, setBlocks] = useState<TheoryBlock[]>([]);
  const [level, setLevel] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const load = useCallback(async (lv: string) => {
    if (!slug) return;
    setLoading(true);
    setError('');
    try {
      const [t, b] = await Promise.all([
        api<Topic>(`/api/v1/content/topics/${slug}`),
        api<{ theory: TheoryBlock[] }>(
          `/api/v1/content/topics/${slug}/theory${lv ? `?level=${lv}` : ''}`
        ),
      ]);
      setTopic(t);
      setBlocks(b.theory);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load content');
    } finally {
      setLoading(false);
    }
  }, [slug]);

  useEffect(() => { load(level); }, [load, level]);

  if (loading) return <div className="learn-wrap"><p className="learn-muted">Loading…</p></div>;
  if (error) return <div className="learn-wrap"><p className="learn-error">{error}</p></div>;

  return (
    <div className="learn-wrap">
      <button className="learn-back" onClick={() => navigate('/learn')}>← All topics</button>
      <header className="learn-head">
        <h1>{topic?.icon} {topic?.name}</h1>
        {topic?.description && <p className="learn-muted">{topic.description}</p>}
      </header>
      <div className="learn-filters">
        {['', 'beginner', 'intermediate', 'advanced', 'expert'].map((lv) => (
          <button
            key={lv || 'all'}
            className={`learn-chip${level === lv ? ' active' : ''}`}
            onClick={() => setLevel(lv)}
          >
            {lv === '' ? 'All levels' : LEVEL_LABEL[lv]}
          </button>
        ))}
      </div>
      {blocks.length === 0 ? (
        <p className="learn-muted">No theory blocks here yet.</p>
      ) : (
        <div className="learn-blocks">
          {blocks.map((b) => (
            <TheoryCard key={b.id} title={b.title} content={b.content} />
          ))}
        </div>
      )}
    </div>
  );
}

export default function Learn() {
  const { slug } = useParams<{ slug: string }>();
  return slug ? <TopicDetail /> : <TopicList />;
}
