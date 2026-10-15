import type { ReactNode } from 'react';
import type { LangCode } from '../../lib/translations';
import type { DiagramType } from './ConceptDiagram';
import ConceptDiagram from './ConceptDiagram';
import ListenButton from './ListenButton';
import './visual.css';

interface Props {
  title: string;
  /** Markdown-ish content: ##/### headings, **bold**, *italic*, `code`, - bullets, 1. lists, > quotes. */
  content: string;
  lang?: LangCode;
  /** Optional animated diagram shown under the title. */
  diagram?: DiagramType;
  diagramTitle?: string;
  /** false → shows a "Non-coding" badge (for visual/theory topics). Default true. */
  coding?: boolean;
  /** Custom text for the Listen button (defaults to content with markdown stripped). */
  audioText?: string;
  className?: string;
}

/* ---------- tiny markdown-ish renderer (no dependencies) ---------- */

function renderInline(text: string, keyPrefix: string): ReactNode[] {
  // Split on **bold**, *italic*, `code` — keep delimiters.
  const parts = text.split(/(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g);
  return parts.map((p, i) => {
    const key = `${keyPrefix}-i${i}`;
    if (p.startsWith('**') && p.endsWith('**') && p.length > 4) {
      return <strong key={key}>{p.slice(2, -2)}</strong>;
    }
    if (p.startsWith('*') && p.endsWith('*') && p.length > 2) {
      return <em key={key}>{p.slice(1, -1)}</em>;
    }
    if (p.startsWith('`') && p.endsWith('`') && p.length > 2) {
      return <code key={key} className="visual-inline-code">{p.slice(1, -1)}</code>;
    }
    return <span key={key}>{p}</span>;
  });
}

function renderMarkdown(content: string): ReactNode[] {
  const lines = content.split('\n');
  const out: ReactNode[] = [];
  let list: string[] = [];
  let listOrdered = false;

  const flushList = () => {
    if (list.length === 0) return;
    const items = list.map((item, i) => <li key={`li-${out.length}-${i}`}>{renderInline(item, `li-${out.length}-${i}`)}</li>);
    out.push(
      listOrdered ? (
        <ol key={`ol-${out.length}`} className="visual-md-list">{items}</ol>
      ) : (
        <ul key={`ul-${out.length}`} className="visual-md-list">{items}</ul>
      )
    );
    list = [];
  };

  lines.forEach((raw, idx) => {
    const line = raw.trim();
    if (!line) {
      flushList();
      return;
    }
    const bullet = line.match(/^[-*]\s+(.*)$/);
    const numbered = line.match(/^\d+\.\s+(.*)$/);
    if (bullet) {
      if (listOrdered) flushList();
      listOrdered = false;
      list.push(bullet[1]);
      return;
    }
    if (numbered) {
      if (!listOrdered) flushList();
      listOrdered = true;
      list.push(numbered[1]);
      return;
    }
    flushList();
    if (line.startsWith('### ')) {
      out.push(<h4 key={idx} className="visual-md-h4">{renderInline(line.slice(4), `h4-${idx}`)}</h4>);
    } else if (line.startsWith('## ')) {
      out.push(<h3 key={idx} className="visual-md-h3">{renderInline(line.slice(3), `h3-${idx}`)}</h3>);
    } else if (line.startsWith('> ')) {
      out.push(<blockquote key={idx} className="visual-md-quote">{renderInline(line.slice(2), `q-${idx}`)}</blockquote>);
    } else {
      out.push(<p key={idx} className="visual-md-p">{renderInline(line, `p-${idx}`)}</p>);
    }
  });
  flushList();
  return out;
}

/** Strip markdown for clean text-to-speech output. */
export function stripMarkdown(md: string): string {
  return md
    .replace(/^#{1,4}\s+/gm, '')
    .replace(/^>\s+/gm, '')
    .replace(/^[-*]\s+/gm, '')
    .replace(/^\d+\.\s+/gm, '')
    .replace(/(\*\*|__)(.*?)\1/g, '$2')
    .replace(/(\*|_)(.*?)\1/g, '$2')
    .replace(/`([^`]+)`/g, '$1')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

/* ---------- component ---------- */

export default function TheoryCard({
  title,
  content,
  lang = 'en',
  diagram,
  diagramTitle,
  coding = true,
  audioText,
  className = '',
}: Props) {
  return (
    <article className={`visual-theory-card${className ? ` ${className}` : ''}`}>
      <header className="visual-theory-head">
        <div className="visual-theory-titles">
          <h3 className="visual-theory-title">{title}</h3>
          {diagram && (
            <span className="visual-badge visual-badge-visual" title="Includes an animated visual explanation">
              🎨 Visual
            </span>
          )}
        </div>
        <ListenButton text={audioText ?? stripMarkdown(content)} lang={lang} />
      </header>

      {diagram && <ConceptDiagram type={diagram} title={diagramTitle} />}

      <div className="visual-theory-body">{renderMarkdown(content)}</div>
    </article>
  );
}
