import { useCallback, useEffect, useRef, useState } from 'react';
import type { LangCode } from '../../lib/translations';
import './visual.css';

interface Props {
  /** Plain text to read aloud. */
  text: string;
  /** Language used to pick the best voice. 'hinglish' uses an English voice. */
  lang?: LangCode;
  className?: string;
}

type Status = 'idle' | 'speaking';

const CHUNK_LEN = 220;

/* Split long theory into speakable chunks at sentence boundaries.
   (Some browsers cut off very long single utterances.) */
function splitIntoChunks(text: string): string[] {
  const flat = text.replace(/\s+/g, ' ').trim();
  if (!flat) return [];
  const sentences = flat.match(/[^.!?]+[.!?]+["')]?|.+$/g) ?? [flat];
  const chunks: string[] = [];
  let cur = '';
  for (const s of sentences) {
    const t = s.trim();
    if (!t) continue;
    if (cur && (cur + ' ' + t).length > CHUNK_LEN) {
      chunks.push(cur);
      cur = t;
    } else {
      cur = cur ? `${cur} ${t}` : t;
    }
  }
  if (cur) chunks.push(cur);
  return chunks;
}

function pickVoice(voices: SpeechSynthesisVoice[], lang: LangCode): SpeechSynthesisVoice | null {
  if (voices.length === 0) return null;
  const want = lang === 'hi' ? 'hi' : 'en';
  return (
    voices.find((v) => v.lang.toLowerCase().startsWith(want) && v.localService) ??
    voices.find((v) => v.lang.toLowerCase().startsWith(want)) ??
    voices.find((v) => v.default) ??
    voices[0] ??
    null
  );
}

/* 🔊 Free text-to-speech via the browser's speechSynthesis API.
   No network calls, no API keys. Toggle to play/stop. */
export default function ListenButton({ text, lang = 'en', className = '' }: Props) {
  const [status, setStatus] = useState<Status>('idle');
  const chunksRef = useRef<string[]>([]);
  const runIdRef = useRef(0);
  const langRef = useRef(lang);
  langRef.current = lang;

  const supported = typeof window !== 'undefined' && 'speechSynthesis' in window;

  /* Preload voices (Chrome fills them in asynchronously) + cleanup on unmount. */
  useEffect(() => {
    if (!supported) return;
    const synth = window.speechSynthesis;
    const load = () => {
      void pickVoice(synth.getVoices(), langRef.current);
    };
    load();
    synth.addEventListener('voiceschanged', load);
    return () => {
      synth.removeEventListener('voiceschanged', load);
      synth.cancel();
    };
  }, [supported]);

  const speakChunk = useCallback((run: number, i: number) => {
    if (runIdRef.current !== run) return;
    const synth = window.speechSynthesis;
    const chunks = chunksRef.current;
    if (i >= chunks.length) {
      setStatus('idle');
      return;
    }
    const u = new SpeechSynthesisUtterance(chunks[i]);
    const voice = pickVoice(synth.getVoices(), langRef.current);
    if (voice) {
      u.voice = voice;
      u.lang = voice.lang;
    } else {
      u.lang = langRef.current === 'hi' ? 'hi-IN' : 'en-US';
    }
    u.rate = 1;
    u.onend = () => speakChunk(run, i + 1);
    u.onerror = () => {
      if (runIdRef.current === run) setStatus('idle');
    };
    synth.speak(u);
  }, []);

  const stop = useCallback(() => {
    runIdRef.current += 1; // invalidate any queued onend callbacks
    if (supported) window.speechSynthesis.cancel();
    setStatus('idle');
  }, [supported]);

  const toggle = useCallback(() => {
    if (!supported || !text.trim()) return;
    if (status === 'speaking') {
      stop();
      return;
    }
    window.speechSynthesis.cancel();
    chunksRef.current = splitIntoChunks(text);
    if (chunksRef.current.length === 0) return;
    const run = runIdRef.current + 1;
    runIdRef.current = run;
    setStatus('speaking');
    speakChunk(run, 0);
  }, [supported, status, stop, speakChunk, text]);

  if (!supported) return null;

  const speaking = status === 'speaking';
  return (
    <button
      type="button"
      className={`visual-listen${speaking ? ' is-speaking' : ''}${className ? ` ${className}` : ''}`}
      onClick={toggle}
      aria-label={speaking ? 'Stop reading aloud' : 'Listen to this theory'}
      aria-pressed={speaking}
      title={speaking ? 'Stop' : 'Listen 🔊'}
    >
      <span aria-hidden="true">{speaking ? '⏹' : '🔊'}</span>
      <span className="visual-listen-label">{speaking ? 'Stop' : 'Listen'}</span>
      {speaking && (
        <span className="visual-listen-bars" aria-hidden="true">
          <i />
          <i />
          <i />
        </span>
      )}
    </button>
  );
}
