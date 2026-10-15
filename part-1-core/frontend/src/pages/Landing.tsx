import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useLang } from '../lib/i18n';
import type { TKey } from '../lib/translations';
import './Landing.css';

const SEO_TITLE = 'SkillForge — From Learner to Job-Ready Engineer';
const SEO_DESC =
  'SkillForge assesses your skills, finds your gaps, and builds a personalized roadmap — with real code practice, projects, and proof of work.';

function setMeta(name: string, content: string, attr: 'name' | 'property' = 'name') {
  let el = document.querySelector(`meta[${attr}="${name}"]`) as HTMLMetaElement | null;
  if (!el) {
    el = document.createElement('meta');
    el.setAttribute(attr, name);
    document.head.appendChild(el);
  }
  el.setAttribute('content', content);
}

function setCanonical() {
  let el = document.querySelector('link[rel="canonical"]') as HTMLLinkElement | null;
  if (!el) {
    el = document.createElement('link');
    el.setAttribute('rel', 'canonical');
    document.head.appendChild(el);
  }
  el.setAttribute('href', window.location.origin + '/');
}

const tk = (s: string): TKey => s as TKey;

function IconTarget() {
  return (
    <svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round">
      <circle cx="12" cy="12" r="9" /><circle cx="12" cy="12" r="5" /><circle cx="12" cy="12" r="1.4" fill="currentColor" />
    </svg>
  );
}
function IconMap() {
  return (
    <svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2Z" /><path d="M9 4v14M15 6v14" />
    </svg>
  );
}
function IconCode() {
  return (
    <svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="m8 8-5 4 5 4M16 8l5 4-5 4M13 4l-2 16" />
    </svg>
  );
}
function IconAward() {
  return (
    <svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="9" r="6" /><path d="M8.5 14 7 22l5-3 5 3-1.5-8" />
    </svg>
  );
}

