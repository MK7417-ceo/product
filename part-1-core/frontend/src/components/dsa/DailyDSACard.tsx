import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './DailyDSACard.css';
import { ApiError, dsaApi } from '../../lib/api';
import type { DailyDSAQuestion } from '../../lib/api';

/* Self-contained Daily DSA card for the dashboard right rail.
   Fetches today's question; "Solve →" deep-links to /codelab?date=<date>.
   Solved state is tracked locally (localStorage) since the backend exposes
   no submit-history endpoint — set when /codelab?date=… submit is accepted.
   Green is used ONLY for the solved badge. */

const SOLVED_KEY = 'sf_dsa_solved_v1';

function solvedDates(): string[] {
  try {
    return JSON.parse(localStorage.getItem(SOLVED_KEY) ?? '[]') as string[];
  } catch {
    return [];
  }
}

function difficultyClass(d: string): string {
  const s = (d ?? '').toLowerCase();
  if (s === 'medium') return 'medium';
  if (s === 'hard') return 'hard';
  return 'easy';
}

export interface DailyDSACardProps {
  /** YYYY-MM-DD; defaults to the backend's "today". */
  date?: string;
  className?: string;
}

export function DailyDSACard({ date, className }: DailyDSACardProps) {
  const [question, setQuestion] = useState<DailyDSAQuestion | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [solved, setSolved] = useState(false);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    setError(null);
    dsaApi
      .daily(date)
      .then((q) => {
        if (!alive) return;
        setQuestion(q);
        setLoading(false);
        setSolved(solvedDates().includes(q.date));
      })
      .catch((e) => {
        if (!alive) return;
        setLoading(false);
        setError(e instanceof ApiError ? e.message : 'Failed to load the daily question.');
      });
    return () => {
      alive = false;
    };
  }, [date]);

  return (
    <div className={`dsa-card${className ? ` ${className}` : ''}`} data-testid="daily-dsa-card">
      <div className="kicker">Daily DSA</div>

      {loading && (
        <div className="loading">
          <span className="spin" />
          Picking today&apos;s question…
        </div>
      )}

      {error && <div className="err">{error}</div>}

      {question && (
        <>
          <div className="row">
            <h3>{question.title}</h3>
            {solved ? (
              <span className="dsa-badge solved">✓ Solved</span>
            ) : (
              <span className={`dsa-badge ${difficultyClass(question.difficulty)}`}>
                {question.difficulty}
              </span>
            )}
          </div>
          <div className="dsa-tags">
            {question.topic_tags.map((t) => (
              <span className="dsa-tag" key={t}>
                {t}
              </span>
            ))}
          </div>
          <div className="foot">
            <span className="meta">{question.date}</span>
            <Link className="dsa-solve" to={`/codelab?date=${encodeURIComponent(question.date)}`}>
              Solve →
            </Link>
          </div>
        </>
      )}
    </div>
  );
}

export default DailyDSACard;
