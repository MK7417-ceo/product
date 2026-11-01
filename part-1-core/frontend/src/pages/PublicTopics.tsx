import { useCallback, useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { api } from '../lib/api';
import TheoryCard from '../components/visual/TheoryCard';
import './PublicTopics.css';

/* Public SEO pages: /topics and /topics/:slug (Hinglish, original),
   plus /en/topics and /en/topics/:slug (English chrome).
   These render OUTSIDE the login wall (see App.tsx) so search engines
   and visitors without an account can read real Learn content. They
   show only what the public content API returns — topics with zero
   theory blocks are hidden, never promised. Roadmap / practice /
   assessment stay behind login; this page says so honestly and links
   to /register instead of faking them.

   HONEST LANGUAGE RULE: stored theory blocks are written in Hinglish
   ("Variables: naam do, value rakho"). English pages translate the
   page chrome (headings, nav, CTAs, meta) but NEVER machine-translate
   the lesson blocks and never present a translation as the original:
   English detail pages show the blocks as stored, with a clear note
   that the lesson content is in Hinglish. */

type Lang = 'hi' | 'en';

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

const STRINGS: Record<Lang, {
  navTopics: string;
  navCerts: string;
  login: string;
  cta: string;
  footTagline: string;
  footAllTopics: string;
  indexTitle: string;
  indexDesc: string;
  indexH1: string;
  indexMuted: string;
  loadingTopics: string;
  errorTopics: string;
  emptyTopics: string;
  cardCta: string;
  back: string;
  loadingContent: string;
  errorContent: string;
  emptyContent: string;
  allLevels: string;
  ctaBox: string;
  langCurrent: string;
  langOther: string;
  langOtherLabel: string;
  noteHinglishContent: string;
  detailTitleSuffix: string;
}> = {
  hi: {
    navTopics: 'Topics',
    navCerts: 'Certificates',
    login: 'Login',
    cta: 'Free Account Banao',
    footTagline: 'SkillForge — seekho, practice karo, proof banao.',
    footAllTopics: 'Sab Topics',
    indexTitle: 'Free Topics — Python, DSA, ML Seekho Hinglish Me | SkillForge',
    indexDesc:
      'Python, DSA, ML aur career skills seekho Hinglish me, free me. Har topic pe theory padho, phir free account bana ke practice aur assessment do.',
    indexH1: '📖 Topics — Free Me Padho, Hinglish Me Samjho',
    indexMuted:
      'Python, DSA, ML — har topic ki theory yahan free me padh sakte ho, bina login ke. Practice, assessment aur roadmap ke liye free account banao.',
    loadingTopics: 'Topics load ho rahe hain…',
    errorTopics: 'Topics load nahi ho paye',
    emptyTopics: 'Abhi koi topic publish nahi hua hai — jald wapas aao.',
    cardCta: 'Theory padho →',
    back: '← Sab topics',
    loadingContent: 'Content load ho raha hai…',
    errorContent: 'Content load nahi ho paya',
    emptyContent: 'Is topic me abhi theory nahi hai.',
    allLevels: 'Sab levels',
    ctaBox: 'Theory padh li — ab practice, skill check aur apna roadmap chahiye?',
    langCurrent: 'Hinglish',
    langOther: 'English',
    langOtherLabel: 'Read this page in English',
    noteHinglishContent: '',
    detailTitleSuffix: 'Seekho Hinglish Me',
  },
  en: {
    navTopics: 'Topics',
    navCerts: 'Certificates',
    login: 'Login',
    cta: 'Create Free Account',
    footTagline: 'SkillForge — learn, practise, build proof.',
    footAllTopics: 'All Topics',
    indexTitle: 'Free Topics — Learn Python, DSA, ML in English | SkillForge',
    indexDesc:
      'Learn Python, DSA, ML and career skills in English, free. Read theory for every topic, then create a free account to practise and take assessments.',
    indexH1: '📖 Topics — Learn Free, in English',
    indexMuted:
      'Read theory for Python, DSA, ML and more here, free and without login. Create a free account for practice, assessments and your roadmap.',
    loadingTopics: 'Loading topics…',
    errorTopics: 'Could not load topics',
    emptyTopics: 'No topic published yet — check back soon.',
    cardCta: 'Read theory →',
    back: '← All topics',
    loadingContent: 'Loading content…',
    errorContent: 'Could not load content',
    emptyContent: 'No theory in this topic yet.',
    allLevels: 'All levels',
    ctaBox: "You've read the theory — now want practice, skill checks and your own roadmap?",
    langCurrent: 'English',
    langOther: 'Hinglish',
    langOtherLabel: 'Is page ko Hinglish me padho',
    noteHinglishContent:
      'Note: the lesson content below is written in Hinglish, as authored. All navigation and guidance on this page is in English.',
    detailTitleSuffix: 'Learn in English',
  },
};

/* SPA meta: sets title/description/OG tags + JSON-LD + hreflang
   alternates per page. Honest limit: crawlers that do not execute
   JavaScript see only the static index.html meta; Google renders JS,
   and /sitemap.xml lists every public URL (both languages) for
   discovery. */
function useSeo(opts: {
  title: string;
  description: string;
  jsonLd?: Record<string, unknown>;
  alternates?: { hi: string; en: string };
}) {
  const { title, description, jsonLd, alternates } = opts;
  useEffect(() => {
    document.title = title;
    const setMeta = (attr: string, key: string, value: string) => {
      let el = document.querySelector(`meta[${attr}="${key}"]`) as HTMLMetaElement | null;
      if (!el) {
        el = document.createElement('meta');
        el.setAttribute(attr, key);
        document.head.appendChild(el);
      }
      el.setAttribute('content', value);
    };
    setMeta('name', 'description', description);
    setMeta('property', 'og:title', title);
    setMeta('property', 'og:description', description);
    let script = document.querySelector('script[data-seo-jsonld]') as HTMLScriptElement | null;
    if (jsonLd) {
      if (!script) {
        script = document.createElement('script');
        script.type = 'application/ld+json';
        script.setAttribute('data-seo-jsonld', 'true');
        document.head.appendChild(script);
      }
      script.textContent = JSON.stringify(jsonLd);
    } else if (script) {
      script.remove();
    }
    if (alternates) {
      (Object.entries(alternates) as Array<['hi' | 'en', string]>).forEach(([hl, href]) => {
        let link = document.querySelector(
          `link[data-seo-alt="${hl}"]`
        ) as HTMLLinkElement | null;
        if (!link) {
          link = document.createElement('link');
          link.setAttribute('data-seo-alt', hl);
          document.head.appendChild(link);
        }
        link.setAttribute('rel', 'alternate');
        link.setAttribute('hreflang', hl);
        link.setAttribute('href', href);
      });
    }
  }, [title, description, jsonLd, alternates]);
}

/* Language switcher: preserves the page (index or same topic) across
   /topics/... <-> /en/topics/... . The current language is plain
   text; the other language is the link. */
function langUrls(lang: Lang, slug?: string): { current: string; other: string } {
  if (slug) {
    return lang === 'hi'
      ? { current: `/topics/${slug}`, other: `/en/topics/${slug}` }
      : { current: `/en/topics/${slug}`, other: `/topics/${slug}` };
  }
  return lang === 'hi'
    ? { current: '/topics', other: '/en/topics' }
    : { current: '/en/topics', other: '/topics' };
}

function PublicHeader({ lang, slug }: { lang: Lang; slug?: string }) {
  const s = STRINGS[lang];
  const urls = langUrls(lang, slug);
  return (
    <header className="pub-head">
      <div className="pub-head-inner">
        <Link to="/" className="pub-logo">SkillForge</Link>
        <nav className="pub-nav" aria-label="Public">
          <Link to={lang === 'hi' ? '/topics' : '/en/topics'}>{s.navTopics}</Link>
          <Link to="/directory">{s.navCerts}</Link>
        </nav>
        <div className="pub-actions">
          <span className="pub-lang" aria-label="Language">
            <span className="pub-lang-current" aria-current="true">{s.langCurrent}</span>
            {' · '}
            <Link to={urls.other} aria-label={s.langOtherLabel}>{s.langOther}</Link>
          </span>
          <Link to="/login" className="pub-link">{s.login}</Link>
          <Link to="/register" className="pub-cta">{s.cta}</Link>
        </div>
      </div>
    </header>
  );
}

function PublicFooter({ lang }: { lang: Lang }) {
  const s = STRINGS[lang];
  const indexUrl = lang === 'hi' ? '/topics' : '/en/topics';
  return (
    <footer className="pub-foot">
      <p>{s.footTagline}</p>
      <p className="pub-foot-links">
        <a href="/sitemap.xml">Sitemap</a>
        {' · '}
        <a href="/robots.txt">Robots</a>
        {' · '}
        <Link to={indexUrl}>{s.footAllTopics}</Link>
      </p>
    </footer>
  );
}

const LEVEL_LABEL: Record<string, string> = {
  beginner: '🌱 Beginner',
  intermediate: '🌿 Intermediate',
  advanced: '🌳 Advanced',
  expert: '🔥 Expert',
};

function TopicIndex({ lang }: { lang: Lang }) {
  const s = STRINGS[lang];
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const origin = typeof window !== 'undefined' ? window.location.origin : '';

  useSeo({
    title: s.indexTitle,
    description: s.indexDesc,
    jsonLd: {
      '@context': 'https://schema.org',
      '@type': 'CollectionPage',
      name: lang === 'hi' ? 'SkillForge free topics' : 'SkillForge free topics (English)',
      description: s.indexDesc,
      ...(lang === 'en' ? { inLanguage: 'en' } : {}),
    },
    alternates: { hi: `${origin}/topics`, en: `${origin}/en/topics` },
  });

  useEffect(() => {
    (async () => {
      try {
        const r = await api<{ topics: Topic[] }>('/api/v1/content/topics');
        // Same honest rule as Learn: hide topics with no theory content.
        setTopics(r.topics.filter((t) => (t.theory_count ?? 0) > 0));
      } catch (e) {
        setError(e instanceof Error ? e.message : s.errorTopics);
      } finally {
        setLoading(false);
      }
    })();
  }, [s.errorTopics]);

  const detailBase = lang === 'hi' ? '/topics' : '/en/topics';

  return (
    <div className="pub-page">
      <PublicHeader lang={lang} />
      <main className="pub-wrap">
        <h1>{s.indexH1}</h1>
        <p className="pub-muted">{s.indexMuted}</p>
        {loading && <p className="pub-muted">{s.loadingTopics}</p>}
        {error && <p className="pub-error">{error}</p>}
        {!loading && !error && topics.length === 0 && (
          <p className="pub-muted">{s.emptyTopics}</p>
        )}
        <div className="pub-grid">
          {topics.map((t) => (
            <Link key={t.slug} to={`${detailBase}/${t.slug}`} className="pub-card">
              <span className="pub-card-icon">{t.icon || '📘'}</span>
              <span className="pub-card-name">{t.name}</span>
              {t.description && <span className="pub-card-desc">{t.description}</span>}
              <span className="pub-card-cta">{s.cardCta}</span>
            </Link>
          ))}
        </div>
      </main>
      <PublicFooter lang={lang} />
    </div>
  );
}

function TopicDetail({ lang }: { lang: Lang }) {
  const s = STRINGS[lang];
  const { slug } = useParams<{ slug: string }>();
  const [topic, setTopic] = useState<Topic | null>(null);
  const [blocks, setBlocks] = useState<TheoryBlock[]>([]);
  const [level, setLevel] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const origin = typeof window !== 'undefined' ? window.location.origin : '';

  const topicTitle = topic ? `${topic.name} ${s.detailTitleSuffix} | SkillForge` : 'Topic | SkillForge';
  const topicDesc = topic
    ? lang === 'hi'
      ? `${topic.name} ki theory Hinglish me padho${topic.description ? ` — ${topic.description}` : ''}. Practice aur assessment ke liye free account banao.`
      : `Read ${topic.name} theory${topic.description ? ` — ${topic.description}` : ''}. Create a free account for practice and assessments.`
    : lang === 'hi'
      ? 'SkillForge free topic theory, Hinglish me.'
      : 'SkillForge free topic theory, in English.';
  useSeo({
    title: topicTitle,
    description: topicDesc,
    jsonLd: topic
      ? {
          '@context': 'https://schema.org',
          '@type': 'LearningResource',
          name: topic.name,
          description: topic.description || topicDesc,
          learningResourceType: 'theory',
          ...(lang === 'en' ? { inLanguage: 'en' } : {}),
        }
      : undefined,
    alternates: slug
      ? { hi: `${origin}/topics/${slug}`, en: `${origin}/en/topics/${slug}` }
      : undefined,
  });

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
      setError(e instanceof Error ? e.message : s.errorContent);
    } finally {
      setLoading(false);
    }
  }, [slug, s.errorContent]);

  useEffect(() => { load(level); }, [load, level]);

  const indexUrl = lang === 'hi' ? '/topics' : '/en/topics';

  return (
    <div className="pub-page">
      <PublicHeader lang={lang} slug={slug} />
      <main className="pub-wrap">
        <Link to={indexUrl} className="pub-back">{s.back}</Link>
        {loading && <p className="pub-muted">{s.loadingContent}</p>}
        {error && <p className="pub-error">{error}</p>}
        {!loading && !error && topic && (
          <>
            <h1>{topic.icon} {topic.name}</h1>
            {topic.description && <p className="pub-muted">{topic.description}</p>}
            <div className="pub-filters">
              {['', 'beginner', 'intermediate', 'advanced', 'expert'].map((lv) => (
                <button
                  key={lv || 'all'}
                  className={`pub-chip${level === lv ? ' active' : ''}`}
                  onClick={() => setLevel(lv)}
                >
                  {lv === '' ? s.allLevels : LEVEL_LABEL[lv]}
                </button>
              ))}
            </div>
            {blocks.length === 0 ? (
              <p className="pub-muted">{s.emptyContent}</p>
            ) : (
              <>
                {lang === 'en' && s.noteHinglishContent && (
                  <p className="pub-note">{s.noteHinglishContent}</p>
                )}
                <div className="pub-blocks">
                  {blocks.map((b) => (
                    <TheoryCard key={b.id} title={b.title} content={b.content} />
                  ))}
                </div>
              </>
            )}
            <div className="pub-cta-box">
              <p><strong>{lang === 'hi' ? 'Aage kya?' : "What's next?"}</strong> {s.ctaBox}</p>
              <Link to="/register" className="pub-cta">{s.cta} →</Link>
            </div>
          </>
        )}
      </main>
      <PublicFooter lang={lang} />
    </div>
  );
}

export default function PublicTopics({ lang = 'hi' }: { lang?: Lang }) {
  const { slug } = useParams<{ slug: string }>();
  return slug ? <TopicDetail lang={lang} /> : <TopicIndex lang={lang} />;
}
