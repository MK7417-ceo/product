import { useEffect, useState } from 'react';
import { useLang } from '../../lib/i18n';
import { tourSteps, ui } from './guideBrain';

interface Props {
  onDone: () => void;
}

/* Centered card walkthrough — 5 steps, progress dots, Next/Back/Skip. */
export default function GuideTour({ onDone }: Props) {
  const { lang } = useLang();
  const [idx, setIdx] = useState(0);
  const steps = tourSteps(lang);
  const step = steps[idx];
  const last = idx === steps.length - 1;

  /* Escape skips the tour */
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onDone();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onDone]);

  /* lock body scroll while touring */
  useEffect(() => {
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = prev;
    };
  }, []);

  return (
    <div className="guide-tour-overlay" role="dialog" aria-modal="true" aria-label={step.title}>
      <div className="guide-tour-card" key={`${lang}-${idx}`}>
        <div className="guide-tour-emoji" aria-hidden="true">
          {['👋', '🏠', '📝', '🗺️', '🏆'][idx] ?? '🤖'}
        </div>
        <p className="guide-tour-kicker">
          {ui(lang, 'tourStepOf')} {idx + 1} / {steps.length}
        </p>
        <h3 className="guide-tour-title">{step.title}</h3>
        <p className="guide-tour-text">{step.text}</p>

        <div className="guide-tour-dots" aria-hidden="true">
          {steps.map((_, i) => (
            <span key={i} className={`tour-dot${i === idx ? ' active' : ''}${i < idx ? ' done' : ''}`} />
          ))}
        </div>

        <div className="guide-tour-actions">
          <button type="button" className="guide-tour-skip" onClick={onDone}>
            {ui(lang, 'tourSkip')}
          </button>
          <div className="guide-tour-nav">
            {idx > 0 && (
              <button
                type="button"
                className="guide-tour-back"
                onClick={() => setIdx((i) => i - 1)}
              >
                {ui(lang, 'tourBack')}
              </button>
            )}
            <button
              type="button"
              className="guide-tour-next"
              onClick={() => (last ? onDone() : setIdx((i) => i + 1))}
            >
              {last ? ui(lang, 'tourDone') : ui(lang, 'tourNext')}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
