import { useEffect, useRef, useState } from 'react';
import { api } from '../lib/api';

/* Global search — modelled on Apple Notes search:
   one field, live results as you type, type-filter chips (like Notes'
   suggested searches such as "Notes with Drawings"), and a snippet that
   shows the matched text in context. Only the signed-in user's own
   content is ever searched (like locked notes staying private). */

export type SearchType = 'roadmap' | 'task' | 'evidence' | 'assessment' | 'certificate';

export interface SearchResultItem {
  type: SearchType;
  id: string;
  title: string;
  snippet: string; // HTML with <mark> around matches — rendered via dangerouslySetInnerHTML
  score: number;
  created_at: string;
}

const FILTERS: Array<{ key: SearchType | 'all'; label: string }> = [
  { key: 'all', label: 'All' },
  { key: 'roadmap', label: 'Roadmaps' },
  { key: 'task', label: 'Tasks' },
  { key: 'evidence', label: 'Evidence' },
  { key: 'assessment', label: 'Assessments' },
  { key: 'certificate', label: 'Certificates' },
];

const TYPE_LABEL: Record<SearchType, string> = {
  roadmap: 'Roadmap',
  task: 'Task',
  evidence: 'Evidence',
  assessment: 'Assessment',
  certificate: 'Certificate',
};

export default function SearchBar() {
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState<SearchType | 'all'>('all');
  const [results, setResults] = useState<SearchResultItem[]>([]);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const boxRef = useRef<HTMLDivElement>(null);
  const debounceRef = useRef<number | undefined>(undefined);

  useEffect(() => {
    const onDocClick = (e: MouseEvent) => {
      if (boxRef.current && !boxRef.current.contains(e.target as Node)) setOpen(false);
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setOpen(false);
    };
    document.addEventListener('mousedown', onDocClick);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('mousedown', onDocClick);
      document.removeEventListener('keydown', onKey);
    };
  }, []);

  const onQueryChange = (value: string) => {
    setQuery(value);
    if (value.trim().length < 2) {
      window.clearTimeout(debounceRef.current);
      setResults([]);
      setLoading(false);
      setOpen(false);
    }
  };

  useEffect(() => {
    const q = query.trim();
    if (q.length < 2) return;
    debounceRef.current = window.setTimeout(async () => {
      setLoading(true);
      try {
        const params = new URLSearchParams({ q, limit: '12' });
        if (filter !== 'all') params.set('types', filter);
        const data = await api<{ results: SearchResultItem[] }>(
          `/api/v1/search?${params.toString()}`,
        );
        setResults(data.results);
        setOpen(true);
      } catch {
        setResults([]);
      } finally {
        setLoading(false);
      }
    }, 250);
    return () => window.clearTimeout(debounceRef.current);
  }, [query, filter]);

  return (
    <div className="sf-search" ref={boxRef}>
      <div className="sf-search-field">
        <span className="sf-search-icon" aria-hidden>⌕</span>
        <input
          value={query}
          onChange={(e) => onQueryChange(e.target.value)}
          onFocus={() => query.trim().length >= 2 && setOpen(true)}
          placeholder="Search roadmaps, tasks, evidence…"
          aria-label="Global search"
        />
        {loading && <span className="sf-search-spinner" aria-hidden />}
        {query && (
          <button
            className="sf-search-clear"
            onClick={() => {
              setQuery('');
              setResults([]);
            }}
            aria-label="Clear search"
          >
            ×
          </button>
        )}
      </div>

      {open && query.trim().length >= 2 && (
        <div className="sf-search-pop">
          <div className="sf-search-filters" role="tablist" aria-label="Result type filter">
            {FILTERS.map((f) => (
              <button
                key={f.key}
                role="tab"
                aria-selected={filter === f.key}
                className={filter === f.key ? 'active' : ''}
                onClick={() => setFilter(f.key)}
              >
                {f.label}
              </button>
            ))}
          </div>

          <div className="sf-search-results">
            {!loading && results.length === 0 && (
              <div className="sf-search-empty">No matches for “{query.trim()}”.</div>
            )}
            {results.map((r) => (
              <div key={`${r.type}:${r.id}`} className="sf-search-hit">
                <span className={`sf-search-tag tag-${r.type}`}>{TYPE_LABEL[r.type]}</span>
                <div className="sf-search-hit-body">
                  <div
                    className="sf-search-hit-title"
                    dangerouslySetInnerHTML={{ __html: r.title }}
                  />
                  {r.snippet && (
                    <div
                      className="sf-search-hit-snippet"
                      dangerouslySetInnerHTML={{ __html: r.snippet }}
                    />
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