export default function Landing() {
  const { t, lang, setLang, languages } = useLang();
  const [langOpen, setLangOpen] = useState(false);
  const [openFaq, setOpenFaq] = useState<number | null>(null);

  useEffect(() => {
    document.title = SEO_TITLE;
    setMeta('description', SEO_DESC);
    setMeta('og:title', SEO_TITLE, 'property');
    setMeta('og:description', SEO_DESC, 'property');
    setMeta('og:type', 'website', 'property');
    setCanonical();
  }, []);

  const features = [
    { icon: <IconTarget />, title: t('landing.features.assess.title'), desc: t('landing.features.assess.desc'), accent: 'violet' },
    { icon: <IconMap />, title: t('landing.features.roadmap.title'), desc: t('landing.features.roadmap.desc'), accent: 'cyan' },
    { icon: <IconCode />, title: t('landing.features.code.title'), desc: t('landing.features.code.desc'), accent: 'magenta' },
    { icon: <IconAward />, title: t('landing.features.certs.title'), desc: t('landing.features.certs.desc'), accent: 'green' },
  ];

  const steps = [1, 2, 3, 4].map((n) => ({
    n,
    title: t(tk(`landing.how.step${n}.title`)),
    desc: t(tk(`landing.how.step${n}.desc`)),
  }));

  const heroStats = [1, 2, 3].map((n) => ({
    value: t(tk(`landing.hero.stat${n}.value`)),
    label: t(tk(`landing.hero.stat${n}.label`)),
  }));

  const bandStats = [1, 2, 3, 4].map((n) => ({
    value: t(tk(`landing.stats.s${n}.value`)),
    label: t(tk(`landing.stats.s${n}.label`)),
  }));

  const tiers: Array<{
    name: string; price: string; period: string; desc: string; cta: string;
    badge?: string; popular?: boolean; feats: string[];
  }> = (['free', 'pro', 'expert'] as const).map((tier) => ({
    name: t(tk(`landing.pricing.${tier}.name`)),
    price: t(tk(`landing.pricing.${tier}.price`)),
    period: t(tk(`landing.pricing.${tier}.period`)),
    desc: t(tk(`landing.pricing.${tier}.desc`)),
    cta: t(tk(`landing.pricing.${tier}.cta`)),
    badge: tier === 'pro' ? t('landing.pricing.pro.badge') : undefined,
    popular: tier === 'pro',
    feats: [1, 2, 3, 4].map((f) => t(tk(`landing.pricing.${tier}.f${f}`))),
  }));

  const faqs = [1, 2, 3, 4, 5, 6].map((n) => ({
    q: t(tk(`landing.faq.q${n}`)),
    a: t(tk(`landing.faq.a${n}`)),
  }));

  const currentLang = languages.find((l) => l.code === lang);

  return (
    <div className="ld-page">
      {/* ============ NAV ============ */}
      <header className="ld-nav">
        <div className="ld-nav-inner">
          <Link to="/" className="ld-logo" aria-label="SkillForge home">
            <span className="ld-logo-mark">⬡</span>
            <span className="ld-logo-text">SKILLFORGE</span>
          </Link>
          <nav className="ld-nav-links" aria-label="Primary">
            <a href="#features">{t('nav.features')}</a>
            <a href="#features">{t('nav.certificates')}</a>
            <a href="#pricing">{t('nav.pricing')}</a>
          </nav>
          <div className="ld-nav-actions">
            <div className="ld-lang">
              <button
                className="ld-lang-btn"
                onClick={() => setLangOpen((o) => !o)}
                aria-haspopup="listbox"
                aria-expanded={langOpen}
                aria-label={t('common.language')}
              >
                🌐 {currentLang?.native}
                <span className="ld-caret">▾</span>
              </button>
              {langOpen && (
                <ul className="ld-lang-menu" role="listbox" aria-label={t('common.language')}>
                  {languages.map((l) => (
                    <li key={l.code} role="option" aria-selected={l.code === lang}>
                      <button
                        className={l.code === lang ? 'active' : ''}
                        onClick={() => { setLang(l.code); setLangOpen(false); }}
                      >
                        {l.native}
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>
            <Link to="/login" className="btn-ghost ld-nav-btn">{t('nav.login')}</Link>
            <Link to="/register" className="btn-primary ld-nav-btn">{t('nav.signup')}</Link>
          </div>
        </div>
      </header>

      <main>
        {/* ============ HERO ============ */}
        <section className="ld-hero" aria-labelledby="ld-hero-title">
          <div className="ld-hero-bg" aria-hidden="true" />
          <div className="ld-hero-inner">
            <span className="ld-badge">{t('landing.hero.badge')}</span>
            <h1 id="ld-hero-title">{t('landing.hero.title')}</h1>
            <p className="ld-hero-sub">{t('landing.hero.subtitle')}</p>
            <div className="ld-hero-ctas">
              <Link to="/register" className="btn-primary ld-cta-lg">{t('landing.hero.cta.start')}</Link>
              <Link to="/login" className="btn-ghost ld-cta-lg">{t('landing.hero.cta.login')}</Link>
            </div>
            <div className="ld-hero-stats">
              {heroStats.map((s) => (
                <div key={s.label} className="ld-hero-stat">
                  <div className="ld-hero-stat-v">{s.value}</div>
                  <div className="ld-hero-stat-l">{s.label}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ============ FEATURES ============ */}
        <section id="features" className="ld-section" aria-labelledby="ld-features-title">
          <div className="ld-wrap">
            <h2 id="ld-features-title" className="ld-h2">{t('landing.features.title')}</h2>
            <div className="ld-grid-4">
              {features.map((f) => (
                <article key={f.title} className={`card ld-card accent-${f.accent}`}>
                  <div className="ld-card-icon">{f.icon}</div>
                  <h3>{f.title}</h3>
                  <p>{f.desc}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        {/* ============ HOW IT WORKS ============ */}
        <section id="how" className="ld-section ld-alt" aria-labelledby="ld-how-title">
          <div className="ld-wrap">
            <h2 id="ld-how-title" className="ld-h2">{t('landing.how.title')}</h2>
            <ol className="ld-steps">
              {steps.map((s) => (
                <li key={s.n} className="ld-step">
                  <div className="ld-step-n" aria-hidden="true">{s.n}</div>
                  <h3>{s.title}</h3>
                  <p>{s.desc}</p>
                </li>
              ))}
            </ol>
          </div>
        </section>

        {/* ============ STATS BAND ============ */}
        <section className="ld-stats-band" aria-label={t('landing.stats.title')}>
          <div className="ld-wrap ld-stats-grid">
            {bandStats.map((s) => (
              <div key={s.label} className="ld-band-stat">
                <div className="ld-band-v">{s.value}</div>
                <div className="ld-band-l">{s.label}</div>
              </div>
            ))}
          </div>
        </section>

        {/* ============ PRICING ============ */}
        <section id="pricing" className="ld-section" aria-labelledby="ld-pricing-title">
          <div className="ld-wrap">
            <h2 id="ld-pricing-title" className="ld-h2">{t('landing.pricing.title')}</h2>
            <p className="ld-sub">{t('landing.pricing.subtitle')}</p>
            <div className="ld-grid-3">
              {tiers.map((tier) => (
                <article key={tier.name} className={`tier-card${tier.popular ? ' popular' : ''}`}>
                  {tier.badge && <div className="ld-tier-badge">{tier.badge}</div>}
                  <h3>{tier.name}</h3>
                  <p className="tier-desc">{tier.desc}</p>
                  <div className="price">{tier.price}<small>{tier.period}</small></div>
                  <ul>
                    {tier.feats.map((f) => <li key={f}>{f}</li>)}
                  </ul>
                  <Link
                    to="/register"
                    className={tier.popular ? 'btn-primary ld-tier-cta' : 'btn-ghost ld-tier-cta'}
                  >
                    {tier.cta}
                  </Link>
                </article>
              ))}
            </div>
          </div>
        </section>

        {/* ============ FAQ ============ */}
        <section id="faq" className="ld-section ld-alt" aria-labelledby="ld-faq-title">
          <div className="ld-wrap ld-faq-wrap">
            <h2 id="ld-faq-title" className="ld-h2">{t('landing.faq.title')}</h2>
            <div className="ld-faq-list">
              {faqs.map((f, i) => {
                const open = openFaq === i;
                return (
                  <div key={f.q} className={`ld-faq-item${open ? ' open' : ''}`}>
                    <button
                      className="ld-faq-q"
                      onClick={() => setOpenFaq(open ? null : i)}
                      aria-expanded={open}
                      aria-controls={`ld-faq-a${i}`}
                    >
                      <span>{f.q}</span>
                      <span className="ld-faq-plus" aria-hidden="true">{open ? '−' : '+'}</span>
                    </button>
                    {open && (
                      <div id={`ld-faq-a${i}`} className="ld-faq-a">
                        <p>{f.a}</p>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* ============ FINAL CTA ============ */}
        <section className="ld-section ld-final" aria-labelledby="ld-cta-title">
          <div className="ld-wrap ld-final-inner">
            <h2 id="ld-cta-title">{t('landing.cta.title')}</h2>
            <Link to="/register" className="btn-primary ld-cta-lg">{t('landing.cta.button')}</Link>
          </div>
        </section>
      </main>

      {/* ============ FOOTER ============ */}
      <footer className="ld-footer">
        <div className="ld-wrap ld-footer-grid">
          <div className="ld-footer-brand">
            <span className="ld-logo-mark">⬡</span>
            <span className="ld-logo-text">SKILLFORGE</span>
            <p>{t('landing.footer.tagline')}</p>
          </div>
          <nav aria-label={t('landing.footer.product')}>
            <h4>{t('landing.footer.product')}</h4>
            <a href="#features">{t('nav.features')}</a>
            <a href="#pricing">{t('nav.pricing')}</a>
            <Link to="/register">{t('nav.signup')}</Link>
          </nav>
          <nav aria-label={t('landing.footer.resources')}>
            <h4>{t('landing.footer.resources')}</h4>
            <a href="#faq">{t('landing.faq.title')}</a>
            <Link to="/login">{t('nav.login')}</Link>
          </nav>
        </div>
        <div className="ld-footer-bottom">
          © {new Date().getFullYear()} SkillForge. {t('landing.footer.rights')}
        </div>
      </footer>
    </div>
  );
}
