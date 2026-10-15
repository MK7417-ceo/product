import { createContext, useCallback, useContext, useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import { languages, translations } from './translations';
import type { LangCode, TKey } from './translations';

interface LangCtx {
  lang: LangCode;
  setLang: (l: LangCode) => void;
  t: (key: TKey, fallback?: string) => string;
  languages: typeof languages;
}

const Ctx = createContext<LangCtx | null>(null);
const KEY = 'sf-lang';

function detect(): LangCode {
  try {
    const saved = localStorage.getItem(KEY) as LangCode | null;
    if (saved && (['en', 'hi', 'hinglish'] as string[]).includes(saved)) return saved;
  } catch { /* ignore */ }
  return 'en';
}

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<LangCode>(detect);

  const setLang = useCallback((l: LangCode) => {
    setLangState(l);
    try { localStorage.setItem(KEY, l); } catch { /* ignore */ }
    document.documentElement.lang = l === 'hi' ? 'hi' : 'en';
  }, []);

  useEffect(() => {
    document.documentElement.lang = lang === 'hi' ? 'hi' : 'en';
  }, [lang]);

  const t = useCallback((key: TKey, fallback?: string): string => {
    return translations[lang][key] ?? translations.en[key] ?? fallback ?? key;
  }, [lang]);

  return <Ctx.Provider value={{ lang, setLang, t, languages }}>{children}</Ctx.Provider>;
}

export function useLang(): LangCtx {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error('useLang must be used inside LanguageProvider');
  return ctx;
}
