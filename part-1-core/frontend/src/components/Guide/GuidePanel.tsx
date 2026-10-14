import { useEffect, useRef, useState } from 'react';
import { useLang } from '../../lib/i18n';
import type { LangCode } from '../../lib/translations';
import {
  answer,
  quickChips,
  ui,
  welcomeMessage,
  type ChatMessage,
} from './guideBrain';

interface Props {
  onStartTour: () => void;
  onClose: () => void;
}

let msgId = 1;

/* Chat panel: header w/ language chips, messages, quick chips, input. */
export default function GuidePanel({ onStartTour, onClose }: Props) {
  const { lang, setLang, languages } = useLang();
  const [messages, setMessages] = useState<ChatMessage[]>(() => [
    { id: msgId++, from: 'bot', text: welcomeMessage(lang) },
  ]);
  const [input, setInput] = useState('');
  const [typing, setTyping] = useState(false);
  const bodyRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const timerRef = useRef<number | null>(null);

  /* auto-scroll on new messages */
  useEffect(() => {
    const el = bodyRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages, typing]);

  /* focus input when panel opens */
  useEffect(() => {
    inputRef.current?.focus();
    return () => {
      if (timerRef.current) window.clearTimeout(timerRef.current);
    };
  }, []);

  /* Escape closes the panel */
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onClose]);

  const pushBot = (text: string) => {
    setTyping(true);
    timerRef.current = window.setTimeout(() => {
      setMessages((m) => [...m, { id: msgId++, from: 'bot', text }]);
      setTyping(false);
    }, 450);
  };

  const handleSend = (raw: string) => {
    const text = raw.trim();
    if (!text || typing) return;
    setMessages((m) => [...m, { id: msgId++, from: 'user', text }]);
    setInput('');
    pushBot(answer(text, lang));
  };

  const handleChip = (chipId: string, query: string) => {
    if (chipId === 'tour') {
      onStartTour();
      return;
    }
    handleSend(query);
  };

  const switchLang = (l: LangCode) => {
    setLang(l);
  };

  return (
    <section className="guide-panel" role="dialog" aria-label={ui(lang, 'title')}>
      {/* header */}
      <header className="guide-header">
        <div className="guide-header-bot" aria-hidden="true">
          🤖
        </div>
        <div className="guide-header-text">
          <strong>{ui(lang, 'title')}</strong>
          <span>{ui(lang, 'subtitle')}</span>
        </div>
        <div className="guide-lang-chips" role="group" aria-label="Language">
          {languages.map((l) => (
            <button
              key={l.code}
              type="button"
              className={`guide-lang-chip${lang === l.code ? ' active' : ''}`}
              onClick={() => switchLang(l.code)}
              aria-pressed={lang === l.code}
            >
              {l.code === 'en' ? 'EN' : l.code === 'hi' ? 'हिं' : 'Hing'}
            </button>
          ))}
        </div>
        <button
          type="button"
          className="guide-close"
          onClick={onClose}
          aria-label={ui(lang, 'close')}
        >
          ✕
        </button>
      </header>

      {/* messages */}
      <div className="guide-body" ref={bodyRef} aria-live="polite">
        {messages.map((m) => (
          <div key={m.id} className={`guide-msg ${m.from}`}>
            {m.from === 'bot' && (
              <span className="guide-msg-avatar" aria-hidden="true">
                🤖
              </span>
            )}
            <p className="guide-bubble">{m.text}</p>
          </div>
        ))}
        {typing && (
          <div className="guide-msg bot">
            <span className="guide-msg-avatar" aria-hidden="true">
              🤖
            </span>
            <p className="guide-bubble typing">
              <span className="dot" />
              <span className="dot" />
              <span className="dot" />
              <span className="sr-only">{ui(lang, 'typing')}</span>
            </p>
          </div>
        )}
      </div>

      {/* quick chips */}
      <div className="guide-chips">
        {quickChips.map((c) => (
          <button
            key={c.id}
            type="button"
            className="guide-chip"
            onClick={() => handleChip(c.id, c.query)}
          >
            {c.label[lang]}
          </button>
        ))}
      </div>

      {/* input */}
      <form
        className="guide-input-row"
        onSubmit={(e) => {
          e.preventDefault();
          handleSend(input);
        }}
      >
        <input
          ref={inputRef}
          className="guide-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={ui(lang, 'placeholder')}
          aria-label={ui(lang, 'placeholder')}
          maxLength={500}
        />
        <button
          type="submit"
          className="guide-send"
          disabled={!input.trim() || typing}
          aria-label={ui(lang, 'send')}
        >
          ➤
        </button>
      </form>
    </section>
  );
}
