import { useEffect, useState } from 'react';
import { codeApi, ApiError, type CodeRunResult, type EngineLanguage } from '../lib/api';

const STARTER: Record<string, string> = {
  python: 'def solve():\n    # apna code yahan likho\n    print("hello skillforge")\n\nsolve()\n',
  c: '#include <stdio.h>\n\nint main() {\n    printf("hello skillforge\\n");\n    return 0;\n}\n',
  cpp: '#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    cout << "hello skillforge" << endl;\n    return 0;\n}\n',
  java: 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("hello skillforge");\n    }\n}\n',
};

const VERDICT_COLOR: Record<string, string> = {
  OK: '#4ade80',
  COMPILE_ERROR: '#fbbf24',
  RUNTIME_ERROR: '#f87171',
  TLE: '#fb923c',
  MLE: '#c084fc',
};

export default function Code() {
  const [langs, setLangs] = useState<EngineLanguage[]>([]);
  const [lang, setLang] = useState('cpp');
  const [code, setCode] = useState(STARTER.cpp);
  const [stdin, setStdin] = useState('');
  const [result, setResult] = useState<CodeRunResult | null>(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    codeApi.languages().then((r) => setLangs(r.languages)).catch(() => {});
    const saved = localStorage.getItem('sf-code-cpp');
    if (saved) setCode(saved);
  }, []);

  const switchLang = (l: string) => {
    localStorage.setItem(`sf-code-${lang}`, code);
    setLang(l);
    setCode(localStorage.getItem(`sf-code-${l}`) || STARTER[l] || '');
    setResult(null);
  };

  const onCode = (v: string) => {
    setCode(v);
    localStorage.setItem(`sf-code-${lang}`, v);
  };

  const run = async () => {
    if (busy || !code.trim()) return;
    setError('');
    setBusy(true);
    setResult(null);
    try {
      setResult(await codeApi.run(lang, code, stdin));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Run failed');
    } finally {
      setBusy(false);
    }
  };

  const onKey = (e: React.KeyboardEvent) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      run();
    }
  };

  return (
    <div onKeyDown={onKey}>
      <h1 className="page-title">Code Runner</h1>
      <p className="page-sub">Browser mein likho, sandboxed engine par chalao. Ctrl+Enter = run.</p>
      {error && <p className="error">{error}</p>}

      <div className="lang-tabs">
        {['python', 'c', 'cpp', 'java'].map((l) => {
          const info = langs.find((x) => x.id === l);
          const avail = info ? info.available : true;
          return (
            <button
              key={l}
              className={'lang-tab' + (lang === l ? ' active' : '')}
              disabled={!avail}
              onClick={() => switchLang(l)}
              title={avail ? l : 'toolchain not installed on engine'}
            >
              {l}{avail ? '' : ' ✕'}
            </button>
          );
        })}
      </div>

      <div className="editor-grid">
        <div className="card editor-card">
          <textarea
            className="code-area"
            value={code}
            onChange={(e) => onCode(e.target.value)}
            spellCheck={false}
            placeholder="// code yahan likho"
          />
          <div className="editor-foot">
            <div>
              <label className="muted" style={{ fontSize: 12 }}>stdin</label>
              <textarea
                className="stdin-area"
                value={stdin}
                onChange={(e) => setStdin(e.target.value)}
                placeholder="input (optional)"
                spellCheck={false}
              />
            </div>
            <button className="btn primary" disabled={busy || !code.trim()} onClick={run}>
              {busy ? 'Running…' : '▶ Run'}
            </button>
          </div>
        </div>

        <div className="card output-card">
          <h3 style={{ marginTop: 0 }}>Output</h3>
          {!result && !busy && <p className="muted">Run dabao — result yahan aayega.</p>}
          {busy && <p className="muted">Engine par chal raha hai…</p>}
          {result && (
            <div>
              <div className="verdict-row">
                <span
                  className="verdict"
                  style={{ background: (VERDICT_COLOR[result.verdict] || '#8b93a7') + '22', color: VERDICT_COLOR[result.verdict] || '#8b93a7' }}
                >
                  {result.verdict}
                </span>
                <span className="muted" style={{ fontSize: 12 }}>
                  {result.cpu_ms != null && `${result.cpu_ms} ms`}
                  {result.peak_ram_mb != null && ` · ${result.peak_ram_mb} MB`}
                  {result.exit_code != null && ` · exit ${result.exit_code}`}
                </span>
              </div>
              {result.stdout && (
                <div>
                  <label className="muted" style={{ fontSize: 12 }}>stdout{result.truncated && ' (truncated)'}</label>
                  <pre className="out">{result.stdout}</pre>
                </div>
              )}
              {result.stderr && (
                <div>
                  <label className="muted" style={{ fontSize: 12 }}>stderr</label>
                  <pre className="out err">{result.stderr}</pre>
                </div>
              )}
              {!result.stdout && !result.stderr && <p className="muted">koi output nahi</p>}
            </div>
          )}
        </div>
      </div>

      <style>{`
        .lang-tabs { display: flex; gap: 8px; margin: 14px 0; }
        .lang-tab { padding: 8px 16px; border-radius: 10px; border: 1px solid #232838; background: #141821; color: #c6cddb; cursor: pointer; font-family: monospace; }
        .lang-tab.active { border-color: #7dd3fc; color: #7dd3fc; }
        .lang-tab:disabled { opacity: 0.4; cursor: not-allowed; }
        .editor-grid { display: grid; gap: 14px; }
        @media (min-width: 900px) { .editor-grid { grid-template-columns: 1.2fr 1fr; } }
        .code-area { width: 100%; min-height: 320px; background: #0d1117; color: #e6e9f0; border: 1px solid #232838; border-radius: 10px; padding: 14px; font-family: ui-monospace, monospace; font-size: 14px; line-height: 1.6; resize: vertical; box-sizing: border-box; }
        .stdin-area { width: 100%; min-height: 56px; background: #0d1117; color: #e6e9f0; border: 1px solid #232838; border-radius: 8px; padding: 8px 10px; font-family: ui-monospace, monospace; font-size: 13px; resize: vertical; box-sizing: border-box; margin-top: 4px; }
        .editor-foot { display: flex; gap: 12px; align-items: flex-end; justify-content: space-between; margin-top: 10px; }
        .editor-foot > div { flex: 1; }
        .verdict-row { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
        .verdict { font-family: monospace; font-weight: 700; font-size: 13px; padding: 4px 12px; border-radius: 20px; }
        .out { background: #0d1117; border: 1px solid #232838; border-radius: 8px; padding: 10px 12px; font-size: 13px; white-space: pre-wrap; word-break: break-word; max-height: 300px; overflow: auto; }
        .out.err { color: #fca5a5; }
      `}</style>
    </div>
  );
}
