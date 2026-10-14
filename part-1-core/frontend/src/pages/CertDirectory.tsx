import { useMemo, useState } from 'react';
import { useLang } from '../lib/i18n';
import type { TKey } from '../lib/translations';
import certsData from '../data/certificates.json';
import './CertDirectory.css';

interface CertEntry {
  id: string;
  platform: string;
  title: string;
  domain: string;
  duration: string;
  price: string;
  priceTier: 'free' | 'budget' | 'premium';
  url: string;
  description: string;
  skills: string[];
}

type Tier = 'free' | 'budget' | 'premium';

const ENTRIES = certsData as CertEntry[];
const TIERS: Tier[] = ['free', 'budget', 'premium'];
const TAB_KEYS: Record<Tier, TKey> = {
  free: 'certs.dir.tab.free',
  budget: 'certs.dir.tab.budget',
  premium: 'certs.dir.tab.premium',
};

export default function CertDirectory() {
  const { t } = useLang();
  const [tier, setTier] = useState<Tier>('free');
  const [query, setQuery] = useState('');
  const [domain, setDomain] = useState<string>('__all');

  const domains = useMemo(() => {
    const seen = new Set<string>();
    for (const c of ENTRIES) if (c.priceTier === tier) seen.add(c.domain);
    return [...seen].sort();
  }, [tier]);

  const results = useMemo(() => {
    const q = query.trim().toLowerCase();
    return ENTRIES.filter((c) => {
      if (c.priceTier !== tier) return false;
      if (domain !== '__all' && c.domain !== domain) return false;
      if (!q) return true;
      const hay = `${c.title} ${c.platform} ${c.domain} ${c.skills.join(' ')}`.toLowerCase();
      return hay.includes(q);
    });
  }, [tier, query, domain]);

  const pickTier = (nt: Tier) => {
    setTier(nt);
    setDomain('__all');
  };

  return (
    <div className="certdir">
      <header className="certdir-head">
        <h1 className="certdir-title">{t('certs.dir.title')}</h1>
        <p className="certdir-sub">{t('certs.dir.subtitle')}</p>
      </header>

      <div className="certdir-tabs" role="tablist">
        {TIERS.map((k) => (
          <button
            key={k}
            role="tab"
            aria-selected={tier === k}
            className={`certdir-tab${tier === k ? ' active' : ''}`}
            onClick={() => pickTier(k)}
          >
            {t(TAB_KEYS[k])}
          </button>
        ))}
      </div>

      <div className="certdir-controls">
        <input
          className="certdir-search"
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={t('certs.dir.search')}
          aria-label={t('certs.dir.search')}
        />
        <div className="certdir-chips">
          <button
            className={`certdir-chip${domain === '__all' ? ' active' : ''}`}
            onClick={() => setDomain('__all')}
          >
            {t('certs.dir.filter.all')}
          </button>
          {domains.map((d) => (
            <button
              key={d}
              className={`certdir-chip${domain === d ? ' active' : ''}`}
              onClick={() => setDomain(d)}
            >
              {d}
            </button>
          ))}
        </div>
      </div>

      {results.length === 0 ? (
        <p className="certdir-empty">{t('certs.dir.empty')}</p>
      ) : (
        <div className="certdir-grid">
          {results.map((c) => (
            <article key={c.id} className="certdir-card">
              <div className="certdir-top">
                <span className="certdir-platform">{c.platform}</span>
                <span className={`certdir-price ${c.priceTier}`}>
                  {c.price}
                </span>
              </div>
              <h3 className="certdir-card-title">{c.title}</h3>
              <p className="certdir-desc">{c.description}</p>
              <div className="certdir-meta">
                <span className="certdir-domain">{c.domain}</span>
                <span className="certdir-duration">{c.duration}</span>
              </div>
              <div className="certdir-skills">
                {c.skills.map((s) => (
                  <span key={s} className="certdir-skill">{s}</span>
                ))}
              </div>
              <a
                className="certdir-btn"
                href={c.url}
                target="_blank"
                rel="noopener noreferrer"
              >
                {t('certs.dir.view')}
              </a>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
