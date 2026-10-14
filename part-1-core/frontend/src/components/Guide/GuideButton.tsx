import { useLang } from '../../lib/i18n';

interface Props {
  open: boolean;
  onToggle: () => void;
}

/* Floating action button — bottom-right, aurora gradient, pulse ring. */
export default function GuideButton({ open, onToggle }: Props) {
  const { t } = useLang();
  return (
    <button
      type="button"
      className={`guide-fab${open ? ' is-open' : ''}`}
      onClick={onToggle}
      aria-label={t('guide.button')}
      aria-expanded={open}
      title={t('guide.button')}
    >
      <span className="guide-fab-ring" aria-hidden="true" />
      <span className="guide-fab-icon" aria-hidden="true">
        {open ? '✕' : '🤖'}
      </span>
    </button>
  );
}
